# 🏠 Real Estate Listings Scraper

This project scrapes real estate-style listings from a website using **Scrapy**, **Selenium**, and **pandas**, and outputs data such as price, location, number of bedrooms, area (sqft), image URL, and listing link into a xlsx file.

It is built as a portfolio project to demonstrate real-world scraping skills that could be used by real estate analysts, investors, or lead-generation services.
---
## 🚀 Features

- Extracts:
  - Title or listing name
  - Price
  - Location (simulated or real)
  - Bedrooms and area (sqft)
  - Listing and image URLs
- Supports pagination
- Outputs to clean `.xlsx` file
- Easy to adapt to real websites with dynamic content

## 📂 Project Structure

real-estate-scraper/
├── spiders/
│ └── realestate_spider.py # Main spider file
├── data/
│ └── listings.csv # Output file (sample)
├── screenshots/
│ ├── terminal_run.png # Screenshot of terminal
│ └── sample_output.png # Screenshot of output
├── requirements.txt # Python dependencies
├── scrapy.cfg
└── README.md
---

## 🧪 How to Run the Scraper

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/real-estate-scraper.git
cd real-estate-scraper
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the Scraper
```bash
scrapy crawl realestate -o data/listings.csv
```
