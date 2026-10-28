Hardware photo findings — October 28, 2026
===========================================

These observations come from the team's inspection photographs. The raw photos
are not published in the public repository.

Controller identification
-------------------------

The team confirmed that four **distinct** ODESC V4.2 motor controllers are
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
