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

def search_company(name):
    """
    Inputs the company name into the search and searchs for it
    Takes the company name as a parameter
    """
    search = driver.find_element(By.NAME, "company")
    search.clear()
    search.send_keys(name)

    # Clicks the Submit Button
    submit_xpath = "//*[@id='block-secgov-content']/article/div[1]/div[2]/div[2]/div/div[1]/form/p[1]/input[2]"
    submit = driver.find_element(By.XPATH, submit_xpath)
    submit.click()
    return


def find_match():
    """
    Finds the matching CIK number to the company name
    Assumes that the search will always match the result with the least amount characters
    Returns an int of where the result is located in the HTML code
    """
    string_results = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td[2]/pre[2]").text
    table = string_results.splitlines()
    match = -1

    # Separate results into separate lists
    for i in range(len(table)):
        table[i] = table[i].strip(" ")
        table[i] = table[i].split("   ")

    for i in range(len(table)):
        if i == 0:
            match = i
        elif len(table[i][1]) < len(table[match][1]):
            match = i

    return table[match][0]

# Access the Edgar CIK Lookup Webpage
driver = webdriver.Chrome()
driver.get("https://www.sec.gov/edgar/searchedgar/cik")
assert "SEC.gov" in driver.title
time.sleep(2)  # Allows elements to load

# Input Search Into the Company Lookup
company_name = str(input("Input the Name of the Company you wish to search for: "))
search_company(company_name)

# Checks if the Website has loaded
WebDriverWait(driver, timeout=10).until(title_is("EDGAR CIK Lookup"))
assert "EDGAR CIK Lookup" == driver.title

# Finds the number of results
text = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td[2]/p[1]")
results = int(text.text[16])
cik_num = "N/A"

# If there are results to parse through
if results > 0:
    cik_num = str(find_match())

print(cik_num)

driver.close()

# /html/body/table/tbody/tr/td[2]/pre[2]/text()[3] " + str((i+1)) + "
# /html/body/table/tbody/tr/td[2]/pre[2]/text()[1]
# /html/body/table/tbody/tr/td[2]/pre[2]/a[2]
# /html/body/table/tbody/tr/td[2]/pre[2]/text()[2]
