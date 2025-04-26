from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def get_driver(browser_name):
    """
    Return a WebDriver instance for the given browser name.

    Args:
        browser_name: one of "chrome" or "firefox"

    Returns:
        a WebDriver instance

    Raises:
        ValueError: if browser_name is not one of "chrome" or "firefox"
    """
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
