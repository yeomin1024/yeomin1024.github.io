# VERSION: v1.0.0 — 2026-11-10 — 3D 지도(지형·바다·핀·루트) 생성 스크립트 템플릿 최초 작성
"""
부산 3D 영상 프로젝트 — 3D 지도 생성 스크립트 (MAP01 지형·바다 / MAP02 루트 / MAP03 핀)

[사용법]
  1. 이 파일을 busan-3d/assets/MAP01_BusanMap/map_build.py 로 복사한다.
  2. "1. 설정" 블록만 고친다. 장소 좌표는 FACTS.md 4장(OpenStreetMap 확인 좌표)을 쓴다.
  3. 지형 높이 자료(DEM 높이 이미지 PNG)가 있으면 HEIGHTMAP["path"] 에 넣는다.
     없으면 평평한 땅 없이 바다판 + 핀 + 루트만 만들고 WARNING 을 남긴다.
  4. Blender 4.2 이상에서 Run Script (명령줄: blender --background --python map_build.py).
  5. 블렌더 밖에서 `python map_build.py --self-test` 로 좌표 변환·입력 검사만 할 수 있다.

[좌표 규칙]
  - 1 Blender unit(=1 m) = 실제 KM_PER_UNIT km.
  - +Y = 북쪽, +X = 동쪽, Z = 높이. 지도 중심(REF_LAT, REF_LON)이 원점이다.
  - 위경도 → 평면 변환: 등장방형 근사(지도 범위 수십 km 에서 오차 0.5% 미만, self-test 로 확인).

[높이 이미지 규칙]
  - 흑백 PNG. 픽셀 값 0 = 해발 0 m, 1 = MAX_ELEVATION_M.
  - 이미지 네 변 = HEIGHTMAP["bounds"] (남, 서, 북, 동 위경도), 위쪽이 북쪽.
  - 출처(예: SRTM, Copernicus DEM)의 표기 문구를 CREDITS.md 에 반드시 적는다.

[루트 규칙]
  - ROUTES 의 stops 는 PLACES 의 key 순서. 정류장 사이는 직선이다(실제 도로 경로 아님 → 영상 자막에 '경로 개략').
  - 더 정확히 그리려면 via 에 중간 지점 (lat, lon) 을 넣는다.
  - 루트는 bevel_factor_end 를 0→1 로 키프레임해서 '그려지는' 애니메이션을 만든다.
"""

import logging
import math
import re
import sys
import time

try:
    import bpy
    import bmesh
    from mathutils import Vector
    IN_BLENDER = True
except ImportError:
    bpy = bmesh = Vector = None
    IN_BLENDER = False

# ─────────────────────────────────────────────
# 1. 설정
# ─────────────────────────────────────────────
MAP_ID = "MAP01"
MAP_NAME = "BusanMap"
SPEC_VERSION = "v1.0"
REF_LAT, REF_LON = 35.150, 129.115      # [설정] 지도 중심
KM_PER_UNIT = 10.0                       # [설정] 1 unit = 10 km
HEIGHT_EXAGGERATION = 3.0                # [설정] 높이 3배 과장
LOG_LEVEL = logging.INFO

HEIGHTMAP = {
    "path": "",                          # 예) "//dem_busan.png" (// = .blend 파일 기준 상대경로)
    "bounds": (35.05, 128.98, 35.25, 129.26),   # (남, 서, 북, 동) [설정] 일정 전체 + 여백
    "max_elevation_m": 800.0,            # 이미지 값 1.0 에 해당하는 해발 고도
    "subdiv": 256,                       # 격자 분할 수 (클수록 정밀·무거움)
}
SEA_LEVEL_OFFSET_M = 2.0                 # 바다판을 해발 몇 m 높이에 둘지 (해안선 표현)

PIN = {"stem_height": 0.06, "stem_diameter": 0.006, "head_diameter": 0.02, "segments": 16}
ROUTE = {"bevel_depth": 0.003, "lift": 0.004, "frames_per_day": 72, "start_frame": 1}
FONT_PATH = ""                           # 한글 글꼴 경로(예: NotoSansKR). 비우면 이름표를 만들지 않음
LABEL_SIZE = 0.03

