from numpy import append
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
import logging
import pandas as pd
import requests, re
import time 
import os
from bs4 import BeautifulSoup
import pyautogui

import getpass
import time
import csv

# Driver Configuration
options = Options()
options.add_argument('--start-maximized')
options.add_argument("user-data-dir=C:/Users/Diogo Fernandes/AppData/Local/Google/Chrome/User Data") 

driver = webdriver.Chrome("C:/Users/Diogo Fernandes/Documents/Portfolio/linkedin_positions/chromedriver.exe", options=options)
wait = WebDriverWait(driver, 12)
driver.maximize_window()


# LinkedIn login
#loginURL = "https://www.linkedin.com/uas/login"

#email = os.environ.get('VS_EMAIL')
#password = os.environ.get('VS_PASSWORD')

# driver.get(loginURL)

# element = driver.find_element_by_id("username")
# element.send_keys(email)

# element = driver.find_element_by_id("password")
# element.send_keys(password)

# element.submit()

df = pd.DataFrame(columns = ["Id","Position","Location","Company Name","Num Applicants","Sector","Num Employees","Position Type","Remote","Easy Apply","Job Details"])

# job_title_urls = ['https://www.linkedin.com/jobs/search/?geoId=100364837&keywords=data%20analyst&location=Portugal&start=', 'https://www.linkedin.com/jobs/search/?geoId=100364837&keywords=data%20engineer&location=Portugal&start=', 'https://www.linkedin.com/jobs/search/?geoId=100364837&keywords=data%20scientist&location=Portugal&start=']
job_title_urls = ['https://www.linkedin.com/jobs/search/?geoId=100364837&keywords=data%20scientist&location=Portugal&start=']

for job_title_url in job_title_urls:
    # Loop through the job listings pages
    for page_start in range(0,1000,25):

        # searchURL = "https://www.linkedin.com/jobs/search/?keywords=data%20analyst&location=Portugal&start="+str(page_start)
        searchURL = job_title_url + str(page_start)

        time.sleep(3)
        driver.get(searchURL)
        time.sleep(3)

        # Close messages box
        if page_start == 0:
            try:
                driver.find_element_by_class_name("msg-overlay-bubble-header__button").click()
            except:
                try:
                    driver.find_element_by_class_name("msg-overlay-list-bubble__convo-card-content").click()
                except:
                    pass

        # Scroll jobs listings until all elements load
        jobs_list = driver.find_elements_by_class_name("job-card-list__title")
        actual_jobs_length = len(jobs_list)
        previous_jobs_length = 0

        while len(jobs_list)<25 and previous_jobs_length != actual_jobs_length:
            for job_listed in jobs_list:
                driver.execute_script("arguments[0].scrollIntoView();", job_listed )
                ActionChains(driver).move_to_element(job_listed).perform()
            
            target = driver.find_element_by_class_name("jobs-search-results")
            time.sleep(1)
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', target)
            driver.implicitly_wait(3)
            time.sleep(1)

            previous_jobs_length = actual_jobs_length
            jobs_list = driver.find_elements_by_class_name("job-card-list__title")
            actual_jobs_length = len(jobs_list)

        # Find job postings
        all_jobs = []
        all_jobs = driver.find_elements_by_class_name("job-card-list")

        job_index = 0
        for job in all_jobs:
            try:
                #Click on post to expand job details
                time.sleep(1)
                ActionChains(driver).move_to_element(job).perform()
                job.click()
                driver.execute_script("return arguments[0].scrollIntoView(0, document.documentElement.scrollHeight-1);", job)

                field_id = 'N/A'
                field_position = 'N/A'
                field_companyName = 'N/A'
                field_location = 'N/A'
                field_num_applicants = '0 applicants'
                field_position_type = 'N/A'
                field_num_employees = 'N/A'
                field_sector = 'N/A'
                field_remote = False
                field_easy_apply = False
                field_job_details = 'N/A'

                # Job card main data (Position Title, Company Name, Location)
                result_html = job.get_attribute('innerHTML')
                soup = BeautifulSoup(result_html, 'html.parser')

                try:
                    url = driver.current_url
                    field_id = url.split("currentJobId=")[1].split("&")[0]
                except:
                    pass

                try:
                    field_position = soup.find("a", class_ = "job-card-list__title").text.replace('\n','').strip()
                except:
                    pass

                try:
                    field_companyName = soup.find(class_ = "job-card-container__company-name").text.replace('\n','').strip()
                except:
                    pass
                
                try:
                    field_location = soup.find(class_ = "job-card-container__metadata-item").text.replace('\n','').strip()
                except:
                    pass

                try:
                    field_num_applicants = soup.find(class_ = "job-card-container__applicant-count").text
                except:
                    pass

                try:
                    if 'Easy Apply\n' in soup.text:
                        field_easy_apply = True
                except:
                    pass

                try: 
                    if 'Remote' in soup.text:
                        field_remote = True
                except:
                    pass

                try:
                    field_job_details = driver.find_element_by_xpath("//*[@id='job-details']/span").text
                except:
                    pass
                # print(field_job_details)
                    
                # Job card secondary data, only avaiable after selecting job posting 
                positions_info = []
                positions_info = driver.find_elements_by_class_name("jobs-unified-top-card__job-insight")
                section_index = 0

                if len(positions_info) > 0:
                    for position_info in positions_info:
                        try:
                            result_html2 = position_info.get_attribute('innerHTML')
                            soup2 = BeautifulSoup(result_html2, 'html.parser')

                            # print(position_info.text)

                            try:
                                if section_index == 0:
                                    field_position_type = position_info.text
                                    # print(field_position_type)
                            except:
                                pass

                            try:
                                if 'employees' in position_info.text:
                                    field_num_employees = position_info.text.split(' · ')[0]
                                    # print(field_num_employees)
                            except:
                                pass
                                    
                            try:
                                if 'employees' in position_info.text:
                                    field_sector = position_info.text.split(' · ')[1]
                                    # print(field_sector)
                            except:
                                pass

                            section_index += 1
                        except:
                            pass
            
                # Add current selected job listing to dataframe
                df = df.append({"Id":field_id,
                                "Position":field_position,
                                "Location":field_location,
                                "Company Name":field_companyName,
                                "Num Applicants":field_num_applicants,
                                "Sector":field_sector,
                                "Num Employees":field_num_employees,
                                "Position Type":field_position_type,
                                "Remote":field_remote,
                                "Easy Apply":field_easy_apply,
                                "Job Details":field_job_details}, ignore_index=True)
                
                job_index += 1

                print(str(len(df)) + " jobs collected!")
            except:
                pass

    # Save dataframe to CSV file
    df.to_csv("job_positions.csv", index=False, encoding='utf-16', mode='a')

# Close webdriver
driver.quit()






