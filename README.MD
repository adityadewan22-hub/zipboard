# zipBoard Help Center Audit & Gap Detection System

## Overview

This project implements an automated, state-aware documentation audit system for the zipBoard help center.  
It catalogs help articles, detects content changes, selectively applies LLM-based analysis, and synthesizes documentation gaps into a prioritized report.

The system is designed to be:

- **Automated** (daily via GitHub Actions)
- **Idempotent** (safe to re-run)
- **Cost-aware** (LLM usage is gated)
- **Auditable** (Excel as a transparent state store)

---

## Key Features

### 📄 Help Article Cataloging

Automatically scrapes and catalogs all help center articles (325+), capturing metadata such as:

- Article title
- Category
- URL
- Word count
- Screenshot presence

---

### 🔍 Hash-Based Change Detection

Uses **SHA256 hashing** on normalized article content to reliably detect real content changes instead of relying on timestamps.

---

### 🤖 State-Aware LLM Execution

LLM analysis runs **only when**:

- The article content has changed, **and**
- `analysis_scope = TRUE`

This prevents unnecessary LLM usage and keeps costs under control.

---

### 🧠 Cross-Article Gap Synthesis

Aggregates article-level gaps and synthesizes them into a:

- Deduplicated
- Prioritized
- Actionable gap analysis report

---

### 📊 Excel-Based State Management

The Excel file serves as the **source of truth**, containing:

- `Articles_Catalog`
- `Gap_Analysis`

This enables auditability, manual overrides, and transparency.

---

## Project Structure

```

zipboard/
├── app/
│ ├── main.py
│ ├── orchestrator.py
│ ├── config.py
│ │
│ ├── pipelines/
│ │ ├── run_article_audit.py
│ │ └── run_gap_synthesis.py
│ │
│ ├── extractors/
│ ├── processing/
│ ├── llm/
│ ├── io/
│ └── utils/
│
├── data/
│ └── zipboard_help_articles.xlsx
│
├── .github/
│ └── workflows/
│ └── daily_audit.yml
│
├── requirements.txt
└── README.md

```

---

## Workflow Overview

GitHub Actions (Daily)
↓
Fetch Article URLs
↓
Extract Metadata
↓
Fetch & Normalize Content
↓
SHA256 Hash Comparison
↓
UNCHANGED → Skip
UPDATED / NEW
↓
analysis_scope == TRUE ?
↓
LLM Article Analysis
↓
Collect Article-Level Gaps
↓
Cross-Article Gap Synthesis
↓
Update Excel:

Articles_Catalog

Gap_Analysis

---

## Automation

The system runs automatically once per day using GitHub Actions:

```yaml
on:
  schedule:
    - cron: "0 3 * * *"
  workflow_dispatch:
Safe to re-run

Manual trigger supported

No duplicate LLM calls due to hashing

Configuration
Create a .env file:

GEMINI_API_KEY=your_api_key_here
Install dependencies:

pip install -r requirements.txt
Run locally:

python -m app.main
Design Trade-offs
Polling vs Event-Driven:
Scheduled audits + hashing were chosen due to lack of native webhooks.

Excel vs Database:
Excel provides transparency and manual control for audit scenarios.

LLM Choice:
Gemini offers a cost-effective balance for repeated automated audits.

Future Improvements
Event-driven triggers if webhooks become available

Database-backed state store for very large documentation sets

More advanced LLMs or retrieval-augmented analysis
```
