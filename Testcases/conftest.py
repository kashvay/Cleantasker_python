import inspect
import json
import os
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from Base import selenium_cmd_helpers
from Utilities.Utils import custom_log, get_abs_file_path
from configfiles.Read_user_inputs import read_test_data
import chrome_version


@pytest.fixture(scope="class")
def read_user_input():
    try:
        user_inputs = read_test_data()
        url,login_title,home_page_title = user_inputs
        if len(user_inputs) < 3:
           fail_with_log("Insufficient data in test data file")
        return {
            "url": url,
            "login_title":login_title,
            "home_page_title": home_page_title
        }
    except Exception as ex:
        custom_log().error("unable to read data - " + str(ex))
        pytest.fail("Failed to read user input")


# Fixture for browsers
@pytest.fixture(params=["chrome","firefox"],scope="class")
def browser(request):
    return request.param

def load_user_data():
    current_file= inspect.getfile(lambda: None)
    file_path = get_abs_file_path(current_file,"dataconfig.json")
    try:
        with open(file_path, "r") as file:
            return json.load(file)["user_logins"]
    except FileNotFoundError:
        custom_log().error("dataconfig.json file not found")
        pytest.fail("User data file is missing")
    except json.JSONDecodeError:
        custom_log().error("Error parsing dataconfig.json")
        pytest.fail("Invalid JSON format in user data file")

# Fixture for user login data
@pytest.fixture( params=load_user_data(),scope="class")
def user_logins(request):
    user = request.param
    allure.dynamic.parameter("username", user["username"])
    allure.attach("******", name="password", attachment_type=allure.attachment_type.TEXT)
    return user


@pytest.fixture(scope="function",autouse=True)
def setup(request,read_user_input,browser,user_logins):
    web_driver = None
    try:
        url = read_user_input["url"]
        login_title = read_user_input["login_title"]
        home_page_title =read_user_input["home_page_title"]

        # Initialize WebDriver based on browser_name
        with allure.step(f"Initialize WebDriver based on browser_name {browser}"):
            if browser == 'chrome':
                chrome_latest_version=chrome_version.get_chrome_version()
                web_driver  = webdriver.Chrome(service=ChromeService(ChromeDriverManager(chrome_latest_version).install()))
            elif browser == 'firefox':
                web_driver =webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            elif browser == 'edge':
                web_driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            else:
                fail_with_log(f"Unsupported browser: {browser}")
            custom_log().info(f"Opened the {browser}  browser")


        # Assign driver to test class
        request.cls.driver = web_driver
        yield web_driver,browser,url,login_title,home_page_title,user_logins

    except Exception as error:
        custom_log().error(f'Unable to launch the browser {request.param} due to error: {error}')

    finally:
        #  Ensure the WebDriver is quit after the test runs if it was created
        if webdriver:
            web_driver.quit()

# Hook to capture test results and quit the WebDriver if the test failed
def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        # Check if the failure was due to pytest.fail
        if getattr(call.excinfo.value, pytest.fail.Exception):
            failure_message = str(call.excinfo.value)
            custom_log().error(f"Test {item.name} failed with message: {failure_message}")
        else:
            custom_log().error(f"Test {item.name} failed. Error: {call.excinfo.value}")

        # Get the WebDriver instance from the test class fixture
        driver = item.cls.driver if hasattr(item.cls, 'driver') else None
        if driver:
            custom_log().error(f"Test {item.name} failed. Quitting WebDriver...")
            driver.quit()

def fail_with_log(message):
    """
    Custom wrapper to log the message before raising pytest.fail
    """
    custom_log().error(f"Test failed with message: {message}")
    pytest.fail(message)