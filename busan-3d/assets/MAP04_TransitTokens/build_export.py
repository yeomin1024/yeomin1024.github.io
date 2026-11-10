# VERSION: v1.0.0 — 2026-11-11 — MAP04 토큰 빌드 → 미리보기(직교 3면·사시·지도 위 배치) → .blend/.glb 저장
"""
실행: blender --background --python build_export.py
결과: TransitTokens.blend, TransitTokens.glb, previews/_tiles(→ make_sheet.py 로 sheet.png), previews/perspective.png,
      previews/on_map_spec_0.08.png, previews/on_map_adjusted_0.03.png, validation.json
"""
import json
import math
import os
import runpy
import sys
import time

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
MAP_BLEND = os.path.normpath(os.path.join(HERE, "..", "MAP01_BusanMap", "BusanMap.blend"))
ns = runpy.run_path(os.path.join(HERE, "blockout.py"), run_name="blockout")
log, hexl = ns["log"], ns["hex_to_linear_rgba"]
objs, rep = ns["build_tokens"]()
sc = bpy.context.scene
for n in ("Cube", "Camera", "Light"):
    if n in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[n], do_unlink=True)
roots = {k: objs[k] for k in ns["ROOTS"]}


def eevee(res):
    sc.render.engine = "BLENDER_EEVEE_NEXT"
    sc.eevee.taa_render_samples = 16
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100


def world(hex_color, strength):
    w = sc.world or bpy.data.worlds.new("World")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = hexl(hex_color)
    bg.inputs["Strength"].default_value = strength


def sun(name, rot, energy):
    d = bpy.data.lights.get(name) or bpy.data.lights.new(name, "SUN")
    d.energy = energy
    o = bpy.data.objects.get(name) or bpy.data.objects.new(name, d)
    if o.name not in sc.collection.objects:
        sc.collection.objects.link(o)
    o.rotation_euler = rot
    return o


def cam(name, ortho, loc, rot, val):
    d = bpy.data.cameras.get(name) or bpy.data.cameras.new(name)
    d.type = "ORTHO" if ortho else "PERSP"
    if ortho:
        d.ortho_scale = val
    else:
        d.lens = val
    d.clip_start, d.clip_end = 0.01, 200
    o = bpy.data.objects.get(name) or bpy.data.objects.new(name, d)
    if o.name not in sc.collection.objects:
        sc.collection.objects.link(o)
    o.location, o.rotation_euler = loc, rot
    sc.camera = o
    return o


def render(path):
    sc.render.filepath = path
    t = time.time()
    bpy.ops.render.render(write_still=True)
    log("RENDER", file=os.path.relpath(path, HERE), seconds=f"{time.time() - t:.1f}")


def show_only(root):
    for r in roots.values():
        hide = r is not root
        for o in [r] + list(r.children):
            o.hide_render = hide


os.makedirs(os.path.join(HERE, "previews"), exist_ok=True)
tmp = os.path.join(HERE, "previews", "_tiles")
os.makedirs(tmp, exist_ok=True)
world("#E6E8EC", 1.0)
sun("KeySun", (math.radians(40), 0, math.radians(30)), 3.0)
eevee((480, 300))
# 직교 3면: 토큰마다 정면(-Y 에서), 오른쪽(+X 에서), 윗면(+Z 에서)
views = {"front": ((0, -6, 0.55), (math.radians(90), 0, 0)),
         "side": ((6, 0, 0.55), (math.radians(90), 0, math.radians(90))),
         "top": ((0, 0, 6), (0, 0, math.radians(90)))}   # 윗면: 길이 방향이 가로가 되게 돌림 (앞 = 왼쪽)
for rname, r in roots.items():
    show_only(r)
    x = r.location.x
    for vname, (loc, rot) in views.items():
        scale = 3.2 if vname != "front" else 1.9
        cam("OrthoCam", True, (loc[0] + x, loc[1], loc[2]), rot, scale)
        render(os.path.join(tmp, f"{rname}_{vname}.png"))
show_only(None)
for r in roots.values():
    for o in [r] + list(r.children):
        o.hide_render = False
