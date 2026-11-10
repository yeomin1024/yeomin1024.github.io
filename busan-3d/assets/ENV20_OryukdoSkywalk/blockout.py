# VERSION: v1.0 — 2026-11-10 — ENV20 최초 작성
"""
부산 3D 영상 프로젝트 — Blender 블록아웃(기본 형태) 스크립트 템플릿

[사용법]
  1. 이 파일을 busan-3d/assets/{ID}_{영문명}/blockout.py 로 복사한다.
  2. "1. 에셋 정보" ~ "3. 부품" 블록만 설계도(spec.md) 값으로 채운다. 아래 함수는 고치지 않는다.
  3. Blender 4.2 이상 > Scripting 탭 > 열기 > Run Script.
     (명령줄: blender --background --python blockout.py)
  4. 콘솔에 나오는 [STAGE] 로그와 [REPORT] 로그를 확인한다. 치수 오차가 TOLERANCE_M 를 넘으면 WARNING 이 찍힌다.
  5. 블렌더 밖에서 `python blockout.py --self-test` 로 입력값 검사만 따로 돌릴 수 있다.

[좌표 규칙]  1 unit = 1 m, Z-up, 정면은 -Y, 에셋 원점은 바닥 중앙(0,0,0).

[부품 정의 방법]
  name        : 부품 이름. 최종 오브젝트 이름은 {ASSET_ID}_{ASSET_NAME}_{name}_{LOD} 가 된다.
  shape       : "cube" | "cylinder" | "cone" | "sphere" | "plane" | "empty"
  size        : (x, y, z) 전체 치수(m). cylinder/cone/sphere 는 (지름X, 지름Y, 높이).
                cone 은 radius_top_ratio(0~1)로 위쪽 반지름 비율을 정한다.
  location    : 부모 기준 원점 위치(m). 부모가 없으면 에셋 원점 기준.
  rotation_deg: (x, y, z) 회전(도).
  pivot       : 이 부품 원점(회전 중심)이 도형의 어디에 있는지.
                "center"(도형 중심) | "bottom"(바닥 중앙) | (x, y, z) = 도형 중심에서 원점까지의 오프셋(m).
                예) 문 경첩이 문 왼쪽 끝 세로선이면 pivot=(-폭/2, 0, -높이/2) → 원점이 왼쪽 아래 모서리.
  parent      : 부모 부품 name (부모는 목록에서 먼저 나와야 한다).
  material    : MATERIALS 의 키.
  segments    : 원형 도형의 분할 수(기본 32).
  smooth      : True 면 면을 부드럽게 표시.
  bevel       : {"width": m, "segments": n}  (모디파이어, Apply 하지 않음)
  array       : {"count": n, "offset": (x, y, z)}  (일정 간격 반복, m)
  mirror      : "X" | "Y" | "Z" | "XY" ... 부모 원점 기준 대칭(부모가 없으면 자기 원점 기준).
                예) 오른쪽 바퀴를 차체(원점=바닥 중앙)의 자식으로 두고 mirror="X" → 왼쪽 바퀴가 생긴다.
  note        : 설계도 근거 메모([확인]/[추정]/[설정]).
"""

import logging
import math
import re
import sys
import time

try:
    import bpy
    import bmesh
    from mathutils import Euler, Vector
    IN_BLENDER = True
except ImportError:  # 블렌더 밖에서 --self-test 할 때
    bpy = bmesh = Euler = Vector = None
    IN_BLENDER = False

# ─────────────────────────────────────────────
# 1. 에셋 정보 (설계도 0~3번 섹션 값)
# ─────────────────────────────────────────────
ASSET_ID = 'ENV20'
ASSET_NAME = 'OryukdoSkywalk'
SPEC_VERSION = "v1.0"
LOD = "L0"  # [설정] 초안 블록아웃
EXPECTED_DIMS_M = (39.25, 34.0, 36.13)  # [설정] 사전 계산한 부품 합성 외곽; 실측 아님
TRI_BUDGET = 40000  # [설정] 완성 목표 상한
TOLERANCE_M = 0.01  # [설정] m
LOG_LEVEL = logging.INFO

# 2. 재질 — 모든 PBR·색 수치 [설정], 전역 팔레트
MATERIALS = {'Rock': {'base_hex': '#6E6A64', 'roughness': 0.65, 'metallic': 0.0},
 'Sky': {'base_hex': '#A9D6F0', 'roughness': 0.12, 'metallic': 0.0, 'alpha': 0.3, 'ior': 1.45},
 'Concrete': {'base_hex': '#B9B6AE', 'roughness': 0.65, 'metallic': 0.0}}

