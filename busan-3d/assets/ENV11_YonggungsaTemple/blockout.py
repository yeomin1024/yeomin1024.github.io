# VERSION: v1.0 — 2026-11-10 — ENV11 최초 작성
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
ASSET_ID = 'ENV11'
ASSET_NAME = 'YonggungsaTemple'
SPEC_VERSION = "v1.0"
LOD = "L0"  # [설정] 초안 블록아웃
EXPECTED_DIMS_M = (30.0, 60.15, 28.36)  # [설정] 사전 계산한 부품 합성 외곽; 실측 아님
TRI_BUDGET = 40000  # [설정] 완성 목표 상한
TOLERANCE_M = 0.01  # [설정] m
LOG_LEVEL = logging.INFO

# 2. 재질 — 모든 PBR·색 수치 [설정], 전역 팔레트
MATERIALS = {'Concrete': {'base_hex': '#B9B6AE', 'roughness': 0.65, 'metallic': 0.0},
 'Rock': {'base_hex': '#6E6A64', 'roughness': 0.65, 'metallic': 0.0},
 'White': {'base_hex': '#F2EFE6', 'roughness': 0.65, 'metallic': 0.0},
 'Wood': {'base_hex': '#9A7350', 'roughness': 0.65, 'metallic': 0.0},
 'Sky': {'base_hex': '#A9D6F0', 'roughness': 0.65, 'metallic': 0.0},
 'Night': {'base_hex': '#121A33', 'roughness': 0.65, 'metallic': 0.0},
 'BusGreen': {'base_hex': '#4E9A5B', 'roughness': 0.65, 'metallic': 0.0}}

