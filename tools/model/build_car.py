"""Dzire Tour S (4th-gen Maruti Suzuki Dzire, VXI-level, Arctic White) — procedural model.

Run:  blender -b -P tools/model/build_car.py -- [--render cameras.json] [--out DIR]
Out:  assets/models/dzire-tour-s.glb (then `npm run models:compress`, see PROGRESS.md)
Spec: reference/dzire-3d/DZIRE_3D_MODEL_BRIEF.md (dimensions §2, parts §3, materials §4).

All geometry is authored in glTF space via G(x, y, z): metres, +Y up, +Z forward (car front),
+X = car's LEFT side. Blender stores it Z-up, and the glTF exporter converts back.
"""
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------- dimensions (§2)
LENGTH, WIDTH, WHEELBASE = 3.995, 1.735, 2.450
FRONT_OVERHANG = 0.73
TYRE_R, TYRE_W, RIM_R = 0.31, 0.165, 0.178
TRACK = 1.52
Z_FRONT, Z_REAR = LENGTH / 2, -LENGTH / 2
Z_AXLE_F = Z_FRONT - FRONT_OVERHANG          # 1.2675
Z_AXLE_R = Z_AXLE_F - WHEELBASE              # -1.1825
HALF_W = WIDTH / 2

# ---------------------------------------------------------------- profile curves (z -> value)
# Side silhouette, traced against photos 03/04 after camera solve. Tune here.
BODY_TOP = [  # hood / beltline / boot deck height
    (Z_REAR, 0.92), (-1.985, 1.04), (-1.95, 1.10), (-1.90, 1.125), (-1.70, 1.13), (-1.42, 1.115),
    (-1.10, 1.06), (-0.90, 1.04), (0.0, 1.005), (0.70, 0.985), (0.97, 0.965),
    (1.30, 0.925), (1.60, 0.885), (1.85, 0.845), (1.95, 0.80), (1.985, 0.74), (Z_FRONT, 0.66)]
BODY_BOTTOM = [
    (Z_REAR, 0.36), (-1.97, 0.28), (-1.85, 0.25), (-1.55, 0.24), (0.0, 0.20),
    (1.60, 0.23), (1.88, 0.25), (1.97, 0.29), (Z_FRONT, 0.36)]
BODY_HALF_WIDTH = [  # plan view, at the shoulder
    (Z_REAR, 0.70), (-1.97, 0.79), (-1.88, 0.835), (-1.55, 0.862), (-0.5, HALF_W), (1.0, HALF_W),
    (1.55, 0.858), (1.82, 0.83), (1.94, 0.79), (1.98, 0.74), (Z_FRONT, 0.66)]
ROOF = [  # greenhouse top (centreline)
    (-1.42, 1.115), (-1.30, 1.18), (-1.10, 1.28), (-0.88, 1.36), (-0.62, 1.43), (-0.30, 1.468),
    (0.0, 1.47), (0.15, 1.455), (0.35, 1.36), (0.60, 1.21), (0.80, 1.08), (0.97, 0.975)]
Z_WINDSCREEN_BASE, Z_REAR_WINDOW_BASE = 0.97, -1.42
Z_ROOF_FRONT, Z_ROOF_REAR = 0.12, -0.80        # painted roof panel between these
Z_B_PILLAR = (-0.27, -0.15)                    # gloss-black B-pillar
Z_C_PILLAR = -0.98                             # side glass ends here; black quarter surround behind
Z_QUARTER = -1.22                              # ...back to here, then body colour
GREENHOUSE_TOP_HALF_W = 0.56
TUMBLEHOME = 0.915                             # greenhouse base width / shoulder width


def pchip(points):
    """Monotone cubic interpolant through (x, y) control points (Fritsch-Carlson)."""
    xs, ys = map(np.asarray, zip(*points))
    h, d = np.diff(xs), np.diff(ys) / np.diff(xs)
    m = np.zeros_like(ys)
    m[0], m[-1] = d[0], d[-1]
    for k in range(1, len(xs) - 1):
        if d[k - 1] * d[k] > 0:
            w1, w2 = 2 * h[k] + h[k - 1], h[k] + 2 * h[k - 1]
            m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])

    def f(x):
        k = int(np.clip(np.searchsorted(xs, x) - 1, 0, len(xs) - 2))
        t = (x - xs[k]) / h[k]
        return ((2 * t**3 - 3 * t**2 + 1) * ys[k] + (t**3 - 2 * t**2 + t) * h[k] * m[k]
                + (-2 * t**3 + 3 * t**2) * ys[k + 1] + (t**3 - t**2) * h[k] * m[k + 1])
    return f


body_top, body_bottom, body_w, roof = map(pchip, (BODY_TOP, BODY_BOTTOM, BODY_HALF_WIDTH, ROOF))


def catmull(pts, n_per_seg=4):
    """Resample an open polyline with a Catmull-Rom spline (keeps the endpoints)."""
    p = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        a, b, c, d = map(np.asarray, p[i - 1:i + 3])
        for t in np.linspace(0, 1, n_per_seg, endpoint=False):
            out.append(0.5 * ((2 * b) + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t**2
                              + (-a + 3 * b - 3 * c + d) * t**3))
    out.append(np.asarray(pts[-1]))
    return [tuple(q) for q in out]


# Body cross-section, half profile from bottom centre to top centre: (x / half_width, height fraction).
BODY_SECTION = catmull([(0, 0), (0.78, 0), (0.93, 0.035), (0.985, 0.14), (1.0, 0.42), (1.0, 0.80),
                        (0.985, 0.885), (0.95, 0.945), (0.87, 0.985), (0.55, 1.0), (0, 1.0)])


# ---------------------------------------------------------------- scene helpers
def G(x, y, z):
    """glTF (x, y-up, z-forward) -> Blender (x, -z, y)."""
    return Vector((x, -z, y))


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


MATERIALS = {}


