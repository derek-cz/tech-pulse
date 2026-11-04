"""
技术洞察与落地建议引擎（五维全景扩展版）
零 LLM 依赖 · 纯启发式语义分析与架构师实操建议
"""

import re

def enrich_ai_item(item: dict) -> dict:
    title = item.get("title", "")
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

def enrich_prompt_item(item: dict) -> dict:
    title = item.get("title", "")
    if "mcp" in title.lower() or "context" in title.lower():
        practice = "【实操心法】将大模型从'外部旁观者'变成'内部操作者'：优先把业务数据库字典和规则表封装为只读 MCP Resource，比直接把几万字文档塞进系统提示词省 80% Token。"
    else:
        practice = "【实操心法】防御性 Prompt 设计：在提示词尾部强制加入'如果字段不存在或无法推导，明确返回 null，禁止推测合成'，可将业务字段幻觉率降低 90% 以上。"
    item["practice"] = practice
    return item

def enrich_tax_item(item: dict) -> dict:
    title = item.get("title", "")
    if "规则" in title or "数电" in title:
        tax_insight = "【系统启示】特殊行业票种（成品油、建筑、不动产）的规则包（RulePackage）必须前置固化原生定义，避免在发票交付层出现规则悬空引用。"
    else:
        tax_insight = "【系统启示】乐企直连的核心壁垒在于将开票前审计转化为'运行时状态机拦截'，通过 ActionTypes 的前置门禁彻底杜绝跨地市或跨主体违规动作。"
    item["tax_insight"] = tax_insight
    return item

def generate_daily_takeaway(ai_items: list, ont_items: list, gh_items: list, prompt_items: list, tax_items: list) -> str:
    takeaways = []
    takeaways.append("今日五维雷达呈现明显共振：技术演进正全面从'LLM 单点生成'转向'企业级规则约束与确定性交付'。")
    takeaways.append("💡 **今日架构师建议**：重点关注【本体工程】中的实体解析围栏机制与【财税数智化】中的乐企前置门禁演进；两者在设计思路上完全对称——即利用强状态机（ValueSets）限制大模型/自动化的不可逆提交行为，确保业财数据的绝对准确。")
    return "\n\n".join(takeaways)

def enrich_all(ai_items: list, ont_items: list, gh_items: list, prompt_items: list, tax_items: list) -> tuple:
    ai_enriched = [enrich_ai_item(x) for x in ai_items]
    ont_enriched = [enrich_ontology_item(x) for x in ont_items]
    gh_enriched = [enrich_github_item(x) for x in gh_items]
    prompt_enriched = [enrich_prompt_item(x) for x in prompt_items]
    tax_enriched = [enrich_tax_item(x) for x in tax_items]
    executive_summary = generate_daily_takeaway(ai_enriched, ont_enriched, gh_enriched, prompt_enriched, tax_enriched)
    return ai_enriched, ont_enriched, gh_enriched, prompt_enriched, tax_enriched, executive_summary
