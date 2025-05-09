"""
  Test case number 3 
  Caso automatizado 3: Realizar Login en UAT1..

  @Author: Rafael Daniel Farfán
"""
import allure


@allure.title("Automated case 3: Login UAT1")
@allure.severity(allure.severity_level.NORMAL)
def test_avtest_case_1(booking_context_case_3):   

    """
    Test case for logging in and booking a round trip flight in UAT1.

    This test automates the process of logging in and booking a round trip flight,
    including selecting the origin and destination cities, departure and arrival 
    dates, passenger details, and various services. It navigates through multiple
    pages such as Home, Booking Select, Form, Services, Seats, Payment, and Itinerary, 
    verifying each step with Allure steps for better reporting.

    Args:
        booking_context_case_3 (dict): A dictionary containing initialized page 
        objects and booking parameters for the test.
    """
    page = booking_context_case_3["page"]
    form = booking_context_case_3["form"]
    services = booking_context_case_3["services"]
    seat_map = booking_context_case_3["seat_map"]
    payment_page = booking_context_case_3["payment_page"]
    booking_select_page = booking_context_case_3["booking_select_page"]
    itinerary_page = booking_context_case_3["itinerary_page"]
    params = booking_context_case_3["params"]

    # --- Home Page ---
    with allure.step("Test Home page"):
        page.load()
        page.login(username=params["user_name"], password=params["user_password"])
        page.select_language(params["language"])
        page.select_currency(params["currency"])
        page.select_origin(params["city_origin"])
        page.select_destination(params["city_destination"])
        page.select_deaperture_date(**params["departure_date"])
        page.select_arrival_date(**params["arrival_date"])
        page.click_plus_adult(times=params["passenger_count"])
        page.click_plus_young(times=params["young_count"])
        page.click_plus_child(times=params["child_count"])
        page.click_plus_infant(times=params["baby_count"])
        page.confirm_button_passengers_quantity()
        page.click_search_flight_button()

    page.loader_a()

    # --- Booking Select ---
    with allure.step("Test Booking Select page"):
        booking_select_page.loader_b()
        booking_select_page.click_relative_date(label= params["relative_day"])
        booking_select_page.loader_b()
        booking_select_page.click_drop_down_flight()
        booking_select_page.click_on_fare_flight()
        booking_select_page.loader_b()
        booking_select_page.click_relative_date(label= params["relative_day"])
        booking_select_page.loader_b()
        booking_select_page.click_drop_down_return_flight()
        booking_select_page.click_on_fare_flight()
        booking_select_page.loader_b()
        booking_select_page.get_sesion_params()
        booking_select_page.button_continue_to_move_to_passenger_form()

    booking_select_page.loader_b()

    # --- Form ---
    with allure.step("Test Form passengers page"):
        form.fill_passenger_form_method()        
        

    # --- Services ---
    with allure.step("Test services page"):
        services.load()
        services.add_carry_on_and_checked_baggage()
        services.click_on_bagage_plus_button()
        services.confirm_carry_on_modal_and_checked_baggage_modal()
        
        services.add_sport_baggage()
        services.click_on_sport_bagage_plus_button()
        services.confirm_sport_baggage_modal()
        
        services.add_bussines_lounge()
        services.click_on_some_lounge_plus_button()
        services.confirm_lounge_bussiness_modal()
        
        services.add_special_asistance_services()
        services.click_on_add_special_asistance_plus_button()
        services.confirm_special_asistance_modal()
        
        services.continue_to_the_next_step()

    # --- Seats ---
    with allure.step("Test select seats page"):
        
        seat_map.load()
        seat_map.select_seats_for_odd_passengers()
        seat_map.continue_to_the_next_step()

    # --- Payment ---
    with allure.step("Test fill payment form page"):
        payment_page.load()

        payment_page.select_avianca_credits(params["a_credits_number"], params["a_credits_pin"])       

        payment_page.accept_terms_and_conditions()
        payment_page.click_continue()
        payment_page.loader()
        payment_page.loader()

    # --- Itinerary ---
    with allure.step("Test itinerary page"):
        itinerary_page.wait_for_loader_c_disappear()
        itinerary_page.get_reservation_code()
        itinerary_page.validate_departure_city(params["city_origin"])
        itinerary_page.validate_arrival_city(params["city_destination"])
        itinerary_page.validate_passenger_adult_number(str(params["passenger_count"]))


    
