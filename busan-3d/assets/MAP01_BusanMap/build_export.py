# VERSION: v1.0.2 — 2026-11-10 — MAP01 빌드 → 미리보기 렌더 → .blend/.glb 저장
"""
실행: blender --background --python build_export.py
      (또는 bpy 모듈이 있는 파이썬: python build_export.py)
결과: BusanMap.blend, BusanMap.glb, previews/top.png, previews/oblique.png, validation.json
"""
import json
import math
import os
import runpy
import sys
import time

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ns = runpy.run_path(os.path.join(HERE, "map_build.py"), run_name="map_build")
g = ns["main"].__globals__
log = g["log"]

positions = g["main"]()
if positions is None:
    sys.exit("map_build 실패 — 위 로그 확인")

# 핀 위치의 실제 해발 고도(m) 기록
sampler = g["HeightSampler"]()
elev = {}
for p in g["PLACES"]:
    z = sampler.height(p["lat"], p["lon"])
    elev[p["key"]] = round(z / g["HEIGHT_EXAGGERATION"] * 1000.0 * g["KM_PER_UNIT"], 1)
log("ELEVATION", **{k: f"{v}m" for k, v in elev.items()})

sc = bpy.context.scene
for o in list(sc.objects):
    if o.name in ("Cube", "Camera", "Light"):
        bpy.data.objects.remove(o, do_unlink=True)
sc.frame_set(217)   # 루트 3일치가 모두 그려진 프레임 (1일차 1~73, 2일차 73~145, 3일차 145~217)

# 조명·배경 (미리보기용, [설정])
sun_d = bpy.data.lights.get("PreviewSun") or bpy.data.lights.new("PreviewSun", "SUN")
sun_d.energy, sun_d.angle = 3.0, math.radians(3)
sun = bpy.data.objects.get("PreviewSun") or bpy.data.objects.new("PreviewSun", sun_d)
if sun.name not in sc.collection.objects:
    sc.collection.objects.link(sun)
sun.rotation_euler = (math.radians(50), 0, math.radians(-35))
world = sc.world or bpy.data.worlds.new("World")
sc.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs["Color"].default_value = g["hex_to_linear_rgba"]("#A9D6F0")
bg.inputs["Strength"].default_value = 0.6

sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 48
sc.cycles.use_denoising = True
sc.render.film_transparent = False


def camera(name, ortho, loc, rot, scale_or_lens):
    cd = bpy.data.cameras.get(name) or bpy.data.cameras.new(name)
    cd.type = "ORTHO" if ortho else "PERSP"
    if ortho:
        cd.ortho_scale = scale_or_lens
    else:
        cd.lens = scale_or_lens
    cd.clip_end = 100
    co = bpy.data.objects.get(name) or bpy.data.objects.new(name, cd)
    if co.name not in sc.collection.objects:
        sc.collection.objects.link(co)
    co.location, co.rotation_euler = loc, rot
    return co


s, w, n, e = g["HEIGHTMAP"]["bounds"]
x0, y0 = g["latlon_to_xy"](s, w)
x1, y1 = g["latlon_to_xy"](n, e)
cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
os.makedirs(os.path.join(HERE, "previews"), exist_ok=True)
shots = {
    "top": camera("PreviewTop", True, (cx, cy, 5.0), (0, 0, 0), (x1 - x0) * 1.02),
    "oblique": camera("PreviewOblique", False, (cx - 0.35, cy - 2.6, 1.55), (math.radians(58), 0, math.radians(-8)), 32),
}
res = {"top": (1600, 1388), "oblique": (1600, 900)}
for key, cam in shots.items():
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = res[key]
    sc.render.filepath = os.path.join(HERE, "previews", f"{key}.png")
    t = time.time()
    bpy.ops.render.render(write_still=True)
    log("RENDER", shot=key, file=f"previews/{key}.png", seconds=f"{time.time() - t:.1f}")
sc.camera = shots["oblique"]

# 저장
bpy.ops.file.pack_all()
bpy.context.preferences.filepaths.save_version = 0   # BusanMap.blend1 백업 파일을 만들지 않음
blend = os.path.join(HERE, "BusanMap.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True)
col = bpy.data.collections[f"{g['MAP_ID']}_{g['MAP_NAME']}"]
for o in sc.objects:
    o.select_set(o.name in col.objects)
glb = os.path.join(HERE, "BusanMap.glb")
# glb 는 정지 모델로 내보낸다: 루트 '그리기' 애니메이션을 빼고 전체 길이로 고정 (.blend 는 위에서 애니메이션 포함 저장됨)
for o in col.objects:
    if "Route" in o.name:
        o.data.animation_data_clear()
        o.data.bevel_factor_end = 1.0
bpy.ops.export_scene.gltf(filepath=glb, export_format="GLB", use_selection=True, export_apply=True,
                          export_animations=False)

# 검증 기록
dg = bpy.context.evaluated_depsgraph_get()
tris = {}
for o in col.objects:
    if o.type in ("MESH", "CURVE", "FONT"):
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        tris[o.name] = sum(len(p.vertices) - 2 for p in me.polygons)
        ev.to_mesh_clear()
routes = {o.name: o.get("path_km") for o in col.objects if "Route" in o.name}
report = {
    "map": "MAP01_BusanMap", "spec_version": g["SPEC_VERSION"], "blender": bpy.app.version_string,
    "objects": len(col.objects), "triangles_total": sum(tris.values()),
    "triangles_terrain": tris.get("MAP01_BusanMap_Terrain_L0"), "route_path_km": routes,
    "pin_ground_elevation_m": elev, "heightmap": g["HEIGHTMAP"],
    "files": {"blend_MB": round(os.path.getsize(blend) / 1e6, 2), "glb_MB": round(os.path.getsize(glb) / 1e6, 2)},
}
with open(os.path.join(HERE, "validation.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
log("EXPORT", blend=f"{report['files']['blend_MB']}MB", glb=f"{report['files']['glb_MB']}MB",
    triangles=report["triangles_total"], terrain_tris=report["triangles_terrain"])

if not bpy.app.binary_path:
    # bpy 모듈(pip 설치)로 실행했을 때만: 종료 정리 단계의 충돌을 피한다. Blender 프로그램 안에서는 실행되지 않음
    sys.stdout.flush()
    os._exit(0)

# CHANGELOG
# v1.0.2 — 2026-11-10 — bpy 모듈로 실행 시 종료 충돌 회피, .blend1 백업 파일 만들지 않음
# v1.0.1 — 2026-11-10 — glb 에서 루트가 빠지던 문제 수정(애니메이션 첫 프레임 길이 0 → 정지 모델로 내보냄)
# v1.0.0 — 2026-11-10 — 최초 작성
