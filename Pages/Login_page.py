import time
import traceback

import allure
from selenium.webdriver.common.by import By

from Base import selenium_cmd_helpers
from Testcases.conftest import fail_with_log
from Utilities.Utils import custom_log


class Loginpage:
    def __init__(self,driver):
        self.driver = driver
        self.user_name_element =(By.NAME,'username')
        self.password_element = (By.NAME,'password')
        self.submit_btn_element= (By.XPATH,"//button[contains(text(),'Sign In')]")
        self.failed_msg_element=(By.XPATH,"//p[@class='text-destructive text-sm mt-2']")

    def login_application(self,user_name,password,browser_name,url,login_title,home_page_title):  #(user_name,password,browser_name,url,page_title)
        try:
            # Navigate to URL and validate page title
            with allure.step(f"Navigate to URL {url} and validate page title"):
                custom_log().info("Open the URL")
                self.driver.get(url)
                custom_log().info(f"Launching website: {url} using {browser_name.capitalize()} browser.")
                self.driver.maximize_window()
                self.driver.implicitly_wait(10)

                # verify login title
            with allure.step(f"verify the application is available with the expected title {login_title}"):
                verify_status,actual_title = selenium_cmd_helpers.verify_title(self.driver, login_title, browser_name)
                if verify_status:
                    with allure.step("Application is available"):
                        selenium_cmd_helpers.take_screenshot(self.driver, "login_page", browser_name)
                        custom_log().info(f"The title matched successfully with the value {login_title}")

                else:
                    with allure.step("Application is not available due to some error. Refer to log for more details"):
                        custom_log().error(f"The title {actual_title} doesn't match with the expected title {login_title}")

            #Login to the application
            with allure.step(f"Login the application for the user name {user_name} "):
                custom_log().info(f"Logging the application using user name {user_name}")

                input_user_name =self.driver.find_element(*self.user_name_element)
                input_user_name.send_keys(user_name)
                custom_log().info("user name field entered")

                input_password = self.driver.find_element(*self.password_element)
                input_password.send_keys(password)
                custom_log().info("password field entered")

                submit_button= self.driver.find_element(*self.submit_btn_element)
                submit_button.click()
                custom_log().info("submit button clicked")


            #verify the credentials
            with allure.step("verify the customer logged in successfully"):
                with allure.step("validate the title after successfully logged in the application"):
                    custom_log().info("compare the title of the application after logged in ")
                    verify_status,actual_title = selenium_cmd_helpers.verify_title(self.driver, home_page_title, browser_name)
                    if verify_status:
                        with allure.step("customer logged in successfully"):
                            #need this delay to take screenshot after a pause
                            time.sleep(2)
                            selenium_cmd_helpers.take_screenshot(self.driver, "login_page", browser_name)
                            custom_log().info(f"The title matched successfully with the value {home_page_title}")
                    else:
                        custom_log().error(f"The title {actual_title}  doesn't match with the expected title {home_page_title}")


        except Exception as error:
            custom_log().error(f"Unable to launch the application due to error: {error}\n{traceback.format_exc()}")


    def failed_login(self,user_name,password,browser_name,url,login_title):
        try:
            # Navigate to URL and validate page title
            with allure.step(f"Navigate to URL {url} and validate page title"):
                custom_log().info("Open the URL")
                self.driver.get(url)
                custom_log().info(f"Launching website: {url} using {browser_name.capitalize()} browser.")
                self.driver.maximize_window()
                self.driver.implicitly_wait(10)

                # verify login title
            with allure.step(f"verify the application is available with the expected title {login_title}"):
                verify_status,actual_title = selenium_cmd_helpers.verify_title(self.driver, login_title, browser_name)
                if verify_status:
                    with allure.step("Application is available"):
                        custom_log().info(f"The title matched successfully with the value {login_title}")

                else:
                    with allure.step("Application is not available due to some error. Refer to log for more details"):
                        custom_log().error(f"The title {actual_title}  doesn't match with the expected title {login_title}")

            #Login to the application
            with allure.step(f"Login the application for the user name {user_name} "):
                custom_log().info(f"Logging the application using user name {user_name}")

                input_user_name =self.driver.find_element(*self.user_name_element)
                input_user_name.send_keys(user_name)
                custom_log().info("user name field entered")

                input_password = self.driver.find_element(*self.password_element)
                input_password.send_keys(password+"#!@") # entering wrong password
                custom_log().info("password field entered")

                submit_button= self.driver.find_element(*self.submit_btn_element)
                submit_button.click()
                custom_log().info("submit button clicked")
                self.driver.implicitly_wait(10)

            #verify the credentials
            with allure.step("Verify the Invalid message displayed"):
                invalid_msg_element = self.driver.find_element(*self.failed_msg_element)
                failed_msg = invalid_msg_element.text
                if failed_msg == "Invalid login credentials":
                    with allure.step("Invalid login credentials message shown successfully"):
                        custom_log().error("wrong credentials entered, please try again")
                        selenium_cmd_helpers.take_screenshot(self.driver, "open_corp_site", browser_name)

        except Exception as error:
            custom_log().error(f"Unable to launch the application due to error: {error}\n{traceback.format_exc()}")