def material(name, color, metallic=0.0, roughness=0.5, alpha=1.0, clearcoat=0.0,
             clearcoat_roughness=0.03, emission=None, emission_strength=0.0, transmission=0.0):
    if name in MATERIALS:
        return MATERIALS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    rgb = [((int(color[i:i + 2], 16) / 255) ** 2.2) for i in (1, 3, 5)]  # sRGB hex -> linear
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = roughness
    b.inputs["Coat Weight"].default_value = clearcoat
    b.inputs["Coat Roughness"].default_value = clearcoat_roughness
    b.inputs["Transmission Weight"].default_value = transmission
    if emission:
        b.inputs["Emission Color"].default_value = (*[(int(emission[i:i + 2], 16) / 255) ** 2.2
                                                      for i in (1, 3, 5)], 1)
        b.inputs["Emission Strength"].default_value = emission_strength
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = "BLENDED"
    m.diffuse_color = (*rgb, alpha)
    MATERIALS[name] = m
    return m


def make_materials():
    material("Paint_ArcticWhite", "#F2F3F0", roughness=0.25, clearcoat=1.0, clearcoat_roughness=0.05)
    material("Plastic_GlossBlack", "#0A0A0B", roughness=0.15)
    material("Plastic_MatteBlack", "#151517", roughness=0.7)
    material("Chrome", "#E8E8E8", metallic=1.0, roughness=0.08)
    material("Accent_Red", "#B5121B", roughness=0.3)
    material("Glass_Tinted", "#1A2228", roughness=0.05, alpha=0.35)
    material("WheelCover_Silver", "#9EA3A8", metallic=0.3, roughness=0.45)
    material("Tyre_Rubber", "#1B1B1B", roughness=0.9)
    material("Lens_Headlamp", "#FFFFFF", roughness=0.02, alpha=0.2)
    material("Lamp_Projector", "#D8DDE3", metallic=1.0, roughness=0.1)
    material("TailLamp_Lens", "#3A0508", roughness=0.1, alpha=0.6)
    material("TailLamp_Emissive", "#FF1A1A", roughness=0.4, emission="#FF1A1A", emission_strength=2.5)
    material("Interior_Black", "#1E1E1E", roughness=0.8)
    material("Interior_Beige", "#CFC3AE", roughness=0.8)
    material("Panel_Gap", "#2A2C2E", roughness=0.8)
    material("Plate_White", "#FFFFFF", roughness=0.5)
    material("Plate_Text", "#0A0A0B", roughness=0.5)


def mesh_object(name, bm, mats, smooth=True, parent=None):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(MATERIALS[m])
    for p in me.polygons:
        p.use_smooth = smooth
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    if parent:
        ob.parent = parent
    return ob


def loft(bm, rings, cap_start=True, cap_end=True, closed=True):
    """Bridge equal-length rings of Blender-space points into quads. Returns faces[ring][seg]."""
    verts = [[bm.verts.new(p) for p in ring] for ring in rings]
    n = len(rings[0])
    segs = n if closed else n - 1
    faces = []
    for a, b in zip(verts, verts[1:]):
        faces.append([bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i])) for i in range(segs)])
    if cap_start:
        bm.faces.new(list(reversed(verts[0])))
    if cap_end:
        bm.faces.new(verts[-1])
    return faces


def end_spaced(z0, z1, n):
    """Samples denser near both ends (where the body curves fastest)."""
    t = (1 - np.cos(np.linspace(0, math.pi, n))) / 2
    return z0 + (z1 - z0) * t


# ---------------------------------------------------------------- body (§3.1)
def build_body():
    bm = bmesh.new()
    rings = []
    for z in end_spaced(Z_REAR, Z_FRONT, 110):
        yb, yt, w = body_bottom(z), body_top(z), body_w(z)
        half = [(fx * w, yb + fy * (yt - yb)) for fx, fy in BODY_SECTION]
        # ring: -X side top->bottom, then +X side bottom->top (mirror of the half profile)
        ring = [G(-x, y, z) for x, y in reversed(half[1:-1])] + [G(x, y, z) for x, y in half]
        rings.append(ring)
    loft(bm, rings)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    body = mesh_object("Body", bm, ["Paint_ArcticWhite", "Plastic_MatteBlack"])
    cut_wheel_arches(body)
    return body


def cut_wheel_arches(body):
    """Boolean out the 4 wheel wells; cut faces take the cutter's matte-black (well liner)."""
    for side in (1, -1):
        for z in (Z_AXLE_F, Z_AXLE_R):
            bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.365, depth=0.40,
                                                location=G(side * 0.80, TYRE_R + 0.015, z),
                                                rotation=(0, math.pi / 2, 0))
            cutter = bpy.context.object
            cutter.data.materials.append(MATERIALS["Plastic_MatteBlack"])
            mod = body.modifiers.new("arch", "BOOLEAN")
            mod.operation, mod.object = "DIFFERENCE", cutter
            bpy.context.view_layer.objects.active = body
            bpy.ops.object.modifier_apply(modifier=mod.name)
            bpy.data.objects.remove(cutter)


# ---------------------------------------------------------------- greenhouse (glass + pillars + roof)
GH_SIDE, GH_CORNER, GH_TOP = "side", "corner", "top"


def greenhouse_half(z):
    yb = body_top(z) - 0.02
    yt = max(roof(z), yb)
    h = yt - yb
    wb = body_w(z) * TUMBLEHOME
    wt = GREENHOUSE_TOP_HALF_W  # roof width; screens open out so the A/C pillars sit at their edges
    if z > Z_ROOF_FRONT:
        wt += (wb - 0.07 - wt) * (z - Z_ROOF_FRONT) / (Z_WINDSCREEN_BASE - Z_ROOF_FRONT)
    elif z < Z_ROOF_REAR:
        wt += (wb - 0.12 - wt) * (Z_ROOF_REAR - z) / (Z_ROOF_REAR - Z_REAR_WINDOW_BASE)
    wt = min(wt, wb)
    pts = [(wb + (wt - wb) * v, yb + v * 0.86 * h, GH_SIDE) for v in (0, 0.25, 0.5, 0.75, 1.0)]
    pts += [(wt - 0.035, yb + 0.95 * h, GH_CORNER), (wt - 0.09, yb + 0.99 * h, GH_CORNER),
            (wt * 0.6, yb + 0.998 * h, GH_TOP), (wt * 0.3, yt, GH_TOP), (0.0, yt, GH_TOP)]
    return pts


