from collections import defaultdict

def analyze(results):
    agg = defaultdict(int)
    for r in results:
        for item in r["rankings"]:
            agg[item["brand"]] += 1

    freq = [{"brand": k, "count": v} for k, v in agg.items()]
    insights = ["Basic analysis complete"]
    return {"frequency": freq, "insights": insights}
