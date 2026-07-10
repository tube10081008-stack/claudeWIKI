-- pgvector 운영 경로용 DDL (MODE="pgvector").
-- lite 모드(기본)에서는 불필요. 운영 전환 시 참고용 스텁.
--
-- 적용:  psql "$RAG_PG_DSN" -f schema.sql
-- 전제:  PostgreSQL + pgvector 확장 설치.

CREATE EXTENSION IF NOT EXISTS vector;

-- ④ 출처 태깅: 원문 문서 단위(provenance 루트).
CREATE TABLE IF NOT EXISTS documents (
    id          BIGSERIAL PRIMARY KEY,
    source      TEXT NOT NULL UNIQUE,   -- 예: 'concepts/finetuning-lora.md'
    title       TEXT NOT NULL,          -- 마크다운 H1 제목
    raw         TEXT NOT NULL,          -- 원문 전체(감사·재청킹용)
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ①②③ 청크: 시맨틱 청킹 + 맥락 헤더 + dense 임베딩.
CREATE TABLE IF NOT EXISTS chunks (
    id           BIGSERIAL PRIMARY KEY,
    document_id  BIGINT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index  INT  NOT NULL,         -- 문서 내 순서
    section      TEXT,                  -- 소속 섹션 헤더(맥락 보강용)
    text         TEXT NOT NULL,         -- 원문 청크(생성 컨텍스트로 사용)
    context_text TEXT NOT NULL,         -- "[제목 > 섹션] " + text (임베딩 대상)
    embedding    vector(768),           -- EMBED_DIM과 일치(multilingual-e5-base)
    UNIQUE (document_id, chunk_index)
);

-- ③ Dense 인덱스: 코사인 거리 ANN(HNSW). 차원/연산자 클래스 일치 필요.
CREATE INDEX IF NOT EXISTS idx_chunks_embedding
    ON chunks USING hnsw (embedding vector_cosine_ops);

-- ③ Sparse(키워드) 인덱스: PostgreSQL FTS를 BM25 대용으로.
--    (운영에서는 OpenSearch BM25 등 별도 축을 둘 수 있음.)
CREATE INDEX IF NOT EXISTS idx_chunks_fts
    ON chunks USING gin (to_tsvector('simple', text));

-- 출처 역추적 조회 가속.
CREATE INDEX IF NOT EXISTS idx_chunks_document ON chunks (document_id);

-- ─────────────────────────────────────────────────────────────────────
-- 검색 쿼리 스텁(참고). 실제 융합(RRF)은 애플리케이션(retrieve.py)에서 수행.
--
-- Dense top-k:
--   SELECT id, text, 1 - (embedding <=> :qvec) AS score
--   FROM chunks ORDER BY embedding <=> :qvec LIMIT :k;
--
-- Sparse top-k:
--   SELECT id, text, ts_rank(to_tsvector('simple', text),
--                            plainto_tsquery('simple', :q)) AS score
--   FROM chunks
--   WHERE to_tsvector('simple', text) @@ plainto_tsquery('simple', :q)
--   ORDER BY score DESC LIMIT :k;
-- ─────────────────────────────────────────────────────────────────────
