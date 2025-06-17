# YC Startup Scraper

A Python-based web scraper that collects detailed information about 500 Y Combinator startups from the official YC Company Directory using Selenium and BeautifulSoup. The scraped data includes company name, batch, description, founders, and LinkedIn URLs, and is saved in a structured CSV file.

## 📌 Features

- Collects links for 500 companies using Selenium (with scrolling).
- Extracts detailed company data from each individual profile page.
- Supports headless browsing with ChromeDriver.
- Outputs data to `yc_500_startups.csv`.

## 🚀 Technologies Used

- Python 
- Selenium
- BeautifulSoup (bs4)
- Requests
- Pandas

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/imandikavithma/YC-startup-scraper.git
   cd yc-startup-scraper