def build_greenhouse():
    bm = bmesh.new()
    zs = end_spaced(Z_REAR_WINDOW_BASE, Z_WINDSCREEN_BASE, 70)
    rings, tags = [], None
    for z in zs:
        half = greenhouse_half(z)
        ring = [G(-x, y, z) for x, y, _ in reversed(half[1:])] + [G(x, y, z) for x, y, _ in half]
        rings.append(ring)
        tags = [t for _, _, t in reversed(half[1:])] + [t for _, _, t in half]
    faces = loft(bm, rings, cap_start=False, cap_end=False, closed=False)
    label = {}
    for k, row in enumerate(faces):
        zc = (zs[k] + zs[k + 1]) / 2
        for i, f in enumerate(row):
            tag = tags[i] if tags[i] == tags[i + 1] else GH_CORNER
            if tag == GH_CORNER:
                name = "Greenhouse"                              # A/C pillars + roof rails
            elif tag == GH_TOP:
                name = ("Greenhouse" if Z_ROOF_REAR < zc < Z_ROOF_FRONT
                        else "Glass_Front" if zc > 0 else "Glass_Rear")
            elif Z_B_PILLAR[0] < zc < Z_B_PILLAR[1] or Z_QUARTER < zc < Z_C_PILLAR:
                name = "Pillars_Black"
            elif zc < Z_QUARTER:
                name = "Greenhouse"
            else:
                name = "Glass_Side"
            label[f] = name
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.faces.index_update()
    by_index = [label[f] for f in bm.faces]
    for name, mat in (("Greenhouse", "Paint_ArcticWhite"), ("Pillars_Black", "Plastic_GlossBlack"),
                      ("Glass_Front", "Glass_Tinted"), ("Glass_Rear", "Glass_Tinted"),
                      ("Glass_Side", "Glass_Tinted")):
        part = bm.copy()  # copy keeps face order, so by_index still lines up
        part.faces.ensure_lookup_table()
        bmesh.ops.delete(part, geom=[f for f in part.faces if by_index[f.index] != name], context="FACES")
        mesh_object(name, part, [mat])
    bm.free()


# ---------------------------------------------------------------- wheels (§3.4)
def lathe(bm, profile, steps=64):
    """Revolve (radius, axial x) profile around the local X axis."""
    rings = []
    for k in range(steps):
        a = 2 * math.pi * k / steps
        rings.append([Vector((x, r * math.cos(a), r * math.sin(a))) for r, x in profile])
    verts = [[bm.verts.new(p) for p in ring] for ring in rings]
    for k in range(steps):
        a, b = verts[k], verts[(k + 1) % steps]
        for i in range(len(profile) - 1):
            bm.faces.new((a[i], a[i + 1], b[i + 1], b[i]))


def build_wheel(name, side, z):
    hw = TYRE_W / 2
    bm = bmesh.new()
    lathe(bm, [(RIM_R, -hw * 0.85), (0.25, -hw), (0.29, -hw * 0.97), (0.305, -hw * 0.8),
               (TYRE_R, -hw * 0.35), (TYRE_R, hw * 0.35), (0.305, hw * 0.8), (0.29, hw * 0.97),
               (0.25, hw), (RIM_R, hw * 0.85)])
    tyre = mesh_object(name + "_Tyre", bm, ["Tyre_Rubber"])

    bm = bmesh.new()  # domed full wheel cover with a dark centre cap
    lathe(bm, [(0.0, hw + 0.025), (0.035, hw + 0.025), (0.04, hw + 0.022), (0.12, hw + 0.012),
               (0.185, hw - 0.002), (0.19, hw - 0.012), (RIM_R, hw * 0.85)])
    cover = mesh_object(name + "_Cover", bm, ["WheelCover_Silver", "Plastic_MatteBlack"])
    for p in cover.data.polygons:  # innermost ring of faces = centre cap
        if p.center.yz.length < 0.04:
            p.material_index = 1

    bm = bmesh.new()  # 10 twisted turbine vents (dark slots) on the cover face
    for k in range(10):
        a = 2 * math.pi * k / 10
        mat = Matrix.Rotation(a, 4, "X") @ Matrix.Translation((hw + 0.014, 0, 0.115)) \
            @ Matrix.Rotation(math.radians(35), 4, "X")
        bmesh.ops.create_cube(bm, size=1.0, matrix=mat @ Matrix.Diagonal((0.012, 0.022, 0.07, 1)))
    vents = mesh_object(name + "_Vents", bm, ["Plastic_MatteBlack"], smooth=False)

    pivot = bpy.data.objects.new(name, None)  # hub-centred pivot: spin about local X
    bpy.context.scene.collection.objects.link(pivot)
    for part in (tyre, cover, vents):
        part.parent = pivot
    pivot.location = G(side * TRACK / 2, TYRE_R, z)
    if side < 0:
        pivot.rotation_euler = (0, 0, math.pi)  # same part mirrored by rotation, cover faces out
    return pivot


def build_wheels():
    return [build_wheel(n, s, z) for n, s, z in (("Wheel_FL", 1, Z_AXLE_F), ("Wheel_FR", -1, Z_AXLE_F),
                                                ("Wheel_RL", 1, Z_AXLE_R), ("Wheel_RR", -1, Z_AXLE_R))]


# ---------------------------------------------------------------- surface-conforming parts
# Anchor points come from tools/model/pick.py (photo pixel -> solved camera ray -> Body hit):
# front from photo 05, side from 03. Rear heights from 03; rear shapes eyeballed from 01
# (its camera is hand-placed, so its hits are not trusted).
BODY = None  # set in main(); every patch is snapped onto it


def resample(poly, n, u0=0.0, u1=1.0, smooth=True):
    """n points evenly spaced by arc length over [u0, u1] of a (Catmull-smoothed) polyline."""
    pts = np.asarray(catmull(poly, 8) if smooth and len(poly) > 2 else poly, float)
    t = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    t /= t[-1]
    q = np.linspace(u0, u1, n)
    return np.column_stack([np.interp(q, t, pts[:, k]) for k in range(3)])


def sub(a, b, u0, u1, v0, v1):
    """Sub-rectangle (in patch u/v) of the ruled surface between polylines a and b."""
    A, B = resample(a, 64), resample(b, 64)
    return (resample(A + (B - A) * v0, 32, u0, u1, smooth=False),
            resample(A + (B - A) * v1, 32, u0, u1, smooth=False))


