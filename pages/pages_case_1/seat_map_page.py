

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.common import Common
from logger import get_logger
import time


from utils.exception import catch_exceptions



class SeatMapPage(Common):
    #Loader that indicate that the page is loading in some cases.
    LOADER_C:             tuple = (By.XPATH, "//*[contains(@class, 'page-loader') or contains(@class, 'loading') or contains(@class, 'loader')]")
    PAX_TYPE:             tuple = (By.CLASS_NAME, "paxtype_total_value")
    AVAILABLE_SEATS:      tuple = (By.CSS_SELECTOR, "button.seat.ng-star-inserted")
    CONFIRM_BUTTON:       tuple = (By.XPATH, "//button[contains(@class,'button btn-action btn-Medium')]//span[contains(text(),'Ir a pagar')]")
    

    @catch_exceptions()
    def __init__(self, driver):
        """
        Initialize a SeatMapPage instance.

        Args:
            driver (selenium.webdriver): A selenium webdriver instance.
        """

        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)
    
    @catch_exceptions()
    def load(self):
        """
        Load the page and wait for the page loader to disappear.

        This method is used to load the page and wait until the page loader
        disappears. If the page loader does not disappear within the timeout
        period, a TimeoutException is raised.

        """
    
        # We wait unitll the page loader disapear.
        try:
            self.logger.info("Waiting for loader to disappear...")
            # EXecute the wait_for_loader_to_disappear method twice
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.logger.info("Page loaded correctly.")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {self.__class__.__name__}") from e

    @catch_exceptions()  
    def select_seats_based_on_quantity_of_passengers(self):
        """
        Select seats based on passengers count.
        """
        try:
            self.logger.info("Get passengers count...")            

            try:
                # Try finding the main passenger counter
                passengers_element = self.wait_for(self.PAX_TYPE)
                self._wait.until(lambda driver: passengers_element.text.strip() != '')
                passengers_count = int(passengers_element.text.strip())
            except TimeoutException:
                # If the main counter is not available (e.g., screen maximized), fallback to default or alternate
                self.logger.warning("Could not find 'paxtype_total_value'. Trying alternative method...")
                alt_locator = (By.CLASS_NAME, "paxtype_label")
                alt_elements = self.find_all(alt_locator)
                passengers_count = len(alt_elements)
                if passengers_count == 0:
                    raise Exception("No passengers info found using any method.")

            self.logger.info(f"Quantity of passengers found: {passengers_count}")

            selected_seats = 0

            while selected_seats < passengers_count:
                available_seats = self.find_all(self.AVAILABLE_SEATS)

                self.logger.info(f"Number of available seats found: {len(available_seats)}")

                for seat in available_seats:
                    seat_label = seat.text.strip() or seat.get_attribute('aria-label').strip()

                    if "no disponible" in seat_label.lower():
                        self.logger.info(f"Seat {seat_label} is not available. Skipping...")
                        continue

                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seat)
                        seat.click()
                        self.wait_for_loader_to_disappear(self.LOADER_C)
                        self.logger.info(f"Seat {seat_label} selected.")
                        selected_seats += 1
                        break
                    except Exception as click_error:
                        self.logger.warning(f"Could not click on seat {seat_label}: {click_error}. Trying next seat...")

                else:
                    raise Exception("Could not find a clickable available seat.")

        except Exception as e:
            self.logger.error(f"Error selecting seats: {str(e)}")
            raise
    
    @catch_exceptions()
    def select_seats_for_odd_passengers(self):
        """
        Select seats only for passengers in odd positions (1st, 3rd, 5th, etc.).
        """
        try:
            self.logger.info("Searching for passenger items...")

            # Find all passenger items
            pax_selector_xpath = "//*[contains(@class,'pax-selector_list')]"
            pax_list = self.wait_for((By.XPATH, pax_selector_xpath))
            pax_items = pax_list.find_elements(By.XPATH, ".//div[contains(@class, 'pax-selector_item')]")

            self.logger.info(f"Total passenger elements found: {len(pax_items)}")

            selected_seats = 0

            for index, item in enumerate(pax_items):
                if index % 2 == 0:  
                    try:
                        # Click on "Seleccionar" button
                        button = item.find_element(By.XPATH, ".//button")
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                        button.click()
                        self.logger.info(f"Passenger #{index + 1} selected.")

                        # Find available seats
                        available_seats = self.find_all(self.AVAILABLE_SEATS)

                        self.logger.info(f"Available seats found: {len(available_seats)}")

                        for seat in available_seats:
                            seat_label = seat.text.strip() or seat.get_attribute('aria-label').strip()

                            if "no disponible" in seat_label.lower():
                                continue

                            try:
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seat)
                                seat.click()
                                self.wait_for_loader_to_disappear(self.LOADER_C)
                                self.logger.info(f"Seat {seat_label} assigned to passenger #{index + 1}")
                                selected_seats += 1
                                break
                            except Exception as seat_error:
                                self.logger.warning(f"Could not click on seat {seat_label}: {seat_error}")
                        else:
                            self.logger.warning(f"No seat could be selected for passenger #{index + 1}")
                    except Exception as item_error:
                        self.logger.warning(f"Could not select passenger #{index + 1}: {item_error}")

            self.logger.info(f"Total odd-position passengers with seats: {selected_seats}")

        except Exception as e:
            self.logger.error(f"Error assigning seats to odd passengers: {str(e)}")
            raise

    @catch_exceptions()
    def continue_to_the_next_step(self):     
        """
        Continues to the next step by clicking the "Continue" button.

        This method waits until the "Continue" button is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.

        """
        try:
            self.logger.info("Waiting for the button to appear...")
            
            # Wait for any loaders to disappear first
            self.logger.info("Waiting for loaders to disappear...")
            try:
                self.wait_for_invisibility(self.LOADER_C)
                self.logger.info("Loaders disappeared.")
            except:
                self.logger.warning("Loader wait timed out, continuing...")
            
            # Additional wait to ensure page is stable
            time.sleep(1)
            
            # First, scroll down to ensure modal content is visible
            self.logger.info("Scrolling down to make continue button visible...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Try multiple locator strategies (same as services_page)
            self.logger.info("Trying to find seat map continue button...")
            
            # First, let's diagnose what's in the DOM
            self.logger.info("Diagnosing DOM for seat map continue button...")
            try:
                # Check if any buttons with "Ir a pagar" text exist
                ir_pagar_buttons = self.driver.find_elements(By.XPATH, "//button//span[contains(text(),'Ir a pagar')]")
                self.logger.info(f"Found {len(ir_pagar_buttons)} buttons with 'Ir a pagar' text")
                
                # Check if any buttons with btn-action class exist
                action_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class,'btn-action')]")
                self.logger.info(f"Found {len(action_buttons)} buttons with 'btn-action' class")
                
                # Check if any buttons with dsButtonId exist
                ds_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@id,'dsButtonId_')]")
                self.logger.info(f"Found {len(ds_buttons)} buttons with 'dsButtonId_' pattern")
                
                # Log current page source snippet for debugging
                page_source = self.driver.page_source
                if "Ir a pagar" in page_source:
                    self.logger.info("'Ir a pagar' text found in page source")
                else:
                    self.logger.warning("'Ir a pagar' text NOT found in page source")
                    
            except Exception as e:
                self.logger.warning(f"DOM diagnosis failed: {e}")
            
            # Strategy: Try to find the button using find_elements (not wait_to_be_clickable)
            continue_button = None
            
            # Try different locators to find the button
            locators_to_try = [
                self.CONFIRM_BUTTON,
                (By.XPATH, "//button[contains(@class,'btn-action btn-Medium')]//span[text()='Ir a pagar']"),
                (By.XPATH, "//button//span[text()='Ir a pagar']"),
                (By.XPATH, "//button[contains(@id,'dsButtonId_')]//span[text()='Ir a pagar']"),
                (By.XPATH, "//button[contains(@class,'button') and contains(@class,'btn-action')]"),
                (By.XPATH, "//button[contains(@class,'btn-action')]//span[contains(text(),'Ir a pagar')]"),
                (By.XPATH, "//button[contains(@class,'btn-action')]"),
                (By.XPATH, "//button[contains(@id,'dsButtonId_')]"),
                (By.XPATH, "//span[contains(text(),'Ir a pagar')]/parent::button"),
                (By.XPATH, "//span[contains(text(),'Ir a pagar')]/ancestor::button"),
                (By.XPATH, "//button[.//span[contains(text(),'Ir a pagar')]]"),
                (By.XPATH, "//button[contains(@class,'button')]//span[contains(text(),'Ir a pagar')]"),
                (By.XPATH, "//button[contains(@class,'btn')]//span[contains(text(),'Ir a pagar')]")
            ]
            
            for i, locator in enumerate(locators_to_try):
                try:
                    buttons = self.driver.find_elements(*locator)
                    if buttons:
                        # Find the button that contains "Ir a pagar" text
                        for button in buttons:
                            try:
                                button_text = button.text.strip()
                                button_html = button.get_attribute("innerHTML") or ""
                                
                                # Check for "Ir a pagar" text in various ways
                                if ("Ir a pagar" in button_text or 
                                    "Ir a pagar" in button_html or
                                    "pagar" in button_text.lower() or
                                    "pagar" in button_html.lower()):
                                    continue_button = button
                                    self.logger.info(f"Seat map continue button found with locator strategy {i+1}")
                                    self.logger.info(f"Button text: '{button_text}', HTML: '{button_html[:100]}...'")
                                    break
                            except Exception as btn_error:
                                self.logger.warning(f"Error checking button: {btn_error}")
                                continue
                        if continue_button:
                            break
                except Exception as e:
                    self.logger.warning(f"Locator strategy {i+1} failed: {e}")
                    continue
            
            if not continue_button:
                self.logger.error("Could not find seat map continue button with any strategy")
                raise Exception("Could not find seat map continue button with any strategy")
            
            self.logger.info("Seat map continue button found, ensuring it's visible and clickable...")

            # Enhanced scroll strategy to ensure button is visible
            self.logger.info("Performing enhanced scroll to make seat map continue button visible...")
            self.driver.execute_script("""
                var button = arguments[0];
                
                // First, scroll to the very bottom to ensure modal is fully loaded
                window.scrollTo(0, document.body.scrollHeight);
                
                // Wait a moment for scroll to complete
                setTimeout(function() {
                    // Scroll the button into view with center alignment
                    button.scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});
                    
                    // Additional scroll down to ensure button is not at the very bottom edge
                    setTimeout(function() {
                        window.scrollBy(0, 100);
                        
                        // Remove any overlays that might be blocking
                        var overlays = document.querySelectorAll('.modal-backdrop, .overlay, .loading, [class*="backdrop"]');
                        overlays.forEach(function(overlay) {
                            overlay.style.display = 'none';
                            overlay.style.visibility = 'hidden';
                        });
                        
                        // Make sure button is clickable
                        button.style.pointerEvents = 'auto';
                        button.style.zIndex = '9999';
                        button.style.position = 'relative';
                        button.style.display = 'block';
                        button.style.visibility = 'visible';
                    }, 300);
                }, 500);
            """, continue_button)
            
            time.sleep(2)  # Wait for scroll to complete

            # Verify button is visible before clicking
            self.logger.info("Verifying seat map continue button is visible and clickable...")
            if not continue_button.is_displayed():
                self.logger.warning("Button is not displayed, trying additional scroll...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
                time.sleep(1)

            # Try different click strategies
            try:
                continue_button.click()
                self.logger.info("Seats added... Going to the payment page... with direct click.")
            except Exception as e:
                self.logger.warning(f"Direct click failed: {e}, trying JavaScript click...")
                self.driver.execute_script("arguments[0].click();", continue_button)
                self.logger.info("Seats added... Going to the payment page... with JavaScript click.")
                
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to continue to payment page") from e
        except Exception as e:
            self.logger.error(f"Error clicking on continue button: {str(e)}")
            raise

