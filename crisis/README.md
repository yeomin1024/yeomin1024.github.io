# crisis — "범죄·사고 위기 상황, 당신이라면?" 채널 분석

이 채널 자료만 모아 둔 폴더입니다 (주식·심리 채널 자료와 섞이지 않음).
연구·기획용입니다. 영상 속 안전 수칙은 공식 지침(소방청·경찰청·국민재난안전포털)으로 꼭 다시 확인하세요.

## 폴더 구성

```
crisis/
├── README.md          ← 지금 이 안내
├── titles.md          ← ★ 제목·썸네일 문구 4쌍과 근거 (사람이 쓴 기획안)
├── CHANGELOG.md       ← 코드 버전별 변경·결과 비교
├── code/
│   ├── crisis_lab.py        분석 코드 (수집 → 성공 사례 → 댓글 → 페르소나 → 추세)
│   └── test_crisis_lab.py   단위 테스트
├── result/            ← 코드가 만드는 결과 (다시 돌리면 덮어씀)
│   ├── analysis.md          성공 사례, 위험 유형·장르·쇼츠/롱폼·제목 형식별 성과, 최근 28일 추세
│   ├── personas.md          최종 페르소나 4명 + 세부 묶음 9개 (대표 댓글, 작성자 이름 없음)
│   ├── personas.json · videos.csv · title_lift.csv
│   └── run_log.txt          마지막 실행 로그
└── cache/             ← YouTube API 응답 저장 (git 제외)
```

## 실행
```bash
python crisis/code/crisis_lab.py run       # YouTube API로 수집 + 분석 (cache/ 에 있으면 호출 안 함)
python crisis/code/crisis_lab.py analyze   # 캐시만으로 분석 (할당량 0)
LOG_LEVEL=DEBUG python crisis/code/crisis_lab.py analyze
python -m unittest crisis/code/test_crisis_lab.py
```
- `YOUTUBE_API_KEY` 환경 변수 필요. 첫 실행 약 2,500 단위(검색 1회 = 100).
- `cache/`는 git에 올리지 않음 → 새 환경에서는 `run`이 다시 받음.
- 기준일 `AS_OF`가 고정이라 재실행해도 같은 숫자가 나옴. 새 데이터로 보려면 `AS_OF`를 바꾸고 `cache/`를 지운 뒤 `run`.

## 성공 사례 기준
조회수 ≥ 30,000 그리고 조회수 ÷ max(구독자, 1,000) ≥ 2 (최근 180일, 3일 미만 제외).
성공 비율은 채널 가중(한 채널 k편이면 각 1/k). 기준을 1·5·10배로 바꾼 개수는 `result/run_log.txt`의 `sensitivity` 줄.
