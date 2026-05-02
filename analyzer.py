"""Cross-persona analysis: frequency, AI Visibility Score, insights."""
from collections import defaultdict


def analyze(results: list[dict]) -> dict:
    successful = [r for r in results if r.get("rankings")]
    n = len(successful)

    agg = defaultdict(lambda: {"brand": "", "count": 0, "personas": [],
                               "best_rank": 99, "score": 0})

    for r in successful:
        for item in r["rankings"]:
            key = item["brand"].lower()
            points = 6 - item["rank"]  # rank 1 -> 5, rank 5 -> 1
            entry = agg[key]
            entry["brand"] = item["brand"]
            entry["count"] += 1
            entry["personas"].append(r["label"])
            entry["best_rank"] = min(entry["best_rank"], item["rank"])
            entry["score"] += points

    max_score = n * 5 if n else 1
    frequency = []
    for v in agg.values():
        frequency.append({**v, "visibility": round(v["score"] / max_score * 100)})
    frequency.sort(key=lambda x: (-x["score"], x["best_rank"]))

    insights, suggestions = [], []
    if frequency:
        w = frequency[0]
        insights.append(
            f"🏆 **{w['brand']}** dominates with a Visibility Score of "
            f"{w['visibility']}/100, recommended by {w['count']}/{n} personas."
        )
    consensus = [b for b in frequency if b["count"] == n]
    if consensus:
        insights.append(
            f"✅ {len(consensus)} brand(s) appear across ALL personas — "
            f"universal appeal: {', '.join(b['brand'] for b in consensus)}."
        )
    elif n > 1:
        insights.append(
            "⚠️ No brand appears in every persona's top 5 — "
            "the market is segmented by buyer type."
        )
    niche = [b for b in frequency if b["count"] == 1]
    if niche:
        insights.append(
            f"🎯 {len(niche)} brand(s) appeal to only one persona — niche positioning."
        )

    if frequency and frequency[0]["visibility"] < 100:
        suggestions.append(
            f"To dethrone **{frequency[0]['brand']}**, target the personas where "
            "it ranks lowest with persona-specific content."
        )
    suggestions.append(
        "Brands missing from all personas have **zero AI visibility** — "
        "invest in structured data, expert reviews, and persona-targeted content."
    )

    return {"frequency": frequency, "insights": insights, "suggestions": suggestions}
