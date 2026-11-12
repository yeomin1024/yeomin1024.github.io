# VERSION: v1.2.0 — 2026-11-12 — 묶음 9개 → 제목용 최종 페르소나 4명 합치기 (merge_personas)
# (이전) v1.1.0 — 2026-11-12 — 주제 필터·채널 쏠림 보정·장르 태그·댓글 사전 확장·선택형 검색어 4개
# (이전) v1.0.0 — 2026-11-12 — 위기 상황 채널 1차 분석 파이프라인 신규 작성
"""
crisis_lab.py — "범죄·사고 위기 상황, 당신이라면?" 채널 기획용 유튜브 분석기

흐름 (심리·주식 채널 분석과 같은 순서)
  1. LOAD     : YouTube Data API 검색 → 영상·채널 통계 (응답은 cache/ 에 저장, 재실행 시 할당량 0)
  2. VALIDATE : 중복 영상, 빠진 통계, 숨긴 구독자 수, 너무 최근 영상 점검
  3. FEATURE  : 위험 유형(범죄/사고/재난…), 제목 형식(질문형·생존/사망 대비·실화…) 표시
  4. SIGNAL   : 성공 사례 판정 (조회수 ≥ MIN_VIEWS, 조회수/구독자 ≥ MIN_VIEWS_PER_SUB)
  5. COMMENT  : 성공 사례·하루 조회수 상위 영상의 댓글 수집
  6. SEGMENT  : 댓글을 시청자 묶음(규칙 기반 키워드)으로 분류
  7. PERSONA  : 묶음별 나이·성별 단서·관심 위험·"나라면" 행동·원하는 것·대표 댓글
  8. TREND    : 최근 28일 vs 그 이전 비교 (날짜 경계 로그로 남김)
  9. EXPORT   : result/*.md, result/*.csv

규칙 기반(키워드 사전) 분류를 쓴 이유: 어떤 댓글이 왜 그 묶음에 들어갔는지
사전만 보면 바로 추적할 수 있음. 무작위 요소 없음(SEED 는 기록용).

주의: 연구·기획용 도구. 영상 속 안전 조언은 반드시 소방청·경찰청 등 공식 지침으로 따로 확인할 것.

실행:  python crisis/crisis_lab.py run            # 수집+분석 (캐시 있으면 API 호출 안 함)
       python crisis/crisis_lab.py analyze        # 캐시만으로 분석
       LOG_LEVEL=DEBUG python crisis/crisis_lab.py analyze
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import requests

VERSION = "v1.2.0"
SEED = 0  # 무작위 요소 없음 — 재현성 기록용

# ─────────────────────────── 설정 ───────────────────────────
ROOT = Path(__file__).resolve().parent
CACHE_DIR = ROOT / "cache"
RESULT_DIR = ROOT / "result"
API = "https://www.googleapis.com/youtube/v3"

# 분석 기준일을 고정해야 재실행해도 "며칠 지났나"가 바뀌지 않음 (재현성)
AS_OF = datetime(2026, 11, 12, tzinfo=timezone.utc)
WINDOW_DAYS = 180          # 이보다 오래된 영상은 제외 (심리 채널 분석과 같은 기준)
MIN_AGE_DAYS = 3           # 3일 미만 영상은 하루 조회수가 불안정 → 제외
RECENT_DAYS = 28           # 추세: 최근 28일 vs 그 이전
SHORTS_MAX_SEC = 180       # 2024-10 이후 쇼츠 최대 3분

MIN_VIEWS = 30_000         # 성공 사례: 절대 조회수 하한
MIN_VIEWS_PER_SUB = 2.0    # 성공 사례: 구독자 수의 2배 이상 조회
SUB_FLOOR = 1_000          # 구독자 수가 아주 작으면 비율이 폭주 → 하한 1,000명으로 계산
DAILY_TOP_Q = 0.90         # 구독자와 무관하게 하루 조회수 상위 10% → 별도 묶음

COMMENT_VIDEOS_SUCCESS = 50  # 댓글 받을 성공 사례 수 (점수순)
COMMENT_VIDEOS_DAILY = 15    # 댓글 받을 하루 조회수 상위 수
COMMENT_PAGES = 1            # 영상당 100개(관련성순) × 페이지
MAX_PER_CHANNEL = 3          # v1.1.0: 댓글 대상·상위 표에서 한 채널은 최대 3편 (한 채널이 결과를 덮지 않게)

QUERIES = [
    # 채널 형식 그대로 (질문형·선택형)
    "당신이라면 어떻게 하시겠습니까",
    "만약 당신이라면 살아남을 수 있을까",
    "이 상황에서 당신의 선택은",
    "생존자와 사망자의 차이",
    "실화 위기 모면",
    # 범죄
    "납치 대처법 실제 사건",
    "강도 만났을 때 대처",
    "스토킹 실제 사건",
    "보이스피싱 실제 통화",
    "묻지마 범죄 대처",
    "택시 납치 실화",
    "주거침입 실제 사건",
    # 사고·재난
    "화재 생존 실화",
    "엘리베이터 갇혔을 때",
    "교통사고 생존 블랙박스",
    "물에 빠졌을 때 살아남는 법",
    "조난 생존 실화",
    "압사 사고 생존 방법",
    "지진 생존 대처",
    "급발진 대처법",
    # v1.1.0: 선택형 형식 (코밈 '엘레베이터에서 살아남기' 시리즈 발견 후 추가)
    "살아남기 선택",
    "당신은 살아남을 수 있을까",
    "어떤 선택을 하시겠습니까 생존",
    "위험한 상황 대처 실제 영상",
]

# ─────────────────────────── 로깅 ───────────────────────────
class StageFormatter(logging.Formatter):
    """[STAGE] [TIMESTAMP] key=value ... 형식."""

    def format(self, record: logging.LogRecord) -> str:
        stage = getattr(record, "stage", "INFO")
        ts = datetime.fromtimestamp(record.created).strftime("%Y-%m-%dT%H:%M:%S")
        return f"[{stage}] [{ts}] {record.getMessage()}"


log = logging.getLogger("crisis_lab")


def setup_logging() -> None:
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(StageFormatter())
    log.handlers[:] = [h]
    log.setLevel(os.environ.get("LOG_LEVEL", "INFO").upper())


def kv(**items) -> str:
    out = []
    for k, v in items.items():
        s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)
        if isinstance(v, str) and (" " in v or "=" in v):
            s = json.dumps(v, ensure_ascii=False)
        out.append(f"{k}={s}")
    return " ".join(out)


def L(stage: str, level: int = logging.INFO, **items) -> None:
    log.log(level, kv(**items), extra={"stage": stage})


# ─────────────────────────── API (캐시 우선) ───────────────────────────
class QuotaExceeded(RuntimeError):
    pass


@dataclass
class YT:
    key: str | None
    offline: bool = False
    units: int = 0
    calls: int = 0
    cache_hits: int = 0
    quota_dead: bool = False
    COST: dict = field(default_factory=lambda: {"search": 100, "videos": 1, "channels": 1, "commentThreads": 1})

    def get(self, endpoint: str, **params) -> dict | None:
        params = {k: v for k, v in params.items() if v is not None}
        h = hashlib.sha1(json.dumps([endpoint, params], sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
        path = CACHE_DIR / endpoint / f"{h}.json"
        if path.exists():
            self.cache_hits += 1
            return json.loads(path.read_text())
        if self.offline or self.quota_dead or not self.key:
            L("LOAD", logging.DEBUG, skip=endpoint, reason="offline/quota/no-key", params=params)
            return None
        try:
            r = requests.get(f"{API}/{endpoint}", params={**params, "key": self.key}, timeout=30)
        except requests.RequestException as e:
            L("LOAD", logging.WARNING, error="network", endpoint=endpoint, params=params, detail=str(e)[:200],
              next_step="잠시 후 run 다시 실행 (받은 응답은 캐시에 남아 있음)")
            return None
        self.calls += 1
        self.units += self.COST.get(endpoint, 1)
        if r.status_code == 403 and "quota" in r.text.lower():
            self.quota_dead = True
            L("LOAD", logging.WARNING, error="quotaExceeded", endpoint=endpoint, units_used=self.units,
              next_step="태평양 자정(KST 17시) 할당량 초기화 후 run 다시 실행 — 캐시된 부분은 다시 받지 않음")
            return None
        if r.status_code == 403 and "commentsDisabled" in r.text:
            data = {"items": [], "_disabled": True}
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data))
            return data
        if r.status_code != 200:
            L("LOAD", logging.WARNING, error=f"http{r.status_code}", endpoint=endpoint, params=params, body=r.text[:200])
            return None
        data = r.json()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False))
        return data


# ─────────────────────────── 1. LOAD ───────────────────────────
def iso_duration_sec(s: str | None) -> float:
    if not s:
        return np.nan
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s)
    if not m:
        return np.nan
    d, h, mi, se = (int(x) if x else 0 for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + se


def load_videos(yt: YT) -> pd.DataFrame:
    after = (AS_OF - timedelta(days=WINDOW_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    hits: list[tuple[str, str]] = []
    for q in QUERIES:
        data = yt.get("search", part="snippet", q=q, type="video", order="viewCount", maxResults=50,
                      regionCode="KR", relevanceLanguage="ko", publishedAfter=after)
        ids = [it["id"]["videoId"] for it in (data or {}).get("items", []) if it.get("id", {}).get("videoId")]
        hits += [(v, q) for v in ids]
        L("LOAD", logging.DEBUG, query=q, found=len(ids))
    if not hits:
        raise RuntimeError("검색 결과 0건 — 캐시도 없고 API도 실패. YOUTUBE_API_KEY·할당량 확인 후 다시 실행")
    hit_df = pd.DataFrame(hits, columns=["video_id", "query"])
    queries_by_vid = hit_df.groupby("video_id")["query"].agg(lambda s: "|".join(sorted(set(s))))
    vids = list(queries_by_vid.index)

    rows = []
    for i in range(0, len(vids), 50):
        data = yt.get("videos", part="snippet,statistics,contentDetails", id=",".join(vids[i:i + 50]), maxResults=50)
        for it in (data or {}).get("items", []):
            sn, st, cd = it["snippet"], it.get("statistics", {}), it.get("contentDetails", {})
            rows.append({
                "video_id": it["id"], "title": sn.get("title", ""), "channel_id": sn.get("channelId"),
                "channel": sn.get("channelTitle", ""), "published": sn.get("publishedAt"),
                "description": (sn.get("description") or "")[:500], "tags": "|".join(sn.get("tags", [])[:20]),
                "lang": sn.get("defaultAudioLanguage") or sn.get("defaultLanguage") or "",
                "views": st.get("viewCount"), "likes": st.get("likeCount"), "comments": st.get("commentCount"),
                "duration_sec": iso_duration_sec(cd.get("duration")),
            })
    vdf = pd.DataFrame(rows)
    chans = vdf["channel_id"].dropna().unique().tolist()
    crow = []
    for i in range(0, len(chans), 50):
        data = yt.get("channels", part="statistics", id=",".join(chans[i:i + 50]), maxResults=50)
        for it in (data or {}).get("items", []):
            st = it.get("statistics", {})
            crow.append({"channel_id": it["id"], "subs": None if st.get("hiddenSubscriberCount") else st.get("subscriberCount"),
                         "channel_videos": st.get("videoCount")})
    cdf = pd.DataFrame(crow, columns=["channel_id", "subs", "channel_videos"])
    vdf = vdf.merge(cdf, on="channel_id", how="left")
    vdf["queries"] = vdf["video_id"].map(queries_by_vid)
    L("LOAD", source="YouTube Data API v3 search(order=viewCount,KR,ko)", queries=len(QUERIES),
      search_hits=len(hit_df), unique_videos=len(vdf), channels=len(cdf),
      date_range=f"{after[:10]}~{AS_OF:%Y-%m-%d}", api_calls=yt.calls, units=yt.units, cache_hits=yt.cache_hits)
    return vdf


# ─────────────────────────── 2. VALIDATE ───────────────────────────
HANGUL = re.compile(r"[가-힣]")


def validate(vdf: pd.DataFrame) -> pd.DataFrame:
    n0 = len(vdf)
    dup = int(vdf.duplicated("video_id").sum())
    vdf = vdf.drop_duplicates("video_id").copy()
    for c in ["views", "likes", "comments", "subs", "channel_videos"]:
        vdf[c] = pd.to_numeric(vdf[c], errors="coerce")
    vdf["published"] = pd.to_datetime(vdf["published"], utc=True, errors="coerce")
    vdf["age_days"] = (AS_OF - vdf["published"]).dt.total_seconds() / 86400
    anomalies = {
        "duplicate_ids": dup,
        "missing_views": int(vdf["views"].isna().sum()),
        "hidden_or_missing_subs": int(vdf["subs"].isna().sum()),
        "missing_published": int(vdf["published"].isna().sum()),
        "future_published": int((vdf["age_days"] < 0).sum()),
        "too_new(<%dd)" % MIN_AGE_DAYS: int((vdf["age_days"] < MIN_AGE_DAYS).sum()),
        "older_than_window": int((vdf["age_days"] > WINDOW_DAYS + 1).sum()),
        "non_korean_title": int((~vdf["title"].str.contains(HANGUL)).sum()),
        "negative_counts": int((vdf[["views", "likes", "comments"]] < 0).any(axis=1).sum()),
    }
    keep = (vdf["views"].notna() & vdf["published"].notna() & vdf["age_days"].between(MIN_AGE_DAYS, WINDOW_DAYS + 1)
            & vdf["title"].str.contains(HANGUL))
    out = vdf[keep].copy()
    L("VALIDATE", level=logging.WARNING if sum(anomalies.values()) else logging.INFO,
      rows_in=n0, rows_out=len(out), anomalies=anomalies,
      note="구독자 숨김 채널은 성공 판정에서 빠지고 하루 조회수 상위 묶음으로만 볼 수 있음")
    return out


# ─────────────────────────── 3. FEATURE ───────────────────────────
DANGER = {  # 위험 유형 — 제목+태그+설명 앞부분에서 판정, 여러 개 가능
    "범죄_흉기·폭력": r"강도|흉기|칼부림|칼을|칼 든|칼든|살인|묻지마|폭행|괴한|인질|테러|총기|조폭|살해",
    "범죄_납치·감금": r"납치|감금|인신매매|끌려|유괴",
    "범죄_스토킹·침입": r"스토킹|스토커|미행|따라오|주거침입|침입|몰카|도어락|현관문",
    "범죄_사기": r"보이스피싱|피싱|스미싱|사기|스캠|전세사기|대출사기",
    "사고_교통": r"교통사고|블랙박스|역주행|급발진|추돌|충돌|트럭|오토바이|횡단보도|고속도로|운전",
    "사고_항공·선박": r"비행기|항공|여객기|추락기|불시착|선박|침몰|여객선|크루즈",  # v1.1.0: 화재보다 먼저 (엔진 폭발 = 항공)
    "사고_화재·폭발": r"화재|불길|불이 |불난|불나|연기|폭발|가스 ?누출|대피",
    "사고_물·수난": r"익사|물에 빠|계곡|바다|이안류|급류|침수|홍수|물놀이|수영장|저수지",
    "사고_추락·시설": r"엘리베이터|엘레베이터|엘베|에스컬레이터|추락|붕괴|지하철|공사장|놀이기구|맨홀|갇혔|갇힌",
    "재난_자연·조난": r"조난|등산|산에서|산속|실종|지진|쓰나미|태풍|산불|폭염|한파|눈사태|동굴|무인도",
    "재난_군중": r"압사|인파|군중|밀집",
    "동물": r"곰|멧돼지|상어|맹견|개물림|뱀|말벌|악어",
}
GENRE = {  # v1.1.0: 같은 위험 주제라도 장르가 다르면 시청자가 다름
    "유머·장난": r"웃긴|유머|ㅋㅋ|놀리|참교육|장난|빅맥송|parrot|앵무새|밈|meme|MZ식|빡치",
    "영화·드라마 리뷰": r"영화|결말포함|결말 포함|리뷰|드라마|주연|넷플릭스|띵작|명작",
    "괴담·공포": r"괴담|무서운이야기|무서운 이야기|공포라디오|공포이야기|미스터리",
    "뉴스·사건 보도": r"뉴스|NEWS|KNN|MBC|KBS|SBS|JTBC|YTN|연합|신상공개|기자|히든아이",
    "정보·대처법": r"대처|방법|팁|하는 법|수칙|강사|전문가|소방|경찰|하면 안|절대",
}
CRISIS_WORDS = r"살아남|생존|위기|갇혔|갇힌|탈출|구조|대피|사고|사건|위험|조난|재난|참사|사망|피해"

TITLE_FMT = {
    "질문형": r"\?|할까|일까|하시겠|어떻게 할|당신이라면|여러분이라면|당신은|당신의 선택|살아남을 수",
    "2인칭·참여": r"당신|여러분|너라면|나라면|저라면|당신의",
    "생존_결말": r"살아남|생존|살았|구조|기적|모면|탈출|피했|목숨을 건",
    "사망_결말": r"사망|죽음|죽었|숨진|숨졌|희생|참사|비극|목숨을 잃",
    "실화·실제": r"실화|실제|사건|CCTV|cctv|블랙박스|영상 공개|녹취",
    "대처법": r"대처|방법|하는 법|해야|하면 안|절대|꼭|반드시|요령|수칙",
    "충격·소름": r"소름|충격|경악|끔찍|공포|무서|섬뜩|레전드",
    "숫자": r"\d",
    "선택·비교": r"vs|VS|선택|둘 중|차이|갈린|갈렸",
}


def flag_frame(text: pd.Series, table: dict[str, str]) -> pd.DataFrame:
    """키워드 사전 → 0/1 열 (벡터화 str.contains)."""
    return pd.DataFrame({k: text.str.contains(p, regex=True, na=False).astype(np.int8) for k, p in table.items()})


def features(vdf: pd.DataFrame) -> pd.DataFrame:
    vdf = vdf.copy()
    text = vdf["title"] + " " + vdf["tags"].fillna("").str.replace("|", " ") + " " + vdf["description"].fillna("").str[:200]
    dang = flag_frame(text, DANGER).add_prefix("d_")
    genre = flag_frame(text, GENRE)
    fmt = flag_frame(vdf["title"], TITLE_FMT).add_prefix("t_")
    vdf = pd.concat([vdf.reset_index(drop=True), dang.reset_index(drop=True), fmt.reset_index(drop=True)], axis=1)
    dcols = [c for c in vdf if c.startswith("d_")]
    vdf["danger_main"] = np.where(vdf[dcols].sum(axis=1) > 0,
                                  vdf[dcols].idxmax(axis=1).str[2:], "기타·미분류")
    genre = genre.reset_index(drop=True)
    vdf["genre"] = np.where(genre.sum(axis=1) > 0, genre.idxmax(axis=1), "그 밖")
    # v1.1.0 주제 필터: 위험 유형 키워드가 있거나 위기 단어가 제목에 있어야 분석 대상
    # 게임·은유('AI시대에 살아남기')처럼 위기 단어만 빌린 영상 제외
    game = vdf["title"].str.contains(r"LCK|롤드컵|T1|티원|롤 |리그오브레전드|구마유시|페이커|템 선택|마인크래프트|로블록스|roblox|ROBLOX|"
                                     r"AI ?시대|취업|주식|코인|부동산|직장에서 살아남", regex=True, na=False)
    vdf["on_topic"] = ((vdf[dcols].sum(axis=1) > 0) | vdf["title"].str.contains(CRISIS_WORDS, regex=True, na=False)) & ~game
    n_off = int((~vdf["on_topic"]).sum())
    L("FEATURE", on_topic=int(vdf["on_topic"].sum()), off_topic=n_off,
      off_topic_examples=vdf.loc[~vdf["on_topic"], "title"].str[:30].head(5).tolist())
    vdf = vdf[vdf["on_topic"]].copy()
    # 채널 가중치: 한 채널이 k편이면 각 1/k → 채널 하나가 성공률을 부풀리지 않음
    vdf["ch_w"] = 1.0 / vdf.groupby("channel_id")["video_id"].transform("size")
    vdf["is_shorts"] = vdf["duration_sec"] <= SHORTS_MAX_SEC
    vdf["vpd"] = vdf["views"] / vdf["age_days"].clip(lower=1)
    subs_f = vdf["subs"].clip(lower=SUB_FLOOR)
    vdf["views_per_sub"] = vdf["views"] / subs_f
    vdf["vpd_per_sub"] = vdf["vpd"] / subs_f
    vdf["comment_rate"] = vdf["comments"] / vdf["views"].clip(lower=1) * 1000
    L("FEATURE", danger_types=len(DANGER), title_formats=len(TITLE_FMT),
      danger_counts=vdf["danger_main"].value_counts().to_dict(),
      genre_counts=vdf["genre"].value_counts().to_dict(),
      top_channels=vdf["channel"].value_counts().head(3).to_dict(),
      shorts=int(vdf["is_shorts"].sum()), long=int((~vdf["is_shorts"]).sum()),
      params={"SUB_FLOOR": SUB_FLOOR, "SHORTS_MAX_SEC": SHORTS_MAX_SEC})
    return vdf


# ─────────────────────────── 4. SIGNAL (성공 판정) ───────────────────────────
def label_success(vdf: pd.DataFrame, min_views: int = MIN_VIEWS, min_vps: float = MIN_VIEWS_PER_SUB) -> pd.DataFrame:
    vdf = vdf.copy()
    vdf["success"] = (vdf["views"] >= min_views) & (vdf["views_per_sub"] >= min_vps) & vdf["subs"].notna()
    vpd_cut = vdf["vpd"].quantile(DAILY_TOP_Q)
    vdf["daily_top"] = vdf["vpd"] >= vpd_cut
    vdf["group"] = np.select([vdf["success"], vdf["daily_top"]], ["성공 사례", "하루 조회수 상위"], "그 밖")
    vdf["score"] = vdf["vpd_per_sub"]
    L("SIGNAL", rule=f"views>={min_views} & views/max(subs,{SUB_FLOOR})>={min_vps}",
      success=int(vdf["success"].sum()), daily_top_cut=round(float(vpd_cut)), by_group=vdf["group"].value_counts().to_dict(),
      success_rate=round(float(vdf["success"].mean()), 3),
      success_rate_channel_weighted=round(float((vdf["success"] * vdf.get("ch_w", 1)).sum() / np.sum(vdf.get("ch_w", np.ones(len(vdf))))), 3),
      success_channels=int(vdf.loc[vdf["success"], "channel_id"].nunique()) if "channel_id" in vdf else None)
    # 기준을 바꾸면 결과가 얼마나 흔들리는지 (민감도) — 한 줄로 확인
    sens = {f"x{m}": int(((vdf["views"] >= min_views) & (vdf["views_per_sub"] >= m) & vdf["subs"].notna()).sum())
            for m in (1.0, 2.0, 5.0, 10.0)}
    L("SIGNAL", sensitivity_views_per_sub=sens)
    return vdf


def lift_table(vdf: pd.DataFrame) -> pd.DataFrame:
    """제목 형식·위험 유형별로 성공 사례 비율이 전체보다 몇 배인지."""
    def wrate(d):  # 채널 가중 성공률
        return float((d["success"] * d["ch_w"]).sum() / d["ch_w"].sum()) if len(d) else np.nan

    base = wrate(vdf)
    rows = []
    for c in [c for c in vdf if c.startswith(("t_", "d_"))]:
        m = vdf[c] == 1
        if m.sum() < 5:
            continue
        sub = vdf[m]
        rows.append({"feature": c[2:], "kind": "제목 형식" if c.startswith("t_") else "위험 유형", "n": int(m.sum()),
                     "channels": int(sub["channel_id"].nunique()),
                     "success_n": int(sub["success"].sum()), "success_rate": wrate(sub),
                     "raw_rate": sub["success"].mean(),
                     "lift": wrate(sub) / base if base else np.nan,
                     "median_views_per_sub": sub["views_per_sub"].median(), "median_vpd": sub["vpd"].median()})
    lt = pd.DataFrame(rows).sort_values(["kind", "lift"], ascending=[True, False])
    top = lt.nlargest(5, "lift")[["feature", "n", "lift"]].round(2).values.tolist()
    L("SIGNAL", base_success_rate_channel_weighted=round(float(base), 3), top_lift=top)
    return lt


# ─────────────────────────── 5. COMMENT ───────────────────────────
def load_comments(yt: YT, vdf: pd.DataFrame) -> pd.DataFrame:
    def capped(d, col, n):
        d = d.sort_values(col, ascending=False)
        return d[d.groupby("channel_id").cumcount() < MAX_PER_CHANNEL].head(n)

    succ = capped(vdf[vdf["success"]], "score", COMMENT_VIDEOS_SUCCESS)
    daily = capped(vdf[vdf["daily_top"] & ~vdf["success"]], "vpd", COMMENT_VIDEOS_DAILY)
    targets = pd.concat([succ, daily])
    rows, disabled = [], 0
    for vid, grp in zip(targets["video_id"], targets["group"]):
        token = None
        for _ in range(COMMENT_PAGES):
            data = yt.get("commentThreads", part="snippet", videoId=vid, order="relevance", maxResults=100,
                          textFormat="plainText", pageToken=token)
            if data is None:
                break
            disabled += int(bool(data.get("_disabled")))
            for it in data.get("items", []):
                s = it["snippet"]["topLevelComment"]["snippet"]
                # 작성자 이름은 저장하지 않음 (개인 정보 최소화)
                rows.append({"video_id": vid, "group": grp, "text": s.get("textDisplay", ""),
                             "likes": s.get("likeCount", 0), "published": s.get("publishedAt"),
                             "replies": it["snippet"].get("totalReplyCount", 0)})
            token = data.get("nextPageToken")
            if not token:
                break
    cdf = pd.DataFrame(rows, columns=["video_id", "group", "text", "likes", "published", "replies"])
    cdf["published"] = pd.to_datetime(cdf["published"], utc=True, errors="coerce")
    n0 = len(cdf)
    cdf = cdf.drop_duplicates(["video_id", "text"])
    cdf = cdf[cdf["text"].str.strip().str.len() >= 2]
    cdf = cdf[cdf["published"] <= AS_OF]  # 기준일 이후 댓글은 쓰지 않음
    L("COMMENT", target_videos=len(targets), max_per_channel=MAX_PER_CHANNEL, target_channels=int(targets["channel_id"].nunique()), success_videos=len(succ), daily_videos=len(daily),
      comments_raw=n0, comments_clean=len(cdf), comments_disabled_videos=disabled,
      api_calls=yt.calls, units=yt.units, cache_hits=yt.cache_hits)
    return cdf


# ─────────────────────────── 6. SEGMENT ───────────────────────────
SEGMENTS = {  # 시청자 묶음 — 댓글 문장에서 판정 (여러 개 가능). v1.1.0: 실제 댓글 표본 보고 말투 맞춤
    "simulator": ("'나라면' 시뮬레이터", r"나라면|저라면|나 같으면|저 같으면|내가 저|만약 나|만약에 나|나는 바로|저는 바로|나였으면|저였으면|"
                  r"난 무조건|나는 무조건|저는 무조건|전 무조건|난 그냥|나는 그냥|할듯|할 듯|하겠다|하겠음|하겠네|하겠습니다|할 것 같|할거같|할 거 같|"
                  r"고른다|고름|골랐|선택한다|선택함|[1-9]번이|[1-9]번 고|[1-9]번 선택|[1-9]번이지|[1-9]번 문"),
    "survivor": ("실제로 겪어 본 사람", r"저도 비슷|저도 예전|실제로 겪|당한 적|당했었|겪었|경험이 있|경험했|그때 생각|트라우마|제가 당|저희 집에|제 친구가|친구가 당|"
                 r"겪어 봐서|겪어봐서|저도 그런 적|뻔했|뻔한|뻔 했|뻔함|어릴 때|어렸을 때|어릴때|어렸을때|얼마 ?전에|예전에 제가|작년에|"
                 r"전화 ?받았|문자 ?왔|문자가 왔|전화가 왔|전화 왔|저도 이거|나도 이거|저희 엄마가|우리 엄마가|저희 아버지가|우리 아빠가"),
    "fact_checker": ("정보 보태고 바로잡는 사람", r"사실은|사실 |틀린|틀렸|아닙니다|아님|오히려|잘못된|정확히는|정확하게|원래는|이론상|이론은|"
                     r"하면 됩니다|해야 합니다|해야됩니다|해야 됩니다|하세요|주의하세요|참고로|과학적으로|물리적으로|사례는|통계|확률|팩트|"
                     r"해야함|해야 함|해야돼|해야 돼|꼭 |한정|필수|연습|알려줘야|교육이 필요|배워야|무조건 산다"),
    "empathy": ("그 자리에 있던 사람에 감정이입", r"얼마나 (?:무서웠|두려웠|힘들었|아팠|괴로웠|놀랬|놀랐)|안타깝|눈물|억장|마음이 아프|가슴이 아프|가슴 아프|"
                r"명복|영면|내 ?가족|우리 가족이|생각만 해도|상상만 해도|상상도 안|끔찍"),
    "judge": ("선택을 판정하는 사람", r"대처 잘|잘 대처|대처를 잘|현명|침착하|침착한|똑똑|대단하|잘했|멋지|훌륭|영웅|왜 문을|저러면 안|답답|바보|멍청|"
              r"왜 저렇게|왜 저기|판단|희생할|살린|살렸"),
    "humor": ("가볍게 즐기는 쇼츠 시청자", r"ㅋㅋㅋ|웃기|개웃|빵 ?터|터졌|ㅎㅎㅎ|드립|웃겨|웃음|😂|🤣"),
    "justice": ("참사·제도에 분노하는 사람", r"처벌|형량|정당방위|판사|법이|사형|감옥|가해자|솜방망이|집행유예|법원|국회|참사|밝혀|입법부|사법부|"
                r"나라가|정부|책임자|세월호|이태원|무안|정치인|경찰도 믿|무비자"),
    "woman_safety": ("혼자 다니는 여성", r"여자 ?혼자|여성 ?혼자|혼자 사는|자취|밤길|귀갓길|여자라서|여자들은|여자분들|원룸|여성분들|딸 가진|여자 입장|여자분|여자가 혼자"),
    "parent": ("아이 걱정하는 부모", r"우리 아이|우리 애|우리 딸|우리 아들|딸아이|자녀|애 키우|아이 키우|엄마로서|아빠로서|부모로서|부모 입장|학부모|육아|우리 아기|애들 데리고"),
    "pro": ("현직·경험 전문가", r"현직|경찰관|경찰입니다|소방관|소방대원|구급대원|간호사|응급실|군인|군대에서|부사관|장교|경호|보안요원|택시기사|기사입니다|구조대|해병|"
            r"수영 ?강사|안전요원|라이프가드|인명구조|해경|기관사|승무원|조종사|정비사|엘리베이터 기사|변호사"),
    "driver": ("운전·출퇴근 하는 사람", r"운전|차선|블랙박스|브레이크|엑셀|악셀|핸들|고속도로|출퇴근|택시|버스"),
}
AGE_PATTERNS = [
    r"(?:저는|전|제가|나는|난|저|나|올해)\s*(?:올해\s*)?([1-9])0대",
    r"([1-9])0대\s*(?:인데|입니다|이에요|예요|아줌마|아저씨|주부|남자|여자|여성|남성|직장인|후반|초반|중반)",
]
STUDENT = r"중학생|고등학생|고딩|중딩|대학생|학생인데|학생입니다|고3|고2|고1|수험생"
AGE_HINT = {  # v1.1.0: 나이를 직접 안 밝힌 댓글의 간접 단서 (숫자 나이보다 약한 근거 — 따로 집계)
    "10대": r"초딩|중딩|고딩|중학생|고등학생|고3|고2|고1|수험생|학교에서 배",
    "20대": r"대학생|군대|전역|군복무|예비군|신입|취준",
    "30~40대": r"애 키우|아이 키우|육아|우리 애|우리 아이|어린이집|유치원",
    "50대 이상": r"손주|손자|손녀|할머니인데|할아버지인데|환갑|퇴직|은퇴|노후",
}
FEMALE = r"여자(?:인데|입니다|라서)|여성(?:인데|입니다|으로서)|엄마(?:인데|입니다|로서)|아줌마|주부|딸 가진|애엄마|아내|와이프는 아닌"
MALE = r"남자(?:인데|입니다|라서)|남성(?:인데|입니다)|아빠(?:인데|입니다|로서)|아저씨|군대|전역|예비군|군복무|남편은 아닌"
ACTIONS = {  # "나라면" 댓글에서 말하는 행동
    "도망·피하기": r"도망|튀|뛰어|달려|피하|도망가|자리를 뜨|빠져나",
    "맞서기·제압": r"싸우|때리|제압|패버|맞서|반격|덤비|죽여|찌르",
    "신고·도움요청": r"112|119|신고|경찰 부르|경찰에 전화|경찰서|도와달라|도와주세요|살려",  # v1.1.0: '전화'·'문자' 제외 (보이스피싱 댓글 오탐)
    "침착·순응": r"침착|가만히|시키는 대로|순순히|협조|모른 척|아무렇지 않",
    "얼어붙음": r"얼어|굳어|아무것도 못|몸이 안 움직|패닉|멘붕|머리가 하얘|그대로 당",
    "미리 대비": r"호신|호루라기|스프레이|삼단봉|잠그|잠가|체인|비상구|위치 확인|소화기|미리|평소에",
}
EMOTION = {
    "공포·불안": r"무섭|무서워|소름|떨려|불안|공포|섬뜩|오싹",
    "안도": r"다행|살아서|무사|천만다행|감사하",
    "슬픔·애도": r"명복|안타깝|슬프|눈물|마음이 아프|가슴이 아프",
    "분노": r"화가|열받|빡치|분노|어이없|미친|쓰레기",
}
WANTS = {
    "구체적 대처법": r"방법|알려|대처|어떻게 해야|해야 하|요령|팁|정보",
    "다음 편·더 많은 사례": r"다음 편|다음편|2탄|후속|더 올려|더 알려|시리즈|또 해",
    "후일담·결말": r"결말|어떻게 됐|그 후|그후|이후에|잡혔|검거",
    "공유·전파": r"공유|퍼가|알려야|널리|보여줘야|봐야 합니다|꼭 봐",
}


def segment(cdf: pd.DataFrame) -> pd.DataFrame:
    cdf = cdf.copy().reset_index(drop=True)
    t = cdf["text"]
    seg = flag_frame(t, {k: v[1] for k, v in SEGMENTS.items()}).add_prefix("s_")
    act = flag_frame(t, ACTIONS).add_prefix("a_")
    emo = flag_frame(t, EMOTION).add_prefix("e_")
    want = flag_frame(t, WANTS).add_prefix("w_")
    cdf = pd.concat([cdf, seg, act, emo, want], axis=1)
    age = pd.Series(np.nan, index=cdf.index)
    for p in AGE_PATTERNS:
        age = age.fillna(t.str.extract(p, expand=False).astype(float) * 10)
    cdf["age"] = age
    yob = t.str.extract(r"(?<!\d)([0-9]{2})년생", expand=False).astype(float)
    yob_age = ((AS_OF.year - np.where(yob > 26, 1900 + yob, 2000 + yob)) // 10 * 10)
    cdf["age"] = cdf["age"].fillna(pd.Series(yob_age, index=cdf.index).where(yob.notna()))
    cdf["age"] = cdf["age"].where(cdf["age"].between(10, 90))
    ah = flag_frame(t, AGE_HINT)
    cdf["age_hint"] = np.where(ah.sum(axis=1) > 0, ah.idxmax(axis=1), None)
    cdf["student"] = t.str.contains(STUDENT, regex=True).astype(np.int8)
    cdf["female"] = t.str.contains(FEMALE, regex=True).astype(np.int8)
    cdf["male"] = t.str.contains(MALE, regex=True).astype(np.int8)
    scol = [c for c in cdf if c.startswith("s_")]
    cover = float((cdf[scol].sum(axis=1) > 0).mean())
    L("SEGMENT", comments=len(cdf), segments=len(SEGMENTS),
      counts={c[2:]: int(cdf[c].sum()) for c in scol}, cover=round(cover, 3),
      age_n=int(cdf["age"].notna().sum()), age_hint=cdf["age_hint"].value_counts().to_dict(), student_n=int(cdf["student"].sum()),
      female_n=int(cdf["female"].sum()), male_n=int(cdf["male"].sum()))
    return cdf


# ─────────────────────────── 7. PERSONA ───────────────────────────
# v1.2.0: 제목·썸네일을 만들 최종 페르소나 — 행동이 비슷한 묶음끼리 합침 (댓글 중복은 한 번만 셈)
PERSONA_GROUPS = {
    "F1": ("웃으려고 보는 쇼츠 시청자", ["humor"]),
    "F2": ("참사에 감정이입하고 분노하는 사람", ["justice", "empathy"]),
    "F3": ("정보를 보태는 경험자·전문가", ["fact_checker", "pro", "survivor"]),
    "F4": ("선택을 판정하는 '나라면' 참여자", ["judge", "simulator", "parent", "woman_safety"]),
}

STOP = set("진짜 너무 정말 그냥 저런 이런 저는 나는 그리고 근데 그런 이거 저거 하는 있는 없는 같은 같아요 합니다 했는데 하고 있어 "
           "있다 없다 것 수 더 다 안 잘 좀 또 왜 이 저 그 거 게 걸 건 데 때 분 중 및 영상 감사합니다 보고 봤는데 ㅋㅋ ㅋㅋㅋ ㅠㅠ".split())


def tokens(series: pd.Series) -> pd.Series:
    """아주 단순한 한국어 토큰: 공백 분리 + 끝 조사 몇 개 제거 (형태소 분석기 없이 추적 가능하게)."""
    s = series.str.replace(r"[^가-힣a-zA-Z0-9 ]", " ", regex=True).str.split()
    ex = s.explode().dropna()
    ex = ex.str.replace(r"(은|는|이|가|을|를|에|에서|으로|로|도|만|의|과|와|한테|에게)$", "", regex=True)
    return ex[(ex.str.len() >= 2) & ~ex.isin(STOP)]


def top_of(df: pd.DataFrame, prefix: str, k: int = 3) -> list[tuple[str, float]]:
    cols = [c for c in df if c.startswith(prefix)]
    if not len(df):
        return []
    r = df[cols].mean().sort_values(ascending=False).head(k)
    return [(c[len(prefix):], round(float(v), 3)) for c, v in r.items()]


def personas(cdf: pd.DataFrame, vdf: pd.DataFrame) -> list[dict]:
    vmeta = vdf.set_index("video_id")[["danger_main", "title", "genre", "is_shorts"]]
    cdf = cdf.join(vmeta, on="video_id")
    split = AS_OF - timedelta(days=RECENT_DAYS)
    out = []
    for key, (name, _) in SEGMENTS.items():
        m = cdf[f"s_{key}"] == 1
        sub = cdf[m]
        if len(sub) < 30:
            L("PERSONA", logging.DEBUG, key=key, skipped="n<15", n=int(m.sum()))
            continue
        recent, old = sub[sub["published"] >= split], sub[sub["published"] < split]
        quotes = (sub[sub["text"].str.len().between(20, 160)].nlargest(4, "likes")[["text", "likes", "title"]]
                  .to_dict("records"))
        p = {
            "key": key, "name": name, "n": int(len(sub)), "share": round(len(sub) / len(cdf), 3),
            "videos": int(sub["video_id"].nunique()),
            "age_n": int(sub["age"].notna().sum()),
            "age_median": None if sub["age"].notna().sum() == 0 else float(sub["age"].median()),
            "student_n": int(sub["student"].sum()), "female_n": int(sub["female"].sum()), "male_n": int(sub["male"].sum()),
            "age_hint": sub["age_hint"].value_counts().to_dict(),
            "top_danger": sub["danger_main"].value_counts(normalize=True).head(3).round(3).to_dict(),
            "top_genre": sub["genre"].value_counts(normalize=True).head(3).round(3).to_dict(),
            "shorts_share": round(float(sub["is_shorts"].mean()), 3),
            "top_action": top_of(sub, "a_"), "top_emotion": top_of(sub, "e_"), "top_want": top_of(sub, "w_"),
            "median_likes": float(sub["likes"].median()), "like_share": round(float(sub["likes"].sum() / max(cdf["likes"].sum(), 1)), 3),
            "recent": int(len(recent)), "old": int(len(old)),
            "top_words": tokens(sub["text"]).value_counts().head(12).index.tolist(),
            "quotes": quotes,
        }
        out.append(p)
    out.sort(key=lambda p: p["n"], reverse=True)
    for i, p in enumerate(out, 1):
        p["id"] = f"P{i}"
        L("PERSONA", id=p["id"], key=p["key"], n=p["n"], share=p["share"], age_n=p["age_n"], age_median=p["age_median"],
          f=p["female_n"], m=p["male_n"], top_danger=next(iter(p["top_danger"]), None),
          top_action=p["top_action"][0][0] if p["top_action"] else None,
          top_want=p["top_want"][0][0] if p["top_want"] else None, like_share=p["like_share"])
    return out


def merge_personas(cdf: pd.DataFrame, vdf: pd.DataFrame) -> list[dict]:
    vmeta = vdf.set_index("video_id")[["danger_main", "title", "genre", "is_shorts"]]
    cdf = cdf.join(vmeta, on="video_id")
    total_likes = max(cdf["likes"].sum(), 1)
    out = []
    for fid, (name, keys) in PERSONA_GROUPS.items():
        m = cdf[[f"s_{k}" for k in keys]].sum(axis=1) > 0
        sub = cdf[m]
        top_q = sub[sub["text"].str.len().between(15, 140)].nlargest(3, "likes")[["text", "likes", "title"]].to_dict("records")
        p = {"id": fid, "name": name, "from": keys, "n": int(len(sub)), "share": round(float(m.mean()), 3),
             "like_share": round(float(sub["likes"].sum() / total_likes), 3),
             "median_likes": float(sub["likes"].median()) if len(sub) else 0.0,
             "videos": int(sub["video_id"].nunique()), "shorts_share": round(float(sub["is_shorts"].mean()), 3),
             "age_n": int(sub["age"].notna().sum()), "age_hint": sub["age_hint"].value_counts().to_dict(),
             "female_n": int(sub["female"].sum()), "male_n": int(sub["male"].sum()),
             "top_danger": sub["danger_main"].value_counts(normalize=True).head(3).round(3).to_dict(),
             "top_genre": sub["genre"].value_counts(normalize=True).head(2).round(3).to_dict(),
             "top_emotion": top_of(sub, "e_", 2), "quotes": top_q,
             # 좋아요가 영상 한 편에 몰렸는지 — 높으면 '이 묶음 전체'가 아니라 '그 영상 하나'의 반응
             "top_video_like_share": round(float(sub.groupby("video_id")["likes"].sum().max() / max(sub["likes"].sum(), 1)), 3)}
        out.append(p)
        L("PERSONA", final=fid, name=name, n=p["n"], share=p["share"], like_share=p["like_share"],
          median_likes=p["median_likes"], top_video_like_share=p["top_video_like_share"],
          top_danger=next(iter(p["top_danger"]), None), shorts_share=p["shorts_share"])
    overlap = int((cdf[[f"s_{k}" for g in PERSONA_GROUPS.values() for k in g[1]]].sum(axis=1) > 0).sum())
    L("PERSONA", final_cover=round(overlap / max(len(cdf), 1), 3), note="나머지 댓글은 묶음 단서 없음(짧은 감탄·잡담)")
    return out


# ─────────────────────────── 8. TREND ───────────────────────────
def trend(vdf: pd.DataFrame, cdf: pd.DataFrame) -> dict:
    split = AS_OF - timedelta(days=RECENT_DAYS)
    rv, ov = vdf[vdf["published"] >= split], vdf[vdf["published"] < split]
    L("TREND", split=f"old<{split:%Y-%m-%d}<=recent<={AS_OF:%Y-%m-%d}", recent_videos=len(rv), old_videos=len(ov))

    def share(df):
        return df["danger_main"].value_counts(normalize=True)

    ds = pd.concat({"old": share(ov), "recent": share(rv)}, axis=1).fillna(0).round(3)
    ds["diff"] = (ds["recent"] - ds["old"]).round(3)
    # 최근 영상 중 성공 사례 — 지금 먹히는 소재
    hot = rv.sort_values("score", ascending=False).head(5)[["title", "views", "subs", "views_per_sub"]].to_dict("records")
    rc, oc = cdf[cdf["published"] >= split], cdf[cdf["published"] < split]
    rt, ot = tokens(rc["text"]).value_counts(), tokens(oc["text"]).value_counts()
    rate = ((rt + 1) / (len(rc) + 1)) / ((ot.reindex(rt.index).fillna(0) + 1) / (len(oc) + 1))
    rising = rate[rt >= 8].sort_values(ascending=False).head(12).index.tolist()
    L("TREND", danger_share_diff=ds["diff"].sort_values(ascending=False).head(4).to_dict(),
      recent_comments=len(rc), old_comments=len(oc), rising_words=rising,
      hot=hot[0]["title"] if hot else None)
    return {"split": split, "danger_share": ds, "hot": hot, "rising": rising, "recent_videos": len(rv), "old_videos": len(ov)}


# ─────────────────────────── 9. EXPORT ───────────────────────────
def fmt_int(x) -> str:
    return "-" if pd.isna(x) else f"{int(x):,}"


def export(vdf, lt, cdf, ps, tr, t0, fps=None) -> None:
    RESULT_DIR.mkdir(exist_ok=True)
    cols = ["group", "title", "channel", "subs", "views", "views_per_sub", "vpd", "age_days", "is_shorts",
            "duration_sec", "danger_main", "genre", "comments", "published", "video_id", "queries"]
    vdf.sort_values("score", ascending=False)[cols].to_csv(RESULT_DIR / "videos.csv", index=False)
    lt.to_csv(RESULT_DIR / "title_lift.csv", index=False)

    s = vdf[vdf["success"]].sort_values("score", ascending=False)
    s_cap = s[s.groupby("channel_id").cumcount() < MAX_PER_CHANNEL]
    a = [f"# 위기 상황 채널 — 성공 사례 분석 ({VERSION}, 기준일 {AS_OF:%Y-%m-%d})", "",
         f"- 검색어 {len(QUERIES)}개 · 영상 {len(vdf)}개(최근 {WINDOW_DAYS}일, {MIN_AGE_DAYS}일 미만 제외) · "
         f"성공 사례 {len(s)}개 (조회수 ≥ {MIN_VIEWS:,} & 조회수/구독자 ≥ {MIN_VIEWS_PER_SUB}, 구독자 하한 {SUB_FLOOR:,})",
         f"- 쇼츠(≤{SHORTS_MAX_SEC}초) 성공 {int(s['is_shorts'].sum())}개 · 롱폼 성공 {int((~s['is_shorts']).sum())}개 · "
         f"롱폼 성공 길이 중앙값 {s.loc[~s['is_shorts'], 'duration_sec'].median() / 60:.1f}분", "",
         f"- 성공 사례를 낸 채널 {s['channel_id'].nunique()}개 · 가장 많이 낸 채널: "
         + ", ".join(f"{k} {v}편" for k, v in s["channel"].value_counts().head(3).items()),
         f"- 비율은 모두 **채널 가중**(한 채널 k편이면 각 1/k) — 한 채널이 수십 편 올린 효과를 지움", "",
         f"## 성공 사례 상위 25 (채널당 최대 {MAX_PER_CHANNEL}편)", "",
         "| # | 제목 | 채널 | 구독자 | 조회수 | 조회/구독 | 형식 | 위험 유형 | 장르 |", "|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(s_cap.head(25).itertuples(), 1):
        a.append(f"| {i} | {r.title.replace('|', '/')} | {r.channel.replace('|', '/')} | {fmt_int(r.subs)} | {fmt_int(r.views)} | "
                 f"{r.views_per_sub:.1f} | {'쇼츠' if r.is_shorts else f'{r.duration_sec / 60:.0f}분'} | {r.danger_main} | {r.genre} |")
    a += ["", "## 위험 유형별 성과", "", "| 위험 유형 | 영상 | 성공 | 성공 비율 | 조회/구독 중앙값 |", "|---|---|---|---|---|"]
    def grp_table(col):
        g = vdf.assign(ws=vdf["success"] * vdf["ch_w"]).groupby(col).agg(
            n=("video_id", "size"), ch=("channel_id", "nunique"), succ=("success", "sum"), ws=("ws", "sum"),
            w=("ch_w", "sum"), vps=("views_per_sub", "median"))
        g["rate"] = g["ws"] / g["w"]
        return g.sort_values("rate", ascending=False)

    for k, r in grp_table("danger_main").iterrows():
        a.append(f"| {k} | {int(r.n)} ({int(r.ch)}채널) | {int(r.succ)} | {r.rate:.0%} | {r.vps:.2f} |")
    a += ["", "## 장르별 성과", "", "| 장르 | 영상 | 성공 | 성공 비율 | 조회/구독 중앙값 |", "|---|---|---|---|---|"]
    for k, r in grp_table("genre").iterrows():
        a.append(f"| {k} | {int(r.n)} ({int(r.ch)}채널) | {int(r.succ)} | {r.rate:.0%} | {r.vps:.2f} |")
    a += ["", "## 쇼츠 vs 롱폼", "", "| 형식 | 영상 | 성공 | 성공 비율 | 조회/구독 중앙값 |", "|---|---|---|---|---|"]
    for k, r in grp_table("is_shorts").iterrows():
        a.append(f"| {'쇼츠' if k else '롱폼'} | {int(r.n)} ({int(r.ch)}채널) | {int(r.succ)} | {r.rate:.0%} | {r.vps:.2f} |")
    a += ["", f"## 제목 형식별 성공 비율 (전체 {(vdf['success'] * vdf['ch_w']).sum() / vdf['ch_w'].sum():.0%} 대비 배수, 채널 가중)", "",
          "| 제목 형식 | 영상 | 채널 | 성공 | 성공 비율 | 배수 |", "|---|---|---|---|---|---|"]
    for r in lt[lt["kind"] == "제목 형식"].itertuples():
        a.append(f"| {r.feature} | {r.n} | {r.channels} | {r.success_n} | {r.success_rate:.0%} | {r.lift:.2f} |")
    a += ["", f"## 추세 (최근 {RECENT_DAYS}일 vs 이전, 경계 {tr['split']:%Y-%m-%d})", "",
          f"- 최근 영상 {tr['recent_videos']}개 / 이전 {tr['old_videos']}개", "",
          "| 위험 유형 | 이전 비중 | 최근 비중 | 변화 |", "|---|---|---|---|"]
    for k, r in tr["danger_share"].sort_values("diff", ascending=False).iterrows():
        a.append(f"| {k} | {r.old:.0%} | {r.recent:.0%} | {r['diff']:+.0%} |")
    a += ["", "최근 영상 중 구독자 대비 가장 잘 된 것:", ""]
    a += [f"- {h['title']} — 구독자 {fmt_int(h['subs'])} · 조회수 {fmt_int(h['views'])} · 조회/구독 {h['views_per_sub']:.1f}" for h in tr["hot"]]
    a += ["", f"최근 댓글에서 늘어난 단어: {', '.join(tr['rising']) or '-'}", ""]
    (RESULT_DIR / "analysis.md").write_text("\n".join(a))

    b = [f"# 위기 상황 채널 — 시청자 페르소나 ({VERSION})", "",
         f"- 댓글 {len(cdf):,}개 (성공 사례·하루 조회수 상위 영상, 관련성순 상위 100개씩). 작성자 이름은 저장하지 않음.",
         "- 묶음은 키워드 사전(`crisis_lab.py` SEGMENTS)으로 판정 — 댓글 하나가 여러 묶음에 들어갈 수 있음.",
         "- 나이를 밝힌 댓글이 거의 없음(심리 채널과 다름) → 나이는 간접 단서로만 적고, 페르소나 나이는 판단으로 둠.", ""]
    if fps:
        b += ["## 최종 페르소나 4명 (제목·썸네일용, 묶음 합침)", "",
              "| ID | 페르소나 | 합친 묶음 | 댓글 | 비중 | 좋아요 몫 | 그중 영상 1편 몫 | 쇼츠 비중 | 위험 유형 1·2위 |", "|---|---|---|---|---|---|---|---|---|"]
        for f in fps:
            b.append(f"| {f['id']} | {f['name']} | {', '.join(f['from'])} | {f['n']:,} | {f['share']:.0%} | {f['like_share']:.0%} | "
                     f"{f['top_video_like_share']:.0%} | {f['shorts_share']:.0%} | " + ", ".join(f"{k} {v:.0%}" for k, v in list(f["top_danger"].items())[:2]) + " |")
        b += ["", "## 세부 묶음 (판정 근거)", ""]
    for p in ps:
        age = f"{p['age_median']:.0f}대 (나이 밝힌 {p['age_n']}명)" if p["age_median"] else f"단서 부족 (나이 밝힌 {p['age_n']}명)"
        b += [f"## {p['id']} {p['name']} — 댓글 {p['n']:,}개 ({p['share']:.0%}) · 좋아요 몫 {p['like_share']:.0%}", "",
              f"- 나이: {age} · 간접 단서 {p['age_hint'] or '-'} · 여성 단서 {p['female_n']} / 남성 단서 {p['male_n']}",
              f"- 주로 보는 장르: " + ", ".join(f"{k} {v:.0%}" for k, v in p["top_genre"].items()) + f" · 쇼츠 댓글 비중 {p['shorts_share']:.0%}",
              f"- 주로 댓글 다는 위험 유형: " + ", ".join(f"{k} {v:.0%}" for k, v in p["top_danger"].items()),
              f"- '나라면' 행동: " + ", ".join(f"{k} {v:.0%}" for k, v in p["top_action"]),
              f"- 감정: " + ", ".join(f"{k} {v:.0%}" for k, v in p["top_emotion"]),
              f"- 원하는 것: " + ", ".join(f"{k} {v:.0%}" for k, v in p["top_want"]),
              f"- 최근 {RECENT_DAYS}일 {p['recent']} / 이전 {p['old']} · 자주 쓰는 말: {', '.join(p['top_words'])}", "", "대표 댓글 (좋아요순):", ""]
        b += [f"> {q['text'].replace(chr(10), ' ')} — 좋아요 {q['likes']:,} · 영상 「{q['title'][:40]}」" for q in p["quotes"]]
        b.append("")
    (RESULT_DIR / "personas.md").write_text("\n".join(b))
    (RESULT_DIR / "personas.json").write_text(json.dumps({"final": fps, "segments": ps}, ensure_ascii=False, indent=1, default=str))
    L("EXPORT", files=["analysis.md", "personas.md", "personas.json", "videos.csv", "title_lift.csv"],
      dir=str(RESULT_DIR.relative_to(ROOT.parent)), seconds=round(time.time() - t0, 1))


# ─────────────────────────── main ───────────────────────────
def main(argv: list[str]) -> int:
    setup_logging()
    mode = argv[1] if len(argv) > 1 else "run"
    t0 = time.time()
    L("DONE", version=VERSION, mode=mode, as_of=f"{AS_OF:%Y-%m-%d}", seed=SEED,
      note="연구·기획용 — 안전 조언은 공식 지침으로 확인")
    yt = YT(key=os.environ.get("YOUTUBE_API_KEY"), offline=(mode == "analyze"))
    try:
        vdf = load_videos(yt)
    except RuntimeError as e:
        L("LOAD", logging.ERROR, failed="load_videos", detail=str(e))
        return 1
    vdf = label_success(features(validate(vdf)))
    lt = lift_table(vdf)
    cdf = segment(load_comments(yt, vdf))
    ps = personas(cdf, vdf)
    fps = merge_personas(cdf, vdf)
    tr = trend(vdf, cdf)
    export(vdf, lt, cdf, ps, tr, t0, fps)
    L("DONE", personas=len(ps), success=int(vdf["success"].sum()), api_calls=yt.calls, units=yt.units,
      cache_hits=yt.cache_hits, quota_dead=yt.quota_dead, seconds=round(time.time() - t0, 1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