COLORS = {
    "sea": "#0E4C77", "land": "#B9B6AE", "pin": "#F2EFE6",
    "day1": "#F28C5B", "day2": "#3FA7B5", "day3": "#C3B1E1",
}

# 장소: key / 표시 이름 / 위도 / 경도 / 출처 — FACTS.md 4장과 같다 (OpenStreetMap, 2026-11-10 조회)
# 부평깡통시장·차이나타운은 OSM 검색 결과가 없어 빠져 있다 → 좌표 확인 후 추가
PLACES = [
    {"key": "busan_station", "name": "부산역", "lat": 35.11555, "lon": 129.04259, "src": "OSM node/8693385785"},
    {"key": "gamcheon", "name": "감천문화마을", "lat": 35.09634, "lon": 129.00879, "src": "OSM way/382693934"},
    {"key": "biff", "name": "BIFF광장", "lat": 35.09876, "lon": 129.02898, "src": "OSM node/4524166889"},
    {"key": "gukje", "name": "국제시장", "lat": 35.10116, "lon": 129.02819, "src": "OSM way/500548799"},
    {"key": "yeongdo_bridge", "name": "영도대교", "lat": 35.09557, "lon": 129.03646, "src": "OSM way/496277558"},
    {"key": "huinnyeoul", "name": "흰여울문화마을", "lat": 35.07740, "lon": 129.04565, "src": "OSM node/5450264422"},
    {"key": "jagalchi", "name": "자갈치시장", "lat": 35.09709, "lon": 129.02887, "src": "OSM node/4807672423"},
    {"key": "haeundae_beach", "name": "해운대해수욕장", "lat": 35.15918, "lon": 129.15903, "src": "OSM node/4943685023 (정류장)"},
    {"key": "haeundae_station", "name": "해운대역", "lat": 35.16375, "lon": 129.15875, "src": "OSM node/5208472150"},
    {"key": "yonggungsa", "name": "해동용궁사", "lat": 35.18843, "lon": 129.22298, "src": "OSM way/382701819"},
    {"key": "yeonhwari", "name": "연화리 해녀촌", "lat": 35.21790, "lon": 129.22828, "src": "OSM way/1371848245"},
    {"key": "songjeong_beach", "name": "송정해수욕장", "lat": 35.17765, "lon": 129.19858, "src": "OSM relation/21218076"},
    {"key": "songjeong_station", "name": "송정정거장", "lat": 35.18124, "lon": 129.20049, "src": "OSM way/154253036"},
    {"key": "daritdol", "name": "다릿돌전망대", "lat": 35.16422, "lon": 129.19600, "src": "OSM node/12817542739"},
    {"key": "cheongsapo", "name": "청사포", "lat": 35.16126, "lon": 129.19138, "src": "OSM node/7983215374"},
    {"key": "mipo", "name": "미포", "lat": 35.15808, "lon": 129.17293, "src": "OSM node/12817477565"},
    {"key": "nurimaru", "name": "동백섬 누리마루", "lat": 35.15235, "lon": 129.15137, "src": "OSM way/239280379"},
    {"key": "millak", "name": "민락 회센터", "lat": 35.15424, "lon": 129.12786, "src": "OSM way/784099272"},
    {"key": "gwangalli", "name": "광안리해수욕장", "lat": 35.15089, "lon": 129.11678, "src": "OSM way/107642460"},
    {"key": "gwangan_bridge", "name": "광안대교", "lat": 35.14569, "lon": 129.12839, "src": "OSM way/382760140"},
    {"key": "kyungsung", "name": "경성대·부경대역", "lat": 35.13821, "lon": 129.10202, "src": "OSM node/5004041091 (정류장)"},
    {"key": "oryukdo_skywalk", "name": "오륙도 스카이워크", "lat": 35.10154, "lon": 129.12169, "src": "OSM node/4533702794 (정류장)"},
    {"key": "oryukdo", "name": "오륙도", "lat": 35.09200, "lon": 129.12700, "src": "OSM relation/6995498"},
    {"key": "igidae_bridge", "name": "이기대 구름다리", "lat": 35.13040, "lon": 129.12092, "src": "OSM way/1350821443"},
    {"key": "dongsaengmal", "name": "동생말", "lat": 35.13199, "lon": 129.12119, "src": "OSM node/4537682606"},
]

