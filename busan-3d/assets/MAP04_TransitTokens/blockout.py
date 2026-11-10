# VERSION: v1.0.0 — 2026-11-11 — MAP04 탈것 토큰 6종 블록아웃 (spec.md v1.0, templates/blockout_template.py v1.1.0 기반)
"""
MAP04 탈것 토큰 6종 — Claude 모델링

실행: blender --background --python blockout.py   (또는 bpy 모듈 파이썬)
결과: TransitTokens.blend, TransitTokens.glb, previews/*.png, validation.json (build_tokens() 끝에서 저장)

설계도(spec.md v1.0)와 다른 점은 PARTS 의 note 에 [조정] 으로 적었다:
  앞 유리·램프가 차체 앞면 안쪽에 묻혀 보이지 않는 부품은 앞면보다 1 cm 나오게 옮겼다(전체 길이 오차 1 cm 이내).
"""
import logging
import math
import os
import re
import sys
import time

import bpy
import bmesh
from mathutils import Euler, Vector

IN_BLENDER = True
HERE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────
# 1. 에셋 정보
# ─────────────────────────────────────────────
ASSET_ID = "MAP04"
ASSET_NAME = "TransitTokens"
SPEC_VERSION = "v1.0"
LOD = "L0"
EXPECTED_DIMS_M = (0.0, 0.0, 0.0)     # 토큰마다 따로 검사 (ROOTS 참고). 전체 크기 검사는 쓰지 않음
TRI_BUDGET = 2770
TOLERANCE_M = 0.01
LOG_LEVEL = logging.INFO

# 토큰별 목표 (spec 14번) 와 보기용 배치 위치(Root 위치, 형상 원점은 각 Root 바닥 중앙)
ROOTS = {
    "BusStdRoot":     {"dims": (0.90, 2.40, 0.90), "tri": 450, "x": -4.125},
    "BusExpressRoot": {"dims": (0.90, 2.40, 0.85), "tri": 450, "x": -2.475},
    "BusVillageRoot": {"dims": (0.90, 1.80, 0.85), "tri": 420, "x": -0.825},
    "KTXRoot":        {"dims": (0.75, 2.80, 0.75), "tri": 500, "x": 0.825},
    "BeachTrainRoot": {"dims": (0.90, 2.10, 0.85), "tri": 450, "x": 2.475},
    "SkyCapsuleRoot": {"dims": (0.90, 1.10, 1.10), "tri": 500, "x": 4.125},
}

# ─────────────────────────────────────────────
# 2. 재질 (spec 8번)
# ─────────────────────────────────────────────
MATERIALS = {
    "BusBlue":      {"base_hex": "#2E6FB7", "roughness": 0.62, "metallic": 0.0},
    "ExpressRed":   {"base_hex": "#C8423B", "roughness": 0.62, "metallic": 0.0},
    "VillageGreen": {"base_hex": "#4E9A5B", "roughness": 0.62, "metallic": 0.0},
    "OffWhite":     {"base_hex": "#F2EFE6", "roughness": 0.58, "metallic": 0.0},
    "SeaDeep":      {"base_hex": "#0E4C77", "roughness": 0.60, "metallic": 0.0},
    "SeaShallow":   {"base_hex": "#3FA7B5", "roughness": 0.60, "metallic": 0.0},
    "SunsetCoral":  {"base_hex": "#F28C5B", "roughness": 0.60, "metallic": 0.0},
    "DarkGlass":    {"base_hex": "#121A33", "roughness": 0.25, "metallic": 0.0},   # 밤: 발광 #121A33 0.2 (spec 11)
    "SkyGlass":     {"base_hex": "#A9D6F0", "roughness": 0.25, "metallic": 0.0},   # 밤: 발광 #A9D6F0 0.2
    "Asphalt":      {"base_hex": "#3A3D42", "roughness": 0.78, "metallic": 0.0},
}

# ─────────────────────────────────────────────
# 3. 부품 (spec 5번). 베벨 세그먼트·원기둥 분할 수는 삼각형 예산에 맞춰 Claude 가 정함(spec 14 허용)
# ─────────────────────────────────────────────
def P(name, shape, size, loc, parent, mat=None, rot=(0, 0, 0), bevel=None, mirror=None, seg=None, note="[설정]"):
    d = {"name": name, "shape": shape, "size": size, "location": loc, "rotation_deg": rot, "pivot": "center",
         "parent": parent, "note": note}
    if mat: d["material"] = mat
    if bevel: d["bevel"] = {"width": bevel[0], "segments": bevel[1]}
    if mirror: d["mirror"] = mirror
    if seg: d["segments"] = seg
    return d

