# Kavasam — 3D-printable iPhone 15 Pro Max case

Parametric case designed in CadQuery (`iphone15promax_case.py`). Edit the
parameters at the top of the script and re-run it to regenerate the STLs
(`pip install cadquery`, then `python iphone15promax_case.py`).

## Files

| File | What it is |
|---|---|
| `iphone15promax_case_flat.stl` | Flat back — prints support-free. Start here. |
| `iphone15promax_case_lensring.stl` | Raised 2.4 mm lens-guard ring around the camera. Needs supports under the ring only. |
| `iphone15promax_case.step` | CAD-neutral STEP file for editing in Fusion/FreeCAD/etc. |
| `iphone15promax_case.py` | The parametric source. All dimensions live here. |

## Print settings

- **Material:** TPU 95A strongly recommended (flexes to snap on). PLA will crack; if you must go rigid, use PETG and raise `CLR` to 0.45 before regenerating.
- **Orientation:** back flat on the bed (as exported).
- **Layers:** 0.2 mm, 3 perimeters, 25–40 % gyroid infill (the part is mostly walls anyway).
- **TPU tips:** slow (25–35 mm/s), direct-drive extruder preferred, no cooling for first layers.
- Estimated material: ~30 g.

## Design notes

- Body dimensions from Apple's published specs: 159.86 × 76.73 × 8.25 mm.
- Fit clearance 0.30 mm per side; 1.7 mm walls, 1.6 mm back (MagSafe still
  attaches through 1.6 mm, though with reduced strength), 1 mm screen lip.
- Apple does not publish the camera plateau footprint, so the camera window is
  cut oversized (~2 mm margin around an assumed 38.7 mm plateau).
- Cutouts: two slots on the volume/Action side, one on the side-button side,
  and a 58 mm bottom opening for USB-C, speaker, and mics.
- **Sanity check before printing:** hold your phone screen-toward-you — volume
  buttons on the left, and the camera bump shares that same left edge. The
  model is built to that rule (camera window and the two-slot wall share an
  edge). Thirty seconds against your actual phone beats any datasheet.
- First print is a fit test: if it's too tight anywhere, bump `CLR` by 0.1 and
  regenerate; too loose, drop it.

Interactive 3D preview: see the "Kavasam" artifact, or open the STLs in any
slicer.
