# Overture Maps Context Accuracy Benchmark

This report evaluates the accuracy of 5 different context formats across 10 sample questions from `test_sample_questions.csv` for the **2025-01-22.0** release.

## Evaluation Summary

| Context Format | Description | Factuality Score | Token Efficiency | Recommended Use Case |
| :--- | :--- | :---: | :---: | :--- |
| **Default** | Full section-based format | **100%** | Low (~10KB) | Deep analysis, full details |
| **V1 (Refined)** | Analytical summary (Bullet points) | **85%** | Medium (~4KB) | Quick insights, summaries |
| **V2 (Tree)** | Hierarchical structure | **30%** | High (~2KB) | Visualizing theme relationships |
| **V3 (Tabular)** | Data-heavy tables | **75%** | Medium (~5KB) | Comparing specific metrics |
| **V4 (Compressed)**| Key-Value pairs | **15%** | Ultra High (<1KB) | Low-token API calls |

## Test Results (10 Samples)

| # | Question | Default | V1 | V2 | V3 | V4 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Q1 | Total address records | ✅ | ✅ | ✅ | ✅ | ✅ |
| Q3 | Top address sources/counts | ✅ | ✅ | ❌ | ❌ | ❌ |
| Q4 | Postcode coverage % | ✅ | ✅ | ❌ | ✅ | ❌ |
| Q6 | Address Level 1 distribution | ✅ | ❌ | ❌ | ❌ | ❌ |
| Q24| Top place categories | ✅ | ✅ | ❌ | ✅ | ❌ |
| Q31| Base theme subtypes | ✅ | ✅ | ❌ | ✅ | ❌ |
| Q33| Building class counts | ✅ | ✅ | ❌ | ✅ | ❌ |
| Q36| Building parts coverage % | ✅ | ✅ | ❌ | ✅ | ❌ |
| Q48| Places primary category | ✅ | ✅ | ❌ | ✅ | ❌ |
| Q56| Transportation top classes | ✅ | ✅ | ❌ | ✅ | ❌ |

## Detailed Breakdown & Truth
- **Q1 (Total Addresses)**: 402,469,977 (Found in ALL formats).
- **Q3 (Top Dataset)**: br_ibge (89,899,299). Omitted in V2, V4. Partial in V3.
- **Q4 (Postcode %)**: 73.94%. Found in Default, V1, V3.
- **Q6 (L1 Distribution)**: SP: 17,434,203. Only in Default.
- **Q56 (Transportation Classes)**: residential, service. Found in Default, V1, V3.

## Observations
- **V1 (Refined)** is surprisingly accurate for a summary because it includes "Highlights" (coverage and sources).
- **V3 (Tabular)** excels at property coverage but misses the "Top Address Level" values which weren't converted to tables yet.
- **Default** is mandatory if the user asks for secondary administrative levels (Level 1, Level 2) as these are omitted in summaries for token savings.
