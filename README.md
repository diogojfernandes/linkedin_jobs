# LinkedIn Jobs in Portugal: Project Overview
* Scraped over 800 job posts from LinkedIn using Python, Selenium and BeautifulSoup
* Data exploration and analysis

## Code and Resources Used 
**Python Version:** 3.7  
**Packages:** pandas, selenium, beautifulsoup, numpy, matplotlib, seaborn

## Web Scraping
Created a job scraper and collected from LinkedIn over 800 job posts located in Portugal.
*	Job title
*	Location
*	Company Name
*	Number of Applicants
*	Company Sector
*	Number of Employees
*	Position Type
*	Remote Job
*	LinkedIn Easy Apply
*	Seniority

## Data Cleaning
After scraping the data, I clean it up and made the following changes:

*	Removed secondary data from position title 
*	Extracted city name from location
*	Parsed numeric data out of number of applicants 
*	Removed employees text from number of employees
*	Added column Seniority
