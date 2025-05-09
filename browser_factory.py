from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def get_driver(browser_name, headless=False):

   

    """
    Initializes and returns a Selenium WebDriver instance based on the specified browser.

    This function sets up a WebDriver instance for either Chrome, Firefox, or Edge, with
    options to run in headless mode. It uses the `webdriver_manager` package to automatically
    manage driver binaries.

    Args:
        browser_name (str): The name of the browser to use ("chrome", "firefox", or "edge").
        headless (bool): Optional; whether to run the browser in headless mode. Default is False.

    Returns:
        selenium.webdriver: An instance of the Selenium WebDriver for the specified browser.

    Raises:
        ValueError: If the specified browser is not supported.
    """

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--start-maximized")        
        if headless:
            options.add_argument("--headless")
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()     
        if headless:
            options.add_argument("--headless")
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    elif browser_name == "edge":
        options = EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--start-maximized")
        if headless:

            options.add_argument("--headless=new") 
            options.add_argument("--disable-gpu")       

        return webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        ) 

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
