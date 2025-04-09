import inspect
import logging
import os
import pyodbc


def custom_log():

    # create logger
    logger_name = str(inspect.stack()[1][3])
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()

    #logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    # create file handler and define the log file name
    filehandler = logging.FileHandler(filename='execution.log', mode='a')
    # define the format for the log
    formatter = logging.Formatter('%(asctime)s | %(levelname)s : %(name)s | %(message)s')
    # set the formatter to the file
    filehandler.setFormatter(formatter)
    # add the filehandler to the logger
    logger.addHandler(filehandler)
    return logger

def data_base_validation(sql_query,environment):
       # get the db credentials from environment variables
       db_server_name = os.getenv(f'{environment}_db_server_name')
       db_user_name = os.getenv(f'{environment}_db_user_name')
       db_password = os.getenv(f'{environment}_db_password')
       db_name = os.getenv(f'{environment}_db_name')

       # Check if all environment variables are set
       if not all([db_server_name, db_user_name, db_password, db_name]):
           custom_log().error("One or more environment variables for DB connection are missing.")
           return None
       try:
           custom_log().info("Connecting to the database...")
           db_constructing = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_server_name};DATABASE={db_name};UID={db_user_name};PWD={db_password}'
           conn = pyodbc.connect(db_constructing)
           cursor = conn.cursor()
           custom_log().info("Executing query...")
           cursor.execute(sql_query)
           result = cursor.fetchall()
           custom_log().info("Query executed successfully.")

           conn.close()
           custom_log().info("Database connection closed.")
           return result
       except KeyError as e:
           custom_log().error(f"Missing environment variable: {e}")
       except Exception as e:
           custom_log().error(f"An error occurred: {e}")
           return None

def get_abs_file_path(current_file,file_name):
    try:
        file_path = None
        base_path = os.path.abspath(os.path.join(current_file, '..', '..'))
        if file_name=="dataconfig.json":
            file_path = os.path.abspath(os.path.join(base_path, 'configfiles', str(file_name)))

        if os.path.exists(file_path):
            return file_path
    except (FileExistsError , FileNotFoundError) as error:
        custom_log().error(f"Unable to find file -{file_name} ")

class Utils:
    pass















