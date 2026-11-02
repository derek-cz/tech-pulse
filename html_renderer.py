"""
HTML 生成器：将抓取到的数据渲染为现代化响应式报纸/看板风格的 HTML 页面
"""

import os
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>技术雷达日报 · {date_str}</title>
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
      --tag-ai: #dbeafe;
      --tag-ai-text: #1d4ed8;
      --tag-ont: #f3e8ff;
      --tag-ont-text: #7e22ce;
      --tag-gh: #dcfce7;
      --tag-gh-text: #15803d;
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
        --tag-ai: #1e293b;
        --tag-ai-text: #60a5fa;
        --tag-ont: #2e1065;
        --tag-ont-text: #c084fc;
        --tag-gh: #064e3b;
        --tag-gh-text: #4ade80;
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
      max-width: 960px;
      margin: 0 auto;
    }}
    header {{
      margin-bottom: 36px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 24px;
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
    }}
    .section-title {{
      font-size: 20px;
      font-weight: 700;
      margin: 36px 0 18px 0;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
    }}
    @media (min-width: 640px) {{
      .grid-2 {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .card:hover {{
      border-color: var(--primary);
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
      transform: translateY(-2px);
    }}
    .card-top {{
      margin-bottom: 12px;
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
    .card-title {{
      font-size: 16px;
      font-weight: 600;
      color: var(--text);
      text-decoration: none;
      line-height: 1.4;
      display: block;
      margin-bottom: 8px;
    }}
    .card-title:hover {{
      color: var(--primary);
    }}
    .card-desc {{
      font-size: 14px;
      color: var(--muted);
      margin-bottom: 16px;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
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
      <div class="header-badge">Daily Intelligence Radar</div>
      <h1>技术雷达简报</h1>
      <div class="meta">更新时间：{date_str} · 自动化采集自 Hacker News / arXiv / GitHub</div>
    </header>

    <!-- 1. AI 前沿 -->
    <div class="section-title">🔥 1. AI 前沿动态</div>
    <div class="grid grid-2">
      {ai_cards}
    </div>

    <!-- 2. 本体与知识工程 -->
    <div class="section-title">🧩 2. 本体与知识工程前沿</div>
    <div class="grid">
      {ontology_cards}
    </div>

    <!-- 3. GitHub 增长工具 -->
    <div class="section-title">⚡ 3. GitHub 增长最快开源项目</div>
    <div class="grid grid-2">
      {github_cards}
    </div>

    <footer>
      <p>由 Tech-Radar 自动化引擎生成 · 数据沉淀于 05-助手 知识库</p>
    </footer>
  </div>
</body>
</html>
"""

def render_html(ai_items: list, ontology_items: list, gh_items: list, date_str: str, output_path: str):
    # 渲染 AI 卡片
    ai_cards = ""
    for item in ai_items:
        src = item.get("source", "Web")
        region = item.get("region", "")
        region_tag = f"<span class='badge' style='background: #fee2e2; color: #991b1b; margin-right: 4px;'>{region}</span>" if region else ""
        ai_cards += f"""
        <div class="card">
          <div class="card-top">
            <div>{region_tag}<span class="badge badge-ai">{src}</span></div>
            <a href="{item['link']}" target="_blank" class="card-title">{item['title']}</a>
          </div>
          <div class="card-footer">
            <span>关注度: {item.get('points', 0)}</span>
            <a href="{item['link']}" target="_blank" class="btn">阅读原文 &rarr;</a>
          </div>
        </div>
        """

    # 渲染本体论文卡片
    ont_cards = ""
    for item in ontology_items:
        authors = ", ".join(item.get("authors", []))
        ont_cards += f"""
        <div class="card">
          <div class="card-top">
            <span class="badge badge-ont">arXiv cs.AI / cs.LO</span>
            <a href="{item['link']}" target="_blank" class="card-title">{item['title']}</a>
            <div class="card-desc">{item.get('summary', '')}</div>
          </div>
          <div class="card-footer">
            <span>作者: {authors} ({item.get('published', '')})</span>
            <a href="{item['link']}" target="_blank" class="btn">论文直达 &rarr;</a>
          </div>
        </div>
        """

    # 渲染 GitHub 卡片
    gh_cards = ""
    for item in gh_items:
        region = item.get("region", "")
        region_tag = f"<span class='badge' style='background: #fee2e2; color: #991b1b; margin-right: 4px;'>{region}</span>" if region else ""
        gh_cards += f"""
        <div class="card">
          <div class="card-top">
            <div>{region_tag}<span class="badge badge-gh">⭐ {item.get('stars', 0)} · {item.get('language', 'General')}</span></div>
            <a href="{item['link']}" target="_blank" class="card-title">{item['name']}</a>
            <div class="card-desc">{item.get('description', '')}</div>
          </div>
          <div class="card-footer">
            <span>开源项目</span>
            <a href="{item['link']}" target="_blank" class="btn">GitHub 仓库 &rarr;</a>
          </div>
        </div>
        """

    html_content = HTML_TEMPLATE.format(
        date_str=date_str,
        ai_cards=ai_cards,
        ontology_cards=ont_cards,
        github_cards=gh_cards
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return output_path
