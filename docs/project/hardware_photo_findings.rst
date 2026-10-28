Hardware photo findings — October 28, 2026
===========================================

These observations come from the photographs we took while inspecting the
robot. We do not publish the raw photographs here.

Controller identification
-------------------------

We confirmed that four **distinct** ODESC V4.2 motor controllers are
shown, in upload order:

.. list-table::
   :header-rows: 1

   * - Location
     - Photograph
   * - Front-left (FL)
     - IMG_0785.jpeg
   * - Front-right (FR)
     - IMG_0786.jpeg
   * - Rear-left (RL)
     - IMG_0787.jpeg
   * - Rear-right (RR)
     - IMG_0788.jpeg

Visible board markings include ODESC V4.2, 24 V QC stickers, 100 uF / 63 V
capacitors, USB-C ports, terminals labeled motor A/C/B and DC +/-, and
terminals labeled AUX +/- . Orange aluminum resistor housings are marked
50W 2RJ, consistent with 2 ohms / nominal 50 W. These markings do not
establish actual controller input voltage limits, correct resistor
wiring, or adequate resistor heatsinking.

.. warning::

   The HOT PAXX seven-series battery can reach 29.4 V fully charged,
   above the documented operating limit of some 24 V ODESC variants.
   Keep motor power disconnected until each board's permitted input
   voltage and power/braking installation have been verified.

Mechanical evidence
-------------------

* IMG_0789: Zeee 3S LiPo pack and balance connector.
* IMG_0790: pneumatic tire marked 4.10/3.50-4, air valve, metal rim.
  Replace the older unverified description of nylon tires.
* IMG_0791: custom-looking wheel hub adapter, metal clamping collar and
  printed-looking support bracket. Material, retention and whether the
  gearbox shaft bears vehicle wheel loads remain unknown.
* IMG_0792-IMG_0793: aluminum T-slot extrusion frame, 3D-printed-looking
  brackets, open electronics tray and exposed cables.
* IMG_0794: front sensor assembly with three blue circuit boards on a
  custom-looking housing; exact electronics and pin assignments unverified.
* IMG_0795-IMG_0798: further chassis/enclosure dimension views, top-mounted
  LiDAR, and front/rear drive assembly views. Exact dimensions require
  direct, consistent measurement.

Prioritize controller electrical ratings, resistors, fuses and physical
motor stop before drive tests. Verify wheel-to-shaft retention and support
bearing arrangements before outdoor travel. Exposed boards/tray are
not evidence of R-6 weather compliance.

See the companion hardware audit checklist for pending tests.


RL underside identification - October 28, 2026
-----------------------------------------------

A close-up of the rear-left (RL) controller shows the marking JMT G3002B
on multiple power-stage components. This corresponds to the JieJie
Microelectronics JMTG3002B N-channel power MOSFET. Manufacturer
documentation specifies a **30 V absolute-maximum drain-source voltage**.
We subsequently confirmed that **all four controllers are identical
hardware**. Thus the RL MOSFET identification is the working power-stage
identification for FL, FR, RL and RR as well. Only the RL MOSFET
markings were directly photographed in close-up; the other three have
not been individually inspected at the component-marking level.

The present HOT PAXX 7S motor pack is specified as 29.4 V fully
charged. That provides only 0.6 V below the transistor's absolute
maximum, even before switching and regenerative-braking transients.
There is no acceptable engineering voltage margin for directly
powering these four identical controllers from the current pack. The
24V QC marking is consistent with a low-voltage ODESC variant.

Keep the motor battery disconnected pending a reviewed compatible
power architecture. The RL heat sink was removed for inspection;
restore and verify its thermal interface before future operation.

Reference: JieJie Microelectronics JMTG3002B datasheet, version 1.4.
https://e-nexty.dxp.nexty-ele.com/product_files/download?maker_code=JJM&product_part_number=JMTG3002B&product_file_id=5467845&product_id=6198730&lc_code=ja&search_log_id=4389931