def snap(p, axis_z):
    """Project glTF point p horizontally onto the Body, along the ray from (0, p.y, axis_z)."""
    o = np.array([0.0, p[1], axis_z])
    d = np.asarray(p, float) - o
    d[1] = 0
    d /= np.linalg.norm(d)
    ok, hit, n, _ = BODY.ray_cast(G(*(o + 4 * d)), G(*-d))
    if not ok:
        raise RuntimeError(f"snap missed the body at {p}")
    return hit, n


def patch(bm, a, b, mi, lift, axis_z, nu=16, nv=3):
    """Raised panel on the body: ruled surface a->b snapped to Body, lifted along the normal,
    with a skirt down to the surface so it reads solid edge-on."""
    A, B = resample(a, nu + 1), resample(b, nu + 1)
    grid = [[snap(A[i] + (B[i] - A[i]) * v, axis_z) for i in range(nu + 1)]
            for v in np.linspace(0, 1, nv + 1)]
    top = [[bm.verts.new(h + n * lift) for h, n in row] for row in grid]
    base = [[bm.verts.new(h - n * 0.002) for h, n in row] for row in grid]
    centre = sum((v.co for row in top for v in row), Vector()) / ((nu + 1) * (nv + 1))
    new = []
    for r in range(nv):
        for i in range(nu):
            f = bm.faces.new((top[r][i], top[r][i + 1], top[r + 1][i + 1], top[r + 1][i]))
            f.normal_update()
            if f.normal.dot(grid[r][i][1] + grid[r + 1][i + 1][1]) < 0:
                f.normal_flip()
            new.append(f)
    ring = ([(0, i) for i in range(nu + 1)] + [(r, nu) for r in range(1, nv + 1)]
            + [(nv, i) for i in range(nu - 1, -1, -1)] + [(r, 0) for r in range(nv - 1, 0, -1)])
    for (r0, i0), (r1, i1) in zip(ring, ring[1:] + ring[:1]):
        f = bm.faces.new((top[r0][i0], top[r1][i1], base[r1][i1], base[r0][i0]))
        f.normal_update()
        if f.normal.dot(f.calc_center_median() - centre) < 0:
            f.normal_flip()
        new.append(f)
    for f in new:
        f.material_index = mi


def mirror_x(poly, s):
    return [(s * x, y, z) for x, y, z in poly]


def beam(bm, p0, p1, w, h, mi):
    """Box from Blender point p0 to p1, w wide (local Y) and h tall (local Z)."""
    d = p1 - p0
    up = "Z" if abs(d.normalized().z) < 0.9 else "Y"
    m = (Matrix.Translation((p0 + p1) / 2) @ d.to_track_quat("X", up).to_matrix().to_4x4()
         @ Matrix.Diagonal((d.length, w, h, 1)))
    for v in bmesh.ops.create_cube(bm, size=1.0, matrix=m)["verts"]:
        for f in v.link_faces:
            f.material_index = mi


def box(bm, c, size, mi, pitch=0.0):
    """Box at glTF centre c, glTF size (x, y, z); pitch (deg) tips +Y toward +Z."""
    m = (Matrix.Translation(G(*c)) @ Matrix.Rotation(math.radians(pitch), 4, "X")
         @ Matrix.Diagonal((size[0], size[2], size[1], 1)))
    for v in bmesh.ops.create_cube(bm, size=1.0, matrix=m)["verts"]:
        for f in v.link_faces:
            f.material_index = mi


# ---------------------------------------------------------------- front (§3.2)
AX_F, AX_R = 1.0, -1.0  # snap axes for front / rear parts
BAR_TOP = [(-0.51, 0.785, 2.0), (0.0, 0.78, 2.0), (0.51, 0.785, 2.0)]
BAR_BOT = [(-0.51, 0.696, 2.0), (0.0, 0.696, 2.0), (0.51, 0.696, 2.0)]
GRILLE_EDGE = [(0.515, 0.675, 2.0), (0.545, 0.53, 2.0), (0.47, 0.39, 2.0)]  # top -> bottom, +X side
INSERT_IN = [(0.737, 0.631, 1.98), (0.647, 0.523, 2.0), (0.575, 0.398, 2.0)]
INSERT_OUT = [(0.79, 0.62, 1.95), (0.70, 0.51, 2.0), (0.62, 0.40, 2.0)]
HL_TOP = [(0.51, 0.785, 1.97), (0.64, 0.843, 1.84), (0.82, 0.85, 1.64)]  # inner -> outer, +X side
HL_BOT = [(0.51, 0.70, 1.99), (0.64, 0.77, 1.97), (0.80, 0.80, 1.76)]


def build_front():
    bm = bmesh.new()  # gloss bar joining the headlamps + red accent line under it
    patch(bm, BAR_TOP, BAR_BOT, 0, 0.006, AX_F, nu=24, nv=2)
    patch(bm, [(x, 0.696, z) for x, _, z in BAR_BOT], [(x, 0.684, z) for x, _, z in BAR_BOT],
          1, 0.007, AX_F, nu=24, nv=1)
    mesh_object("Front_UpperBar", bm, ["Plastic_GlossBlack", "Accent_Red"])

    bm = bmesh.new()  # trapezoid grille (gloss backing) + 4 horizontal matte slats
    patch(bm, mirror_x(GRILLE_EDGE, -1), GRILLE_EDGE, 0, 0.004, AX_F, nu=8, nv=8)
    ys, xs = [p[1] for p in GRILLE_EDGE][::-1], [p[0] for p in GRILLE_EDGE][::-1]
    for yc in (0.44, 0.50, 0.56, 0.62):
        hw = float(np.interp(yc, ys, xs)) - 0.03
        patch(bm, [(-hw, yc + 0.012, 2.0), (hw, yc + 0.012, 2.0)],
              [(-hw, yc - 0.012, 2.0), (hw, yc - 0.012, 2.0)], 1, 0.014, AX_F, nu=8, nv=1)
    mesh_object("Front_Grille", bm, ["Plastic_GlossBlack", "Plastic_MatteBlack"])

    bm = bmesh.new()
    for s in (1, -1):
        patch(bm, mirror_x(INSERT_IN, s), mirror_x(INSERT_OUT, s), 0, 0.004, AX_F, nu=10, nv=1)
    mesh_object("Front_CornerInserts", bm, ["Plastic_MatteBlack"])


