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

### Full Code
Below is the full code used in this project:

```python
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
from warnings import warn

# Define the URL and Parameters
raw_url = 'https://www.linkedin.com/jobs/search/?geoId=104170880&keywords=%20&location=Qatar'
pages_to_extract = 40  # Number of pages to scrape
page_inc = 25  # Number of jobs listed per page

# Function to Generate URLs
def get_urls(raw_url, pages_to_extract, page_inc):
    return [raw_url + '&start=' + str(x * page_inc) for x in range(pages_to_extract)]

# Function to Extract Job Data
def get_job_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    except requests.exceptions.RequestException as e:
        warn(f"Request failed: {e}")
        return None

# Function to Extract Job Fields
def get_job_fields(soup):
    if soup is None:
        return None

    job_container_jobs = soup.find_all('a', class_='base-card__full-link')
    job_names = [x.span.text.strip() for x in job_container_jobs]
    job_urls = [x['href'] for x in job_container_jobs]
    job_id = [re.findall(r'(?!-)([0-9]*)(?=\?)', x)[0] for x in job_urls]

    job_container_company = soup.find_all('a', class_='hidden-nested-link')
    company_names = [x.text.strip() for x in job_container_company]
    company_urls = [x['href'] for x in job_container_company]

    job_info = soup.find_all('div', class_='base-search-card__metadata')
    company_benefits = ['None' if x is None else x.text.strip() for x in [x.find('span', class_='result-benefits__text') for x in job_info]]
    date_posted = [x.time['datetime'] for x in job_info]
    salary = ['Not mentioned' if x is None else x.text.strip() for x in [x.find('span', class_='job-search-card__salary-info') for x in job_info]]
    job_location = ['Not mentioned' if x is None else x.text.strip() for x in [x.find('span', class_='job-search-card__location') for x in job_info]]
    job_snippet = ['None' if x is None else x.text.strip() for x in [x.find('p', class_='job-search-card__snippet') for x in job_info]]
    easy_apply = ['Not enabled' if x is None else 'Enabled' for x in [x.find('span', class_='job-search-card__easy-apply-label') for x in job_info]]

    return [job_id, job_names, company_names, date_posted, salary, job_location, easy_apply, company_benefits, job_urls, company_urls, job_snippet]

# Extracting Data
urls = get_urls(raw_url, pages_to_extract, page_inc)
soups = [get_job_soup(url) for url in urls]
job_fields = [get_job_fields(soup) for soup in soups if soup is not None]

# Storing Data
keys = [[] for _ in range(11)]
for i in range(len(job_fields)):
    for j in range(11):
        keys[j].extend(job_fields[i][j])

link_jobs = pd.DataFrame(data=zip(*keys),
                         columns=['Linkedin Job ID', 'Job Title', 'Company', 'Date Posted', 'Salary',
                                  'Location', 'Easy Apply', 'Hiring status', 'Job Link', 'Company Profile', 'Job Desc'])

# Saving to CSV
link_jobs_unq = link_jobs.drop_duplicates(subset='Linkedin Job ID', keep='first', inplace=False).sort_values(by=['Date Posted'], ascending=False)
link_jobs_unq.to_csv('data/jobs.csv', index=False)

Results
After extracting and analyzing the data, we found that the majority of job listings in Qatar are in the IT and engineering sectors. Most companies do not mention the salary in the job description, and a significant number of jobs are available for easy apply.

Conclusion
This project demonstrated the ability to scrape job data from LinkedIn and analyze the job market trends in Qatar. Future improvements could include automating the script to run at regular intervals and adding more sophisticated data analysis and visualization.

Code Repository
You can view the full code for this project on my GitHub repository.