# 루트: FACTS.md 1장 일정 순서. 광안대교·오륙도는 루트 없이 핀만 둔다.
ROUTES = [
    {"day": 1, "color": "day1", "via": {},
     "stops": ["busan_station", "gamcheon", "biff", "gukje", "yeongdo_bridge", "huinnyeoul", "jagalchi", "haeundae_beach"]},
    {"day": 2, "color": "day2", "via": {},
     "stops": ["haeundae_beach", "haeundae_station", "yonggungsa", "yeonhwari", "songjeong_beach", "songjeong_station",
               "daritdol", "cheongsapo", "mipo", "haeundae_beach", "nurimaru", "millak", "gwangalli", "haeundae_beach"]},
    {"day": 3, "color": "day3", "via": {},
     "stops": ["haeundae_beach", "mipo", "kyungsung", "oryukdo_skywalk", "igidae_bridge", "dongsaengmal", "busan_station"]},
]

# ═════════════════════════════════════════════
# 아래는 공용 함수 — 수정하지 않는다
# ═════════════════════════════════════════════
KM_PER_DEG_LAT = 110.574
KM_PER_DEG_LON_EQ = 111.320
EARTH_R_KM = 6371.0088

logger = logging.getLogger("busan3d.map")


def log(stage, level=logging.INFO, **kv):
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    logger.log(level, "[%s] [%s] %s", stage, ts, " ".join(f"{k}={v}" for k, v in kv.items()))


def setup_logging():
    logger.setLevel(LOG_LEVEL)
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        logger.addHandler(h)
    logger.propagate = False


