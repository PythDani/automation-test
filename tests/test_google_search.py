# """
#   example-class to testing the right operation of
#   selenium and libraries used in the project.

#   @Author: Rafael Daniel Farfán
# """
# import allure
# from pages.google_page import GooglePage

# @allure.title("Search on Google")
# @allure.severity(allure.severity_level.CRITICAL)
# def test_google_search(browser):
#     """
#     Tests that the Google search page loads successfully and
#     that searching for "Selenium WebDriver" yields a page that
#     contains the string "Selenium" (case-insensitive).
#     """
#     page = GooglePage(browser)
#     page.load()
#     # page.search("Selenium WebDriver")
#     # assert "Seleniumr" in browser.title or "selenium webDriver" in browser.page_source.lower()
