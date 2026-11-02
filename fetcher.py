"""
技术雷达数据采集模块（全维度双引擎·中国区严格保底·强摘要质检版）
改进点：
1. 本体论前沿：全面纳入双轨保底（🇨🇳 中国区前沿成果至少 1 篇 + 🌐 全球顶会成果至少 1 篇）；
2. 描述强门禁：过滤掉 GitHub 上作者未写 description 的半成品项目（严禁出现“暂无详细描述”）；
3. 容灾与快照保障：网络或 API 抖动时无缝降级回退。
"""

import os
import json
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
import requests

HEADERS = {
    "User-Agent": "TechRadar/8.0 (Mozilla/5.0 Windows NT 10.0; Win64; x64)"
}

CACHE_FILE = os.path.join(os.path.dirname(__file__), ".cache_snapshot.json")

def load_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_cache(key: str, data: list):
    cache = load_cache()
    cache[key] = data
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def apply_region_floor(candidates: list[dict], sort_key: str, total_limit: int = 4, min_each: int = 1) -> list[dict]:
    """品质优先 + 区域双向保底排序：确保中国区与全球区各至少有 min_each 项"""
    cn_pool = [x for x in candidates if "中国" in x.get("region", "")]
    global_pool = [x for x in candidates if "全球" in x.get("region", "")]

    cn_pool.sort(key=lambda x: x.get(sort_key, 0), reverse=True)
    global_pool.sort(key=lambda x: x.get(sort_key, 0), reverse=True)

    selected = []

    # 优先满足保底名额
    if cn_pool and min_each > 0:
        selected.extend(cn_pool[:min_each])
    if global_pool and min_each > 0:
        selected.extend(global_pool[:min_each])

    # 剩余池子混合自由竞逐
    used_ids = {x.get("link") or x.get("name") or x.get("title") for x in selected}
    remaining_pool = [
        x for x in candidates
        if (x.get("link") or x.get("name") or x.get("title")) not in used_ids
    ]
    remaining_pool.sort(key=lambda x: x.get(sort_key, 0), reverse=True)

    for item in remaining_pool:
        if len(selected) >= total_limit:
            break
        selected.append(item)

    selected.sort(key=lambda x: x.get(sort_key, 0), reverse=True)
    return selected

def fetch_ai_news() -> list[dict]:
    """采集 AI 前沿动态：中国区(OSChina)与全球(HN/HF)自由竞逐，双区各保底至少1条"""
    candidates = []

    # 1. 🇨🇳 中国区：开源中国 (OSChina)
    try:
        url = "https://www.oschina.net/news/rss"
        resp = requests.get(url, headers=HEADERS, timeout=8)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            channel = root.find("channel")
            for entry in channel.findall("item"):
                title = entry.find("title").text.strip()
                link = entry.find("link").text.strip()
                if any(k in title for k in ["AI", "大模型", "Agent", "框架", "模型", "开源", "算力", "发布"]):
                    candidates.append({
                        "region": "🇨🇳 中国区",
                        "source": "开源中国 OSChina",
                        "title": title,
                        "points": "热点",
                        "score": 85,
                        "link": link,
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
                    if len([x for x in candidates if "中国" in x.get("region", "")]) >= 3:
                        break
    except Exception as e:
        print(f"[Warn] Fetch OSChina AI failed: {e}")

    # 2. 🌐 全球：Hacker News
    try:
        url = "https://hn.algolia.com/api/v1/search_by_date?tags=story&query=AI+OR+LLM+OR+Agent&numericFilters=points%3E30&hitsPerPage=6"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for hit in data.get("hits", []):
                pts = hit.get("points", 0)
                candidates.append({
                    "region": "🌐 全球",
                    "source": "Hacker News",
                    "title": hit.get("title", ""),
                    "points": pts,
                    "score": min(pts, 150),
                    "link": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                    "date": hit.get("created_at", "")[:10]
                })
    except Exception as e:
        print(f"[Warn] Fetch Hacker News failed: {e}")

    # 3. 🌐 全球：Hugging Face Daily
    try:
        url = "https://huggingface.co/api/daily_papers?limit=3"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for p in data[:2]:
                paper = p.get("paper", {})
                candidates.append({
                    "region": "🌐 全球",
                    "source": "Hugging Face Daily",
                    "title": paper.get("title", "").strip().replace("\n", " "),
                    "points": p.get("upvotes", 0) + 10,
                    "score": 90,
                    "link": f"https://huggingface.co/papers/{paper.get('id')}",
                    "date": paper.get("publishedAt", "")[:10]
                })
    except Exception as e:
        print(f"[Warn] Fetch Hugging Face Papers failed: {e}")

    result = apply_region_floor(candidates, sort_key="score", total_limit=5, min_each=1)
    if result:
        save_cache("ai_news", result)
    else:
        result = load_cache().get("ai_news", [])
    return result

def fetch_ontology_updates() -> list[dict]:
    """采集本体与知识工程前沿：双轨保底（中国区前沿突破至少 1 篇，全球理论演进至少 1 篇）"""
    candidates = []

    # 通道 1: 🇨🇳 中国区学者与机构在知识图谱、本体工程、GraphRAG 与神经符号学的最新成果
    try:
        q_cn = '(ti:ontology OR abs:ontology OR ti:knowledge-graph OR ti:GraphRAG) AND (abs:Chinese OR abs:China OR abs:Tsinghua OR abs:Peking OR abs:Zhejiang)'
        url_cn = f"https://export.arxiv.org/api/query?search_query={urllib.parse.quote(q_cn)}&sortBy=submittedDate&sortOrder=descending&max_results=3"
        resp = requests.get(url_cn, headers=HEADERS, timeout=12)
        if resp.status_code == 200:
            root = ET.fromstring(resp.text)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
                summary = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
                link = entry.find("atom:id", ns).text.strip()
                published = entry.find("atom:published", ns).text[:10]
                authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)[:2]]
                candidates.append({
                    "region": "🇨🇳 中国区",
                    "title": title,
                    "authors": authors,
                    "published": published,
                    "score": 90,
                    "summary": summary[:220].strip() + "...",
                    "link": link
                })
    except Exception as e:
        print(f"[Warn] Fetch Chinese ontology failed: {e}")

    # 通道 2: 🌐 全球顶会与学术机构在本体论与可执行逻辑层面的最新演进
    try:
        q_global = '(ti:ontology OR abs:ontology OR ti:"neuro-symbolic") AND (cat:cs.AI OR cat:cs.LO OR cat:cs.DB)'
        url_global = f"https://export.arxiv.org/api/query?search_query={urllib.parse.quote(q_global)}&sortBy=submittedDate&sortOrder=descending&max_results=3"
        resp = requests.get(url_global, headers=HEADERS, timeout=12)
        if resp.status_code == 200:
            root = ET.fromstring(resp.text)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
                summary = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
                link = entry.find("atom:id", ns).text.strip()
                published = entry.find("atom:published", ns).text[:10]
                authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)[:2]]
                candidates.append({
                    "region": "🌐 全球",
                    "title": title,
                    "authors": authors,
                    "published": published,
                    "score": 85,
                    "summary": summary[:220].strip() + "...",
                    "link": link
                })
    except Exception as e:
        print(f"[Warn] Fetch Global ontology failed: {e}")

    # 3 篇配额：双区各至少保底 1 篇
    result = apply_region_floor(candidates, sort_key="score", total_limit=3, min_each=1)
    if result:
        save_cache("ontology", result)
    else:
        result = load_cache().get("ontology", [])
    return result

