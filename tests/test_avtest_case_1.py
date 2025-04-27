"""
  Test case number 
  Caso automatizado 1: Realizar booking / reserva One-way (Solo ida).

  @Author: Rafael Daniel Farfán
"""
import allure
from pages.form_passengers import FormPassengers
from pages.home_page import HomePage

@allure.title("Caso automatizado 1: One way booking")
@allure.severity(allure.severity_level.NORMAL)
def test_avtest_case_1(browser):
    """
    Tests that we do when we have one way booking scenario
    """
    page = HomePage(browser)
    form = FormPassengers(browser)
    page.load()
    with allure.step("Seleccionar vuelo de solo ida"):
        # page.select_one_way_flight()
        page.select_one_way_radio_button()
    with allure.step("Seleccionar ciudad de origen"):
        assert page.is_one_way_selected(), "No se ha seleccionado el radio button de ida"
    with allure.step("Validar selección de idiomas"):
        # Get language
        language = browser.execute_script("return navigator.language || navigator.userLanguage;")
        print(f"Idioma detectado: {language}")
    
    # Select Origin city
    page.select_origin()

    # Select destination city 
    page.select_destination()

    # Select a month randomly
    page.select_random_month(times = 3)    

    # Click on the datepicker button.
    page.select_date_departure()        

    # Select plus adults button
    page.click_plus_adult(times =1)

    # Confirm button number passengers and click
    page.confirm_button_passengers_quantity()        

    # Click on search button
    page.click_search_flight_button()

    # We wait unitll the page loader disapear.
    page.loader_a()         

    # Click on flight selected button
    page.click_drop_down_flight()

    # Click on basic fare button
    page.click_on_fare_flight()

    # We wait unitll the page loader disapear.
    page.loader_b() 

    # Click on continue button TO MOVE TO PASSENGER FORM
    page.button_continue_to_move_to_passenger_form()

    # We wait unitll the page loader disapear.
    page.loader_b()

    form.fill_passenger_form_method() 



    
