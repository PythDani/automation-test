


import time
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
    CONTINUE_BUTTON:             tuple = (By.XPATH, "//button[contains(@class,'ds-button ds-btn-action ds-btn-medium')]//span[contains(text(),'Confirmar y pagar')]")
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
            self.logger.info("Starting Avianca credits selection...")
            self.logger.info(f"Received parameters - number: '{number}' (type: {type(number)}), pin: '{pin}' (type: {type(pin)})")
            self.logger.info(f"PIN value details - length: {len(pin)}, isdigit: {pin.isdigit()}, repr: {repr(pin)}")
            
            # Ensure PIN is properly formatted as string and contains only digits
            pin = str(pin).strip()
            if not pin.isdigit():
                raise ValueError(f"PIN must contain only digits, got: '{pin}'")
            if len(pin) != 6:
                raise ValueError(f"PIN must be exactly 6 digits, got: '{pin}' (length: {len(pin)})")
            
            self.logger.info(f"Processed PIN: '{pin}' (length: {len(pin)})")
            self.wait_for_loader_to_disappear(self.LOADER_C)
            
            # Click on the checkbox
            self.logger.info("Looking for Avianca credits checkbox...")
            check_avianca_credits = self.find(self.CHECK_AVIANCA_CREDITS)
            if check_avianca_credits is None:
                raise Exception("Checkbox not found")
            check_avianca_credits.click()
            self.logger.info("Avianca credits checkbox clicked.")

            # Fill number
            self.logger.info("Looking for Avianca credits number input...")
            input_number = self.find(self.INPUT_NUMBER_AVIANCA_CREDITS)
            if input_number is None:
                raise Exception("Number input not found")
            input_number.clear()
            input_number.send_keys(number)
            self.logger.info("Avianca credits number filled.")

            # Fill PIN - Multiple strategies
            self.logger.info("Looking for Avianca credits PIN input...")
            input_pin = None
            
            # Strategy 1: Try the current locator
            try:
                self.logger.info("Trying PIN locator: //input[contains(@id,'pin')]")
                input_pin = self.wait_for_visibility_of_element_located(self.INPUT_PIN_AVIANCA_CREDITS)
                self.logger.info("PIN input found with current locator.")
            except Exception as e:
                self.logger.warning(f"Current PIN locator failed: {e}")
                
                # Strategy 2: Try alternative locators
                alternative_pin_locators = [
                    (By.ID, "pin"),
                    (By.XPATH, "//input[@id='pin']"),
                    (By.XPATH, "//input[@name='pin']"),
                    (By.XPATH, "//input[contains(@name,'pin')]"),
                    (By.XPATH, "//input[contains(@placeholder,'PIN')]"),
                    (By.XPATH, "//input[contains(@placeholder,'pin')]"),
                    (By.XPATH, "//input[@type='text' and contains(@class,'ds-input')]"),
                    (By.XPATH, "//input[@type='password']"),
                    (By.XPATH, "//input[@type='text' and @maxlength='6']")
                ]
                
                for i, locator in enumerate(alternative_pin_locators):
                    try:
                        self.logger.info(f"Trying alternative PIN locator {i+1}: {locator}")
                        input_pin = self.wait_for_visibility_of_element_located(locator)
                        self.logger.info(f"PIN input found with alternative locator {i+1}.")
                        break
                    except Exception as alt_e:
                        self.logger.warning(f"Alternative PIN locator {i+1} failed: {alt_e}")
                        continue
            
            if input_pin is None:
                raise Exception("Could not find PIN input field with any locator strategy")
            
            # Ensure element is interactable before filling
            self.logger.info("Ensuring PIN input is interactable...")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", input_pin)
            time.sleep(0.5)
            
            # Check element properties before interacting
            self.logger.info(f"PIN element is_displayed: {input_pin.is_displayed()}")
            self.logger.info(f"PIN element is_enabled: {input_pin.is_enabled()}")
            self.logger.info(f"PIN element tag_name: {input_pin.tag_name}")
            self.logger.info(f"PIN element type: {input_pin.get_attribute('type')}")
            self.logger.info(f"PIN element id: {input_pin.get_attribute('id')}")
            self.logger.info(f"PIN element name: {input_pin.get_attribute('name')}")
            
            # Clear and fill PIN field with special handling for security fields
            try:
                self.logger.info("Attempting to clear PIN field...")
                input_pin.clear()
                self.logger.info("PIN field cleared successfully.")
            except Exception as clear_e:
                self.logger.warning(f"Clear failed: {clear_e}, trying JavaScript clear...")
                self.driver.execute_script("arguments[0].value = '';", input_pin)
                self.logger.info("PIN field cleared with JavaScript.")
            
            # PIN field requires manual typing (no paste allowed) - send keys one by one
            self.logger.info(f"Filling PIN field manually (character by character): {pin}")
            try:
                # Focus the element first
                input_pin.click()
                time.sleep(0.2)
                
                # Send each character individually with small delays
                for char in pin:
                    input_pin.send_keys(char)
                    time.sleep(0.1)  # Small delay between characters
                
                self.logger.info(f"PIN filled successfully with manual typing: {pin}")
                
                # Verify the value was entered correctly
                entered_value = input_pin.get_attribute('value')
                self.logger.info(f"PIN field value after typing: '{entered_value}'")
                
                if entered_value != pin:
                    self.logger.warning(f"PIN value mismatch! Expected: '{pin}', Got: '{entered_value}'")
                    # Try to clear and retry
                    input_pin.clear()
                    time.sleep(0.2)
                    for char in pin:
                        input_pin.send_keys(char)
                        time.sleep(0.1)
                    self.logger.info("PIN retry completed.")
                
            except Exception as send_e:
                self.logger.warning(f"Manual typing failed: {send_e}, trying JavaScript with events...")
                try:
                    # JavaScript approach with proper events for security fields
                    self.driver.execute_script("""
                        var input = arguments[0];
                        var value = arguments[1];
                        input.focus();
                        input.value = '';
                        input.value = value;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                        input.dispatchEvent(new Event('blur', { bubbles: true }));
                    """, input_pin, pin)
                    self.logger.info(f"PIN filled with JavaScript and events: {pin}")
                except Exception as js_e:
                    self.logger.error(f"JavaScript approach also failed: {js_e}")
                    raise Exception(f"All PIN filling methods failed: {send_e}, {js_e}")

            self.logger.info("Avianca credits form filled successfully.")

            # Submit button - Multiple strategies
            self.logger.info("Looking for submit button...")
            submit_button = None
            
            # Strategy 1: Try the original locator
            try:
                self.logger.info("Trying submit button locator: //*[contains(@id,'buttonAviancaCredits')]")
                submit_button = self.find(self.BUTTON_ENTER_AVIANCA_CREDITS)
                if submit_button is None:
                    raise Exception("Submit button not found with original locator")
                self.logger.info("Submit button found with original locator.")
            except Exception as e:
                self.logger.warning(f"Original submit button locator failed: {e}")
                
                # Strategy 2: Try alternative locators
                alternative_submit_locators = [
                    (By.XPATH, "//button[contains(@id,'buttonAviancaCredits')]"),
                    (By.XPATH, "//*[contains(@class,'button') and contains(@id,'buttonAviancaCredits')]"),
                    (By.XPATH, "//button[contains(text(),'Ingresar')]"),
                    (By.XPATH, "//button[contains(text(),'Continuar')]"),
                    (By.XPATH, "//button[contains(text(),'Aplicar')]"),
                    (By.XPATH, "//button[contains(@class,'btn-primary')]"),
                    (By.XPATH, "//button[contains(@class,'ds-button')]")
                ]
                
                for i, locator in enumerate(alternative_submit_locators):
                    try:
                        self.logger.info(f"Trying alternative submit locator {i+1}: {locator}")
                        submit_button = self.find(locator)
                        if submit_button is not None:
                            self.logger.info(f"Submit button found with alternative locator {i+1}.")
                            break
                    except Exception as alt_e:
                        self.logger.warning(f"Alternative submit locator {i+1} failed: {alt_e}")
                        continue
            
            if submit_button is None:
                raise Exception("Could not find submit button with any locator strategy")
            
            # Try different click strategies
            try:
                submit_button.click()
                self.logger.info("Submit button clicked with direct click.")
            except Exception as click_e:
                self.logger.warning(f"Direct click failed: {click_e}, trying JavaScript click...")
                try:
                    self.driver.execute_script("arguments[0].click();", submit_button)
                    self.logger.info("Submit button clicked with JavaScript click.")
                except Exception as js_e:
                    self.logger.error(f"JavaScript click also failed: {js_e}")
                    raise Exception(f"Both direct and JavaScript clicks failed: {click_e}, {js_e}")
            
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.wait_for_loader_to_disappear(self.LOADER_C)

            # Apply Avianca credits - Multiple strategies
            self.logger.info("Looking for apply Avianca credits button...")
            apply_avianca_credits = None
            
            # Strategy 1: Try the original locator
            try:
                self.logger.info("Trying apply button locator: //*[contains(@class,'ds-button ds-btn-primary ds-btn-small')]")
                apply_avianca_credits = self.wait_for_visibility_of_element_located(self.APPLY_AVIANCA_CREDITS)
                self.logger.info("Apply button found with original locator.")
            except Exception as e:
                self.logger.warning(f"Original apply button locator failed: {e}")
                
                # Strategy 2: Try alternative locators
                alternative_apply_locators = [
                    (By.XPATH, "//button[contains(@class,'ds-button ds-btn-primary ds-btn-small')]"),
                    (By.XPATH, "//*[contains(@class,'ds-btn-primary') and contains(@class,'ds-btn-small')]"),
                    (By.XPATH, "//button[contains(@class,'ds-btn-primary')]"),
                    (By.XPATH, "//button[contains(text(),'Aplicar')]"),
                    (By.XPATH, "//button[contains(text(),'Apply')]"),
                    (By.XPATH, "//button[contains(text(),'Continuar')]"),
                    (By.XPATH, "//button[contains(text(),'Continue')]"),
                    (By.XPATH, "//button[contains(@class,'btn-primary')]"),
                    (By.XPATH, "//button[contains(@class,'ds-button')]")
                ]
                
                for i, locator in enumerate(alternative_apply_locators):
                    try:
                        self.logger.info(f"Trying alternative apply locator {i+1}: {locator}")
                        apply_avianca_credits = self.wait_for_visibility_of_element_located(locator)
                        self.logger.info(f"Apply button found with alternative locator {i+1}.")
                        break
                    except Exception as alt_e:
                        self.logger.warning(f"Alternative apply locator {i+1} failed: {alt_e}")
                        continue
            
            if apply_avianca_credits is None:
                raise Exception("Could not find apply Avianca credits button with any locator strategy")
            
            # Try different click strategies
            try:
                apply_avianca_credits.click()
                self.logger.info("Apply Avianca credits button clicked with direct click.")
            except Exception as click_e:
                self.logger.warning(f"Direct click failed: {click_e}, trying JavaScript click...")
                try:
                    self.driver.execute_script("arguments[0].click();", apply_avianca_credits)
                    self.logger.info("Apply Avianca credits button clicked with JavaScript click.")
                except Exception as js_e:
                    self.logger.error(f"JavaScript click also failed: {js_e}")
                    raise Exception(f"Both direct and JavaScript clicks failed: {click_e}, {js_e}")
            
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.wait_for_loader_to_disappear(self.LOADER_C)
            
            self.logger.info("Avianca credits selection completed successfully.")

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
            
            # Wait for any loaders to disappear first
            self.logger.info("Waiting for loaders to disappear...")
            try:
                self.wait_for_invisibility(self.LOADER_C)
                self.logger.info("Loaders disappeared.")
            except:
                self.logger.warning("Loader wait timed out, continuing...")
            
            # Additional wait to ensure page is stable
            time.sleep(2)
            
            # Try to find the button using find_elements (not wait_to_be_clickable)
            continue_button = None
            
            # Diagnose the DOM first
            self.logger.info("Diagnosing DOM for payment continue button...")
            try:
                all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                self.logger.info(f"Found {len(all_buttons)} buttons on the page")
                
                ds_buttons = self.driver.find_elements(By.TAG_NAME, "ds-button")
                self.logger.info(f"Found {len(ds_buttons)} ds-button elements")
                
                # Look for any button with "Confirmar" or "pagar" text
                confirmar_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(),'Confirmar') or contains(text(),'pagar')]")
                self.logger.info(f"Found {len(confirmar_buttons)} buttons with 'Confirmar' or 'pagar' text")
                
                # Look for any span with "Confirmar y pagar" text
                confirmar_spans = self.driver.find_elements(By.XPATH, "//span[contains(text(),'Confirmar y pagar')]")
                self.logger.info(f"Found {len(confirmar_spans)} spans with 'Confirmar y pagar' text")
                
                # Look for any element with ds-btn-action class
                action_buttons = self.driver.find_elements(By.XPATH, "//*[contains(@class,'ds-btn-action')]")
                self.logger.info(f"Found {len(action_buttons)} elements with 'ds-btn-action' class")
                
                # Print some button texts for debugging
                for i, button in enumerate(all_buttons[:10]):  # First 10 buttons
                    try:
                        text = button.text.strip()
                        if text:
                            self.logger.info(f"Button {i+1} text: '{text}'")
                    except:
                        pass
                        
            except Exception as e:
                self.logger.warning(f"DOM diagnosis failed: {e}")

            # Try different locators to find the button
            locators_to_try = [
                self.CONTINUE_BUTTON,
                (By.XPATH, "//button[contains(@class,'ds-btn-action ds-btn-medium')]//span[text()='Confirmar y pagar']"),
                (By.XPATH, "//button//span[text()='Confirmar y pagar']"),
                (By.XPATH, "//ds-button//button[contains(@class,'ds-btn-action')]//span[text()='Confirmar y pagar']"),
                (By.XPATH, "//button[contains(@class,'ds-button') and contains(@class,'ds-btn-action')]"),
                (By.XPATH, "//button[contains(text(),'Confirmar y pagar')]"),
                (By.XPATH, "//span[contains(text(),'Confirmar y pagar')]/parent::button"),
                (By.XPATH, "//ds-button[contains(@class,'ds-button-container')]//button"),
                (By.XPATH, "//button[contains(@class,'ds-button')]//span[contains(text(),'Confirmar')]"),
                (By.XPATH, "//*[contains(@class,'ds-btn-action')]//span[contains(text(),'Confirmar')]")
            ]
            
            for i, locator in enumerate(locators_to_try):
                try:
                    buttons = self.driver.find_elements(*locator)
                    if buttons:
                        # Find the button that contains "Confirmar y pagar" text
                        for button in buttons:
                            try:
                                if "Confirmar y pagar" in button.text or "Confirmar y pagar" in button.get_attribute("innerHTML"):
                                    continue_button = button
                                    self.logger.info(f"Continue button found with locator strategy {i+1}")
                                    break
                            except:
                                continue
                        if continue_button:
                            break
                except Exception as e:
                    self.logger.warning(f"Locator strategy {i+1} failed: {e}")
                    continue
            
            if not continue_button:
                self.logger.error("Could not find continue button with any strategy")
                raise Exception("Could not find continue button with any strategy")
            
            # Make the button clickable if it's not
            try:
                # Scroll to the button
                self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
                time.sleep(0.5)
                
                # Try to make it clickable by removing any overlays
                self.driver.execute_script("""
                    var button = arguments[0];
                    var overlays = document.querySelectorAll('.modal-backdrop, .overlay, .loading');
                    overlays.forEach(function(overlay) {
                        overlay.style.display = 'none';
                    });
                    button.style.pointerEvents = 'auto';
                    button.style.zIndex = '9999';
                """, continue_button)
                
                self.logger.info("Button prepared for clicking")
                
            except Exception as e:
                self.logger.warning(f"Button preparation failed: {e}")

            self.logger.info("Continue button is clickable, attempting to click...")

            # Scroll to the button
            self.scroll_down_to_element(continue_button)
            time.sleep(0.5)  # Wait after scrolling

            # Try different click strategies
            try:
                continue_button.click()
                self.logger.info("Continue button clicked with direct click...")
            except Exception as e:
                self.logger.warning(f"Direct click failed: {e}, trying JavaScript click...")
                self.driver.execute_script("arguments[0].click();", continue_button)
                self.logger.info("Continue button clicked with JavaScript click...")
                
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
            self.driver.get(f"{self.URL}es/booking/itinerary")

        except TimeoutException:
            print("Modal NO detectado → continuando con el flujo normal...")
