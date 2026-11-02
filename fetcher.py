"""
技术雷达数据采集模块（品质优先 + 区域保底 + 自动缓存容灾）
核心规则：
1. 自由竞逐：总体按质量、热度、新颖度自由排序；
2. 区域保底：严格确保 🇨🇳 中国区 与 🌐 全球区 各至少有 1 个入选名额；
3. 容灾兜底：当遇到 GitHub API 频控或网络波动时，自动从本地快照优雅回退，保证简报永不留白。
"""

import os
import json
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
import requests

HEADERS = {
    "User-Agent": "TechRadar/7.0 (Mozilla/5.0 Windows NT 10.0; Win64; x64)"
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
    """品质优先 + 区域保底排序：确保双区各至少有 min_each 项"""
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
    """采集 AI 前沿动态：中国区与全球混合择优，各保底至少1条"""
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
    """采集本体与知识工程前沿：涵盖业务本体、知识图谱推理、神经符号学与可执行规范"""
    items = []
    try:
        query = '(ti:ontology OR abs:ontology OR ti:"knowledge graph" OR ti:"neuro-symbolic") AND (cat:cs.AI OR cat:cs.LO OR cat:cs.DB)'
        encoded_query = urllib.parse.quote(query)
        url = f"https://export.arxiv.org/api/query?search_query={encoded_query}&sortBy=submittedDate&sortOrder=descending&max_results=3"

        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            root = ET.fromstring(resp.text)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
                summary = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
                link = entry.find("atom:id", ns).text.strip()
                published = entry.find("atom:published", ns).text[:10]
                authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)[:2]]

                items.append({
                    "title": title,
                    "authors": authors,
                    "published": published,
                    "summary": summary[:220] + "...",
                    "link": link
                })
    except Exception as e:
        print(f"[Warn] Fetch arXiv ontology failed: {e}")

    if items:
        save_cache("ontology", items)
    else:
        items = load_cache().get("ontology", [])
    return items

def fetch_github_trending() -> list[dict]:
    """采集 GitHub 增长工具：大池自由竞逐，且双区各至少保底 1 个高星新工具"""
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
            url = f"https://api.github.com/search/repositories?q={q_str}&sort=stars&order=desc&per_page=6"
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for repo in data.get("items", []):
                    desc = repo.get("description") or "暂无详细描述"
                    if any(noise in desc.lower() for noise in ["wallpaper", "gallery", "姿势", "photo", "awesome-"]):
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
        # 网络或频控故障时自动从缓存快照回退
        result = load_cache().get("github", [])

    return result

if __name__ == "__main__":
    print("Testing resilient quality-first fetcher...")
    ai = fetch_ai_news()
    gh = fetch_github_trending()
    print(f"AI: {len(ai)} 条, GitHub: {len(gh)} 条")
