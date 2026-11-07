Communications: RoboBeacon, Jetson and home station
==================================================

This describes inherited hardware and implemented interfaces, not an
end-to-end field-tested radio system. The current delivery requires one
FleetBot following a RoboBeacon; home-station functions are optional.

RoboBeacon GPS over HC-12
-------------------------

The inherited beacon uses a SparkFun/u-blox NEO-M8P-2 GPS receiver and an HC-12
serial radio. The receiver on the FleetBot feeds the Jetson's
`/dev/ttyTHS1` and publishes `/gps/beacon/fix`.

The documented bench connection is:

.. code-block:: text

   NEO-M8P UART1 TX ----> HC-12 RXD
   NEO-M8P GND ---------> HC-12 GND (shared)
   5 V power bank ------> NEO-M8P USB power and HC-12 VCC

Check the **actual board markings, voltage limits and logic levels** before
connecting wires. The HC-12 SET pin is normally left unconnected in this
inherited setup. The assumed link settings are 9600 baud, channel 001, FU3
on both ends; verify them on the devices rather than assuming factory settings.

The repository's setup script configures the NEO-M8P's UART1 to emit
GGA sentences only at 5 Hz, at 9600 baud, and requests persistent storage.

.. code-block:: bash

   python3 src/beacon_pkg/scripts/configure_beacon_gps.py /dev/ttyACM0 --check

Only after identifying the correct USB serial port and confirming the
intended receiver/configuration should the non-check setup command be
considered. The check mode is for inspection; reconfiguration writes device
settings. See :doc:`../project/robobeacon_plan` for remaining beacon work.

Optional Meshtastic equipment
-----------------------------

The inherited Meshtastic nodes are LILYGO T-Beams. These IDs are historical
configuration references, not verified live-discovery results:

.. list-table::
   :header-rows: 1
   :widths: 18 28 54

   * - Label
     - Node ID
     - Role
   * - ROBT
     - `!6c73d700`
     - USB-connected robot radio (`/dev/meshtastic`), onboard GPS off
   * - HOME
     - `!6c743480`
     - Optional home station; GPS and smart position broadcasts
   * - TOM
     - `!bb80e074`
     - Handheld paired with the operator's phone

Channel 0 has historically been called `roboflock`. The channel-position
precision is configured to 32 bits; the separate `fromJetson` channel
carries robot status. **Do not publish the private channel key.** The
historical local key-file *path* is
`~/.config/roboflock/meshtastic_primary_psk.b64`; the file itself is
not part of this repository. Internal historic identifiers are deliberately
left unchanged.

The source currently expects a Meshtastic Python dependency matching the
inherited setup (historically `meshtastic==2.7.11`); verify the actual
installed version and compatibility before updating it.

Commands and message flow
-------------------------

With the optional station bridge enabled, home positions are received on
`/home/fix`, mode commands on `/station/command`, and robot telemetry
on `/robot/status`. The implemented modes include `follow`, `home`,
`stop` and `status`. Return-home is outside the current acceptance scope.

The GPS-to-goal and command-control pipelines are documented at
:doc:`beacon_following` and :doc:`control_safety`. Test loss of messages
and watchdog behavior before operating outdoors. HC-12 radio range and
regulatory compliance are **not yet verified**; see
:doc:`../project/robobeacon_plan`.
