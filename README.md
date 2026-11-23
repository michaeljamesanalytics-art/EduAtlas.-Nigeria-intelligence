# EduAtlas Nigeria — Learning Atlas + Education Intelligence

**Expanded research prototype, editorial learning content dated 23 November 2026.** Independent project; not affiliated with government. Designed for learners who want to understand Nigeria's education system from foundations to governance, finance, classroom instruction, research, and practical reform.

## What is in this edition?

- **13 systematic learning tracks / 65 connected lessons.** Each includes foundational explanation, mechanism, Nigeria-specific example, investigation, learning check, reasoning guide, primary-source link and local field notes.
- **69-term searchable glossary** of Nigerian education, teaching, regulation, finance, and policy terms.
- **Institutional systems map**, expanded role directory containing 20 officeholder/institution entries, with the important difference between named officeholders and enduring offices.
- **Policy tracker, historical timeline, financing evidence chain, source library, curated intelligence feed**, local research notebook.
- **Daily 07:00 WAT monitoring desk** with the latest source check time, health status and separately labelled *unreviewed* discoveries. An open hosted app checks for a new static feed every five minutes and when its browser tab regains focus.

The 65 study notes are a structured **starting corpus, not exhaustive coverage** of every historical event, state's law, ministry, institution, curriculum edition, legal interpretation, budget line, school, or university. For research or advocacy, read the exact original document and verify its date, scope, and authority. The notes cannot replace formal accredited training or legal advice.

## How to open the app today

**Offline demo:** Open `EduAtlas-Nigeria-Expanded-Demo.html` in a browser. No installation or account required. It embeds the 65 lessons and dated starter research, but **cannot update itself in the background**. Local completion and notes are saved in the browser; incognito windows, clearing browser data, or switching devices may remove them.

**Deployable source:** Upload this project folder to a GitHub repository. You can test it with `python -m http.server 8000` from the project root and browse to `http://localhost:8000`.

## Publish and activate the daily updater

1. Create a repository for EduAtlas. If you intend to use GitHub Pages on a free account, publishing the project publicly may be necessary; review the repository's visibility before uploading anything. **Do not commit personal notes, secrets or pupil data.**
2. Upload the source project, including the `.github/workflows/` folder, `index.html`, `app.js`, `styles.css`, `data/`, and `scripts/`.
3. In repository **Settings → Pages**, choose **Deploy from a branch**, the default branch and **/(root)**. Verify your Pages URL works.
4. In **Settings → Actions → General → Workflow permissions**, allow GitHub Actions to write repository content, if permitted by your repository policies. The workflow commits a new static feed status after checks.
5. In **Actions → Nigeria education daily discovery**, use **Run workflow** to test immediately. Read logs and inspect `data/feed_status.json`, `data/auto_updates.json` and `data/daily_brief.json`.
6. Return to the website and visit **Daily 7am brief**; confirm its **last successful source check** actually updates. A header date from editorial content is not proof of current news.

### How 7 AM Nigeria time works

Nigeria uses **West Africa Time, UTC+1**, without daylight saving time. The workflow runs at **05:15 UTC (06:15 WAT)**, **05:45 UTC (06:45 WAT)** and **06:00 UTC (07:00 WAT)**, so that an earlier completed pass can be available by 7:00 AM and the later pass can catch further publications. GitHub-hosted scheduled workflows are **best-effort**, may be delayed, paused or disabled in inactive repositories, and **cannot guarantee** publication exactly by 07:00. The app shows the *actual successful source check time* and source health; old data is never presented as freshly checked.

The update workflow currently discovers RSS records from **FME, UBEC and NUC only**. Agency feeds may stop working or publish incomplete information. Sources outside these feeds, including 36 state ministries, the FCT, budget reports, appointments, research papers and data portals, are **not yet comprehensively automated**. A blank daily feed does **not** mean nothing happened in education that day. Do not label scraped headlines as verified outcomes.

A separate **ChatGPT daily 7:00 AM education briefing** was scheduled for the user in this conversation; this is *independent of the hosted app*, and does not write directly to GitHub Pages.

## Editorial quality checklist

For every major claim, record: original source link, original publication date, event date, responsible office, legal/policy status, affected geography and learners, budget period, and what phase is actually verified:

1. **Budget approved** — authorization or financing decision.
2. **Funds released** — verified disbursement or cash availability.
3. **Funds utilized** — expenditure or paid obligations.
4. **Outputs delivered** — functioning goods, works, services or training.
5. **Learning outcomes** — independently assessed achievement, preferably with credible causal evaluation.

Do not silently infer any later stage from an earlier stage. A policy announcement demonstrates intention, not implementation. Headline monitoring is only the first step toward verified policy research.

## Code and content organization

| File | Purpose |
| --- | --- |
| `index.html`, `styles.css`, `app.js` | Responsive app and interactions |
| `data/academy.json`, `data/academy.js` | 13 learning tracks, 65 lessons, sources and glossary |
| `data/curated.json`, `data/curated.js` | Editorially reviewed policies, leaders, timeline and evidence |
| `data/auto_updates.json` | Unreviewed discoveries from selected official feeds |
| `data/daily_brief.json`, `data/daily_brief.js` | Actual check timestamp, source health and recent discovery summary |
| `data/feed_status.json` | Last feed check errors and per-source results (created by workflow) |
| `scripts/update_feeds.py` | Official RSS discovery with hostname validation and deduplication |
| `scripts/build_daily_brief.py` | Publish a source-health-aware daily digest snapshot |
| `scripts/build_learning_data.py` | Editorial curriculum builder (do not confuse it with automatic research) |
| `scripts/build_standalone.py` | Package static source into a standalone HTML demo |
| `.github/workflows/discover-education-updates.yml` | Best-effort daily scheduling |

Regenerate edited content files with `python scripts/build_learning_data.py` when editing the **builder**, or manually update both `data/academy.json` and `data/academy.js` if editing the rendered dataset. After changing files, run `python scripts/build_standalone.py` to rebuild the standalone HTML. Python standard library is sufficient for the updater; the app itself uses plain JavaScript and CSS.

## Priorities for a true national product

The next generation needs a maintained source registry across 36 states and FCT, a document archive with version history, normalized officeholder–institution–policy–finance relationships, published editorial corrections, searchable FOI/accountability records, direct quarterly budget ingestion, and a provenance-aware research database. Build a moderated backend rather than presenting unverified generated summaries as definitive. For users across devices, add authenticated profiles with consent and strong security. For compliance, do not collect unnecessary child records or biometrics.

## Research anchors

- National Policy on Education: https://education.gov.ng/fme-resources/national-policy-on-education-2014/
- NERDC: https://nerdc.gov.ng/
- UBEC: https://ubec.gov.ng/
- NESRI: https://nesri.education.gov.ng/pillars
- Federal Ministry of Education: https://education.gov.ng/
- DNEMIS: https://emis.education.gov.ng/
- Budget implementation reports: https://budgetoffice.gov.ng/index.php/resources/internal-resources/reports/quarterly-budget-implementation
- UNICEF foundational learning: https://www.unicef.org/nigeria/reports/foundational-literacy-and-numeracy-nigeria
- UNICEF basic education finance: https://www.unicef.org/nigeria/reports/public-finance-basic-education-nigeria

**Privacy:** No analytics, account creation, or server-side storage of study notes are included in this release. LocalStorage only. Do not upload identifiable learner information to the public repository.