W = 8    # 바퀴 원기둥 분할 수 (삼각형 예산)
PARTS = [
    P("BusStdRoot", "empty", (0.10, 0.10, 0.10), (0, 0, 0), None),
    P("BusStdBody", "cube", (0.86, 2.40, 0.62), (0, 0, 0.53), "BusStdRoot", "BusBlue", bevel=(0.06, 2)),
    P("BusStdRoof", "cube", (0.90, 2.16, 0.12), (0, 0.05, 0.84), "BusStdRoot", "BusBlue", bevel=(0.05, 2)),
    P("BusStdFrontGlass", "cube", (0.72, 0.04, 0.32), (0, -1.185, 0.64), "BusStdRoot", "DarkGlass", bevel=(0.02, 1),
      note="[조정] y -1.17→-1.185 (차체 앞면 -1.20 안에 묻혀 안 보임 → 앞면보다 5 mm 나오게)"),
    P("BusStdSideGlassR", "cube", (0.03, 1.50, 0.30), (0.435, -0.10, 0.65), "BusStdRoot", "DarkGlass", mirror="X"),
    P("BusStdWheelFR", "cylinder", (0.30, 0.30, 0.10), (0.40, -0.72, 0.15), "BusStdRoot", "Asphalt", rot=(0, 90, 0), mirror="X", seg=W),
    P("BusStdWheelRR", "cylinder", (0.30, 0.30, 0.10), (0.40, 0.72, 0.15), "BusStdRoot", "Asphalt", rot=(0, 90, 0), mirror="X", seg=W),
    P("BusStdLampR", "cube", (0.12, 0.03, 0.10), (0.25, -1.19, 0.36), "BusStdRoot", "OffWhite", mirror="X",
      note="[조정] y -1.18→-1.19 (묻힘 → 5 mm 나오게)"),

    P("BusExpressRoot", "empty", (0.10, 0.10, 0.10), (0, 0, 0), None),
    P("BusExpressBody", "cube", (0.86, 2.40, 0.58), (0, 0, 0.50), "BusExpressRoot", "ExpressRed", bevel=(0.06, 2)),
    P("BusExpressRoof", "cube", (0.90, 2.14, 0.11), (0, 0.06, 0.795), "BusExpressRoot", "ExpressRed", bevel=(0.05, 2)),
    P("BusExpressFrontGlass", "cube", (0.72, 0.05, 0.30), (0, -1.16, 0.62), "BusExpressRoot", "DarkGlass", rot=(-12, 0, 0), bevel=(0.02, 1),
      note="[설정] 기울인 유리: 아래쪽이 앞면 밖으로 나옴(설계도 그대로)"),
    P("BusExpressSideGlassR", "cube", (0.03, 1.62, 0.29), (0.435, -0.04, 0.62), "BusExpressRoot", "DarkGlass", mirror="X"),
    P("BusExpressWheelFR", "cylinder", (0.30, 0.30, 0.10), (0.40, -0.72, 0.15), "BusExpressRoot", "Asphalt", rot=(0, 90, 0), mirror="X", seg=W),
    P("BusExpressWheelRR", "cylinder", (0.30, 0.30, 0.10), (0.40, 0.72, 0.15), "BusExpressRoot", "Asphalt", rot=(0, 90, 0), mirror="X", seg=W),
    P("BusExpressLampR", "cube", (0.12, 0.03, 0.09), (0.25, -1.19, 0.34), "BusExpressRoot", "OffWhite", mirror="X",
      note="[조정] y -1.18→-1.19 (묻힘 → 5 mm 나오게)"),

    P("BusVillageRoot", "empty", (0.10, 0.10, 0.10), (0, 0, 0), None),
    P("BusVillageBody", "cube", (0.86, 1.80, 0.60), (0, 0, 0.51), "BusVillageRoot", "VillageGreen", bevel=(0.06, 2)),
    P("BusVillageRoof", "cube", (0.90, 1.58, 0.11), (0, 0.03, 0.795), "BusVillageRoot", "VillageGreen", bevel=(0.05, 2)),
    P("BusVillageFrontGlass", "cube", (0.72, 0.04, 0.31), (0, -0.885, 0.62), "BusVillageRoot", "DarkGlass", bevel=(0.02, 1),
      note="[조정] y -0.87→-0.885 (묻힘 → 5 mm 나오게)"),
    P("BusVillageSideGlassR", "cube", (0.03, 1.02, 0.29), (0.435, -0.04, 0.63), "BusVillageRoot", "DarkGlass", mirror="X"),
    P("BusVillageWheelFR", "cylinder", (0.29, 0.29, 0.10), (0.40, -0.51, 0.145), "BusVillageRoot", "Asphalt", rot=(0, 90, 0), mirror="X", seg=W),
    P("BusVillageWheelRR", "cylinder", (0.29, 0.29, 0.10), (0.40, 0.51, 0.145), "BusVillageRoot", "Asphalt", rot=(0, 90, 0), mirror="X", seg=W),
    P("BusVillageLampR", "cube", (0.12, 0.03, 0.09), (0.25, -0.89, 0.34), "BusVillageRoot", "OffWhite", mirror="X",
      note="[조정] y -0.88→-0.89 (묻힘 → 5 mm 나오게)"),

    P("KTXRoot", "empty", (0.10, 0.10, 0.10), (0, 0, 0), None),
    P("KTXBody", "cube", (0.70, 2.16, 0.52), (0, 0.32, 0.40), "KTXRoot", "OffWhite", bevel=(0.06, 2)),
    P("KTXNose", "sphere", (0.74, 0.95, 0.68), (0, -0.925, 0.41), "KTXRoot", "OffWhite", seg=10,
      note="[설정] 앞쪽 절반 윗면을 끝으로 갈수록 낮춰 쐐기형, 10분할 (spec 14: 코 메시 분할은 Claude 결정)"),
    P("KTXRoof", "cube", (0.75, 1.65, 0.10), (0, 0.42, 0.70), "KTXRoot", "OffWhite", bevel=(0.04, 1)),
    P("KTXCockpit", "sphere", (0.56, 0.40, 0.28), (0, -1.16, 0.53), "KTXRoot", "DarkGlass", seg=8,
      note="[조정] 16분할→8분할 (설계도 16분할이면 KTX 736 삼각형, 예산 500 초과. 대부분 코 안에 있어 보이는 부분 작음)"),
    P("KTXAccentR", "cube", (0.03, 2.10, 0.13), (0.36, 0.12, 0.22), "KTXRoot", "SeaDeep", mirror="X"),
    P("KTXSideGlassR", "cube", (0.03, 1.10, 0.22), (0.35, 0.40, 0.50), "KTXRoot", "DarkGlass", mirror="X"),
    P("KTXBogieF", "cube", (0.48, 0.34, 0.12), (0, -0.36, 0.06), "KTXRoot", "Asphalt"),
    P("KTXBogieR", "cube", (0.48, 0.34, 0.12), (0, 0.78, 0.06), "KTXRoot", "Asphalt"),

    P("BeachTrainRoot", "empty", (0.10, 0.10, 0.10), (0, 0, 0), None),
    P("BeachTrainBody", "cube", (0.86, 2.10, 0.58), (0, 0, 0.50), "BeachTrainRoot", "SeaShallow", bevel=(0.06, 2)),
    P("BeachTrainRoof", "cube", (0.90, 1.90, 0.12), (0, 0.02, 0.79), "BeachTrainRoot", "OffWhite", bevel=(0.05, 1)),
    P("BeachTrainFrontGlass", "cube", (0.72, 0.04, 0.34), (0, -1.035, 0.62), "BeachTrainRoot", "DarkGlass", bevel=(0.02, 1),
      note="[조정] y -1.02→-1.035 (차체 앞면 -1.05 안에 묻힘 → 5 mm 나오게)"),
    P("BeachTrainSideGlassR", "cube", (0.03, 1.64, 0.34), (0.435, -0.02, 0.62), "BeachTrainRoot", "DarkGlass", mirror="X"),
    P("BeachTrainTrimR", "cube", (0.03, 1.94, 0.08), (0.438, 0, 0.34), "BeachTrainRoot", "OffWhite", mirror="X"),
    P("BeachTrainWheelFR", "cylinder", (0.27, 0.27, 0.10), (0.40, -0.62, 0.135), "BeachTrainRoot", "Asphalt", rot=(0, 90, 0), mirror="X", seg=W),
    P("BeachTrainWheelRR", "cylinder", (0.27, 0.27, 0.10), (0.40, 0.62, 0.135), "BeachTrainRoot", "Asphalt", rot=(0, 90, 0), mirror="X", seg=W),
    P("BeachTrainLampR", "cylinder", (0.13, 0.13, 0.03), (0.23, -1.04, 0.36), "BeachTrainRoot", "OffWhite", rot=(90, 0, 0), mirror="X", seg=6,
      note="[조정] y -1.03→-1.04 (묻힘 → 5 mm 나오게)"),

    P("SkyCapsuleRoot", "empty", (0.10, 0.10, 0.10), (0, 0, 0), None),
    P("SkyCapsuleSled", "cube", (0.70, 1.10, 0.08), (0, 0, 0.04), "SkyCapsuleRoot", "Asphalt", bevel=(0.02, 1)),
    P("SkyCapsuleBody", "cube", (0.90, 1.04, 0.82), (0, 0, 0.59), "SkyCapsuleRoot", "SunsetCoral", bevel=(0.10, 2)),
    P("SkyCapsuleRoof", "cube", (0.78, 0.90, 0.18), (0, 0.04, 1.01), "SkyCapsuleRoot", "SunsetCoral", bevel=(0.08, 2)),
    P("SkyCapsuleFrontGlass", "cube", (0.70, 0.04, 0.54), (0, -0.53, 0.66), "SkyCapsuleRoot", "SkyGlass", bevel=(0.04, 2)),
    P("SkyCapsuleSideGlassR", "cube", (0.03, 0.62, 0.54), (0.445, -0.03, 0.66), "SkyCapsuleRoot", "SkyGlass", mirror="X",
      note="[설정] 설계도 그대로 → 전체 폭 0.92 m (목표 0.90 보다 2 cm 큼, validation 에 기록)"),
    P("SkyCapsuleFrame", "cube", (0.06, 1.06, 0.10), (0, 0, 0.18), "SkyCapsuleRoot", "DarkGlass", bevel=(0.02, 1)),
]

