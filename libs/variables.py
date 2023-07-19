import random as _random

BROWSER = "chromium"
NEW_POLL_NAME = f"Poll_{_random.randint(0, 10000)}"

# Open VibeCatch login
LOGIN_PAGE = "https://env-5369504.paas.datacenter.fi/"
ALLOW_COOKIES = "#adroll_allow_all"
LOGIN_BUTTON = "a.login"

# Open and log in
USERNAME_FIELD = "#username"
PASSWORD_FIELD = "#password"
VALID_USERNAME = "test@knowit.com"
VALID_PASSWORD = "Knowit123_"
SUBMIT_CREDENTIAL = "xpath=//input[@value='Login']"

# Log out
LOGOUT_BUTTON = "text=Log out"

# Create new poll
HOME_PAGE = "//img[@alt='VibeCatch']"
CREATE_POLL = "(//*[contains(@class,'btn add-project')])[1]"
ADD_NAME = "#addProjectName"

CREATE_QWL = "//button[normalize-space()='Create a QWL poll']"
SHOW_QWL = "//a[normalize-space()='Show QWL questions']"
CREATE_CUSTOM = "//button[normalize-space()='Create a custom poll']"

# Delete poll
DELETE1 = "//vibe-settings-advanced-button[@class='removal-section']//div[@class='accordionTitle']"
DELETE2 = "//a[@class='btn btn-danger delete-project']"
DELETE3 = "//button[normalize-space()='Delete now']"

# Translate to Finnish
BASIC_SETTINGS = "//vibe-settings-advanced-button[@icon='cog']//div[@class='accordionTitle']"
TRANSLATE = "//span[contains(text(),'Add')]//select[@class='ng-untouched ng-pristine ng-valid']"
ENGLISH = "//div[@class='well']//span[1]//a[1]//i[1]"

# Add email
ADD_EMAIL = "//div[@class='well']//a[@class='btn']"
EMAIL_FIELD = "//textarea[@placeholder='List of recipients']"
ADD_RECIPIENT = "//button[normalize-space()='Add']"
EMAIL = 'teantestaus@gmail.com'
MY_EMAIL = "//span[@tooltip='Click to edit']"
SAVE_CONT = "#saveAndContinue"

# Send immediately
SEND_NOW = "//a[@class='btn']"
SEND_OK = "//button[@type='button']"

# Make_streamlined
QWL_TYPE = "//*[@id='masterContainer']/vibe-settings/div/div[2]/div[2]/div[1]/div[2]/select[1]"
GO_AWAY = "//button[normalize-space()='OK']"

# Change name
SHOW_ALL_QST_BTN = "//a[normalize-space()='Show QWL questions']"
BASIC_SETTINGS = "//vibe-settings-advanced-button[@icon='cog']//div[@class='accordionTitle']"
NAME_FIELD = "//input[@id='projectName']"
SAVE_BTN = "//a[@id='save']"

# View results
QWL_ANALYSIS = "//a[@class='selected']"
NO_EMAIL_NOTIF = "//div[@class='textContainer']"
NO_EMAIL_NOTIF_OK_BTN = "//button[@type='button']"
SEND_NOW_BTN = "//a[@class='btn']"
NOTIFICATION = "//div[@class='textContainer']"
NOTICATION_OK_BTN = "//button[@type='button']"

# Mark as a template
TEMPLATE = """//div[contains(text(),'Save poll as a template, allowing anyone in your o')]
           //input[@type='checkbox']"""
CREATE_FROM_TEMPLATE = "//button[@type='submit']"

# Help options
HELP_BTN = "//a[normalize-space()='Help']"
FAQ = "//a[normalize-space()='Frequently Asked Questions']"
FAQ_TITLE = "//h1[normalize-space()='VibeCatch FAQ']"
TUTORIAL = "//a[normalize-space()='Pulse Poll Tutorial']"
QWL_PLAYGROUND = "//a[normalize-space()='QWL Playground']"
QWL_OVERVIEW = "//vibe-youtube[1]//a[1]"
HELP_WIN = "//h4[@class='modal-title']"

# Poll question options
POLL_FORM_BTN = "//a[@class='relativeLinkToForm']"
MOVE_FORWARD = "//img[@class='ng-scope']"
QUESTIONS = "//div[@class='pageStatus ng-binding']"

# Delete poll
SET_BTN = "//i[@class='fa fa-fw fa-gears fa-fw']"
DEL_BUT1 = "text=Tweak feedback or remove poll"
DEL_BUT2 = "text=Delete this poll and all its feedback completely"
DEL_BUT3 = "text=Delete now"
ADD_Q = """//*[@id='masterContainer']/vibe-settings/div/div[2]/div[2]/
           vibe-settings-resources/div/div/div/a"""
NEW_Q = "#customQuestionText"
ADD_NEW_Q = "//button[@type='submit']//i[@class='fa fa-plus-circle']"
Q_ROW = """//*[@id='masterContainer']/vibe-settings/div/div[2]/div[2]/
           vibe-settings-resources/div/div/div/div/span/a[3]"""
