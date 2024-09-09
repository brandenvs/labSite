import time
import gspread

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.edge.options import Options as EdgeOptions

from google.oauth2 import service_account

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from labSite.settings import CREDS_FILE


class Student:
    def __init__(self, student_name, bootcamp, current_level=0):
        self.fullname = student_name
        self.bootcamp = bootcamp
        self.current_level = current_level

class StuRecord:
    def __init__(self, task_title='No Title', task_status='No Status', task_score='N/A', task_level='No Set'):
        self.task_title = task_title
        self.task_status = task_status
        self.task_score = task_score
        self.task_level = task_level


# Get driver 
def get_driver(port_url: str) -> webdriver.Edge:
    # Set up Microsoft Edge options
    edge_options = EdgeOptions()
    edge_options.add_argument('--headless')  # Run in headless mode
    edge_options.add_argument('--disable-gpu')  # Disable GPU for better compatibility
    edge_options.add_argument('--no-sandbox')  # Bypass OS security model
    edge_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

    # Path to msedgedriver (make sure it's correctly installed)
    driver: webdriver.Edge = webdriver.Edge(options=edge_options, executable_path='/usr/local/bin/msedgedriver')

    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver.get(port_url)

    return driver

# Click accept cookies
def accept_cookies(driver: webdriver.Edge) -> webdriver.Edge:
    print('⌛Waiting for element ...')
    # Waiting until an element is clickable
    accept_cookie = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')))
    accept_cookie.click()

    print('💤Sleeping for 1 seconds ...')
    time.sleep(1)# Snooze 2

    return driver    

# Get student information
def get_student(driver: webdriver.Edge) -> Student:
    # Locate student details
    student_name = driver.find_element(By.CLASS_NAME, 'profile__excerpt-fullname').text
    bootcamp = driver.find_element(By.CLASS_NAME, 'profile__excerpt-bootcamp-level').text
    print(student_name, bootcamp)

    student = Student(student_name, bootcamp)

    return student

# Get task table
def get_table(driver: webdriver.Edge, level: str) -> list[StuRecord]:
    student_records = []

    # Locate table object
    # get_table = driver.find_element(By.CLASS_NAME, 'table')/html/body/div[1]/div/div[2]/div[1]/section[1]/div[3]/div/div[2]/div/table
    if level == 'Level 1':
        get_table = driver.find_element(By.ID, 'jsLevel1')
    elif level == 'Level 2':
        get_table = driver.find_element(By.ID, 'jsLevel2')
    elif level == 'Level 3':
        get_table = driver.find_element(By.ID, 'jsLevel3')
    else:
        get_table = driver.find_element(By.ID, '//div/table[@class="table"]')
        print('Defaulting...')

    # Extract table data
    
    table_body = get_table.find_element(By.TAG_NAME, 'tbody') # Table
    table_rows = table_body.find_elements(By.TAG_NAME, 'tr') # Table rows
    task_titles = [entry.find_element(By.CLASS_NAME, 'jsTaskOverview' ) for entry in table_rows] # Task titles

    task_details = [entry.find_elements(By.TAG_NAME, 'td') for entry in table_rows]

    pos = 0
    for detail in task_details: 

        _title = ''
        _score = 0
        _status = ''

        try:
            _title = task_titles[pos].text
        except Exception as ex:
            print(ex)

        try:
            _status = detail[1].text
        except Exception as ex:
            print(ex)

        try:
            _score = detail[2].text
        except Exception as ex:
            print(ex)
        pos += 1

        student_records.append(StuRecord(
            task_title=_title,
            task_score=_score,
            task_status=_status
        ))
    
    return student_records

