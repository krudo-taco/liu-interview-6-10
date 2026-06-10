"""读取体检 CSV，把每个病人的一行记录拼成一段医学文本。"""
import pandas as pd


def load_documents(csv_path: str) -> list[str]:
    df = pd.read_csv(csv_path, dtype=str)
    # 采集/翻译管线偶尔会产生重复列（pandas 读入后带 .1 后缀），统一去重
    df = df.drop(columns=[c for c in df.columns if c.endswith(".1")])

    docs = []
    for _, row in df.iterrows():
        parts = [f"【病人{row['编号']}】"]
        for col in df.columns:
            if col == "编号":
                continue
            val = str(row[col]).strip() if pd.notna(row[col]) else ""
            if not val:
                continue
            parts.append(f"{col}：{val}")
        docs.append("，".join(parts))
    return docs
