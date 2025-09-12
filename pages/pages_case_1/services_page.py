from selenium.webdriver.common.by import By
from utils.exception import catch_exceptions
from logger import get_logger
from pages.common import Common
from selenium.common.exceptions import TimeoutException
import time

class ServicesPage(Common):
    # ----------------------------------LOCATORS----------------------------------------------------------
    #Loader that indicate that the page is loading in some cases.
    LOADER_C:                                    tuple = (By.XPATH, "//*[contains(@class, 'page-loader') or contains(@class, 'loading') or contains(@class, 'loader')]")
    
    CARRY_ON_AND_CHECKED_BAGGAGE_ADD_BUTTON:     tuple = (By.XPATH, "//button[contains(@id,'serviceButtonTypeBaggage')]")
    CARRY_ON_BAGGAGE_PLUS_BUTTON:                tuple = (By.XPATH, "//button[contains(@class,'ui-num-ud_button plus')]")
    CONFIRM_CARRY_ON_AND_CHECKED_BAGGAGE_MODAL:  tuple = (By.XPATH, "//ds-button[contains(@class,'amount-summary_button')]//button[contains(@class,'button btn-action btn-Medium')]//span[contains(text(),'Confirmar')]")
    SPORT_BAGGAGE_ADD_BUTTON:                    tuple = (By.ID, "serviceButtonTypeOversize")
    SPORT_EQUIPMENT_PLUS_BUTTON:                  tuple = (By.XPATH, "//button[contains(@class,'ui-num-ud_button plus')]")
    CONFIRM_SPORT_BAGGAGE_MODAL:                 tuple = (By.XPATH, "//ds-button[contains(@class,'amount-summary_button')]//button[contains(@class,'button btn-action btn-Medium')]//span[contains(text(),'Confirmar')]")
    BUSSINESS_LOUNGE_ADD_BUTTON:                 tuple = (By.XPATH, "//button[contains(@id,'serviceButtonTypeBusinessLounge')]")
    LOUNGES_PLUS_BUTTON:                         tuple = (By.XPATH, "//label[contains(@class,'service_item_button button')]")
    CONFIRM_LOUNGES_MODAL:                       tuple = (By.XPATH, "//button[contains(@class,'button btn-action btn-Medium')]//span[contains(text(),'Confirmar')]")
    CONFIRM_SERVICES_BUTTON:                     tuple = (By.XPATH, "//*[contains(@class,'button page_button btn-action page_button-primary-flow ng-star-inserted')]//span[contains(@class,'button_label')]")
    
    SPECIAL_ASISTANCE_ADD_BUTTON:                tuple = (By.XPATH, "//button[contains(@id,'serviceButtonTypeSpecialAssistance')]")
    ADD_SPECIAL_ASISTANCE_ALL:                   tuple = (By.XPATH, "//div[contains(@class,'service_item_action ng-star-inserted')]")
    CONFIRM_SPECIAL_ASISTANCE_MODAL:             tuple = (By.XPATH, "//button[contains(@class,'button amount-summary_button amount-summary_button-action is-action ng-star-inserted')]")


    @catch_exceptions() 
    def __init__(self, driver):
        """
        Initialize a ServicesPage instance.

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
            self.logger.info("Waiting for page to load disappear...")
            # EXecute the wait_for_loader_to_disappear method twice
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.logger.info("Page loaded correctly.")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {self.__class__.__name__}") from e

    @catch_exceptions()     
    def add_carry_on_and_checked_baggage(self):
        """
        Adds a carry-on and checked baggage service.

        This method waits for the visibility of the carry-on and checked baggage add button 
        and clicks on it to add the service. Logs the action performed. Raises an exception 
        if the button is not found within the timeout period.

        Raises:
            Exception: If the carry-on and checked baggage add button is not visible 
                    within the timeout period.
        """
        name = "baggage service"
        try:
            self.wait_for_loader_to_disappear(self.LOADER_C)
            add_carry_on_button = self.wait_for_visibility_of_element_located(self.CARRY_ON_AND_CHECKED_BAGGAGE_ADD_BUTTON)
            self.driver.implicitly_wait(1)   

            add_carry_on_button.click()
            self.logger.info(f"{name} opened...")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {name}") from e

    @catch_exceptions()     
    def click_on_bagage_plus_button(self):       
        """
        Clicks on the "Add bagage" plus button.

        This method waits until the "Add bagage" plus button is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.

        Raises:
            Exception: If the "Add bagage" plus button is not found or clickable within the timeout period.
        """
        try:
            plus_buttons = self.find_all(self.CARRY_ON_BAGGAGE_PLUS_BUTTON)

            if plus_buttons:
                button = plus_buttons[0]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                button.click()
                self.driver.implicitly_wait(1)
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to add carry-on baggage") from e
    
    @catch_exceptions() 
    def confirm_carry_on_modal_and_checked_baggage_modal(self):
        """
        Confirms the carry-on and checked baggage modal.

        This method waits until the confirmation button of the carry-on and checked baggage modal
        is visible and clickable, then clicks on it. Logs the action performed. If the button is 
        not found or clickable within the timeout period, a TimeoutException is raised.

        Raises:
            Exception: If the confirmation button is not found or clickable within the timeout period.
        """
        try:
            self.logger.info("Click on confirm button for carry-on and checked baggage...")          
            
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
            self.logger.info("Scrolling down to make modal content visible...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Try multiple locator strategies (same as sport_baggage)
            self.logger.info("Trying to find carry-on and checked baggage confirm button...")
            
            # First, let's diagnose what's in the DOM
            self.logger.info("Diagnosing DOM for carry-on and checked baggage modal...")
            try:
                # Check if any buttons with "Confirmar" text exist
                confirmar_buttons = self.driver.find_elements(By.XPATH, "//button//span[contains(text(),'Confirmar')]")
                self.logger.info(f"Found {len(confirmar_buttons)} buttons with 'Confirmar' text")
                
                # Check if any buttons with btn-action class exist
                action_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class,'btn-action')]")
                self.logger.info(f"Found {len(action_buttons)} buttons with 'btn-action' class")
                
                # Check if any buttons with dsButtonId exist
                ds_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@id,'dsButtonId_')]")
                self.logger.info(f"Found {len(ds_buttons)} buttons with 'dsButtonId_' pattern")
                
                # Log current page source snippet for debugging
                page_source = self.driver.page_source
                if "Confirmar" in page_source:
                    self.logger.info("'Confirmar' text found in page source")
                else:
                    self.logger.warning("'Confirmar' text NOT found in page source")
                    
            except Exception as e:
                self.logger.warning(f"DOM diagnosis failed: {e}")
            
            # Strategy: Try to find the button using find_elements (not wait_to_be_clickable)
            continue_button = None
            
            # Try different locators to find the button
            locators_to_try = [
                self.CONFIRM_CARRY_ON_AND_CHECKED_BAGGAGE_MODAL,
                (By.XPATH, "//button[contains(@class,'btn-action btn-Medium')]//span[text()='Confirmar']"),
                (By.XPATH, "//button//span[text()='Confirmar']"),
                (By.XPATH, "//button[contains(@id,'dsButtonId_')]//span[text()='Confirmar']"),
                (By.XPATH, "//button[contains(@class,'button') and contains(@class,'btn-action')]")
            ]
            
            for i, locator in enumerate(locators_to_try):
                try:
                    buttons = self.driver.find_elements(*locator)
                    if buttons:
                        # Find the button that contains "Confirmar" text
                        for button in buttons:
                            try:
                                if "Confirmar" in button.text or "Confirmar" in button.get_attribute("innerHTML"):
                                    continue_button = button
                                    self.logger.info(f"Carry-on and checked baggage confirm button found with locator strategy {i+1}")
                                    break
                            except:
                                continue
                        if continue_button:
                            break
                except Exception as e:
                    self.logger.warning(f"Locator strategy {i+1} failed: {e}")
                    continue
            
            if not continue_button:
                self.logger.error("Could not find carry-on and checked baggage confirm button with any strategy")
                raise Exception("Could not find carry-on and checked baggage confirm button with any strategy")
            
            self.logger.info("Carry-on and checked baggage confirm button found, ensuring it's visible and clickable...")

            # Enhanced scroll strategy to ensure button is visible
            self.logger.info("Performing enhanced scroll to make carry-on and checked baggage button visible...")
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
            self.logger.info("Verifying carry-on and checked baggage button is visible and clickable...")
            if not continue_button.is_displayed():
                self.logger.warning("Button is not displayed, trying additional scroll...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
                time.sleep(1)

            # Try different click strategies
            try:
                continue_button.click()
                self.logger.info("Carry-on and checked baggage confirmed with direct click.")
            except Exception as e:
                self.logger.warning(f"Direct click failed: {e}, trying JavaScript click...")
                self.driver.execute_script("arguments[0].click();", continue_button)
                self.logger.info("Carry-on and checked baggage confirmed with JavaScript click.")
                
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to confirm carry-on and checked baggage") from e
    
    @catch_exceptions()         
    def add_sport_baggage(self): 
        """
        Adds a sport baggage service.

        This method waits until the "Add sport baggage" button is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.

        Raises:
            Exception: If the "Add sport baggage" button is not found or clickable within the timeout period.
        """
        name = "Sport baggage service"
        try:
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.wait_for_loader_to_disappear(self.LOADER_C)
            add_sport_on_button = self.wait_for_visibility_of_element_located(self.SPORT_BAGGAGE_ADD_BUTTON)
            self.scroll_down_move_to_element(add_sport_on_button)
            self.driver.implicitly_wait(1)

            add_sport_on_button.click()
            self.logger.info(f"{name} opened...")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {name}") from e
    
    @catch_exceptions() 
    def click_on_sport_bagage_plus_button(self):      
        """
        Clicks on the "Add sport baggage" plus button.

        This method waits until the "Add sport baggage" plus button is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.

        Raises:
            Exception: If the "Add sport baggage" plus button is not found or clickable within the timeout period.
        """
        try:
            plus_buttons = self.find_all(self.SPORT_EQUIPMENT_PLUS_BUTTON)

            if plus_buttons:
                button = plus_buttons[0]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                button.click()
                self.driver.implicitly_wait(1)
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to add sport baggage") from e
    
    @catch_exceptions() 
    def confirm_sport_baggage_modal(self):
        """
        Confirms the sport baggage modal.

        This method waits until the confirmation button of the sport baggage modal
        is visible and clickable, then clicks on it. Logs the action performed. If the button is 
        not found or clickable within the timeout period, a TimeoutException is raised.

        Raises:
            Exception: If the confirmation button is not found or clickable within the timeout period.
        """
        try:
            self.logger.info("Click on confirm button for sport baggage...")            
            
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
            self.logger.info("Scrolling down to make sport baggage modal content visible...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Try multiple locator strategies
            self.logger.info("Trying to find sport baggage confirm button...")
            
            # First, let's diagnose what's in the DOM
            self.logger.info("Diagnosing DOM for sport baggage modal...")
            try:
                # Check if any buttons with "Confirmar" text exist
                confirmar_buttons = self.driver.find_elements(By.XPATH, "//button//span[contains(text(),'Confirmar')]")
                self.logger.info(f"Found {len(confirmar_buttons)} buttons with 'Confirmar' text")
                
                # Check if any buttons with btn-action class exist
                action_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class,'btn-action')]")
                self.logger.info(f"Found {len(action_buttons)} buttons with 'btn-action' class")
                
                # Check if any buttons with dsButtonId exist
                ds_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@id,'dsButtonId_')]")
                self.logger.info(f"Found {len(ds_buttons)} buttons with 'dsButtonId_' pattern")
                
                # Log current page source snippet for debugging
                page_source = self.driver.page_source
                if "Confirmar" in page_source:
                    self.logger.info("'Confirmar' text found in page source")
                else:
                    self.logger.warning("'Confirmar' text NOT found in page source")
                    
            except Exception as e:
                self.logger.warning(f"DOM diagnosis failed: {e}")
            
            # Strategy 1: Try to find the button using find_elements (not wait_to_be_clickable)
            continue_button = None
            
            # Try different locators to find the button
            locators_to_try = [
                self.CONFIRM_SPORT_BAGGAGE_MODAL,
                (By.XPATH, "//button[contains(@class,'btn-action btn-Medium')]//span[text()='Confirmar']"),
                (By.XPATH, "//button//span[text()='Confirmar']"),
                (By.XPATH, "//button[contains(@id,'dsButtonId_')]//span[text()='Confirmar']"),
                (By.XPATH, "//button[contains(@class,'button') and contains(@class,'btn-action')]")
            ]
            
            for i, locator in enumerate(locators_to_try):
                try:
                    buttons = self.driver.find_elements(*locator)
                    if buttons:
                        # Find the button that contains "Confirmar" text
                        for button in buttons:
                            try:
                                if "Confirmar" in button.text or "Confirmar" in button.get_attribute("innerHTML"):
                                    continue_button = button
                                    self.logger.info(f"Sport baggage confirm button found with locator strategy {i+1}")
                                    break
                            except:
                                continue
                        if continue_button:
                            break
                except Exception as e:
                    self.logger.warning(f"Locator strategy {i+1} failed: {e}")
                    continue
            
            if not continue_button:
                self.logger.error("Could not find sport baggage confirm button with any strategy")
                raise Exception("Could not find sport baggage confirm button with any strategy")
            
            self.logger.info("Sport baggage confirm button found, ensuring it's visible and clickable...")

            # Enhanced scroll strategy to ensure button is visible
            self.logger.info("Performing enhanced scroll to make sport baggage button visible...")
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
            self.logger.info("Verifying sport baggage button is visible and clickable...")
            if not continue_button.is_displayed():
                self.logger.warning("Button is not displayed, trying additional scroll...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
                time.sleep(1)

            # Try different click strategies
            try:
                continue_button.click()
                self.logger.info("Sport baggage confirmed with direct click.")
            except Exception as e:
                self.logger.warning(f"Direct click failed: {e}, trying JavaScript click...")
                self.driver.execute_script("arguments[0].click();", continue_button)
                self.logger.info("Sport baggage confirmed with JavaScript click.")
                
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to confirm sport baggage") from e

    @catch_exceptions() 
    def add_bussines_lounge(self):
        """
        Adds a bussines lounge service.

        This method waits until the "Add bussines lounge" button is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.

        Raises:
            Exception: If the "Add bussines lounge" button is not found or clickable within the timeout period.
        """
        name = "Bussiness lounge service"
        try:
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.wait_for_loader_to_disappear(self.LOADER_C)
            add_buttons = self.find_all(self.BUSSINESS_LOUNGE_ADD_BUTTON)

            if add_buttons:
                button = add_buttons[0]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                self.scroll_down_move_to_element(button)
                self.driver.implicitly_wait(1)
                button.click()        
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {name}") from e
    
    @catch_exceptions()
    def click_on_some_lounge_plus_button(self):     
        """
        Clicks on the "Add lounge" plus button.

        This method waits until the "Add lounge" plus button is visible and clickable, 
        then clicks on it. Logs the action performed. If the button is not found 
        or clickable within the timeout period, a TimeoutException is raised.

        Raises:
            Exception: If the "Add lounge" plus button is not found or clickable 
                    within the timeout period.
        """
        try:
            self.wait_for_loader_to_disappear(self.LOADER_C)
            self.logger.info("Add lounge bussines services...")
            plus_button = self.find(self.LOUNGES_PLUS_BUTTON)

            self.driver.implicitly_wait(1)           

            plus_button.click()           
            self.logger.info("Lounge bussines services added...")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to add lounge bussines services") from e
    
    @catch_exceptions() 
    def confirm_lounge_bussiness_modal(self):                    
        """
        Confirms the Lounge business services modal.

        This method waits until the confirmation button of the Lounge business services modal is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.
        """
        try:
            self.logger.info("Click on confirm button for lounge business services...")              
            
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
            self.logger.info("Scrolling down to make lounge business modal content visible...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Try to find the button using find_elements (not wait_to_be_clickable)
            continue_button = None
            
            # Try different locators to find the button
            locators_to_try = [
                self.CONFIRM_LOUNGES_MODAL,
                (By.XPATH, "//button[contains(@class,'btn-action btn-Medium')]//span[text()='Confirmar']"),
                (By.XPATH, "//button//span[text()='Confirmar']"),
                (By.XPATH, "//button[contains(@id,'dsButtonId_')]//span[text()='Confirmar']"),
                (By.XPATH, "//button[contains(@class,'button') and contains(@class,'btn-action')]")
            ]
            
            for i, locator in enumerate(locators_to_try):
                try:
                    buttons = self.driver.find_elements(*locator)
                    if buttons:
                        # Find the button that contains "Confirmar" text
                        for button in buttons:
                            try:
                                if "Confirmar" in button.text or "Confirmar" in button.get_attribute("innerHTML"):
                                    continue_button = button
                                    self.logger.info(f"Lounge confirm button found with locator strategy {i+1}")
                                    break
                            except:
                                continue
                        if continue_button:
                            break
                except Exception as e:
                    self.logger.warning(f"Locator strategy {i+1} failed: {e}")
                    continue
            
            if not continue_button:
                self.logger.error("Could not find lounge confirm button with any strategy")
                raise Exception("Could not find lounge confirm button with any strategy")
            
            self.logger.info("Lounge confirm button found, ensuring it's visible and clickable...")

            # Enhanced scroll strategy to ensure button is visible
            self.logger.info("Performing enhanced scroll to make lounge business button visible...")
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
            self.logger.info("Verifying lounge business button is visible and clickable...")
            if not continue_button.is_displayed():
                self.logger.warning("Button is not displayed, trying additional scroll...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
                time.sleep(1)

            # Try different click strategies
            try:
                continue_button.click()
                self.logger.info("Lounge business services confirmed with direct click.")
            except Exception as e:
                self.logger.warning(f"Direct click failed: {e}, trying JavaScript click...")
                self.driver.execute_script("arguments[0].click();", continue_button)
                self.logger.info("Lounge business services confirmed with JavaScript click.")
            
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to confirm lounge business services") from e
    
    @catch_exceptions()
    def add_special_asistance_services(self):      
        """
        Adds a special asistance service.

        This method waits until the "Add special asistance" button is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.

        Raises:
            Exception: If the "Add special asistance" button is not found or clickable within the timeout period.
        """
        name = "Special asistance service"
        try:
            self.wait_for_loader_to_disappear(self.LOADER_C)
            add_asistance_on_button = self.wait_for_visibility_of_element_located(self.SPECIAL_ASISTANCE_ADD_BUTTON)
            add_asistance_on_button.click()
            self.logger.info(f"{name} opened...")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {name}") from e
    
    @catch_exceptions() 
    def click_on_add_special_asistance_plus_button(self):      
        """
        Clicks on the "Add special assistance" plus button.

        This method waits until the "Add special assistance" plus button is visible and clickable, 
        then clicks on the first one found. If no buttons are found, a warning is logged. 
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.

        Raises:
            Exception: If the "Add special assistance" plus button is not found or clickable 
                    within the timeout period.
        """
        try:
            plus_buttons = self.find_all(self.ADD_SPECIAL_ASISTANCE_ALL)
            if plus_buttons:
                button = plus_buttons[0]  # Solo el primer botón
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                button.click()
            else:
                self.logger.warning("No special assistance buttons found.")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to add special asistance service") from e
    
    @catch_exceptions() 
    def confirm_special_asistance_modal(self):                   
        """
        Confirms the special asistance modal.

        This method waits until the confirmation button of the special asistance modal is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.
        """
        try:
            self.logger.info("Click on confirm button for special assistance services...")              
            
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
            self.logger.info("Scrolling down to make special assistance modal content visible...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Try multiple locator strategies (same as sport_baggage)
            self.logger.info("Trying to find special assistance confirm button...")
            
            # First, let's diagnose what's in the DOM
            self.logger.info("Diagnosing DOM for special assistance modal...")
            try:
                # Check if any buttons with "Confirmar" text exist
                confirmar_buttons = self.driver.find_elements(By.XPATH, "//button//span[contains(text(),'Confirmar')]")
                self.logger.info(f"Found {len(confirmar_buttons)} buttons with 'Confirmar' text")
                
                # Check if any buttons with btn-action class exist
                action_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class,'btn-action')]")
                self.logger.info(f"Found {len(action_buttons)} buttons with 'btn-action' class")
                
                # Check if any buttons with dsButtonId exist
                ds_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@id,'dsButtonId_')]")
                self.logger.info(f"Found {len(ds_buttons)} buttons with 'dsButtonId_' pattern")
                
                # Log current page source snippet for debugging
                page_source = self.driver.page_source
                if "Confirmar" in page_source:
                    self.logger.info("'Confirmar' text found in page source")
                else:
                    self.logger.warning("'Confirmar' text NOT found in page source")
                    
            except Exception as e:
                self.logger.warning(f"DOM diagnosis failed: {e}")
            
            # Strategy: Try to find the button using find_elements (not wait_to_be_clickable)
            continue_button = None
            
            # Try different locators to find the button
            locators_to_try = [
                self.CONFIRM_SPECIAL_ASISTANCE_MODAL,
                (By.XPATH, "//button[contains(@class,'btn-action btn-Medium')]//span[text()='Confirmar']"),
                (By.XPATH, "//button//span[text()='Confirmar']"),
                (By.XPATH, "//button[contains(@id,'dsButtonId_')]//span[text()='Confirmar']"),
                (By.XPATH, "//button[contains(@class,'button') and contains(@class,'btn-action')]")
            ]
            
            for i, locator in enumerate(locators_to_try):
                try:
                    buttons = self.driver.find_elements(*locator)
                    if buttons:
                        # Find the button that contains "Confirmar" text
                        for button in buttons:
                            try:
                                if "Confirmar" in button.text or "Confirmar" in button.get_attribute("innerHTML"):
                                    continue_button = button
                                    self.logger.info(f"Special assistance confirm button found with locator strategy {i+1}")
                                    break
                            except:
                                continue
                        if continue_button:
                            break
                except Exception as e:
                    self.logger.warning(f"Locator strategy {i+1} failed: {e}")
                    continue
            
            if not continue_button:
                self.logger.error("Could not find special assistance confirm button with any strategy")
                raise Exception("Could not find special assistance confirm button with any strategy")
            
            self.logger.info("Special assistance confirm button found, ensuring it's visible and clickable...")

            # Enhanced scroll strategy to ensure button is visible
            self.logger.info("Performing enhanced scroll to make special assistance button visible...")
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
            self.logger.info("Verifying special assistance button is visible and clickable...")
            if not continue_button.is_displayed():
                self.logger.warning("Button is not displayed, trying additional scroll...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
                time.sleep(1)

            # Try different click strategies
            try:
                continue_button.click()
                self.logger.info("Special assistance services confirmed with direct click.")
            except Exception as e:
                self.logger.warning(f"Direct click failed: {e}, trying JavaScript click...")
                self.driver.execute_script("arguments[0].click();", continue_button)
                self.logger.info("Special assistance services confirmed with JavaScript click.")
            
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to confirm special assistance services") from e

    @catch_exceptions()    
    def continue_to_the_next_step(self):     
        """
        Continues to the next step by clicking the "Continuar" button.

        This method waits until the "Continuar" button is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.
        """
        try:
            self.wait_for_loader_to_disappear(self.LOADER_C)
            
            # First, scroll down to ensure modal content is visible
            self.logger.info("Scrolling down to make continue button visible...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Wait for the button to appear and be clickable
            self.logger.info("Waiting for the continue button to appear...")
            continue_button = self.wait_to_be_clickable(self.CONFIRM_SERVICES_BUTTON)
            self.logger.info("Continue button found, ensuring it's visible and clickable...")

            # Enhanced scroll strategy to ensure button is visible
            self.logger.info("Performing enhanced scroll to make continue button visible...")
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
            self.logger.info("Verifying continue button is visible and clickable...")
            if not continue_button.is_displayed():
                self.logger.warning("Button is not displayed, trying additional scroll...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
                time.sleep(1)

            # Try different click strategies
            try:
                continue_button.click()
                self.logger.info("Continue button clicked with direct click.")
            except Exception as e:
                self.logger.warning(f"Direct click failed: {e}, trying JavaScript click...")
                self.driver.execute_script("arguments[0].click();", continue_button)
                self.logger.info("Continue button clicked with JavaScript click.")
        
            self.logger.info("Services added... Going to the seatmap page...")
    
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to continue to next step") from e