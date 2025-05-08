from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    
from selenium.webdriver.common.action_chains import ActionChains
from config import HOME_URL
class Common:

    def __init__(self, driver):
        """
        Constructor of the Common class.

        Args:
            driver (selenium.webdriver): The selenium webdriver instance.

        Attributes:
            driver (selenium.webdriver): The selenium webdriver instance.
            _wait (selenium.webdriver.support.wait.WebDriverWait):
                The WebDriverWait instance.
            _action (selenium.webdriver.common.action_chains.ActionChains):
                The ActionChains instance.
            URL (str): The URL of the application's home page.
        """
        self.driver = driver
        self._wait = WebDriverWait(self.driver, 10)
        self._action = ActionChains(self.driver)
        self.URL = HOME_URL

    def wait_for(self, locator):
        """
        Waits until the element identified by the given locator is present.

        Args:
            locator (tuple): A tuple containing the By class and the value of the element to search for.

        Returns:
            selenium.webdriver.remote.webelement.WebElement: The element identified by the given locator.

        Raises:
            selenium.common.exceptions.TimeoutException: If the element is not found within the timeout period.
        """
        return self._wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_unitll_not(self, locator):

        """
        Waits until the element identified by the given locator is not present.

        Args:
            locator (tuple): A tuple containing the By class and the value of the element to search for.

        Returns:
            None

        Raises:
            selenium.common.exceptions.TimeoutException: If the element is still present within the timeout period.
        """

        return self._wait.until_not(EC.presence_of_element_located(locator))
    
    def wait_for_invisibility(self, locator):
        """
        Waits until the element identified by the given locator is not visible.

        Args:
            locator (tuple): A tuple containing the By class and the value of the element to search for.

        Returns:
            None

        Raises:
            selenium.common.exceptions.TimeoutException: If the element is still visible within the timeout period.
        """
        return self._wait.until(EC.invisibility_of_element_located(locator))
    
    def wait_to_be_clickable(self, locator):
        """
        Waits until the element identified by the given locator is clickable.

        Args:
            locator (tuple): A tuple containing the By class and the value of the element to search for.

        Returns:
            selenium.webdriver.remote.webelement.WebElement: The element identified by the given locator.

        Raises:
            selenium.common.exceptions.TimeoutException: If the element is not clickable within the timeout period.
        """
        return self._wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_visibility(self, element):

        """
        Waits until the specified web element is visible.

        Args:
            element (selenium.webdriver.remote.webelement.WebElement): The web element to wait for visibility.

        Returns:
            selenium.webdriver.remote.webelement.WebElement: The web element once it becomes visible.

        Raises:
            selenium.common.exceptions.TimeoutException: If the element does not become visible within the timeout period.
        """

        return self._wait.until(EC.visibility_of(element))
    
    def wait_for_visibility_of_element_located(self, locator):
        """
        Waits until the element identified by the given locator is visible.

        Args:
            locator (tuple): A tuple containing the By class and the value of the element to search for.

        Returns:
            selenium.webdriver.remote.webelement.WebElement: The element identified by the given locator once it becomes visible.

        Raises:
            selenium.common.exceptions.TimeoutException: If the element does not become visible within the timeout period.
        """


        return self._wait.until(EC.visibility_of_element_located(locator))

    def find(self, locator):
        
        """
        Finds an element given a locator.

        Args:
            locator (tuple): A tuple containing the By class and the value of the element to search for.

        Returns:
            selenium.webdriver.remote.webelement.WebElement: The element identified by the given locator.

        Raises:
            selenium.common.exceptions.NoSuchElementException: If the element is not found.
        """
        
        return self.driver.find_element(*locator)
    
    def find_all(self, locator):
        
        """
        Finds all elements matching the given locator.

        Args:
            locator (tuple): A tuple containing the By class and the value of the elements to search for.

        Returns:
            list[selenium.webdriver.remote.webelement.WebElement]: A list of elements identified by the given locator.

        Raises:
            selenium.common.exceptions.NoSuchElementException: If no elements are found.
        """

        return self.driver.find_elements(*locator)
    
    def context_click(self, element):
        
        """
        Performs a context-click (right-click) on an element.

        Args:
            element (selenium.webdriver.remote.webelement.WebElement): The element to context-click.

        Returns:
            selenium.webdriver.common.action_chains.ActionChains: The action chain object used to perform the context-click.
        """
        return self._action.context_click(element)
    
    def scroll_down_to_element(self, element):
        """
        Scrolls the page down to the given element.

        Args:
            element (selenium.webdriver.remote.webelement.WebElement): The element to scroll down to.

        Returns:
            selenium.webdriver.common.action_chains.ActionChains: The action chain object used to scroll down to the element.
        """
        return self._action.move_to_element(element)

    def scroll_down_move_to_element(self, element):

        
        """
        Scrolls the page down to the given element, and moves the element to the center of the screen.

        Args:
            element (selenium.webdriver.remote.webelement.WebElement): The element to scroll down to.

        Returns:
            None
        """
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def scroll_down_by_pixels(self, pixels: int = 200):
        """
        Scrolls the page down by the given number of pixels.

        Args:
            pixels (int, optional): The number of pixels to scroll down. Defaults to 200.
        """
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")    

    
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