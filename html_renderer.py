"""
HTML 生成器（五维全景研报版）：支持顶部快捷导航、架构师速读、Prompt心法与财税前沿
"""

import os
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>技术脉搏每日全景研报 · {date_str}</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #0f172a;
      --muted: #64748b;
      --border: #e2e8f0;
      --primary: #2563eb;
      --primary-light: #eff6ff;
      --accent: #0ea5e9;
      --summary-bg: #f0fdf4;
      --summary-border: #bbf7d0;
      --summary-text: #166534;
      --tag-ai: #dbeafe;
      --tag-ai-text: #1d4ed8;
      --tag-ont: #f3e8ff;
      --tag-ont-text: #7e22ce;
      --tag-gh: #dcfce7;
      --tag-gh-text: #15803d;
      --tag-prompt: #fef3c7;
      --tag-prompt-text: #b45309;
      --tag-tax: #e0e7ff;
      --tag-tax-text: #4338ca;
      --insight-bg: #f8fafc;
      --insight-border: #e2e8f0;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #090d16;
        --card-bg: #131b2e;
        --text: #f1f5f9;
        --muted: #94a3b8;
        --border: #1e293b;
        --primary: #3b82f6;
        --primary-light: #1e293b;
        --accent: #38bdf8;
        --summary-bg: #064e3b22;
        --summary-border: #047857;
        --summary-text: #6ee7b7;
        --tag-ai: #1e293b;
        --tag-ai-text: #60a5fa;
        --tag-ont: #2e1065;
        --tag-ont-text: #c084fc;
        --tag-gh: #064e3b;
        --tag-gh-text: #4ade80;
        --tag-prompt: #451a03;
        --tag-prompt-text: #fcd34d;
        --tag-tax: #1e1b4b;
        --tag-tax-text: #a5b4fc;
        --insight-bg: #0d1527;
        --insight-border: #1e293b;
      }}
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 32px 16px;
    }}
    .container {{
      max-width: 980px;
      margin: 0 auto;
    }}
    header {{
      margin-bottom: 24px;
    }}
    .header-badge {{
      display: inline-block;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 4px 10px;
      border-radius: 9999px;
      background: var(--primary-light);
      color: var(--primary);
      margin-bottom: 12px;
    }}
    h1 {{
      font-size: 32px;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}
    .meta {{
      color: var(--muted);
      font-size: 14px;
      margin-bottom: 20px;
    }}
    .nav-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }}
    .nav-item {{
      font-size: 13px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 8px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text);
      text-decoration: none;
      transition: all 0.2s;
    }}
    .nav-item:hover {{
      border-color: var(--primary);
      color: var(--primary);
    }}
    .summary-card {{
      background: var(--summary-bg);
      border: 1px solid var(--summary-border);
      border-radius: 12px;
      padding: 18px 22px;
      margin-bottom: 32px;
      font-size: 14px;
      line-height: 1.7;
      color: var(--text);
    }}
    .summary-title {{
      font-weight: 700;
      color: var(--summary-text);
      margin-bottom: 8px;
      font-size: 15px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .section-title {{
      font-size: 20px;
      font-weight: 700;
      margin: 36px 0 18px 0;
      display: flex;
      align-items: center;
      gap: 8px;
      scroll-margin-top: 20px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 18px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 22px;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .card:hover {{
      border-color: var(--primary);
      box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    }}
    .card-top {{
      margin-bottom: 14px;
    }}
    .badge {{
      display: inline-block;
      font-size: 12px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 6px;
      margin-bottom: 8px;
    }}
    .badge-ai {{ background: var(--tag-ai); color: var(--tag-ai-text); }}
    .badge-ont {{ background: var(--tag-ont); color: var(--tag-ont-text); }}
    .badge-gh {{ background: var(--tag-gh); color: var(--tag-gh-text); }}
    .badge-prompt {{ background: var(--tag-prompt); color: var(--tag-prompt-text); }}
    .badge-tax {{ background: var(--tag-tax); color: var(--tag-tax-text); }}
    .card-title {{
      font-size: 17px;
      font-weight: 700;
      color: var(--text);
      text-decoration: none;
      line-height: 1.4;
      display: block;
      margin-bottom: 10px;
    }}
    .card-title:hover {{
      color: var(--primary);
    }}
    .card-desc {{
      font-size: 14px;
      color: var(--muted);
      margin-bottom: 14px;
      line-height: 1.6;
    }}
    .insight-box {{
      background: var(--insight-bg);
      border-left: 3px solid var(--primary);
      padding: 10px 14px;
      border-radius: 0 8px 8px 0;
      font-size: 13px;
      margin-top: 8px;
      margin-bottom: 14px;
      line-height: 1.6;
    }}
    .insight-line {{
      margin-bottom: 4px;
    }}
    .insight-line:last-child {{
      margin-bottom: 0;
    }}
    .insight-label {{
      font-weight: 600;
      margin-right: 4px;
    }}
    .card-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: var(--muted);
      border-top: 1px solid var(--border);
      padding-top: 12px;
      margin-top: auto;
    }}
    .btn {{
      font-size: 12px;
      font-weight: 600;
      color: var(--primary);
      text-decoration: none;
    }}
    footer {{
      margin-top: 60px;
      padding-top: 24px;
      border-top: 1px solid var(--border);
      text-align: center;
      font-size: 13px;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="header-badge">Daily Tech Intelligence · 5D Edition</div>
      <h1>技术脉搏每日全景研报</h1>
      <div class="meta">更新时间：{date_str} · 五维自动化雷达 · 架构师落地实战提炼</div>

      <!-- 快捷导航 -->
      <div class="nav-bar">
        <a href="#sec-ai" class="nav-item">🔥 AI 产业前沿</a>
        <a href="#sec-ont" class="nav-item">🧩 本体论与知识工程</a>
        <a href="#sec-gh" class="nav-item">🛠️ 爆发开源工具</a>
        <a href="#sec-prompt" class="nav-item">💡 Prompt & Agent实操</a>
        <a href="#sec-tax" class="nav-item">📊 财税数智化与企业级演进</a>
      </div>

      <!-- 每日宏观速读与建议 -->
      <div class="summary-card">
        <div class="summary-title">📌 今日脉搏全景速读与架构师建议</div>
        <div>{executive_summary}</div>
      </div>
    </header>

    <!-- 1. AI 前沿 -->
    <div id="sec-ai" class="section-title">🔥 1. AI 战略与产业前沿</div>
    <div class="grid">
      {ai_cards}
    </div>

    <!-- 2. 本体与知识工程 -->
    <div id="sec-ont" class="section-title">🧩 2. 本体论与知识工程深潜</div>
    <div class="grid">
      {ontology_cards}
    </div>

    <!-- 3. GitHub 增长工具 -->
    <div id="sec-gh" class="section-title">🛠️ 3. 智能体与开发者爆发新工具</div>
    <div class="grid">
      {github_cards}
    </div>

    <!-- 4. Prompt 与 Agent 实战 -->
    <div id="sec-prompt" class="section-title">💡 4. 提示词工程与 Agent 实战技巧</div>
    <div class="grid">
      {prompt_cards}
    </div>

    <!-- 5. 财税数智化与企业应用 -->
    <div id="sec-tax" class="section-title">📊 5. 财税数智化与企业级应用演进</div>
    <div class="grid">
      {tax_cards}
    </div>

    <footer>
      <p>由 Tech-Pulse 五维全景引擎生成 · 自动沉淀于 05-助手 知识库</p>
    </footer>
  </div>
</body>
</html>
"""

def render_html(ai_items: list, ontology_items: list, gh_items: list, prompt_items: list, tax_items: list, date_str: str, output_path: str, executive_summary: str = ""):
    # 1. 渲染 AI 卡片
    ai_cards = ""
    for item in ai_items:
        src = item.get("source", "Web")
        region = item.get("region", "")
        region_tag = f"<span class='badge' style='background: #fee2e2; color: #991b1b; margin-right: 4px;'>{region}</span>" if region else ""

        takeaway_block = ""
        if item.get("takeaway"):
            takeaway_block = f"""
            <div class="insight-box">
              <div class="insight-line"><span class="insight-label" style="color: var(--primary);">💡 核心看点:</span>{item['takeaway']}</div>
              <div class="insight-line"><span class="insight-label" style="color: var(--primary);">🎯 行业影响:</span>{item.get('impact', '')}</div>
            </div>
            """

        ai_cards += f"""
        <div class="card">
          <div class="card-top">
            <div>{region_tag}<span class="badge badge-ai">{src}</span></div>
            <a href="{item['link']}" target="_blank" class="card-title">{item['title']}</a>
            {takeaway_block}
          </div>
          <div class="card-footer">
            <span>关注度: {item.get('points', 0)} · 日期: {item.get('date', '')}</span>
            <a href="{item['link']}" target="_blank" class="btn">阅读原文 &rarr;</a>
          </div>
        </div>
        """

    # 2. 渲染本体论文卡片
    ont_cards = ""
    for item in ontology_items:
        authors = ", ".join(item.get("authors", []))
        region = item.get("region", "")
        region_tag = f"<span class='badge' style='background: #fee2e2; color: #991b1b; margin-right: 4px;'>{region}</span>" if region else ""

        insight_block = ""
        if item.get("thesis"):
            insight_block = f"""
            <div class="insight-box" style="border-left-color: #9333ea;">
              <div class="insight-line"><span class="insight-label" style="color: #9333ea;">🔬 学术主旨:</span>{item['thesis']}</div>
              <div class="insight-line"><span class="insight-label" style="color: #9333ea;">💡 落地启发:</span>{item.get('inspiration', '')}</div>
            </div>
            """

        ont_cards += f"""
        <div class="card">
          <div class="card-top">
            <div>{region_tag}<span class="badge badge-ont">arXiv cs.AI / cs.LO</span></div>
            <a href="{item['link']}" target="_blank" class="card-title">{item['title']}</a>
            <div class="card-desc">{item.get('summary', '')}</div>
            {insight_block}
          </div>
          <div class="card-footer">
            <span>作者: {authors} ({item.get('published', '')})</span>
            <a href="{item['link']}" target="_blank" class="btn">论文直达 &rarr;</a>
          </div>
        </div>
        """

    # 3. 渲染 GitHub 卡片
    gh_cards = ""
    for item in gh_items:
        region = item.get("region", "")
        region_tag = f"<span class='badge' style='background: #fee2e2; color: #991b1b; margin-right: 4px;'>{region}</span>" if region else ""

        tool_insight_block = ""
        if item.get("role"):
            tool_insight_block = f"""
            <div class="insight-box" style="border-left-color: #16a34a;">
              <div class="insight-line"><span class="insight-label" style="color: #16a34a;">🛠️ 工具定位:</span>{item['role']}</div>
              <div class="insight-line"><span class="insight-label" style="color: #16a34a;">🎯 落地参考:</span>{item.get('practical_use', '')}</div>
            </div>
            """

        gh_cards += f"""
        <div class="card">
          <div class="card-top">
            <div>{region_tag}<span class="badge badge-gh">⭐ {item.get('stars', 0)} · {item.get('language', 'General')}</span></div>
            <a href="{item['link']}" target="_blank" class="card-title">{item['name']}</a>
            <div class="card-desc">{item.get('description', '')}</div>
            {tool_insight_block}
          </div>
          <div class="card-footer">
            <span>开源项目</span>
            <a href="{item['link']}" target="_blank" class="btn">GitHub 仓库 &rarr;</a>
          </div>
        </div>
        """

    # 4. 渲染 Prompt 与 Agent 技巧卡片
    prompt_cards = ""
    for item in prompt_items:
        prompt_cards += f"""
        <div class="card">
          <div class="card-top">
            <div><span class="badge badge-prompt">Prompt / MCP 最佳范式</span></div>
            <a href="{item.get('link', '#')}" target="_blank" class="card-title">{item['title']}</a>
            <div class="card-desc">{item.get('summary', '')}</div>
            <div class="insight-box" style="border-left-color: #d97706;">
              <div class="insight-line"><span class="insight-label" style="color: #d97706;">💡 实战心法:</span>{item.get('practice', '')}</div>
            </div>
          </div>
          <div class="card-footer">
            <span>工程规范与心法</span>
            <a href="{item.get('link', '#')}" target="_blank" class="btn">参考范式 &rarr;</a>
          </div>
        </div>
        """

    # 5. 渲染财税与企业数智化卡片
    tax_cards = ""
    for item in tax_items:
        tax_cards += f"""
        <div class="card">
          <div class="card-top">
            <div><span class="badge badge-tax">{item.get('tag', '财税数智化')}</span></div>
            <a href="{item.get('link', '#')}" target="_blank" class="card-title">{item['title']}</a>
            <div class="card-desc">{item.get('summary', '')}</div>
            <div class="insight-box" style="border-left-color: #4f46e5;">
              <div class="insight-line"><span class="insight-label" style="color: #4f46e5;">🎯 业财系统启示:</span>{item.get('tax_insight', '')}</div>
            </div>
          </div>
          <div class="card-footer">
            <span>行业与系统演进</span>
            <a href="{item.get('link', '#')}" target="_blank" class="btn">行业溯源 &rarr;</a>
          </div>
        </div>
        """

    html_content = HTML_TEMPLATE.format(
        date_str=date_str,
        executive_summary=executive_summary.replace("\n", "<br>"),
        ai_cards=ai_cards,
        ontology_cards=ont_cards,
        github_cards=gh_cards,
        prompt_cards=prompt_cards,
        tax_cards=tax_cards
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return output_path
