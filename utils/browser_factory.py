from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def get_driver(browser_name, headless=False):
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
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--remote-debugging-port=9222")
        # options.add_argument("--headless")
        if headless:
            options.add_argument("--headless")
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        # options.set_preference("devtools.console.stdout.content", True)  # Mostrar logs si es posible
        # options.set_preference("dom.webnotifications.enabled", False)    # Desactiva notificaciones
        # options.set_preference("dom.push.enabled", False)                # Desactiva push API
        # options.set_preference("dom.disable_open_during_load", False)    # Permitir popups si es necesario

        # options.set_preference("security.sandbox.content.level", 0)
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-extensions")
        # options.add_argument("--headless")
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
       
        if headless:
            options.add_argument("--headless=new")  # "new" para compatibilidad moderna
            options.add_argument("--disable-gpu")

       
        # options.add_argument(f"user-data-dir=C:\\Users\\{os.environ.get('username')}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default")
        # options.add_argument("--start-maximized") // We have a trooble with page size in seatmap page, for this reason we comment this line.

        # Inicializa el driver con EdgeService
        return webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )

    
    
    
    
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
