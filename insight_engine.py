"""依据当期条目生成速读，不推断原文未提供的结论。"""


def generate_daily_takeaway(ai_items: list, ont_items: list, gh_items: list) -> str:
    sections = (("AI", ai_items, "title"), ("本体", ont_items, "title"),
                ("开源项目", gh_items, "name"))
    lines = []
    for label, items, key in sections:
        if items:
            name = str(items[0].get(key) or "未提供标题").strip()
            lines.append(f"{label}：{len(items)} 条；首项：{name}")
        else:
            lines.append(f"{label}：本期未获取到条目。")
    lines.append("速读依据本期采集条目生成；具体内容请查阅原文。")
    return "\n".join(lines)


def enrich_all(ai_items: list, ont_items: list, gh_items: list) -> tuple:
    # 不添加关键词模板生成的结论，保留采集到的原始摘要和简介。
    return ai_items, ont_items, gh_items, generate_daily_takeaway(ai_items, ont_items, gh_items)
