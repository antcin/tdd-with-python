from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Cleopatra has heard that there is a cool new to-do app in town. She goes to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices that the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # She types "Buy birthday present for Marc Anthony" into a text box ("Cleopatra is currently dating this guy from Rome")
        inputbox.send_keys('Buy birthday present for Marc Anthony')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy birthday present" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy birthday present for Marc Anthony')

        # There is still a text-box inviting her to add another item. She enters
        # "Go to that nice perfume shop, he needs new cologne" (Marc Anthony does not have the best smell)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Go to that nice perfume shop, he needs new cologne')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('1: Buy birthday present for Marc Anthony')
        self.wait_for_row_in_list_table('2: Go to that nice perfume shop, he needs new cologne')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Cleopatra starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy birthday present for Marc Anthony')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy birthday present for Marc Anthony')

        # She notices that her list has a unique URL
        cleopatra_list_url = self.browser.current_url
        self.assertRegex(cleopatra_list_url, '/lists/.+')

        # Now a new user, Nefertiti, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Cleopatra is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Nefertiti visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy birthday present for Marc Anthony', page_text)
        self.assertNotIn('bake a cake', page_text)

        # Nefertiti starts a new list by entering a new item. She does not have a boyfriend, yet and she loves baking
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy flour')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flour')

        # Nefertiti gets her own unique URL
        nefertiti_list_url = self.browser.current_url
        self.assertRegex(nefertiti_list_url, '/lists/.+')
        self.assertNotEqual(nefertiti_list_url, cleopatra_list_url)

        # Again, there is no trace of Cleopatra's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy birthday present for Marc Anthony', page_text)
        self.assertIn('Buy flour', page_text)

        # Satisfied, they both go back to sleep

