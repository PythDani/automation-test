
import json
from seleniumwire.utils import decode
from pages.common import Common
from logger import get_logger
from selenium.webdriver.common.by import By
from utils.exception import catch_exceptions

from config import HOME_URL

class BookingSelectPage(Common):   
    #Loader that indicate that the page is loading in some cases.
    LOADER_B:                            tuple = (By.XPATH, "//*[contains(@class, 'page-loader') or contains(@class, 'loading') or contains(@class, 'loader')]")
    # Select another date button
    SELECT_ANOTHER_DATE_BUTTON:          tuple = (By.XPATH, "//*[@class='day-selector_item ng-star-inserted'][{}]//*[contains(@class,'day-control') and contains(@aria-label,'Schedule.A11y.CalendarDay.AriaLabel')]")   
    #Flight button
    FLIGHT_BUTTON:                       tuple = (By.XPATH, "(//*[@class='journey-select_list ng-star-inserted']/*)[1]//*[@class='journey_price']")
    # Flight button return
    FLIGHT_BUTTON_RETURN:                tuple = (By.XPATH, "(//*[@class='journey-select_journey-filter ng-star-inserted']/following-sibling::*[@class='journey-select_list ng-star-inserted']/*)[1]//*[@class='journey_price']")
    # BASIC_FARE_BUTTON 
    BASIC_FARE_BUTTON:                   tuple = (By.XPATH, "//div[@role='button' and contains(@class, 'fare-control')]")
    # Continue button
    CONTINUE_BUTTON:                     tuple = (By.XPATH, "//*[@id='maincontent']/div/div[2]/div/div/button-container/div/div/button")
    # Relative day mapping
    RELATIVE_DAY_MAPPING = {
    "3 days before": 1,
    "2 days before": 2,
    "1 day before": 3,
    "1 day after": 4,
    "2 days after": 5,
    "3 days after": 6,
}
    @catch_exceptions()
    def __init__(self, driver):
        """
        Initialize a BookingSelectPage instance.

        Args:
            driver (selenium.webdriver): A selenium webdriver instance.
        """
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)
    
    @catch_exceptions()
    def click_relative_date(self, label):
        """
        Clicks on the departure date option based on a human-readable label.

        Args:
            label (str): One of the keys in RELATIVE_DAY_MAPPING, like "2 días después"
        """
        self.loader_b()
        self.logger.info(f"Resolving label '{label}' to index...")

        index = self.RELATIVE_DAY_MAPPING.get(label)
        if index is None:
            raise ValueError(f"Invalid label '{label}' passed. Expected one of: {list(self.RELATIVE_DAY_MAPPING)}")

        xpath = self.SELECT_ANOTHER_DATE_BUTTON[1].format(index)
        locator = (self.SELECT_ANOTHER_DATE_BUTTON[0], xpath)

        self.logger.info(f"Clicking on element with label '{label}' and xpath: {xpath}")
        button = self.wait_to_be_clickable(locator)

        self.driver.implicitly_wait(2)
        button.click()
    
    @catch_exceptions()
    def click_drop_down_flight(self):
        """
        Clicks on the dropdown button of the flight to select a tariff.
        
        This method waits until the button is clickable, moves to the element using
        ActionChains, clicks on it, and logs the action performed. If the button is not
        found or clickable within the timeout period, a TimeoutException is raised.
        """
        try:
            self.loader_b()
            flight_button = self.wait_to_be_clickable(self.FLIGHT_BUTTON)                

            self._action.move_to_element(flight_button).perform()
            self.driver.implicitly_wait(2)        

            flight_button.click()
            self.logger.info("Flight selected")
        except Exception as e:
            self.logger.error(f"No flights found: {str(e)}")
            raise

    @catch_exceptions()  
    def click_drop_down_return_flight(self):
        """
        Clicks on the dropdown button of the flight to select a tariff.
        
        This method waits until the button is clickable, moves to the element using
        ActionChains, clicks on it, and logs the action performed. If the button is not
        found or clickable within the timeout period, a TimeoutException is raised.
        """
        try:
            self.loader_b()
            self.scroll_down_by_pixels(350)
            flight_button = self.wait_to_be_clickable(self.FLIGHT_BUTTON_RETURN)                         

            self._action.move_to_element(flight_button).perform()
            self.driver.implicitly_wait(2)            

            flight_button.click()
            self.logger.info("Return flight selected")
        except Exception as e:
            self.logger.error(f"No flights found: {str(e)}")
            raise

    @catch_exceptions()
    def click_on_fare_flight(self):
        """
        Clicks on the 'Basic' fare button.

        This method waits until the button is clickable, moves to the element using
        ActionChains, clicks on it, and logs the action performed. If the button is not
        found or clickable within the timeout period, a TimeoutException is raised.
        """
        try:
            basic_fare_button = self.wait_to_be_clickable(self.BASIC_FARE_BUTTON)        

            self._action.move_to_element(basic_fare_button).perform()
            self.scroll_down_by_pixels(350)
            self.driver.implicitly_wait(1)        

            basic_fare_button.click()
            self.logger.info("Fee selected")
        except Exception as e:
            self.logger.error(f"Error selecting fee: {str(e)}")
            raise
    
    @catch_exceptions()
    def loader_b(self):
        """
        Waits for the page loader to disappear.

        This method waits until the page loader disappears. If the loader does not
        disappear within the timeout period, a TimeoutException is raised.

        """
        self.wait_for_loader_to_disappear(self.LOADER_B)

    @catch_exceptions()
    def button_continue_to_move_to_passenger_form(self):
        """
        Clicks the "Continue" button to move to the passenger form.

        This method waits until the button is visible, scrolls down to the element
        using ActionChains, clicks on it, and logs the action performed. If the button
        is not found or clickable within the timeout period, a TimeoutException is raised.
        """
        try:
            continue_button = self.find(self.CONTINUE_BUTTON)

            #Scroll down to move to the button       
            self._action.move_to_element(continue_button).perform()              
            continue_button.click()
            self.logger.info("Button continue clicked.")
        except Exception as e:
            self.logger.error(f"Error clicking continue button: {str(e)}")
            raise
    
    def get_sesion_params(self):       
       
        """
        Get the session parameters from the last request.

        This method searches the last request with url
        "https://nuxqa.avtest.ink/booking/api/v1/booking/session" and decodes the body
        using the encoding specified in the response headers. The body is then
        converted to a JSON object and searched for the "Data required from network -
        session" parameters.

        The method returns a list of dictionaries, where each dictionary contains the
        parameters for a journey:

        - origin: string
        - destination: string
        - std: string
        - productClass: list of strings

        If no session url response is found or if an error occurs during decoding or
        parsing, the method returns None.

        :return: list of dictionaries or None
        """
        for request in self.driver.requests:
            if request.response:
                if request.url == "https://nuxqa.avtest.ink/booking/api/v1/booking/session":
                    try:
                        self.logger.info(f"Session response (url): {request.url}")
                        # Decode the body according to the encoding
                        body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                        body_content = body.decode('utf-8')                        
                                             
                        # Convert the body to a JSON object
                        json_data = json.loads(body_content)
                        self.logger.info(f"Session response (json): {json.dumps(json_data, indent=2)}")
                        
                        # Get the "Data required from network - session"
                        journeys = json_data.get("booking", {}).get("journeys", [])
                        result = []
                        for journey in journeys:
                            origin = journey.get("origin")
                            self.logger.info(f"Origin: {origin}")
                            destination = journey.get("destination")
                            std = journey.get("std")
                            self.logger.info(f"Journey: Origin: {origin}, Destination: {destination}, STD: {std}")
                            fares = journey.get("fares", [])
                            product_classes = [fare.get("productClass") for fare in fares if "productClass" in fare]
                            self.logger.info(f"Product classes: {product_classes}")

                            result.append({
                                "origin": origin,
                                "destination": destination,
                                "std": std,
                                "productClass": product_classes
                            })

                        return result

                    except Exception as e:
                        self.logger.error(f"Error decoding session response: {e}")
                        return None

        # If no session url response is found
        self.logger.warning("No session url response found")
        return None
          
                    
        
        
