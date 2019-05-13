import unittest
from selenium import webdriver
import time
from unittest.mock import Mock


class TestMyFront(unittest.TestCase):

    def get_admin_creds(self):
        mock = Mock()
        mock.login = "admin@mail.ru"
        mock.password = "admin01"
        return mock

    def test(self):

        mess = self.get_admin_creds()
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
        driver.get("http://localhost:3000/login")
        login_input_el = driver.find_element_by_xpath('//form/div[1]/input')
        login_input_el.send_keys(mess.login)
        password_input_el = driver.find_element_by_xpath('//form/div[2]/input')
        password_input_el.send_keys(mess.password)
        button = driver.find_element_by_xpath('//form/button[1]')
        button.click()
        time.sleep(3)
        third_link = driver.find_element_by_xpath('//ul/a[3]')
        # print(type(third_link), third_link)
        self.assertIsNotNone(third_link)

        driver.close()

if __name__ == "__main__":
    unittest.main()