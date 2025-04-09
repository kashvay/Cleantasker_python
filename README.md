# Python Test Automation
This project is about automating the regression test cases for the Cleantasker portal and client area. It uses **selenium python with pytest framework**. 
It uses POM model. The test runs in Chrome , Firefox and Edge as parameterized tests. This document describes about how to setup this project in local.

## Pre-requisites
The following softwares needs to be installed
- **Python** (>= 3.8) → [Download Here](https://www.python.org/downloads/). Make sure Add PATH to system variable is selected during installation.
- **Pycharm**
- **Google Chrome** (Latest version) → [Download Here](https://www.google.com/chrome/).
- **Java (for Allure Reports)** → [Download Here](https://www.oracle.com/java/technologies/javase-downloads.html). After installation JAVA HOME variable to be added to PATH variable
- **Allure** (for test reporting) → Installed via archive (see below)

## Installation
1️. **Clone the repository**  
```bash
git clone https://github.com/ICMarkets/icm_automation.git
cd your-repo
```
2. **Install required Python dependencies**

```bash
pip install -r requirements.txt
```
Note: requirements.txt contains all dependencies required in the project. Refer this site [How to create requirement.txt using pipreqs](https://github.com/bndr/pipreqs)

3. **Allure**
    1. Go to the latest [Allure Report release on GitHub](https://github.com/allure-framework/allure2/releases) and download the allure-*.zip or allure-*.tgz archive.
    2. Uncompress the archive into the directory of your choice.
    3. Remember the path to its bin subdirectory.
    4. Add the allure path to PATH variable as mentioned below.
        1. Press Win+R and enter the command: sysdm.cpl to open the System Properties tool.
        2. On the Advanced tab, click Environment variables.
        3. In either the User variables or System variables list, double-click the Path variable to open the editing dialog. Note that editing the system variable requires administrator privileges and affects all users of the computer.
        4. In the Edit environment variable dialog, click New to add a new line entry to the paths list. In the new line, specify the full path to the bin subdirectory from an earlier step, for example: D:\Tools\allure-2.29.0\bin.
        5. If the list contains a path to a previously installed Allure version, delete it.
        6. Click OK to save the changes.

# Running the Tests
- Run all the tests and to generate an Allure report:
```bash
 # run the test alone
pytest your-test-name 

# run test along with allure report
pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```
- Run specific tests inside a tests file and to generate an Allure report: 
```
pytest tests/test_login.py --alluredir=reports/allure-results
```
- To Run Tests in a Specific Directory
  - Run all tests inside a specific folder (tests/):
```
pytest tests/ --alluredir=reports/allure-results
```
 - To Run a Single Test File
```
pytest tests/test_login.py --alluredir=reports/allure-results
```
- To Run a Specific Test Case
```
pytest tests/test_login.py::test_valid_login --alluredir=reports/allure-results
```
- To Run Tests with a Specific Marker
If your tests use markers (e.g., @pytest.mark.smoke), run only smoke tests:
```
pytest -m smoke --alluredir=reports/allure-results
```