def build_headlamp(name, s):
    """Housing, chrome reflector (inner), projector bowl (outer), smoked clear lens."""
    top, bot = mirror_x(HL_TOP, s), mirror_x(HL_BOT, s)
    bm = bmesh.new()
    patch(bm, top, bot, 0, 0.004, AX_F, nu=20, nv=3)
    patch(bm, *sub(top, bot, 0.02, 0.42, 0.15, 0.85), 1, 0.008, AX_F, nu=8, nv=2)
    c, _ = sub(top, bot, 0.62, 0.62, 0.5, 0.5)
    hit, n = snap(c[0], AX_F)
    m = (Matrix.Translation(hit + n * 0.006) @ n.to_track_quat("Z", "Y").to_matrix().to_4x4())
    for v in bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.034, radius2=0.026,
                                   depth=0.012, matrix=m)["verts"]:
        for f in v.link_faces:
            f.material_index = 2
    patch(bm, top, bot, 3, 0.016, AX_F, nu=20, nv=3)
    mesh_object(name, bm, ["Plastic_GlossBlack", "Chrome", "Lamp_Projector", "Lens_Headlamp"])


# ---------------------------------------------------------------- rear (§3.6)
TL_TOP = [(0.84, 1.00, -1.86), (0.78, 0.99, -1.96), (0.45, 0.975, -1.995)]  # outer -> inner, +X
TL_BOT = [(0.85, 0.77, -1.88), (0.76, 0.79, -1.97), (0.50, 0.86, -1.995)]
GARNISH_TOP = [(-0.46, 0.975, -2.0), (0.0, 0.982, -2.0), (0.46, 0.975, -2.0)]


def build_taillamp(name, s):
    """Gloss housing, three stacked emissive 'Trinity' bars, smoked red lens."""
    top, bot = mirror_x(TL_TOP, s), mirror_x(TL_BOT, s)
    bm = bmesh.new()
    patch(bm, top, bot, 0, 0.003, AX_R, nu=20, nv=3)
    for v0 in (0.12, 0.40, 0.68):
        patch(bm, *sub(top, bot, 0.08, 0.80, v0, v0 + 0.12), 1, 0.007, AX_R, nu=12, nv=1)
    patch(bm, top, bot, 2, 0.012, AX_R, nu=20, nv=3)
    mesh_object(name, bm, ["Plastic_GlossBlack", "TailLamp_Emissive", "TailLamp_Lens"])


def deck_height(x, z):
    ok, hit, _, _ = BODY.ray_cast(G(x, 3.0, z), Vector((0, 0, -1)))
    return hit.z if ok else body_top(z)


def build_rear():
    bm = bmesh.new()  # gloss bar across the boot joining the lamps, chrome strip inset near its top
    patch(bm, GARNISH_TOP, [(x, 0.915, z) for x, _, z in GARNISH_TOP], 0, 0.006, AX_R, nu=24, nv=2)
    patch(bm, [(x, y - 0.007, z) for x, y, z in GARNISH_TOP],  # black above + below = contrast
          [(x, y - 0.025, z) for x, y, z in GARNISH_TOP], 1, 0.012, AX_R, nu=24, nv=1)
    mesh_object("Rear_Garnish", bm, ["Plastic_GlossBlack", "Chrome"])

    bm = bmesh.new()  # aero lip along the boot's rear edge, overhanging the rear face
    rings = []
    for x in np.linspace(-0.64, 0.64, 33):
        y1, y2 = deck_height(x, -1.86), deck_height(x, -1.965)
        rings.append([G(x, y1 - 0.003, -1.85), G(x, y2 + 0.045, -1.955),
                      G(x, y2 + 0.038, -2.015), G(x, y2 - 0.014, -1.985)])
    loft(bm, rings)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh_object("Rear_Spoiler", bm, ["Paint_ArcticWhite"])


# ---------------------------------------------------------------- side (§3.3)
HANDLES = [(0.892, -0.092), (0.922, -1.093)]  # (y, z) of front / rear door handle (photo 03)
MIRROR_CAP = (0.92, 1.03, 0.72)                 # centre, +X side; boxy cap 0.17 x 0.10 x 0.10 m


def build_side():
    bm = bmesh.new()
    for s in (1, -1):
        for y, z in HANDLES:
            hit, n = snap((s, y, z), z)
            p = hit + n * 0.012
            beam(bm, p + G(0, 0, -0.095), p + G(0, 0, 0.095), 0.022, 0.032, 0)
            patch(bm, [(s, y + 0.022, z + 0.07), (s, y + 0.022, z - 0.07)],
                  [(s, y - 0.020, z + 0.07), (s, y - 0.020, z - 0.07)], 1, 0.002, z, nu=4, nv=1)
    mesh_object("Door_Handles", bm, ["Paint_ArcticWhite", "Plastic_MatteBlack"])

    for name, s in (("Mirror_L", 1), ("Mirror_R", -1)):
        bm = bmesh.new()
        cx, cy, cz = MIRROR_CAP
        frame = Matrix.Translation(G(s * cx, cy, cz)) @ Matrix.Rotation(math.radians(8 * s), 4, "Z")
        cap = bmesh.ops.create_cube(bm, size=1.0, matrix=frame @ Matrix.Diagonal((0.17, 0.10, 0.10, 1)))
        bmesh.ops.bevel(bm, geom=list({e for v in cap["verts"] for e in v.link_edges}), offset=0.03,
                        segments=3, profile=0.5, affect="EDGES")  # rounded box, outer end swept back
        for v in bmesh.ops.create_cube(bm, size=1.0, matrix=frame @ Matrix.Translation((0, 0.051, 0))
                                       @ Matrix.Diagonal((0.135, 0.004, 0.07, 1)))["verts"]:
            for f in v.link_faces:
                f.material_index = 2  # mirror glass on the rear face
        beam(bm, G(s * 0.80, 1.0, 0.80), G(s * 0.80, 1.0, 0.66), 0.03, 0.055, 1)  # base flag
        beam(bm, G(s * 0.80, 1.02, 0.74), G(s * (cx - 0.06), 1.025, cz + 0.01), 0.05, 0.045, 1)  # arm
        mesh_object(name, bm, ["Paint_ArcticWhite", "Plastic_MatteBlack", "Chrome"])

    bm = bmesh.new()  # black beltline trim strip under the side windows
    rings = []
    for z in np.linspace(Z_C_PILLAR, 0.90, 40):
        p0, p1 = greenhouse_half(z)[:2]
        q = (p0[0] + (p1[0] - p0[0]) * 0.12, p0[1] + (p1[1] - p0[1]) * 0.12)
        half = [(p0[0] + 0.004, p0[1] - 0.004), (q[0] + 0.004, q[1])]
        rings.append([G(-x, y, z) for x, y in half] + [G(x, y, z) for x, y in half])
    faces = loft(bm, rings, cap_start=False, cap_end=False, closed=False)
    bmesh.ops.delete(bm, geom=[row[1] for row in faces], context="FACES")  # drop the cross-car span
    mesh_object("Window_Trim", bm, ["Plastic_GlossBlack"])

    bm = bmesh.new()  # parked wiper arms on the scuttle
    for x0, x1 in ((-0.55, 0.05), (0.0, 0.58)):
        beam(bm, G(x0, roof(0.93) + 0.012, 0.935), G(x1, roof(0.945) + 0.012, 0.945), 0.018, 0.01, 0)
    mesh_object("Wipers", bm, ["Plastic_MatteBlack"])


