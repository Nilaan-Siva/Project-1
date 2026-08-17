"""
Parametric 3D-printable case for iPhone 15 Pro Max.

Coordinate frame = BACK VIEW of the phone (looking at the case exterior back):
  x -> right, y -> up (toward the phone top), z = 0 at the back exterior,
  +z toward the screen. In this frame the camera plateau sits TOP-LEFT and
  shares the LEFT edge with the action/volume buttons; the side button is on
  the RIGHT edge; USB-C + speakers on the bottom edge.

Body dims per Apple tech specs: 159.86 x 76.73 x 8.25 mm, camera plateau
rises ~3.6 mm. The plateau footprint is not published, so the camera window
uses a ~2 mm safety margin around a 38.7 mm assumed plateau.

Prints back-flat on the bed. Default variant has a flat back (support-free).
The "lensring" variant adds a raised lens-guard ring (enable supports for it).
Recommended: TPU 95A, 0.2 mm layers, 3 walls. For rigid PETG raise CLR to 0.45.
"""
import cadquery as cq

# ---------------- parameters (mm) ----------------
L, W, T = 159.86, 76.73, 8.25    # phone body
BODY_R = 15.5                    # phone corner radius (approx)
CLR = 0.30                       # fit clearance per side (TPU)
WALL = 1.7                       # side wall thickness
BACK = 1.6                       # back thickness (MagSafe still works through this)
LIP = 1.15                       # how far the front lip wraps over the screen edge
LIP_H = 1.0                      # lip height above the phone front
CAM_PLATEAU = 38.7               # assumed plateau square size
CAM_INSET = 3.3                  # plateau inset from top and left phone edges
CAM_MARGIN = 1.9                 # extra opening margin around the plateau
CAM_R = 11.0                     # camera window corner radius
RING_H = 2.4                     # lens-guard ring height (lensring variant)
RING_W = 2.2                     # lens-guard ring width
SLOT_H = 7.5                     # button slot height in z
SLOT_Z0 = 2.5                    # slot lower z
SLOT_R = 2.6                     # slot corner radius
# from-top spans for side cutouts (generous; buttons protrude ~1 mm)
ACTION_SPAN = (26.5, 41.5)       # left wall: Action button
VOLUME_SPAN = (44.5, 73.0)       # left wall: volume up + down
POWER_SPAN = (62.0, 88.0)        # right wall: side button
BOTTOM_W = 58.0                  # bottom opening width (USB-C + speaker + mic)

cavL, cavW, cavR = L + 2*CLR, W + 2*CLR, BODY_R + CLR
outL, outW, outR = cavL + 2*WALL, cavW + 2*WALL, BODY_R + CLR + WALL
H = BACK + T + CLR + LIP_H       # total case height


def rbox(w, l, r, h, z0=0.0, cx=0.0, cy=0.0):
    """Rounded-corner (about z) box, centered at (cx, cy), from z0 to z0+h."""
    return (cq.Workplane("XY").workplane(offset=z0).center(cx, cy)
            .rect(w, l).extrude(h).edges("|Z").fillet(r))


def slot(cx, cy, wx, wy, axis):
    """Capsule slot from z SLOT_Z0, rounded on edges parallel to `axis`."""
    s = (cq.Workplane("XY").workplane(offset=SLOT_Z0).center(cx, cy)
         .rect(wx, wy).extrude(SLOT_H))
    return s.edges("|" + axis).fillet(SLOT_R)


def build(ring=False):
    case = rbox(outW, outL, outR, H)

    # phone cavity up to the phone front; the lip stays above it
    case = case.cut(rbox(cavW, cavL, cavR, T + CLR, z0=BACK))
    # screen opening through the lip
    winW, winL = cavW - 2*LIP, cavL - 2*LIP
    case = case.cut(rbox(winW, winL, max(1.0, cavR - LIP), LIP_H + 1,
                         z0=BACK + T + CLR))

    # soften outer edges before cutting features
    for sel, r in (("<Z", 1.1), (">Z", 0.5)):
        try:
            case = case.edges(sel).fillet(r)
        except Exception:
            pass

    # camera window, top-left in back view
    cam_open = CAM_PLATEAU + 2*CAM_MARGIN
    ccx = -W/2 + CAM_INSET + CAM_PLATEAU/2          # negative x = left
    ccy = L/2 - CAM_INSET - CAM_PLATEAU/2           # positive y = top
    if ring:
        ring_solid = (cq.Workplane("XY").workplane(offset=-RING_H)
                      .center(ccx, ccy)
                      .rect(cam_open + 2*RING_W, cam_open + 2*RING_W)
                      .extrude(RING_H + BACK/2)
                      .edges("|Z").fillet(CAM_R + RING_W))
        case = case.union(ring_solid)
    cam = (cq.Workplane("XY").workplane(offset=-RING_H - 1)
           .center(ccx, ccy).rect(cam_open, cam_open)
           .extrude(BACK + RING_H + 2).edges("|Z").fillet(CAM_R))
    case = case.cut(cam)
    try:  # ease the window rim on the outside
        case = case.edges(
            cq.selectors.BoxSelector((ccx - cam_open, ccy - cam_open, -RING_H - 0.7),
                                     (ccx + cam_open, ccy + cam_open, 0.55))
        ).chamfer(0.5)
    except Exception:
        pass

    # side + bottom cutouts, cut through the walls
    def span_center(span):
        y_hi, y_lo = cavL/2 - span[0], cavL/2 - span[1]
        return (y_hi + y_lo) / 2, y_hi - y_lo

    for span in (ACTION_SPAN, VOLUME_SPAN):        # LEFT wall (volume side)
        yc, ln = span_center(span)
        case = case.cut(slot(-outW/2 + 1, yc, 8, ln, "X"))
    yc, ln = span_center(POWER_SPAN)               # RIGHT wall (side button)
    case = case.cut(slot(outW/2 - 1, yc, 8, ln, "X"))
    case = case.cut(slot(0, -outL/2 + 1, BOTTOM_W, 8, "Y"))   # bottom ports

    # snap-in chamfer on the inner lip edge
    try:
        case = case.edges(
            cq.selectors.BoxSelector((-winW/2 - 0.6, -winL/2 - 0.6, BACK + T + CLR - 0.05),
                                     (winW/2 + 0.6, winL/2 + 0.6, H + 0.1))
        ).chamfer(0.45)
    except Exception:
        pass

    # debossed label on the cavity floor (prints as a clean top surface)
    try:
        label = (cq.Workplane("XY").workplane(offset=BACK - 0.4)
                 .center(0, -cavL/2 + 22)
                 .text("15 PRO MAX", 5.5, 0.4, font="DejaVu Sans", kind="bold"))
        case = case.cut(label)
    except Exception:
        pass
    return case


if __name__ == "__main__":
    import os
    out = os.path.dirname(os.path.abspath(__file__))
    flat = build(ring=False)
    ringv = build(ring=True)
    cq.exporters.export(flat, f"{out}/iphone15promax_case_flat.stl",
                        tolerance=0.04, angularTolerance=0.25)
    cq.exporters.export(ringv, f"{out}/iphone15promax_case_lensring.stl",
                        tolerance=0.04, angularTolerance=0.25)
    cq.exporters.export(flat, f"{out}/iphone15promax_case.step")
    cq.exporters.export(ringv, f"{out}/viewer.stl",
                        tolerance=0.2, angularTolerance=0.6)
    bb = flat.val().BoundingBox()
    print(f"bbox: {bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f} mm  (expect ~81.1 x 164.3 x 11.2)")
    print("exported: flat.stl, lensring.stl, case.step, viewer.stl")
