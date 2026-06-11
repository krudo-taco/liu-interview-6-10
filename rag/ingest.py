"""读取体检 CSV，把每个病人的一行记录拼成一段医学文本。"""
import pandas as pd


def load_documents(csv_path: str) -> list[str]:
    df = pd.read_csv(csv_path, dtype=str)
    # 采集/翻译管线偶尔会产生重复列（pandas 读入后带 .1 后缀）
    # 合并重复列的信息（如心率=心律齐，心率.1=58 → 心率=心律齐(58次/分)）
    for col in df.columns:
        if col.endswith('.1'):
            base_col = col[:-2]
            if base_col in df.columns:
                # 合并两列信息：原列信息 + (.1列数值 + 单位)
                df[base_col] = df.apply(
                    lambda row: f"{row[base_col]}（{row[col]}次/分）"
                    if pd.notna(row[base_col]) and pd.notna(row[col]) and row[base_col]
                    else row[base_col] if pd.notna(row[base_col])
                    else row[col],
                    axis=1
                )
    df = df.drop(columns=[c for c in df.columns if c.endswith('.1')])

    # 数据归一化：将各种"未测量"表示统一为"未测"
    unmeasured_keywords = ['弃检', '放弃', '未检', '/', '不愿检', '未测']
    df = df.replace(unmeasured_keywords, '未测')

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
