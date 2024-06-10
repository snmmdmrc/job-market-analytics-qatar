# Importing packages
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
from warnings import warn

raw_url = 'https://www.linkedin.com/jobs/search/?geoId=104170880&keywords=%20&location=Qatar'
pages_to_extract = 40  # Number of Job Search Pages to scrape
page_inc = 25  # Do not change, number of jobs that is usually listed in LinkedIn per page

def get_urls(raw_url, pages_to_extract, page_inc):
    """Creates a list of URLs for each job page of LinkedIn, based on pages_to_extract"""
    return [raw_url + '&start=' + str(x * page_inc) for x in range(pages_to_extract)]

def get_job_soup(url):
    """For a URL, extract the soup using BeautifulSoup Parser"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    except requests.exceptions.RequestException as e:
        warn(f"Request failed: {e}")
        return None

def get_job_fields(soup):
    """Extract job fields from a LinkedIn Job Page Soup"""
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

urls = get_urls(raw_url, pages_to_extract, page_inc)
soups = [get_job_soup(url) for url in urls]
job_fields = [get_job_fields(soup) for soup in soups if soup is not None]

# Flatten the extracted lists
keys = [[] for _ in range(11)]
for i in range(len(job_fields)):
    for j in range(11):
        keys[j].extend(job_fields[i][j])

# Create a DataFrame
link_jobs = pd.DataFrame(data=zip(*keys),
                         columns=['Linkedin Job ID', 'Job Title', 'Company', 'Date Posted', 'Salary',
                                  'Location', 'Easy Apply', 'Hiring status', 'Job Link', 'Company Profile', 'Job Desc'])

link_jobs_unq = link_jobs.drop_duplicates(subset='Linkedin Job ID', keep='first', inplace=False).sort_values(by=['Date Posted'], ascending=False)
link_jobs_unq.to_csv('jobs.csv', index=False)
