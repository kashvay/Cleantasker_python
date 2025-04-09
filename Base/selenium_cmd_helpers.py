import datetime
import os

import allure
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.Utils import custom_log


def select_dropdown(select_type, find_element_value, text, driver):
    try:
        element = driver.find_element_by_xpath(find_element_value)
        select_element = select.Select(element)
        if select_type == 'value':
            select_element.select_by_value(text)
        else:
            select_element.select_by_index(text)
    except select_dropdown as e:
        custom_log().error('Unable to select dropdown' + str(e))



def javascript_executor(driver, element, jstype):
    try:
        web_element= element
        if jstype.lower() == 'click':
            driver.execute_script("arguments[0].click();", web_element)
        elif jstype.lower() == 'scroll':
            driver.execute_script("arguments[0].scrollIntoView();", web_element)
    except javascript_executor as e:
        custom_log().error('JavaScript executor failed'+ str(e))

def explicit_wait(driver,wait_type,element=None,text=None):
    try:

        wait = WebDriverWait(driver, 20)
        if wait_type.lower()=='clickable':
            wait.until(EC.element_to_be_clickable(element))

        elif wait_type.lower()=='text_to_be_present':
            wait.until(EC.text_to_be_present_in_element(element,text))

        elif wait_type.lower()=='presence_of_element_located':
            wait.until(EC.presence_of_element_located(element))

        elif wait_type.lower()=='title_check':
            wait.until(EC.title_contains(element))

        elif wait_type.lower()=='visibility':
            wait.until(EC.visibility_of_element_located(element))

        elif wait_type.lower()=='javascript_wait':
            wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        return wait

    except TimeoutException as e:
        if wait_type.lower() == 'clickable':
            custom_log().error('Timeout while waiting for element to be clicked: ' + str(e))
        elif wait_type.lower()=='text_to_be_present':
            custom_log().error('Timeout while waiting for the text to be present: ' + str(e))
        elif wait_type.lower()=='presence_of_element_located':
            custom_log().error('Timeout while waiting for element to be visible: ' + str(e))
        elif wait_type.lower()=='title_check':
            custom_log().error('Timeout while waiting for title to be checked: ' + str(e))
        elif wait_type.lower()=='visibility':
            custom_log().error('Timeout while waiting for the visibility of the element:  ' + str(e))
        elif wait_type.lower()=='javascript_wait':
            custom_log().error('Timeout while waiting for the javascript load:  ' + str(e))

def get_shadow_root(driver, locator_data):
    shadow_root=None
    try:
        shadow_root=driver.find_element(By.ID, locator_data).shadow_root
    except NoSuchElementException as e:
        custom_log().error('Shadow root element not found'+ str(e))
    return shadow_root

def take_screenshot(driver,test_name,browser_name):
    try:
        # Get the current timestamp for the image name
        today = datetime.datetime.now()
        image_name = today.strftime("%d-%m-%Y %H:%M:%S").replace(" ", "_").replace(":",
                                                                                   "-")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        screenshot_dir = os.path.join(project_root,"Screenshots")
        screenshot_name= f"{test_name}_{browser_name}_{image_name}.png"

        # Capture and attach screenshot to Allure without saving to disk
        allure.attach(
            driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG
        )
        custom_log().info(f"Screenshot named {screenshot_name } saved to allure report")
    except NoSuchElementException as e:
        custom_log().info(f'Screenshot not taken due to error: {str(e)}')
    except Exception as e:
        custom_log().info(f"An error occurred while taking the screenshot: {str(e)}")

def verify_title(driver,expected_title,browser_name):
    verified_title= True
    explicit_wait(driver,'title_check',expected_title)
    title=driver.title
    if title != expected_title:
        take_screenshot(driver, "initial_setup", browser_name)
        verified_title=False
        return verified_title,title
        #raise Exception(f"Page title mismatch. Expected: '{expected_title}', but got: '{title}'")

    else:
        return verified_title,title

def get_dropdown_locator(driver,class_name):
    """ this function is used to get the locate the drop_down
    by looking for first value only"""
    first_dropdown_value = driver.find_element(By.XPATH, "//div[contains(@class, '"+str(class_name)+"')]").text
    drop_down_locator = (By.XPATH, "//div[contains(@class, '"+str(class_name)+"') and .//div[text()='" + str(
        first_dropdown_value) + "']]")
    return drop_down_locator,first_dropdown_value

class Selenium_Cmd_Helpers:

    def __init__(self, driver):
        self.driver = driver




