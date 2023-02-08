"""
Author: Justin Pham
Date: 2/4/2023
Description: Allows the user to find the number of results pop up in the SEC EDGAR CIK Lookup Database
"""

# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from fuzzywuzzy import fuzz
from selenium.common.exceptions import NoSuchElementException
import openpyxl

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
    undesired = ["inc.", "limited", "inc", "llc", "llc.", "l.l.c.", "(tiso)", "corp", "corp.", "ltd", "ltd.", "and other issuers", "et al.", "tiso", "l.p.", "lp", "company", "corp", "corporation"]

    # Make all characters lower case and split them into different lists
    temp = name.lower()
    temp = temp.strip(" ")
    temp = temp.split(" ")
    reform_name = ""  # Return value

    # Remove any undesired phrases in the list
    for i in range(len(temp)):
        if temp[i] not in undesired:
            reform_name += temp[i]
            reform_name += " "

    # Change characters to be more readable to the search
    reform_name = reform_name.replace(",", "")
    reform_name = reform_name.replace(".COM", " COM")
    reform_name = reform_name.rstrip(" .s")
    return reform_name

def search_company(name, wait):
    """
    Inputs the company name into the search and searchs for it
    Takes the company name as a parameter
    """
    # Explicit wait for the submit button to be clicked
    wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@id='block-secgov-content']/article/div[1]/div[2]/div[2]/div/div[1]/form/p[1]/input[2]")))

    # Inputs search name into search bar
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
    # Stores the results into a list
    string_results = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td[2]/pre[2]").text
    table = string_results.splitlines()
    match = -1
    current = 0

    # Separate results into separate lists
    for i in range(len(table)):
        table[i] = table[i].strip(" ")
        table[i] = table[i].split("   ")
        table[i][1] = reformat_name(table[i][1])  # Reformat the naming to account for any shifts in adjustments

    # Compares the results to the name and compares it to the best result, storing only the best result
    for i in range(len(table)):
        if fuzz.ratio(name, table[i][1]) > current and fuzz.ratio(name, table[i][1]) > 70:
            current = fuzz.ratio(name, table[i][1])
            match = i

    if match == -1:  # If the match is not found
        return "N/A"
    else:  # If the match is found return the cik number
        return table[match][0]

def click_button(xpath):
    """
    Clicks a button on a website
    """
    temp = driver.find_element(By.XPATH, xpath)
    temp.click()


# Access the Edgar CIK Lookup Webpage
driver = webdriver.Chrome()
file = openpyxl.load_workbook("InvestigationsJul20toSep21.xlsx")
sheet = file['Sheet1']
wait = WebDriverWait(driver, timeout=10)

for x in range(2, 1165):
    print(x)
    driver.get("https://www.sec.gov/edgar/searchedgar/cik")

    # If there is a pop-up on the EDGAR website
    if check_exists_by_xpath("//*[@id='fsrFocusFirst']"):
        click_button("//*[@id='fsrFocusFirst']")

    # Input Search Into the Company Lookup
    company_name = reformat_name(str(sheet["A"+str(x)+""].value))
    # reformat_name(str(input("Input the Name of the Company you wish to search for: ")))
    search_company(company_name, wait)

    # Checks if the Website has loaded
    wait.until(ec.title_is("EDGAR CIK Lookup"))
    assert "EDGAR CIK Lookup" == driver.title

    # If there is a pop-up on the EDGAR website
    if check_exists_by_xpath("//*[@id='fsrFocusFirst']"):
        click_button("//*[@id='fsrFocusFirst']")

    # Finds the number of results
    text = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td[2]/p[1]")
    text = ''.join(filter(str.isdigit, text.text))
    results = int(text)

    cik_num = "N/A"  # output value to .xlsx

    # If there are results to parse through
    if results > 0:
        cik_num = str(find_match(company_name))

    sheet["E"+str(x)+""].value = cik_num

file.save('CIKsForInvestigationsJul10toSep21')
driver.close()
