# crisis — "범죄·사고 위기 상황, 당신이라면?" 채널 분석

연구·기획용입니다. 영상 속 안전 수칙은 공식 지침(소방청·경찰청·국민재난안전포털)으로 꼭 다시 확인하세요.

## 결과
- `result/titles.md` — **제목·썸네일 문구 4쌍**과 근거
- `result/personas.md` — 최종 페르소나 4명 + 세부 묶음 9개 (대표 댓글 포함, 작성자 이름 없음)
- `result/analysis.md` — 성공 사례, 위험 유형·장르·쇼츠/롱폼·제목 형식별 성과, 최근 28일 추세
- `result/videos.csv`, `result/title_lift.csv`, `result/personas.json`, `result/run_log.txt`

## 실행
```bash
python crisis/crisis_lab.py run       # YouTube API로 수집 + 분석 (cache/ 에 있으면 호출 안 함)
python crisis/crisis_lab.py analyze   # 캐시만으로 분석 (할당량 0)
LOG_LEVEL=DEBUG python crisis/crisis_lab.py analyze
python -m unittest crisis/test_crisis_lab.py
```
- `YOUTUBE_API_KEY` 환경 변수 필요. 첫 실행 약 2,500 단위(검색 1회 = 100).
- `cache/`는 git에 올리지 않음 → 새 환경에서는 `run`이 다시 받음.
- 기준일 `AS_OF`가 고정이라 재실행해도 같은 숫자가 나옴. 새 데이터로 보려면 `AS_OF`를 바꾸고 `cache/`를 지운 뒤 `run`.

## 성공 사례 기준
조회수 ≥ 30,000 그리고 조회수 ÷ max(구독자, 1,000) ≥ 2 (최근 180일, 3일 미만 제외).
성공 비율은 채널 가중(한 채널 k편이면 각 1/k). 기준을 1·5·10배로 바꾼 개수는 `run_log.txt`의 `sensitivity` 줄.
