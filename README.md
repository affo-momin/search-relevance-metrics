# 🔍 Search Relevance Metrics

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white) ![No dependencies](https://img.shields.io/badge/dependencies-none-2ea44f?style=flat-square) ![Tests](https://img.shields.io/badge/tests-unittest-2ea44f?style=flat-square) ![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

Turn human search-quality ratings into standard ranking metrics: NDCG@k, Precision@k and MRR, and flag results where raters disagree.

## Why this exists

Search raters judge each result on a relevance scale. Those judgments only become useful to an engineering team when they're rolled up into ranking metrics. This tool does that, and also points out results that need a second look because raters scored them far apart.

## Features

- **Consensus rating** per result (average across raters, 0-4 scale)
- **NDCG@k**: rewards putting the most relevant results at the top
- **Precision@k**: share of top-k results rated relevant (>= 3)
- **MRR**: how early the first relevant result appears
- **Re-check list** of results where raters are 2+ points apart

## Quick start

No installs needed, just Python 3.9+.

```bash
git clone https://github.com/affo-momin/search-relevance-metrics.git
cd search-relevance-metrics
python relevance.py sample_ratings.csv 5
```

## Input

A CSV with `query, rank, rater, rating` (rating 0-4).

## Sample output

Running `python relevance.py sample_ratings.csv 5` on the included sample data:

# Search relevance report (k=5)

| Query | NDCG@5 | P@5 | RR |
|---|---|---|---|
| best budget smartphone 2026 | 1.000 | 0.40 | 1.00 |
| pizza near me | 0.918 | 0.40 | 1.00 |
| how to renew passport india | 1.000 | 0.60 | 1.00 |
| python csv tutorial | 0.665 | 0.40 | 0.50 |
| **Mean** | **0.896** | **0.45** | **0.88** (MRR) |

## Results to re-check (raters 2+ points apart)

- 'pizza near me' rank 3: ratings [2.0, 0.0]

## Tests

```bash
python -m unittest -v test_relevance
```

## License

MIT
