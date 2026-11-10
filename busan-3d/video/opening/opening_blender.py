# VERSION: v1.1.0 — 2026-11-10 — 오프닝(1일차 앞부분) 3D 장면 구성·렌더 (지형 부드러운 음영, 핀 축소, 샘플 설정)
"""
오프닝 3D 장면: MAP01 지도 위에서 카메라 이동, 1일차 첫 구간(부산역 → 감천) 루트 그리기,
KTX·버스 토큰 이동. 글자·사진 자리는 opening_overlay.py 가 2D 로 얹는다.

실행 (Blender 4.2 이상):
  blender --background --python opening_blender.py -- --out <프레임 폴더> [--stills] [--frames 1-528]
  --stills : timeline.json 의 check_frames 만 렌더 (구도 확인용)
결과:
  <out>/frame_0001.png ...  (3D 렌더)
  <out>/screen_points.json  (프레임별 핀·토큰의 화면 좌표 → 글자 위치용)

탈것 토큰은 임시 도형이다(MAP04 설계도가 아직 없음). 설계도가 오면 Claude 가 교체한다.
"""
import json
import logging
import math
import os
import sys
import time

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
MAP_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "assets", "MAP01_BusanMap"))
TL = json.load(open(os.path.join(HERE, "timeline.json"), encoding="utf-8"))
import runpy
MB = runpy.run_path(os.path.join(MAP_DIR, "map_build.py"), run_name="map_build")   # 좌표 변환·경유 지점을 지도와 똑같이 쓴다

log_ = logging.getLogger("opening")


def log(stage, level=logging.INFO, **kv):
    log_.log(level, "[%s] [%s] %s", stage, time.strftime("%Y-%m-%dT%H:%M:%S"), " ".join(f"{k}={v}" for k, v in kv.items()))


def args():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    out, stills, frames = None, False, None
    i = 0
    while i < len(a):
        if a[i] == "--out":
            out = a[i + 1]; i += 1
        elif a[i] == "--stills":
            stills = True
        elif a[i] == "--frames":
            s, e = a[i + 1].split("-"); frames = (int(s), int(e)); i += 1
        i += 1
    if not out:
        sys.exit("--out <폴더> 가 필요함")
    return out, stills, frames


