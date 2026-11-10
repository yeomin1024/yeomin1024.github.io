# {ID} {이름} 3D 설계도

<!-- 양식 버전: v1.1 — 2026-11-10 — 3D 항목(MAP) 전용으로 범위 변경. 실제 사진은 PHOTO_SHEET_TEMPLATE, 일러스트는 IMAGE_SHEET_TEMPLATE -->
버전: v1.0 — YYYY-MM-DD — {변경 요약}
상태: 초안 | 검토 | 확정
폴더: `busan-3d/assets/{ID}_{영문명}/`

> 이 양식의 섹션 번호와 제목은 바꾸지 않는다. 모든 숫자에 [확인] / [추정] / [설정] 태그를 붙인다.
> 3D 항목(REGISTRY.md A표: 지도·지형·토큰·액자·패널)에만 쓴다. 지도(MAP01~03)는 `map_template.py`, 나머지는 `blockout_template.py`를 쓴다. 해당 없는 섹션은 "해당 없음"이라고 적는다.

## 1. 개요
| 항목 | 내용 |
|---|---|
| 등장 장면 | (FACTS.md 1장의 일차·시각·장소) |
| 화면에서의 역할 | (이 오브젝트가 전달할 정보 1문장) |
| 등급 | H / M / B |
| 가장 가까운 카메라 거리 | m |
| 화면 점유율 | 최대 % |

## 2. 핵심 특징
- **지켜야 할 것** (이것만 지키면 그 대상으로 보인다, 3~5개)
  1.
- **생략·단순화할 것** (3~5개)
  1.

## 3. 치수표
| 부위 | 가로 X (m) | 깊이 Y (m) | 높이 Z (m) | 근거 태그 | 근거·계산식 |
|---|---|---|---|---|---|
| 전체 | | | | | |
| | | | | | |

사람(1.70 m) 대비 비율: 높이 ___배

## 4. 정면·측면·윗면 도면
### 4-1. 주요 점 좌표 (에셋 원점 = 바닥 중앙, 단위 m)
| 점 이름 | x | y | z | 설명 |
|---|---|---|---|---|

### 4-2. 텍스트 실루엣 (가로세로 비율 유지)
```
정면 (-Y에서 본 모습)

측면 (+X에서 본 모습)

윗면 (+Z에서 본 모습)
```

### 4-3. 치수선
| 치수선 | 시작점 → 끝점 | 길이 (m) |
|---|---|---|

## 5. 부품 목록
`blockout.py`의 `PARTS`와 1:1로 맞춘다. 부모는 위쪽에 쓴다.

| 부품명 | 도형 | 크기 X×Y×Z (m) | 위치 x,y,z (부모 기준) | 회전 x,y,z (°) | 원점(pivot) | 부모 | 재질 | 반복·대칭 | 근거 |
|---|---|---|---|---|---|---|---|---|---|

## 6. 모델링 순서
| 단계 | 작업 | 쓸 모디파이어·설정값 |
|---|---|---|
| 1 | 블록아웃 (`blockout.py` 실행) | – |
| 2 | 1차 형태 | |
| 3 | 디테일 | |
| 4 | 베벨·웨이티드 노멀 | |
| 5 | UV | |

## 7. 폴리곤 예산
| 부품 | 삼각형 목표 | 베벨 폭·세그먼트 | 서브디비전 | 비고 |
|---|---|---|---|---|
| 합계 | | | | 예산: H 2만~8만 / M 5천~2만 / B 5천 이하 |

## 8. 재질표
| 재질 이름 | 색 hex (팔레트 이름) | 거칠기 | 금속성 | 노멀 강도 | 야간 발광 색·강도 | 투명도·IOR |
|---|---|---|---|---|---|---|

텍스처: 해상도, 채널(BaseColor / Normal / ORM / Emission), 트림시트·타일 계획.

## 9. 글자·그래픽
| 위치 | 내용 | 처리 방법 (텍스처 교체 / 가상 디자인) | 글꼴 성격 |
|---|---|---|---|

## 10. 움직임
| 부품 | 움직임 | 원점(회전 중심) 좌표 | 축 | 범위 | 속도·식 |
|---|---|---|---|---|---|

예) 바퀴 회전 각도 = 이동 거리 ÷ (2π × 반지름) × 360°

## 11. 변형
| 종류 | 내용 |
|---|---|
| 낮 / 밤 | |
| 색상 변형 | |
| LOD1 (약 50%) / LOD2 (약 15%) | |

## 12. 참고 이미지 프롬프트 (영어)
`reference_prompt.txt`에도 같은 내용을 저장한다.

```
Create an orthographic model reference sheet for a 3D modeler.
Subject: {object description}
Layout: 4 views in a 2x2 grid — FRONT, RIGHT SIDE, BACK, TOP — all at exactly the same scale, aligned to a faint 1-meter grid, true orthographic projection, no perspective.
Style: stylized miniature diorama, soft bevels, simplified forms, clean dark outlines, flat even lighting, no cast shadows, light gray background.
Include: a 1.7 m human silhouette beside each view for scale; a row of flat color swatches along the bottom using: {hex list}.
Exclude: brand logos, readable signage text, watermarks, scenery backgrounds.
```

## 13. 확실하지 않은 값과 필요한 사진
| 값 | 현재 값 | 태그 | 영향도 (상·중·하) | 확정에 필요한 사진 (대상·각도) |
|---|---|---|---|---|

## 14. 블록아웃 스크립트
- 파일: 지도는 `map_build.py`(`templates/map_template.py` 복사본, `1. 설정` 블록만 채움), 나머지는 `blockout.py`(`templates/blockout_template.py` 복사본, `1. 에셋 정보`·`2. 재질`·`3. 부품` 블록만 채움)
- 실행 후 확인할 로그: `[REPORT] dims_m=... expected_m=... max_err_m=...` (1 cm 넘으면 WARNING), `triangles=... budget=...`

## (종류별 추가 섹션)
해당 없음 (v1의 키트·캐릭터·음식 3D 섹션은 폐기됨)

---

## Changelog
- v1.0 — YYYY-MM-DD — 최초 작성
