# VERSION: v1.0.1 — 2026-11-12 — crisis/code/ 로 이동 (테스트 내용 변경 없음)
# (이전) v1.0.0 — 2026-11-12 — crisis_lab 분류·성공 판정 단위 테스트
"""python -m unittest crisis/code/test_crisis_lab.py  (네트워크 불필요)"""
import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import crisis_lab as cl  # noqa: E402


class TestFeatures(unittest.TestCase):
    def test_duration(self):
        self.assertEqual(cl.iso_duration_sec("PT1H2M3S"), 3723)
        self.assertEqual(cl.iso_duration_sec("PT59S"), 59)
        self.assertTrue(pd.isna(cl.iso_duration_sec(None)))

    def test_danger_and_title_flags(self):
        t = pd.Series(["엘리베이터에 갇혔을 때 당신이라면 어떻게 하시겠습니까?",
                       "택시 납치 실화… 살아남은 여자의 선택",
                       "칼로리 낮은 다이어트 식단"])
        d = cl.flag_frame(t, cl.DANGER)
        f = cl.flag_frame(t, cl.TITLE_FMT)
        self.assertEqual(d.loc[0, "사고_추락·시설"], 1)
        self.assertEqual(d.loc[1, "범죄_납치·감금"], 1)
        self.assertEqual(d.loc[2].sum(), 0, "칼로리 ≠ 칼 (오탐 방지)")
        self.assertEqual(f.loc[0, "질문형"], 1)
        self.assertEqual(f.loc[1, "생존_결말"], 1)
        self.assertEqual(f.loc[1, "실화·실제"], 1)

    def test_success_rule(self):
        df = pd.DataFrame({
            "video_id": list("abcd"), "views": [100_000, 100_000, 10_000, 500_000],
            "subs": [10_000, 200_000, 100, None], "vpd": [1000, 1000, 100, 9000],
            "views_per_sub": [10.0, 0.5, 10.0, float("nan")], "vpd_per_sub": [0.1, 0.005, 0.1, float("nan")],
        })
        out = cl.label_success(df)
        # a: 조회 10만·구독 1만 → 성공 / b: 큰 채널 → 아님 / c: 조회수 하한 미달 / d: 구독자 숨김 → 성공 판정 불가
        self.assertEqual(out["success"].tolist(), [True, False, False, False])
        self.assertEqual(out.loc[3, "group"], "하루 조회수 상위")


class TestSegments(unittest.TestCase):
    def test_segment_age_gender(self):
        c = pd.DataFrame({"text": ["저는 30대 여자인데 밤길 혼자 다닐 때 너무 무서워요",
                                   "나라면 바로 도망가고 112 신고함",
                                   "현직 소방관입니다. 연기 나면 무조건 낮게 기어서 비상구로"],
                          "likes": [5, 3, 9], "video_id": ["v"] * 3, "group": ["성공 사례"] * 3,
                          "published": pd.to_datetime(["2026-11-01"] * 3, utc=True), "replies": [0] * 3})
        s = cl.segment(c)
        self.assertEqual(s.loc[0, "age"], 30)
        self.assertEqual(s.loc[0, "female"], 1)
        self.assertEqual(s.loc[0, "s_woman_safety"], 1)
        self.assertEqual(s.loc[1, "s_simulator"], 1)
        self.assertEqual(s.loc[1, "a_도망·피하기"], 1)
        self.assertEqual(s.loc[1, "a_신고·도움요청"], 1)
        self.assertEqual(s.loc[2, "s_pro"], 1)
        self.assertEqual(s.loc[2, "a_미리 대비"], 1)


if __name__ == "__main__":
    unittest.main()
