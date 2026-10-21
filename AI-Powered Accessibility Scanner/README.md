#AI-Powered Accessibility Scanner

An AI-assisted accessibility testing platform that automatically scans web applications for WCAG compliance violations, generates remediation recommendations using LLMs, stores historical results, and provides actionable insights through dashboards and automated reporting.

🚀 ##Project Overview

Manual accessibility testing is time-consuming and often lacks scalability across large web applications. This project automates the accessibility validation process using:

Playwright for browser automation
axe-core for WCAG rule evaluation
Python for orchestration and data processing
PostgreSQL for historical data storage
n8n for workflow automation
LLMs (Claude/Ollama/Llama 3) for AI-powered explanations and remediation guidance
FastAPI for API services
Streamlit for reporting dashboards

The platform scans websites, detects accessibility violations, enriches findings with AI-generated recommendations, and provides development teams with prioritized remediation plans.

🎯 ##Key Features
Accessibility Scanning
Automated WCAG 2.1 compliance scanning
Keyboard accessibility validation
Form label checks
Image alt-text validation
ARIA attribute verification
Color contrast analysis
Semantic HTML validation
AI-Powered Analysis
Human-readable explanations of violations
WCAG guideline references
Suggested code fixes
Prioritized remediation recommendations
Executive summary generation
Reporting & Analytics
Historical trend tracking
Violation severity analysis
Accessibility scoring
Dashboard visualization
PDF/Email-ready reports
Automation
On-demand scans via API
Scheduled scans with n8n
Slack/Email notifications
CI/CD integration support

🛠 ##Technology Stack
Testing & Automation
Python 3.11+
Playwright
axe-core
Pytest
Backend
FastAPI
SQLAlchemy
PostgreSQL
AI Layer
Claude API
Ollama
Llama 3
Mistral
Workflow Automation
n8n
Reporting
Streamlit
Plotly
Pandas
DevOps
Docker
Docker Compose
GitHub Actions

ai-accessibility-scanner/

├── scanner/
│   ├── scan.py
│   ├── axe_runner.py
│   └── report_generator.py
│
├── api/
│   ├── main.py
│   └── routes.py
│
├── ai/
│   ├── analyzer.py
│   └── prompts.py
│
├── database/
│   ├── schema.sql
│   └── db.py
│
├── dashboard/
│   └── streamlit_app.py
│
├── workflows/
│   └── n8n_workflow.json
│
├── tests/
│   ├── test_api.py
│   └── test_scanner.py
│
├── docker-compose.yml
├── requirements.txt
└── README.md

⚙ ##Installation
Clone Repository
Shell
git clone https://github.com/yourusername/ai-accessibility-scanner.git
 
cd ai-accessibility-scanner
Create Virtual Environment
Shell
python -m venv venv
 
source venv/bin/activate

Windows:

PowerShell
venv\Scripts\activate
Install Dependencies
Shell
pip install -r requirements.txt
Install Playwright Browsers
Shell
playwright install
🗄 Database Setup

Create PostgreSQL database:

SQL
CREATE DATABASE accessibility_db;

Run schema:

Shell
psql -U postgres -d accessibility_db -f database/schema.sql
▶ Running the Scanner
Scan a Website
Shell
python scanner/scan.py https://example.com

Example Response:

JSON
{
"critical": 3,
"serious": 5,
"moderate": 8,
"minor": 6
}
🤖 AI Analysis Example

Raw Violation:

JSON
{
"id": "image-alt",
"impact": "critical"
}

AI Output:

Plain Text
Issue:
Images do not contain meaningful alternative text.
 
Impact:
Screen reader users cannot understand image content.
 
WCAG:
1.1.1 Non-text Content
 
Recommended Fix:
Provide descriptive alt attributes for informative images.
 
Example:
<img src="logo.png"
alt="Company Logo">
🌐 FastAPI Endpoints
Start Accessibility Scan
Request
HTTP
POST /scan

Body

JSON
{
"url": "https://example.com"
}
Response
JSON
{
"scan_id": 101,
"status": "completed",
"critical": 4,
"score": 82
}
Get Scan Results
HTTP
GET /scan/{scan_id}
Retrieve Historical Reports
HTTP
GET /reports
🔄 n8n Workflow
Automated Scan Process
Plain Text
Webhook Trigger
│
▼
Python Scanner
│
▼
Store Results
│

Supported triggers:

Manual Trigger
Scheduled Daily Scan
GitHub Deployment Trigger
API Request Trigger
📊 Dashboard
Summary Metrics
Total Violations
Accessibility Score
Critical Issues
Top WCAG Failures
Trend Analysis
Sample Dashboard Widgets
Plain Text
Accessibility Score: 87/100
 
Critical Issues: 4
Serious Issues: 7
Moderate Issues: 11
Minor Issues: 6
Trend Analysis
Plain Text
Month Violations
 
January 42
February 28
March 17
April 11
🧪 API Testing

Automated API validation using Pytest.

Example:

Python
def test_scan_endpoint():
response = requests.post(
"http://localhost:8000/scan",
json={
"url":"https://example.com"
}
)
 
assert response.status_code == 200
🐳 Docker Deployment

Build and start services:

Shell
docker-compose up --build

Containers:

Plain Text
PostgreSQL
FastAPI
Accessibility Scanner
Streamlit Dashboard
n8n
📈 Future Enhancements
Multi-page crawling
WCAG 2.2 support
AI-generated code fixes
Jira defect creation
GitHub Actions integration
Accessibility scorecards
Trend forecasting using AI
Visual accessibility testing
PDF report generation
💼 Skills Demonstrated

This project showcases expertise in:

Accessibility Testing
WCAG 2.1 Standards
Python Automation
Playwright
axe-core
API Testing
FastAPI
SQL & PostgreSQL
n8n Workflow Automation
AI/LLM Integration
Docker
CI/CD Concepts
Test Reporting & Analytics