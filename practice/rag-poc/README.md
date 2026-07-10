# 🔎 RAG PoC — 성숙한 파일링 시스템 실행본 (RAGAS-주도)

> [성숙한 RAG 설계도](../../concepts/mature-rag-blueprint.md)의 **실행 가능한 최소 구현**.
> **코퍼스:** 이 위키의 `concepts/*.md` (자기 위키를 RAG로 질문 = dogfooding).
> **목표:** 하이브리드 검색 + 재랭킹 + 인용 생성 + Self/CRAG 폴백 + **RAGAS 평가 게이트**.

```
rag-poc/
├── README.md
├── requirements.txt
├── config.py              # 경로·모델·임계값
├── schema.sql             # pgvector 운영용 DDL (lite 모드는 불필요)
├── src/
│   ├── ingest.py          # ① 청킹 + ② 맥락헤더 + ③ 임베딩/BM25 인덱싱
│   ├── retrieve.py        # ⑦ 하이브리드(Dense+BM25, RRF) + ⑧ 재랭킹
│   ├── generate.py        # ⑩ 인용강제 생성 + 무근거 폴백
│   ├── selfrag.py         # ⑪ 관련성 평가 + CRAG-lite 폴백 판단
│   └── pipeline.py        # ⑤ 라우팅 → 전체 질의 파이프라인
└── eval/
    ├── golden_set.jsonl   # 평가셋 (question/ground_truth/evidence/type)
    └── evaluate.py        # RAGAS 4지표 + CI 임계 게이트
```

## ▶ 실행
```bash
cd practice/rag-poc
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python src/ingest.py            # concepts/*.md 인덱싱 (기본: lite 인메모리)
python src/pipeline.py "LoRA가 뭐야?"   # 단일 질의 → 인용 포함 답변
python eval/evaluate.py         # 골든셋으로 RAGAS 평가 + 임계 게이트
```

## 모드
- **lite (기본):** 인메모리(numpy 코사인 + rank_bm25) — DB 없이 바로 실행.
- **prod:** `schema.sql`로 pgvector 구성 후 `config.py`에서 `MODE="pgvector"`.

## RAGAS 게이트 (eval/evaluate.py)
| 지표 | 임계 |
|---|---|
| faithfulness | ≥ 0.90 |
| answer_relevancy | ≥ 0.85 |
| context_precision | ≥ 0.80 |
| context_recall | ≥ 0.85 |
> 미달 시 **exit code 1** (CI 머지 차단용).

## 골든셋 스키마 (`eval/golden_set.jsonl`, 1줄 1 JSON)
```json
{"question":"LoRA가 뭐야?","ground_truth":"전체가 아닌 끝의 작은 행렬만 학습하는 저비용 파인튜닝","evidence":[{"source":"concepts/finetuning-lora.md","snippet":"끝의 작은 행렬만 바꿈 → 전체의 약 0.29%만 학습"}],"type":"simple"}
```
- `type`: simple / multihop / relational / refusal(자료에 없음) / adversarial

> ⚠️ PoC 단순화: 생성 LLM은 `config.py`의 provider 설정(미설정 시 stub). 운영 전환 시 인증·캐싱·관측 추가.
