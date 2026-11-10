# VERSION: v1.0 — 2026-11-10 — FOOD07 최초 작성
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
ASSET_ID = 'FOOD07'
ASSET_NAME = 'BangeoSashimi'
SPEC_VERSION = "v1.0"
LOD = "L0"  # [설정] 초안 블록아웃
EXPECTED_DIMS_M = (0.3819, 0.2902822897576198, 0.034)  # [설정] 사전 계산한 부품 합성 외곽; 실측 아님
TRI_BUDGET = 40000  # [설정] 완성 목표 상한
TOLERANCE_M = 0.01  # [설정] m
LOG_LEVEL = logging.INFO

# 2. 재질 — 모든 PBR·색 수치 [설정], 전역 팔레트
MATERIALS = {'White': {'base_hex': '#F2EFE6', 'roughness': 0.65, 'metallic': 0.0},
 'Coral': {'base_hex': '#F4A6A0', 'roughness': 0.65, 'metallic': 0.0},
 'Mint': {'base_hex': '#8FC9B9', 'roughness': 0.65, 'metallic': 0.0},
 'Wood': {'base_hex': '#9A7350', 'roughness': 0.65, 'metallic': 0.0},
 'BusRed': {'base_hex': '#C8423B', 'roughness': 0.65, 'metallic': 0.0},
 'BusGreen': {'base_hex': '#4E9A5B', 'roughness': 0.65, 'metallic': 0.0}}

