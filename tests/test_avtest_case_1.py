"""
  Test case number 1
  Caso automatizado 1: Realizar booking / reserva One-way (Solo ida).

  @Author: Rafael Daniel Farfán
"""
import allure


@allure.title("Automated case 1: One way booking")
@allure.severity(allure.severity_level.NORMAL)
def test_avtest_case_1(booking_context):
    page = booking_context["page"]
    form = booking_context["form"]
    services = booking_context["services"]
    seat_map = booking_context["seat_map"]
    payment_page = booking_context["payment_page"]
    booking_select_page = booking_context["booking_select_page"]
    itinerary_page = booking_context["itinerary_page"]
    params = booking_context["params"]

    # --- Home Page ---
    with allure.step("Test Home page"):
        page.load()
        page.select_language(params["language"])
        page.select_currency(params["currency"])
        page.select_one_way_radio_button()
        page.select_origin(params["city_origin"])
        page.select_destination(params["city_destination"])
        page.select_deaperture_date(**params["departure_date"])
        page.click_plus_adult(times=params["passenger_count"])
        page.confirm_button_passengers_quantity()
        page.click_search_flight_button()

    page.loader_a()

    # --- Booking Select ---
    with allure.step("Test Booking Select page"):
        booking_select_page.click_drop_down_flight()
        booking_select_page.click_on_fare_flight()
        booking_select_page.loader_b()
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
        services.continue_to_the_next_step()

    # --- Seats ---
    with allure.step("Test select seats page"):
        
        seat_map.load()
        seat_map.select_seats_based_on_quantity_of_passengers()
        seat_map.continue_to_the_next_step()

    # --- Payment ---
    with allure.step("Test fill payment form page"):
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

    # --- Itinerary ---
    with allure.step("Test itinerary page"):
        itinerary_page.get_reservation_code()
        itinerary_page.validate_departure_city(params["city_origin"])
        itinerary_page.validate_arrival_city(params["city_destination"])
        itinerary_page.validate_passenger_adult_number(str(params["passenger_count"]))


    
