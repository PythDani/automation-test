"""
  Test case number 
  Caso automatizado 1: Realizar booking / reserva One-way (Solo ida).

  @Author: Rafael Daniel Farfán
"""
import allure
from pages.booking_select_page import BookingSelectPage
from pages.form_passengers_page import FormPassengersPage
from pages.home_page import HomePage
from pages.itinerary_page import ItineraryPage
from pages.payment_page import PaymentPage
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
    payment_page = PaymentPage(browser)
    bokking_select_page = BookingSelectPage(browser) 
    itinerary_page = ItineraryPage(browser)

    # Load page
    with allure.step("Test Home page"):
      page.load()
      #Select language
      page.select_language(language="Español")
      #Select currency
      page.select_currency(currency="Colombia")
      # Select one way Flight
      page.select_one_way_radio_button()
      #Select Origin city
      page.select_origin(city_origin="Medellín")
      #Select destination city
      page.select_destination(city_destination="Bogotá")
      #Select a month randomly
      page.select_random_month(times = 3)
      # Click on the datepicker button to select date    
      page.select_date_departure()
      # Select plus adults button        
      page.click_plus_adult(times = 1)
      # Confirm button number passengers
      page.confirm_button_passengers_quantity() 
      # Click on search button       
      page.click_search_flight_button()
   
    # We wait unitll the page loader disapear.
    page.loader_a()         

    # Click on flight selected button
    with allure.step("Test Booking Select Page"):
      # Click on basic fare button
      bokking_select_page.click_drop_down_flight()
      # We wait unitll the page loader disapear.
      bokking_select_page.click_on_fare_flight()
      # We wait unitll the page loader disapear.
      bokking_select_page.loader_b() 
      # Click on continue button TO MOVE TO PASSENGER FORM
      bokking_select_page.button_continue_to_move_to_passenger_form()

    bokking_select_page.loader_b()   

    # Click on submit button
    with allure.step("Form passengers page"):
      form.fill_passenger_form_method()   

    # Open services page
    with allure.step("Go to services page"):
      services.load()
      services.add_carry_on_and_checked_baggage()
      services.click_on_bagage_plus_button()
      services.confirm_carry_on_modal_and_checked_baggage_modal()
      services.wait_for_loader_to_disappear()
      services.add_sport_baggage()
      services.click_on_sport_bagage_plus_button()
      services.confirm_sport_baggage_modal()
      services.wait_for_loader_to_disappear()
      services.add_bussines_lounge()
      services.click_on_some_lounge_plus_button()
      services.confirm_lounge_bussiness_modal()
      services.wait_for_loader_to_disappear()
      services.continue_to_the_next_step()  

    # Select seats
    with allure.step("Select seats"):
      seat_map.load()
      seat_map.select_seats_based_on_quantity_of_passengers()
      seat_map.continue_to_the_next_step()    
      
    # Fill payment form
    with allure.step("Fill payment form"):         
      payment_page.load()
      payment_page.scroll_to_element(200)
      payment_page.fill_cardholder_name("Lola Perez")     
      payment_page.fill_card_number("4111111111111111")
      payment_page.select_expiration_month("12")
      payment_page.select_expiration_year("25")
      payment_page.fill_cvv("123")
      payment_page.fill_email("test@test.com")
      payment_page.fill_address("calle #13")
      payment_page.fill_city("Medellin")
      payment_page.select_country("Colombia")
      payment_page.accept_terms_and_conditions()
      payment_page.click_continue()
      payment_page.loader()
      payment_page.loader()
     
    # Itinerary
    with allure.step("Iitinerary test validation"):
      itinerary_page.get_reservation_code()
      itinerary_page.validate_departure_city('Medellín')
      itinerary_page.validate_arrival_city('Bogotá')
      itinerary_page.validate_reserve_holder('Andres Perez')
      itinerary_page.validate_passenger_adult_number('1')






    
