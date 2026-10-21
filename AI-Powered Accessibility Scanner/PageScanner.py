from datetime import datetime
from playwright.sync_api import sync_playwright
from axe_playwright_python.sync_playwright import Axe
import requests
from AILayerInjection import explain_issue

def ScanPage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        target_url = "https://vabysmo.com"
        page.goto(target_url)
        
        # Run the accessibility scan
        results = Axe().run(page)
        
        # Capture the exact scan time
        scan_time = datetime.now() 
        
        extracted_violations = []

        if results.response and "violations" in results.response:
            for violation in results.response["violations"]:
                record = {
                    "page_url": target_url,
                    "rule_id": violation.get("id"),        
                    "impact": violation.get("impact"),       
                    "description": violation.get("description"),
                    "scan_date": scan_time.isoformat()
                }
                extracted_violations.append(record)

        print(f"Successfully extracted {len(extracted_violations)} records:")
        for record in extracted_violations:
            record["ai_analysis"] = explain_issue(record["rule_id"], record["description"])
            response = requests.post("http://127.0.0.1:5000/violations",json=record )

    print(response.text)