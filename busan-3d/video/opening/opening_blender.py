# VERSION: v1.2.0 — 2026-11-11 — 오프닝(1일차 앞부분) 3D 장면 구성·렌더 (MAP04 탈것 토큰 사용)
"""
오프닝 3D 장면: MAP01 지도 위에서 카메라 이동, 1일차 첫 구간(부산역 → 감천) 루트 그리기,
KTX·버스 토큰 이동. 글자·사진 자리는 opening_overlay.py 가 2D 로 얹는다.

실행 (Blender 4.2 이상):
  blender --background --python opening_blender.py -- --out <프레임 폴더> [--stills] [--frames 1-528]
  --stills : timeline.json 의 check_frames 만 렌더 (구도 확인용)
결과:
  <out>/frame_0001.png ...  (3D 렌더)
  <out>/screen_points.json  (프레임별 핀·토큰의 화면 좌표 → 글자 위치용)

탈것 토큰은 MAP04 모델(TransitTokens.blend)에서 BusStd·KTX 를 불러온다. 표시 배율·높이는 timeline.json tokens.
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

    # ── 탈것 토큰: MAP04 모델을 불러온다 ──
    T = TL["tokens"]
    col = bpy.data.collections.new("V01_Opening"); sc.collection.children.link(col)
    tok_blend = os.path.normpath(os.path.join(HERE, T["blend"]))
    want = ("MAP04_TransitTokens_BusStd", "MAP04_TransitTokens_KTX")
    with bpy.data.libraries.load(tok_blend, link=False) as (src, dst):
        dst.objects = [n for n in src.objects if n.startswith(want)]
    for o in dst.objects:
        col.objects.link(o)
    bus, ktx = bpy.data.objects[T["bus_root"]], bpy.data.objects[T["ktx_root"]]
    wheels = [o for o in bus.children if "Wheel" in o.name]
    for w in wheels:
        w.rotation_mode = "ZYX"            # (0, 90°, 회전) → 원기둥 축 둘레로 굴러감
    S, LIFT, DAY1_LIFT = T["scale"], T["lift"], 0.004   # 1일차 루트 점은 지면 + 0.004
    def face(dx, dy):                       # 토큰 정면이 -Y 라서: yaw = atan2(Δx, -Δy) (MAP04 spec 10번)
        return math.atan2(dx, -dy)
    b0, b1 = TL["bus_token"]["start"], TL["bus_token"]["end"]
    prev, rolled = None, 0.0
    for f in range(fs, fe + 1):
        visible = b0 - 6 <= f <= TL["bus_token"].get("hide_after", b1)
        d = route_fraction(min(max(f, b0), b1)) * cum[-1]
        p, _ = point_at(pts, cum, d)
        p2, _ = point_at(pts, cum, d + 0.01)
        if prev is not None:
            rolled += (p - prev).length / S / T["bus_wheel_radius_m"]   # 굴러간 각도(rad) = 토큰 기준 이동거리 ÷ 반지름
        prev = p.copy()
        bus.location = p + Vector((0, 0, LIFT - DAY1_LIFT))
        bus.rotation_euler = (0, 0, face(p2.x - p.x, p2.y - p.y))
        bus.scale = (S, S, S) if visible else (0, 0, 0)
        for k in ("location", "rotation_euler", "scale"):
            bus.keyframe_insert(k, frame=f)
        for w in wheels:
            w.rotation_euler = (0, math.radians(90), -rolled)
            w.keyframe_insert("rotation_euler", frame=f)
    # KTX: 부산진(1003 경유 지점과 같은 위치) → 부산역
    st = pin(TL["ktx_token"]["to_place"]).location.copy()
    vp = MB["VIA_POINTS"][TL["ktx_token"]["from_via"]]
    bj = Vector(MB["latlon_to_xy"](vp["lat"], vp["lon"]))
    near_bj = min(pts, key=lambda q: (q.xy - bj).length).copy()   # 부산진역 정류장과 가장 가까운 루트 점(높이 포함)
    k0, k1 = TL["ktx_token"]["start"], TL["ktx_token"]["end"]
    a0 = near_bj + Vector((0, 0, LIFT - DAY1_LIFT))
    a1 = st + Vector((0, 0, LIFT))
    for f in range(fs, fe + 1):
        t = min(max((f - k0) / (k1 - k0), 0.0), 1.0)
        t = 1 - (1 - t) ** 3   # 도착하며 감속
        ktx.location = a0.lerp(a1, t)
        ktx.rotation_euler = (0, 0, face(a1.x - a0.x, a1.y - a0.y))
        ktx.scale = (S, S, S) if k0 - 6 <= f <= 252 else (0, 0, 0)
        for k in ("location", "rotation_euler", "scale"):
            ktx.keyframe_insert(k, frame=f)
    log("TOKENS", source=os.path.relpath(tok_blend, HERE), bus=T["bus_root"], ktx=T["ktx_root"], scale=S, lift=LIFT,
        bus_frames=f"{b0}-{b1}", ktx_frames=f"{k0}-{k1}", ktx_from=f"{near_bj.x:.4f},{near_bj.y:.4f}",
        busanjin_xy=f"{bj.x:.4f},{bj.y:.4f}", wheel_turns=f"{rolled / (2 * math.pi):.1f}")

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
        v = world_to_camera_view(sc, cam, bus.matrix_world.translation + Vector((0, 0, 0.035)))
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
# v1.2.0 — 2026-11-11 — 임시 상자 토큰 → MAP04 BusStd·KTX, 정면 -Y 기준 방향, 바퀴 굴림, 배율 0.03
# v1.1.0 — 2026-11-10 — 지형 부드러운 음영, 핀 크기 조절, 렌더 샘플을 timeline.json 에서 읽음
# v1.0.0 — 2026-11-10 — 최초 작성
