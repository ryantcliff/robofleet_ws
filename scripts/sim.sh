#!/usr/bin/env bash
# Run the hardware-free simulation and tests over SSH, safely side by side
# with other people doing the same on this Jetson.
#
#   scripts/sim.sh test [all|nav|nav-local|nav-gps|beacon|follow|unit]
#   scripts/sim.sh gazebo [launch args...]   Gazebo + SLAM + Nav2, headless, Foxglove on
#   scripts/sim.sh teleop <domain>           drive a running sim from another terminal
#   scripts/sim.sh shell <domain>            ros2 CLI shell attached to a running sim
#   scripts/sim.sh list                      who is simulating, on which domain/port
#
# Each run takes its own ROS domain (20-80) and Gazebo partition, so it never
# sees the real robot (domain 0) or anyone else's run. Logs: /tmp/robofleet-sim/
set -eo pipefail

WS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE=/tmp/robofleet-sim
DOMAIN_MIN=20
DOMAIN_MAX=80
FOXGLOVE_BASE=8765

die() { echo "sim.sh: $*" >&2; exit 1; }

ros_env() {
  [ -f /opt/ros/humble/setup.bash ] || die "ROS 2 Humble not found in /opt/ros/humble"
  [ -f "$WS/install/setup.bash" ] || die "workspace not built. Run:
  cd $WS && source /opt/ros/humble/setup.bash && colcon build --symlink-install --executor sequential"
  set +u
  # shellcheck disable=SC1091
  source /opt/ros/humble/setup.bash
  # shellcheck disable=SC1091
  source "$WS/install/setup.bash"
  export ROS_LOCALHOST_ONLY=1
}

# Take the first free domain. The lock is held by this shell's fd 9 and is
# released automatically when the run ends, even if the SSH session drops.
claim_domain() {
  mkdir -p "$STATE" && chmod 1777 "$STATE" 2>/dev/null || true
  local d
  for ((d = DOMAIN_MIN; d <= DOMAIN_MAX; d++)); do
    exec 9>>"$STATE/domain-$d.lock" || continue
    if flock -n 9; then
      : > "$STATE/domain-$d.lock"
      printf '%s pid=%s since=%s port=%s cmd=%s\n' "${USER:-$(id -un)}" "$$" \
        "$(date +%H:%M)" "$((FOXGLOVE_BASE + d - DOMAIN_MIN))" "$*" >> "$STATE/domain-$d.lock"
      DOMAIN=$d
      FOXGLOVE_PORT=$((FOXGLOVE_BASE + d - DOMAIN_MIN))
      RUN_DIR="$STATE/${USER:-$(id -un)}/$(date +%Y%m%d-%H%M%S)-d$d"
      mkdir -p "$RUN_DIR"
      export ROS_DOMAIN_ID=$DOMAIN ROS_LOG_DIR="$RUN_DIR/ros"
      export IGN_PARTITION="${USER:-$(id -un)}_$DOMAIN"
      return
    fi
    exec 9>&-
  done
  die "all domains $DOMAIN_MIN-$DOMAIN_MAX are busy (see: scripts/sim.sh list)"
}

attach() {
  local d="$1"
  [[ "$d" =~ ^[0-9]+$ ]] || die "usage: scripts/sim.sh $2 <domain>   (domains in use: scripts/sim.sh list)"
  ros_env
  export ROS_DOMAIN_ID="$d" IGN_PARTITION="${USER:-$(id -un)}_$d"
}

run_test() {
  local name="$1"; shift
  echo "---- $name (domain $DOMAIN)"
  if "$@"; then echo "---- $name: PASS"; return 0; fi
  # Two Nav2 stacks starting at once on the Jetson can drop a lifecycle
  # service reply ("change_state (timeout)") and stall. Retry once, loudly.
  echo "---- $name failed; retrying once (often CPU load from other runs: scripts/sim.sh list)"
  if "$@"; then echo "---- $name: FLAKY (passed on retry; first attempt's log was overwritten)"; return 0; fi
  echo "---- $name: FAIL (logs in $RUN_DIR)"; return 1
}

