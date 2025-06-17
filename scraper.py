import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

COMPANIES_DIR ="https://www.ycombinator.com/companies/"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def get_company_links():
    """Uses Selenium to scrape first 100 company links from Y Combinator"""
    company_links = []

    options = Options()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.ycombinator.com/companies")

    time.sleep(5)  # Wait for JavaScript to load
    
    # Find all <a> tags linking to company profiles
    anchors = driver.find_elements(By.CSS_SELECTOR, "a[href^='/companies/']") 

    
    for a in anchors:
        href = a.get_attribute("href")
      
        if href and href not in company_links:
            company_links.append(href)
        if len(company_links) >= 100:
            break

        
    driver.quit()
    print(f"✅ Collected {len(company_links)} company links.")
    return company_links



def get_company_data(link):
    import re
    from bs4 import BeautifulSoup
    
    try:
        print(f"🔍 Scraping: {link}")
        res = requests.get(link, headers=headers)

        if res.status_code != 200:
            print(f"❌ Failed to fetch page. Status code: {res.status_code}")
            return {}

        soup = BeautifulSoup(res.text, "html.parser")

        # Company Name
        name_tag = soup.find("h1")
        name = name_tag.text.strip() if name_tag else ""

        # Batch
        all_text = soup.get_text(separator="\n")
        batch_match = re.search(r"Batch:\s*(.*)", all_text)
        batch = batch_match.group(1).strip() if batch_match else ""

        # Description (from meta tag)
        meta = soup.find("meta", attrs={"name": "description"})
        description = meta["content"] if meta else ""

        # Founders & Company LinkedIn URLs
        founders = []
        company_linkedin_url = ""
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "linkedin.com/in" in href:
                Fname = a.text.strip()
                if Fname:
                    founders.append(Fname)
            elif "linkedin.com/company/" in href and not company_linkedin_url:
                company_linkedin_url = href    

        # If no founders found, try to extract from specific divs
        if not founders:
            founder_divs = soup.find_all("div", class_="text-xl font-bold")
            for div in founder_divs:
                name = div.text.strip()
                if name != name_tag.text.strip():  # avoid duplicating company name
                    founders.append(name)

        # Return data as a dictionary
        return {
            "Company Name": name,
            "Batch": batch,
            "Description": description,
            "Founders": ", ".join(founders),
            "LinkedIn URLs": company_linkedin_url,
            "Company URLs": link
        }

    except Exception as e:
        print(f"❌ Error scraping {link}: {e}")
        return {}

def main():
    #Get all company links
    company_links = get_company_links()

    #Scrape data for each company
    all_data = []
    for i, link in enumerate(company_links, 1):
        print(f"\n[{i}/{len(company_links)}]")
        data = get_company_data(link)
        if data:
            all_data.append(data)
        time.sleep(1)  # delay to avoid overload

   
    #save all data to a CSV file
    df = pd.DataFrame(all_data)
    df.to_csv("yc_500_startups.csv", index=False)
    print("\n All Data saved to yc_500_startups.csv")


if __name__ == "__main__":
    main()