# 3. 부품 — 모든 치수·좌표·각도·분할 [설정], note의 확인값은 예외
PARTS = [{'name': 'Root',
  'shape': 'empty',
  'size': (0.1, 0.1, 0.1),
  'location': (0, 0, 0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님'},
 {'name': 'Cliff',
  'shape': 'cube',
  'size': (18, 10, 35),
  'location': (-10.625, -12.0, 17.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Rock',
  'bevel': {'width': 0.4, 'segments': 2}},
 {'name': 'SkywalkGlass0',
  'shape': 'cube',
  'size': (1.5, 0.625, 0.05549),
  'location': (-12.625, -6.6875, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkRail0S0',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-13.375, -6.6875, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkRail0S2',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-11.875, -6.6875, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkGlass1',
  'shape': 'cube',
  'size': (1.5, 0.625, 0.05549),
  'location': (-12.625, -6.0625, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkRail1S0',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-13.375, -6.0625, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkRail1S2',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-11.875, -6.0625, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkGlass2',
  'shape': 'cube',
  'size': (1.5, 0.625, 0.05549),
  'location': (-12.625, -5.4375, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkRail2S0',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-13.375, -5.4375, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkRail2S2',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-11.875, -5.4375, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkGlass3',
  'shape': 'cube',
  'size': (1.5, 0.625, 0.05549),
  'location': (-12.625, -4.8125, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkRail3S0',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-13.375, -4.8125, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkRail3S2',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-11.875, -4.8125, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkGlass4',
  'shape': 'cube',
  'size': (1.5, 0.625, 0.05549),
  'location': (-12.625, -4.1875, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkRail4S0',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-13.375, -4.1875, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkRail4S2',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-11.875, -4.1875, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkGlass5',
  'shape': 'cube',
  'size': (1.5, 0.625, 0.05549),
  'location': (-12.625, -3.5625, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkRail5S0',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-13.375, -3.5625, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkRail5S2',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-11.875, -3.5625, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0)},
 {'name': 'SkywalkGlass6',
  'shape': 'cube',
  'size': (1.5, 0.6249998134478305, 0.05549),
  'location': (-12.624965585678249, -2.937500095171038, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -0.0063097471477691095)},
 {'name': 'SkywalkRail6S0',
  'shape': 'cube',
  'size': (0.06, 0.6249998134478305, 0.06),
  'location': (-13.37496558113036, -2.937417500774182, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0063097471477691095)},
 {'name': 'SkywalkRail6S2',
  'shape': 'cube',
  'size': (0.06, 0.6249998134478305, 0.06),
  'location': (-11.87496559022614, -2.9375826895678943, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -0.0063097471477691095)},
 {'name': 'SkywalkGlass7',
  'shape': 'cube',
  'size': (1.5, 0.6224599710942239, 0.05549),
  'location': (-12.573950205033835, -2.317974059570666, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -9.427810059727996)},
 {'name': 'SkywalkRail7S0',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942239, 0.06),
  'location': (-13.31381978306876, -2.195120457676291, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -9.427810059727996)},
 {'name': 'SkywalkRail7S2',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942239, 0.06),
  'location': (-11.83408062699891, -2.4408276614650415, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -9.427810059727996)},
 {'name': 'SkywalkGlass8',
  'shape': 'cube',
  'size': (1.5, 0.6224599710942242, 0.05549),
  'location': (-12.38006572761628, -1.7344652161020466, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -27.3327411575662)},
 {'name': 'SkywalkRail8S0',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942242, 0.06),
  'location': (-13.046331974932984, -1.3900972621828185, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -27.3327411575662)},
 {'name': 'SkywalkRail8S2',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942242, 0.06),
  'location': (-11.713799480299574, -2.0788331700212748, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -27.3327411575662)},
 {'name': 'SkywalkGlass9',
  'shape': 'cube',
  'size': (1.5, 0.6224599710942242, 0.05549),
  'location': (-12.016178381201154, -1.2388244589920978, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -45.237672255404455)},
 {'name': 'SkywalkRail9S0',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942242, 0.06),
  'location': (-12.544304014792054, -0.7062990463175378, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -45.237672255404455)},
 {'name': 'SkywalkRail9S2',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942242, 0.06),
  'location': (-11.488052747610254, -1.7713498716666578, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -45.237672255404455)},
 {'name': 'SkywalkGlass10',
  'shape': 'cube',
  'size': (1.5, 0.6224599710942242, 0.05549),
  'location': (-11.517535787520842, -0.8790615860364035, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -63.14260335324265)},
 {'name': 'SkywalkRail10S0',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942242, 0.06),
  'location': (-11.856364391139605, -0.20996131151115804, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -63.14260335324265)},
 {'name': 'SkywalkRail10S2',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942242, 0.06),
  'location': (-11.17870718390208, -1.548161860561649, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -63.14260335324265)},
 {'name': 'SkywalkGlass11',
  'shape': 'cube',
  'size': (1.5, 0.6224599710942241, 0.05549),
  'location': (-10.932438514580381, -0.6900247055416209, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -81.04753445108089)},
 {'name': 'SkywalkRail11S0',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942241, 0.06),
  'location': (-11.049149759160548, 0.05083863232073327, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -81.04753445108089)},
 {'name': 'SkywalkRail11S2',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942241, 0.06),
  'location': (-10.815727270000213, -1.430888043403975, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -81.04753445108089)},
 {'name': 'SkywalkGlass12',
  'shape': 'cube',
  'size': (1.5, 0.6224599710942241, 0.05549),
  'location': (-10.317561485419619, -0.6900247055416209, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -98.95246554891911)},
 {'name': 'SkywalkRail12S0',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942241, 0.06),
  'location': (-10.200850240839452, 0.05083863232073327, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -98.95246554891911)},
 {'name': 'SkywalkRail12S2',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942241, 0.06),
  'location': (-10.434272729999787, -1.430888043403975, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -98.95246554891911)},
 {'name': 'SkywalkGlass13',
  'shape': 'cube',
  'size': (1.5, 0.6224599710942242, 0.05549),
  'location': (-9.732464212479156, -0.8790615860364035, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -116.85739664675737)},
 {'name': 'SkywalkRail13S0',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942242, 0.06),
  'location': (-9.393635608860393, -0.20996131151115804, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -116.85739664675737)},
 {'name': 'SkywalkRail13S2',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942242, 0.06),
  'location': (-10.07129281609792, -1.548161860561649, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -116.85739664675737)},
 {'name': 'SkywalkGlass14',
  'shape': 'cube',
  'size': (1.5, 0.622459971094224, 0.05549),
  'location': (-9.233821618798846, -1.2388244589920978, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -134.76232774459555)},
 {'name': 'SkywalkRail14S0',
  'shape': 'cube',
  'size': (0.06, 0.622459971094224, 0.06),
  'location': (-8.705695985207944, -0.7062990463175378, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -134.76232774459555)},
 {'name': 'SkywalkRail14S2',
  'shape': 'cube',
  'size': (0.06, 0.622459971094224, 0.06),
  'location': (-9.761947252389746, -1.7713498716666578, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -134.76232774459555)},
 {'name': 'SkywalkGlass15',
  'shape': 'cube',
  'size': (1.5, 0.6224599710942242, 0.05549),
  'location': (-8.86993427238372, -1.7344652161020466, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -152.66725884243382)},
 {'name': 'SkywalkRail15S0',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942242, 0.06),
  'location': (-8.203668025067016, -1.3900972621828185, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -152.66725884243382)},
 {'name': 'SkywalkRail15S2',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942242, 0.06),
  'location': (-9.536200519700426, -2.0788331700212748, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -152.66725884243382)},
 {'name': 'SkywalkGlass16',
  'shape': 'cube',
  'size': (1.5, 0.6224599710942239, 0.05549),
  'location': (-8.676049794966165, -2.317974059570666, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -170.572189940272)},
 {'name': 'SkywalkRail16S0',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942239, 0.06),
  'location': (-7.936180216931239, -2.195120457676291, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -170.572189940272)},
 {'name': 'SkywalkRail16S2',
  'shape': 'cube',
  'size': (0.06, 0.6224599710942239, 0.06),
  'location': (-9.41591937300109, -2.4408276614650415, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -170.572189940272)},
 {'name': 'SkywalkGlass17',
  'shape': 'cube',
  'size': (1.5, 0.6249998134478305, 0.05549),
  'location': (-8.625034414321751, -2.937500095171038, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -179.99369025285222)},
 {'name': 'SkywalkRail17S0',
  'shape': 'cube',
  'size': (0.06, 0.6249998134478305, 0.06),
  'location': (-7.875034418869641, -2.937417500774182, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -179.99369025285222)},
 {'name': 'SkywalkRail17S2',
  'shape': 'cube',
  'size': (0.06, 0.6249998134478305, 0.06),
  'location': (-9.37503440977386, -2.9375826895678943, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -179.99369025285222)},
 {'name': 'SkywalkGlass18',
  'shape': 'cube',
  'size': (1.5, 0.625, 0.05549),
  'location': (-8.625, -3.5625, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkRail18S0',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-7.875, -3.5625, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkRail18S2',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-9.375, -3.5625, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkGlass19',
  'shape': 'cube',
  'size': (1.5, 0.625, 0.05549),
  'location': (-8.625, -4.1875, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkRail19S0',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-7.875, -4.1875, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkRail19S2',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-9.375, -4.1875, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkGlass20',
  'shape': 'cube',
  'size': (1.5, 0.625, 0.05549),
  'location': (-8.625, -4.8125, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkRail20S0',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-7.875, -4.8125, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkRail20S2',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-9.375, -4.8125, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkGlass21',
  'shape': 'cube',
  'size': (1.5, 0.625, 0.05549),
  'location': (-8.625, -5.4375, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkRail21S0',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-7.875, -5.4375, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkRail21S2',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-9.375, -5.4375, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkGlass22',
  'shape': 'cube',
  'size': (1.5, 0.625, 0.05549),
  'location': (-8.625, -6.0625, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkRail22S0',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-7.875, -6.0625, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkRail22S2',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-9.375, -6.0625, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkGlass23',
  'shape': 'cube',
  'size': (1.5, 0.625, 0.05549),
  'location': (-8.625, -6.6875, 34.972255),
  'pivot': 'center',
  'note': 'X/Y [설정], Z=.05549m [확인: FACTS.md ENV20]',
  'parent': 'Root',
  'material': 'Sky',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkRail23S0',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-7.875, -6.6875, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SkywalkRail23S2',
  'shape': 'cube',
  'size': (0.06, 0.625, 0.06),
  'location': (-9.375, -6.6875, 36.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'rotation_deg': (0, 0, -180.0)},
 {'name': 'SchematicIsland0',
  'shape': 'sphere',
  'size': (3.0, 4, 3),
  'location': (-2.625, 5.0, 1.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Rock',
  'segments': 12,
  'smooth': True},
 {'name': 'SchematicIsland1',
  'shape': 'sphere',
  'size': (3.3, 4, 4),
  'location': (1.375, 7.0, 2.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Rock',
  'segments': 12,
  'smooth': True},
 {'name': 'SchematicIsland2',
  'shape': 'sphere',
  'size': (3.6, 4, 5),
  'location': (5.375, 9.0, 2.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Rock',
  'segments': 12,
  'smooth': True},
 {'name': 'SchematicIsland3',
  'shape': 'sphere',
  'size': (3.9, 4, 3),
  'location': (9.375, 11.0, 1.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Rock',
  'segments': 12,
  'smooth': True},
 {'name': 'SchematicIsland4',
  'shape': 'sphere',
  'size': (4.2, 4, 4),
  'location': (13.375, 13.0, 2.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Rock',
  'segments': 12,
  'smooth': True},
 {'name': 'SchematicIsland5',
  'shape': 'sphere',
  'size': (4.5, 4, 5),
  'location': (17.375, 15.0, 2.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Rock',
  'segments': 12,
  'smooth': True}]

# ═════════════════════════════════════════════
# 아래는 공용 함수 — 수정하지 않는다
# ═════════════════════════════════════════════
NAME_RE = re.compile(r"^(VEH|ENV|SF|CHR|PRP|FOOD|FX)\d{2}_[A-Za-z0-9]+_[A-Za-z0-9]+_L[0-2]$")
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
    if not re.fullmatch(r"(VEH|ENV|SF|CHR|PRP|FOOD|FX)\d{2}", ASSET_ID):
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
    assert not NAME_RE.match("veh02_CityBus_Door_L0")
    problems = validate_inputs()
    assert not problems, problems
    log("SELFTEST", result="통과", checks=8)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        main()

# CHANGELOG
# v1.0.0 — 2026-11-10 — 최초 작성: 입력 검사, 재질(hex→linear), bmesh 도형 생성, 원점(pivot) 처리,
#                       모디파이어(베벨·배열·미러[부모 원점 기준]), 부품/전체 치수·삼각형 리포트, --self-test
#                       Blender 4.2.0 / 5.2.3 (bpy 모듈)에서 2회 연속 실행·전 도형·옵션 동작 확인
