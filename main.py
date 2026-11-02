"""
技术雷达主程序
功能：
1. 抓取 AI 动态、本体前沿论文、GitHub 热门开源工具
2. 沉淀归档至 E:\\AI\\05-助手\\03-外部知识\\技术雷达\\简报归档
3. 通过自建应用机器人直接向个人飞书发送富文本交互卡片（支持单聊）
"""

import os
import sys
import json
from datetime import datetime
import requests
from fetcher import fetch_ai_news, fetch_ontology_updates, fetch_github_trending
from html_renderer import render_html

DEFAULT_LOCAL_ARCHIVE = r"E:\AI\05-助手\03-外部知识\技术雷达\简报归档"
if os.path.exists(os.path.dirname(DEFAULT_LOCAL_ARCHIVE)):
    ARCHIVE_DIR = os.environ.get("ARCHIVE_DIR") or DEFAULT_LOCAL_ARCHIVE
else:
    ARCHIVE_DIR = os.environ.get("ARCHIVE_DIR") or os.path.join(os.path.dirname(__file__), "digests")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    resp = requests.post(url, headers=headers, json={"app_id": app_id, "app_secret": app_secret}, timeout=10)
    res = resp.json()
    if res.get("code") == 0:
        return res.get("tenant_access_token")
    return None

def build_card_content(ai_items: list, ontology_items: list, gh_items: list, date_str: str, web_url: str = None) -> dict:
    elements = []

    # 快捷直达按钮区（置顶）
    if web_url:
        elements.append({
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": "🌐 在浏览器中打开今日完整版 HTML (图文排版)"
                    },
                    "type": "primary",
                    "url": web_url
                }
            ]
        })
        elements.append({"tag": "hr"})

    # 1. AI 板块
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": "**🔥 1. AI 前沿动态**"}
    })
    for item in ai_items:
        src = item.get("source", "Web")
        region = item.get("region", "")
        region_str = f"`{region}` " if region else ""
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"• {region_str}`[{src}]` **[{item['title']}]({item['link']})**\n  ⭐ 关注度: {item.get('points', 0)} | 📅 日期: {item.get('date', '')}"
            }
        })
    elements.append({"tag": "hr"})

    # 2. 本体/知识图谱板块
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": "**🧩 2. 本体与知识工程前沿 (arXiv)**"}
    })
    for item in ontology_items:
        authors_str = ", ".join(item.get("authors", []))
        region = item.get("region", "")
        region_str = f"`{region}` " if region else ""
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"• {region_str}**[{item['title']}]({item['link']})**\n  ✍️ 作者: {authors_str} ({item.get('published', '')})\n  💡 摘要: {item.get('summary', '')}"
            }
        })
    elements.append({"tag": "hr"})

    # 3. GitHub 增长工具
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": "**⚡ 3. GitHub 增长最快新项目**"}
    })
    for item in gh_items:
        region = item.get("region", "")
        region_str = f"`{region}` " if region else ""
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"• {region_str}**[{item['name']}]({item['link']})** (⭐ {item.get('stars', 0)} | {item.get('language', '')})\n  🛠️ 简介: {item.get('description', '')}"
            }
        })

    elements.append({"tag": "hr"})
    elements.append({
        "tag": "note",
        "elements": [
            {"tag": "plain_text", "content": f"已归档至 05-助手/03-外部知识/技术雷达 · 发送至个人单聊"}
        ]
    })

    return {
        "header": {
            "title": {"tag": "plain_text", "content": f"📡 技术雷达日报 ({date_str})"},
            "template": "blue"
        },
        "elements": elements
    }

def archive_to_assistant(ai_items: list, ontology_items: list, gh_items: list, date_str: str) -> str:
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    filepath = os.path.join(ARCHIVE_DIR, f"{date_str}.md")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# 技术雷达简报 ({date_str})\n\n")
        f.write("> **可信度**: 🟢 官方公开数据源 | **保密级别**: 🔓 可对外 | **更新日期**: " + date_str + "\n\n")

        f.write("## 1. AI 前沿动态\n\n")
        for item in ai_items:
            f.write(f"- **[{item['title']}]({item['link']})**\n")
            f.write(f"  - 热度: {item.get('points')} 点赞 | 发布日期: {item.get('date')}\n\n")

        f.write("## 2. 本体与知识工程前沿\n\n")
        for item in ontology_items:
            f.write(f"- **[{item['title']}]({item['link']})**\n")
            f.write(f"  - 作者: {', '.join(item.get('authors', []))} ({item.get('published')})\n")
            f.write(f"  - 摘要: {item.get('summary')}\n\n")

        f.write("## 3. GitHub 增长最快开源项目\n\n")
        for item in gh_items:
            f.write(f"- **[{item['name']}]({item['link']})** (⭐ {item.get('stars')} | 语言: {item.get('language')})\n")
            f.write(f"  - 简介: {item.get('description')}\n\n")

    return filepath

def send_to_user(token: str, open_id: str, card: dict) -> bool:
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    body = {
        "receive_id": open_id,
        "msg_type": "interactive",
        "content": json.dumps(card, ensure_ascii=False)
    }
    resp = requests.post(url, headers=headers, json=body, timeout=10)
    res = resp.json()
    return res.get("code") == 0

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"=== 开始执行技术雷达抓取与推送 [{date_str}] ===")

    cfg = load_config()
    app_id = os.environ.get("FEISHU_APP_ID") or cfg.get("feishu", {}).get("app_id")
    app_secret = os.environ.get("FEISHU_APP_SECRET") or cfg.get("feishu", {}).get("app_secret")
    open_id = os.environ.get("FEISHU_OPEN_ID") or cfg.get("feishu", {}).get("receive_open_id")

    ai_items = fetch_ai_news()
    print(f"✓ 采集 AI 资讯: {len(ai_items)} 条")

    ontology_items = fetch_ontology_updates()
    print(f"✓ 采集本体论文: {len(ontology_items)} 条")

    gh_items = fetch_github_trending()
    print(f"✓ 采集 GitHub 项目: {len(gh_items)} 条")

    # 1. 沉淀至 05-助手 (Markdown 与 HTML 双版本)
    archive_path = archive_to_assistant(ai_items, ontology_items, gh_items, date_str)
    html_path = os.path.join(ARCHIVE_DIR, f"{date_str}.html")
    render_html(ai_items, ontology_items, gh_items, date_str, html_path)

    # 同时生成 index.html（便于作为 Web 站点首页直接访问）
    index_html_path = os.path.join(os.path.dirname(__file__), "index.html")
    render_html(ai_items, ontology_items, gh_items, date_str, index_html_path)

    print(f"✓ 简报已沉淀到助手知识库: {archive_path}")
    print(f"✓ HTML 页面已生成: {html_path}")
    print(f"✓ Web 站点首页已更新: {index_html_path}")

    # GitHub Pages 专属在线访问 URL
    web_url = os.environ.get("PAGES_URL") or "https://derek-cz.github.io/tech-pulse/"

    # 2. 推送飞书个人单聊
    token = get_tenant_access_token(app_id, app_secret)
    if token and open_id:
        card = build_card_content(ai_items, ontology_items, gh_items, date_str, web_url=web_url)
        ok = send_to_user(token, open_id, card)
        if ok:
            print(f"✓ 已成功通过机器人直接推送至你的飞书！")
        else:
            print(f"✗ 飞书消息发送失败，请检查机器人权限配置。")
    else:
        print(f"✗ 缺少飞书凭据或 Open ID，跳过推送。")

if __name__ == "__main__":
    main()
