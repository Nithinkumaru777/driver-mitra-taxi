"""Compare round: solve photo cameras -> build + render in Blender -> side-by-side images.

Run:  python tools/model/compare.py
Out:  tools/model/compare/NN-<photo>-side.jpg (photo | render) and NN-<photo>-overlay.jpg (50 % blend).

Cameras are solved from 2D<->3D correspondences (pose + focal length, principal point = image centre).
3D points are in glTF space: metres, +Y up, +Z = car front, +X = car's LEFT side.
Photos 03/04 use only the wheels (exact from the spec: wheelbase, track, tyre size), so they are
the trustworthy views. 01/02/05 also use body features whose 3D positions are estimates, so
their camera carries some of the model's error. Pixel coordinates are in the full-res photo.
"""
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw
from scipy.optimize import least_squares

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PHOTOS = ROOT / "reference/dzire-3d/photos"
OUT, COMPARE = HERE / "out", HERE / "compare"
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"

ZF, ZR, TYRE_R, COVER_R, COVER_X = 1.2675, -1.1825, 0.31, 0.188, 0.85


def wheel_points(side, z, centre, top, bottom, front, rear, tyre_top):
    """Cover centre + 4 cover extremes + tyre top for one wheel (side=+1 left, -1 right)."""
    x = side * COVER_X
    return [((x, TYRE_R, z), centre), ((x, TYRE_R + COVER_R, z), top),
            ((x, TYRE_R - COVER_R, z), bottom), ((x, TYRE_R, z + COVER_R), front),
            ((x, TYRE_R, z - COVER_R), rear), ((side * 0.84, 2 * TYRE_R, z), tyre_top)]


VIEWS = {
    "01-rear-three-quarter-left": [  # rear 3/4 from the car's left; tail lamps = outer wrap corners
        ((0, 1.525, -0.70), (892, 1061)), ((0, 1.37, -0.85), (1082, 1196)),
        ((0, 0.80, -1.97), (1643, 2171)), ((0.84, 0.0, -1.1825), (190, 3315)),
        ((0.845, 0.93, -1.80), (299, 2002)),
        ((-0.845, 0.93, -1.80), (2309, 1994))],
    "02-front-three-quarter-left": [
        ((0, 0.48, 1.99), (1404, 1602)), ((0, 0.74, 1.96), (1425, 1269)),
        ((-0.80, 0.80, 1.72), (545, 936)), ((0.80, 0.80, 1.72), (2808, 1134)),
        ((-0.97, 1.02, 0.62), (1082, 395)), ((0.97, 1.02, 0.62), (3234, 603)),
        ((0, 0.975, 0.97), (1934, 624)), ((0, 0.29, 1.99), (1414, 1903))],
    "03-side-profile-right":
        wheel_points(-1, ZF, (2865, 1790), (2870, 1570), (2860, 2050), (3120, 1790), (2625, 1790), (2870, 1460))
        + wheel_points(-1, ZR, (510, 1462), (505, 1295), (510, 1640), (655, 1470), (360, 1460), (520, 1170)),
    "04-side-profile-left":
        wheel_points(1, ZF, (1038, 1712), (1035, 1510), (1040, 1915), (810, 1712), (1265, 1712), (1035, 1305))
        + wheel_points(1, ZR, (3240, 1425), (3240, 1265), (3240, 1585), (3080, 1425), (3400, 1425), (3250, 1110)),
    "05-front-straight-lights-off": [
        ((-0.865, 0.70, 1.35), (202, 1829)), ((0.865, 0.70, 1.35), (1628, 1829)),
        ((0, 0.29, 1.99), (922, 2255)), ((0, 1.455, 0.15), (868, 1066)),
        ((0, 0.975, 0.97), (891, 1380)), ((0, 0.84, 1.90), (922, 1736)),
        ((-0.80, 0.80, 1.72), (209, 1705)), ((0.80, 0.80, 1.72), (1620, 1697))],
}


