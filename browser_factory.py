import platform
import tempfile
import os
import random
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
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-application-cache")
        
        # Create unique user data directory and port for each session
        user_data_dir = tempfile.mkdtemp(prefix="chrome_user_data_")
        debug_port = random.randint(9223, 9999)
        
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument(f"--remote-debugging-port={debug_port}")
        
        if headless:
            options.add_argument("--headless=new")
        
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
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-application-cache")
        
        # Create unique user data directory and port for each session
        user_data_dir = tempfile.mkdtemp(prefix="edge_user_data_")
        debug_port = random.randint(9223, 9999)
        
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument(f"--remote-debugging-port={debug_port}")
        
        if headless:
            options.add_argument("--headless=new")

        return webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
    elif browser_name == "safari":
        if platform.system() != "Darwin":
            raise EnvironmentError("Safari is only supported on macOS.")
        if headless:
            raise ValueError("Safari does not support headless mode.")
        return webdriver.Safari()
 

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