def fetch_github_trending() -> list[dict]:
    """采集 GitHub 增长工具：强质检门禁（排除无描述半成品），双区各保底 1 个高星新工具"""
    candidates = []
    since_date = (datetime.now(timezone.utc) - timedelta(days=10)).strftime("%Y-%m-%d")

    queries = [
        # 中国区高星开发者工具 / 中文生态
        (f"created:>{since_date} stars:>20 (中文 OR 国内 OR zh-cn) fork:false", "🇨🇳 中国区"),
        # 全球通用高星新工具 / Agent 原生框架
        (f"created:>{since_date} stars:>50 fork:false", "🌐 全球")
    ]

    for q_str, default_region in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={q_str}&sort=stars&order=desc&per_page=8"
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for repo in data.get("items", []):
                    desc = (repo.get("description") or "").strip()

                    # ⚠️ 强质检门禁 1：排除作者未写描述或描述太短（<10字符）的未完善项目，绝不展示“暂无详细描述”
                    if len(desc) < 10:
                        continue

                    # ⚠️ 强质检门禁 2：排除纯壁纸、姿势图库、设计模板等非技术/非开发工具
                    if any(noise in desc.lower() for noise in ["wallpaper", "gallery", "姿势", "photo", "awesome-", "cheat-sheet"]):
                        continue

                    region = "🇨🇳 中国区" if any("一" <= ch <= "鿿" for ch in desc[:50]) else default_region

                    candidates.append({
                        "region": region,
                        "name": repo.get("full_name"),
                        "stars": repo.get("stargazers_count", 0),
                        "description": desc,
                        "language": repo.get("language") or "General",
                        "link": repo.get("html_url")
                    })
        except Exception as e:
            print(f"[Warn] Fetch GitHub candidates failed: {e}")

    result = apply_region_floor(candidates, sort_key="stars", total_limit=4, min_each=1)
    if result:
        save_cache("github", result)
    else:
        result = load_cache().get("github", [])

    return result

if __name__ == "__main__":
    print("Testing upgraded dual-region fetcher with strict descriptions...")
    ai = fetch_ai_news()
    ont = fetch_ontology_updates()
    gh = fetch_github_trending()
    print(f"\nAI: {len(ai)} 条 (中国区: {len([x for x in ai if '中国' in x['region']])}, 全球: {len([x for x in ai if '全球' in x['region']])})")
    print(f"本体: {len(ont)} 篇 (中国区: {len([x for x in ont if '中国' in x['region']])}, 全球: {len([x for x in ont if '全球' in x['region']])})")
    for o in ont:
        print(f"  [{o['region']}] {o['title'][:50]}... | 作者: {o['authors']}")
    print(f"GitHub: {len(gh)} 个 (中国区: {len([x for x in gh if '中国' in x['region']])}, 全球: {len([x for x in gh if '全球' in x['region']])})")
    for g in gh:
        print(f"  [{g['region']}] {g['name']} (⭐ {g['stars']}): {g['description'][:50]}")