LONG_SIDE = 4160  # all photos are from one phone lens; f scales with the image's long side


def to_camera(p, f, size):
    W, H = size
    R, _ = cv2.Rodrigues(np.asarray(p[:3]))
    C = -R.T @ np.asarray(p[3:6])
    M = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])  # glTF -> Blender axes
    rot = np.column_stack([M @ R[0], M @ -R[1], M @ -R[2]])  # OpenCV cam -> Blender cam
    mw = np.eye(4)
    mw[:3, :3], mw[:3, 3] = rot, M @ C
    return {"size": [W, H], "f": float(f), "cx": W / 2, "cy": H / 2, "matrix_world": mw.tolist(),
            "camera_gltf": C.round(3).tolist(), "params": [*map(float, p[:6]), float(f)]}


# Hand-placed cameras (eye, target in glTF metres) for views whose correspondences are too
# uncertain to solve. 01: rear face fills ~91 % of frame width at the shared lens -> ~3.5 m back.
MANUAL = {"01-rear-three-quarter-left": ((0.95, 1.70, -5.45), (0.05, 0.85, -1.9))}


def look_at(eye, target, f, size):
    eye, target = np.asarray(eye, float), np.asarray(target, float)
    z = (target - eye) / np.linalg.norm(target - eye)
    x = np.cross(z, (0, 1, 0)); x /= np.linalg.norm(x)
    R = np.array([x, np.cross(z, x), z])  # OpenCV rows: right, down, forward
    r, _ = cv2.Rodrigues(R)
    return to_camera([*r.ravel(), *(-R @ eye)], f, size)


def solve(views, f_ref=None):
    """Joint pose solve for several views sharing one focal length (solved if f_ref is None)."""
    data = {n: (np.array([q for q, _ in pts], float), np.array([u for _, u in pts], float),
                Image.open(PHOTOS / f"{n}.jpg").size) for n, pts in views.items()}
    scale = {n: max(sz) / LONG_SIDE for n, (_, _, sz) in data.items()}

    def resid(x, f_fixed):
        f = f_fixed if f_fixed else x[-1]
        out = []
        for k, (n, (obj, img, (W, H))) in enumerate(data.items()):
            fv = f * scale[n]
            K = np.array([[fv, 0, W / 2], [0, fv, H / 2], [0, 0, 1]])
            proj, _ = cv2.projectPoints(obj, x[6 * k:6 * k + 3], x[6 * k + 3:6 * k + 6], K, None)
            out.append((proj.reshape(-1, 2) - img).ravel())
        return np.concatenate(out)

    best = None
    for f0 in ([f_ref] if f_ref else (2600, 3100, 3600, 4200)):
        x0 = []
        for n, (obj, img, (W, H)) in data.items():
            fv = f0 * scale[n]
            K = np.array([[fv, 0, W / 2], [0, fv, H / 2], [0, 0, 1]])
            _, r, t = cv2.solvePnP(obj, img, K, None, flags=cv2.SOLVEPNP_SQPNP)
            x0 += [*r.ravel(), *t.ravel()]
        x0 = np.r_[x0] if f_ref else np.r_[x0, f0]
        res = least_squares(resid, x0, args=(f_ref,), loss="soft_l1", f_scale=15)
        if best is None or res.cost < best.cost:
            best = res
    f = f_ref or best.x[-1]
    cams = {}
    for k, n in enumerate(data):
        c = to_camera(best.x[6 * k:6 * k + 6], f * scale[n], data[n][2])
        r = resid(best.x, f_ref)  # per-view rms
        lo = sum(2 * len(data[m][0]) for m in list(data)[:k])
        c["rms_px"] = float(np.sqrt(np.mean(r[lo:lo + 2 * len(data[n][0])] ** 2)))
        cams[n] = c
    return cams, f


