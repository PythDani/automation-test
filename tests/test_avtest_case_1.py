"""
  Test case number 
  Caso automatizado 1: Realizar booking / reserva One-way (Solo ida).

  @Author: Rafael Daniel Farfán
"""
import allure
from pages.form_passengers_page import FormPassengersPage
from pages.home_page import HomePage


@allure.title("Caso automatizado 1: One way booking")
@allure.severity(allure.severity_level.NORMAL)
def test_avtest_case_1(browser):
    """
    Tests that we do when we have one way booking scenario
    """
    page = HomePage(browser)
    form = FormPassengersPage(browser)

    # Load page
    with allure.step("Cargar página"):
      page.load()

    # Validate that the page has loaded correctly
    with allure.step("Validar que la página haya cargado correctamente"):
        assert "avianca - encuentra tiquetes y vuelos baratos | Web oficial" in browser.title, f"La página no cargó correctamente. Título encontrado: {browser.title}"
    
    # Select one way Flight
    with allure.step("Seleccionar vuelo de solo ida"):        
        page.select_one_way_radio_button()

    # Validar que el radio button de ida haya sido seleccionado
    with allure.step("Validar selección de vuelo de solo ida"):
        assert page.is_one_way_selected(), "No se ha seleccionado el radio button de ida"

    # Select language
    with allure.step("Validar selección de idiomas"):
        # Get language
        language = browser.execute_script("return navigator.language || navigator.userLanguage;")
        print(f"Idioma detectado: {language}")
    
    # Select Origin city
    with allure.step("Seleccionar ciudad de origen"):
      page.select_origin()

    # Select destination city
    with allure.step("Seleccionar ciudad de destino"): 
      page.select_destination()

    # Select a month randomly
    with allure.step("Seleccionar un mes"):
      page.select_random_month(times = 3)    

    # Click on the datepicker button.
    with allure.step("Seleccionar fecha de salida"):
      page.select_date_departure()        

    # Select plus adults button
    with allure.step("Seleccionar dos pasajeros"):
      page.click_plus_adult(times =1)

    # Confirm button number passengers and click
    with allure.step("Pulsar en botón de confirmar cantidad de pasajeros"):
      page.confirm_button_passengers_quantity()        

    # Click on search button
    with allure.step("Pulsar en botón de buscar vuelo"):
      page.click_search_flight_button()

    # We wait unitll the page loader disapear.
    page.loader_a()         

    # Click on flight selected button
    with allure.step("Click en un vuelo y desplegar tarifas"):
      page.click_drop_down_flight()

    # Click on basic fare button
    with allure.step("Click en tarifa básica"):
      page.click_on_fare_flight()

    # We wait unitll the page loader disapear.
    page.loader_b() 

    # Click on continue button TO MOVE TO PASSENGER FORM
    with allure.step("Click en botón de continuar al formulario de pasajeros"):
      page.button_continue_to_move_to_passenger_form()

    # We wait unitll the page loader disapear.
    page.loader_b()

    # Click on submit button
    with allure.step("Click en botón de submit información de pasajeros"):
      form.fill_passenger_form_method() 



    
