"""
RAG PoC 전역 설정.

경로·모델명·임계값·LLM provider를 한곳에 모은다.
무인증/오프라인에서도 실행되도록 합리적 기본값(stub, 더미 임베딩 폴백)을 둔다.
"""

import os
from pathlib import Path

# --- 경로 ---
# 이 파일(config.py) 기준 상대경로로 위키 코퍼스/산출물 위치를 계산한다.
BASE_DIR = Path(__file__).resolve().parent          # .../practice/rag-poc
WIKI_ROOT = BASE_DIR.parent.parent                  # .../claudeWIKI
CONCEPTS_DIR = WIKI_ROOT / "concepts"               # 코퍼스: concepts/*.md
EVAL_DIR = BASE_DIR / "eval"                         # 인덱스 산출물·골든셋
INDEX_PATH = EVAL_DIR / "index.pkl"                  # ingest 산출 인메모리 인덱스(pickle)

# --- 임베딩 모델 ---
# 한국어 포함 다국어 모델. e5 계열은 "query:"/"passage:" 프리픽스 관례가 있다.
EMBED_MODEL = os.getenv("RAG_EMBED_MODEL", "intfloat/multilingual-e5-base")
# CrossEncoder 리랭커(있으면 사용). 다국어 지원 모델 예시.
RERANK_MODEL = os.getenv("RAG_RERANK_MODEL", "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1")

# --- 인덱싱/검색 모드 ---
MODE = os.getenv("RAG_MODE", "lite")                # "lite"(인메모리) | "pgvector"
TOP_K = int(os.getenv("RAG_TOP_K", "5"))            # 최종 컨텍스트 개수
CANDIDATE_K = int(os.getenv("RAG_CANDIDATE_K", "20"))  # 융합 전 각 축에서 뽑을 후보 수
RRF_K = 60                                          # RRF 상수(관례값 60)
RERANK = os.getenv("RAG_RERANK", "1") == "1"        # CrossEncoder 재랭킹 사용 여부

# --- 청킹 ---
MIN_CHUNK_CHARS = 200                               # 이보다 작은 청크는 인접 청크와 병합
MAX_CHUNK_CHARS = 1200                              # 이보다 크면 문단 경계로 분할

# --- Self/CRAG-lite 관련성 임계 ---
# grade_contexts가 돌려주는 confidence(0~1)가 이 미만이면 low_confidence + 무근거 폴백.
RELEVANCE_THRESHOLD = float(os.getenv("RAG_RELEVANCE_THRESHOLD", "0.25"))

# --- LLM provider ---
# None이면 stub 생성기(컨텍스트 추출/요약)로 폴백 → 무인증 실행 가능.
# 운영 시 예: {"provider": "anthropic", "model": "claude-...", "api_key_env": "ANTHROPIC_API_KEY"}
LLM_PROVIDER = None  # type: ignore  # dict | None

# --- RAGAS CI 게이트 임계(README 표와 일치) ---
RAGAS_THRESHOLDS = {
    "faithfulness": 0.90,
    "answer_relevancy": 0.85,
    "context_precision": 0.80,
    "context_recall": 0.85,
}

# --- pgvector 접속(MODE="pgvector"일 때만 사용) ---
PG_DSN = os.getenv("RAG_PG_DSN", "postgresql://localhost:5432/rag")
EMBED_DIM = 768  # multilingual-e5-base 차원(schema.sql vector(768)와 일치)
