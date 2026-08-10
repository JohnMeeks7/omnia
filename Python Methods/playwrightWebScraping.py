import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        

        context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        url = "https://www.indeed.com/jobs?q=quantitative+finance&l=Charlotte%2C+NC"
        response = page.goto(url)
        print("Response status:", response.status)
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        browser.close()
        jobCards = soup.find_all("div", class_="job_seen_beacon")
        print(f"Found {len(jobCards)} jobs")
        jobsData = []
        for index, card in enumerate(jobCards):
            titleTag = card.find("a", class_="jcs-JobTitle")
            if titleTag:
                title = titleTag.get_text()
            else:
                title = "Title not found"
            companyTag = card.find("span", {"data-testid": "company-name"}) or card.find("span", class_="companyName")
            company = companyTag.get_text() if companyTag else "Company Not Found"
            locationTag = card.find("div", {"data-testid": "text-location"}) or card.find("div", class_="companyLocation")
            location = locationTag.get_text() if locationTag else "Job Location Not Found"
            jobsData.append({
                "Title": title,
                "Company": company,
                "Location": location
            })
        df = pd.DataFrame(jobsData)
        df.to_csv("charlotteQuantJobs.csv", index=False, encoding="utf-8-sig")
        print("csv saved, good to exit")
run()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
