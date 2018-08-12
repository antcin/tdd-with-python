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

        # Cleopatra wonders whether the site will remember her list. Then she sees that the site has generated a unique URL
        # for her -- there is some explanatory text to that effect.
        self.fail('Finish the test!')

        # She visits taht URL -- her to-do list is still there.

        # Satisfied, she goes back to sleep.

