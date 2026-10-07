"""Back-project photo pixels onto the block-out body: pixel -> camera ray -> first Body hit.

Run:  blender -b tools/model/out/dzire-blockout.blend -P tools/model/pick.py
Needs tools/model/out/cameras.json from compare.py. Prints glTF-space points (x left, y up, z fwd)
used to place the parts in build_car.py. Pixels are full-res photo coordinates.
"""
import json
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

HERE = Path(__file__).resolve().parent
PIXELS = {
    "05-front-straight-lights-off": {
        "hood_edge_c": (922, 1725), "bar_top_c": (922, 1800), "red_c": (922, 1898),
        "bar_end_top": (455, 1805), "bar_end_bot": (455, 1885),
        "hl_upper": (340, 1730), "hl_outer_top": (205, 1650), "hl_outer_bot": (205, 1770),
        "hl_lower_mid": (330, 1820),
        "gr_top_c": (922, 1905), "gr_top_corner": (450, 1925), "gr_mid": (425, 2040),
        "gr_bot_corner": (500, 2165), "gr_bot_c": (922, 2170),
        "ins_top": (245, 1950), "ins_mid": (330, 2050), "ins_bot": (400, 2160),
        "plate_tl": (680, 2000), "plate_br": (1200, 2130), "bumper_bot_c": (922, 2255)},
    "03-side-profile-right": {
        "handle_f": (1410, 970), "handle_r": (556, 875), "mirror_c": (2100, 800),
        "mirror_front": (2240, 830), "mirror_rear": (1982, 790), "mirror_top": (2110, 722),
        "mirror_bot": (2110, 880), "hl_side_rear": (3390, 1175), "hl_side_front": (3855, 1370),
        "tl_side_top": (60, 760), "tl_side_bot": (60, 980), "fin": (1060, 290)},
    "01-rear-three-quarter-left": {
        "tl_top_outer": (334, 2000), "tl_top_inner": (610, 2048), "tl_bot_inner": (857, 2353),
        "tl_bot_outer": (247, 2397), "gar_top_l": (610, 2041), "gar_top_r": (2296, 1786),
        "gar_bot_l": (915, 2150), "gar_bot_r": (2223, 2062), "gar_c": (1453, 1917),
        "spoiler_l": (639, 1830), "spoiler_r": (2238, 1656), "fin": (880, 1090)},
}


def ray(cam, u, v):
    """OpenCV pinhole ray -> (origin, direction) in Blender space."""
    r = Vector(cam["params"][:3])
    R = Matrix.Rotation(r.length, 3, r.normalized()) if r.length else Matrix.Identity(3)
    t, f = Vector(cam["params"][3:6]), cam["params"][6]
    C = -(R.transposed() @ t)
    d = R.transposed() @ Vector(((u - cam["cx"]) / f, (v - cam["cy"]) / f, 1))
    to_b = lambda p: Vector((p.x, -p.z, p.y))  # glTF -> Blender
    return to_b(C), to_b(d).normalized()


cams = json.loads((HERE / "out/cameras.json").read_text())
deps = bpy.context.evaluated_depsgraph_get()
targets = [bpy.data.objects[n] for n in ("Body", "Greenhouse")]
for view, pts in PIXELS.items():
    print(f"--- {view}")
    for name, (u, v) in pts.items():
        o, d = ray(cams[view], u, v)
        hits = [h for h in (ob.ray_cast(o, d, depsgraph=deps) for ob in targets) if h[0]]
        if hits:
            _, p, n, _ = min(hits, key=lambda h: (h[1] - o).length)
            print(f"{name:16s} x={p.x:+.3f} y={p.z:.3f} z={-p.y:+.3f}  n=({n.x:+.2f},{n.z:+.2f},{-n.y:+.2f})")
        else:
            print(f"{name:16s} miss")
