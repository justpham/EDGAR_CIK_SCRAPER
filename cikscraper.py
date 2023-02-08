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
from fuzzywuzzy import fuzz
from selenium.common.exceptions import NoSuchElementException

def check_exists_by_xpath(xpath):
    """
    Checks if xpath exist within a given webpage
    """
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def reformat_name(name):
    """
    Removes undesired phrases in a string; also replaces . with a space
    """
    undesired = ["inc.", "inc", "llc", "llc.", "l.l.c.", "(tiso)", "corp", "corp.", "ltd", "ltd.", "and other issuers", "et al.", "tiso"]

    temp = name.lower()
    temp = temp.strip(" ")
    temp = temp.split(" ")
    reform_name = ""

    for i in range(len(temp)):
        if temp[i] not in undesired:
            reform_name += temp[i]
            reform_name += " "

    reform_name = reform_name.replace(",", "")
    reform_name = reform_name.replace(".", " ")
    reform_name = reform_name.strip(" ")
    return reform_name

def search_company(name):
    """
    Inputs the company name into the search and searchs for it
    Takes the company name as a parameter
    """
    search = driver.find_element(By.NAME, "company")
    search.clear()
    search.send_keys(name)

    # Clicks the Submit Button
    click_button("//*[@id='block-secgov-content']/article/div[1]/div[2]/div[2]/div/div[1]/form/p[1]/input[2]")
    return

def find_match(name):
    """
    Finds the matching CIK number to the company name
    Assumes that the search will always match the result with the least amount characters
    Returns an int of where the result is located in the HTML code
    """
    string_results = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td[2]/pre[2]").text
    table = string_results.splitlines()
    match = -1
    current = 0

    # Separate results into separate lists
    for i in range(len(table)):
        table[i] = table[i].strip(" ")
        table[i] = table[i].split("   ")
        table[i][1] = reformat_name([i][1])

    # Need to add functionality to truncate LLC, LTD, etc. from end of the results

    for i in range(len(table)):
        if fuzz.ratio(name, table[i][1]) > current:
            current = fuzz.ratio(name, table[i][1])
            match = i

    if match == -1:
        return "N/A"
    else:
        return table[match][0]

def click_button(xpath):
    """
    Clicks a button on a website
    """
    temp = driver.find_element(By.XPATH, xpath)
    temp.click()


# Access the Edgar CIK Lookup Webpage
driver = webdriver.Chrome()
driver.get("https://www.sec.gov/edgar/searchedgar/cik")
assert "SEC.gov" in driver.title
time.sleep(2)  # Allows elements to load

# Input Search Into the Company Lookup
company_name = reformat_name(str(input("Input the Name of the Company you wish to search for: ")))
search_company(company_name)

# Checks if the Website has loaded
WebDriverWait(driver, timeout=10).until(title_is("EDGAR CIK Lookup"))
assert "EDGAR CIK Lookup" == driver.title

# If there is a pop-up on the EDGAR website
if check_exists_by_xpath("//*[@id='fsrFocusFirst']"):
    click_button("//*[@id='fsrFocusFirst']")

# Finds the number of results
text = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td[2]/p[1]")
results = int(text.text[16])
cik_num = "N/A"  # output value to csv

# If there are results to parse through
if results > 0:
    cik_num = str(find_match(company_name))

print(cik_num)
time.sleep(1)

# Goes back to the Search Page
click_button("/html/body/table/tbody/tr/td[2]/a")

driver.close()
