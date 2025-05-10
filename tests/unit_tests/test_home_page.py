import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.pages_case_1.home_page import HomePage

class TestHomePage(unittest.TestCase):

    def setUp(self):
        self.driver = MagicMock()
        self.home_page = HomePage(self.driver)

    @patch('pages.pages_case_1.home_page.get_logger')
    def test_load(self, mock_logger):
        self.home_page.URL = "http://example.com"
        self.home_page.wait_for_invisibility = MagicMock()
        self.driver.get = MagicMock()

        self.home_page.load()

        self.driver.get.assert_called_once_with("http://example.com")
        self.home_page.wait_for_invisibility.assert_called_once_with(self.home_page.LOADER)

    def test_login(self):
        self.home_page.wait_for_visibility_of_element_located = MagicMock(return_value=MagicMock())
        self.home_page.wait_for_new_window = MagicMock()
        self.home_page.wait_until_focus_be_usable = MagicMock()
        self.home_page.wait_for = MagicMock()
        self.home_page.find = MagicMock()
        self.home_page.wait_for_window_close = MagicMock()
        self.driver.window_handles = ["main", "new"]

        self.home_page.login("test_user", "test_password")

        self.home_page.wait_for_visibility_of_element_located.assert_called_once_with(self.home_page.BUTTON_LOGIN)
        self.home_page.wait_for_new_window.assert_called_once()
        self.home_page.wait_until_focus_be_usable.assert_called_once_with("new")
        self.home_page.find.assert_any_call(self.home_page.USER_FIELD)
        self.home_page.find.assert_any_call(self.home_page.PASSWORD_FIELD)
        self.home_page.find.assert_any_call(self.home_page.LOGIN_CONFIRM)

    def test_select_language(self):
        self.home_page.wait_for_loader_to_disappear = MagicMock()
        self.home_page.wait_for_invisibility = MagicMock()
        self.home_page.wait_to_be_clickable = MagicMock(return_value=MagicMock())

        self.home_page.select_language("English")

        self.home_page.wait_for_loader_to_disappear.assert_called_once_with(self.home_page.LOADER)
        self.home_page.wait_for_invisibility.assert_called_once_with(self.home_page.LOADER_B)
        self.home_page.wait_to_be_clickable.assert_called()

    def test_select_currency(self):
        self.home_page.wait_for_loader_to_disappear = MagicMock()
        self.home_page.wait_to_be_clickable = MagicMock(return_value=MagicMock())

        self.home_page.select_currency("España")

        self.home_page.wait_for_loader_to_disappear.assert_called_once_with(self.home_page.LOADER)
        self.home_page.wait_to_be_clickable.assert_called()

    def test_select_one_way_radio_button(self):
        self.home_page.wait_for = MagicMock(return_value=MagicMock())

        self.home_page.select_one_way_radio_button()

        self.home_page.wait_for.assert_called_with(self.home_page.RADIO_ONE_WAY)

    
    def test_is_logged_in(self):
        self.home_page.find = MagicMock()

        result = self.home_page.is_logged_in()

        self.assertTrue(result)
        self.home_page.find.assert_called_once_with(self.home_page.LOGGED)

if __name__ == "__main__":
    unittest.main()