cmd_test() {
  local which="${1:-all}" failed=0
  ros_env
  claim_domain "test $which"
  local py="python3" s="$WS/src"
  local d=(--domain-id "$DOMAIN")
  case "$which" in
    all|nav)       run_test nav       $py "$s/bring_up/scripts/nav2_smoke_test.py" "${d[@]}" --log "$RUN_DIR/nav.log" || failed=1 ;;&
    all|nav-local) run_test nav-local $py "$s/bring_up/scripts/nav2_smoke_test.py" "${d[@]}" --localization local --log "$RUN_DIR/nav-local.log" || failed=1 ;;&
    all|nav-gps)   run_test nav-gps   $py "$s/bring_up/scripts/nav2_smoke_test.py" "${d[@]}" --localization gps --log "$RUN_DIR/nav-gps.log" || failed=1 ;;&
    all|beacon)    run_test beacon    $py "$s/beacon_pkg/scripts/beacon_smoke_test.py" "${d[@]}" --log "$RUN_DIR/beacon.log" || failed=1 ;;&
    all|follow)    run_test follow    $py "$s/bring_up/scripts/follow_smoke_test.py" "${d[@]}" --beacon-speed 1.2 --log "$RUN_DIR/follow.log" || failed=1 ;;&
    all|unit)      run_test unit      $py -m pytest -q "$s/bring_up/test" "$s/urdf_description/test/test_urdf_frames.py" \
                     -k 'not flake8 and not pep257 and not copyright' || failed=1 ;;
    nav|nav-local|nav-gps|beacon|follow) ;;
    *) die "unknown test '$which' (all|nav|nav-local|nav-gps|beacon|follow|unit)" ;;
  esac
  [ "$failed" = 0 ] && echo "All requested tests passed. Logs: $RUN_DIR" || { echo "Some tests failed. Logs: $RUN_DIR"; exit 1; }
}

cmd_gazebo() {
  ros_env
  ros2 pkg prefix ros_gz_sim >/dev/null 2>&1 || die "Gazebo is not installed. Ask someone with sudo to run:
  sudo apt install ros-humble-ros-gz ros-humble-foxglove-bridge
(The headless tests still work without it: scripts/sim.sh test)"
  local foxglove=false
  ros2 pkg prefix foxglove_bridge >/dev/null 2>&1 && foxglove=true
  local avail_mb
  avail_mb=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
  [ "$avail_mb" -lt 2000 ] && echo "WARNING: only ${avail_mb} MB RAM free; Gazebo + Nav2 needs ~2 GB. Someone else may be simulating (scripts/sim.sh list)."
  claim_domain "gazebo $*"
  cat <<EOF
================================================================
 Simulation on ROS domain $DOMAIN   logs: $RUN_DIR
 Drive it (new SSH terminal):   $WS/scripts/sim.sh teleop $DOMAIN
 ros2 CLI  (new SSH terminal):  $WS/scripts/sim.sh shell $DOMAIN
EOF
  if [ "$foxglove" = true ]; then cat <<EOF
 View it: on YOUR computer run
     ssh -N -L $FOXGLOVE_PORT:localhost:$FOXGLOVE_PORT ${USER:-$(id -un)}@$(hostname -I | awk '{print $1}')
   then open https://app.foxglove.dev -> Open connection -> ws://localhost:$FOXGLOVE_PORT
EOF
  else echo " (foxglove_bridge not installed: no browser view, CLI only)"; fi
  echo " Stop: Ctrl+C"
  echo "================================================================"
  ros2 launch bring_up sim.launch.py headless:=true foxglove:="$foxglove" \
    foxglove_port:="$FOXGLOVE_PORT" "$@" 2>&1 | tee "$RUN_DIR/launch.log"
}

cmd_list() {
  shopt -s nullglob
  local f any=0
  for f in "$STATE"/domain-*.lock; do
    if ! flock -n "$f" true 2>/dev/null; then
      any=1; echo "domain $(basename "$f" .lock | cut -d- -f2): $(cat "$f")"
    fi
  done
  [ "$any" = 1 ] || echo "No simulations running."
}

case "${1:-}" in
  test)   shift; cmd_test "$@" ;;
  gazebo) shift; cmd_gazebo "$@" ;;
  teleop) attach "${2:-}" teleop; echo "Driving the sim on domain $ROS_DOMAIN_ID"
          exec ros2 run teleop_twist_keyboard teleop_twist_keyboard ;;
  shell)  attach "${2:-}" shell
          # ~/.bashrc forces ROS_DOMAIN_ID=0 (the real robot), so re-apply after it.
          exec bash --rcfile <(printf 'source ~/.bashrc\nsource %q\nsource %q\nexport ROS_DOMAIN_ID=%q ROS_LOCALHOST_ONLY=1 IGN_PARTITION=%q\nPS1="(sim d%s) $PS1"\necho "Attached to sim on domain %s. exit to leave."\n' \
            /opt/ros/humble/setup.bash "$WS/install/setup.bash" "$ROS_DOMAIN_ID" "$IGN_PARTITION" "$ROS_DOMAIN_ID" "$ROS_DOMAIN_ID") -i ;;
  list)   cmd_list ;;
  *) sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