def mark_fit(name, cam, points):
    """Debug image: measured points (green) vs reprojection (red)."""
    im = Image.open(PHOTOS / f"{name}.jpg").convert("RGB")
    d = ImageDraw.Draw(im)
    p = np.array(cam["params"])
    K = np.array([[p[6], 0, cam["cx"]], [0, p[6], cam["cy"]], [0, 0, 1]])
    proj, _ = cv2.projectPoints(np.array([q for q, _ in points], float), p[:3], p[3:6], K, None)
    for (_, (u, v)), (pu, pv) in zip(points, proj.reshape(-1, 2)):
        d.ellipse((u - 14, v - 14, u + 14, v + 14), outline=(0, 255, 0), width=5)
        d.ellipse((pu - 8, pv - 8, pu + 8, pv + 8), fill=(255, 0, 0))
    im.thumbnail((1600, 1600))
    im.save(OUT / f"fit_{name}.jpg", quality=85)


def compose(name):
    photo = Image.open(PHOTOS / f"{name}.jpg").convert("RGB")
    photo = photo.resize((round(photo.width * 1000 / photo.height), 1000), Image.LANCZOS)
    render = Image.open(OUT / f"render_{name}.png").convert("RGBA").resize(photo.size, Image.LANCZOS)
    on_grey = Image.new("RGBA", photo.size, (128, 128, 132, 255))
    on_grey.alpha_composite(render)

    side = Image.new("RGB", (photo.width * 2 + 10, 1000), (255, 255, 255))
    side.paste(photo, (0, 0))
    side.paste(on_grey.convert("RGB"), (photo.width + 10, 0))
    d = ImageDraw.Draw(side)
    d.rectangle((0, 0, 330, 26), fill=(0, 0, 0))
    d.text((6, 6), f"{name}  |  photo  vs  model", fill=(255, 255, 255))
    side.save(COMPARE / f"{name}-side.jpg", quality=88)

    ghost = render.copy()
    ghost.putalpha(render.getchannel("A").point(lambda a: a // 2))
    over = photo.convert("RGBA")
    over.alpha_composite(ghost)
    over.convert("RGB").save(COMPARE / f"{name}-overlay.jpg", quality=88)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    COMPARE.mkdir(parents=True, exist_ok=True)
    side = ("03-side-profile-right", "04-side-profile-left")
    cams, f = solve({n: VIEWS[n] for n in side})  # wheel-only views fix the lens
    for n, (eye, target) in MANUAL.items():
        size = Image.open(PHOTOS / f"{n}.jpg").size
        cams[n] = look_at(eye, target, f * max(size) / LONG_SIDE, size)
        p = np.array(cams[n]["params"])
        K = np.array([[p[6], 0, size[0] / 2], [0, p[6], size[1] / 2], [0, 0, 1]])
        proj, _ = cv2.projectPoints(np.array([q for q, _ in VIEWS[n]], float), p[:3], p[3:6], K, None)
        cams[n]["rms_px"] = float(np.sqrt(np.mean((proj.reshape(-1, 2) - [u for _, u in VIEWS[n]]) ** 2)))
    for n in VIEWS:
        if n not in side and n not in MANUAL:
            # 05 is a crop with a different effective lens: solve its f separately (01 stays approximate)
            cams.update(solve({n: VIEWS[n]}, f_ref=None if n[:2] == "05" else f)[0])
    print(f"shared focal: {f:.0f}px @ {LONG_SIDE}px long side")
    for name, c in cams.items():
        mark_fit(name, c, VIEWS[name])
        print(f"{name}: rms {c['rms_px']:.1f}px  camera {c['camera_gltf']}")
    cam_file = OUT / "cameras.json"
    cam_file.write_text(json.dumps(cams, indent=1))
    subprocess.run([BLENDER, "-b", "--python-exit-code", "1", "-P", str(HERE / "build_car.py"), "--", "--render", str(cam_file)],
                   check=True, stdout=subprocess.DEVNULL)
    for name in VIEWS:
        compose(name)
    print("compare images ->", COMPARE)


main()
