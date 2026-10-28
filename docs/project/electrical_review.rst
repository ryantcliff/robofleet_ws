Motor power review
==================

These are our notes on whether the four motor controllers can run safely off
our 7S battery pack. They cover what worries us, what we checked, what we
changed, and what is left. The numbers are real. Where we did not check
something, we say so.

The problem
-----------

* The pack is a HOT PAXX 7S4P: 25.2 V nominal, **29.4 V full**, with a BMS rated
  40 A continuous and 60 A peak (from the label).
* The power MOSFET we inspected on the RL controller is a JMTG3002B. Its
  datasheet says **30 V absolute maximum** drain-source. The other three
  controllers are identical to it, but we have not looked at their markings.
* At full charge that is 0.6 V of room before any switching spike or braking
  surge.
* The controllers are 24 V boards (24 V QC stickers). Seller listings for the
  "ODESC V4.2 24V" give an 8 to 24 V working range, and the pack sits at about
  28 V. We found no manufacturer datasheet to confirm the range.
* The driver chip's 6 to 60 V rating is not a rating for the whole board.
* The robot was driven for more than 30 minutes before our team inherited it. That shows it
  works in some conditions, not that it is safe at full charge.

Where we are
------------

We are still using the stock pack and controllers. The earlier version of these
docs said to keep the motor battery disconnected. We are not doing that: on
October 28 we connected the battery and ran things with the robot up on blocks,
and then unplugged it again.

Right now the drive service is turned off and the battery is unplugged. We
have not changed anything to fix the voltage margin. The ways to deal with it
are listed at the bottom of this page.

What we checked
---------------

