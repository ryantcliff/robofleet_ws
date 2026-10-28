Hardware photo findings — October 28, 2026
==========================================

What we saw in the photos we took while inspecting the robot. We do not publish
the raw photos here.

Which controller is which
-------------------------

The photos show four separate ODESC V4.2 motor controllers. In the order we
uploaded them:

.. list-table::
   :header-rows: 1

   * - Location
     - Photo
   * - Front-left (FL)
     - IMG_0785.jpeg
   * - Front-right (FR)
     - IMG_0786.jpeg
   * - Rear-left (RL)
     - IMG_0787.jpeg
   * - Rear-right (RR)
     - IMG_0788.jpeg

We can read these markings: ODESC V4.2, 24 V QC stickers, 100 uF / 63 V
capacitors, USB-C ports, terminals labeled motor A/C/B and DC +/-, and
terminals labeled AUX +/-. The orange aluminum resistor housings say 50W 2RJ,
which fits a 2 ohm, 50 W part. None of these markings tell us the controller's
real input voltage limit, whether the resistors are wired right, or whether
they have enough heat sinking.

.. warning::

   The HOT PAXX 7S pack reaches 29.4 V fully charged, which is above the
   documented limit of some 24 V ODESC variants. See :doc:`electrical_review`.

Mechanical
----------

* IMG_0789: the Zeee 3S LiPo pack and its balance connector.
* IMG_0790: a pneumatic tire marked 4.10/3.50-4, with the air valve and metal
  rim. This replaces our older note that said nylon tires.
* IMG_0791: a custom-looking wheel hub adapter, a metal clamping collar and a
  printed-looking support bracket. We do not know the material or how the wheel
  is retained, or whether the gearbox shaft carries the weight of the robot.
* IMG_0792 and IMG_0793: aluminum T-slot frame, 3D-printed-looking brackets, an
  open electronics tray and exposed cables.
* IMG_0794: the front sensor assembly, three blue circuit boards on a custom
  housing. We have not confirmed the exact electronics or pin assignments.
* IMG_0795 to IMG_0798: more views of the chassis and enclosure, the top-mounted
  LiDAR and the front and rear drive assemblies. We still need to measure real
  dimensions.

Before we drive: motor controller ratings, the resistors, the fuses and a
physical motor stop. Before we go outside: how the wheels attach to the shafts
and how they are supported. An open tray with exposed boards does not count as
weather protection for R-6.

The open checks are in the audit checklist.

RL underside, October 28, 2026
------------------------------

A close-up of the rear-left (RL) controller shows the marking JMT G3002B on
several power-stage parts. That is the JieJie Microelectronics JMTG3002B N-channel
MOSFET, and its datasheet gives a **30 V absolute-maximum drain-source voltage**.
We confirmed that **all four controllers are identical hardware**, so we are
using the RL identification for FL, FR, RL and RR. We only photographed the RL
MOSFETs up close and have not read the markings on the other three.

The HOT PAXX pack is 29.4 V fully charged, which is only 0.6 V under the
transistor's absolute maximum, before any switching or braking spikes. That is
too little margin for running these four controllers directly off this pack.
The 24 V QC marking fits a low-voltage ODESC variant.

The RL heat sink was taken off for the inspection and has since been put back
on. We have not checked the thermal paste or how tight it is.

Reference: JieJie Microelectronics JMTG3002B datasheet, version 1.4.
https://e-nexty.dxp.nexty-ele.com/product_files/download?maker_code=JJM&product_part_number=JMTG3002B&product_file_id=5467845&product_id=6198730&lc_code=ja&search_log_id=4389931
