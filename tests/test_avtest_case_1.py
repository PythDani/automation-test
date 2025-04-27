"""
  Test case number 
  Caso automatizado 1: Realizar booking / reserva One-way (Solo ida).

  @Author: Rafael Daniel Farfán
"""
import allure
from pages.home_page import HomePage

@allure.title("Caso automatizado 1: One way booking")
@allure.severity(allure.severity_level.NORMAL)
def test_avtest_case_1(browser):
    """
    Tests that we do when we have one way booking scenario
    """
    page = HomePage(browser)
    page.load()
    page.select_one_way_flight()
    with allure.step("Validar selección de idiomas"):
        # Get language
        language = browser.execute_script("return navigator.language || navigator.userLanguage;")
        print(f"Idioma detectado: {language}")
    
