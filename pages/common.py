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
    
    def wait_for_invisibility(self, locator):
        return self._wait.until(EC.invisibility_of_element_located(locator))
    
    def wait_to_be_clickable(self, locator):
        return self._wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_visibility(self, locator):
        return self._wait.until(EC.visibility_of(locator))

    def find(self, locator):
        return self.driver.find_element(*locator)
    
    def find_all(self, locator):
        return self.driver.find_elements(*locator)
    
    def context_click(self, element):
        return self._action.context_click(element)
    
    def scroll_down_to_element(self, element):
        return self._action.move_to_element(element)

    def alert(self):
        return self._wait.until(EC.alert_is_present())