# VERSION: v1.0.0 — 2026-11-10 — MAP01 부산 3D 지도 빌드 (templates/map_template.py v1.1.0 복사, 1. 설정의 HEIGHTMAP 경로만 채움)
"""
부산 3D 영상 프로젝트 — 3D 지도 생성 스크립트 (MAP01 지형·바다 / MAP02 루트 / MAP03 핀)

[사용법]
  1. 이 파일을 busan-3d/assets/MAP01_BusanMap/map_build.py 로 복사한다.
  2. "1. 설정" 블록만 고친다. 장소 좌표는 FACTS.md 4장(OpenStreetMap 확인 좌표)을 쓴다.
  3. 지형 높이 자료(DEM 높이 이미지 PNG)가 있으면 HEIGHTMAP["path"] 에 넣는다.
     상대경로는 이 스크립트 파일이 있는 폴더 기준이다. "//" 로 시작하면 .blend 파일 기준이다.
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
  - ROUTES 의 stops 는 PLACES 의 key 순서. via 는 그 장소에 도착하기 전에 지나는 VIA_POINTS key 목록이다
    (실제 버스가 지나는 주요 정류장, OpenStreetMap 좌표).
  - 점과 점 사이는 직선이다. 도로를 정확히 따르지 않으므로 영상 자막에 '경로 개략'이라고 쓴다.
  - 선은 ROUTE['step_km'] 간격으로 잘게 나눠 지형 높이 위에 올린다(산을 뚫고 지나가지 않게).
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
    "path": "dem_busan_cop30.png",       # 이 폴더의 높이 이미지 (dem_process.py 결과, dem_busan_cop30.json 참고)
    "bounds": (35.05, 128.98, 35.25, 129.26),   # (남, 서, 북, 동) [설정] 일정 전체 + 여백
    "max_elevation_m": 640.0,            # 이미지 값 1.0 에 해당하는 해발 고도 (MAP01 고도 자료 처리 기록과 맞춘다)
    "subdiv": 300,                       # 격자 분할 수 (300 → 삼각형 약 18만, 지시서 예산 20만 이하)
}
SEA_LEVEL_OFFSET_M = 0.3                 # 이 높이(해발 m) 아래는 바다 색. Copernicus DEM 은 바다가 0 m, 육지는 대부분 0.5 m 이상

PIN = {"stem_height": 0.06, "stem_diameter": 0.006, "head_diameter": 0.02, "segments": 16}
ROUTE = {"bevel_depth": 0.004, "lift": 0.004, "day_offset": 0.003, "step_km": 0.25, "frames_per_day": 72, "start_frame": 1}
FONT_PATH = ""                           # 한글 글꼴 경로(예: NotoSansKR). 비우면 이름표를 만들지 않음
LABEL_SIZE = 0.03

COLORS = {
    "sea": "#0E4C77", "land": "#B9B6AE", "land_high": "#8FC9B9", "pin": "#F2EFE6",
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

# 경유 지점: 실제 버스가 지나는 주요 정류장 (OpenStreetMap, 2026-11-10 조회) — FACTS.md 4-2
VIA_POINTS = {
    "toseong": {"name": "부산대학병원(토성역) 정류장", "lat": 35.09912, "lon": 129.01996, "src": "OSM node/5004274572"},
    "busanjin": {"name": "부산진역 정류장", "lat": 35.12870, "lon": 129.04884, "src": "OSM node/5004396500"},
    "munhyeon": {"name": "문현교차로 정류장", "lat": 35.13655, "lon": 129.07166, "src": "OSM node/5004274583"},
    "gwangan_stn": {"name": "광안역 정류장", "lat": 35.15928, "lon": 129.11334, "src": "OSM node/5004247389"},
    "dongbaek_entr": {"name": "동백섬입구 정류장", "lat": 35.15827, "lon": 129.15406, "src": "OSM node/5004282295"},
    "dongbaek_stn": {"name": "동백역 정류장", "lat": 35.16177, "lon": 129.14733, "src": "OSM node/4986798628"},
    "igidae_entr": {"name": "이기대입구 정류장", "lat": 35.12321, "lon": 129.11252, "src": "OSM node/4533702797"},
}

# 루트: FACTS.md 1장 일정 순서. 광안대교·오륙도는 루트 없이 핀만 둔다.
# via 의 값은 VIA_POINTS 또는 PLACES 의 key (그 장소에 도착하기 전에 지나는 순서)
ROUTES = [
    {"day": 1, "color": "day1",
     "stops": ["busan_station", "gamcheon", "biff", "gukje", "yeongdo_bridge", "huinnyeoul", "jagalchi", "haeundae_beach"],
     "via": {"gamcheon": ["biff", "toseong"],                    # 61·서구2-2: 부산역 → 남포·자갈치 → 토성 → 감천
             "biff": ["toseong"],                                # 서구2-2 하행
             "jagalchi": ["yeongdo_bridge"],                     # 7·71: 영도대교 건너 자갈치
             "haeundae_beach": ["busan_station", "busanjin", "munhyeon", "kyungsung", "gwangan_stn", "dongbaek_entr"]}},  # 1003
    {"day": 2, "color": "day2",
     "stops": ["haeundae_beach", "haeundae_station", "yonggungsa", "yeonhwari", "songjeong_beach", "songjeong_station",
               "daritdol", "cheongsapo", "mipo", "haeundae_beach", "nurimaru", "millak", "gwangalli", "haeundae_beach"],
     "via": {"yonggungsa": ["songjeong_beach"],                  # 181: 해운대역 → 송정 → 용궁사
             "songjeong_beach": ["yonggungsa"],                  # 181 상행: 연화리 → 용궁사 → 송정
             "millak": ["dongbaek_stn"],                         # 38: 동백역 → 민락
             "haeundae_beach": ["gwangan_stn", "dongbaek_entr"]}},  # 마지막 구간 1003 (앞 구간 mipo→해운대는 도보라 영향 없음)
    {"day": 3, "color": "day3",
     "stops": ["haeundae_beach", "mipo", "kyungsung", "oryukdo_skywalk", "igidae_bridge", "dongsaengmal", "busan_station"],
     "via": {"kyungsung": ["haeundae_beach", "dongbaek_entr", "gwangan_stn"],   # 1003: 미포 → 해운대 → 광안 → 경성대
             "oryukdo_skywalk": ["igidae_entr"],                               # 131
             "busan_station": ["igidae_entr", "kyungsung", "munhyeon", "busanjin"]}},  # 27
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
        for k, vias in r.get("via", {}).items():
            if k not in r["stops"]:
                problems.append(f"{r['day']}일차 via: 루트에 없는 장소 {k}")
            for v in vias:
                if v not in VIA_POINTS and v not in keys:
                    problems.append(f"{r['day']}일차 via: 없는 경유 지점 {v}")
    for k, v in VIA_POINTS.items():
        if not (s <= v["lat"] <= n and w <= v["lon"] <= e) or not v.get("src"):
            problems.append(f"경유 지점 {k}: 범위 밖이거나 출처 없음")
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


def resolve_path(path):
    """'//' 는 .blend 기준, 그 밖의 상대경로는 이 스크립트 파일 폴더 기준."""
    import os
    if path.startswith("//"):
        return bpy.path.abspath(path)
    if os.path.isabs(path):
        return path
    base = os.path.dirname(os.path.abspath(globals().get("__file__", "") or os.getcwd()))
    return os.path.join(base, path)


def land_material(image):
    """높이 이미지 값으로 색을 정한다: 0 m(바다) → sea, 땅은 낮을수록 land, 높을수록 land_high.
    해안선이 메시 격자(약 85 m)가 아니라 이미지 해상도(약 30 m)로 깔끔하게 그려진다."""
    name = f"M_{MAP_NAME}_land"
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None) or nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Roughness"].default_value = 0.8
    for n in [n for n in nt.nodes if n.type in ("UVMAP", "TEX_IMAGE", "VALTORGB", "NEW_GEOMETRY", "SEPXYZ", "MAP_RANGE")]:
        nt.nodes.remove(n)
    uv = nt.nodes.new("ShaderNodeUVMap")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image, tex.interpolation, tex.extension = image, "Linear", "EXTEND"
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    sea_edge = meters_to_units(SEA_LEVEL_OFFSET_M) / meters_to_units(HEIGHTMAP["max_elevation_m"])  # 높이 비율
    els = ramp.color_ramp.elements
    els[0].position, els[0].color = 0.0, hex_to_linear_rgba(COLORS["sea"])
    els[1].position, els[1].color = 1.0, hex_to_linear_rgba(COLORS["land_high"])
    e1 = els.new(sea_edge * 0.999)
    e1.color = hex_to_linear_rgba(COLORS["sea"])
    e2 = els.new(sea_edge)
    e2.color = hex_to_linear_rgba(COLORS["land"])
    nt.links.new(uv.outputs["UV"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    mat.diffuse_color = hex_to_linear_rgba(COLORS["land"])
    return mat


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
            self.image = bpy.data.images.load(resolve_path(path), check_existing=True)
        except RuntimeError as e:
            log("TERRAIN", logging.ERROR, issue="높이 이미지 열기 실패", path=path, error=e,
                next_step="경로·파일 형식(PNG) 확인")
            return
        # 높이 자료는 색이 아니다: sRGB → 선형 변환이 걸리면 낮은·중간 높이가 눌린다 (예: 13 m → 1 m)
        self.image.colorspace_settings.name = "Non-Color"
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

    if sampler.ok:
        build_terrain_mesh(col, sampler, cx, cy, sx, sy)
        return
    # 높이 자료가 없을 때: 바다판만
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

    log("TERRAIN", built="sea_only", size_units=f"{sx:.3f}x{sy:.3f}")


def build_terrain_mesh(col, sampler, cx, cy, sx, sy):
    """지형 격자 + 높이 이미지 Displace. 바다(0 m)도 이 격자가 덮고, 재질이 바다 색을 칠한다."""
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
    me.materials.append(land_material(sampler.image))
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


def route_latlons(r):
    """한 루트의 (lat, lon, 이름) 목록: 정류장 + 그 앞의 경유 지점."""
    place = {p["key"]: p for p in PLACES}
    out = []
    for k in r["stops"]:
        for v in r.get("via", {}).get(k, []):
            vp = VIA_POINTS.get(v) or place[v]
            out.append((vp["lat"], vp["lon"], vp["name"]))
        out.append((place[k]["lat"], place[k]["lon"], place[k]["name"]))
    return out


def build_routes(col, sampler, positions):
    frame = ROUTE["start_frame"]
    for r in ROUTES:
        ll = route_latlons(r)
        pts = []
        length_km = 0.0
        for (la0, lo0, _), (la1, lo1, _) in zip(ll, ll[1:]):
            seg_km = haversine_km(la0, lo0, la1, lo1)
            length_km += seg_km
            n = max(1, math.ceil(seg_km / ROUTE["step_km"]))
            for t in range(n):
                f = t / n
                la, lo = la0 + (la1 - la0) * f, lo0 + (lo1 - lo0) * f
                x, y = latlon_to_xy(la, lo)
                pts.append((x, y, sampler.height(la, lo)))
        x, y = latlon_to_xy(ll[-1][0], ll[-1][1])
        pts.append((x, y, sampler.height(ll[-1][0], ll[-1][1])))
        cu = bpy.data.curves.new(f"{MAP_ID}_{MAP_NAME}_RouteDay{r['day']}_L0", "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth = ROUTE["bevel_depth"]
        cu.bevel_resolution = 2
        sp = cu.splines.new("POLY")
        sp.points.add(len(pts) - 1)
        lift = ROUTE["lift"] + (r["day"] - 1) * ROUTE.get("day_offset", 0.0)   # 같은 길을 지나는 날끼리 겹침 방지
        for i, (x, y, z) in enumerate(pts):
            sp.points[i].co = (x, y, z + lift, 1.0)
        obj = bpy.data.objects.new(cu.name, cu)
        obj["path_km"] = round(length_km, 2)
        obj["path_note"] = "정류장·경유 정류장을 이은 직선(경로 개략)"
        cu.materials.append(material(r["color"], emission=0.8))
        col.objects.link(obj)
        cu.bevel_factor_end = 0.0
        cu.keyframe_insert("bevel_factor_end", frame=frame)
        cu.bevel_factor_end = 1.0
        cu.keyframe_insert("bevel_factor_end", frame=frame + ROUTE["frames_per_day"])
        log("ROUTE", day=r["day"], stops=len(r["stops"]), waypoints=len(ll), curve_points=len(pts),
            path_km=f"{length_km:.1f}", draw_frames=f"{frame}-{frame + ROUTE['frames_per_day']}")
        frame += ROUTE["frames_per_day"]


def _camel(key):
    return "".join(part.capitalize() for part in key.split("_"))


def main():
    setup_logging()
    log("START", map=f"{MAP_ID}_{MAP_NAME}", spec_version=SPEC_VERSION, places=len(PLACES),
        via_points=len(VIA_POINTS), routes=len(ROUTES))
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
    ll = route_latlons(ROUTES[0])
    assert ll[0][2] == "부산역" and len(ll) == len(ROUTES[0]["stops"]) + sum(len(v) for v in ROUTES[0]["via"].values())
    log("SELFTEST", result="통과", checks=8, sample_km=f"approx={approx_km:.3f} haversine={true_km:.3f}")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        main()

# CHANGELOG
# v1.1.0 — 2026-11-10 — VIA_POINTS(실제 버스 경유 정류장 7곳) 추가, 루트를 step_km 간격으로 나눠 지형 위로 올림,
#                       경로 길이에 경유 지점 포함, 산 높이에 따라 땅 색 변화, 상대경로=스크립트 폴더 기준,
#                       바다판 0.3 m(Copernicus 바다=0 m), 격자 300, 루트 두께 0.004,
#                       높이 이미지를 Non-Color 로 읽음(색 변환 때문에 높이가 눌리던 문제 수정),
#                       지형이 있으면 바다판 대신 지형 재질이 높이 이미지로 바다·땅을 칠함(해안선 계단 현상 제거),
#                       루트 발광 0.8(색이 하얗게 날아가던 문제)
#                       일차별 높이 차(day_offset 0.003)로 같은 길을 지나는 루트끼리 색이 섞이지 않게 함
# v1.0.0 — 2026-11-10 — 최초 작성: 위경도→평면 변환, 바다판, 높이 이미지 Displace 지형,
#                       높이 샘플링 핀, 일차별 루트 곡선(그려지는 애니메이션), 한글 이름표(선택), --self-test
