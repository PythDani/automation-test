

from logger import get_logger
from pages.common import Common
from selenium.webdriver.common.by import By


class BookingSelectPage(Common):
    #Loader
    LOADER:                                         tuple = (By.CLASS_NAME, "loader")
    #Loader that indicate that the page is loading in some cases.
    LOADER_B:                                       tuple = (By.CLASS_NAME, "page-loader")
    #Flight button
    FLIGHT_BUTTON:                                  tuple = (By.XPATH, "//*[@class='journey_price_button ng-tns-c12-2 ng-star-inserted']")
    # BASIC_FARE_BUTTON 
    BASIC_FARE_BUTTON:                              tuple = (By.XPATH, "//div[@role='button' and contains(@class, 'fare-control') and .//span[contains(text(), 'basic')]]")
    # Continue button
    CONTINUE_BUTTON:                                tuple = (By.XPATH, "//*[@id='maincontent']/div/div[2]/div/div/button-container/div/div/button")
    def __init__(self, driver):
        """
        Initialize a BookingSelectPage instance.

        Args:
            driver (selenium.webdriver): A selenium webdriver instance.
        """
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)
    
    def click_drop_down_flight(self):
        """
        Clicks on the dropdown button of the flight to select a tariff.
        
        This method waits until the button is clickable, moves to the element using
        ActionChains, clicks on it, and logs the action performed. If the button is not
        found or clickable within the timeout period, a TimeoutException is raised.
        """
        flight_button = self.wait_to_be_clickable(self.FLIGHT_BUTTON)        
        self._action.move_to_element(flight_button).perform()        
        flight_button.click()
        self.logger.info("Flight selected")

    def click_on_fare_flight(self):
        """
        Clicks on the 'Basic' fare button.

        This method waits until the button is clickable, moves to the element using
        ActionChains, clicks on it, and logs the action performed. If the button is not
        found or clickable within the timeout period, a TimeoutException is raised.
        """
        basic_fare_button = self.wait_to_be_clickable(self.BASIC_FARE_BUTTON)        
        self._action.move_to_element(basic_fare_button).perform()        
        basic_fare_button.click()
        self.logger.info("Fee selected")
    
    def loader_b(self):
        """
        Waits for the page loader to disappear.

        This method waits until the page loader disappears. If the loader does not
        disappear within the timeout period, a TimeoutException is raised.

        """
        self.wait_for_invisibility(self.LOADER_B)

    def button_continue_to_move_to_passenger_form(self):
        """
        Clicks the "Continue" button to move to the passenger form.

        This method waits until the button is visible, scrolls down to the element
        using ActionChains, clicks on it, and logs the action performed. If the button
        is not found or clickable within the timeout period, a TimeoutException is raised.
        """
        continue_button = self.find(self.CONTINUE_BUTTON)

        #Scroll down to move to the button       
        self._action.move_to_element(continue_button).perform()              
        continue_button.click()
        self.logger.info("Button continue clicked.") 