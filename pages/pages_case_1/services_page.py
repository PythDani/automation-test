

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
    CONFIRM_CARRY_ON_AND_CHECKED_BAGGAGE_MODAL:  tuple = (By.XPATH, "//*[contains(@class,'button amount-summary_button amount-summary_button-action is-action ng-star-inserted')]")
    SPORT_BAGGAGE_ADD_BUTTON:                    tuple = (By.ID, "serviceButtonTypeOversize")
    SPORT_EQUIPMENT_PLUS_BUTTON:                  tuple = (By.XPATH, "//button[contains(@class,'ui-num-ud_button plus')]")
    CONFIRM_SPORT_BAGGAGE_MODAL:                 tuple = (By.XPATH, "//*[contains(@class,'button amount-summary_button amount-summary_button-action is-action ng-star-inserted')]")
    BUSSINESS_LOUNGE_ADD_BUTTON:                 tuple = (By.XPATH, "//button[contains(@id,'serviceButtonTypeBusinessLounge')]")
    LOUNGES_PLUS_BUTTON:                         tuple = (By.XPATH, "//label[contains(@class,'service_item_button button')]")
    CONFIRM_LOUNGES_MODAL:                       tuple = (By.XPATH, "//*[contains(@class,'button amount-summary_button amount-summary_button-action is-action ng-star-inserted')]")
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
            add_carry_on_button =self.wait_for_visibility_of_element_located(self.CARRY_ON_AND_CHECKED_BAGGAGE_ADD_BUTTON)
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
            self.logger.info("Click on confirm button...")          
            self.wait_for(self.CONFIRM_CARRY_ON_AND_CHECKED_BAGGAGE_MODAL)
            continue_button = self.wait_for(self.CONFIRM_CARRY_ON_AND_CHECKED_BAGGAGE_MODAL)
            self._action.scroll_to_element(continue_button).perform()

            self.scroll_down_move_to_element(continue_button)
            self.driver.implicitly_wait(1)

            continue_button.click()
            self.logger.info("Baggage confirmed...")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to confirm baggage") from e
    
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
            add_sport_on_button =self.wait_for_visibility_of_element_located(self.SPORT_BAGGAGE_ADD_BUTTON)
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
            self.logger.info("Click on confirm button...")            
            continue_button = self.find(self.CONFIRM_SPORT_BAGGAGE_MODAL)
            self._action.scroll_to_element(continue_button).perform()

            self.scroll_down_move_to_element(continue_button)
            self.driver.implicitly_wait(1)           

            continue_button.click()
            self.logger.info("Sport baggage confirmed...")
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
        self.logger.info("Click on confirm button...")              
        continue_button = self.find(self.CONFIRM_LOUNGES_MODAL)

        self._action.scroll_to_element(continue_button).perform() 
        self.scroll_down_move_to_element(continue_button)
        self.driver.implicitly_wait(1)    

        continue_button.click()
        self.logger.info("Lounge business services confirmed")
    
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
            add_asistance_on_button =self.wait_for_visibility_of_element_located(self.SPECIAL_ASISTANCE_ADD_BUTTON)
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
        self.logger.info("Click on confirm button...")              
        continue_button = self.find(self.CONFIRM_SPECIAL_ASISTANCE_MODAL)
        self._action.scroll_to_element(continue_button).perform()       
        continue_button.click()
        self.logger.info("special asistance services confirmed")

    @catch_exceptions()    
    def continue_to_the_next_step(self):     
        """
        Continues to the next step by clicking the "Continuar" button.

        This method waits until the "Continuar" button is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.

        """
        self.wait_for_loader_to_disappear(self.LOADER_C)
        # Wait for the button to appear
        self.logger.info("Waiting for the button to appear...")
        add_bussines_on_button = self.wait_for(self.CONFIRM_SERVICES_BUTTON)

        # Scroll to the button
        self.scroll_down_move_to_element(add_bussines_on_button)
        self.logger.info("Scroll to the button Continue...'")

        # SLEEP(1) added
        time.sleep(1)

        # Click the button            
        self.driver.execute_script("arguments[0].click();", add_bussines_on_button)
        self.logger.info("Services added... Going to the seatmap page...")
    
    
        

        

    



