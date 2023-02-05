"""
Author: Justin Pham
Date: 2/4/2023
Description: Allows the user to find the number of results pop up in the SEC EDGAR CIK Lookup Database
"""

# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import title_is
from selenium.webdriver.support.wait import WebDriverWait
import time

# Access the Edgar CIK Lookup Webpage
driver = webdriver.Chrome()
driver.get("https://www.sec.gov/edgar/searchedgar/cik")
assert "SEC.gov" in driver.title
time.sleep(2)  # Allows elements to load

# Input Search Into the Company Lookup
company_name = str(input("Input the Name of the Company you wish to search for: "))
search = driver.find_element(By.NAME, "company")
search.clear()
search.send_keys(company_name)

# Clicks the Submit Button
submit_xpath = "//*[@id='block-secgov-content']/article/div[1]/div[2]/div[2]/div/div[1]/form/p[1]/input[2]"
submit = driver.find_element(By.XPATH, submit_xpath)
submit.click()

# Checks if the Website has loaded
WebDriverWait(driver, timeout=10).until(title_is("EDGAR CIK Lookup"))
assert "EDGAR CIK Lookup" == driver.title

# Finds the number of results
text = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td[2]/p[1]")
results = int(text.text[16])
print(results)

driver.close()