# AI-Powered Accessibility Scanner

A Python proof of concept that scans a web page for accessibility violations, asks an AI service to explain each finding, stores the results in PostgreSQL, and displays them in a Streamlit dashboard.

## What it currently does

The current implementation is a single-page prototype:

1. Launches a headless Chromium browser with Playwright.
2. Runs axe on the page configured in `Utils/PageScanner.py` and collects each violation's rule ID, impact, description, and scan time.
3. Requests an AI-generated explanation for each violation.
4. Sends the findings to a Flask API for storage in PostgreSQL.
5. Provides a Streamlit dashboard for filtering and reviewing findings, viewing summaries and charts, downloading a CSV, and asking questions about the results.

The scanner currently targets a URL configured in source code; it does not accept a URL as a command-line or API parameter.

## Project layout

```text
AI-Powered Accessibility Scanner/
├── AccessibilityAnalysis.py         # Application entry point
├── Database/
│   └── Accessibility_Database.sql   # PostgreSQL database dump
├── Utils/
│   ├── AILayerInjection.py          # AI explanations for findings
│   ├── ApiEndpointCreation.py       # Flask API and database writes
│   ├── DashboardCreation.py         # Streamlit dashboard
│   └── PageScanner.py               # Playwright and axe scan
├── Dockerfile
├── docker-compose.yml
└── Requirements.txt
```

## Technology

- Python 3.12
- Playwright with Chromium
- axe-core via `axe-playwright-python`
- Flask
- PostgreSQL and psycopg2
- Streamlit and pandas
- Portkey AI client

## API

The Flask service defines these endpoints on port `5000`:

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/violations` | Save a finding and return its database ID |
| `GET` | `/violations` | Return saved findings |

The `POST` body is expected to include `page_url`, `rule_id`, `impact`, `description`, `scan_date`, and `ai_analysis`.

## Setup and current status

The repository includes a Dockerfile and Compose file, but the current configuration needs adjustment before the application can be run reliably. In particular, some imports and script paths do not match the `Utils/` layout, and the Compose file refers to database and requirements paths whose names do not match the checked-in files. The API and dashboard also use database connection settings that need to be aligned with the Compose service.

For a local Python environment, the dependency installation commands are:

```powershell
cd "AI-Powered Accessibility Scanner"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r Requirements.txt
playwright install chromium
```

These commands install dependencies and the browser only; they do not resolve the application configuration gaps described above.

## Configuration and safety

- The scan target and AI provider settings are currently defined in source code. Configure these through environment variables or another secret-management mechanism before using the project beyond local experimentation.
- Do not commit API tokens, database passwords, or other credentials. Rotate any credential that has been exposed in a shared repository.
- Only scan websites that you own or are authorized to test. The configured scan target should be changed to an authorized test site before running the scanner.
- AI-generated explanations are suggestions, not a substitute for validating findings against the applicable WCAG criteria and assistive technologies.

## Database

The schema stores findings in `accessibility_violations`, including the URL, axe rule, impact, description, scan timestamp, and AI explanation. `Database/Accessibility_Database.sql` is a PostgreSQL dump; it is not a plain SQL schema file.

## Limitations

- The scanner currently scans one hard-coded page per run.
- The AI service is called once per violation, so scans depend on provider availability and may incur usage costs.
- The dashboard and API have configuration that must be aligned with the database service before containerized use.
- This proof of concept is not a complete WCAG conformance test and should not be treated as certification.
