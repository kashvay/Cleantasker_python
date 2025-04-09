import json
import os
import random

from Utilities import Utils
from Utilities.Utils import custom_log



def read_test_data():
    url = None
    web_page_title = None
    login_title= None
    home_page_title= None


    try:
        # open the data config file in the mentioned location
        file_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "dataconfig.json"))
        with open(file_path,'r') as file:
            jsonobj = json.load(file)
        # loop through thw JSON file for all settings and assign to local variable.
        for i in jsonobj:
            if i == 'app_url':
                url = str(jsonobj[i])

            elif i =='app_titles':
                for app_tl in jsonobj["app_titles"]:
                    login_title=str(app_tl["login_title"])
                    home_page_title = str(app_tl["home_page_title"])

        custom_log().info("The test data fetched successfully")

    except Exception as e:
        custom_log().info("Unable to fetch the test data due to   " + str(e))

    # return all the assigned variable
    return url, login_title,home_page_title


class Read_user_inputs:
    def __init__(self):
     self.log =Utils.custom_log()




