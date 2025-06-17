import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. Test URL: One real YC company
company_url = "https://www.ycombinator.com/companies/clipboard-health"

# 2. Set headers to avoid being blocked
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 3. Scraper function
def get_company_data(link):
    import re
    """Extracts details from YC company page with debug output."""
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

        # Founders & LinkedIn URLs
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

# 4. Scrape the test company
company_data = get_company_data(company_url)

# 5. Save to CSV
if company_data:
    df = pd.DataFrame([company_data])  # Wrap the dictionary in a list
    df.to_csv("yc_startups.csv", index=False)
    print("✅ Data saved to yc_startups.csv")
else:
    print("⚠️ No data to save")
