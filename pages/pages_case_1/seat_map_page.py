

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.common import Common
from logger import get_logger
import time


from utils.exception import catch_exceptions



class SeatMapPage(Common):
    #Loader that indicate that the page is loading in some cases.
    LOADER_C:             tuple = (By.CLASS_NAME, "loading")
    PAX_TYPE:             tuple = (By.CLASS_NAME, "paxtype_total_value")
    AVAILABLE_SEATS:      tuple = (By.CSS_SELECTOR, "button.seat.ng-star-inserted")
    CONFIRM_BUTTON:       tuple = (By.XPATH, "//button[contains(@class, 'amount-summary_button') and .//span[normalize-space()='Continuar']]")
    

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
        Continues to the next step by clicking the "Continuar" button.

        This method waits until the "Continuar" button is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.

        """
        try:
            # Wait for the button to appear
            self.logger.info("Waiting for the button to appear...")
            add_bussines_on_button = self.wait_for(self.CONFIRM_BUTTON)

            # Scroll to the button
            self.scroll_down_move_to_element(add_bussines_on_button)
            self.logger.info("Scroll to the button Continue...'")

            # SLEEP(1) added
            time.sleep(1)

            # Click the button            
            self.driver.execute_script("arguments[0].click();", add_bussines_on_button)
            self.logger.info("Seats added... Going to the payment page...")
        except Exception as e:
            self.logger.error(f"Error clicking on continue button: {str(e)}")
            raise

