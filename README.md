# Qatar Job Market Data Scraper

## Introduction
In this project, I developed a Python script to scrape job listings from LinkedIn for opportunities in Qatar. The goal was to gather and analyze data on job availability, company details, and job descriptions to gain insights into the job market.

## Tools and Technologies
- Python
- BeautifulSoup
- Pandas
- Requests

## Project Overview
1. **Define the URL and Parameters:** Set the URL for the LinkedIn job search and specify the number of pages to scrape.
2. **Extract Job Data:** Use BeautifulSoup to parse the HTML content and extract relevant job details.
3. **Store Data:** Organize the extracted data into a Pandas DataFrame.
4. **Save to CSV:** Export the DataFrame to a CSV file for further analysis.

## Code Explanation

### 1. Define the URL and Parameters
We start by defining the URL for the LinkedIn job search and specifying the number of pages to scrape.

```python
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
from warnings import warn

raw_url = 'https://www.linkedin.com/jobs/search/?geoId=104170880&keywords=%20&location=Qatar'
pages_to_extract = 40  # Number of pages to scrape
page_inc = 25  # Number of jobs listed per page
