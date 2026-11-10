# VERSION: v1.0 — 2026-11-10 — ENV17 최초 작성
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
ASSET_ID = 'ENV17'
ASSET_NAME = 'GwanganBridge'
SPEC_VERSION = "v1.0"
LOD = "L0"  # [설정] 초안 블록아웃
EXPECTED_DIMS_M = (7420.0, 27.0, 100.0)  # [설정] 사전 계산한 부품 합성 외곽; 실측 아님
TRI_BUDGET = 40000  # [설정] 완성 목표 상한
TOLERANCE_M = 0.01  # [설정] m
LOG_LEVEL = logging.INFO

# 2. 재질 — 모든 PBR·색 수치 [설정], 전역 팔레트
MATERIALS = {'Concrete': {'base_hex': '#B9B6AE', 'roughness': 0.65, 'metallic': 0.0},
 'White': {'base_hex': '#F2EFE6', 'roughness': 0.65, 'metallic': 0.0}}

# 3. 부품 — 모든 치수·좌표·각도·분할 [설정], note의 확인값은 예외
PARTS = [{'name': 'Root',
  'shape': 'empty',
  'size': (0.1, 0.1, 0.1),
  'location': (0, 0, 0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님'},
 {'name': 'LowerDeck',
  'shape': 'cube',
  'size': (7420, 24, 1.2),
  'location': (0.0, 0.0, 12.0),
  'pivot': 'center',
  'note': 'X=7420m·Y=24m [확인: FACTS.md ENV17], Z [설정]',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'UpperDeck',
  'shape': 'cube',
  'size': (7420, 24, 1.2),
  'location': (0.0, 0.0, 18.0),
  'pivot': 'center',
  'note': 'X=7420m·Y=24m [확인: FACTS.md ENV17], Z [설정]',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Tower0Leg0',
  'shape': 'cube',
  'size': (5, 5, 100),
  'location': (-250.0, -11.0, 50.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'bevel': {'width': 0.1, 'segments': 2}},
 {'name': 'Tower0Leg1',
  'shape': 'cube',
  'size': (5, 5, 100),
  'location': (-250.0, 11.0, 50.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'bevel': {'width': 0.1, 'segments': 2}},
 {'name': 'TowerCross0',
  'shape': 'cube',
  'size': (8, 27, 4),
  'location': (-250.0, 0.0, 86.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White'},
 {'name': 'Tower1Leg0',
  'shape': 'cube',
  'size': (5, 5, 100),
  'location': (250.0, -11.0, 50.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'bevel': {'width': 0.1, 'segments': 2}},
 {'name': 'Tower1Leg1',
  'shape': 'cube',
  'size': (5, 5, 100),
  'location': (250.0, 11.0, 50.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'bevel': {'width': 0.1, 'segments': 2}},
 {'name': 'TowerCross1',
  'shape': 'cube',
  'size': (8, 27, 4),
  'location': (250.0, 0.0, 86.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White'},
 {'name': 'Hanger0N0',
  'shape': 'cube',
  'size': (0.15, 0.15, 15.999999999999993),
  'location': (-450.0, -11.0, 25.999999999999996),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Hanger0N1',
  'shape': 'cube',
  'size': (0.15, 0.15, 22.999999999999993),
  'location': (-425.0, -11.0, 29.499999999999996),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N1',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-437.5, -11.0, 37.49999999999999),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger0N2',
  'shape': 'cube',
  'size': (0.15, 0.15, 29.999999999999993),
  'location': (-400.0, -11.0, 33.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N2',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-412.5, -11.0, 44.49999999999999),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger0N3',
  'shape': 'cube',
  'size': (0.15, 0.15, 37.0),
  'location': (-375.0, -11.0, 36.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N3',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-387.5, -11.0, 51.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208744, 0)},
 {'name': 'Hanger0N4',
  'shape': 'cube',
  'size': (0.15, 0.15, 44.0),
  'location': (-350.0, -11.0, 40.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N4',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-362.5, -11.0, 58.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger0N5',
  'shape': 'cube',
  'size': (0.15, 0.15, 51.0),
  'location': (-325.0, -11.0, 43.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N5',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-337.5, -11.0, 65.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger0N6',
  'shape': 'cube',
  'size': (0.15, 0.15, 58.0),
  'location': (-300.0, -11.0, 47.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N6',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-312.5, -11.0, 72.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger0N7',
  'shape': 'cube',
  'size': (0.15, 0.15, 65.0),
  'location': (-275.0, -11.0, 50.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N7',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-287.5, -11.0, 79.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger0N8',
  'shape': 'cube',
  'size': (0.15, 0.15, 72.0),
  'location': (-250.0, -11.0, 54.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N8',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-262.5, -11.0, 86.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger0N9',
  'shape': 'cube',
  'size': (0.15, 0.15, 61.55000000000001),
  'location': (-225.0, -11.0, 48.775000000000006),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N9',
  'shape': 'cube',
  'size': (27.096171316257944, 0.3, 0.3),
  'location': (-237.5, -11.0, 84.775),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 22.68492755117529, 0)},
 {'name': 'Hanger0N10',
  'shape': 'cube',
  'size': (0.15, 0.15, 52.20000000000002),
  'location': (-200.0, -11.0, 44.10000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N10',
  'shape': 'cube',
  'size': (26.691243882591905, 0.3, 0.3),
  'location': (-212.5, -11.0, 74.87500000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 20.505796796146676, 0)},
 {'name': 'Hanger0N11',
  'shape': 'cube',
  'size': (0.15, 0.15, 43.949999999999996),
  'location': (-175.0, -11.0, 39.974999999999994),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N11',
  'shape': 'cube',
  'size': (26.32608022475052, 0.3, 0.3),
  'location': (-187.5, -11.0, 66.075),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 18.262889942194175, 0)},
 {'name': 'Hanger0N12',
  'shape': 'cube',
  'size': (0.15, 0.15, 36.8),
  'location': (-150.0, -11.0, 36.4),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N12',
  'shape': 'cube',
  'size': (26.002355662516425, 0.3, 0.3),
  'location': (-162.5, -11.0, 58.375),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.960529492624033, 0)},
 {'name': 'Hanger0N13',
  'shape': 'cube',
  'size': (0.15, 0.15, 30.75),
  'location': (-125.0, -11.0, 33.375),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N13',
  'shape': 'cube',
  'size': (25.721634862504366, 0.3, 0.3),
  'location': (-137.5, -11.0, 51.775),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 13.604034564773448, 0)},
 {'name': 'Hanger0N14',
  'shape': 'cube',
  'size': (0.15, 0.15, 25.800000000000004),
  'location': (-100.0, -11.0, 30.900000000000002),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N14',
  'shape': 'cube',
  'size': (25.485338922604107, 0.3, 0.3),
  'location': (-112.5, -11.0, 46.275000000000006),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 11.199706023793224, 0)},
 {'name': 'Hanger0N15',
  'shape': 'cube',
  'size': (0.15, 0.15, 21.950000000000003),
  'location': (-75.0, -11.0, 28.975),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N15',
  'shape': 'cube',
  'size': (25.294712886293055, 0.3, 0.3),
  'location': (-87.5, -11.0, 41.875),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 8.754772989799235, 0)},
 {'name': 'Hanger0N16',
  'shape': 'cube',
  'size': (0.15, 0.15, 19.200000000000003),
  'location': (-50.0, -11.0, 27.6),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N16',
  'shape': 'cube',
  'size': (25.15079521605629, 0.3, 0.3),
  'location': (-62.5, -11.0, 38.575),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 6.2772984895975545, 0)},
 {'name': 'Hanger0N17',
  'shape': 'cube',
  'size': (0.15, 0.15, 17.549999999999997),
  'location': (-25.0, -11.0, 26.775),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N17',
  'shape': 'cube',
  'size': (25.054390832746265, 0.3, 0.3),
  'location': (-37.5, -11.0, 36.375),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 3.776044984895022, 0)},
 {'name': 'Hanger0N18',
  'shape': 'cube',
  'size': (0.15, 0.15, 17.0),
  'location': (0.0, -11.0, 26.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N18',
  'shape': 'cube',
  'size': (25.006049268127104, 0.3, 0.3),
  'location': (-12.5, -11.0, 35.275),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 1.2603038465035832, 0)},
 {'name': 'Hanger0N19',
  'shape': 'cube',
  'size': (0.15, 0.15, 17.549999999999997),
  'location': (25.0, -11.0, 26.775),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N19',
  'shape': 'cube',
  'size': (25.006049268127104, 0.3, 0.3),
  'location': (12.5, -11.0, 35.275),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -1.2603038465035832, 0)},
 {'name': 'Hanger0N20',
  'shape': 'cube',
  'size': (0.15, 0.15, 19.200000000000003),
  'location': (50.0, -11.0, 27.6),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N20',
  'shape': 'cube',
  'size': (25.054390832746265, 0.3, 0.3),
  'location': (37.5, -11.0, 36.375),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -3.776044984895022, 0)},
 {'name': 'Hanger0N21',
  'shape': 'cube',
  'size': (0.15, 0.15, 21.950000000000003),
  'location': (75.0, -11.0, 28.975),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N21',
  'shape': 'cube',
  'size': (25.15079521605629, 0.3, 0.3),
  'location': (62.5, -11.0, 38.575),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -6.2772984895975545, 0)},
 {'name': 'Hanger0N22',
  'shape': 'cube',
  'size': (0.15, 0.15, 25.800000000000004),
  'location': (100.0, -11.0, 30.900000000000002),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N22',
  'shape': 'cube',
  'size': (25.294712886293055, 0.3, 0.3),
  'location': (87.5, -11.0, 41.875),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -8.754772989799235, 0)},
 {'name': 'Hanger0N23',
  'shape': 'cube',
  'size': (0.15, 0.15, 30.75),
  'location': (125.0, -11.0, 33.375),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N23',
  'shape': 'cube',
  'size': (25.485338922604107, 0.3, 0.3),
  'location': (112.5, -11.0, 46.275000000000006),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -11.199706023793224, 0)},
 {'name': 'Hanger0N24',
  'shape': 'cube',
  'size': (0.15, 0.15, 36.8),
  'location': (150.0, -11.0, 36.4),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N24',
  'shape': 'cube',
  'size': (25.721634862504366, 0.3, 0.3),
  'location': (137.5, -11.0, 51.775),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -13.604034564773448, 0)},
 {'name': 'Hanger0N25',
  'shape': 'cube',
  'size': (0.15, 0.15, 43.949999999999996),
  'location': (175.0, -11.0, 39.974999999999994),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N25',
  'shape': 'cube',
  'size': (26.002355662516425, 0.3, 0.3),
  'location': (162.5, -11.0, 58.375),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.960529492624033, 0)},
 {'name': 'Hanger0N26',
  'shape': 'cube',
  'size': (0.15, 0.15, 52.20000000000002),
  'location': (200.0, -11.0, 44.10000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N26',
  'shape': 'cube',
  'size': (26.32608022475052, 0.3, 0.3),
  'location': (187.5, -11.0, 66.075),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -18.262889942194175, 0)},
 {'name': 'Hanger0N27',
  'shape': 'cube',
  'size': (0.15, 0.15, 61.55000000000001),
  'location': (225.0, -11.0, 48.775000000000006),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N27',
  'shape': 'cube',
  'size': (26.691243882591905, 0.3, 0.3),
  'location': (212.5, -11.0, 74.87500000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -20.505796796146676, 0)},
 {'name': 'Hanger0N28',
  'shape': 'cube',
  'size': (0.15, 0.15, 72.0),
  'location': (250.0, -11.0, 54.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N28',
  'shape': 'cube',
  'size': (27.096171316257944, 0.3, 0.3),
  'location': (237.5, -11.0, 84.775),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -22.68492755117529, 0)},
 {'name': 'Hanger0N29',
  'shape': 'cube',
  'size': (0.15, 0.15, 65.0),
  'location': (275.0, -11.0, 50.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N29',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (262.5, -11.0, 86.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger0N30',
  'shape': 'cube',
  'size': (0.15, 0.15, 58.0),
  'location': (300.0, -11.0, 47.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N30',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (287.5, -11.0, 79.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger0N31',
  'shape': 'cube',
  'size': (0.15, 0.15, 51.0),
  'location': (325.0, -11.0, 43.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N31',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (312.5, -11.0, 72.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger0N32',
  'shape': 'cube',
  'size': (0.15, 0.15, 44.0),
  'location': (350.0, -11.0, 40.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N32',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (337.5, -11.0, 65.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger0N33',
  'shape': 'cube',
  'size': (0.15, 0.15, 37.0),
  'location': (375.0, -11.0, 36.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N33',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (362.5, -11.0, 58.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger0N34',
  'shape': 'cube',
  'size': (0.15, 0.15, 29.999999999999993),
  'location': (400.0, -11.0, 33.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N34',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (387.5, -11.0, 51.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208744, 0)},
 {'name': 'Hanger0N35',
  'shape': 'cube',
  'size': (0.15, 0.15, 22.999999999999993),
  'location': (425.0, -11.0, 29.499999999999996),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N35',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (412.5, -11.0, 44.49999999999999),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger0N36',
  'shape': 'cube',
  'size': (0.15, 0.15, 15.999999999999993),
  'location': (450.0, -11.0, 25.999999999999996),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable0N36',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (437.5, -11.0, 37.49999999999999),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger1N0',
  'shape': 'cube',
  'size': (0.15, 0.15, 15.999999999999993),
  'location': (-450.0, 11.0, 25.999999999999996),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Hanger1N1',
  'shape': 'cube',
  'size': (0.15, 0.15, 22.999999999999993),
  'location': (-425.0, 11.0, 29.499999999999996),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N1',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-437.5, 11.0, 37.49999999999999),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger1N2',
  'shape': 'cube',
  'size': (0.15, 0.15, 29.999999999999993),
  'location': (-400.0, 11.0, 33.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N2',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-412.5, 11.0, 44.49999999999999),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger1N3',
  'shape': 'cube',
  'size': (0.15, 0.15, 37.0),
  'location': (-375.0, 11.0, 36.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N3',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-387.5, 11.0, 51.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208744, 0)},
 {'name': 'Hanger1N4',
  'shape': 'cube',
  'size': (0.15, 0.15, 44.0),
  'location': (-350.0, 11.0, 40.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N4',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-362.5, 11.0, 58.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger1N5',
  'shape': 'cube',
  'size': (0.15, 0.15, 51.0),
  'location': (-325.0, 11.0, 43.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N5',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-337.5, 11.0, 65.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger1N6',
  'shape': 'cube',
  'size': (0.15, 0.15, 58.0),
  'location': (-300.0, 11.0, 47.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N6',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-312.5, 11.0, 72.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger1N7',
  'shape': 'cube',
  'size': (0.15, 0.15, 65.0),
  'location': (-275.0, 11.0, 50.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N7',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-287.5, 11.0, 79.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger1N8',
  'shape': 'cube',
  'size': (0.15, 0.15, 72.0),
  'location': (-250.0, 11.0, 54.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N8',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (-262.5, 11.0, 86.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.642246457208728, 0)},
 {'name': 'Hanger1N9',
  'shape': 'cube',
  'size': (0.15, 0.15, 61.55000000000001),
  'location': (-225.0, 11.0, 48.775000000000006),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N9',
  'shape': 'cube',
  'size': (27.096171316257944, 0.3, 0.3),
  'location': (-237.5, 11.0, 84.775),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 22.68492755117529, 0)},
 {'name': 'Hanger1N10',
  'shape': 'cube',
  'size': (0.15, 0.15, 52.20000000000002),
  'location': (-200.0, 11.0, 44.10000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N10',
  'shape': 'cube',
  'size': (26.691243882591905, 0.3, 0.3),
  'location': (-212.5, 11.0, 74.87500000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 20.505796796146676, 0)},
 {'name': 'Hanger1N11',
  'shape': 'cube',
  'size': (0.15, 0.15, 43.949999999999996),
  'location': (-175.0, 11.0, 39.974999999999994),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N11',
  'shape': 'cube',
  'size': (26.32608022475052, 0.3, 0.3),
  'location': (-187.5, 11.0, 66.075),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 18.262889942194175, 0)},
 {'name': 'Hanger1N12',
  'shape': 'cube',
  'size': (0.15, 0.15, 36.8),
  'location': (-150.0, 11.0, 36.4),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N12',
  'shape': 'cube',
  'size': (26.002355662516425, 0.3, 0.3),
  'location': (-162.5, 11.0, 58.375),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.960529492624033, 0)},
 {'name': 'Hanger1N13',
  'shape': 'cube',
  'size': (0.15, 0.15, 30.75),
  'location': (-125.0, 11.0, 33.375),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N13',
  'shape': 'cube',
  'size': (25.721634862504366, 0.3, 0.3),
  'location': (-137.5, 11.0, 51.775),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 13.604034564773448, 0)},
 {'name': 'Hanger1N14',
  'shape': 'cube',
  'size': (0.15, 0.15, 25.800000000000004),
  'location': (-100.0, 11.0, 30.900000000000002),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N14',
  'shape': 'cube',
  'size': (25.485338922604107, 0.3, 0.3),
  'location': (-112.5, 11.0, 46.275000000000006),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 11.199706023793224, 0)},
 {'name': 'Hanger1N15',
  'shape': 'cube',
  'size': (0.15, 0.15, 21.950000000000003),
  'location': (-75.0, 11.0, 28.975),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N15',
  'shape': 'cube',
  'size': (25.294712886293055, 0.3, 0.3),
  'location': (-87.5, 11.0, 41.875),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 8.754772989799235, 0)},
 {'name': 'Hanger1N16',
  'shape': 'cube',
  'size': (0.15, 0.15, 19.200000000000003),
  'location': (-50.0, 11.0, 27.6),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N16',
  'shape': 'cube',
  'size': (25.15079521605629, 0.3, 0.3),
  'location': (-62.5, 11.0, 38.575),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 6.2772984895975545, 0)},
 {'name': 'Hanger1N17',
  'shape': 'cube',
  'size': (0.15, 0.15, 17.549999999999997),
  'location': (-25.0, 11.0, 26.775),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N17',
  'shape': 'cube',
  'size': (25.054390832746265, 0.3, 0.3),
  'location': (-37.5, 11.0, 36.375),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 3.776044984895022, 0)},
 {'name': 'Hanger1N18',
  'shape': 'cube',
  'size': (0.15, 0.15, 17.0),
  'location': (0.0, 11.0, 26.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N18',
  'shape': 'cube',
  'size': (25.006049268127104, 0.3, 0.3),
  'location': (-12.5, 11.0, 35.275),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 1.2603038465035832, 0)},
 {'name': 'Hanger1N19',
  'shape': 'cube',
  'size': (0.15, 0.15, 17.549999999999997),
  'location': (25.0, 11.0, 26.775),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N19',
  'shape': 'cube',
  'size': (25.006049268127104, 0.3, 0.3),
  'location': (12.5, 11.0, 35.275),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -1.2603038465035832, 0)},
 {'name': 'Hanger1N20',
  'shape': 'cube',
  'size': (0.15, 0.15, 19.200000000000003),
  'location': (50.0, 11.0, 27.6),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N20',
  'shape': 'cube',
  'size': (25.054390832746265, 0.3, 0.3),
  'location': (37.5, 11.0, 36.375),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -3.776044984895022, 0)},
 {'name': 'Hanger1N21',
  'shape': 'cube',
  'size': (0.15, 0.15, 21.950000000000003),
  'location': (75.0, 11.0, 28.975),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N21',
  'shape': 'cube',
  'size': (25.15079521605629, 0.3, 0.3),
  'location': (62.5, 11.0, 38.575),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -6.2772984895975545, 0)},
 {'name': 'Hanger1N22',
  'shape': 'cube',
  'size': (0.15, 0.15, 25.800000000000004),
  'location': (100.0, 11.0, 30.900000000000002),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N22',
  'shape': 'cube',
  'size': (25.294712886293055, 0.3, 0.3),
  'location': (87.5, 11.0, 41.875),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -8.754772989799235, 0)},
 {'name': 'Hanger1N23',
  'shape': 'cube',
  'size': (0.15, 0.15, 30.75),
  'location': (125.0, 11.0, 33.375),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N23',
  'shape': 'cube',
  'size': (25.485338922604107, 0.3, 0.3),
  'location': (112.5, 11.0, 46.275000000000006),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -11.199706023793224, 0)},
 {'name': 'Hanger1N24',
  'shape': 'cube',
  'size': (0.15, 0.15, 36.8),
  'location': (150.0, 11.0, 36.4),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N24',
  'shape': 'cube',
  'size': (25.721634862504366, 0.3, 0.3),
  'location': (137.5, 11.0, 51.775),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -13.604034564773448, 0)},
 {'name': 'Hanger1N25',
  'shape': 'cube',
  'size': (0.15, 0.15, 43.949999999999996),
  'location': (175.0, 11.0, 39.974999999999994),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N25',
  'shape': 'cube',
  'size': (26.002355662516425, 0.3, 0.3),
  'location': (162.5, 11.0, 58.375),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -15.960529492624033, 0)},
 {'name': 'Hanger1N26',
  'shape': 'cube',
  'size': (0.15, 0.15, 52.20000000000002),
  'location': (200.0, 11.0, 44.10000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N26',
  'shape': 'cube',
  'size': (26.32608022475052, 0.3, 0.3),
  'location': (187.5, 11.0, 66.075),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -18.262889942194175, 0)},
 {'name': 'Hanger1N27',
  'shape': 'cube',
  'size': (0.15, 0.15, 61.55000000000001),
  'location': (225.0, 11.0, 48.775000000000006),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N27',
  'shape': 'cube',
  'size': (26.691243882591905, 0.3, 0.3),
  'location': (212.5, 11.0, 74.87500000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -20.505796796146676, 0)},
 {'name': 'Hanger1N28',
  'shape': 'cube',
  'size': (0.15, 0.15, 72.0),
  'location': (250.0, 11.0, 54.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N28',
  'shape': 'cube',
  'size': (27.096171316257944, 0.3, 0.3),
  'location': (237.5, 11.0, 84.775),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, -22.68492755117529, 0)},
 {'name': 'Hanger1N29',
  'shape': 'cube',
  'size': (0.15, 0.15, 65.0),
  'location': (275.0, 11.0, 50.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N29',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (262.5, 11.0, 86.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger1N30',
  'shape': 'cube',
  'size': (0.15, 0.15, 58.0),
  'location': (300.0, 11.0, 47.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N30',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (287.5, 11.0, 79.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger1N31',
  'shape': 'cube',
  'size': (0.15, 0.15, 51.0),
  'location': (325.0, 11.0, 43.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N31',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (312.5, 11.0, 72.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger1N32',
  'shape': 'cube',
  'size': (0.15, 0.15, 44.0),
  'location': (350.0, 11.0, 40.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N32',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (337.5, 11.0, 65.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger1N33',
  'shape': 'cube',
  'size': (0.15, 0.15, 37.0),
  'location': (375.0, 11.0, 36.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N33',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (362.5, 11.0, 58.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger1N34',
  'shape': 'cube',
  'size': (0.15, 0.15, 29.999999999999993),
  'location': (400.0, 11.0, 33.0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N34',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (387.5, 11.0, 51.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208744, 0)},
 {'name': 'Hanger1N35',
  'shape': 'cube',
  'size': (0.15, 0.15, 22.999999999999993),
  'location': (425.0, 11.0, 29.499999999999996),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N35',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (412.5, 11.0, 44.49999999999999),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)},
 {'name': 'Hanger1N36',
  'shape': 'cube',
  'size': (0.15, 0.15, 15.999999999999993),
  'location': (450.0, 11.0, 25.999999999999996),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'Cable1N36',
  'shape': 'cube',
  'size': (25.96150997149434, 0.3, 0.3),
  'location': (437.5, 11.0, 37.49999999999999),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 15.642246457208728, 0)}]

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
