

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.common import Common
from selenium.common.exceptions import TimeoutException
from logger import get_logger


class SeatMapPage(Common):
    #Loader that indicate that the page is loading in some cases.
    LOADER_C:             tuple = (By.CLASS_NAME, "loading")
    PAX_TYPE:             tuple = (By.CLASS_NAME, "paxtype_total_value")
    AVAILABLE_SEATS:      tuple = (By.CSS_SELECTOR, "button.seat.ng-star-inserted")
    
    def __init__(self, driver):
        """
        Initialize a SeatMapPage instance.

        Args:
            driver (selenium.webdriver): A selenium webdriver instance.
        """

        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)

    def load(self):
        """
        Load the page and wait for the page loader to disappear.

        This method is used to load the page and wait until the page loader
        disappears. If the page loader does not disappear within the timeout
        period, a TimeoutException is raised.

        """
    
        # We wait unitll the page loader disapear.
        try:
            self.logger.info("Waiting for page to load disappear...")
            # EXecute the wait_for_loader_to_disappear method twice
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.logger.info("Page loaded correctly.")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {self.__class__.__name__}") from e
        
    def select_seats_based_on_passengers(self):
        """
        Select seats based on passengers count.

        This method selects seats based on the count of passengers
        found on the page. It refreshes the list of available seats
        after each selection to avoid stale element errors.

        If there are not enough available seats, an Exception is raised.

        :return: None
        """
        try:
            self.logger.info("Get passengers count...")

            # Get passengers count
            passengers_element = self.wait_for(self.PAX_TYPE)
            # Wait until passengers count is not empty
            self._wait.until(lambda driver: passengers_element.text.strip() != '')
            passengers_count = int(passengers_element.text.strip())

            self.logger.info(f"Quantity of passengers found: {passengers_count}")

            selected_seats = 0

            while selected_seats < passengers_count:
                # Re-obtain available seats in each iteration to avoid stale element issues
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
                        break  # Break inner for-loop to refresh available seats list
                    except Exception as click_error:
                        self.logger.warning(f"Could not click on seat {seat_label}: {click_error}. Trying next seat...")

                else:
                    # If no seat was selected in this iteration
                    raise Exception("Could not find a clickable available seat.")

        except Exception as e:
            self.logger.error(f"Error selecting seats: {str(e)}")
            raise



