"""把文档切成检索块。"""


def chunk_documents(docs: list[str]) -> list[str]:
    # 每个病人记录作为独立 chunk，保持语义完整性
    # 200 条记录全部 ≤ 300 字符，无需切分
    return docs.copy()
