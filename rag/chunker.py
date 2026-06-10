"""把文档切成检索块。"""

CHUNK_SIZE = 200


def chunk_documents(docs: list[str]) -> list[str]:
    chunks = []
    for doc in docs:
        # 统一定长切块，控制每块大小，方便后续向量化扩展
        for i in range(0, len(doc), CHUNK_SIZE):
            chunks.append(doc[i:i + CHUNK_SIZE])
    return chunks
