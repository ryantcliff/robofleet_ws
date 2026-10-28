Electrical review checklist
===========================

This is our working checklist for the motor-power review listed as Priority 0
in :doc:`hardware_audit_checklist`. It adds measurement steps and a place to
record results. It is a planning aid, **not** an engineering sign-off: we leave
pass criteria and margins to the qualified reviewer, and nothing here
authorizes driving, braking tests, or changes to pack or controller wiring.

Current state against the hold
------------------------------

.. list-table::
   :widths: 25 75

   * - The documentation says
     - Keep motor power disconnected. Do not reconnect the current 7S pack
       (:doc:`hardware_inventory`, :doc:`hardware_audit_checklist`).
   * - Our robot on 2026-10-28
     - We had the 7S motor battery connected and all four ODESC controllers
       enumerated on USB. The drive stack was not running and its boot service
       was disabled. The robot was on blocks.
   * - Consequence
     - We are not following the hold. We either disconnect the pack, or record
       who accepted the risk, under what conditions and until when, and update
       this documentation either way.

The concern
-----------

* Pack: 7S4P, 25.2 V nominal, 29.4 V at full charge, BMS 40 A continuous and
  60 A peak (from labels).
* The inspected RL controller's power MOSFET is marked JMTG3002B, identified as
  30 V drain-source absolute maximum. **Confirm against the current
  manufacturer datasheet** (item A1). The other three boards are identical to
  it, but we have not yet photographed them individually.
* Headroom at full charge is 0.6 V before switching spikes and regeneration.
* The gate driver's 6-60 V range does not rate the assembled board.
* The driving demonstration of more than 30 minutes that we were told about
  shows the robot worked under unknown conditions. It does not show safety at
  full charge.

Stage A: de-energized
---------------------

Battery disconnected, discharge connector open.

.. list-table::
   :header-rows: 1
   :widths: 6 50 44

   * - #
     - Item
     - How
   * - A1
     - Datasheet: JMTG3002B drain-source absolute maximum and avalanche rating
     - Manufacturer PDF, saved with date
   * - A2
     - ODESC V4.2 vendor-stated maximum supply voltage, and which variant (24 V or 48 V)
     - Vendor page, board silkscreen
   * - A3
     - Photograph the power MOSFETs on the FL, FR and RR boards (only RL has been photographed)
     - Heat sink off, close-up of top marking
   * - A4
     - Bus capacitor voltage rating and count per board
     - Read markings (100 uF 63 V was seen; that is not a board rating)
   * - A5
     - Fuse ratings and positions: Jetson branch, four ODESC branches, main
     - Read and label, photograph
   * - A6
     - Wire gauge, polarity, connector condition, strain relief
     - Visual
   * - A7
     - Does a master disconnect or physical e-stop exist, and where
     - Trace the power path
   * - A8
     - Braking resistors (four, 2 ohm / 50 W): continuity, terminal assignment, mounting and heat sinking
     - Meter, visual
   * - A9
     - RL heat sink reattached with a suitable thermal interface
     - Visual
   * - A10
     - Pack label, BMS model, cell-level protection per datasheet
     - Documents only; do not open the pack

We record the result, date and tester for each item.

Stage B: energized, idle, no motion
-----------------------------------

Needs a calibrated meter (ideally a logging or oscilloscope capture) and a
second person. Probe only accessible terminals, and not the gate-driver area.

.. list-table::
   :header-rows: 1
   :widths: 6 50 44

   * - #
     - Item
     - How
   * - B1
     - Pack rest voltage
     - Meter at the XT90
   * - B2
     - State of charge at test time, so results map to the 29.4 V case
     - Same reading plus any BMS gauge
   * - B3
     - Input voltage at each ODESC (four readings)
     - Meter at the board input
   * - B4
     - Firmware-reported bus voltage per board compared with the meter
     - Compare with the results log
   * - B5
     - Bus ripple and noise at idle
     - Oscilloscope, if available
   * - B6
     - Jetson 3S supply: LM2596 output at no load, under real load, and at 3S low and full
     - Meter, supervised
   * - B7
     - Heating at fuses, connectors and regulators after 10 minutes idle
     - Touch or IR thermometer with power off

Stage C: deceleration and regeneration
--------------------------------------

**Not authorized; a reviewer decision is required.** Prerequisites: all of
Stage A and Stage B complete; the reviewer sets the maximum acceptable bus
voltage and who is present; wheels off the ground; a hardware power cut within
reach; a capture instrument on the bus.

.. list-table::
   :header-rows: 1
   :widths: 6 94

   * - #
     - Item
   * - C1
     - Peak bus voltage during the most aggressive stop the software can command (50 turns/s^2) from joystick top speed
   * - C2
     - Same, with the pack at full charge (worst case)
   * - C3
     - Braking resistor behavior and temperature, and whether the ODESC brake-resistor setting matches the fitted 2 ohm part
   * - C4
     - USB drop behavior when the motors energize (source comments report ODrives dropping off USB)

Firmware readings
-----------------

We read each controller over USB with the Python API, reading only
(``vbus_voltage``, error registers, brake and bus settings), with no error
clearing, configuration writes or state requests. This gives the bus voltage as
each board sees it. Its accuracy is unknown, so we cross-check it against items
B3 and B4, and it does not replace the meter.

Results log
-----------

On 2026-10-28 we read all four controllers over USB with the battery connected
and the drive stack not running, taking eight samples over four seconds per
board.

