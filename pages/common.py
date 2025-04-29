from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    
from selenium.webdriver.common.action_chains import ActionChains
from config import HOME_URL
class Common:

    def __init__(self, driver):
        self.driver = driver
        self._wait = WebDriverWait(self.driver, 10)
        self._action = ActionChains(self.driver)
        self.URL = HOME_URL

    def wait_for(self, locator):
        return self._wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_unitll_not(self, locator):
        return self._wait.until_not(EC.presence_of_element_located(locator))
    
    def wait_for_invisibility(self, locator):
        return self._wait.until(EC.invisibility_of_element_located(locator))
    
    def wait_to_be_clickable(self, locator):
        return self._wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_visibility(self, locator):
        return self._wait.until(EC.visibility_of(locator))
    
    def wait_for_visibility_of_element_located(self, locator):
        return self._wait.until(EC.visibility_of_element_located(locator))

    def find(self, locator):
        return self.driver.find_element(*locator)
    
    def find_all(self, locator):
        return self.driver.find_elements(*locator)
    
    def context_click(self, element):
        return self._action.context_click(element)
    
    def scroll_down_to_element(self, element):
        return self._action.move_to_element(element)

    def scroll_down_move_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    def alert(self):
        return self._wait.until(EC.alert_is_present())
    
    def wait_for_loader_to_disappear(self, locator):
        """
        Waits for the loader to disappear.

        This method waits until the loader appears, and then waits until the loader disappears.

        If the loader does not appear or does not disappear within the timeout period, a TimeoutException is raised.

        This method is used to wait for the loader to disappear after performing an action that triggers it to appear.

        """        
        try:
            
            loader_locator = (locator)  # ejemplo
            
            # Wait for the loader to appear
            self.wait_for(loader_locator)
            
            # Wait for the loader to disappear
            self.wait_for_unitll_not(loader_locator)
        except:            
            pass