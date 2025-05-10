


from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from logger import get_logger
from pages.common import Common
from utils.exception import catch_exceptions


class PaymentPage(Common):  
    # ----------------------------------LOCATORS----------------------------------------------------------

    ONE_TRUST_ACCEPT_BUTTON:     tuple = (By.ID, "onetrust-accept-btn-handler")
    LOADER_C:                    tuple = (By.XPATH, "//*[contains(@class, 'page-loader') or contains(@class, 'loading') or contains(@class, 'loader')]")
    # Check Avianca credits
    CHECK_AVIANCA_CREDITS:       tuple = (By.XPATH, "//*[@class='toggle_input']//input[contains(@type,'checkbox')]")
    # Input number avianca credits
    INPUT_NUMBER_AVIANCA_CREDITS:tuple = (By.XPATH, "//input[contains(@id,'number') and contains(@name,'number')]")
    # Input pin avianca credits
    INPUT_PIN_AVIANCA_CREDITS:   tuple = (By.XPATH, "//input[contains(@id,'pin')]")
    # Input button
    BUTTON_ENTER_AVIANCA_CREDITS:tuple = (By.XPATH, "//*[contains(@id,'buttonAviancaCredits')]")  
    # Apply Avianca credits
    APPLY_AVIANCA_CREDITS:       tuple = (By.XPATH, "//*[contains(@class,'ds-button ds-btn-primary ds-btn-small')]") 
    
    # Click modal confirmation
    CONFIRM_MODAL:               tuple = (By.XPATH, "//button[contains(@class,'ds-button ds-btn-primary ds-btn-medium')]")
    # Payment panel
    PANEL_PAGO:                  tuple = (By.XPATH, "//*[@id='IdHere']")
    # Payment form
    CARD_HOLDER_NAME_INPUT:      tuple = (By.NAME, "Holder") 
    CARD_NUMBER_INPUT:           tuple = (By.NAME, "Data")
    CVV_INPUT:                   tuple = (By.NAME, "Cvv")
    EMAIL_INPUT:                 tuple = (By.XPATH, "//div[contains(@class, 'ds-input-container')]//input[@id='email']")
    ADDRESS_INPUT:               tuple = (By.XPATH, "//div[contains(@class, 'ds-input-container')]//input[@id='address']")
    CITY_INPUT:                  tuple = (By.XPATH, "//div[contains(@class, 'ds-input-container')]//input[@id='city']")
    CONTINUE_BUTTON:             tuple = (By.XPATH, "//button[contains(@class,'ds-button ds-btn-primary ds-btn-medium')]")
    #Modal content
    MODAL_CONTENT:               tuple = (By.XPATH, "//*[contains(@class, 'modal-content')]")
    #Close modal rejected payment
    CLOSE_MODAL:                 tuple = (By.XPATH, "//*[@class='modal-close ng-star-inserted']")
    # Button modal rejected payment
    BUTTON_MODAL_PAYMENT_REJECTED:  tuple = (By.XPATH, "//button[contains(@class,'ds-button ds-btn-primary ds-btn-medium')]")
    @catch_exceptions()
    def __init__(self, driver):
      """
      Initialize a PaymentPage instance.
      Args:
          driver (selenium.webdriver): A selenium webdriver instance.
      """
      super().__init__(driver)
      self.logger = get_logger(self.__class__.__name__)
   
    @catch_exceptions()
    def load(self):   
        """
        Load the payment page and handle page elements.

        This method clicks on the One Trust accept button and waits for the page loader
        to disappear before confirming that the page is loaded. If the loader does not 
        disappear within the timeout period, a TimeoutException is raised.
        """

        try:               
            # Click on the One Trust accept button
            self.wait_for_loader_to_disappear(self.LOADER_C)  
            one_trust_accept_button = self.wait_to_be_clickable(self.ONE_TRUST_ACCEPT_BUTTON)
            one_trust_accept_button.click()
            #We wait unitll the page loader disapear.
            self.logger.info("Waiting for loader to disappear...")
            self.wait_for_loader_to_disappear(self.LOADER_C)          
            self.logger.info("Page loaded correctly.")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {self.__class__.__name__}") from e
    
    @catch_exceptions()
    def select_avianca_credits(self, number: str, pin: str):
        """
        Select Avianca credits and fill in number and PIN.

        This method clicks on the Avianca credits checkbox, waits for the loader to disappear,
        then fills in the provided number and PIN.
        
        :param number: Avianca credits number
        :param pin: Avianca credits PIN
        """
        try:
            self.wait_for_loader_to_disappear(self.LOADER_C)
            # Click on the checkbox
            check_avianca_credits = self.find(self.CHECK_AVIANCA_CREDITS)
            check_avianca_credits.click()          

            # Fill number
            input_number = self.find(self.INPUT_NUMBER_AVIANCA_CREDITS)
            input_number.clear()
            input_number.send_keys(number)

            # Fill PIN
            input_pin = self.wait_for_visibility_of_element_located(self.INPUT_PIN_AVIANCA_CREDITS)
            input_pin.clear()
            input_pin.send_keys(pin)

            self.logger.info("Avianca credits form filled successfully.")

            submit_button = self.find(self.BUTTON_ENTER_AVIANCA_CREDITS)
            submit_button.click()
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.wait_for_loader_to_disappear(self.LOADER_C)

            # Apply Avianca credits
            apply_avianca_credits = self.wait_for_visibility_of_element_located(self.APPLY_AVIANCA_CREDITS)
            apply_avianca_credits.click()
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.wait_for_loader_to_disappear(self.LOADER_C)      


            
        except Exception as e:
            self.logger.error(f"Error filling Avianca credits: {str(e)}")
            raise

    @catch_exceptions()
    def fill_cardholder_name(self, name: str):
        """
        Fills the card holder name field in the payment form.

        This method waits for the loader to disappear, switches to the iframe containing the
        card input field, scrolls the card holder name field into view, and fills it using
        JavaScript. Logs all significant steps, and raises an exception if an error occurs.

        Args:
            name (str): The name of the cardholder to be entered into the input field.

        Raises:
            Exception: If there is an error during any of the operations.
        """

        try:
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.logger.info("Filling out card holder name field...")      
            

            #  Wait for the iframe to load
            self.logger.info("Switching to iframe containing the card input field...")
            iframe = self.wait_for((By.XPATH, "//iframe[contains(@src, 'htmlprovider/gethtml')]"))
            self.driver.switch_to.frame(iframe)

            # We are inside the iframe
            field = self.find(self.CARD_HOLDER_NAME_INPUT)
            field.location_once_scrolled_into_view

            self.logger.info("Scrolling into view using JavaScript...")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", field)

            self.logger.info("Filling field using JavaScript...")
            self.driver.execute_script("arguments[0].value = '';", field)  # Limpiar
            self.driver.execute_script("arguments[0].value = arguments[1];", field, name)

            self.logger.info("Card holder name field filled using JavaScript.")

            # # Switch back to the main page
            # self.driver.switch_to.default_content()

        except Exception as e:
            self.logger.error(f"Error filling out cardholder name field: {str(e)}")
            raise

    @catch_exceptions()
    def fill_card_number(self, number: str):
          
        """
        Fills out the card number field with the given number.

        Args:
            number (str): The card number to be entered into the input field.

        Raises:
            Exception: If there is an error during any of the operations.
        """

        try:         
            self.scroll_down_move_to_element(self.find(self.CARD_NUMBER_INPUT))
            self.logger.info("Filling out card number field...")
            field = self.wait_to_be_clickable(self.CARD_NUMBER_INPUT)
            self.logger.info("Clearing out card number field...")
            self.scroll_down_to_element(field)
            field.clear()
            self.logger.info("Writting card number...")
            field.send_keys(number)
            self.logger.info("Card number field filled...")
        except Exception as e:
            self.logger.error(f"Error filling out card number field: {str(e)}")
            raise

    @catch_exceptions()
    def select_expiration_month(self, month: str):
        """
        Selects the expiration month from a custom dropdown.
        Args:
            month (str): The expiration month to select (e.g., '3').
        """
        try:
            self.logger.info("Selecting expiration month...")

            # 1. Open the dropdown
            dropdown_button = self.wait_to_be_clickable((By.ID, "expirationMonth_ExpirationDate"))
            self.scroll_down_to_element(dropdown_button)
            dropdown_button.click()

            # 2. Wait for the options to load
            month_option_xpath = f"//ul[@id='listId_expirationMonth_ExpirationDate']//span[text()='{month}']"
            option = self.wait_to_be_clickable((By.XPATH, month_option_xpath))

            # 3. Click on the option
            option.click()
            self.logger.info(f"Expiration month '{month}' selected.")
        except Exception as e:
            self.logger.error(f"Error selecting expiration month: {str(e)}")
            raise

    @catch_exceptions()
    def select_expiration_year(self, year: str):
        
        """
        Selects the expiration year from a custom dropdown.

        Args:
            year (str): The expiration year to select (e.g., '22').

        Raises:
            ValueError: If the year is not a two-digit number.
        """
        try:
            self.logger.info("Selecting expiration year...")

            if not year.isdigit() or len(year) != 2:
                raise ValueError("Year must be a two-digit number.")

            # 1. Open the dropdown
            dropdown_button = self.wait_to_be_clickable((By.ID, "expirationYear_ExpirationDate"))
            self.scroll_down_to_element(dropdown_button)
            dropdown_button.click()

            # 2. Wait for the options to be clickable
            self.logger.info("Waiting for option...")
            year_option_xpath = (
            f"//*[@id='expirationYear_ExpirationDate-{year}']")
            self.logger.debug(f"Using XPath: {year_option_xpath}")
            # option = self.find((By.XPATH, year_option_xpath))

            # 3. Wait for the option to be visible
            self.wait_for_visibility_of_element_located((By.XPATH, year_option_xpath))
            option = self.find((By.XPATH, year_option_xpath))

            # 4. Scroll into view and click via JavaScript for robustness
            self.logger.info("Scrolling into view and clicking using JavaScript...")
            # self.driver.execute_script("arguments[0].scrollIntoView(true);", option)
            self.driver.execute_script("arguments[0].click();", option)

            self.logger.info(f"Expiration year '{year}' selected.")
        except Exception as e:
            self.logger.error(f"Error selecting expiration year: {str(e)}")
            raise

    @catch_exceptions()
    def fill_cvv(self, cvv: str):
        """
        Fills the CVV field with the given value.
        Args:
            cvv (str): The CVV number to enter.
        """
        try:
            self.logger.info("Filling out CVV field...")
            field = self.wait_to_be_clickable(self.CVV_INPUT)
            self.scroll_down_to_element(field)
            field.clear()
            field.send_keys(cvv)
            self.logger.info("CVV field filled...")

            self.logger.info("Switching back to main page..")
            # Switch back to the main page
            self.driver.switch_to.default_content()
        except Exception as e:
            self.logger.error(f"Error filling out CVV field: {str(e)}")
            raise
      
    @catch_exceptions()
    def fill_email(self, email: str):        
        """
        Fills in the email input field.
        Args:
            email (str): The email address to input.
        """
        try:
            self.logger.info("Filling in email...")
            email_input = self.find(self.EMAIL_INPUT)
            self.scroll_down_to_element(email_input)
            email_input.clear()
            email_input.send_keys(email)
            self.logger.info("Email filled.")
        except Exception as e:
            self.logger.error(f"Error filling email: {str(e)}")
            raise

    @catch_exceptions()
    def fill_address(self, address: str):
        """
        Fills in the address input field.
        Args:
            address (str): The address to input.
        """
        try:
            self.logger.info("Filling in address...")
            address_input = self.find(self.ADDRESS_INPUT)
            self.scroll_down_to_element(address_input)
            address_input.clear()
            address_input.send_keys(address)
            self.logger.info("Address filled.")
        except Exception as e:
            self.logger.error(f"Error filling address: {str(e)}")
            raise

    @catch_exceptions()
    def fill_city(self, city: str):
        """
        Fills in the city input field.
        Args:
            city (str): The city name to input.
        """
        try:
            self.logger.info("Filling in city...")
            city_input = self.find(self.CITY_INPUT)
            city_input.clear()
            city_input.send_keys(city)
            self.logger.info("City filled.")
        except Exception as e:
            self.logger.error(f"Error filling city: {str(e)}")
            raise

    @catch_exceptions()
    def select_country(self, country_name: str):
        """
        Selects a country from the custom dropdown.
        Args:
            country_name (str): The visible name of the country to select (e.g., "Colombia").
        """
        try:
            self.logger.info(f"Selecting country: {country_name}...")
            
            # 1. Click on the dropdown button
            dropdown_button = self.wait_to_be_clickable((By.XPATH, "//button[@id='country']"))
            dropdown_button.click()
            self.scroll_down_to_element(dropdown_button)
            # 2. Wait for the options to load
            option_xpath = f"//span[normalize-space(text())='{country_name}']"
            country_option = self.wait_to_be_clickable((By.XPATH, option_xpath))
            # 3. Click on the option
            country_option.click()
            self.logger.info(f"Country '{country_name}' selected.")
        except Exception as e:
            self.logger.error(f"Error selecting country '{country_name}': {str(e)}")
            raise
    
    @catch_exceptions()
    def accept_terms_and_conditions(self):
        """
        Clicks on the checkbox to accept terms and conditions.
        """
        try:
            self.logger.info("Clicking on the terms and conditions checkbox...")
            checkbox = self.wait_to_be_clickable((By.XPATH, "//input[@id='terms' and @type='checkbox']"))
            self.scroll_down_to_element(checkbox)
            if not checkbox.is_selected():
                checkbox.click()
            self.logger.info("Terms and conditions accepted.")
        except Exception as e:
            self.logger.error(f"Error clicking on terms and conditions checkbox: {str(e)}")
            raise

    @catch_exceptions()        
    def click_continue(self):
        """
            Clicks the "Continuar" button.

            This method waits until the button is clickable, then clicks on it.
            If the button is not found or clickable within the timeout period, a TimeoutException is raised.

            Raises:
                Exception: If the button is not found or clickable within the timeout period.
            """
        try:
            self.logger.info("Clicking continue button...")
            button = self.wait_to_be_clickable(self.CONTINUE_BUTTON)
            self.scroll_down_to_element(button)
            button.click()
            self.logger.info("Continue button clicked...")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to click continue button") from e

    @catch_exceptions()  
    def scroll_to_element(self, pixels: int = 200):
        """
        Hace scroll hacia el elemento ubicado por el locator.
        :param driver: instancia de WebDriver
        :param locator: tupla (By, valor)
        """
        # element = self.find(self.PANEL_PAGO)
        # element.click()
        self.scroll_down_by_pixels(pixels)

    def loader(self):
            """
            Waits for the page loader to disappear.

            This method waits until the page loader disappears. If the loader does not
            disappear within the timeout period, a TimeoutException is raised.

            """
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.wait_for_loader_to_disappear(self.LOADER_C)

    @catch_exceptions()  
    def handle_modal_and_navigate(self):
        
        """
        Handles the modal that appears when the payment is rejected and navigates to the
        itinerary page.

        If the modal is detected, the method waits for the modal to appear, goes back to the
        previous page, waits for the page to finish loading, and then navigates to the
        itinerary page.

        If the modal is not detected, the method simply continues with the normal flow.

        :return: None
        """
        try:
            self.wait_for_visibility_of_element_located(self.BUTTON_MODAL_PAYMENT_REJECTED)
            
            print("Modal detected → going back...")

            self.driver.back()

            # Wait for the page to finish loading
            self._wait.until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            # Navigate to the itinerary page
            self.driver.get(f"{self.URL}booking/itinerary")

        except TimeoutException:
            print("Modal NO detectado → continuando con el flujo normal...")
