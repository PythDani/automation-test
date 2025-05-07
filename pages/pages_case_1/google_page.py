# """
#   example-page-class to testing the right operation of
#   selenium and libraries used in the project.

#   @Author: Rafael Daniel Farfán
# """
# from selenium.webdriver.common.by import By
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# class GooglePage:
#     URL = "https://www.google.com"
#     SEARCH_BOX = (By.NAME, "q")
#     RESULT_STATS = (By.ID, "result-stats")

#     def __init__(self, driver):        
#         """
#         Initialize a GooglePage instance.

#         Args:
#             driver (selenium.webdriver): A selenium webdriver instance.
#         """
#         self.driver = driver

#     def load(self):
#         """
#         Navigate to the Google home page.

#         """
#         self.driver.get(self.URL)

#     def search(self, query):
#         """
#         Perform a search on the Google home page.

#         Args:
#             query (str): The text to search for.

#         """
#         search_box = self.driver.find_element(*self.SEARCH_BOX)
#         search_box.send_keys(query)
#         search_box.submit()
#         time.sleep(5)
#         # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(GooglePage.RESULT_STATS))
