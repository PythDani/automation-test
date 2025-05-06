

from selenium.webdriver.common.by import By
from utils.exception import catch_exceptions
from logger import get_logger
from pages.common import Common
from selenium.common.exceptions import TimeoutException
import time

class ServicesPage(Common):
    # ----------------------------------LOCATORS----------------------------------------------------------
    #Loader that indicate that the page is loading in some cases.
    LOADER_C:                                    tuple = (By.CLASS_NAME, "loading")
    
    CARRY_ON_AND_CHECKED_BAGGAGE_ADD_BUTTON:     tuple = (By.ID, "serviceButtonTypeBaggage")
    CARRY_ON_BAGGAGE_PLUS_BUTTON:                tuple = (By.XPATH, "//button[span[@id='434142477E4341525259204F4E20424147474147452031304B4720313135204C434D7E426167676167657E452E3031302E462E365F535431 increase']]")
    CONFIRM_CARRY_ON_AND_CHECKED_BAGGAGE_MODAL:  tuple = (By.XPATH, "//button[.//span[normalize-space(text())='Confirmar']]")
    SPORT_BAGGAGE_ADD_BUTTON:                    tuple = (By.ID, "serviceButtonTypeOversize")
    GOLF_EQUIPMENT_PLUS_BUTTON:                  tuple = (By.XPATH, "//button[contains(@class, 'ui-num-ud_button') and contains(@class, 'plus')]")
    CONFIRM_SPORT_BAGGAGE_MODAL:                 tuple = (By.XPATH, "//button[.//span[normalize-space(text())='Confirmar']]")
    BUSSINESS_LOUNGE_ADD_BUTTON:                 tuple = (By.ID, "serviceButtonTypeBusinessLounge")
    LOUNGES_PLUS_BUTTON:                         tuple = (By.XPATH, "//span[@class='label_text' and normalize-space(text())='Añadir']")
    CONFIRM_LOUNGES_MODAL:                       tuple = (By.XPATH, "//button[.//span[normalize-space(text())='Confirmar']]")
    CONFIRM_SERVICES_BUTTON:                     tuple = (By.XPATH, "//div[contains(@class, 'summary') and contains(@class, 'oneway')]//button[contains(@class, 'btn-next') and .//span[normalize-space()='Continuar']]")
    
    def __init__(self, driver):
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
            self.wait_for_loader_to_disappear()
            self.wait_for_loader_to_disappear()
            self.logger.info("Page loaded correctly.")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {self.__class__.__name__}") from e
        
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
            add_carry_on_button =self.wait_for_visibility_of_element_located(self.CARRY_ON_AND_CHECKED_BAGGAGE_ADD_BUTTON)
            add_carry_on_button.click()
            self.logger.info(f"{name} opened...")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {name}") from e
        
    def click_on_bagage_plus_button(self):
        """
        Clicks on the "Add bagage" plus button.

        This method waits until the "Add bagage" plus button is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.

        """
        
        try:
            self.logger.info("Adding carry-on baggage...")
            self.wait_for(self.CARRY_ON_BAGGAGE_PLUS_BUTTON)
            time.sleep(2)
            plus_button = self.wait_for(self.CARRY_ON_BAGGAGE_PLUS_BUTTON)
            # time.sleep(4)
            plus_button.click()           
            self.logger.info("Adding carry-on baggage added...")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to add carry-on baggage") from e
    
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
            time.sleep(4)
            continue_button.click()
            self.logger.info("Baggage confirmed...")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to confirm baggage") from e
            
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
            add_sport_on_button =self.wait_for_visibility_of_element_located(self.SPORT_BAGGAGE_ADD_BUTTON)
            add_sport_on_button.click()
            self.logger.info(f"{name} opened...")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {name}") from e

    def click_on_sport_bagage_plus_button(self):       
        
        """
        Clicks on the "Add sport baggage" plus button.

        This method waits until the "Add sport baggage" plus button is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.

        Raises:
            Exception: If the "Add sport baggage" plus button is not found or clickable within the timeout period.
        """
        try:
            self.logger.info("Add sport baggage...")
            plus_button = self.find(self.GOLF_EQUIPMENT_PLUS_BUTTON)
            time.sleep(4)
            plus_button.click()           
            self.logger.info("Sport baggage added...")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to add sport baggage") from e
    
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
            time.sleep(4)
            continue_button.click()
            self.logger.info("Sport baggage confirmed...")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to confirm sport baggage") from e
        
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
            continue_next_step_button =self.wait_for_visibility_of_element_located(self.BUSSINESS_LOUNGE_ADD_BUTTON)
            self._action.scroll_to_element(continue_next_step_button).perform()
            continue_next_step_button.click()
            self.logger.info(f" {name} opened")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {name}") from e
  
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
            self.logger.info("Add lounge bussines services...")
            plus_button = self.find(self.LOUNGES_PLUS_BUTTON)
            time.sleep(4)
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
        time.sleep(4)
        continue_button.click()
        self.logger.info("Lounge business services confirmed")
    
    @catch_exceptions()    
    def continue_to_the_next_step(self):     
        """
        Continues to the next step by clicking the "Continuar" button.

        This method waits until the "Continuar" button is visible and clickable, then clicks on it.
        If the button is not found or clickable within the timeout period, a TimeoutException is raised.

        """
        
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
    
    def wait_for_loader_to_disappear(self):
        """
        Waits for the loader to disappear.

        This method waits until the loader appears, and then waits until the loader disappears.

        If the loader does not appear or does not disappear within the timeout period, a TimeoutException is raised.

        This method is used to wait for the loader to disappear after performing an action that triggers it to appear.

        """        
        try:
            
            loader_locator = (self.LOADER_C)  # ejemplo
            
            # Wait for the loader to appear
            self.wait_for(loader_locator)
            
            # Wait for the loader to disappear
            self.wait_for_unitll_not(loader_locator)
        except:            
            pass
        

        

    



