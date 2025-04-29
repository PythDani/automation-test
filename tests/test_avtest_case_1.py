"""
  Test case number 
  Caso automatizado 1: Realizar booking / reserva One-way (Solo ida).

  @Author: Rafael Daniel Farfán
"""
import allure
from pages.form_passengers_page import FormPassengersPage
from pages.home_page import HomePage
from pages.seat_map_page import SeatMapPage
from pages.services_page import ServicesPage


@allure.title("Caso automatizado 1: One way booking")
@allure.severity(allure.severity_level.NORMAL)
def test_avtest_case_1(browser):
    """
    Tests that we do when we have one way booking scenario
    """
    page = HomePage(browser)
    form = FormPassengersPage(browser)
    services = ServicesPage(browser)
    seat_map = SeatMapPage(browser) 

    # Load page
    with allure.step("Load home page"):
      page.load()

    # Validate that the page has loaded correctly
    with allure.step("Validate page title"):
        assert "avianca - encuentra tiquetes y vuelos baratos | Web oficial" in browser.title, f"The page does not load correctly: {browser.title}"
    
    # Select one way Flight
    with allure.step("Select one way flight"):        
        page.select_one_way_radio_button()

    # Validar que el radio button de ida haya sido seleccionado
    with allure.step("Validate one way radio button"):
        assert page.is_one_way_selected(), "No se ha seleccionado el radio button de ida"

    # Select language
    with allure.step("Validate language"):
        # Get language
        language = browser.execute_script("return navigator.language || navigator.userLanguage;")
        print(f"Language: {language}")
    
    # Select Origin city
    with allure.step("Select origin city"):
      page.select_origin()

    # Select destination city
    with allure.step("Select destination city"): 
      page.select_destination()

    # Select a month randomly
    with allure.step("Select a month randomly"):
      page.select_random_month(times = 3)    

    # Click on the datepicker button.
    with allure.step("Select date departure"):
      page.select_date_departure()        

    # Select plus adults button
    with allure.step("Add passengers"):
      page.click_plus_adult(times = 1)

    # Confirm button number passengers and click
    with allure.step("Confirm passengers quantity"):
      page.confirm_button_passengers_quantity()        

    # Click on search button
    with allure.step("Search flights button"):
      page.click_search_flight_button()

    # We wait unitll the page loader disapear.
    page.loader_a()         

    # Click on flight selected button
    with allure.step("Click on flight selected"):
      page.click_drop_down_flight()

    # Click on basic fare button
    with allure.step("Click on basic fare"):
      page.click_on_fare_flight()

    # We wait unitll the page loader disapear.
    page.loader_b() 

    # Click on continue button TO MOVE TO PASSENGER FORM
    with allure.step("Click continue to passenger form"):
      page.button_continue_to_move_to_passenger_form()

    # We wait unitll the page loader disapear.
    page.loader_b()

    # Click on submit button
    with allure.step("Click on submit button"):
      form.fill_passenger_form_method()
   

    # Open services page
    with allure.step("Go to services page"):
      services.load()

    # Add carry on and checked baggage
    with allure.step("Gor to carry on baggage service"):
      services.add_carry_on_and_checked_baggage()
    
    # Click on add plus button to add baggage
    with allure.step("Add carry on and checked baggage"):
       services.click_on_bagage_plus_button()
    
    # Confirm baggage selection
    with allure.step("Click on confirm carry on and checked baggage"):
       services.confirm_carry_on_modal_and_checked_baggage_modal()
    
    services.wait_for_loader_to_disappear()
    
    # # Add sport baggage
    with allure.step("Click to show sport baggage"):    
      services.add_sport_baggage()
    
    
    # # Click on add plus button to add bagolf baggage
    with allure.step("Click to add sport baggage"):
      services.click_on_sport_bagage_plus_button()

    # # Confirm sport baggage selection
    with allure.step("Click to confirm sport baggage"):
      services.confirm_sport_baggage_modal()
    
    services.wait_for_loader_to_disappear()

    # Click on add plus button to add lounge
    with allure.step("Click to add lounge"):
      services.add_bussines_lounge()

    # Click on add plus button to add lounge
    with allure.step("Add lounge"):
      services.click_on_some_lounge_plus_button()
    
    # Confirm lounge selection
    with allure.step("Confirmar lounge"):
      services.confirm_lounge_bussiness_modal()
    
    services.wait_for_loader_to_disappear()

    # Click on continue button to move to the next step "SeatMap"
    with allure.step("Click contiue to SeatMap"):
      services.continue_to_the_next_step()

    seat_map.load()

    # Select seats
    with allure.step("Select seats"):
      seat_map.select_seats_based_on_passengers()   


    # Click on continue button to move to the next step "Paynemt page"
    with allure.step("Click contiue to Paynemt page"):
      seat_map.continue_to_the_next_step()



    