# ═════════════════════════════════════════════
# 아래는 공용 함수 — 수정하지 않는다
# ═════════════════════════════════════════════
NAME_RE = re.compile(r"^(MAP|VEH|ENV|SF|CHR|PRP|FOOD|FX)\d{2}_[A-Za-z0-9]+_[A-Za-z0-9]+_L[0-2]$")
SHAPES = {"cube", "cylinder", "cone", "sphere", "plane", "empty"}

logger = logging.getLogger("busan3d.blockout")


def log(stage, level=logging.INFO, **kv):
    """[STAGE] [TIMESTAMP] key=value ... 형식으로 남긴다."""
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    body = " ".join(f"{k}={v}" for k, v in kv.items())
    logger.log(level, "[%s] [%s] %s", stage, ts, body)


def setup_logging():
    logger.setLevel(LOG_LEVEL)
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        logger.addHandler(h)
    logger.propagate = False


def hex_to_linear_rgba(hex_str, alpha=1.0):
    """'#RRGGBB' (sRGB) → Blender 내부용 선형 RGBA."""
    s = hex_str.strip().lstrip("#")
    if not re.fullmatch(r"[0-9A-Fa-f]{6}", s):
        raise ValueError(f"잘못된 hex 색: {hex_str!r}")
    out = []
    for i in (0, 2, 4):
        c = int(s[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (out[0], out[1], out[2], float(alpha))


def full_name(part_name):
    return f"{ASSET_ID}_{ASSET_NAME}_{part_name}_{LOD}"


def pivot_offset(part):
    """도형 중심에서 '원점'까지의 오프셋을 받아, 메시를 얼마나 옮길지 돌려준다."""
    sx, sy, sz = part["size"]
    pv = part.get("pivot", "center")
    if pv == "center":
        return (0.0, 0.0, 0.0)
    if pv == "bottom":
        return (0.0, 0.0, sz / 2.0)          # 원점이 바닥 → 메시를 위로 반 높이
    ox, oy, oz = pv
    return (-ox, -oy, -oz)                    # 원점 = 중심 + pv → 메시는 반대로 이동


def validate_inputs():
    """입력 검사. 문제 목록을 돌려준다(빈 목록이면 통과)."""
    problems = []
    if not re.fullmatch(r"(MAP|VEH|ENV|SF|CHR|PRP|FOOD|FX)\d{2}", ASSET_ID):
        problems.append(f"ASSET_ID 형식 오류: {ASSET_ID}")
    if not re.fullmatch(r"[A-Za-z0-9]+", ASSET_NAME):
        problems.append(f"ASSET_NAME 은 영문·숫자만: {ASSET_NAME}")
    seen = set()
    for i, p in enumerate(PARTS):
        n = p.get("name", f"<{i}>")
        if not re.fullmatch(r"[A-Za-z0-9]+", n):
            problems.append(f"부품 이름은 영문·숫자만: {n}")
        if n in seen:
            problems.append(f"부품 이름 중복: {n}")
        if p.get("shape") not in SHAPES:
            problems.append(f"{n}: shape 오류 {p.get('shape')}")
        size = p.get("size", (0, 0, 0))
        if p.get("shape") != "empty":
            if len(size) != 3 or any(v <= 0 for v in size[:2]) or (p.get("shape") != "plane" and size[2] <= 0):
                problems.append(f"{n}: size 는 양수 3개여야 함 {size}")
        par = p.get("parent")
        if par and par not in seen:
            problems.append(f"{n}: 부모 {par} 가 먼저 정의되지 않음")
        mat = p.get("material")
        if mat and mat not in MATERIALS:
            problems.append(f"{n}: 재질 {mat} 가 MATERIALS 에 없음")
        if not NAME_RE.match(full_name(n)):
            problems.append(f"{n}: 최종 이름 규칙 위반 {full_name(n)}")
        seen.add(n)
    for k, m in MATERIALS.items():
        try:
            hex_to_linear_rgba(m["base_hex"])
            if m.get("emission_hex"):
                hex_to_linear_rgba(m["emission_hex"])
        except (KeyError, ValueError) as e:
            problems.append(f"재질 {k}: {e}")
    return problems


# ─────────────── 블렌더 전용 함수 ───────────────
def get_clean_collection():
    """같은 이름 컬렉션이 있으면 안의 오브젝트를 지우고 다시 쓴다(여러 번 실행해도 결과 동일)."""
    cname = f"{ASSET_ID}_{ASSET_NAME}"
    col = bpy.data.collections.get(cname)
    removed = 0
    if col is None:
        col = bpy.data.collections.new(cname)
        bpy.context.scene.collection.children.link(col)
    else:
        for obj in list(col.objects):
            data = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            if data is not None and getattr(data, "users", 1) == 0 and isinstance(data, bpy.types.Mesh):
                bpy.data.meshes.remove(data)
            removed += 1
    log("SETUP", collection=cname, removed_objects=removed)
    return col


def build_material(key, spec):
    mname = f"M_{ASSET_NAME}_{key}"
    mat = bpy.data.materials.get(mname) or bpy.data.materials.new(mname)
    mat.use_nodes = True
    bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf is None:
        bsdf = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
    alpha = float(spec.get("alpha", 1.0))
    bsdf.inputs["Base Color"].default_value = hex_to_linear_rgba(spec["base_hex"])
    bsdf.inputs["Roughness"].default_value = float(spec.get("roughness", 0.5))
    bsdf.inputs["Metallic"].default_value = float(spec.get("metallic", 0.0))
    if "IOR" in bsdf.inputs and spec.get("ior"):
        bsdf.inputs["IOR"].default_value = float(spec["ior"])
    bsdf.inputs["Alpha"].default_value = alpha
    if spec.get("emission_hex"):
        em_key = "Emission Color" if "Emission Color" in bsdf.inputs else "Emission"
        bsdf.inputs[em_key].default_value = hex_to_linear_rgba(spec["emission_hex"])
        bsdf.inputs["Emission Strength"].default_value = float(spec.get("emission_strength", 1.0))
    if alpha < 1.0:
        if hasattr(mat, "surface_render_method"):
            mat.surface_render_method = "BLENDED"
        elif hasattr(mat, "blend_method"):
            mat.blend_method = "BLEND"
    mat.diffuse_color = hex_to_linear_rgba(spec["base_hex"], alpha)  # 뷰포트 표시색
    log("MATERIAL", logging.DEBUG, name=mname, base=spec["base_hex"],
        rough=spec.get("roughness", 0.5), metal=spec.get("metallic", 0.0),
        emission=spec.get("emission_hex", "none"))
    return mat


def build_mesh(part):
    """bmesh 로 단위 도형을 만들고, size 로 늘린 뒤, 원점(pivot)에 맞게 옮긴다."""
    shape = part["shape"]
    seg = int(part.get("segments", 32))
    sx, sy, sz = part["size"]
    bm = bmesh.new()
    if shape == "cube":
        bmesh.ops.create_cube(bm, size=1.0)
        scale = (sx, sy, sz)
    elif shape in ("cylinder", "cone"):
        top = 0.5 if shape == "cylinder" else 0.5 * float(part.get("radius_top_ratio", 0.0))
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg,
                              radius1=0.5, radius2=top, depth=1.0)
        scale = (sx, sy, sz)
    elif shape == "sphere":
        bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(8, seg // 2), radius=0.5)
        scale = (sx, sy, sz)
    elif shape == "plane":
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
        scale = (sx, sy, 1.0)
    else:
        raise ValueError(shape)
    bmesh.ops.scale(bm, vec=Vector(scale), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(pivot_offset(part)), verts=bm.verts)
    me = bpy.data.meshes.new(full_name(part["name"]))
    bm.to_mesh(me)
    bm.free()
    if part.get("smooth"):
        me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
    return me


def add_modifiers(obj, part):
    if part.get("bevel"):
        b = obj.modifiers.new("Bevel", "BEVEL")
        b.width = float(part["bevel"]["width"])
        b.segments = int(part["bevel"].get("segments", 2))
        b.limit_method = "ANGLE"
    if part.get("array"):
        a = obj.modifiers.new("Array", "ARRAY")
        a.count = int(part["array"]["count"])
        a.use_relative_offset = False
        a.use_constant_offset = True
        a.constant_offset_displace = part["array"]["offset"]
    if part.get("mirror"):
        m = obj.modifiers.new("Mirror", "MIRROR")
        axes = part["mirror"].upper()
        m.use_axis = ("X" in axes, "Y" in axes, "Z" in axes)
        if obj.parent is not None:
            m.mirror_object = obj.parent      # 부모 원점 기준 대칭


def local_dims(me):
    xs = [v.co.x for v in me.vertices]
    ys = [v.co.y for v in me.vertices]
    zs = [v.co.z for v in me.vertices]
    return (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))


def build_parts(col):
    objs = {}
    for part in PARTS:
        name = full_name(part["name"])
        if part["shape"] == "empty":
            obj = bpy.data.objects.new(name, None)
            obj.empty_display_size = max(part.get("size", (0.2, 0.2, 0.2)))
        else:
            me = build_mesh(part)
            obj = bpy.data.objects.new(name, me)
            if part.get("material"):
                me.materials.append(build_material(part["material"], MATERIALS[part["material"]]))
        col.objects.link(obj)
        if part.get("parent"):
            obj.parent = objs[part["parent"]]   # location 은 부모 기준
        obj.location = part.get("location", (0, 0, 0))
        rx, ry, rz = part.get("rotation_deg", (0, 0, 0))
        obj.rotation_euler = Euler((math.radians(rx), math.radians(ry), math.radians(rz)), "XYZ")
        if part["shape"] != "empty":
            add_modifiers(obj, part)
            got = local_dims(obj.data)
            want = part["size"] if part["shape"] != "plane" else (part["size"][0], part["size"][1], 0.0)
            err = max(abs(g - w) for g, w in zip(got, want))
            lvl = logging.WARNING if err > TOLERANCE_M else logging.INFO
            log("PART", lvl, name=name, shape=part["shape"],
                dims=f"{got[0]:.3f}x{got[1]:.3f}x{got[2]:.3f}", spec=f"{want[0]:.3f}x{want[1]:.3f}x{want[2]:.3f}",
                err_m=f"{err:.4f}", note=part.get("note", "-"))
        objs[part["name"]] = obj
    log("BUILD", parts=len(objs))
    return objs


def report(objs):
    """모디파이어까지 반영한 최종 크기·삼각형 수를 설계도 값과 비교한다."""
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    mins = [math.inf] * 3
    maxs = [-math.inf] * 3
    tris = 0
    for obj in objs.values():
        if obj.type != "MESH":
            continue
        ev = obj.evaluated_get(dg)
        for corner in ev.bound_box:
            w = ev.matrix_world @ Vector(corner)
            for i in range(3):
                mins[i] = min(mins[i], w[i])
                maxs[i] = max(maxs[i], w[i])
        me = ev.to_mesh()
        tris += sum(len(p.vertices) - 2 for p in me.polygons)
        ev.to_mesh_clear()
    dims = tuple(maxs[i] - mins[i] for i in range(3))
    err = max(abs(d - e) for d, e in zip(dims, EXPECTED_DIMS_M))
    log("REPORT", logging.WARNING if err > TOLERANCE_M else logging.INFO,
        asset=f"{ASSET_ID}_{ASSET_NAME}", spec_version=SPEC_VERSION,
        dims_m=f"{dims[0]:.3f}x{dims[1]:.3f}x{dims[2]:.3f}",
        expected_m=f"{EXPECTED_DIMS_M[0]:.3f}x{EXPECTED_DIMS_M[1]:.3f}x{EXPECTED_DIMS_M[2]:.3f}",
        max_err_m=f"{err:.4f}", min_z=f"{mins[2]:.3f}")
    log("REPORT", logging.WARNING if tris > TRI_BUDGET else logging.INFO,
        triangles=tris, budget=TRI_BUDGET, height_vs_person=f"{dims[2] / 1.70:.2f}x")
    if abs(mins[2]) > TOLERANCE_M:
        log("REPORT", logging.WARNING, issue="에셋 바닥이 Z=0 에 있지 않음", min_z=f"{mins[2]:.3f}")
    return dims, tris


def main():
    setup_logging()
    log("START", asset=f"{ASSET_ID}_{ASSET_NAME}", spec_version=SPEC_VERSION,
        parts=len(PARTS), materials=len(MATERIALS))
    problems = validate_inputs()
    for p in problems:
        log("VALIDATE", logging.ERROR, problem=p)
    if problems:
        log("VALIDATE", logging.ERROR, result="중단", count=len(problems),
            next_step="위 문제를 고친 뒤 다시 실행")
        return None
    log("VALIDATE", result="통과")
    if not IN_BLENDER:
        log("END", note="블렌더 밖이라 입력 검사만 함")
        return None
    col = get_clean_collection()
    objs = build_parts(col)
    result = report(objs)
    log("END", result="완료")
    return result


def self_test():
    """블렌더 없이 순수 함수만 검사한다."""
    setup_logging()
    r, g, b, a = hex_to_linear_rgba("#FFFFFF")
    assert abs(r - 1) < 1e-9 and abs(g - 1) < 1e-9 and abs(b - 1) < 1e-9 and a == 1.0
    r, _, _, _ = hex_to_linear_rgba("#808080")
    assert abs(r - 0.21586) < 1e-4, r          # sRGB 128 → linear 약 0.2159
    try:
        hex_to_linear_rgba("#12345")
        raise AssertionError("잘못된 hex 를 통과시킴")
    except ValueError:
        pass
    assert pivot_offset({"size": (1, 2, 3), "pivot": "bottom"}) == (0, 0, 1.5)
    assert pivot_offset({"size": (1, 2, 3), "pivot": (-0.5, 0, -1.5)}) == (0.5, 0, 1.5)
    assert NAME_RE.match("VEH02_CityBus_DoorFront_L0")
    assert NAME_RE.match("MAP04_TransitTokens_BusBody_L0")
    assert not NAME_RE.match("veh02_CityBus_Door_L0")
    problems = validate_inputs()
    assert not problems, problems
    log("SELFTEST", result="통과", checks=9)



# ═════════════════════════════════════════════
# MAP04 전용 추가 (공용 함수는 그대로 두고 여기서만 덧붙인다)
# ═════════════════════════════════════════════
def shape_ktx_nose(objs):
    """KTX 코: 앞쪽(-Y) 절반의 윗면을 끝으로 갈수록 낮춰 둥근 쐐기로 만든다(최대 45 % 낮춤)."""
    me = objs["KTXNose"].data
    ry = 0.95 / 2
    for v in me.vertices:
        if v.co.y < 0 and v.co.z > 0:
            t = min(1.0, -v.co.y / ry)
            v.co.z *= 1.0 - 0.45 * t
    me.update()


def align_wheels(objs):
    """다각형 바퀴의 꼭짓점 하나가 맨 아래(지면 0)에 오도록 원기둥 축 둘레로 돌린다.
    원기둥 로컬 +X 가 회전(0,90,0) 후 아래(-Z)를 향하므로, +X 에 가장 가까운 꼭짓점을 +X 로 맞춘다."""
    for name, o in objs.items():
        if "Wheel" in name and o.type == "MESH":
            ang = min((math.atan2(v.co.y, v.co.x) for v in o.data.vertices), key=abs)
            ca, sa = math.cos(-ang), math.sin(-ang)
            for v in o.data.vertices:
                x, y = v.co.x, v.co.y
                v.co.x, v.co.y = x * ca - y * sa, x * sa + y * ca
            o.data.update()


def finish_shading(objs):
    """둥근 모서리가 매끈하게 보이도록 부드러운 음영 + 가중 노멀."""
    for o in objs.values():
        if o.type != "MESH":
            continue
        o.data.polygons.foreach_set("use_smooth", [True] * len(o.data.polygons))
        if any(m.type == "BEVEL" for m in o.modifiers) or o.name.endswith(("Nose_L0", "Cockpit_L0")):
            wn = o.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
            wn.weight = 50
            wn.keep_sharp = True
        else:
            for p in o.data.polygons:      # 상자·바퀴는 각진 면 유지
                p.use_smooth = False


def check_roots(objs):
    """토큰마다 Root 기준 크기·삼각형 수를 설계도와 비교."""
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    report = {}
    for root_name, want in ROOTS.items():
        root = objs[root_name]
        inv = root.matrix_world.inverted()
        mins, maxs, tris = [math.inf] * 3, [-math.inf] * 3, 0
        for o in objs.values():
            if o.type != "MESH" or o.parent != root:
                continue
            ev = o.evaluated_get(dg)
            me = ev.to_mesh()
            for v in me.vertices:
                p = inv @ (ev.matrix_world @ v.co)
                for i in range(3):
                    mins[i] = min(mins[i], p[i]); maxs[i] = max(maxs[i], p[i])
            tris += sum(len(p.vertices) - 2 for p in me.polygons)
            ev.to_mesh_clear()
        dims = tuple(round(maxs[i] - mins[i], 4) for i in range(3))
        err = max(abs(d - w) for d, w in zip(dims, want["dims"]))
        ok_dim, ok_tri, ok_floor = err <= TOLERANCE_M + 1e-6, tris <= want["tri"], abs(mins[2]) <= 1e-4
        log("ROOT", logging.INFO if (ok_dim and ok_tri and ok_floor) else logging.WARNING, root=root_name,
            dims=f"{dims[0]:.3f}x{dims[1]:.3f}x{dims[2]:.3f}", spec=f"{want['dims'][0]:.2f}x{want['dims'][1]:.2f}x{want['dims'][2]:.2f}",
            max_err_m=f"{err:.4f}", triangles=tris, budget=want["tri"], floor_z=f"{mins[2]:.4f}",
            front_y=f"{mins[1]:.3f}", rear_y=f"{maxs[1]:.3f}")
        report[root_name] = {"dims_m": dims, "spec_dims_m": want["dims"], "max_err_m": round(err, 4), "triangles": tris,
                             "tri_budget": want["tri"], "floor_z": round(mins[2], 4), "dims_ok": ok_dim, "tri_ok": ok_tri}
    return report


def build_tokens():
    setup_logging()
    log("START", asset=f"{ASSET_ID}_{ASSET_NAME}", spec_version=SPEC_VERSION, parts=len(PARTS), roots=len(ROOTS))
    problems = validate_inputs()
    for p in problems:
        log("VALIDATE", logging.ERROR, problem=p)
    if problems:
        return None
    col = get_clean_collection()
    objs_full = build_parts(col)
    shape_ktx_nose(objs_full)
    align_wheels(objs_full)
    finish_shading(objs_full)
    for name, r in ROOTS.items():                      # 보기용 배치 (형상 원점은 각 Root)
        objs_full[name].location.x = r["x"]
    rep = check_roots(objs_full)
    log("END", result="완료", total_triangles=sum(r["triangles"] for r in rep.values()), budget=TRI_BUDGET)
    return objs_full, rep


if __name__ == "__main__":
    build_tokens()

# CHANGELOG
# v1.0.0 — 2026-11-11 — 최초 작성 (spec.md v1.0). 묻힌 앞 유리·램프 위치 조정(5 mm), KTX 코 쐐기형, 바퀴 바닥 맞춤,
#                       삼각형 예산에 맞춘 분할 수(바퀴 8, 코 10·조종석 8, 일부 베벨 1~2), 가중 노멀
