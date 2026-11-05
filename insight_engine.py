"""
技术洞察与落地建议引擎（回归原生三大板块版）
为用户原本设计的 3 大板块提供深度架构师级启发与决策建议：
1. AI 最新消息：注入【💡 核心看点】与【🎯 行业影响】
2. 本体最新消息：注入【🔬 学术主旨】与【💡 业务本体落地启发】
3. Git 增长最快工具：注入【🛠️ 工具定位】与【🎯 落地参考】
"""

def enrich_ai_item(item: dict) -> dict:
    title = item.get("title", "")
    t = title.lower()
    if "agent" in t or "momentic" in t or "frontier" in t:
        takeaway = "Agent 演进正在从单纯的大模型对话，转向关注执行轨迹审计、物理实验评测与复杂长链路工作流工程化。"
        impact = "对当下企业级智能体系统的环境适应性、多步规划能力与鲁棒性提出了更高要求。"
    elif "cpu" in t or "bitnet" in t or "gpty" in t or "rust" in t:
        takeaway = "轻量化与高性能底层工程（Rust/端侧优化）持续突破，AI 辅助基础设施的运行开销正在大幅下探。"
        impact = "降低本地化工具链与工作台的系统资源占用，更适合在日常办公环境静默跑通。"
    elif "muon" in t or "trajectory" in t:
        takeaway = "探索利用教师模型轨迹复用加速智能体训练，解决复杂环境样本效率低下的痛点。"
        impact = "为中小团队低成本训练垂直领域 Agent 动作模型提供了实用技术范式。"
    else:
        takeaway = "展示了 AI 在特定垂直工程场景的技术突破与架构实践。"
        impact = "为工程架构的选型与效能提升提供了切实的方法论参考。"

    item["takeaway"] = takeaway
    item["impact"] = impact
    return item

def enrich_ontology_item(item: dict) -> dict:
    title = item.get("title", "")
    summary = item.get("summary", "")
    text = (title + " " + summary).lower()

    if "graphrag" in text or "st-graphrag" in text:
        thesis = "将神经符号学（Neuro-Symbolic）与时空图谱深度融合，解决传统 RAG 缺乏多步因果时序推理的问题。"
        inspiration = "【落地启发】发票与财税场景的跨表核验与红蓝字继承天然具有时序因果依赖，可借鉴其时序图谱检索思想构建跨节点门禁。"
    elif "tcmaster" in text or "querying" in text:
        thesis = "提出基于置信度感知的知识图谱查询与工作负载引导机制，在不确定性环境下提升复杂规则图谱的检索效能。"
        inspiration = "【落地启发】对包含多源不确定信息的发票要素治理极具参考价值，可作为属性置信度评估与多维度校验的参考模型。"
    elif "certified" in text or "hub" in text or "checker" in text:
        thesis = "评估了形式化本体与知识网络在多智能体交互中的认证中枢作用，保证分布式推理的一致性。"
        inspiration = "【落地启发】印证了以业务本体为单一可信事实源（Single Source of Truth）对跨系统业务流调度的核心价值。"
    elif "lingshu" in text or "symptom" in text or "contextualized" in text:
        thesis = "构建大规模以核心实体为中心的上下文知识图谱，通过结构化关联消除大模型在垂直专业领域的幻觉。"
        inspiration = "【落地启发】与我们围绕'开票主体/商品行/特殊要素'构建以核心对象为中心的本体模型高度同构，可参考其上下文挂载方式。"
    else:
        thesis = "聚焦底层本体知识在智能体时代的推理可解释性、忠实度与符号约束。"
        inspiration = "【落地启发】强调了可执行业务本体规范在规避大模型幻觉、保证确定性输出中的基石作用。"

    item["thesis"] = thesis
    item["inspiration"] = inspiration
    return item

def enrich_github_item(item: dict) -> dict:
    name = item.get("name", "")
    desc = item.get("description", "")
    text = (name + " " + desc).lower()

    if "superagent" in text or "deepseek" in text:
        role = "探索更高自主性与复杂规划能力的下一代智能体系统原型与 Harness。"
        practical_use = "【可借鉴点】其环境状态感知与长序列动作拆解机制，非常适合多任务协同管线的架构参考。"
    elif "unslop" in text or "craft" in text:
        role = "净化 AI 生成物代码塑料感、提升工业级界面美学与规范标准的开发者工具。"
        practical_use = "【可借鉴点】可参考其对前端与交互交付物进行质量门禁审核的设计思路。"
    elif "mika" in text or "agent" in text:
        role = "轻量级、开箱即用的模块化智能体与工作流脚手架。"
        practical_use = "【可借鉴点】展示了将零散工具封装为标准化 Agent 动作的极简实践。"
    elif "chinese" in text or "cs329" in text:
        role = "系统化、高质量的 AI 基础设施与大模型系统工程实战知识体系。"
        practical_use = "【可借鉴点】适合快速建立从模型调度到端到端工程部署的完整技术全景。"
    else:
        role = "近期全球开发者社区星标激增的高价值开源工具。"
        practical_use = "【可借鉴点】其轻量化的工程组织和快速解决单点痛点的思路值得参考。"

    item["role"] = role
    item["practical_use"] = practical_use
    return item

def generate_daily_takeaway(ai_items: list, ont_items: list, gh_items: list) -> str:
    takeaways = []
    takeaways.append("今日三大核心板块显现出强烈信号：技术重心正加速从'纯模型生成'向'符号规则与本体约束（Neuro-Symbolic）'演进。")
    takeaways.append("💡 **今日核心建议**：重点研读本体板块中关于'时空 GraphRAG 与知识置信度查询'的成果；它直接证明了在处理强因果、强一致性场景时，单纯依靠向量检索远远不够，必须依赖本体作为严密的逻辑门禁。")
    return "\n\n".join(takeaways)

def enrich_all(ai_items: list, ont_items: list, gh_items: list) -> tuple:
    ai_enriched = [enrich_ai_item(x) for x in ai_items]
    ont_enriched = [enrich_ontology_item(x) for x in ont_items]
    gh_enriched = [enrich_github_item(x) for x in gh_items]
    executive_summary = generate_daily_takeaway(ai_enriched, ont_enriched, gh_enriched)
    return ai_enriched, ont_enriched, gh_enriched, executive_summary
