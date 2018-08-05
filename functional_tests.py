from selenium import webdriver
import unittest

class NewVisitorTEst(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Cleopatra has heard that there is a cool new to-do app in town. She goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices that the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # She is invited to enter a to-do item straight away


        # She types "Buy birthday present for Marc Anthony" into a text box ("Cleopatra is currently dating this guy from Rome")

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy birthday present" as an item in a to-do list

        # There is still a text-box inviting her to add another item. She enters
        # "Go to that nice perfume shop, he needs new cologne" (Marc Anthony does not have the best smell)

        # The page updates again, and now shows both items on her list

        # Cleopatra wonders whether the site will remember her list. Then she sees that the site has generated a unique URL
        # for her -- there is some explanatory text to that effect.

        # She visits taht URL -- her to-do list is still there.

        # Satisfied, she goes back to sleep.

if __name__ == '__main__':
    unittest.main(warnings='ignore')