.. list-table::
   :header-rows: 1
   :widths: 8 26 66

   * - Item
     - Status
     - What we found
   * - A1
     - Confirmed
     - The JMTG3002B datasheet (JieJie, version 1.2, copies from distributors;
       we did not check the manufacturer's site) says 30 V absolute maximum,
       30 V minimum breakdown, 120 A continuous at 25 C case temperature, and
       240 mJ single-pulse avalanche energy. This applies to the other three
       controllers only because they are identical: they report the same
       hardware (3.6.24) and firmware (0.5.6) versions, but we have not read a
       MOSFET marking on them.
   * - A2
     - Researched, not confirmed
     - No manufacturer datasheet. Seller listings for the Flipsky "ODESC V4.2
       24V" say 8 to 24 V, and the 56 V version 8 to 56 V. The listings
       disagree in places.
   * - A5
     - Checked
     - Four yellow blade fuses marked 20 (20 A) for the motor controllers, and
       one orange blade fuse marked 5 (5 A) for the Jetson. There is no main
       fuse between the battery and the motor fuse block. We read the printed
       numbers and measured nothing. Blade fuses are commonly rated 32 V DC, so
       we should confirm the rating of ours.
   * - A6
     - Checked
     - The battery cable is 10 AWG, marked 200 C, red on positive and black on
       negative. No melting, discoloration or burnt odor. Nothing moved
       when we tugged the wires at the fuse block, and the cable is held in
       place near the block. This was a visual inspection only.
   * - A7
     - Checked; none exists
     - There is no master disconnect, breaker, switch or physical stop in the
       motor power path. Unplugging the XT90 is the only way to cut motor power.
   * - A8
     - Confirmed
     - See the braking resistor section below.
   * - A9
     - Checked
     - The RL controller's heat sink is back on. We did not check the thermal
       paste or how tight it is.
   * - A10
     - Label read only
     - The label reads: BMS ChangFa 40 A; discharge 40 A continuous, 60 A peak,
       19 V minimum; 25.2 V, 20 Ah (504 Wh); EVE 21700 50E cells, 7S4P; XT90
       discharge port; XT60 charge port; charge at 29.4 V, up to 5 A. It does not
       say what protections the BMS has (overvoltage, short circuit and so on),
       and we have not found a BMS datasheet. It also does not say whether the
       discharge port will take charge current from motor braking.

We are not doing the rest of Stage A. That was reading the MOSFET markings on the other three
MOSFETs and recording the bus capacitor ratings. The item numbers still skip
those, so the references in the other pages stay correct.

What we read from the controllers
---------------------------------

On October 28 we read all four controllers over USB, with the battery connected
and the drive stack off, and wrote nothing to them. These are the controllers'
own readings, not meter measurements.

.. list-table::
   :header-rows: 1
   :widths: 14 36 50

   * - Board
     - Bus voltage, min / mean / max (V)
     - State
   * - FL
     - 27.97 / 27.97 / 27.99
     - Idle. All error registers 0.
   * - FR
     - 28.10 / 28.11 / 28.12
     - Same
   * - RL
     - 27.80 / 27.81 / 27.82
     - Same
   * - RR
     - 28.15 / 28.16 / 28.17
     - Same

All four were on firmware 0.5.6 (hardware 3.6.24) and had the same settings
before we changed anything: brake resistor off, brake resistance 0.47 ohm,
``dc_max_negative_current`` -5 A, ``max_regen_current`` 0 A, overvoltage trip
**32 V**, undervoltage trip 18 V, overvoltage ramp off, bus current 0 A. Motor
current limit was 10.5 A. The only difference between boards was RR's motor
calibration voltage setting (2 V, the others 10 V).

Observations:

#. **The overvoltage trip is 32 V, above the transistors' 30 V rating.** The
   ODrive 0.5.6 documentation gives 26 V as the default for the 24 V board, so
   someone raised it, probably so the boards would run on the 29.4 V pack. We
   have not changed it.
#. The resting bus voltage is about 28 V, roughly 4.0 V per cell, so the pack is
   partly charged. A full pack is 29.4 V (4.2 V per cell). During regenerative
   braking the bus voltage rises above its resting value.
#. The four boards disagree by up to 0.35 V with no bus current flowing. With
   0 A there is no resistive drop to explain that, so we suspect differences in
   each board's ADC gain or offset. A meter reading (B3, B4) will settle it.
#. A reading of zero errors does not show a clean history. Our drive stack
   calls ``clear_errors()`` when it connects, and it did so earlier that day.

Braking resistors
-----------------

All four 2 ohm / 50 W resistors are connected and each measures 2 ohm, so
**A8 is confirmed**.

Regenerative braking works like this. When a controller decelerates a motor, the
motor acts as a generator and pushes current back onto the DC bus. If nothing
absorbs it, the bus voltage rises until the overvoltage trip. A brake resistor
absorbs the energy as heat: the firmware switches it across the bus with a duty
cycle, and ``max_regen_current`` sets how much current may flow back to the
supply before the resistor starts to take over.

Before our change the resistor was disabled, with ``brake_resistance`` left at
0.47 ohm, which does not match our parts. All regenerated current therefore had
only one place to go: the pack. That path is limited by ``dc_max_negative_current``
(-5 A) and by whatever the BMS will accept. The pack label lists 5 A as the
maximum charge current, on the separate XT60 charge port, and says nothing about
charging through the discharge port.

On October 28, with the robot on blocks, the battery connected and the drive
stack off, we changed two settings on each controller, one board at a time:
``brake_resistance`` from 0.47 to 2.0 ohm and ``enable_brake_resistor`` from
False to True. We saved each configuration (the board reboots) and read it back.
After each change only those two settings differed, and the board was idle with
no errors. We kept the previous values so the change can be reverted.

We did not change ``max_regen_current`` (0 A), ``dc_max_negative_current``
(-5 A), the overvoltage ramp, the 32 V trip, or any motor setting. The ramp
stays off on purpose: the ODrive documentation warns that a ramp start below the
normal bus voltage drives the brake duty up immediately and overheats the
resistor. With ``max_regen_current`` at 0 A, all regenerated current now goes to
the resistors instead of back to the pack.

We have not run a braking test. With the brake switch fully on, a 2 ohm
resistor across 28 V dissipates V^2/R, about 390 W (roughly 14 A), and about
430 W at 29.4 V. The resistors are rated 50 W, so they depend on a low duty
cycle or short pulses, and a hard stop could exceed their rating. We do not
know their pulse rating.

What is still open
------------------

**Meter readings (not done).** We want these taken with a meter by two people,
touching only accessible terminals and staying out of the gate-driver area:

.. list-table::
   :header-rows: 1
   :widths: 8 56 36

   * - #
     - What
     - How
   * - B1
     - Pack voltage at rest
     - Meter at the XT90
   * - B2
     - State of charge at the time of the test
     - Same reading, plus any BMS gauge
   * - B3
     - Voltage at each controller's input (four readings)
     - Meter at the board input
   * - B4
     - Each controller's own bus voltage reading against the meter
     - Compare with the table above
   * - B5
     - Bus ripple at idle
     - Oscilloscope, if we get one
   * - B6
     - Jetson supply: LM2596 output at no load, under real load, and at low and full 3S
     - Meter
   * - B7
     - Temperature at fuses, connectors and regulators after 10 minutes idle
     - Touch or IR thermometer, with the power off

**Braking test (not done).** Before attempting a hard stop we want:

* the wheels off the ground;
* someone positioned to disconnect the XT90, since that is the only way to cut
  power;
* a meter or oscilloscope on the bus to capture the peak voltage;
* a limit for the highest bus voltage we are willing to accept.

We would then measure the peak bus voltage on the hardest stop the software can
command (``FAST_DECEL`` of 50 turns/s^2) from top joystick speed, with the pack
both partly charged and full. We would also watch the resistor temperature, and
whether the controllers drop off USB when the motors energize (comments in our
code say they have).

Options
-------

* **The boards are adequate at 29.4 V.** We record how we know, using the
  datasheet or a manufacturer statement and the measured peak bus voltage, and
  we keep the pack.
* **They are not adequate.** We choose a mitigation. We would like to keep the
  pack, controllers and chassis, so the candidates are a lower charge ceiling,
  controllers rated for the pack voltage, or a change to the power architecture.
  Any of these has to account for regenerative energy, peak current, BMS limits
  and fusing. A dropper resistor, diodes, an uneven cell tap, firmware voltage
  limits or simply charging less should not be relied on as a permanent fix.
* **We do not know yet.** This is the current state, and the drive service stays
  off.

Physical stop
-------------

There is no physical disconnect. Motor power can only be removed by unplugging
the XT90. The software e-stop sets each axis to IDLE, so the motors freewheel and
nothing brakes the robot actively. Requirement R-7 asks for a rapid means to stop
FleetBot motion. An inline switch or contactor rated for the pack (40 A
continuous, 60 A peak, 29.4 V) would provide one, and it would be our most
valuable single mitigation.
