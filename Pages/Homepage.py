import time
import traceback

import allure
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Base import selenium_cmd_helpers
from Utilities.Utils import custom_log, data_base_validation


class Homepage:
    def __init__(self,driver):
        self.driver = driver
        self.year_column_locator=(By.XPATH,"//div[@class='select-options max-md:w-full'][1]")
        self.month_column_locator=(By.XPATH,"//div[@class='select-options max-md:w-full'][2]")
        self.client_column_locator = (By.XPATH, "//div[@class='select-options max-md:w-full'][3]")
        self.location_column_locator = (By.XPATH, "//div[@class='select-options max-md:w-full'][4]")
        self.manager_column_locator = (By.XPATH, "//div[@class='select-options max-md:w-full'][5]")
        self.go_button_locator=(By.XPATH,"//form//div//button")
        self.report_section=(By.XPATH,"//h3[text()='Daily Tasks']")


    def perform_dashboard_section(self,browser_name):
        try:
            # select the year column

            with allure.step("Select the year column"):
                selenium_cmd_helpers.explicit_wait(self.driver,"visibility",self.year_column_locator)
                year_column = self.driver.find_element(*self.year_column_locator)
                year_column.click()
                time.sleep(1)
                drop_down_locator,drop_down_value=selenium_cmd_helpers.get_dropdown_locator(self.driver,"select__option")
                selenium_cmd_helpers.explicit_wait(self.driver, "visibility", drop_down_locator)
                year_value = self.driver.find_element(*drop_down_locator)
                year_value.click()
                custom_log().info(f"year column selected with the value '{drop_down_value}'")

            # select the month column
            with allure.step("Select the month column"):
                selenium_cmd_helpers.explicit_wait(self.driver, "clickable", self.month_column_locator)
                month_column = self.driver.find_element(*self.month_column_locator)
                month_column.click()
                time.sleep(1)
                drop_down_locator,drop_down_value = selenium_cmd_helpers.get_dropdown_locator(self.driver, "select__option")
                selenium_cmd_helpers.explicit_wait(self.driver, "visibility", drop_down_locator)
                month_column_value = self.driver.find_element(*drop_down_locator)
                month_column_value.click()
                custom_log().info(f"month column selected with the value '{drop_down_value}'")

            # select the client column
            with allure.step("Select the client column"):
                selenium_cmd_helpers.explicit_wait(self.driver, "visibility", self.client_column_locator)
                client_column = self.driver.find_element(*self.client_column_locator)
                client_column.click()
                time.sleep(1)
                drop_down_locator,drop_down_value = selenium_cmd_helpers.get_dropdown_locator(self.driver, "select__option")
                selenium_cmd_helpers.explicit_wait(self.driver, "visibility", drop_down_locator)
                client_column_value = self.driver.find_element(*drop_down_locator)
                client_column_value.click()
                custom_log().info(f"client column selected with the value '{drop_down_value}'")

            # select the location column
            with allure.step("Select the location column"):
                selenium_cmd_helpers.explicit_wait(self.driver, "visibility", self.location_column_locator)
                location_colum = self.driver.find_element(*self.location_column_locator)
                location_colum.click()
                time.sleep(1)
                drop_down_locator,drop_down_value = selenium_cmd_helpers.get_dropdown_locator(self.driver, "select__option")
                selenium_cmd_helpers.explicit_wait(self.driver, "visibility", drop_down_locator)
                location_column_value = self.driver.find_element(*drop_down_locator)
                location_column_value.click()
                custom_log().info(f"location column selected with the value '{drop_down_value}' ")

            # select the manager column
            with allure.step("Select the manager column"):
                selenium_cmd_helpers.explicit_wait(self.driver, "visibility", self.manager_column_locator)
                manager_column = self.driver.find_element(*self.manager_column_locator)
                manager_column.click()
                time.sleep(1)
                drop_down_locator,drop_down_value = selenium_cmd_helpers.get_dropdown_locator(self.driver, "select__option")
                selenium_cmd_helpers.explicit_wait(self.driver, "visibility", drop_down_locator)
                manager_column_value = self.driver.find_element(*drop_down_locator)
                manager_column_value.click()
                custom_log().info(f"manager column selected with the value '{drop_down_value}'")

            with allure.step("Click on Go button"):
                go_button=self.driver.find_element(*self.go_button_locator)
                go_button.click()
                custom_log().info("Go button is clicked")

            with allure.step("Screenshot of the dashboard after loaded with selection"):
                selenium_cmd_helpers.explicit_wait(self.driver, "visibility", self.report_section)
                selenium_cmd_helpers.explicit_wait(self.driver, "javascript_wait")
                time.sleep(2)
                selenium_cmd_helpers.take_screenshot(self.driver, "Dashboard_section", browser_name)


        except Exception as error:
            custom_log().error(f"unable to perform the dashboard verification due to the error {error}\n{traceback.format_exc()}")

