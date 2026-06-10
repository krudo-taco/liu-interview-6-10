# 体检报告 RAG 问答助手 —— 线上实操（45 分钟）

## 背景

你刚加入一家健康管理公司的 AI 团队。团队基于 2015 年体检数据搭了一个体检报告问答助手的 MVP——一条最小化 RAG 链路：

```
CSV 体检数据 → 病人记录文本化(ingest) → 切块(chunker) → TF-IDF 检索(retriever) → LLM 回答(answer)
```

上线前夜跑评测，**全红**。写这条 pipeline 的同事已经联系不上了。数据来自多个采集/翻译环节合并，**未经质量控制**。

你的任务：**45 分钟内诊断并修复这条链路，让评测过线。**

## 任务流程

1. clone 本仓库，从 `main` 切出分支 `fix/<你的姓名拼音>`（例如 `fix/liuxingwei`）
2. 运行 `python eval.py` 复现失败（完全离线，不需要任何 API key）
3. 诊断并修复 `rag/` 目录下的缺陷，把评测修到 **≥ 8/10**（缺陷不止一个，难度有梯度；能到 10/10 是 strong signal）
4. push 你的分支回本仓库
5. 用仓库的 Issue 模板（「诊断报告」）开一个 Issue，**每个你发现的缺陷写一节根因分析**

## 规则

- ✅ **允许并鼓励使用任何 AI 工具**——Claude Code、Cursor、Copilot、任意 MCP / Skills。我们想看的就是你真实的工作流
- ✅ 允许查阅任何资料
- ❌ **禁止修改 `eval.py` 与 `data/` 目录**（面试官会对你的分支做 diff 校验，改动视为无效提交）
- ❌ 除 `rag/` 目录外不要改动其他文件
- 📝 Issue 里请如实记录排查路径，**包括你如何使用 AI 工具**（关键提示词、它哪里说对了、哪里说错了你是怎么发现的）

## 快速开始

```bash
git clone https://github.com/krudo-taco/liu-interview-6-10.git
cd liu-interview-6-10
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python eval.py
```

环境要求：Python 3.9+；核心依赖仅 pandas / numpy（openai 选装，见下）。

## 评测说明

`eval.py` 完全离线，使用两个确定性指标，每条用例**两项同时满足**才算 PASS：

| 指标 | 含义 |
|------|------|
| 检索命中 | 目标病人编号出现在召回的 chunk 文本中 |
| 事实覆盖 | 期望事实字符串全部出现在组装后的上下文（`build_context` 输出）中 |

通过线：10 条用例 **≥ 8 条 PASS**（exit code 0）。

## 可选加分（时间富余再做）

`rag/answer.py` 的 LLM 生成走 OpenAI 兼容接口，用你自己的 key 实际问答 1-2 个问题，把输出贴进 Issue：

```bash
export LLM_API_KEY=sk-xxx
export LLM_BASE_URL=https://api.deepseek.com    # 或其他 OpenAI 兼容端点，如
                                                # https://dashscope.aliyuncs.com/compatible-mode/v1
export LLM_MODEL=deepseek-chat                  # 或 qwen-plus / gpt-4o-mini 等
python -m rag.answer "P20150042 的血压是多少？"
```

## 建议时间分配

| 阶段 | 时间 | 内容 |
|------|------|------|
| 理解 | ~10 min | 跑通评测、读懂 pipeline 和数据形态 |
| 诊断+修复 | ~25 min | 顺着评测输出的线索定位缺陷并修复 |
| 交付 | ~10 min | push 分支 + 写诊断报告 Issue |

## 数据说明

`data/checkup_2015.csv` 为**完全合成**的体检数据（200 行），不包含任何真实病人信息。数据刻意模拟了真实多源采集/翻译管线的产物形态。
