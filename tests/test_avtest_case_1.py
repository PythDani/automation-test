"""
  Test case number 
  Caso automatizado 1: Realizar booking / reserva One-way (Solo ida).

  @Author: Rafael Daniel Farfán
"""
import allure
from pages.avtest_page_case_1 import AvtestPage

@allure.title("Caso automatizado 1: One way booking")
@allure.severity(allure.severity_level.NORMAL)
def test_avtest_case_1(browser):
    """
    Tests that we do when we have one way booking scenario
    """
    page = AvtestPage(browser)
    page.load()
    page.select_one_way_flight()
    
