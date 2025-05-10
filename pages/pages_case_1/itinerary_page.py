

from selenium.webdriver.common.by import By
from logger import get_logger
from pages.common import Common
from utils.exception import catch_exceptions


class ItineraryPage(Common):
    # Page loader
    LOADER_C:                  tuple = (By.XPATH, "//*[contains(@class,'loading')]")
    # Departure city
    DEPARTURE_CITY:     tuple = (By.XPATH, "//*[contains(@class,'summary_travel_departure')]")
    # Arrival city
    ARRIVAL_CITY:       tuple = (By.XPATH, "//*[@class='summary_travel']//*[contains(@class,'summary_travel_arival')]")   
    # Details button
    DETAILS_BUTTON:     tuple = (By.XPATH, "//*[contains(@class,'price-breakdown-header')]")
    # Passengers number
    PASSENGERS_NUMBER:  tuple = (By.XPATH, "//*[@class='price-breakdown-item']//*[@class='price-breakdown-item_label_quantity-value']")

    
    @catch_exceptions()
    def __init__(self, driver):
        """
        Initialize an ItineraryPage instance.

        Args:
            driver (selenium.webdriver): A selenium webdriver instance.
        """

        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)

    @catch_exceptions()
    def departure_city(self):

        """
        Retrieves the departure city from the itinerary page.

        This method waits for the page loader to disappear and then extracts
        the departure city from the page. It logs the retrieved departure city
        and returns it.

        Returns:
            str: The departure city extracted from the itinerary page.
        """

        departure_city = self.find(self.DEPARTURE_CITY).text
        self.logger.info(f"Deaperture city: {departure_city} ")
        return departure_city
    
    @catch_exceptions()
    def arrival_city(self):        

        """
        Retrieves the arrival city from the itinerary page.

        This method extracts the arrival city from the page and logs the
        retrieved arrival city. It returns the arrival city as a string.

        Returns:
            str: The arrival city extracted from the itinerary page.
        """

        arrival_city = self.find(self.ARRIVAL_CITY).text
        self.logger.info(f"Arrival city: {arrival_city} ")
        return arrival_city
    
    @catch_exceptions()
    def validate_departure_city(self, expected_city: str):        
        """
        Validates that the departure city on the itinerary page matches the expected city.

        This method retrieves the departure city from the itinerary page and compares
        it with the expected city. It logs both the expected and the found departure city.
        An assertion error is raised if the cities do not match.

        Args:
            expected_city (str): The expected departure city.

        Raises:
            AssertionError: If the actual departure city does not match the expected city.
        """

        actual_city = self.find(self.DEPARTURE_CITY).text.strip()
        self.logger.info(f"Validating departure city. Expected: '{expected_city}', Found: '{actual_city}'")
        assert actual_city == expected_city, f"Expected '{expected_city}', but got '{actual_city}'"
    
    @catch_exceptions()
    def validate_arrival_city(self, expected_city: str):

        """
        Validates that the arrival city on the itinerary page matches the expected city.

        This method retrieves the arrival city from the itinerary page and compares
        it with the expected city. It logs both the expected and the found arrival city.
        An assertion error is raised if the cities do not match.

        Args:
            expected_city (str): The expected arrival city.

        Raises:
            AssertionError: If the actual arrival city does not match the expected city.
        """

        self.scroll_down_by_pixels(200)
        actual_city = self.find(self.ARRIVAL_CITY).text.strip()
        self.logger.info(f"Validating arrival city. Expected: '{expected_city}', Found: '{actual_city}'")
        assert actual_city == expected_city, f"Expected arrival city '{expected_city}', but got '{actual_city}'"
    
    @catch_exceptions()
    def validate_passenger_adult_number(self, expected_passenger_number: str):

        """
        Validates that the passenger number on the itinerary page matches the expected number.

        This method retrieves the passenger number from the itinerary page and compares
        it with the expected number. It logs both the expected and the found passenger number.
        An assertion error is raised if the numbers do not match.

        Args:
            expected_passenger_number (str): The expected passenger number.

        Raises:
            AssertionError: If the actual passenger number does not match the expected number.
        """
        self.scroll_down_by_pixels(200)
        detail_button = self.find(self.DETAILS_BUTTON)
        detail_button.click()

        actual_passenger_number = self.find(self.PASSENGERS_NUMBER).text
        self.logger.info(f"Validating passenger number. Expected: '{expected_passenger_number}', Found: '{actual_passenger_number}'")
        assert actual_passenger_number == expected_passenger_number, f"Expected passenger number '{expected_passenger_number}', but got '{actual_passenger_number}'"

    def wait_for_loader_c_disappear(self):        

        """
        Waits for the loader C to disappear.

        This method waits until the loader C element becomes invisible.
        If the loader C does not disappear within the timeout period, a TimeoutException is raised.

        """

        self.wait_for_loader_to_disappear(self.LOADER_C)