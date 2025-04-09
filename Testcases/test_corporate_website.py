from datetime import datetime

import allure
import pytest
from Base import selenium_cmd_helpers
from Pages.Homepage import  Homepage
from Pages.Login_page import Loginpage
from Utilities.Utils import custom_log



@pytest.mark.usefixtures("setup")
class BasicTest:
    pass

@allure.feature("Registration")
@allure.story("Cleantasker portal verification")
@allure.severity(allure.severity_level.CRITICAL)
class Testcleantasker(BasicTest):


    def setup_method(self):
      self.driver = self.driver


    @pytest.fixture(scope="session")
    def test_run_date(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_successful_login (self,setup,test_run_date):
        try:
            _,browser_name,url,login_title,home_page_title,login_dict = setup
            user_name = login_dict["username"]
            password = login_dict["password"]
            allure.attach(test_run_date, name="Test Run Date", attachment_type=allure.attachment_type.TEXT)
            allure.title(test_run_date)
            Loginpage(self.driver).login_application(user_name,password,browser_name,url,login_title,home_page_title)
        except Exception as error:
            custom_log().error(f"Unable to launch the application due to error {error}")
            raise error

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_failed_login (self,setup,test_run_date):
        try:
            _, browser_name, url, login_title, _, login_dict = setup
            user_name = login_dict["username"]
            password = login_dict["password"]
            allure.attach(test_run_date, name="Test Run Date", attachment_type=allure.attachment_type.TEXT)
            Loginpage(self.driver).failed_login(user_name, password, browser_name, url,
                                                                       login_title)
        except Exception as error:
            custom_log().error("Unable to launch the application")
            raise error


    def test_home_page(self,setup,test_run_date):
        try:
            _, browser_name, url, login_title, home_page_title, login_dict = setup
            user_name = login_dict["username"]
            password = login_dict["password"]
            allure.attach(test_run_date, name="Test Run Date", attachment_type=allure.attachment_type.TEXT)
            allure.title(test_run_date)

            #login the application
            Loginpage(self.driver).login_application(user_name, password, browser_name, url, login_title,
                                                     home_page_title)
            # verify the dashboard
            Homepage(self.driver).perform_dashboard_section(browser_name)

        except Exception as error:
            custom_log().error(f"Unable to proceed with the application due to the error- {error}")
            raise error


