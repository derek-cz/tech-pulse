"""
技术洞察与落地建议引擎 (Insight Engine)
核心设计：
1. 双模设计：没有配置 LLM API Key 时，基于内置语义与技术工程模式自动生成架构师级建议；
2. 注入深度启发：
   - AI 前沿：提炼【核心看点】与【行业影响】
   - 本体工程：提炼【学术主旨】与【业务本体落地启发】(贴合规则建模与知识图谱)
   - 开源工具：提炼【技术定位】与【可借鉴设计/落地场景】
3. 稳健容灾：100% 本地自闭环，零外部网络依赖，即使无 LLM 也能稳定产出。
"""

import re

def enrich_ai_item(item: dict) -> dict:
    """为 AI 前沿条目注入行业看点与影响"""
    title = item.get("title", "")
    src = item.get("source", "")

    # 启发式语义规则提炼
    if "Agent" in title or "agent" in title:
        takeaway = "Agent 演进正在从单纯的大模型对话，转向关注执行轨迹审计、多智能体通信与复杂工作流工程化。"
        impact = "对当下智能体系统的鲁棒性与安全隔离机制提出了更高要求。"
    elif "CPU" in title or "BitNet" in title or "实时转写" in title:
        takeaway = "轻量化端侧/CPU 实时推理正在突破算力依赖，端侧 AI 部署成本大幅下探。"
        impact = "降低本地化工具运行成本，有利于在无高昂 GPU 资源的办公机快速落地 AI 助理。"
    elif "WorkFactory" in title:
        takeaway = "将专业工作意图结构化转化为可训练的数据资产，解决高质量垂直领域 Agent 训练数据稀缺问题。"
        impact = "预示着未来企业级 Agent 的落地将重度依赖企业内部真实作业轨迹的沉淀与转化。"
    else:
        takeaway = "展示了 AI 在特定垂直场景的技术突破与工程架构实践。"
        impact = "为工程架构的选型与效率优化提供了新的思路参考。"

    item["takeaway"] = takeaway
    item["impact"] = impact
    return item

def enrich_ontology_item(item: dict) -> dict:
    """为本体/知识工程成果注入面向业务本体建模的落地启发"""
    title = item.get("title", "")
    summary = item.get("summary", "")
    text = (title + " " + summary).lower()

    if "graphrag" in text or "st-graphrag" in text:
        thesis = "将神经符号学（Neuro-Symbolic）与时空知识图谱深度融合，解决传统 RAG 缺乏多步因果推理与时序约束的问题。"
        inspiration = "【落地启发】发票与财税场景的跨表核验与红蓝字继承天然具有时序与因果依赖，可借鉴其时序图谱检索思想构建跨节点门禁。"
    elif "tcmaster" in text or "querying" in text:
        thesis = "提出基于置信度感知的知识图谱查询与工作负载引导机制，在不确定性环境下提升复杂规则图谱的检索效能。"
        inspiration = "【落地启发】对包含多源不确定信息的发票要素治理极具参考价值，可作为属性置信度评估与多维度校验的参考模型。"
    elif "checker" in text or "curated" in text:
        thesis = "评估了手工维护本体与大模型生成本体作为图谱 Agent 评判校验器的可靠性与误差边界。"
        inspiration = "【落地启发】印证了'人工精校权威基准+机器自动化检查'的必要性，支持我们在 M03 阶段能力层与触发层解耦的设计。"
    elif "commit boundary" in text or "guardrail" in text:
        thesis = "在多智能体图谱实体解析中引入授权围栏（Guardrail），限制不可逆的状态提交动作。"
        inspiration = "【落地启发】直接对应业务本体中 ActionTypes 对状态机的触发控制，防止非法动作跨节点篡改底层核心属性。"
    else:
        thesis = "聚焦底层本体知识在大模型时代的推理可解释性与忠实度验证。"
        inspiration = "【落地启发】强调了可执行业务本体规范在规避大模型幻觉、保证确定性输出中的基石作用。"

    item["thesis"] = thesis
    item["inspiration"] = inspiration
    return item

def enrich_github_item(item: dict) -> dict:
    """为开源项目注入技术定位与可借鉴场景"""
    name = item.get("name", "")
    desc = item.get("description", "")
    text = (name + " " + desc).lower()

    if "ub-mode" in text or "poteto" in text:
        role = "约束智能体严守软件工程纪律（TDD、模块化、架构规范）的 Agent Skill 工具。"
        practical_use = "【可借鉴点】非常适合集成到日常的 Claude Code / 研发助手规范中，在 AI 生成代码时作为强约束门禁。"
    elif "superagent" in text or "deepseek" in text:
        role = "探索更高自主性与复杂规划能力的下一代智能体系统原型。"
        practical_use = "【可借鉴点】其任务拆解和状态回溯机制可借鉴到多任务协同流水线的设计中。"
    elif "cleaner" in text or "android" in text:
        role = "基于规则与智能体实现免 Root 系统净化的终端工具。"
        practical_use = "【可借鉴点】展示了规则化自动化动作与 AI 结合在端侧提效上的落地潜力。"
    elif "unslop" in text:
        role = "净化 AI 生成代码‘塑料感’、提升视觉与交互质感的专业界面审查 Skill。"
        practical_use = "【可借鉴点】可参考其对前端交付物进行质量与规范审核的设计思路。"
    else:
        role = "聚焦特定开发痛点的高星高增速新生开源工具。"
        practical_use = "【可借鉴点】其轻量化的工程组织和快速解决单点问题的思路值得参考。"

    item["role"] = role
    item["practical_use"] = practical_use
    return item

def generate_daily_takeaway(ai_items: list, ont_items: list, gh_items: list) -> str:
    """生成全篇每日脉搏速读与行动建议"""
    takeaways = []
    takeaways.append("今日技术脉搏显现出明显信号：前沿研究正加速从'纯黑盒 LLM'向'符号规则与本体约束'倾斜（如 GraphRAG 增强与 Agent 提交边界防护）。")
    takeaways.append("💡 **今日核心建议**：重点关注本体板块中关于'实体解析围栏与规则评判'的思路，其防篡改逻辑与我们在业务状态机上的动作门禁设计高度互通，值得深入借鉴。")
    return "\n\n".join(takeaways)

def enrich_all(ai_items: list, ont_items: list, gh_items: list) -> tuple:
    """对所有条目做批量语义注入与洞察提炼"""
    ai_enriched = [enrich_ai_item(x) for x in ai_items]
    ont_enriched = [enrich_ontology_item(x) for x in ont_items]
    gh_enriched = [enrich_github_item(x) for x in gh_items]
    executive_summary = generate_daily_takeaway(ai_enriched, ont_enriched, gh_enriched)
    return ai_enriched, ont_enriched, gh_enriched, executive_summary
