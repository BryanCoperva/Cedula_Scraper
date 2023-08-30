from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
from funciones import *

def find_and_click_element(driver, xpath):
    """
    Find and click an element using its XPath.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        xpath (str): The XPath to locate the element.
    """
    element = driver.find_element(By.XPATH, xpath)
    element.click()

def get_values_from_inputs(driver, input_ids):
    """
    Get values from input elements using their IDs.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        input_ids (list): List of IDs of input elements.

    Returns:
        list: List of values retrieved from the input elements.
    """
    values = [driver.find_element(By.ID, input_id).get_attribute("value") for input_id in input_ids]
    return values




def process_excel_file(init, final, file_path):
    """
    Process an Excel file, perform data transformations, and return a DataFrame.

    Args:
        init (int): Start index for selecting rows from the DataFrame.
        final (int): End index (exclusive) for selecting rows from the DataFrame.
        file_path (str): Path to the Excel file to be processed.

    Returns:
        pandas.DataFrame: A DataFrame with the processed and transformed data.
    """
    df = pd.read_excel(file_path)
    df['Name'] = df.Name.apply(lambda X: X.replace('/', ' ').replace('*', '').rstrip())
    df_filtered = df['Name']
    df_filtered.drop_duplicates(inplace=True)
    df_input = pd.DataFrame(df_filtered).iloc[init:final]
    
    def split_name(name):
        # Implement the split_name function here
        pass
    
    df_input['NameSplit'] = df_input.Name.apply(lambda X: split_name(X))
    df_input['Name'] = df_input.NameSplit.apply(lambda X: X[0])
    df_input['Last Name'] = df_input.NameSplit.apply(lambda X: X[1])
    df_input['Middle Name'] = df_input.NameSplit.apply(lambda X: X[2])
    
    return df_input


def iniciar_scraper(url, execute_zoom=False, zoom_percentage=100):
    """
    Scrapes data from the given URL using SeleniumBase.

    Args:
        url (str): The URL to the webpage to be scraped.
        execute_zoom (bool, optional): Whether to execute a zoom script on the page. Defaults to False.
        zoom_percentage (int, optional): The zoom percentage to set on the page. Defaults to 100.

    Returns:
        None
    """
    driver = Driver(uc=True)
    driver.get(url)

    if execute_zoom:
        zoom_script = f"document.body.style.zoom='{zoom_percentage}%'"
        driver.execute_script(zoom_script)


def split_name(name):
    name = name.replace('*','').replace('/',' ').rstrip()
    #name.replace('/',' ')
    splited = get_name(name)
    if len(splited) <3:
        nam1 = splited[0]
        nam2 = splited[1]
        return [nam1, nam2, None]
    if len(splited) <4:
        nam1 = splited[0]
        nam2 = splited[1]
        nam3 = splited[2]
        return [nam1, nam2, nam3]
    nam1 = ' '.join(splited[:-2])
    nam2 = splited[-2]
    nam3 = splited[-1]
    return [nam1, nam2, nam3]
def get_name(name, inverse=False):
    flag=0
    skips = ['de', 'los', 'la', 'santa', 'del']
    namedir = name.lower().split(' ')
    new_name = list()
    for i in range(len(namedir)):
        word = namedir[i]
        if flag:
            temp.append(namedir[i-1])
        if word in skips:
            if not flag:
                temp = list()
            flag=1
            continue
        if flag:
            temp.append(namedir[i])
            word = ' '.join(temp)
        new_name.append(word)
        flag = 0
    return new_name