# 3. 부품 — 모든 치수·좌표·각도·분할 [설정], note의 확인값은 예외
PARTS = [{'name': 'Root',
  'shape': 'empty',
  'size': (0.1, 0.1, 0.1),
  'location': (0, 0, 0),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님'},
 {'name': 'BowlBase',
  'shape': 'cylinder',
  'size': (0.28, 0.28, 0.008),
  'location': (0.025949999999999987, 1.3877787807814457e-17, 0.004),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'segments': 24,
  'smooth': True},
 {'name': 'BowlRim0',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.16695, 1.3877787807814457e-17, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 90.0)},
 {'name': 'BowlRim1',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.16214554150675858, 0.03649348535945544, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 105.0)},
 {'name': 'BowlRim2',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.14805958193360583, 0.0705, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 120.0)},
 {'name': 'BowlRim3',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.12565205614730318, 0.0997020561473032, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 135.0)},
 {'name': 'BowlRim4',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.09645, 0.12210958193360584, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 150.0)},
 {'name': 'BowlRim5',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.06244348535945541, 0.1361955415067586, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 165.0)},
 {'name': 'BowlRim6',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.025949999999999994, 0.14100000000000001, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 180.0)},
 {'name': 'BowlRim7',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (-0.010543485359455415, 0.1361955415067586, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 195.0)},
 {'name': 'BowlRim8',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (-0.04454999999999998, 0.12210958193360585, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 210.0)},
 {'name': 'BowlRim9',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (-0.0737520561473032, 0.09970205614730321, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 225.0)},
 {'name': 'BowlRim10',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (-0.09615958193360585, 0.0705, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 240.0)},
 {'name': 'BowlRim11',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (-0.11024554150675862, 0.03649348535945547, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 255.0)},
 {'name': 'BowlRim12',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (-0.11505, 3.1145307675792136e-17, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 270.0)},
 {'name': 'BowlRim13',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (-0.11024554150675862, -0.036493485359455416, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 285.0)},
 {'name': 'BowlRim14',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (-0.09615958193360588, -0.07049999999999994, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 300.0)},
 {'name': 'BowlRim15',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (-0.07375205614730326, -0.09970205614730313, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 315.0)},
 {'name': 'BowlRim16',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (-0.044550000000000076, -0.12210958193360578, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 330.0)},
 {'name': 'BowlRim17',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (-0.010543485359455415, -0.1361955415067586, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 345.0)},
 {'name': 'BowlRim18',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.025949999999999963, -0.14099999999999996, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 360.0)},
 {'name': 'BowlRim19',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.06244348535945535, -0.1361955415067586, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 375.0)},
 {'name': 'BowlRim20',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.09645, -0.12210958193360581, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 390.0)},
 {'name': 'BowlRim21',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.12565205614730315, -0.0997020561473032, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 405.0)},
 {'name': 'BowlRim22',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.1480595819336058, -0.07050000000000005, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 420.0)},
 {'name': 'BowlRim23',
  'shape': 'cube',
  'size': (0.039269908169872414, 0.008, 0.018),
  'location': (0.16214554150675858, -0.03649348535945553, 0.009),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 434.99999999999994)},
 {'name': 'Broth',
  'shape': 'cylinder',
  'size': (0.278, 0.278, 0.003),
  'location': (0.025949999999999987, 1.3877787807814457e-17, 0.014),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'segments': 32,
  'smooth': True},
 {'name': 'Garnish0',
  'shape': 'sphere',
  'size': (0.035, 0.025, 0.012),
  'location': (0.10844999999999999, 1.3877787807814457e-17, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Coral',
  'segments': 12,
  'smooth': True},
 {'name': 'Garnish1',
  'shape': 'sphere',
  'size': (0.035, 0.025, 0.012),
  'location': (0.08428630944789016, 0.05303300858899108, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Coral',
  'segments': 12,
  'smooth': True},
 {'name': 'Garnish2',
  'shape': 'sphere',
  'size': (0.035, 0.025, 0.012),
  'location': (0.02594999999999999, 0.07500000000000002, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Coral',
  'segments': 12,
  'smooth': True},
 {'name': 'Garnish3',
  'shape': 'sphere',
  'size': (0.035, 0.025, 0.012),
  'location': (-0.03238630944789017, 0.053033008588991085, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Coral',
  'segments': 12,
  'smooth': True},
 {'name': 'Garnish4',
  'shape': 'sphere',
  'size': (0.035, 0.025, 0.012),
  'location': (-0.05655000000000002, 2.3062638801419607e-17, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Coral',
  'segments': 12,
  'smooth': True},
 {'name': 'Garnish5',
  'shape': 'sphere',
  'size': (0.035, 0.025, 0.012),
  'location': (-0.0323863094478902, -0.05303300858899105, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Coral',
  'segments': 12,
  'smooth': True},
 {'name': 'Garnish6',
  'shape': 'sphere',
  'size': (0.035, 0.025, 0.012),
  'location': (0.025949999999999973, -0.075, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Coral',
  'segments': 12,
  'smooth': True},
 {'name': 'Garnish7',
  'shape': 'sphere',
  'size': (0.035, 0.025, 0.012),
  'location': (0.08428630944789015, -0.05303300858899106, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Coral',
  'segments': 12,
  'smooth': True},
 {'name': 'Green0',
  'shape': 'cube',
  'size': (0.008, 0.05, 0.003),
  'location': (-0.03405000000000001, 0.030000000000000013, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Mint',
  'rotation_deg': (0, 0, 0)},
 {'name': 'Green1',
  'shape': 'cube',
  'size': (0.008, 0.05, 0.003),
  'location': (-0.007050000000000015, 0.030000000000000013, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Mint',
  'rotation_deg': (0, 0, 15)},
 {'name': 'Green2',
  'shape': 'cube',
  'size': (0.008, 0.05, 0.003),
  'location': (0.01994999999999998, 0.030000000000000013, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Mint',
  'rotation_deg': (0, 0, 30)},
 {'name': 'Green3',
  'shape': 'cube',
  'size': (0.008, 0.05, 0.003),
  'location': (0.04694999999999998, 0.030000000000000013, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Mint',
  'rotation_deg': (0, 0, 45)},
 {'name': 'Green4',
  'shape': 'cube',
  'size': (0.008, 0.05, 0.003),
  'location': (0.07394999999999997, 0.030000000000000013, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Mint',
  'rotation_deg': (0, 0, 60)},
 {'name': 'SteamSocket',
  'shape': 'empty',
  'size': (0.02, 0.02, 0.02),
  'location': (0.025949999999999987, 1.3877787807814457e-17, 0.09),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root'},
 {'name': 'Chopstick0',
  'shape': 'cube',
  'size': (0.006, 0.23, 0.006),
  'location': (0.17595, 1.3877787807814457e-17, 0.02),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Wood',
  'bevel': {'width': 0.001, 'segments': 2}},
 {'name': 'Chopstick1',
  'shape': 'cube',
  'size': (0.006, 0.23, 0.006),
  'location': (0.18795, 1.3877787807814457e-17, 0.02),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Wood',
  'bevel': {'width': 0.001, 'segments': 2}},
 {'name': 'Lettuce0',
  'shape': 'sphere',
  'size': (0.045, 0.04, 0.008),
  'location': (-0.06405000000000001, -0.08999999999999998, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Mint',
  'segments': 12,
  'smooth': True},
 {'name': 'Lettuce1',
  'shape': 'sphere',
  'size': (0.045, 0.04, 0.008),
  'location': (-0.0040500000000000085, -0.08999999999999998, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Mint',
  'segments': 12,
  'smooth': True},
 {'name': 'Lettuce2',
  'shape': 'sphere',
  'size': (0.045, 0.04, 0.008),
  'location': (0.05594999999999999, -0.08999999999999998, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Mint',
  'segments': 12,
  'smooth': True},
 {'name': 'Lettuce3',
  'shape': 'sphere',
  'size': (0.045, 0.04, 0.008),
  'location': (0.11594999999999998, -0.08999999999999998, 0.028),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'Mint',
  'segments': 12,
  'smooth': True},
 {'name': 'SauceDishBase',
  'shape': 'cylinder',
  'size': (0.0574, 0.0574, 0.01),
  'location': (-0.15405000000000002, -0.03999999999999999, 0.005),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'segments': 24,
  'smooth': True},
 {'name': 'SauceDishRim0',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.12115000000000002, -0.03999999999999999, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 90.0)},
 {'name': 'SauceDishRim1',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.12227104031508966, -0.03148485341612706, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 105.0)},
 {'name': 'SauceDishRim2',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.12555776421549197, -0.02354999999999999, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 120.0)},
 {'name': 'SauceDishRim3',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.1307861868989626, -0.016736186898962578, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 135.0)},
 {'name': 'SauceDishRim4',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.1376, -0.011507764215491958, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 150.0)},
 {'name': 'SauceDishRim5',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.1455348534161271, -0.00822104031508964, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 165.0)},
 {'name': 'SauceDishRim6',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.15405000000000002, -0.007099999999999988, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 180.0)},
 {'name': 'SauceDishRim7',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.16256514658387294, -0.00822104031508964, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 195.0)},
 {'name': 'SauceDishRim8',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.17049999999999998, -0.011507764215491954, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 210.0)},
 {'name': 'SauceDishRim9',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.17731381310103744, -0.01673618689896257, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 225.0)},
 {'name': 'SauceDishRim10',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.18254223578450807, -0.02354999999999999, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 240.0)},
 {'name': 'SauceDishRim11',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.18582895968491037, -0.03148485341612704, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 255.0)},
 {'name': 'SauceDishRim12',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.18695, -0.03999999999999998, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 270.0)},
 {'name': 'SauceDishRim13',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.18582895968491037, -0.04851514658387292, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 285.0)},
 {'name': 'SauceDishRim14',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.18254223578450807, -0.05644999999999997, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 300.0)},
 {'name': 'SauceDishRim15',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.17731381310103744, -0.06326381310103739, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 315.0)},
 {'name': 'SauceDishRim16',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.17050000000000004, -0.06849223578450801, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 330.0)},
 {'name': 'SauceDishRim17',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.16256514658387294, -0.07177895968491034, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 345.0)},
 {'name': 'SauceDishRim18',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.15405000000000002, -0.07289999999999998, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 360.0)},
 {'name': 'SauceDishRim19',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.1455348534161271, -0.07177895968491034, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 375.0)},
 {'name': 'SauceDishRim20',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.1376, -0.06849223578450801, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 390.0)},
 {'name': 'SauceDishRim21',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.1307861868989626, -0.0632638131010374, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 405.0)},
 {'name': 'SauceDishRim22',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.12555776421549197, -0.05645, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 420.0)},
 {'name': 'SauceDishRim23',
  'shape': 'cube',
  'size': (0.00916297857297023, 0.008, 0.02),
  'location': (-0.12227104031508966, -0.048515146583872945, 0.01),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'rotation_deg': (0, 0, 434.99999999999994)},
 {'name': 'Sauce',
  'shape': 'cylinder',
  'size': (0.06, 0.06, 0.004),
  'location': (-0.15405000000000002, -0.03999999999999999, 0.018),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'BusRed',
  'segments': 16,
  'smooth': True},
 {'name': 'Garlic0',
  'shape': 'sphere',
  'size': (0.009, 0.012, 0.003),
  'location': (0.15594999999999998, -0.044999999999999984, 0.015),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'segments': 8,
  'smooth': True},
 {'name': 'Chili0',
  'shape': 'sphere',
  'size': (0.008, 0.015, 0.004),
  'location': (0.17595, -0.044999999999999984, 0.015),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'BusGreen',
  'segments': 8,
  'smooth': True},
 {'name': 'Garlic1',
  'shape': 'sphere',
  'size': (0.009, 0.012, 0.003),
  'location': (0.15594999999999998, -0.026999999999999986, 0.015),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'segments': 8,
  'smooth': True},
 {'name': 'Chili1',
  'shape': 'sphere',
  'size': (0.008, 0.015, 0.004),
  'location': (0.17595, -0.026999999999999986, 0.015),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'BusGreen',
  'segments': 8,
  'smooth': True},
 {'name': 'Garlic2',
  'shape': 'sphere',
  'size': (0.009, 0.012, 0.003),
  'location': (0.15594999999999998, -0.008999999999999987, 0.015),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'White',
  'segments': 8,
  'smooth': True},
 {'name': 'Chili2',
  'shape': 'sphere',
  'size': (0.008, 0.015, 0.004),
  'location': (0.17595, -0.008999999999999987, 0.015),
  'pivot': 'center',
  'note': '[설정] 제작용 형태·치수; 실측 아님',
  'parent': 'Root',
  'material': 'BusGreen',
  'segments': 8,
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