# ---------------------------------------------------------------- roof (§3.5)
def build_shark_fin(z0=-0.56, z1=-0.76, top=1.525):
    """Fin rising toward the rear; its peak sets the brochure's 1.525 m overall height."""
    hs = pchip([(0, 0.08), (0.35, 0.55), (0.7, 0.93), (0.85, 1.0), (1.0, 0.6)])
    ws = pchip([(0, 0.3), (0.4, 0.85), (1.0, 1.0)])
    h_max = top - roof(z0 + (z1 - z0) * 0.85) + 0.01
    rings = []
    for t in np.linspace(0, 1, 16):
        z = z0 + (z1 - z0) * t
        base, h, w = roof(z) - 0.01, h_max * hs(t), 0.028 * ws(t)
        rings.append([G(w * math.cos(a), base + h * math.sin(a), z) for a in np.linspace(0, math.pi, 11)])
    bm = bmesh.new()
    loft(bm, rings, closed=False)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh_object("Roof_SharkFin", bm, ["Paint_ArcticWhite"])


# ---------------------------------------------------------------- interior (§3.8, photo 09)
def build_interior():
    """Only what shows above the beltline: the solid Body hides cushions, floor and gear lever."""
    bm = bmesh.new()  # black cap over the body top inside the cabin (door trims / parcel shelf)
    rings = []
    for z in end_spaced(Z_REAR_WINDOW_BASE + 0.02, Z_WINDSCREEN_BASE - 0.02, 40):
        wb, yt = body_w(z) * TUMBLEHOME, body_top(z)
        rings.append([G(fx * wb, yt + (0.003 if abs(fx) < 1 else -0.015), z) for fx in (-1, -0.55, 0, 0.55, 1)])
    loft(bm, rings, cap_start=False, cap_end=False, closed=False)
    mesh_object("Interior_Trim", bm, ["Interior_Black"])

    bm = bmesh.new()  # dual-tone dash with satin strip, freestanding touchscreen
    box(bm, (0, 1.03, 0.64), (1.28, 0.06, 0.28), 0)
    box(bm, (0, 0.995, 0.635), (1.28, 0.012, 0.27), 2)
    box(bm, (0, 0.96, 0.63), (1.28, 0.06, 0.26), 1)
    box(bm, (0, 1.14, 0.56), (0.19, 0.11, 0.015), 3, pitch=10)
    box(bm, (0, 1.075, 0.575), (0.04, 0.05, 0.02), 0)
    mesh_object("Interior_Dash", bm, ["Interior_Black", "Interior_Beige", "WheelCover_Silver",
                                      "Plastic_GlossBlack"])

    bm = bmesh.new()  # 3-spoke wheel, built around local X, then aimed at the driver (RHD, -X)
    R, r = 0.18, 0.017
    lathe(bm, [(R + r * math.cos(a), r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 9)], steps=40)
    for end in (Vector((0, R, 0)), Vector((0, -R, 0)), Vector((0, 0, -R))):
        beam(bm, Vector((0, 0, 0)), end, 0.035, 0.012, 0)
    box(bm, (0, 0, 0), (0.05, 0.09, 0.09), 0)
    aim = G(0, 0.42, -0.9).normalized().to_track_quat("X", "Z").to_matrix().to_4x4()
    bmesh.ops.transform(bm, matrix=Matrix.Translation(G(-0.37, 1.04, 0.36)) @ aim, verts=bm.verts)
    mesh_object("Interior_SteeringWheel", bm, ["Interior_Black"])

    bm = bmesh.new()  # beige seat backs + headrests (front pair, rear bench)
    for s in (1, -1):
        box(bm, (s * 0.37, 0.95, -0.15), (0.50, 0.60, 0.10), 0, pitch=-18)
        box(bm, (s * 0.37, 1.33, -0.27), (0.26, 0.16, 0.09), 0, pitch=-10)
        box(bm, (s * 0.40, 1.19, -1.12), (0.24, 0.13, 0.09), 0, pitch=-20)
    box(bm, (0, 0.90, -0.98), (1.30, 0.50, 0.10), 0, pitch=-25)
    mesh_object("Interior_Seats", bm, ["Interior_Beige"])


# ---------------------------------------------------------------- details: badges, plates, gaps (§3, §6)
def groove(bm, poly, width, mi, lift=0.0015):
    """Thin strip drawn on the Body along a glTF polyline (panel gap / crease line). Points are
    projected to the nearest surface, so one line can wrap around corners."""
    pts = np.asarray(catmull(poly, 8), float)
    n = max(4, int(np.linalg.norm(np.diff(pts, axis=0), axis=1).sum() / 0.01))
    hits = [BODY.closest_point_on_mesh(G(*p))[1:3] for p in resample(poly, n)]
    rows = []
    for i, (loc, nrm) in enumerate(hits):
        t = (hits[min(i + 1, n - 1)][0] - hits[max(i - 1, 0)][0]).normalized()
        side = nrm.cross(t).normalized() * width / 2
        c = loc + nrm * lift
        rows.append((bm.verts.new(c + side), bm.verts.new(c - side), nrm))
    for (l0, r0, nrm), (l1, r1, _) in zip(rows, rows[1:]):
        f = bm.faces.new((l0, r0, r1, l1))
        f.normal_update()
        if f.normal.dot(nrm) < 0:
            f.normal_flip()
        f.material_index = mi