def hex_to_linear_rgba(hex_str, alpha=1.0):
    s = hex_str.strip().lstrip("#")
    if not re.fullmatch(r"[0-9A-Fa-f]{6}", s):
        raise ValueError(f"잘못된 hex 색: {hex_str!r}")
    out = []
    for i in (0, 2, 4):
        c = int(s[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (out[0], out[1], out[2], float(alpha))


def latlon_to_xy(lat, lon):
    """위경도 → 지도 평면 좌표(unit). 등장방형 근사."""
    x_km = (lon - REF_LON) * KM_PER_DEG_LON_EQ * math.cos(math.radians(REF_LAT))
    y_km = (lat - REF_LAT) * KM_PER_DEG_LAT
    return (x_km / KM_PER_UNIT, y_km / KM_PER_UNIT)


def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_R_KM * math.asin(math.sqrt(a))


def meters_to_units(m):
    return m / 1000.0 / KM_PER_UNIT


def validate_inputs():
    problems = []
    keys = [p["key"] for p in PLACES]
    if len(keys) != len(set(keys)):
        problems.append("PLACES key 중복")
    s, w, n, e = HEIGHTMAP["bounds"]
    if not (s < n and w < e):
        problems.append(f"HEIGHTMAP bounds 순서 오류 (남,서,북,동): {HEIGHTMAP['bounds']}")
    for p in PLACES:
        if not (33.0 <= p["lat"] <= 39.0 and 124.0 <= p["lon"] <= 132.0):
            problems.append(f"{p['key']}: 한국 범위를 벗어난 좌표 {p['lat']},{p['lon']}")
        if not (s <= p["lat"] <= n and w <= p["lon"] <= e):
            problems.append(f"{p['key']}: 지도 범위(bounds) 밖 좌표")
        if not p.get("src"):
            problems.append(f"{p['key']}: 좌표 출처(src) 없음")
    for r in ROUTES:
        for k in r["stops"]:
            if k not in keys:
                problems.append(f"{r['day']}일차 루트: 없는 장소 {k}")
        if r["color"] not in COLORS:
            problems.append(f"{r['day']}일차 루트: 없는 색 {r['color']}")
        for k in r.get("via", {}):
            if k not in r["stops"]:
                problems.append(f"{r['day']}일차 via: 루트에 없는 장소 {k}")
    for k, v in COLORS.items():
        try:
            hex_to_linear_rgba(v)
        except ValueError as e:
            problems.append(f"색 {k}: {e}")
    return problems


# ─────────────── 블렌더 전용 ───────────────
def get_clean_collection():
    cname = f"{MAP_ID}_{MAP_NAME}"
    col = bpy.data.collections.get(cname)
    removed = 0
    if col is None:
        col = bpy.data.collections.new(cname)
        bpy.context.scene.collection.children.link(col)
    else:
        for obj in list(col.objects):
            data = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            if data is not None and data.users == 0:
                if isinstance(data, bpy.types.Mesh):
                    bpy.data.meshes.remove(data)
                elif isinstance(data, bpy.types.Curve):      # 루트 곡선·이름표(TextCurve)
                    bpy.data.curves.remove(data)
            removed += 1
    log("SETUP", collection=cname, removed_objects=removed, km_per_unit=KM_PER_UNIT,
        ref=f"{REF_LAT},{REF_LON}", exaggeration=HEIGHT_EXAGGERATION)
    return col


def material(key, emission=0.0):
    name = f"M_{MAP_NAME}_{key}"
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf is None:
        bsdf = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
    rgba = hex_to_linear_rgba(COLORS[key])
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = 0.6
    if emission > 0:
        em_key = "Emission Color" if "Emission Color" in bsdf.inputs else "Emission"
        bsdf.inputs[em_key].default_value = rgba
        bsdf.inputs["Emission Strength"].default_value = emission
    mat.diffuse_color = rgba
    return mat


class HeightSampler:
    """높이 이미지에서 위경도의 높이(unit)를 읽는다. 이미지가 없으면 항상 0."""

    def __init__(self):
        self.ok = False
        self.image = None
        path = HEIGHTMAP["path"]
        if not path:
            log("TERRAIN", logging.WARNING, issue="높이 이미지 없음 → 평평한 지도",
                next_step="DEM 높이 PNG 를 준비해 HEIGHTMAP['path'] 에 넣기")
            return
        try:
            self.image = bpy.data.images.load(bpy.path.abspath(path), check_existing=True)
        except RuntimeError as e:
            log("TERRAIN", logging.ERROR, issue="높이 이미지 열기 실패", path=path, error=e,
                next_step="경로·파일 형식(PNG) 확인")
            return
        import numpy as np
        w, h = self.image.size
        px = np.empty(w * h * self.image.channels, dtype=np.float32)
        self.image.pixels.foreach_get(px)
        self.gray = px.reshape(h, w, self.image.channels)[:, :, 0]   # 행 0 = 이미지 아래쪽(남)
        self.w, self.h = w, h
        self.strength = meters_to_units(HEIGHTMAP["max_elevation_m"]) * HEIGHT_EXAGGERATION
        self.ok = True
        log("TERRAIN", path=path, size=f"{w}x{h}", max_elev_m=HEIGHTMAP["max_elevation_m"],
            value_range=f"{float(self.gray.min()):.3f}~{float(self.gray.max()):.3f}",
            strength_units=f"{self.strength:.4f}")

    def height(self, lat, lon):
        if not self.ok:
            return 0.0
        s, w, n, e = HEIGHTMAP["bounds"]
        u = (lon - w) / (e - w)
        v = (lat - s) / (n - s)
        i = min(self.w - 1, max(0, int(round(u * (self.w - 1)))))
        j = min(self.h - 1, max(0, int(round(v * (self.h - 1)))))
        return float(self.gray[j, i]) * self.strength


def build_terrain(col, sampler):
    s, w, n, e = HEIGHTMAP["bounds"]
    x0, y0 = latlon_to_xy(s, w)
    x1, y1 = latlon_to_xy(n, e)
    cx, cy, sx, sy = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0), (y1 - y0)

    # 바다판
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    bmesh.ops.scale(bm, vec=Vector((sx, sy, 1)), verts=bm.verts)
    me = bpy.data.meshes.new(f"{MAP_ID}_{MAP_NAME}_Sea_L0")
    bm.to_mesh(me)
    bm.free()
    sea = bpy.data.objects.new(me.name, me)
    sea.location = (cx, cy, meters_to_units(SEA_LEVEL_OFFSET_M) * HEIGHT_EXAGGERATION)
    me.materials.append(material("sea"))
    col.objects.link(sea)

    if not sampler.ok:
        log("TERRAIN", built="sea_only", size_units=f"{sx:.3f}x{sy:.3f}")
        return
    # 지형 격자 + 높이 이미지 Displace
    seg = int(HEIGHTMAP["subdiv"])
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")
    bmesh.ops.create_grid(bm, x_segments=seg, y_segments=seg, size=0.5, calc_uvs=True)
    bmesh.ops.scale(bm, vec=Vector((sx, sy, 1)), verts=bm.verts)
    me = bpy.data.meshes.new(f"{MAP_ID}_{MAP_NAME}_Terrain_L0")
    bm.to_mesh(me)
    bm.free()
    terrain = bpy.data.objects.new(me.name, me)
    terrain.location = (cx, cy, 0)
    me.materials.append(material("land"))
    col.objects.link(terrain)
    tex = bpy.data.textures.get(f"T_{MAP_NAME}_Height") or bpy.data.textures.new(f"T_{MAP_NAME}_Height", "IMAGE")
    tex.image = sampler.image
    tex.extension = "EXTEND"
    mod = terrain.modifiers.new("Displace", "DISPLACE")
    mod.texture = tex
    mod.texture_coords = "UV"
    mod.mid_level = 0.0
    mod.strength = sampler.strength
    log("TERRAIN", built="sea+terrain", grid=f"{seg}x{seg}", size_units=f"{sx:.3f}x{sy:.3f}",
        real_km=f"{sx * KM_PER_UNIT:.1f}x{sy * KM_PER_UNIT:.1f}")


def build_pins(col, sampler):
    font = None
    if FONT_PATH:
        try:
            font = bpy.data.fonts.load(bpy.path.abspath(FONT_PATH), check_existing=True)
        except RuntimeError as e:
            log("PIN", logging.WARNING, issue="글꼴 열기 실패 → 이름표 생략", path=FONT_PATH, error=e)
    pin_mat = material("pin")
    positions = {}
    for p in PLACES:
        x, y = latlon_to_xy(p["lat"], p["lon"])
        z = sampler.height(p["lat"], p["lon"])
        positions[p["key"]] = (x, y, z)
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=PIN["segments"],
                              radius1=PIN["stem_diameter"] / 2, radius2=PIN["stem_diameter"] / 2,
                              depth=PIN["stem_height"])
        bmesh.ops.translate(bm, vec=Vector((0, 0, PIN["stem_height"] / 2)), verts=bm.verts)
        head = bmesh.ops.create_uvsphere(bm, u_segments=PIN["segments"], v_segments=8,
                                         radius=PIN["head_diameter"] / 2)
        bmesh.ops.translate(bm, vec=Vector((0, 0, PIN["stem_height"])), verts=head["verts"])
        me = bpy.data.meshes.new(f"{MAP_ID}_{MAP_NAME}_Pin{_camel(p['key'])}_L0")
        bm.to_mesh(me)
        bm.free()
        obj = bpy.data.objects.new(me.name, me)
        obj.location = (x, y, z)
        obj["place_name"] = p["name"]
        obj["lat"], obj["lon"], obj["coord_source"] = p["lat"], p["lon"], p["src"]
        me.materials.append(pin_mat)
        col.objects.link(obj)
        if font:
            cu = bpy.data.curves.new(f"{MAP_ID}_{MAP_NAME}_Label{_camel(p['key'])}_L0", "FONT")
            cu.body, cu.font, cu.size, cu.align_x = p["name"], font, LABEL_SIZE, "CENTER"
            t = bpy.data.objects.new(cu.name, cu)
            t.location = (x, y, z + PIN["stem_height"] + PIN["head_diameter"])
            t.rotation_euler = (math.radians(90), 0, 0)
            t.data.materials.append(pin_mat)
            col.objects.link(t)
        log("PIN", logging.DEBUG, key=p["key"], name=p["name"], xy=f"{x:.4f},{y:.4f}", z=f"{z:.4f}", src=p["src"])
    log("PIN", count=len(positions), labels=bool(font))
    return positions


