#!/usr/bin/env python3
"""离线评测：检索命中 + 上下文事实覆盖。不调用任何 LLM，不需要 API key。

⚠️ 本文件与 data/ 目录禁止修改（面试官会 diff 校验）。只允许修改 rag/ 下的代码。

判定规则（每条用例需同时满足两项才算 PASS）：
  - 检索命中：expected_row_ids 中至少一个病人编号出现在召回的 chunk 文本里
  - 事实覆盖：expected_facts 的全部字符串出现在 build_context() 组装的上下文里

通过线：10 条用例 ≥8 条 PASS（exit code 0）。
"""
import json
import sys

from rag.answer import build_context
from rag.chunker import chunk_documents
from rag.ingest import load_documents
from rag.retriever import Retriever

CSV_PATH = "data/checkup_2015.csv"
CASES_PATH = "data/eval_cases.jsonl"
PASS_LINE = 8
TOP_K = 3


def main() -> None:
    docs = load_documents(CSV_PATH)
    chunks = chunk_documents(docs)
    retriever = Retriever(chunks)

    with open(CASES_PATH, encoding="utf-8") as f:
        cases = [json.loads(line) for line in f if line.strip()]

    passed = 0
    for case in cases:
        retrieved = retriever.search(case["question"], top_k=TOP_K)
        context = build_context(retrieved)

        hit = any(rid in chunk for rid in case["expected_row_ids"] for chunk in retrieved)
        facts_ok = all(fact in context for fact in case["expected_facts"])
        ok = hit and facts_ok
        passed += ok

        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] case{case['id']:02d}  检索命中={'✓' if hit else '✗'}  "
              f"事实覆盖={'✓' if facts_ok else '✗'}  | {case['question']}")
        if not ok:
            print(f"       期望病人: {case['expected_row_ids']}  期望事实: {case['expected_facts']}")
            for j, chunk in enumerate(retrieved, 1):
                preview = chunk[:90].replace("\n", " ")
                print(f"       召回#{j}: {preview}…")

    print(f"\n得分: {passed}/{len(cases)}（通过线 ≥{PASS_LINE}）")
    sys.exit(0 if passed >= PASS_LINE else 1)


if __name__ == "__main__":
    main()
