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
        
        # Basic stability options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")
        
        # GPU and hardware acceleration options
        options.add_argument("--disable-gpu-sandbox")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-gpu-process-crash-limit")
        options.add_argument("--disable-gpu-watchdog")
        options.add_argument("--disable-gpu-rasterization")
        options.add_argument("--disable-accelerated-2d-canvas")
        options.add_argument("--disable-accelerated-jpeg-decoding")
        options.add_argument("--disable-accelerated-mjpeg-decode")
        options.add_argument("--disable-accelerated-video-decode")
        options.add_argument("--disable-accelerated-video-encode")
        
        # Memory and performance options
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-background-sync")
        options.add_argument("--disable-background-media-suspend")
        options.add_argument("--disable-background-media-playback")
        
        # Network and process stability
        options.add_argument("--disable-background-mode")
        options.add_argument("--disable-component-extensions-with-background-pages")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-translate")
        options.add_argument("--disable-ipc-flooding-protection")
        
        # Security options (simplified)
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-features=TranslateUI")
        options.add_argument("--disable-features=BlinkGenPropertyTrees")
        options.add_argument("--disable-features=EnableDrDc")
        
        # Additional stability options
        options.add_argument("--disable-hang-monitor")
        options.add_argument("--disable-prompt-on-repost")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-component-update")
        options.add_argument("--disable-domain-reliability")
        options.add_argument("--disable-features=AudioServiceOutOfProcess")
        options.add_argument("--disable-features=MediaRouter")
        options.add_argument("--disable-features=UserAgentClientHint")
        options.add_argument("--disable-features=VizServiceDisplayCompositor")
        
        # Create unique user data directory and port for each session
        user_data_dir = tempfile.mkdtemp(prefix="chrome_user_data_")
        debug_port = random.randint(9223, 9999)
        
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument(f"--remote-debugging-port={debug_port}")
        
        # Additional stability options
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
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