.. list-table::
   :header-rows: 1
   :widths: 14 36 50

   * - Board
     - Bus voltage min / mean / max (V)
     - State and errors
   * - FL
     - 27.97 / 27.97 / 27.99
     - Idle; axis, motor, encoder, controller errors all 0
   * - FR
     - 28.10 / 28.11 / 28.12
     - Same
   * - RL
     - 27.80 / 27.81 / 27.82
     - Same
   * - RR
     - 28.15 / 28.16 / 28.17
     - Same

All four boards report firmware 0.5.6 on hardware 3.6.24, and the same
settings as loaded: brake resistor enabled **False**, configured brake
resistance 0.47 ohm, ``dc_max_negative_current`` -5.0 A, DC bus overvoltage
trip **32.0 V**, undervoltage trip 18.0 V, bus current 0.0 A.

These are firmware values, not meter measurements. What we noticed:

#. **The overvoltage trip (32 V) is above the 30 V MOSFET absolute maximum**
   (the rating is confirmed in the datasheet, item A1). The firmware protection
   therefore trips only after the transistors' limit. The ODrive 0.5.6 documentation
   gives 26 V as the default for the 24 V board, so someone raised the trip
   level to 32 V, probably so the boards would run on the 29.4 V pack. We have
   not changed it.
#. **The brake resistor is disabled in firmware, and the configured resistance
   (0.47 ohm) does not match the fitted 2 ohm / 50 W parts** (items A8, C3; A8 has since confirmed the resistors are fitted and
   read 2 ohm).
   With it disabled, regeneration has no resistor to dump into and goes back to
   the pack, limited by ``dc_max_negative_current`` and by what the BMS and
   connector will accept. Whether the discharge port accepts charge current is
   not known.
#. Bus voltage at rest was about 27.8 to 28.2 V, consistent with a partly
   charged 7S pack. Full charge reaches 29.4 V, and regeneration adds to either.
   The 0.35 V spread between boards at zero current suggests differences in ADC
   calibration, not real voltage drops; confirm with items B3 and B4.
#. A reading of zero errors is not evidence of a clean history: our drive
   stack cleared the stored errors when it started earlier that day.

Braking resistors (item A8)
---------------------------

On 2026-10-28 we checked the four braking resistors with the pack
disconnected. **A8 is confirmed:** all four resistors are connected, and each
reads 2 ohm, as labelled.

This did not match the controller settings we read earlier, where the brake
resistor was disabled and the configured resistance was 0.47 ohm.

On 2026-10-28, with the robot on blocks, the battery connected and the drive
stack not running, we changed exactly two settings on each of the four
controllers, one board at a time: ``brake_resistance`` from 0.47 to 2.0 ohm and
``enable_brake_resistor`` from False to True. We saved each configuration (the
board reboots) and read it back. On every board only those two settings
differed afterwards, and the board was idle with no errors. The original values
are kept so the change can be reversed.

We did not change ``max_regen_current`` (0 A), ``dc_max_negative_current``
(-5 A), the overvoltage ramp (disabled, and we are leaving it that way: the
ODrive documentation warns that a ramp start below the normal bus voltage
overheats the brake resistor), the 32 V overvoltage trip, or any motor setting.
With ``max_regen_current`` at 0, regenerated current now goes to the resistors
instead of back to the pack. The 50 W rating of the resistors for short, hard
stops is still an open question for the reviewer, and we have not run a braking
test (Stage C).

Stage A status
--------------

Where each Stage A item stands as of 2026-10-28.

.. list-table::
   :header-rows: 1
   :widths: 8 22 70

   * - Item
     - Status
     - Evidence
   * - A1
     - Confirmed
     - The JMTG3002B datasheet (JieJie, version 1.2, as hosted by several
       distributors; we did not check the manufacturer's own site) gives a
       drain-source absolute maximum of **30 V**, a minimum breakdown voltage of
       30 V, 120 A continuous at 25 C case temperature, and 240 mJ single-pulse
       avalanche energy.
   * - A2
     - Researched, not confirmed
     - We found no manufacturer datasheet. Seller listings for the Flipsky
       "ODESC V4.2 24V" describe an 8 to 24 V working range (the 56 V variant is
       listed at 8 to 56 V), and some listings conflict. Our pack rests at about
       28 V and charges to 29.4 V, above that listed range.
   * - A3 to A7
     - Not performed
     - MOSFET photographs for FL, FR and RR, bus capacitor ratings, fuse
       ratings, wiring condition, and the master disconnect and physical stop.
   * - A8
     - Confirmed
     - See the section above.
   * - A9, A10
     - Not performed
     - RL heat sink reattachment, and the pack and BMS protection details.

An item marked "Not performed" has not been checked and is not a pass.

Decision outcomes
-----------------

The reviewer chooses; none is preselected.

* **Rated:** the boards are rated for the 29.4 V case with documented margin.
  Record the evidence, update the documentation, keep the pack.
* **Not rated:** choose a mitigation (a charge ceiling, compatible controllers,
  or a power-architecture change). We prefer to keep the pack,
  controllers and chassis, so any change needs a full review of regeneration,
  peak current, BMS limits and fusing. Do not use a dropper resistor, diodes,
  an uneven cell tap, firmware voltage limits or partial charge as a permanent
  fix.
* **Unknown:** keep the drive stack disabled, and the battery disconnected when
  the robot is not under supervision.
