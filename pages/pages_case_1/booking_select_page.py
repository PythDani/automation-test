
import json
import time
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
        try:
            button = self.wait_to_be_clickable(locator)
            self.driver.implicitly_wait(2)
            button.click()
        except Exception as e:
            self.logger.error(f"Failed to click relative date button: {e}")
            self.logger.info("Printing DOM for debugging...")
            self._print_page_html_for_debugging()
            raise

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
            
            # Try multiple strategies to find the flight button
            flight_button = None
            
            # Strategy 1: Try the original locator
            try:
                flight_button = self.wait_to_be_clickable(self.FLIGHT_BUTTON)
                self.logger.info("Flight button found with original locator")
            except Exception as e:
                self.logger.warning(f"Original flight button locator failed: {e}")
                
                # Strategy 2: Try alternative locators
                alternative_flight_locators = [
                    (By.XPATH, "//button[contains(@class,'flight-select')]"),
                    (By.XPATH, "//div[contains(@class,'flight-card')]//button"),
                    (By.XPATH, "//*[contains(@class,'select-flight')]"),
                    (By.XPATH, "//button[contains(text(),'Seleccionar')]"),
                    (By.XPATH, "//button[contains(text(),'Select')]")
                ]
                
                for i, locator in enumerate(alternative_flight_locators):
                    try:
                        self.logger.info(f"Trying alternative flight locator {i+1}: {locator}")
                        flight_button = self.wait_to_be_clickable(locator)
                        self.logger.info(f"Flight button found with alternative locator {i+1}")
                        break
                    except Exception as alt_e:
                        self.logger.warning(f"Alternative flight locator {i+1} failed: {alt_e}")
                        continue
            
            if flight_button is None:
                raise Exception("Could not find flight button with any locator strategy")

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
            self.logger.info("Looking for Basic fare button...")
            basic_fare_button = None
            
            # Strategy 1: Try the original locator
            try:
                self.logger.info("Trying original fare button locator: //div[@role='button' and contains(@class, 'fare-control')]")
                basic_fare_button = self.wait_to_be_clickable(self.BASIC_FARE_BUTTON)
                self.logger.info("Basic fare button found with original locator.")
            except Exception as e:
                self.logger.warning(f"Original fare button locator failed: {e}")
                
                # Strategy 2: Try alternative locators
                alternative_fare_locators = [
                    (By.XPATH, "//div[contains(@class, 'fare-control')]"),
                    (By.XPATH, "//button[contains(@class, 'fare-control')]"),
                    (By.XPATH, "//div[@role='button' and contains(@class, 'fare')]"),
                    (By.XPATH, "//*[contains(@class, 'fare-control') and @role='button']"),
                    (By.XPATH, "//div[contains(@class, 'fare') and contains(@class, 'control')]"),
                    (By.XPATH, "//*[contains(text(), 'Basic') and contains(@class, 'fare')]"),
                    (By.XPATH, "//*[contains(@class, 'fare')]//button"),
                    (By.XPATH, "//*[contains(@class, 'fare')]//div[@role='button']")
                ]
                
                for i, locator in enumerate(alternative_fare_locators):
                    try:
                        self.logger.info(f"Trying alternative fare locator {i+1}: {locator}")
                        basic_fare_button = self.wait_to_be_clickable(locator)
                        self.logger.info(f"Basic fare button found with alternative locator {i+1}.")
                        break
                    except Exception as alt_e:
                        self.logger.warning(f"Alternative fare locator {i+1} failed: {alt_e}")
                        continue
            
            if basic_fare_button is None:
                raise Exception("Could not find Basic fare button with any locator strategy")
            
            # Ensure element is interactable
            self.logger.info("Ensuring fare button is interactable...")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", basic_fare_button)
            time.sleep(0.5)
            
            # Check element properties
            self.logger.info(f"Fare button is_displayed: {basic_fare_button.is_displayed()}")
            self.logger.info(f"Fare button is_enabled: {basic_fare_button.is_enabled()}")
            
            # Try to click with multiple strategies
            try:
                self.logger.info("Attempting direct click on fare button...")
                basic_fare_button.click()
                self.logger.info("Fee selected with direct click.")
            except Exception as click_e:
                self.logger.warning(f"Direct click failed: {click_e}, trying JavaScript click...")
                self.driver.execute_script("arguments[0].click();", basic_fare_button)
                self.logger.info("Fee selected with JavaScript click.")
                
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
        try:
            self.wait_for_loader_to_disappear(self.LOADER_B)
        except Exception as e:
            self.logger.warning(f"Loader did not disappear within timeout: {e}")
            # Continue anyway, as the page might still be functional
            pass

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
    
    def _print_page_html_for_debugging(self):
        """
        Print the current page HTML for debugging purposes.
        This method is specifically designed to help debug DOM elements
        when locators fail to find elements.
        """
        try:
            # Get current URL to identify the page
            current_url = self.driver.current_url
            self.logger.info(f"=== DEBUGGING HTML FOR URL: {current_url} ===")
            
            # Get page title
            page_title = self.driver.title
            self.logger.info(f"Page Title: {page_title}")
            
            # Get the full HTML source
            html_source = self.driver.page_source
            
            # Save HTML to a file for detailed analysis
            import os
            debug_dir = "debug_html"
            if not os.path.exists(debug_dir):
                os.makedirs(debug_dir)
            
            # Create filename with timestamp
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{debug_dir}/booking_select_page_debug_{timestamp}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_source)
            
            self.logger.info(f"Full HTML saved to: {filename}")
            
            # Print key elements for quick analysis
            self.logger.info("=== QUICK DOM ANALYSIS ===")
            
            # Count different types of elements
            buttons = self.driver.find_elements("tag name", "button")
            day_controls = self.driver.find_elements("xpath", "//*[contains(@class, 'day-control')]")
            day_selector_items = self.driver.find_elements("xpath", "//*[contains(@class, 'day-selector_item')]")
            
            self.logger.info(f"Total buttons found: {len(buttons)}")
            self.logger.info(f"Total day-control elements found: {len(day_controls)}")
            self.logger.info(f"Total day-selector_item elements found: {len(day_selector_items)}")
            
            # Look for elements with aria-label containing 'Schedule.A11y.CalendarDay.AriaLabel'
            calendar_elements = self.driver.find_elements("xpath", "//*[contains(@aria-label, 'Schedule.A11y.CalendarDay.AriaLabel')]")
            self.logger.info(f"Elements with calendar aria-label: {len(calendar_elements)}")
            
            # Print details of calendar elements
            for i, element in enumerate(calendar_elements[:5]):  # First 5 elements
                try:
                    tag_name = element.tag_name
                    aria_label = element.get_attribute("aria-label") or ""
                    classes = element.get_attribute("class") or ""
                    element_id = element.get_attribute("id") or ""
                    self.logger.info(f"Calendar element {i+1}: <{tag_name}> aria-label='{aria_label}' class='{classes}' id='{element_id}'")
                except Exception as e:
                    self.logger.warning(f"Could not analyze calendar element {i+1}: {e}")
            
            # Look for day-selector_item elements
            for i, item in enumerate(day_selector_items[:5]):  # First 5 items
                try:
                    classes = item.get_attribute("class") or ""
                    element_id = item.get_attribute("id") or ""
                    inner_html = item.get_attribute("innerHTML")[:200]  # First 200 chars
                    self.logger.info(f"Day selector item {i+1}: class='{classes}' id='{element_id}' innerHTML='{inner_html}...'")
                except Exception as e:
                    self.logger.warning(f"Could not analyze day selector item {i+1}: {e}")
            
            self.logger.info("=== END DOM ANALYSIS ===")
            
        except Exception as e:
            self.logger.error(f"Error during HTML debugging: {e}")
          
                    
        
        
