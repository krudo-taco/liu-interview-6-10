"""轻量级 TF-IDF 检索器（本地实现，无需向量数据库）。

分词策略：连续字母数字串作为整 token（病人编号、数值），中文按单字 + 相邻双字组合。
"""
import math
import re
from collections import Counter


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[A-Za-z0-9]+", text)
    han = re.findall(r"[一-鿿]", text)
    tokens.extend(han)
    tokens.extend(a + b for a, b in zip(han, han[1:]))
    return tokens


class Retriever:
    def __init__(self, chunks: list[str]):
        self.chunks = chunks
        self.doc_tokens = [Counter(tokenize(c)) for c in chunks]
        self.df = Counter()
        for tokens in self.doc_tokens:
            self.df.update(tokens.keys())
        self.n_docs = len(chunks)

    def search(self, query: str, top_k: int = 3) -> list[str]:
        q_tokens = tokenize(query)
        scored = []
        for idx, tokens in enumerate(self.doc_tokens):
            score = 0.0
            for t in q_tokens:
                if t in tokens:
                    tf = 1 + math.log(tokens[t])
                    idf = math.log(self.n_docs / (1 + self.df[t]))
                    score += tf * idf
            scored.append((score, idx))
        scored.sort(reverse=True)  # 按相关度降序排序，取最前面的 top_k 个
        return [self.chunks[idx] for _, idx in scored[:top_k]]