def oval(c, rx, ry):
    """Top and bottom halves (left -> right) of an ellipse at glTF centre c, in the XY plane."""
    ts = np.linspace(math.pi, 0, 13)
    return ([(c[0] + rx * math.cos(t), c[1] + ry * math.sin(t), c[2]) for t in ts],
            [(c[0] + rx * math.cos(t), c[1] - ry * math.sin(t), c[2]) for t in ts])


def badge(bm, c, rx, ry, axis, lift):
    """Generic chrome oval with a black inner ring (stand-in for the Suzuki emblem, §6)."""
    for k, (scale, mi) in enumerate(((1.0, 0), (0.8, 1), (0.55, 0))):
        patch(bm, *oval(c, rx * scale, ry * scale), mi, lift + 0.002 * k, axis, nu=16, nv=2)


def disc(bm, hit, n, r, depth, mi):
    m = Matrix.Translation(hit + n * depth / 2) @ n.to_track_quat("Z", "Y").to_matrix().to_4x4()
    for v in bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=r, radius2=r,
                                   depth=depth, matrix=m)["verts"]:
        for f in v.link_faces:
            f.material_index = mi


def build_plate(name, c, axis, lift):
    """Indian-size 500 x 120 mm plate on a black holder, 'DRIVER MITRA' as real geometry (no texture)."""
    hit, n = snap(c, axis)
    frame = Matrix.Translation(hit + n * lift) @ n.to_track_quat("Z", "Y").to_matrix().to_4x4()
    bm = bmesh.new()
    for dz, size, mi in ((-0.004, (0.515, 0.135, 0.006), 0), (0.0, (0.50, 0.12, 0.004), 1)):
        for v in bmesh.ops.create_cube(bm, size=1.0, matrix=frame @ Matrix.Translation((0, 0, dz))
                                       @ Matrix.Diagonal((*size, 1)))["verts"]:
            for f in v.link_faces:
                f.material_index = mi

    cu = bpy.data.curves.new(name + "_Text", "FONT")  # Blender's built-in font (DejaVu Sans, free)
    cu.body, cu.align_x, cu.align_y = "DRIVER MITRA", "CENTER", "CENTER"
    cu.size, cu.offset, cu.extrude = 1.0, 0.03, 0.01  # offset fattens the strokes to read as plate type
    ob = bpy.data.objects.new(name + "_Text", cu)
    bpy.context.scene.collection.objects.link(ob)
    text = bpy.data.meshes.new_from_object(ob.evaluated_get(bpy.context.evaluated_depsgraph_get()))
    bpy.data.objects.remove(ob)
    xs, ys = [v.co.x for v in text.vertices], [v.co.y for v in text.vertices]
    s = min(0.43 / (max(xs) - min(xs)), 0.075 / (max(ys) - min(ys)))
    centre = Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, 0))
    old = set(bm.faces)
    bm.from_mesh(text)
    bpy.data.meshes.remove(text)
    new = [f for f in bm.faces if f not in old]
    for f in new:
        f.material_index = 2
    verts = list({v for f in new for v in f.verts})
    bmesh.ops.transform(bm, verts=verts, matrix=frame @ Matrix.Translation((0, 0, 0.002 + 0.01 * s))
                        @ Matrix.Scale(s, 4) @ Matrix.Translation(-centre))
    mesh_object(name, bm, ["Plastic_GlossBlack", "Plate_White", "Plate_Text"], smooth=False)


# Panel lines, +X side (mirrored). Door shut lines from photos 03/04: the rear handle (z -1.09) sits on
# the rear door, so its trailing edge is behind it and then curves forward around the rear arch.
DOOR_LINES = [
    [(0.88, 0.33, 0.84), (0.88, 0.70, 0.86), (0.86, 0.96, 0.90)],                 # front door, front
    [(0.88, 0.33, -0.20), (0.88, 0.70, -0.205), (0.86, 0.98, -0.21)],             # between doors
    [(0.86, 0.99, -1.23), (0.87, 0.86, -1.235), (0.88, 0.79, -1.17), (0.88, 0.757, -1.025),
     (0.88, 0.66, -0.86), (0.88, 0.53, -0.77), (0.88, 0.40, -0.735), (0.88, 0.33, -0.73)],  # rear door
    [(0.88, 0.33, 0.84), (0.88, 0.33, -0.73)],                                     # door bottoms
]
HOOD_LINE = [(0.0, 0.80, 2.0), (0.30, 0.80, 2.0), (0.50, 0.80, 1.995), (0.62, 0.86, 1.88),
             (0.78, 0.875, 1.70), (0.845, 0.87, 1.45), (0.855, 0.90, 1.15), (0.85, 0.93, 0.92)]
BOOT_LINE = [(0.0, 0.66, -2.0), (0.38, 0.66, -1.995), (0.47, 0.70, -1.99), (0.50, 0.84, -1.995),
             (0.47, 0.99, -1.99), (0.78, 1.01, -1.95), (0.80, 1.06, -1.88), (0.70, 1.11, -1.70),
             (0.66, 1.11, -1.48), (0.0, 1.115, -1.47)]
FUEL_LID = (0.88, 0.85, -1.47)  # left rear quarter (photo 04), 0.15 m rounded square


