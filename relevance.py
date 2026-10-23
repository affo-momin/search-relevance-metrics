"""Turn search-result relevance ratings into ranking-quality metrics.

Ratings CSV columns:
    query, rank, rater, rating
rating uses a 0-4 scale (0 = off-topic ... 4 = perfect / vital).
When several raters rate the same result, their ratings are averaged.

Metrics per query: NDCG@k, Precision@k (rating >= 3 counts as relevant), MRR.

Usage:
    python relevance.py sample_ratings.csv [k]
"""
import csv
import math
import statistics
import sys
from collections import defaultdict

RELEVANT_AT = 3


def load(path):
    """Return {query: {rank: [ratings]}}."""
    data = defaultdict(lambda: defaultdict(list))
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rating = float(r["rating"])
            if not 0 <= rating <= 4:
                raise ValueError(f"rating {rating} outside 0-4 for {r['query']!r} rank {r['rank']}")
            data[r["query"]][int(r["rank"])].append(rating)
    return data


def consensus(ranked):
    """Average rating per rank, ordered by rank."""
    return [statistics.mean(ranked[k]) for k in sorted(ranked)]


def dcg(gains, k):
    return sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(gains[:k]))


def ndcg(gains, k):
    ideal = dcg(sorted(gains, reverse=True), k)
    return dcg(gains, k) / ideal if ideal else 0.0


def precision(gains, k):
    top = gains[:k]
    return sum(g >= RELEVANT_AT for g in top) / len(top) if top else 0.0


def reciprocal_rank(gains):
    for i, g in enumerate(gains):
        if g >= RELEVANT_AT:
            return 1 / (i + 1)
    return 0.0


def rater_disagreement(data, threshold=2):
    """Results where raters' scores are `threshold` or more points apart."""
    out = []
    for q, ranked in data.items():
        for rank, rs in sorted(ranked.items()):
            if len(rs) > 1 and max(rs) - min(rs) >= threshold:
                out.append((q, rank, rs))
    return out


def report(data, k=5):
    lines = [f"# Search relevance report (k={k})", "", f"| Query | NDCG@{k} | P@{k} | RR |", "|---|---|---|---|"]
    scores = []
    for q, ranked in data.items():
        g = consensus(ranked)
        s = (ndcg(g, k), precision(g, k), reciprocal_rank(g))
        scores.append(s)
        lines.append(f"| {q} | {s[0]:.3f} | {s[1]:.2f} | {s[2]:.2f} |")
    means = [statistics.mean(x) for x in zip(*scores)]
    lines.append(f"| **Mean** | **{means[0]:.3f}** | **{means[1]:.2f}** | **{means[2]:.2f}** (MRR) |")
    lines += ["", "## Results to re-check (raters 2+ points apart)", ""]
    lines += [f"- {q!r} rank {r}: ratings {rs}" for q, r, rs in rater_disagreement(data)] or ["- none"]
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit("usage: python relevance.py ratings.csv [k]")
    print(report(load(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) == 3 else 5))