# 사시 전체
eevee((1600, 700))
cam("PerspCam", False, (6.5, -9.5, 4.2), (math.radians(68), 0, math.radians(34)), 50)
render(os.path.join(HERE, "previews", "perspective.png"))

# 지도 위 배치 시험 (spec 13: 배율 0.08, 지형 위 0.04) — MAP01 을 불러와 부산역 근처에 여섯 개를 놓는다
with bpy.data.libraries.load(MAP_BLEND, link=False) as (src, dst):
    dst.objects = [n for n in src.objects if n.startswith("MAP01_BusanMap_")]
map_col = bpy.data.collections.new("MAP01_preview")
sc.collection.children.link(map_col)
for o in dst.objects:
    if o is not None:
        map_col.objects.link(o)
        if "RouteDay2" in o.name or "RouteDay3" in o.name:
            o.hide_render = True
terrain = bpy.data.objects["MAP01_BusanMap_Terrain_L0"]
terrain.data.polygons.foreach_set("use_smooth", [True] * len(terrain.data.polygons))
station = bpy.data.objects["MAP01_BusanMap_PinBusanStation_L0"].location.copy()
world("#A9D6F0", 0.6)
eevee((1280, 720))
cam("MapCam", False, (station.x + 0.02, station.y - 0.95, 0.50), (0, 0, 0), 32)   # 오프닝 부산역 장면과 비슷한 거리(약 0.9)
tgt = bpy.data.objects.new("MapCamTarget", None)
sc.collection.objects.link(tgt)
tgt.location = station + Vector((0.02, -0.05, 0.0))
tc = sc.camera.constraints.new("TRACK_TO")
tc.target, tc.track_axis, tc.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"
# 설계도 값(배율 0.08, 높이 0.04)과 조정안(0.03, 0.015)을 같은 구도로 비교
for tag, scale, lift in (("spec_0.08", 0.08, 0.04), ("adjusted_0.03", 0.03, 0.015)):
    gap = 2.6 * scale            # 토큰끼리 겹치지 않게 Y 방향으로 띄움
    for i, r in enumerate(roots.values()):
        r.scale = (scale, scale, scale)
        r.location = station + Vector((-0.06, (i - 2.5) * gap * 0.45, lift))
        r.rotation_euler = (0, 0, math.radians(-90))     # 정면(-Y)이 -X 쪽을 봄
    render(os.path.join(HERE, "previews", f"on_map_{tag}.png"))

# 지도 미리보기용 물체를 지우고 원래 배치로 돌린 뒤 저장
for o in list(map_col.objects):
    bpy.data.objects.remove(o, do_unlink=True)
bpy.data.collections.remove(map_col)
for o in ("MapCam", "MapCamTarget", "OrthoCam", "PerspCam"):
    if o in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[o], do_unlink=True)
for k, r in roots.items():
    r.scale = (1, 1, 1)
    r.rotation_euler = (0, 0, 0)
    r.location = (ns["ROOTS"][k]["x"], 0, 0)
bpy.ops.outliner.orphans_purge(do_recursive=True)
bpy.context.preferences.filepaths.save_version = 0
blend = os.path.join(HERE, "TransitTokens.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True)
col = bpy.data.collections["MAP04_TransitTokens"]
for o in sc.objects:
    o.select_set(o.name in col.objects)
glb = os.path.join(HERE, "TransitTokens.glb")
bpy.ops.export_scene.gltf(filepath=glb, export_format="GLB", use_selection=True, export_apply=True, export_animations=False)
with open(os.path.join(HERE, "validation.json"), "w", encoding="utf-8") as f:
    json.dump({"asset": "MAP04_TransitTokens", "spec_version": ns["SPEC_VERSION"], "blender": bpy.app.version_string,
               "roots": rep, "total_triangles": sum(r["triangles"] for r in rep.values()), "tri_budget_total": ns["TRI_BUDGET"],
               "files": {"blend_MB": round(os.path.getsize(blend) / 1e6, 3), "glb_MB": round(os.path.getsize(glb) / 1e6, 3)}},
              f, ensure_ascii=False, indent=2)
log("EXPORT", blend=blend, glb=glb)
sys.stdout.flush()
if not bpy.app.binary_path:
    os._exit(0)

# CHANGELOG
# v1.0.0 — 2026-11-11 — 최초 작성
