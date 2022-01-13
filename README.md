# LinkedIn Data Science Jobs in Portugal: Project Overview
* Scraped over 1000 data science job posts from LinkedIn using Python, Selenium and BeautifulSoup
* Data exploration and analysis

## Code and Resources Used 
**Python Version:** 3.7  
**Packages:** pandas, selenium, beautifulsoup

## Web Scraping
Created a job scraper and collected from LinkedIn over 1000 job posts located in Portugal.

> Scraper script file: [linkedin_job_scraper.py](https://github.com/diogojfernandes/linkedin_jobs/blob/master/linkedin_job_scraper.py)

> Job positions CSV file: [job_positions.csv](https://github.com/diogojfernandes/linkedin_jobs/blob/master/job_positions.csv)

* Job ID
*	Job Title
*	Location
*	Company Name
*	Number of Applicants
*	Company Sector
*	Number of Employees
*	Position Type
*	Remote Job
*	LinkedIn Easy Apply
*	Job Details

Difficulties when scraping:
* Multiple account logins on Linkedin flags account as a bot

> Fixed it by adding my Chrome user data path to webdriver options. Previous login on Linkedin is needed.
```python
# Driver Configuration
options = Options()
options.add_argument('--start-maximized')
options.add_argument("user-data-dir=C:/Users/Diogo Fernandes/AppData/Local/Google/Chrome/User Data") 
```

* Quick scrape also flags account as a bot

> Fixed it by adding sleep times of 1 second when scrolling and iterating trough jobs.

* Linkeding message box don't let iterate trough jobs

> Fixed it by closing message box after loading job searching.
```python
try:
    driver.find_element_by_class_name("msg-overlay-bubble-header__button").click()
except:
    try:
        driver.find_element_by_class_name("msg-overlay-list-bubble__convo-card-content").click()
    except:
        pass
```

* Webdriver don't load all 25 jobs of each page in one scroll
> Fixed it by running multiple scrolls until all 25 job cards are loaded or until maximum cards have been found.
```python
while len(jobs_list)<25 and previous_jobs_length != actual_jobs_length:
    for job_listed in jobs_list:
        driver.execute_script("arguments[0].scrollIntoView();", job_listed )
        ActionChains(driver).move_to_element(job_listed).perform()

    target = driver.find_element_by_class_name("jobs-search-results")
    time.sleep(sleep_time)
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', target)
    driver.implicitly_wait(3)
    time.sleep(sleep_time)

    previous_jobs_length = actual_jobs_length
    jobs_list = driver.find_elements_by_class_name("job-card-list__title")
    actual_jobs_length = len(jobs_list)
```


## Data Cleaning
After scraping the data, I clean it up and made the following changes:
> Data cleaning script file: [data_cleaning.ipynb](https://github.com/diogojfernandes/linkedin_jobs/blob/master/data_cleaning.ipynb)

> Cleaned data CSV file: [cleaned_job_positions.csv](https://github.com/diogojfernandes/linkedin_jobs/blob/master/cleaned_job_positions.csv)

* Job title classification as Data Analyst, Data Engineer or Data Scientist
*	Removed positions outside the data science area
*	Extracted city name from location
*	Parsed numeric data out of number of applicants 
*	Removed employees text from number of employees
*	Deleted unnacessary data from Position Type
*	Fill null values with 'NA' in every column
