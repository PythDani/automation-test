

from selenium.webdriver.common.by import By
from logger import get_logger
from pages.common import Common


class ItineraryPage(Common):
    # Reservation code
    RESERVATION_CODE:   tuple = (By.XPATH, "//*[@class='booking-reference']//*[@class='code']")
    # Deaperture city
    DEPARTURE_CITY:     tuple = (By.XPATH, "//*[@class='summary_travel']//*[contains(@class,'summary_travel_departure')]")
    # Arrival city
    ARRIVAL_CITY:       tuple = (By.XPATH, "//*[@class='summary_travel']//*[contains(@class,'summary_travel_arival')]") 
    #Reserve holder
    RESERVE_HOLDER:     tuple = (By.XPATH, "//*[@class='itinerary-pax_contact-name']//*[@class='ng-star-inserted']")
    # Details button
    DETAILS_BUTTON:     tuple = (By.XPATH, "//*[contains(@class,'price-breakdown-header')]")
    # Passengers number
    PASSENGERS_NUMBER:  tuple = (By.XPATH, "//*[@class='price-breakdown-item']//*[@class='price-breakdown-item_label_quantity-value']")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)

    def get_reservation_code(self):
        reservation_code = self.find(self.RESERVATION_CODE).text
        self.logger.info(f"Reservation code: {reservation_code} ")
        return reservation_code
    
    def deaperture_city(self):        
        deaperture_city = self.find(self.DEPARTURE_CITY).text
        self.logger.info(f"Deaperture city: {deaperture_city} ")
        return deaperture_city
    
    def arrival_city(self):        
        arrival_city = self.find(self.ARRIVAL_CITY).text
        self.logger.info(f"Arrival city: {arrival_city} ")
        return arrival_city
    
    def validate_departure_city(self, expected_city: str):        
        actual_city = self.find(self.DEPARTURE_CITY).text.strip()
        self.logger.info(f"Validating departure city. Expected: '{expected_city}', Found: '{actual_city}'")
        assert actual_city == expected_city, f"Expected '{expected_city}', but got '{actual_city}'"
    
    def validate_arrival_city(self, expected_city: str):
        actual_city = self.find(self.ARRIVAL_CITY).text.strip()
        self.logger.info(f"Validating arrival city. Expected: '{expected_city}', Found: '{actual_city}'")
        assert actual_city == expected_city, f"Expected arrival city '{expected_city}', but got '{actual_city}'"
    
    def validate_reserve_holder(self, expected_reserve_holder: str):
        actual_reserve_holder = self.find(self.RESERVE_HOLDER).text.strip()
        self.logger.info(f"Validating reserve holder. Expected: '{expected_reserve_holder}', Found: '{actual_reserve_holder}'")
        assert actual_reserve_holder == expected_reserve_holder, f"Expected reserve holder '{expected_reserve_holder}', but got '{actual_reserve_holder}'"

    def validate_passenger_adult_number(self, expected_passenger_number: str):
        detail_button = self.find(self.DETAILS_BUTTON)
        detail_button.click()

        actual_passenger_number = self.find(self.PASSENGERS_NUMBER).text
        self.logger.info(f"Validating passenger number. Expected: '{expected_passenger_number}', Found: '{actual_passenger_number}'")
        assert actual_passenger_number == expected_passenger_number, f"Expected passenger number '{expected_passenger_number}', but got '{actual_passenger_number}'"