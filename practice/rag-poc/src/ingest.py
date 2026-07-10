"""
① 청킹 + ② 맥락 보강 + ③ 인덱싱 (수집 파이프라인).

concepts/*.md 를 읽어:
  ① 마크다운 헤더/문단 기준 시맨틱 청킹(너무 작은 조각은 병합).
  ② 각 청크 앞에 "[문서제목 > 섹션] " 맥락 헤더를 prepend(Contextual Retrieval).
  ③ Dense(맥락텍스트 임베딩) + Sparse(BM25 토큰) 인메모리 인덱스 구성.
산출: eval/index.pkl (pickle). retrieve.py가 로드.

실행:  python src/ingest.py
"""

from __future__ import annotations

import pickle
import re
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np

# src/ 단독 실행과 패키지 import 양쪽을 지원.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from src.embeddings import embed_passages, using_dummy


# ─────────────────────────── ① 청킹 ───────────────────────────

def _split_markdown(raw: str) -> List[Dict]:
    """
    마크다운을 (섹션 헤더, 본문 블록) 단위로 1차 분해한다.
    ## / ### 헤더를 섹션 경계로 보고, 그 아래 문단들을 모은다.
    반환: [{"section": str, "text": str}, ...]
    """
    lines = raw.splitlines()
    blocks: List[Dict] = []
    cur_section = ""           # 현재 섹션 헤더(H1은 문서제목이라 섹션에서 제외)
    buf: List[str] = []

    def flush():
        text = "\n".join(buf).strip()
        if text:
            blocks.append({"section": cur_section, "text": text})
        buf.clear()

    for ln in lines:
        m = re.match(r"^(#{2,6})\s+(.*)$", ln)  # H2~H6를 섹션 경계로
        if m:
            flush()
            cur_section = m.group(2).strip()
        else:
            buf.append(ln)
    flush()
    return blocks


def _merge_and_split(blocks: List[Dict]) -> List[Dict]:
    """
    ① 후처리: 너무 작은 청크는 다음 청크와 병합, 너무 큰 청크는 문단 경계로 분할.
    동일 섹션 안에서만 병합한다(맥락 헤더 일관성 유지).
    """
    out: List[Dict] = []
    carry = None  # 병합 대기 중인 작은 블록

    for blk in blocks:
        text = blk["text"]
        if carry is not None and carry["section"] == blk["section"]:
            text = carry["text"] + "\n\n" + text
            blk = {"section": blk["section"], "text": text}
            carry = None

        if len(blk["text"]) < config.MIN_CHUNK_CHARS:
            # 아직 작으면 다음 블록과 병합 시도
            if carry is None:
                carry = blk
            else:
                carry = {"section": blk["section"],
                         "text": carry["text"] + "\n\n" + blk["text"]}
            continue

        if len(blk["text"]) > config.MAX_CHUNK_CHARS:
            out.extend(_split_long(blk))
        else:
            out.append(blk)

    if carry is not None:  # 마지막 잔여(작아도) 보존
        out.append(carry)
    return out


def _split_long(blk: Dict) -> List[Dict]:
    """큰 블록을 문단(빈 줄) 경계로 MAX 이하가 되도록 분할."""
    paras = re.split(r"\n\s*\n", blk["text"])
    out, buf = [], ""
    for p in paras:
        if len(buf) + len(p) + 2 > config.MAX_CHUNK_CHARS and buf:
            out.append({"section": blk["section"], "text": buf.strip()})
            buf = p
        else:
            buf = (buf + "\n\n" + p) if buf else p
    if buf.strip():
        out.append({"section": blk["section"], "text": buf.strip()})
    return out


def _doc_title(raw: str, fallback: str) -> str:
    """마크다운 H1을 문서 제목으로. 없으면 파일명 fallback."""
    for ln in raw.splitlines():
        m = re.match(r"^#\s+(.*)$", ln)
        if m:
            # 이모지/장식 제거는 과하지 않게 — 앞뒤 공백만 정리.
            return m.group(1).strip()
    return fallback


# ─────────────────────── ②③ 맥락헤더 + 인덱싱 ───────────────────────

def build_chunks(concepts_dir: Path) -> List[Dict]:
    """
    모든 .md를 청크로 변환하고 ② 맥락 헤더를 부여한다.
    각 청크: {chunk_id, source, title, section, text, context_text}
      - text: 원문(생성 컨텍스트로 사용)
      - context_text: "[제목 > 섹션] " + text (임베딩/BM25 대상)
    """
    chunks: List[Dict] = []
    files = sorted(concepts_dir.glob("*.md"))
    for fp in files:
        raw = fp.read_text(encoding="utf-8")
        source = f"concepts/{fp.name}"
        title = _doc_title(raw, fp.stem)
        blocks = _merge_and_split(_split_markdown(raw))
        for i, blk in enumerate(blocks):
            section = blk["section"] or "(intro)"
            header = f"[{title} > {section}] "      # ② 맥락 헤더
            chunks.append({
                "chunk_id": f"{fp.stem}#{i}",
                "source": source,
                "title": title,
                "section": section,
                "text": blk["text"],
                "context_text": header + blk["text"],
            })
    return chunks


def _tokenize(text: str) -> List[str]:
    """
    BM25용 토크나이저(단순).
    영문/숫자와 한글을 **분리**해 추출한다. (예: "LoRA가" → "lora", "가")
    한글과 라틴을 한 문자클래스로 묶으면 "lora가"가 한 토큰이 되어
    영어 키워드 매칭이 깨지므로, 스크립트별로 따로 뽑는다.
    """
    return re.findall(r"[0-9a-z]+|[가-힣]+", text.lower())


def ingest() -> Dict:
    """전체 수집 실행 → 인덱스 dict 구성 후 pickle 저장."""
    print(f"[ingest] 코퍼스: {config.CONCEPTS_DIR}")
    chunks = build_chunks(config.CONCEPTS_DIR)
    print(f"[ingest] 청크 {len(chunks)}개 생성")

    # ③ Dense: 맥락텍스트 임베딩
    context_texts = [c["context_text"] for c in chunks]
    embeddings = embed_passages(context_texts)  # (N, D), 더미 폴백 가능
    print(f"[ingest] 임베딩 shape={embeddings.shape} "
          f"(더미={'예' if using_dummy() else '아니오'})")

    # ③ Sparse: BM25 토큰 코퍼스
    bm25_corpus = [_tokenize(t) for t in context_texts]

    index = {
        "chunks": chunks,
        "embeddings": embeddings.astype(np.float32),
        "bm25_corpus": bm25_corpus,
        "meta": {
            "embed_model": config.EMBED_MODEL,
            "dummy_embeddings": using_dummy(),
            "n_chunks": len(chunks),
        },
    }

    config.EVAL_DIR.mkdir(parents=True, exist_ok=True)
    with open(config.INDEX_PATH, "wb") as f:
        pickle.dump(index, f)
    print(f"[ingest] 인덱스 저장 → {config.INDEX_PATH}")
    return index


if __name__ == "__main__":
    ingest()
