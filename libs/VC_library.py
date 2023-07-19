import os
import PyPDF2
import time
import random as _random
from datetime import date, datetime, timedelta
from enum import Enum, auto

from playwright.sync_api import Browser, sync_playwright, expect
from robot.api.deco import keyword, library
from robot.api import logger

import variables


class Browser(Enum):
    """Available browsers."""
    CHROMIUM = auto()
    FIREFOX = auto()


@library(scope='SUITE')
class VC_library:
    """ A library providing keywords for testing functionality of *VibeCatch*
    website (vibecatch.com) in testing environment.
    """

    def __init__(self):
        self.poll_name = ''
        self.playwright = None
        self.browser = None
        self.popup_info = None
        self.page = None
        self.year = date.today().year
        self.popup_info = None
        self.newpage = None
        self.pdf_download = None
        self.full_filename = ''

    @keyword
    def open_browser(self, browser: Browser = Browser.CHROMIUM, headless: bool = False):
        """Opens a new browser. By default browser is _Chromium_.
        Test suite can also be set to use _Firefox_ as a browser.
        """
        self.playwright = sync_playwright().start()
        if browser is Browser.CHROMIUM:
            browser = self.playwright.chromium
        elif browser is Browser.FIREFOX:
            browser = self.playwright.firefox
        self.browser = browser.launch(headless=headless, slow_mo=0)

    @keyword
    def open_login(self):
        """Opens new page to VibeCatch website and clicks the login-button."""
        self.page = self.browser.new_page()
        self.page.set_viewport_size({"width": 1280, "height": 580})
        self.page.goto(variables.LOGIN_PAGE)
        try:
            time.sleep(3)
            expect(self.page).to_have_title('Next generation job satisfaction polls | VibeCatch')
        except AssertionError as err:
            logger.info(err)
            raise AssertionError('The right page was not opened')
        if self.page.locator(variables.ALLOW_COOKIES).is_visible():
            self.page.click(variables.ALLOW_COOKIES)
        self.page.click(variables.LOGIN_BUTTON)

    @keyword
    def open_vibecatch_and_log_in(self):
        """Opens new page to VibeCatch website and logs in."""
        self.open_login()
        self.submit_credentials(variables.VALID_USERNAME, variables.VALID_PASSWORD)
        try:
            expect(self.page).to_have_title('VibeCatch', timeout=10000)
            logger.info('Login succesful!')
        except AssertionError as err:
            logger.info(err)
            raise AssertionError('Login was not succesful')

    @keyword
    def submit_credentials(self, username: str, password: str):
        """Submits given ``username`` and ``password`` as login credentials."""
        self.page.fill(variables.USERNAME_FIELD, username)
        self.page.fill(variables.PASSWORD_FIELD, password)
        self.page.click(variables.SUBMIT_CREDENTIAL)

    @keyword
    def login_should_succeed(self):
        """Verifies login has succeeded by checking home page is open."""
        try:
            expect(self.page).to_have_title('VibeCatch')
            logger.info('Login was succesful')
        except AssertionError as err:
            logger.info(err)
            raise AssertionError('Login was not succesful')

    @keyword
    def login_should_fail(self, username: str, password: str):
        """Submits given invalid credentials (``username``, ``password``) at login.
        Verifies login has failed by checking username field is still enabled.
        """
        self.submit_credentials(username, password)
        try:
            expect(self.page.locator(variables.USERNAME_FIELD)).to_be_enabled()
        except AssertionError as err:
            logger.info(err)
            raise AssertionError(f'Login should not have succeeded with {username} and {password}')

    @keyword
    def logout(self):
        """Logs out, waits for page to load and verifies login button is enabled."""
        expect(self.page.locator(variables.LOGOUT_BUTTON)).to_be_enabled()
        self.page.click(variables.LOGOUT_BUTTON)
        logger.info('Log out button clicked')
        expect(self.page.locator(variables.LOGIN_BUTTON)).to_be_enabled(timeout=10000)

    def initiate_poll(self):
        self.go_to_home_page
        self.page.click(variables.CREATE_POLL)
        try:
            expect(self.page.locator(variables.ADD_NAME)).to_be_enabled()
        except AssertionError as err:
            logger.info(err)
            raise AssertionError('Create-buttons are not pushed correctly')

    @keyword
    def create_new_poll(self):
        """Creates new QWL poll.
        Poll is named "Poll_x" with _x_ being random number between 0 and 9999.
        """
        self.poll_name = f'Poll_{_random.randint(0, 10000)}'
        self.initiate_poll()
        self.page.fill(variables.ADD_NAME, self.poll_name)
        self.page.click(variables.CREATE_QWL)
        try:
            expect(self.page.locator(variables.SHOW_QWL)).to_be_enabled()
        except AssertionError as err:
            logger.info(err)
            raise AssertionError('New poll was not created succesfully')

    @keyword
    def create_new_custom_poll(self):
        """Creates a new custom poll. Poll is named "Poll_x"
        with _x_ being random number between 0 and 9999.
        """
        self.poll_name = f'Poll_{_random.randint(0, 10000)}'
        self.initiate_poll()
        self.page.fill(variables.ADD_NAME, self.poll_name)
        self.page.click(variables.CREATE_CUSTOM)
        try:
            expect(self.page.locator(variables.ADD_Q)).to_be_enabled()
        except AssertionError as err:
            logger.info(err)
            raise AssertionError('New poll was not created succesfully')

    @keyword
    def create_poll_with_empty_namefield(self):
        """Tries to create new QWL poll with empty namefield."""
        self.initiate_poll()
        self.page.fill(variables.ADD_NAME, "")
        self.page.click(variables.CREATE_QWL)

    @keyword
    def create_new_poll_using_template(self):
        """Creates new QWL poll using another poll as a template.
        Poll is named "Poll_x" with _x_ being random number between 0 and 9999.
        """
        self.initiate_poll()
        self.page.fill(variables.ADD_NAME, variables.NEW_POLL_NAME)
        self.page.locator("//select").select_option(label=self.poll_name)
        self.page.click(variables.CREATE_FROM_TEMPLATE)
        logger.info(f'New poll created using {self.poll_name} as a template')

    @keyword
    def creating_poll_should_fail(self):
        """Waits for 3 seconds before verifying creating poll has failed."""
        time.sleep(3)
        try:
            expect(self.page.locator(variables.CREATE_QWL)).to_be_visible()
            logger.info('New poll was not created')
        except AssertionError as err:
            logger.info(err)
            raise AssertionError('New poll should have not been created')

    @keyword
    def poll_should_exist(self, poll_name: str = ""):
        """Verifies poll can be found in poll listing."""
        if poll_name == "":
            poll_name = self.poll_name
        self.go_to_home_page()
        try:
            expect(self.page.locator(f"//a[text()='{poll_name}']")).to_be_visible()
            logger.info(f"New poll '{poll_name}' was created succesfully")
        except AssertionError as err:
            logger.info(err)
            raise AssertionError('New poll was not created succesfully')

    @keyword
    def poll_should_not_exist(self, poll_name: str = ""):
        """Verifies poll can't be found in poll listing."""
        if poll_name == "":
            poll_name = self.poll_name
        self.go_to_home_page()
        if self.page.locator(f"//a[text()='{poll_name}']").is_visible():
            raise AssertionError('New poll was not deleted succesfully')
        else:
            logger.info(f"'{poll_name}' does not exist anymore")

    @keyword
    def go_to_home_page(self):
        """Goes to home page by clicking the home page button."""
        self.page.click(variables.HOME_PAGE)
        try:
            expect(self.page.locator(variables.CREATE_POLL)).to_be_visible()
        except AssertionError as err:
            logger.info(err)
            raise AssertionError("Failed to open home page.")

    def go_to_poll_settings(self, poll_name: str = ""):
        """Opens poll settings from the poll listing view using the settings button."""
        if poll_name == "":
            poll_name = self.poll_name
        set_btn = f"""(//div[@class='row projectRow']//*[text()='{poll_name}']
                       /../../following-sibling::div)[4]//a[3]"""
        time.sleep(5)
        try:
            expect(self.page.locator(set_btn)).to_be_enabled()
            self.page.locator(set_btn).click()
            logger.info(f'Going to the settings of {poll_name}')
        except AssertionError as error:
            logger.info(error)
            raise AssertionError('Was not able to find the poll')

    @keyword
    def add_email(self):
        """Opens poll settings and adds email address (as saved in variable file) to poll
        recipient list.
        """
        if self.page.locator(variables.CREATE_POLL).is_visible():
            self.go_to_poll_settings()
        self.page.click(variables.ADD_EMAIL, timeout=3000)
        self.page.fill(variables.EMAIL_FIELD, variables.EMAIL)
        self.page.click(variables.ADD_RECIPIENT)
        logger.info("Email is added")
        expect(self.page.locator(variables.ADD_RECIPIENT)).not_to_be_visible()
        expect(self.page.locator(variables.MY_EMAIL)).to_be_visible()
        expect(self.page.locator(variables.SAVE_BTN)).to_be_visible(timeout=30000)
        self.page.locator(variables.SAVE_BTN).click(timeout=30000)
        logger.info("Changes saved")

    @keyword
    def send_feedback_request_now(self, poll_name: str = ""):
        """Sends feedback request email immediately using the send button in poll listing.
        If there is no email added, an error with the message "Add an email address!" is raised.
        """
        if poll_name == "":
            poll_name = self.poll_name
        timestamp = f"""(//div[@class='row projectRow']//*[text()='{poll_name}']
                    /../../following-sibling::div)[2]"""
        send_now_set_btn = f"""(//div[@class='row projectRow']//*[text()='{poll_name}']
                           /../../following-sibling::div)[4]//a[4]"""
        self.go_to_home_page()
        try:
            expect(self.page.locator(send_now_set_btn)).to_be_visible()
            self.page.locator(send_now_set_btn).click()
            if self.page.locator(variables.NO_EMAIL_NOTIF).is_visible():
                self.page.locator(variables.NO_EMAIL_NOTIF_OK_BTN).click()
                raise AssertionError('Not possible to send the feedback request, email is missing!')
            else:
                self.page.locator(variables.SEND_NOW_BTN).click()
                self.page.locator(variables.NOTIFICATION).click()
                self.page.locator(variables.NOTICATION_OK_BTN).click()
                if timestamp == "":
                    self.poll_name = poll_name
                    self.email_should_be_sent
                logger.info(f'''Feedback request for the poll {poll_name} was sent now.
                            Check your email!''')
        except AssertionError as error:
            logger.info(error)
            raise AssertionError('Add an email address!')

    @keyword
    def email_should_be_sent(self):
        """Verifies _Last sent_ field in poll listing is active and has current date in it."""
        timestamp = f"""(//div[@class='row projectRow']//*[text()='{self.poll_name}']
                    /../../following-sibling::div)[2]"""
        today = datetime.today()
        try:
            expect(self.page.locator(timestamp)).to_contain_text(f'{today.strftime("%b %#d. %Y")}')
            logger.info(f"Poll '{self.poll_name}' is sent to email")
        except AssertionError as err:
            logger.info(err)
            raise AssertionError('Email is not sent')

    @keyword
    def schedule_sending_email(self):
        """Schedules sending the poll vie email daily at 12PM."""
        if self.page.locator(variables.CREATE_POLL).is_visible():
            self.go_to_poll_settings()
        self.page.click(variables.ADD_EMAIL)
        self.page.fill(variables.EMAIL_FIELD, variables.EMAIL)
        self.page.click(variables.ADD_RECIPIENT)
        logger.info("Email is added")
        self.page.locator('#projectEmailInterval').select_option(label='daily')
        logger.info("Daily is added")
        expect(self.page.locator('#projectEmailIntervalDayOffset')).to_be_visible()
        self.page.locator('#projectEmailIntervalDayOffset').select_option(label='12AM / 12')
        logger.info("Time is added")
        try:
            expect(self.page.locator(variables.SAVE_BTN)).to_be_visible(timeout=30000)
            logger.info("Searching for the save button")
            self.page.locator(variables.SAVE_BTN).click(timeout=30000)
            time.sleep(5)
            logger.info(f"Poll '{self.poll_name}' is scheduled to be sent")
        except AssertionError as err:
            logger.info(err)
            raise AssertionError('Save button is not working')

    @keyword
    def email_should_be_scheduled(self):
        """Verifies _Next mailing_ field in poll listing is active and has next day date in it."""
        timestamp = f"""(//div[@class='row projectRow']//*[text()='{self.poll_name}']
                    /../../following-sibling::div)[3]"""
        tmw = (datetime.today() + timedelta(days=1))
        try:
            expect(self.page.locator(timestamp)).to_contain_text(f'{tmw.strftime("%b %#d. %Y")}')
            logger.info(f"'{self.poll_name}' is scheduled to be sent")
        except AssertionError as err:
            logger.info(err)
            raise AssertionError('Email is not scheduled')

    @keyword
    def view_results_or_send_reminder(self, poll_name: str = ""):
        """Checks whether the _View results_ button in poll listing is active, if not, tries
        to send a request to answer immediately. If there is no email added to the poll,
        raises an error with the message "Add an email address!".
        """
        if poll_name == "":
            poll_name = self.poll_name
            logger.info('There was no name defined for the poll.')
        logger.info(f"Checking if results were received for the poll {poll_name}")
        view_results_btn = f"""(//div[@class='row projectRow']//*[text()='{poll_name}']
                           /../../following-sibling::div)[4]//a[2]"""
        try:
            expect(self.page.locator(view_results_btn)).to_have_class("btn action")
            logger.info('Clicking VIEW RESULTS button.')
            self.page.locator(view_results_btn).click()
            expect(self.page.locator(variables.QWL_ANALYSIS)).to_be_visible()
            logger.info(f'Checking the results of the poll {poll_name}')
        except AssertionError as error:
            logger.info(error)
            logger.info(f"""The results for the poll {poll_name} were not found.
                        Will try to send a request for feedback""")
            self.send_feedback_request_now(poll_name)

    @keyword
    def make_streamlined(self):
        """Changes poll settings to streamlined, which uses scale 1-5 in feedback form
        in stead of quality/quantity-dual-axix scale.
        """
        self.go_to_poll_settings()
        self.page.locator(variables.QWL_TYPE).select_option('streamlined')
        expect(self.page.locator(variables.SAVE_CONT)).to_be_enabled()
        self.page.click(variables.SAVE_CONT)
        logger.info("Poll settings: Streamlined")

    @keyword
    def translate_to_finnish(self):
        """Translates the feedback form from English(default) to Finnish."""
        if self.page.locator(variables.CREATE_POLL).is_visible():
            self.go_to_poll_settings()
        self.page.click(variables.BASIC_SETTINGS)
        logger.info("Basic settings clicked")
        self.page.locator(variables.TRANSLATE).select_option('5: Object')
        logger.info("Option selected")
        expect(self.page.get_by_text("Finnish (suomi)")).to_be_visible()
        logger.info("Language is visible")
        try:
            expect(self.page.locator(variables.SAVE_BTN)).to_be_enabled(timeout=30000)
            self.page(variables.SAVE_BTN).click()
            logger.info("Changes saved")
        except AssertionError as err:
            logger.info(err)
            logger.info('Save button does not work')


    @keyword
    def change_name(self):
        """Changes the name of the existing poll.
        New poll is named "Poll_x" with _x_ being random number between 0 and 9999.
        """
        self.go_to_poll_settings()
        self.poll_name = f'Poll_{_random.randint(0, 10000)}'
        self.page.locator(variables.SHOW_ALL_QST_BTN).click()
        self.page.locator(variables.BASIC_SETTINGS).click()
        self.page.locator(variables.NAME_FIELD).fill(self.poll_name)
        self.page.locator(variables.SAVE_BTN).click()
        logger.info(f'Poll name is now {self.poll_name}')

    @keyword
    def mark_as_a_template(self):
        """Changes poll settings, so it can be later used as a template for other polls."""
        if self.page.locator(variables.CREATE_POLL).is_visible():
            self.go_to_poll_settings()
        self.page.click(variables.BASIC_SETTINGS)
        logger.info("Basic settings clicked")
        self.page.click(variables.TEMPLATE)
        logger.info("Poll settings: Template")
        self.page.click(variables.SAVE_BTN)
        time.sleep(15)
        logger.info("Changes saved")

    @keyword
    def poll_should_be_template(self):
        """Verifies poll type is _QWL template_ in the poll listing view."""
        poll_type = f"""(//div[@class='row projectRow']//*[text()='{self.poll_name}']
                        /following-sibling::span[@class='projectTypeLabel'])[1]"""
        self.go_to_home_page()
        try:
            expect(self.page.locator(poll_type)).to_be_visible()
            expect(self.page.locator(poll_type)).to_contain_text('QWL template')
            logger.info(f'{self.poll_name} is now a template')
        except AssertionError as err:
            logger.info(err)
            raise AssertionError("Changing poll settings to template was unsuccesful")

    @keyword
    def add_new_question(self):
        """Adds a new feedback question to custom poll."""
        if self.page.locator(variables.CREATE_POLL).is_visible():
            self.go_to_poll_settings()
        time.sleep(5)
        self.page.click(variables.ADD_Q)
        logger.info('Starting to add new question to Custom poll')
        try:
            self.page.fill(variables.NEW_Q, f'New question {_random.randint(0, 10000)}')
            logger.info('Writing new question')
            self.page.click(variables.ADD_NEW_Q)
            logger.info('New question added')
        except TypeError as err:
            logger.info(err)
            raise TypeError('Question field did not appear')
        expect(self.page.locator(variables.Q_ROW)).to_contain_text('New question')

    @keyword
    def choose_from_help_options(self, option: str):
        """Opens help options window and chooses given ``option``."""
        self.page.click(variables.HELP_BTN)
        if option == variables.FAQ:
            self.page.click(option)
        else:
            with self.page.expect_popup() as self.popup_info:
                self.page.click(option)

    @keyword
    def faq_page_should_be_open(self):
        """Verifies FAQ page has opened in the current page."""
        try:
            expect(self.page.locator(variables.FAQ_TITLE)).to_be_visible()
        except AssertionError as err:
            logger.info(err)
            raise AssertionError("Failed to open FAQ page.")

    @keyword
    def poll_tutorial_should_be_open(self):
        """Verifies Poll Tutorial Video has been opened in YouTube in new tab."""
        self.newpage = self.popup_info.value
        try:
            expect(self.newpage).to_have_title("VibeCatch Pulse Poll Tutorial - YouTube")
        except AssertionError as err:
            logger.info(err)
            raise AssertionError("Failed to open tutorial video on YouTube.")

    @keyword
    def qwl_playground_should_be_open(self):
        """Verifies QWL Playground page has been opened in new tab."""
        self.newpage = self.popup_info.value
        try:
            expect(self.newpage.locator(variables.QWL_OVERVIEW)).to_be_visible()
        except AssertionError as err:
            logger.info(err)
            raise AssertionError("Failed to open QWL Playground.")

    @keyword
    def choose_pdf_document(self, name: str):
        """Chooses PDF document with given ``name`` from help window
        options. Clicks the link to initialize downloading of PDF document.
        """
        if self.page.locator(variables.HELP_WIN).is_visible() is False:
            self.page.click(variables.HELP_BTN)
        # poista seuraavat demon jälkeen:
        with self.page.expect_popup() as self.popup_info:
            self.page.click(f"//a[normalize-space()='{name}']")
            self.newpage = self.popup_info.value
        # poista tähän asti demon jälkeen
        with self.page.expect_download() as self.pdf_download:
            self.page.click(f"//a[normalize-space()='{name}']", modifiers=["Alt",])

    @keyword
    def download_and_check_pdf(self, text: str, num: int):
        """Downloads and saves PDF document to _pdf_ directory. Checks that content
        of first page and number of pages match to data in datafile.
        """
        download = self.pdf_download.value
        new_path = os.getcwd()
        self.full_filename = f'{new_path}/{download.suggested_filename}'
        download.save_as(self.full_filename)
        reader = PyPDF2.PdfReader(self.full_filename)
        first_page = reader.pages[0]
        content = (first_page.extract_text())
        joint_content = "".join(content.split())
        joint_text = "".join(text.split())
        if len(reader.pages) != num:
            logger.info("Number of pages was different than expected.")
            raise AssertionError
        if joint_text not in joint_content:
            logger.info("Content of first page was different than expected.")
            raise AssertionError

    @keyword
    def remove_pdf(self):
        """Removes downloaded PDF file."""
        os.remove(self.full_filename)

    @keyword
    def adjust_number_of_questions(self, number: int):
        """Adjusts the number of questions in poll to ``number`` given as argument."""
        num_btn = f"//button[normalize-space()='{number}']"
        self.page.click(num_btn)
        try:
            expect(self.page.locator(variables.SAVE_CONT)).to_be_visible()
        except AssertionError as err:
            logger.info(err)
            raise AssertionError("Can't locate _save & continue_ button on the page.")
        self.page.click(variables.SAVE_CONT)
        time.sleep(5)

    @keyword
    def check_poll_form(self, number: int):
        """Opens poll form to a new tab and checks poll form has correct number
        of questions, then closes the tab.
        """
        with self.page.expect_popup() as self.popup_info:
            self.page.click(variables.POLL_FORM_BTN)
            newpage = self.popup_info.value
            newpage.click(variables.MOVE_FORWARD)
            try:
                expect(newpage.locator(variables.QUESTIONS)).to_contain_text(f"1 / {number}")
            except AssertionError as err:
                logger.info(err)
                raise AssertionError("""There's different number of
                                     questions on the poll form than expected.""")
            newpage.close()

    @keyword
    def delete_poll(self, poll_name: str = ""):
        """Deletes the poll used in a test case. This method is used at the end of a
        test case, where new poll is created and not needed in future test cases.
        """
        if poll_name == "":
            poll_name = self.poll_name
        if self.page.locator(variables.CREATE_POLL).is_visible():
            self.go_to_poll_settings(poll_name)
        try:
            expect(self.page.locator(variables.DELETE1)).to_be_enabled()
        except AssertionError as err:
            logger.info(err)
            raise AssertionError("Can't delete poll because browser is on a wrong page.")
        self.page.click(variables.DELETE1)
        self.page.click(variables.DELETE2)
        expect(self.page.locator(variables.DELETE3)).to_be_enabled()
        self.page.click(variables.DELETE3)
        expect(self.page.locator(variables.DELETE3)).not_to_be_visible()

    @keyword
    def close_browser(self):
        """Closes browser and all open pages."""
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.playwright:
            self.playwright.stop()
            self.playwright = None

    @keyword
    def delete_all(self):
        """Clean up method to be used after test has failed and unwanted polls
        are left in the page. This will delete every poll except for the one named "test1",
        which is used again in another test case.
        """
        time.sleep(6)
        project_row = "//div[@class='row projectRow'][1][1]"
        if self.page.locator("//a[@class='sortItem selected']").is_visible():
            expect(self.page.locator(project_row)).not_to_contain_text('test1')
            self.page.click(variables.SET_BTN)
            expect(self.page.locator(variables.DEL_BUT1)).to_be_visible()
            self.page.click(variables.DEL_BUT1)
            self.page.click(variables.DEL_BUT2)
            self.page.click(variables.DEL_BUT3)
        self.delete_all()
