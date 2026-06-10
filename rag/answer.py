"""组装上下文并调用 LLM 生成回答。

eval.py 只评测 build_context（完全离线）；generate_answer 走 OpenAI 兼容接口，
用你自己的 key：LLM_API_KEY / LLM_BASE_URL / LLM_MODEL。
"""
import os
import sys

MAX_CONTEXT_CHARS = 300  # 控制 prompt 长度，节省 token

PROMPT_TEMPLATE = """你是一名体检报告助手。请仅根据下面的体检记录回答问题，不要编造。

[体检记录]
{context}

[问题]
{question}

请用中文简洁回答，并引用记录里的具体数值。"""


def build_context(chunks: list[str]) -> str:
    # 把最相关的块放到最后（更靠近问题的位置），有利于模型注意力
    ordered = list(reversed(chunks))
    context = "\n".join(ordered)
    return context[:MAX_CONTEXT_CHARS]


def generate_answer(question: str, chunks: list[str]) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        raise SystemExit("缺少 openai 包：pip install openai")
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        raise SystemExit("请先设置环境变量 LLM_API_KEY（OpenAI 兼容接口的 key）")
    client = OpenAI(
        api_key=api_key,
        base_url=os.environ.get("LLM_BASE_URL", "https://api.deepseek.com"),
    )
    resp = client.chat.completions.create(
        model=os.environ.get("LLM_MODEL", "deepseek-chat"),
        messages=[{
            "role": "user",
            "content": PROMPT_TEMPLATE.format(context=build_context(chunks), question=question),
        }],
        temperature=0,
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    from rag.chunker import chunk_documents
    from rag.ingest import load_documents
    from rag.retriever import Retriever

    if len(sys.argv) < 2:
        raise SystemExit('用法: python -m rag.answer "P20150042 的血压是多少？"')
    question = sys.argv[1]
    retriever = Retriever(chunk_documents(load_documents("data/checkup_2015.csv")))
    print(generate_answer(question, retriever.search(question, top_k=3)))