# 3. 부품 — 모든 치수·좌표·각도·분할 [설정], note의 확인값은 예외
PARTS = [{'name': 'Root',
  'shape': 'empty',
  'size': (0.1, 0.1, 0.1),
  'location': (0, 0, 0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님'},
 {'name': 'ApproachStep0',
  'shape': 'cube',
  'size': (3, 0.3, 0.17),
  'location': (0.0, -29.925, 0.085),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep1',
  'shape': 'cube',
  'size': (3, 0.3, 0.34),
  'location': (0.0, -29.625000000000004, 0.17),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep2',
  'shape': 'cube',
  'size': (3, 0.3, 0.51),
  'location': (0.0, -29.325, 0.255),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep3',
  'shape': 'cube',
  'size': (3, 0.3, 0.68),
  'location': (0.0, -29.025000000000002, 0.34),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep4',
  'shape': 'cube',
  'size': (3, 0.3, 0.8500000000000001),
  'location': (0.0, -28.724999999999998, 0.42500000000000004),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep5',
  'shape': 'cube',
  'size': (3, 0.3, 1.02),
  'location': (0.0, -28.425, 0.51),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep6',
  'shape': 'cube',
  'size': (3, 0.3, 1.1900000000000002),
  'location': (0.0, -28.125000000000004, 0.5950000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep7',
  'shape': 'cube',
  'size': (3, 0.3, 1.36),
  'location': (0.0, -27.825, 0.68),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep8',
  'shape': 'cube',
  'size': (3, 0.3, 1.53),
  'location': (0.0, -27.525000000000002, 0.765),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep9',
  'shape': 'cube',
  'size': (3, 0.3, 1.7000000000000002),
  'location': (0.0, -27.224999999999998, 0.8500000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep10',
  'shape': 'cube',
  'size': (3, 0.3, 1.87),
  'location': (0.0, -26.925, 0.935),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep11',
  'shape': 'cube',
  'size': (3, 0.3, 2.04),
  'location': (0.0, -26.625000000000004, 1.02),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep12',
  'shape': 'cube',
  'size': (3, 0.3, 2.21),
  'location': (0.0, -26.325, 1.105),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep13',
  'shape': 'cube',
  'size': (3, 0.3, 2.3800000000000003),
  'location': (0.0, -26.025000000000002, 1.1900000000000002),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep14',
  'shape': 'cube',
  'size': (3, 0.3, 2.5500000000000003),
  'location': (0.0, -25.724999999999998, 1.2750000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep15',
  'shape': 'cube',
  'size': (3, 0.3, 2.72),
  'location': (0.0, -25.425, 1.36),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep16',
  'shape': 'cube',
  'size': (3, 0.3, 2.89),
  'location': (0.0, -25.125000000000004, 1.445),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep17',
  'shape': 'cube',
  'size': (3, 0.3, 3.06),
  'location': (0.0, -24.825, 1.53),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep18',
  'shape': 'cube',
  'size': (3, 0.3, 3.2300000000000004),
  'location': (0.0, -24.525000000000002, 1.6150000000000002),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep19',
  'shape': 'cube',
  'size': (3, 0.3, 3.4000000000000004),
  'location': (0.0, -24.224999999999998, 1.7000000000000002),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep20',
  'shape': 'cube',
  'size': (3, 0.3, 3.5700000000000003),
  'location': (0.0, -23.925, 1.7850000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep21',
  'shape': 'cube',
  'size': (3, 0.3, 3.74),
  'location': (0.0, -23.625, 1.87),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep22',
  'shape': 'cube',
  'size': (3, 0.3, 3.91),
  'location': (0.0, -23.325, 1.955),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep23',
  'shape': 'cube',
  'size': (3, 0.3, 4.08),
  'location': (0.0, -23.025000000000002, 2.04),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep24',
  'shape': 'cube',
  'size': (3, 0.3, 4.25),
  'location': (0.0, -22.725, 2.125),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep25',
  'shape': 'cube',
  'size': (3, 0.3, 4.42),
  'location': (0.0, -22.425, 2.21),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep26',
  'shape': 'cube',
  'size': (3, 0.3, 4.590000000000001),
  'location': (0.0, -22.125, 2.2950000000000004),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep27',
  'shape': 'cube',
  'size': (3, 0.3, 4.760000000000001),
  'location': (0.0, -21.825, 2.3800000000000003),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep28',
  'shape': 'cube',
  'size': (3, 0.3, 4.930000000000001),
  'location': (0.0, -21.525000000000002, 2.4650000000000003),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep29',
  'shape': 'cube',
  'size': (3, 0.3, 5.1000000000000005),
  'location': (0.0, -21.225, 2.5500000000000003),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep30',
  'shape': 'cube',
  'size': (3, 0.3, 5.2700000000000005),
  'location': (0.0, -20.925, 2.6350000000000002),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep31',
  'shape': 'cube',
  'size': (3, 0.3, 5.44),
  'location': (0.0, -20.625000000000004, 2.72),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep32',
  'shape': 'cube',
  'size': (3, 0.3, 5.61),
  'location': (0.0, -20.325, 2.805),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep33',
  'shape': 'cube',
  'size': (3, 0.3, 5.78),
  'location': (0.0, -20.025000000000002, 2.89),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep34',
  'shape': 'cube',
  'size': (3, 0.3, 5.95),
  'location': (0.0, -19.725, 2.975),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep35',
  'shape': 'cube',
  'size': (3, 0.3, 6.12),
  'location': (0.0, -19.425, 3.06),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep36',
  'shape': 'cube',
  'size': (3, 0.3, 6.29),
  'location': (0.0, -19.125000000000004, 3.145),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep37',
  'shape': 'cube',
  'size': (3, 0.3, 6.460000000000001),
  'location': (0.0, -18.825, 3.2300000000000004),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep38',
  'shape': 'cube',
  'size': (3, 0.3, 6.630000000000001),
  'location': (0.0, -18.525000000000002, 3.3150000000000004),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep39',
  'shape': 'cube',
  'size': (3, 0.3, 6.800000000000001),
  'location': (0.0, -18.225, 3.4000000000000004),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep40',
  'shape': 'cube',
  'size': (3, 0.3, 6.970000000000001),
  'location': (0.0, -17.925, 3.4850000000000003),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep41',
  'shape': 'cube',
  'size': (3, 0.3, 7.140000000000001),
  'location': (0.0, -17.625000000000004, 3.5700000000000003),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep42',
  'shape': 'cube',
  'size': (3, 0.3, 7.3100000000000005),
  'location': (0.0, -17.325, 3.6550000000000002),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep43',
  'shape': 'cube',
  'size': (3, 0.3, 7.48),
  'location': (0.0, -17.025000000000002, 3.74),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep44',
  'shape': 'cube',
  'size': (3, 0.3, 7.65),
  'location': (0.0, -16.725, 3.825),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep45',
  'shape': 'cube',
  'size': (3, 0.3, 7.82),
  'location': (0.0, -16.425, 3.91),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep46',
  'shape': 'cube',
  'size': (3, 0.3, 7.99),
  'location': (0.0, -16.125000000000004, 3.995),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep47',
  'shape': 'cube',
  'size': (3, 0.3, 8.16),
  'location': (0.0, -15.825, 4.08),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep48',
  'shape': 'cube',
  'size': (3, 0.3, 8.33),
  'location': (0.0, -15.525000000000002, 4.165),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep49',
  'shape': 'cube',
  'size': (3, 0.3, 8.5),
  'location': (0.0, -15.225000000000001, 4.25),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep50',
  'shape': 'cube',
  'size': (3, 0.3, 8.67),
  'location': (0.0, -14.925, 4.335),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep51',
  'shape': 'cube',
  'size': (3, 0.3, 8.84),
  'location': (0.0, -14.625000000000004, 4.42),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep52',
  'shape': 'cube',
  'size': (3, 0.3, 9.01),
  'location': (0.0, -14.325, 4.505),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep53',
  'shape': 'cube',
  'size': (3, 0.3, 9.180000000000001),
  'location': (0.0, -14.025000000000002, 4.590000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep54',
  'shape': 'cube',
  'size': (3, 0.3, 9.350000000000001),
  'location': (0.0, -13.725000000000001, 4.675000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep55',
  'shape': 'cube',
  'size': (3, 0.3, 9.520000000000001),
  'location': (0.0, -13.425, 4.760000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep56',
  'shape': 'cube',
  'size': (3, 0.3, 9.690000000000001),
  'location': (0.0, -13.125, 4.845000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep57',
  'shape': 'cube',
  'size': (3, 0.3, 9.860000000000001),
  'location': (0.0, -12.825000000000003, 4.930000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep58',
  'shape': 'cube',
  'size': (3, 0.3, 10.030000000000001),
  'location': (0.0, -12.525000000000002, 5.015000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep59',
  'shape': 'cube',
  'size': (3, 0.3, 10.200000000000001),
  'location': (0.0, -12.225000000000001, 5.1000000000000005),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep60',
  'shape': 'cube',
  'size': (3, 0.3, 10.370000000000001),
  'location': (0.0, -11.925, 5.1850000000000005),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep61',
  'shape': 'cube',
  'size': (3, 0.3, 10.540000000000001),
  'location': (0.0, -11.625, 5.2700000000000005),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep62',
  'shape': 'cube',
  'size': (3, 0.3, 10.71),
  'location': (0.0, -11.325000000000003, 5.355),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep63',
  'shape': 'cube',
  'size': (3, 0.3, 10.88),
  'location': (0.0, -11.025000000000002, 5.44),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep64',
  'shape': 'cube',
  'size': (3, 0.3, 11.05),
  'location': (0.0, -10.725000000000001, 5.525),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep65',
  'shape': 'cube',
  'size': (3, 0.3, 11.22),
  'location': (0.0, -10.425, 5.61),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep66',
  'shape': 'cube',
  'size': (3, 0.3, 11.39),
  'location': (0.0, -10.125, 5.695),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep67',
  'shape': 'cube',
  'size': (3, 0.3, 11.56),
  'location': (0.0, -9.825000000000003, 5.78),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep68',
  'shape': 'cube',
  'size': (3, 0.3, 11.73),
  'location': (0.0, -9.525000000000002, 5.865),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep69',
  'shape': 'cube',
  'size': (3, 0.3, 11.9),
  'location': (0.0, -9.225000000000001, 5.95),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep70',
  'shape': 'cube',
  'size': (3, 0.3, 12.07),
  'location': (0.0, -8.925, 6.035),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep71',
  'shape': 'cube',
  'size': (3, 0.3, 12.24),
  'location': (0.0, -8.625, 6.12),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep72',
  'shape': 'cube',
  'size': (3, 0.3, 12.41),
  'location': (0.0, -8.325000000000003, 6.205),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep73',
  'shape': 'cube',
  'size': (3, 0.3, 12.58),
  'location': (0.0, -8.025000000000002, 6.29),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep74',
  'shape': 'cube',
  'size': (3, 0.3, 12.750000000000002),
  'location': (0.0, -7.725000000000001, 6.375000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep75',
  'shape': 'cube',
  'size': (3, 0.3, 12.920000000000002),
  'location': (0.0, -7.425000000000001, 6.460000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep76',
  'shape': 'cube',
  'size': (3, 0.3, 13.090000000000002),
  'location': (0.0, -7.125, 6.545000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep77',
  'shape': 'cube',
  'size': (3, 0.3, 13.260000000000002),
  'location': (0.0, -6.825000000000003, 6.630000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep78',
  'shape': 'cube',
  'size': (3, 0.3, 13.430000000000001),
  'location': (0.0, -6.525000000000002, 6.715000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep79',
  'shape': 'cube',
  'size': (3, 0.3, 13.600000000000001),
  'location': (0.0, -6.225000000000001, 6.800000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep80',
  'shape': 'cube',
  'size': (3, 0.3, 13.770000000000001),
  'location': (0.0, -5.925000000000001, 6.885000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep81',
  'shape': 'cube',
  'size': (3, 0.3, 13.940000000000001),
  'location': (0.0, -5.625, 6.970000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep82',
  'shape': 'cube',
  'size': (3, 0.3, 14.110000000000001),
  'location': (0.0, -5.325000000000003, 7.055000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep83',
  'shape': 'cube',
  'size': (3, 0.3, 14.280000000000001),
  'location': (0.0, -5.025000000000002, 7.140000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep84',
  'shape': 'cube',
  'size': (3, 0.3, 14.450000000000001),
  'location': (0.0, -4.725000000000001, 7.2250000000000005),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep85',
  'shape': 'cube',
  'size': (3, 0.3, 14.620000000000001),
  'location': (0.0, -4.425000000000001, 7.3100000000000005),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep86',
  'shape': 'cube',
  'size': (3, 0.3, 14.790000000000001),
  'location': (0.0, -4.125, 7.3950000000000005),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep87',
  'shape': 'cube',
  'size': (3, 0.3, 14.96),
  'location': (0.0, -3.825000000000003, 7.48),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep88',
  'shape': 'cube',
  'size': (3, 0.3, 15.13),
  'location': (0.0, -3.525000000000002, 7.565),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep89',
  'shape': 'cube',
  'size': (3, 0.3, 15.3),
  'location': (0.0, -3.2250000000000014, 7.65),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep90',
  'shape': 'cube',
  'size': (3, 0.3, 15.47),
  'location': (0.0, -2.9250000000000007, 7.735),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep91',
  'shape': 'cube',
  'size': (3, 0.3, 15.64),
  'location': (0.0, -2.625, 7.82),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep92',
  'shape': 'cube',
  'size': (3, 0.3, 15.81),
  'location': (0.0, -2.325000000000003, 7.905),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep93',
  'shape': 'cube',
  'size': (3, 0.3, 15.98),
  'location': (0.0, -2.025000000000002, 7.99),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep94',
  'shape': 'cube',
  'size': (3, 0.3, 16.150000000000002),
  'location': (0.0, -1.7250000000000014, 8.075000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep95',
  'shape': 'cube',
  'size': (3, 0.3, 16.32),
  'location': (0.0, -1.4250000000000007, 8.16),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep96',
  'shape': 'cube',
  'size': (3, 0.3, 16.490000000000002),
  'location': (0.0, -1.1250000000000036, 8.245000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep97',
  'shape': 'cube',
  'size': (3, 0.3, 16.66),
  'location': (0.0, -0.8250000000000028, 8.33),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep98',
  'shape': 'cube',
  'size': (3, 0.3, 16.830000000000002),
  'location': (0.0, -0.5250000000000021, 8.415000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep99',
  'shape': 'cube',
  'size': (3, 0.3, 17.0),
  'location': (0.0, -0.22500000000000142, 8.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep100',
  'shape': 'cube',
  'size': (3, 0.3, 17.17),
  'location': (0.0, 0.07499999999999929, 8.585),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep101',
  'shape': 'cube',
  'size': (3, 0.3, 17.34),
  'location': (0.0, 0.37499999999999645, 8.67),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep102',
  'shape': 'cube',
  'size': (3, 0.3, 17.51),
  'location': (0.0, 0.6749999999999972, 8.755),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep103',
  'shape': 'cube',
  'size': (3, 0.3, 17.68),
  'location': (0.0, 0.9749999999999979, 8.84),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep104',
  'shape': 'cube',
  'size': (3, 0.3, 17.85),
  'location': (0.0, 1.2749999999999986, 8.925),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep105',
  'shape': 'cube',
  'size': (3, 0.3, 18.02),
  'location': (0.0, 1.5749999999999993, 9.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep106',
  'shape': 'cube',
  'size': (3, 0.3, 18.19),
  'location': (0.0, 1.8749999999999964, 9.095),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'ApproachStep107',
  'shape': 'cube',
  'size': (3, 0.3, 18.360000000000003),
  'location': (0.0, 2.1750000000000007, 9.180000000000001),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'TemplePlatform',
  'shape': 'cube',
  'size': (30, 28, 0.5),
  'location': (0.0, 16.075, 18.11),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Rock',
  'bevel': {'width': 0.2, 'segments': 2}},
 {'name': 'HallWall',
  'shape': 'cube',
  'size': (10, 7, 4),
  'location': (0.0, 16.075, 20.36),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'bevel': {'width': 0.06, 'segments': 2}},
 {'name': 'HallRoof',
  'shape': 'cube',
  'size': (10.12, 7.12, 0.15),
  'location': (0.0, 16.075, 22.435),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'bevel': {'width': 0.03, 'segments': 2}},
 {'name': 'HallDoor',
  'shape': 'cube',
  'size': (0.9, 0.04, 2.1),
  'location': (-2.5, 12.555, 19.41),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Wood',
  'bevel': {'width': 0.01, 'segments': 2}},
 {'name': 'HallWindow',
  'shape': 'cube',
  'size': (1.0, 0.05, 0.85),
  'location': (2.2, 12.544999999999998, 20.009999999999998),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Sky',
  'bevel': {'width': 0.015, 'segments': 2}},
 {'name': 'HallEaves',
  'shape': 'cube',
  'size': (13, 9, 0.8),
  'location': (0.0, 16.075, 22.76),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Night',
  'bevel': {'width': 0.2, 'segments': 2}},
 {'name': 'HallRidge',
  'shape': 'cube',
  'size': (8, 1, 0.7),
  'location': (0.0, 16.075, 23.5),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'BusGreen',
  'bevel': {'width': 0.1, 'segments': 2}},
 {'name': 'BodhisattvaRobe',
  'shape': 'cone',
  'size': (3.5, 3.5, 8),
  'location': (10.0, 15.075, 22.36),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 16,
  'radius_top_ratio': 0.4},
 {'name': 'BodhisattvaHead',
  'shape': 'sphere',
  'size': (2, 2, 2),
  'location': (10.0, 15.075, 27.36),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 16,
  'smooth': True},
 {'name': 'ZodiacPlinth0',
  'shape': 'cube',
  'size': (1, 1, 0.3),
  'location': (-8.0, -26.925, 0.15),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'GenericAnimal0',
  'shape': 'sphere',
  'size': (1, 1, 1.6),
  'location': (-8.0, -26.925, 1.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 12,
  'smooth': True},
 {'name': 'ZodiacPlinth1',
  'shape': 'cube',
  'size': (1, 1, 0.3),
  'location': (-8.0, -22.925, 0.15),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'GenericAnimal1',
  'shape': 'sphere',
  'size': (1, 1, 1.6),
  'location': (-8.0, -22.925, 1.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 12,
  'smooth': True},
 {'name': 'ZodiacPlinth2',
  'shape': 'cube',
  'size': (1, 1, 0.3),
  'location': (-8.0, -18.925, 0.15),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'GenericAnimal2',
  'shape': 'sphere',
  'size': (1, 1, 1.6),
  'location': (-8.0, -18.925, 1.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 12,
  'smooth': True},
 {'name': 'ZodiacPlinth3',
  'shape': 'cube',
  'size': (1, 1, 0.3),
  'location': (-8.0, -14.925, 0.15),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'GenericAnimal3',
  'shape': 'sphere',
  'size': (1, 1, 1.6),
  'location': (-8.0, -14.925, 1.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 12,
  'smooth': True},
 {'name': 'ZodiacPlinth4',
  'shape': 'cube',
  'size': (1, 1, 0.3),
  'location': (-8.0, -10.925, 0.15),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'GenericAnimal4',
  'shape': 'sphere',
  'size': (1, 1, 1.6),
  'location': (-8.0, -10.925, 1.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 12,
  'smooth': True},
 {'name': 'ZodiacPlinth5',
  'shape': 'cube',
  'size': (1, 1, 0.3),
  'location': (-8.0, -6.925000000000001, 0.15),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'GenericAnimal5',
  'shape': 'sphere',
  'size': (1, 1, 1.6),
  'location': (-8.0, -6.925000000000001, 1.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 12,
  'smooth': True},
 {'name': 'ZodiacPlinth6',
  'shape': 'cube',
  'size': (1, 1, 0.3),
  'location': (8.0, -26.925, 0.15),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'GenericAnimal6',
  'shape': 'sphere',
  'size': (1, 1, 1.6),
  'location': (8.0, -26.925, 1.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 12,
  'smooth': True},
 {'name': 'ZodiacPlinth7',
  'shape': 'cube',
  'size': (1, 1, 0.3),
  'location': (8.0, -22.925, 0.15),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'GenericAnimal7',
  'shape': 'sphere',
  'size': (1, 1, 1.6),
  'location': (8.0, -22.925, 1.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 12,
  'smooth': True},
 {'name': 'ZodiacPlinth8',
  'shape': 'cube',
  'size': (1, 1, 0.3),
  'location': (8.0, -18.925, 0.15),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'GenericAnimal8',
  'shape': 'sphere',
  'size': (1, 1, 1.6),
  'location': (8.0, -18.925, 1.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 12,
  'smooth': True},
 {'name': 'ZodiacPlinth9',
  'shape': 'cube',
  'size': (1, 1, 0.3),
  'location': (8.0, -14.925, 0.15),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'GenericAnimal9',
  'shape': 'sphere',
  'size': (1, 1, 1.6),
  'location': (8.0, -14.925, 1.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 12,
  'smooth': True},
 {'name': 'ZodiacPlinth10',
  'shape': 'cube',
  'size': (1, 1, 0.3),
  'location': (8.0, -10.925, 0.15),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'GenericAnimal10',
  'shape': 'sphere',
  'size': (1, 1, 1.6),
  'location': (8.0, -10.925, 1.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
  'segments': 12,
  'smooth': True},
 {'name': 'ZodiacPlinth11',
  'shape': 'cube',
  'size': (1, 1, 0.3),
  'location': (8.0, -6.925000000000001, 0.15),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete'},
 {'name': 'GenericAnimal11',
  'shape': 'sphere',
  'size': (1, 1, 1.6),
  'location': (8.0, -6.925000000000001, 1.1),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Concrete',
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
