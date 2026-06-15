# RAG (Retrieval-Augmented Generation)

**한 줄 정의:** 외부에서 정보를 찾아와(Retrieval), 그 내용으로 능력을 강화해(Augmented), 답변을 만든다(Generation).

## 구성 요소
- **Retrieval (찾아오기):** 외부 문서/DB에서 질문 관련 내용을 직접 검색.
- **Augmented (보충하기):** 찾은 근거를 AI의 원래 능력에 덧붙여 강화.
- **Generation (답변 만들기):** 위 정보를 바탕으로 최종 답변 생성.

## 왜 필요한가
- 일반 LLM은 **클로즈북 시험**처럼 외부 지식을 못 가져와 [할루시네이션](./hallucination.md)이 발생.
- RAG는 외부 지식([논파라메트릭 메모리](./memory-types.md))을 결합해 이를 완화한 **첫 시도**.

## 출처
- Lewis et al., 2020 (Facebook AI Research + NYU/UCL)
- *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
- arXiv: https://arxiv.org/pdf/2005.11401

## 관련 개념
[인코더 & 벡터](./encoder-vector.md) · [MIPS](./mips.md) · [메모리 종류](./memory-types.md)
