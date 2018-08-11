from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTEst(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Cleopatra has heard that there is a cool new to-do app in town. She goes to check out its homepage
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy birthday present for Marc Anthony')

        # There is still a text-box inviting her to add another item. She enters
        # "Go to that nice perfume shop, he needs new cologne" (Marc Anthony does not have the best smell)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Go to that nice perfume shop, he needs new cologne')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy birthday present for Marc Anthony')
        self.check_for_row_in_list_table('2: Go to that nice perfume shop, he needs new cologne')

        # Cleopatra wonders whether the site will remember her list. Then she sees that the site has generated a unique URL
        # for her -- there is some explanatory text to that effect.
        self.fail('Finish the test!')

        # She visits taht URL -- her to-do list is still there.

        # Satisfied, she goes back to sleep.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