def build_routes(col, sampler, positions):
    frame = ROUTE["start_frame"]
    for r in ROUTES:
        pts = []
        for k in r["stops"]:
            for (lat, lon) in r.get("via", {}).get(k, []):
                vx, vy = latlon_to_xy(lat, lon)
                pts.append((vx, vy, sampler.height(lat, lon)))
            pts.append(positions[k])
        cu = bpy.data.curves.new(f"{MAP_ID}_{MAP_NAME}_RouteDay{r['day']}_L0", "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth = ROUTE["bevel_depth"]
        cu.bevel_resolution = 2
        sp = cu.splines.new("POLY")
        sp.points.add(len(pts) - 1)
        for i, (x, y, z) in enumerate(pts):
            sp.points[i].co = (x, y, z + ROUTE["lift"], 1.0)
        obj = bpy.data.objects.new(cu.name, cu)
        cu.materials.append(material(r["color"], emission=2.0))
        col.objects.link(obj)
        cu.bevel_factor_end = 0.0
        cu.keyframe_insert("bevel_factor_end", frame=frame)
        cu.bevel_factor_end = 1.0
        cu.keyframe_insert("bevel_factor_end", frame=frame + ROUTE["frames_per_day"])
        length_km = 0.0
        for a, b in zip(r["stops"], r["stops"][1:]):
            pa = next(p for p in PLACES if p["key"] == a)
            pb = next(p for p in PLACES if p["key"] == b)
            length_km += haversine_km(pa["lat"], pa["lon"], pb["lat"], pb["lon"])
        log("ROUTE", day=r["day"], stops=len(r["stops"]), points=len(pts),
            straight_line_km=f"{length_km:.1f}", draw_frames=f"{frame}-{frame + ROUTE['frames_per_day']}")
        frame += ROUTE["frames_per_day"]


def _camel(key):
    return "".join(part.capitalize() for part in key.split("_"))


def main():
    setup_logging()
    log("START", map=f"{MAP_ID}_{MAP_NAME}", spec_version=SPEC_VERSION, places=len(PLACES), routes=len(ROUTES))
    problems = validate_inputs()
    for p in problems:
        log("VALIDATE", logging.ERROR, problem=p)
    if problems:
        log("VALIDATE", logging.ERROR, result="중단", count=len(problems), next_step="위 문제를 고친 뒤 다시 실행")
        return None
    log("VALIDATE", result="통과")
    if not IN_BLENDER:
        log("END", note="블렌더 밖이라 입력 검사만 함")
        return None
    col = get_clean_collection()
    sampler = HeightSampler()
    build_terrain(col, sampler)
    positions = build_pins(col, sampler)
    build_routes(col, sampler, positions)
    log("END", result="완료", objects=len(col.objects))
    return positions


def self_test():
    setup_logging()
    # 등장방형 근사 vs 하버사인: 지도 범위 안에서 0.5% 이내
    a, b = (35.11555, 129.04259), (35.15918, 129.15903)
    ax, ay = latlon_to_xy(*a)
    bx, by = latlon_to_xy(*b)
    approx_km = math.hypot(bx - ax, by - ay) * KM_PER_UNIT
    true_km = haversine_km(*a, *b)
    assert abs(approx_km - true_km) / true_km < 0.005, (approx_km, true_km)
    x, y = latlon_to_xy(REF_LAT, REF_LON)
    assert abs(x) < 1e-12 and abs(y) < 1e-12
    x, y = latlon_to_xy(REF_LAT + 0.1, REF_LON)
    assert y > 0 and abs(x) < 1e-12, "북쪽은 +Y"
    x, y = latlon_to_xy(REF_LAT, REF_LON + 0.1)
    assert x > 0, "동쪽은 +X"
    assert abs(meters_to_units(10000) - 1.0 / (KM_PER_UNIT / 10.0)) < 1e-12
    assert not validate_inputs(), validate_inputs()
    log("SELFTEST", result="통과", checks=6, sample_km=f"approx={approx_km:.3f} haversine={true_km:.3f}")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        main()

# CHANGELOG
# v1.0.0 — 2026-11-10 — 최초 작성: 위경도→평면 변환, 바다판, 높이 이미지 Displace 지형,
#                       높이 샘플링 핀, 일차별 루트 곡선(그려지는 애니메이션), 한글 이름표(선택), --self-test