# Get Google sheet
def get_worksheet():
    # Set up Google Sheets API credentials and scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Create credentials object
    creds = service_account.Credentials.from_service_account_file(CREDS_FILE, scopes=scope)

    # Authorize gspread with the credentials
    client = gspread.authorize(creds)

    # Open a Google Sheet by URL or by name
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1d-7QcJylWTz5rNUjNjMEhPnFzZUaJ3nne3GgpFzJ9yo/edit')

    # Select a worksheet by index or title
    worksheet = sheet.get_worksheet(0)  # First sheet in the spreadsheet

    return worksheet

# Update Google sheet
def update_values(spreadsheet_id, range_name, value_input_option, _values):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    creds = service_account.Credentials.from_service_account_file(CREDS_FILE, scopes=scope)
    # pylint: disable=maybe-no-member
    try:
        service = build("sheets", "v4", credentials=creds)
        values = _values
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

# Processing information into meaningful metrics
def data_processing(driver: webdriver.Edge, level: str):
    student_tasks = get_table(driver, level) # Student progression details

    print('💤Sleeping for 5 seconds ...')
    time.sleep(5)

    # Task Calculations

    completed = [task for task in student_tasks if str(task.task_status) == 'Completed'] # Completed tasks
    below_100 = [task for task in completed if int(task.task_score) < 100] # Below 100% tasks
    resubmissions = [task for task in below_100 if int(task.task_score) <= 31] # Task resubmissions

    incomplete = [task for task in student_tasks if str(task.task_score) == 'N/A'] # Incomplete tasks (0 attempts)

    total_completed = len(completed)
    total_below = len(below_100)

    total_incomplete = len(incomplete)
    total_resubmissions = len(resubmissions)

    return total_completed, total_below, total_incomplete, total_resubmissions

def main():
    port_urls = [
    'https://www.hyperiondev.com/portfolio/319063/', 
    'https://www.hyperiondev.com/portfolio/289469/'
    ]

    pos = 2

    for url in port_urls:
        count = 0
        driver = get_driver(url) # Start new webdriver
        driver = accept_cookies(driver) # Accept cookie prompt        
        student = get_student(driver) # Student identifier details
        level = 'Level 1'
        while count < 4:
            total_completed, total_below, total_incomplete, total_resubmissions = data_processing(driver, level)
            count += 1

            if count == 0:
                update_values(
                    "1d-7QcJylWTz5rNUjNjMEhPnFzZUaJ3nne3GgpFzJ9yo",
                    f"A{pos}:H{pos}",
                    "USER_ENTERED",
                    [
                        [
                            'Student Name', 
                            'Bootcamp', 
                            'Level',
                            'No.of Completed', 
                            'No.of Incomplete',
                            'No.of Resubmissions',
                            'No.of Below 100s',
                        ],
                    ],
                )
                count += 1

            update_values(
                    "1d-7QcJylWTz5rNUjNjMEhPnFzZUaJ3nne3GgpFzJ9yo",
                    f"A{pos}:H{pos}",
                    "USER_ENTERED",
                    [
                        [
                            str(student.fullname),
                            str(student.bootcamp),
                            str(level),
                            total_completed,
                            total_incomplete,
                            total_resubmissions,
                            total_below,
                        ]
                    ],
                )

            active_nav = driver.find_element(By.XPATH, f"//ul/li[{count}]/a[contains(@class, 'active')]").text

            if str(active_nav).strip() == 'Level 1':
                level_2 = driver.find_element(By.ID, 'jsLevel2Tab')
                
                print('⌛Waiting for element ...')
                # Waiting until an element is clickable
                level_2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'jsLevel2Tab')))
                level_2.click()
                level = 'Level 2'
                pos += 1

            elif str(active_nav) == 'Level 2':
                level_3 = driver.find_element(By.ID, 'jsLevel3Tab')

                print('⌛Waiting for element ...')
                # Waiting until an element is clickable
                level_3 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'jsLevel3Tab')))
                level_3.click()
                level = 'Level 3'
                pos += 1

            else:
                print('All done!\nClosing webdriver.')
                break
        driver.close()
        pos += 1
    return 200

# if __name__ == "__main__":
#     main()