def hex_lin(h):
    s = h.lstrip("#")
    out = []
    for k in (0, 2, 4):
        c = int(s[k:k + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


def mat(name, hex_color, emission=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = hex_lin(hex_color)
    b.inputs["Roughness"].default_value = 0.5
    if emission:
        k = "Emission Color" if "Emission Color" in b.inputs else "Emission"
        b.inputs[k].default_value = hex_lin(hex_color)
        b.inputs["Emission Strength"].default_value = emission
    return m


def box(name, size, loc, material):
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(loc), verts=bm.verts)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    me.materials.append(material)
    return me


def token(name, length, color, nose=False):
    """임시 토큰: +X 방향을 보는 둥근 상자 + 창문 띠. 1 unit = 10 km 지도용 아이콘 크기."""
    import bmesh
    w, h = length * 0.32, length * 0.30
    body = mat(f"M_Temp_{name}_Body", color, emission=0.3)
    win = mat(f"M_Temp_{name}_Window", "#121A33")
    me = box(f"{name}_mesh", (length, w, h), (0, 0, h / 2 + length * 0.06), body)
    bm = bmesh.new(); bm.from_mesh(me)
    if nose:   # 앞쪽 위 모서리를 깎아 고속열차처럼
        front_top = [v for v in bm.verts if v.co.x > 0 and v.co.z > h / 2 + length * 0.06]
        for v in front_top:
            v.co.x -= length * 0.25
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    win_me = box(f"{name}_win", (length * 0.86, w * 1.02, h * 0.28), (0, 0, h * 0.72 + length * 0.06), win)
    wobj = bpy.data.objects.new(f"{name}_Window", win_me)
    wobj.parent = obj
    bev = obj.modifiers.new("Bevel", "BEVEL"); bev.width = length * 0.05; bev.segments = 3
    obj["temporary"] = "MAP04 설계도 전 임시 도형"
    return obj, wobj


def spline_points(obj):
    return [Vector(p.co[:3]) for p in obj.data.splines[0].points]


def cumulative(pts):
    c = [0.0]
    for a, b in zip(pts, pts[1:]):
        c.append(c[-1] + (b - a).length)
    return c


def point_at(pts, cum, dist):
    dist = max(0.0, min(dist, cum[-1]))
    for i in range(1, len(cum)):
        if cum[i] >= dist:
            t = (dist - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-12)
            p = pts[i - 1].lerp(pts[i], t)
            d = pts[i] - pts[i - 1]
            return p, math.atan2(d.y, d.x)
    return pts[-1], 0.0


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s", stream=sys.stdout)
    out, stills, frames = args()
    os.makedirs(out, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=os.path.join(MAP_DIR, "BusanMap.blend"))
    sc = bpy.context.scene
    fs, fe = TL["frame_start"], TL["frame_end"]
    sc.frame_start, sc.frame_end = fs, fe
    sc.render.fps = TL["fps"]
    sc.render.resolution_x, sc.render.resolution_y = TL["resolution"]
    sc.render.resolution_percentage = int(TL.get("render", {}).get("resolution_percentage", 100))
    sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in {e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items} else "BLENDER_EEVEE"
    R = TL.get("render", {})
    sc.eevee.taa_render_samples = int(R.get("taa_samples", 16))
    if R.get("terrain_smooth"):
        tm = bpy.data.objects["MAP01_BusanMap_Terrain_L0"].data
        tm.polygons.foreach_set("use_smooth", [True] * len(tm.polygons))   # 가까이서 보이는 각진 면을 부드럽게
    ps = float(R.get("pin_scale", 1.0))
    for o in bpy.data.objects:
        if o.name.startswith("MAP01_BusanMap_Pin"):
            o.scale = (ps, ps, ps)
    log("SETUP", map=os.path.join(MAP_DIR, "BusanMap.blend"), engine=sc.render.engine, frames=f"{fs}-{fe}", res=TL["resolution"],
        samples=sc.eevee.taa_render_samples, pin_scale=R.get("pin_scale", 1.0), terrain_smooth=bool(R.get("terrain_smooth")))

    for n in TL["hide_objects"]:
        o = bpy.data.objects[n]; o.hide_render = o.hide_viewport = True

    # ── 1일차 루트: 부산역 → 감천 구간만 그리기 ──
    route = bpy.data.objects[TL["route"]["object"]]
    pts = spline_points(route)
    cum = cumulative(pts)
    def pin(key):
        return bpy.data.objects["MAP01_BusanMap_Pin" + "".join(p.capitalize() for p in key.split("_")) + "_L0"]
    target_pin = pin(TL["route"]["to_place"])
    gi = min(range(len(pts)), key=lambda i: (pts[i].xy - target_pin.location.xy).length)
    frac = cum[gi] / cum[-1]
    cu = route.data
    cu.animation_data_clear()
    cu.bevel_factor_mapping_end = "SPLINE"
    cu.bevel_factor_end = 0.0
    cu.keyframe_insert("bevel_factor_end", frame=TL["route"]["draw_start"])
    cu.bevel_factor_end = frac
    cu.keyframe_insert("bevel_factor_end", frame=TL["route"]["draw_end"])
    fc = cu.animation_data.action.fcurves[0] if hasattr(cu.animation_data.action, "fcurves") else None
    log("ROUTE", object=route.name, points=len(pts), to=TL["route"]["to_place"], point_index=gi,
        fraction=f"{frac:.4f}", leg_units=f"{cum[gi]:.4f}", leg_km=f"{cum[gi] * 10:.1f}")

    def route_fraction(f):
        if fc is not None:
            return fc.evaluate(f)
        sc.frame_set(f); return cu.bevel_factor_end

    # ── 토큰 ──
    col = bpy.data.collections.new("V01_OpeningTemp"); sc.collection.children.link(col)
    bus, bus_w = token("TempBusToken", 0.035, TL["bus_token"]["color"])
    ktx, ktx_w = token("TempKTXToken", 0.06, TL["ktx_token"]["color"], nose=True)
    for o in (bus, bus_w, ktx, ktx_w):
        col.objects.link(o)
    b0, b1 = TL["bus_token"]["start"], TL["bus_token"]["end"]
    for f in range(fs, fe + 1):
        visible = b0 - 6 <= f <= b1 + 40
        d = route_fraction(min(max(f, b0), b1)) * cum[-1]
        p, ang = point_at(pts, cum, d)
        bus.location = p + Vector((0, 0, 0.002)); bus.rotation_euler = (0, 0, ang)
        bus.scale = (1, 1, 1) if visible else (0, 0, 0)
        bus.keyframe_insert("location", frame=f); bus.keyframe_insert("rotation_euler", frame=f); bus.keyframe_insert("scale", frame=f)
    # KTX: 부산진(1003 경유 지점과 같은 위치) → 부산역, 루트 점에서 높이를 가져온다
    st = pin(TL["ktx_token"]["to_place"]).location.copy()
    vp = MB["VIA_POINTS"][TL["ktx_token"]["from_via"]]
    bj = Vector(MB["latlon_to_xy"](vp["lat"], vp["lon"]))
    near_bj = min(pts, key=lambda q: (q.xy - bj).length).copy()   # 부산진역 정류장과 가장 가까운 루트 점(높이 포함)
    k0, k1 = TL["ktx_token"]["start"], TL["ktx_token"]["end"]
    ang = math.atan2(st.y - near_bj.y, st.x - near_bj.x)
    for f in range(fs, fe + 1):
        t = min(max((f - k0) / (k1 - k0), 0.0), 1.0)
        t = 1 - (1 - t) ** 3   # 도착하며 감속
        ktx.location = near_bj.lerp(st + Vector((0, 0, 0.004)), t)
        ktx.rotation_euler = (0, 0, ang)
        ktx.scale = (1, 1, 1) if k0 - 6 <= f <= 252 else (0, 0, 0)
        ktx.keyframe_insert("location", frame=f); ktx.keyframe_insert("rotation_euler", frame=f); ktx.keyframe_insert("scale", frame=f)
    log("TOKENS", bus=f"{b0}-{b1}", ktx=f"{k0}-{k1}", ktx_from=f"{near_bj.x:.4f},{near_bj.y:.4f}",
        busanjin_xy=f"{bj.x:.4f},{bj.y:.4f}", gap=f"{(near_bj.xy - bj).length:.4f}", note="임시 도형(MAP04 전)")

    # ── 카메라 ──
    cd = bpy.data.cameras.new("V01_Cam"); cd.lens = TL["camera_lens_mm"]; cd.clip_start = 0.005; cd.clip_end = 50
    cam = bpy.data.objects.new("V01_Cam", cd); col.objects.link(cam)
    tgt = bpy.data.objects.new("V01_CamTarget", None); col.objects.link(tgt)
    tr = cam.constraints.new("TRACK_TO"); tr.target = tgt; tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"
    for k in TL["camera_keys"]:
        cam.location = k["loc"]; cam.keyframe_insert("location", frame=k["frame"])
        tgt.location = k["target"]; tgt.keyframe_insert("location", frame=k["frame"])
    sc.camera = cam
    log("CAMERA", keys=len(TL["camera_keys"]), lens=TL["camera_lens_mm"])

    # ── 화면 좌표 (글자 위치) ──
    keys = {l["place"] for l in TL["labels"]}
    screen = {}
    W, H = TL["resolution"]
    for f in range(fs, fe + 1):
        sc.frame_set(f)
        row = {}
        for k in keys:
            o = pin(k)
            top = o.matrix_world @ Vector((0, 0, 0.075))   # 핀 머리 조금 위 (scale 반영)
            v = world_to_camera_view(sc, cam, top)
            row[k] = [round(v.x * W, 1), round((1 - v.y) * H, 1), round(v.z, 4)]
        v = world_to_camera_view(sc, cam, bus.matrix_world.translation + Vector((0, 0, 0.03)))
        row["bus"] = [round(v.x * W, 1), round((1 - v.y) * H, 1), round(v.z, 4)]
        screen[f] = row
    with open(os.path.join(out, "screen_points.json"), "w", encoding="utf-8") as fh:
        json.dump(screen, fh)
    log("SCREEN", frames=len(screen), file="screen_points.json")

    # ── 렌더 ──
    sc.render.image_settings.file_format = "PNG"
    if stills:
        for f in TL["check_frames"]:
            sc.frame_set(f)
            sc.render.filepath = os.path.join(out, f"frame_{f:04d}.png")
            t = time.time(); bpy.ops.render.render(write_still=True)
            log("RENDER", frame=f, seconds=f"{time.time() - t:.1f}")
    else:
        a, b = frames or (fs, fe)
        sc.frame_start, sc.frame_end = a, b
        sc.render.filepath = os.path.join(out, "frame_")
        t = time.time(); bpy.ops.render.render(animation=True)
        log("RENDER", frames=f"{a}-{b}", seconds=f"{time.time() - t:.1f}", per_frame=f"{(time.time() - t) / (b - a + 1):.2f}")
    sys.stdout.flush()
    if not bpy.app.binary_path:   # pip bpy 모듈로 실행했을 때 종료 충돌 회피
        os._exit(0)


main()

# CHANGELOG
# v1.1.0 — 2026-11-10 — 지형 부드러운 음영, 핀 크기 조절, 렌더 샘플을 timeline.json 에서 읽음
# v1.0.0 — 2026-11-10 — 최초 작성