def build_details():
    bm = bmesh.new()
    badge(bm, (0, 0.742, 2.0), 0.07, 0.042, AX_F, 0.012)
    mesh_object("Front_Logo", bm, ["Chrome", "Plastic_GlossBlack"])

    bm = bmesh.new()  # centred oval above the garnish + a plain chrome bar where the model script sits
    badge(bm, (0, 1.008, -2.0), 0.055, 0.028, AX_R, 0.006)
    patch(bm, [(0.20, 0.997, -2.0), (0.36, 0.997, -2.0)], [(0.20, 0.983, -2.0), (0.36, 0.983, -2.0)],
          0, 0.006, AX_R, nu=6, nv=1)
    mesh_object("Rear_Badges", bm, ["Chrome", "Plastic_GlossBlack"])

    build_plate("Front_Plate", (0, 0.50, 2.0), AX_F, 0.026)  # clears the grille slats
    build_plate("Rear_Plate", (0, 0.80, -2.0), AX_R, 0.010)

    bm = bmesh.new()  # panel gaps: hood, 4 doors, boot lid, fuel lid
    for line in DOOR_LINES:
        for s in (1, -1):
            groove(bm, mirror_x(line, s), 0.005, 0)
    for line in (HOOD_LINE, BOOT_LINE):
        groove(bm, mirror_x(line[::-1], -1)[:-1] + line, 0.005, 0)
    x, y, z = FUEL_LID
    corners = [(-1, -0.6), (-1, 0.6), (-0.6, 1), (0.6, 1), (1, 0.6), (1, -0.6), (0.6, -1), (-0.6, -1)]
    groove(bm, [(x, y + 0.075 * v, z + 0.075 * u) for u, v in corners + corners[:2]], 0.004, 0)
    mesh_object("Body_PanelGaps", bm, ["Panel_Gap"], smooth=False)

    bm = bmesh.new()  # bumpers: front lip line, rear crease, diffuser line, 4 sensor dots
    groove(bm, [(-0.58, 0.345, 1.98), (0.0, 0.345, 1.99), (0.58, 0.345, 1.98)], 0.006, 0)
    groove(bm, [(-0.74, 0.58, -1.93), (0.0, 0.58, -2.0), (0.74, 0.58, -1.93)], 0.004, 0)
    groove(bm, [(-0.66, 0.50, -1.97), (-0.56, 0.39, -1.99), (0.0, 0.385, -2.0), (0.56, 0.39, -1.99),
                (0.66, 0.50, -1.97)], 0.008, 0)
    for x in (-0.50, -0.18, 0.18, 0.50):
        disc(bm, *snap((x, 0.48, -2.0), AX_R), 0.011, 0.002, 0)
    mesh_object("Bumper_Details", bm, ["Plastic_MatteBlack"], smooth=False)

    glass = bpy.data.objects["Glass_Rear"]

    def on_glass(x, z):
        ok, hit, _, _ = glass.ray_cast(G(x, 3.0, z), Vector((0, 0, -1)))
        if not ok:
            raise RuntimeError(f"rear glass missed at x={x}, z={z}")
        return hit

    bm = bmesh.new()  # defogger lines + LED high-mount stop lamp on the rear glass
    for z in np.linspace(-1.32, -0.98, 8):
        hw = greenhouse_half(z)[7][0] * 0.85  # [7] = inner edge of the glass band
        rows = [(on_glass(x, z), on_glass(x, z + 0.005)) for x in np.linspace(-hw, hw, 24)]
        lift = Vector((0, 0, 0.002))
        verts = [(bm.verts.new(a + lift), bm.verts.new(b + lift)) for a, b in rows]
        for (a0, b0), (a1, b1) in zip(verts, verts[1:]):
            bm.faces.new((a0, a1, b1, b0))
    top, low = on_glass(0, -0.86), on_glass(0, -0.90)
    pitch = -math.degrees(math.atan2(top.z - low.z, 0.04))
    c = (0.0, (top.z + low.z) / 2 + 0.004, -0.88)
    box(bm, c, (0.28, 0.006, 0.035), 1, pitch=pitch)
    box(bm, c, (0.24, 0.009, 0.012), 2, pitch=pitch)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh_object("Glass_Rear_Details", bm, ["Plastic_MatteBlack", "Plastic_GlossBlack", "TailLamp_Emissive"],
                smooth=False)


# ---------------------------------------------------------------- render / export
def setup_render(cam_data, out_dir):
    sc = bpy.context.scene
    for engine in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            sc.render.engine = engine
            break
        except TypeError:
            continue
    sc.render.film_transparent = True
    sc.view_settings.view_transform = "Standard"
    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.75, 0.75, 0.78, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
    sc.world = world
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    sun.data.energy = 2.5
    sun.rotation_euler = (math.radians(35), 0, math.radians(30))
    sc.collection.objects.link(sun)

    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    for name, c in cam_data.items():
        W, H = c["size"]
        scale = 1000 / H
        sc.render.resolution_x, sc.render.resolution_y = round(W * scale), 1000
        cam.data.sensor_fit = "HORIZONTAL"
        cam.data.sensor_width = 36
        cam.data.lens = c["f"] * 36 / W
        cam.data.shift_x = -(c["cx"] - W / 2) / W
        cam.data.shift_y = (c["cy"] - H / 2) / W
        cam.matrix_world = Matrix(c["matrix_world"])
        sc.render.filepath = str(Path(out_dir) / f"render_{name}.png")
        bpy.ops.render.render(write_still=True)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out_dir = Path(argv[argv.index("--out") + 1]) if "--out" in argv else ROOT / "tools/model/out"
    out_dir.mkdir(parents=True, exist_ok=True)

    global BODY
    reset_scene()
    make_materials()
    BODY = build_body()
    build_greenhouse()
    build_wheels()
    build_front()
    build_headlamp("Headlamp_L", 1)
    build_headlamp("Headlamp_R", -1)
    build_taillamp("TailLamp_L", 1)
    build_taillamp("TailLamp_R", -1)
    build_rear()
    build_side()
    build_shark_fin()
    build_interior()
    build_details()
    tris = sum(len(p.vertices) - 2 for o in bpy.data.objects if o.type == "MESH" for p in o.data.polygons)
    print(f"triangles: {tris}")

    # Uncompressed source; `npm run models:compress` writes public/models/dzire-tour-s.glb from it.
    bpy.ops.export_scene.gltf(filepath=str(ROOT / "assets/models/dzire-tour-s.glb"), export_format="GLB",
                              export_yup=True, export_apply=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out_dir / "dzire.blend"))
    if "--render" in argv:
        setup_render(json.loads(Path(argv[argv.index("--render") + 1]).read_text()), out_dir)


main()
