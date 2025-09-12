# Load environment variables from .env file FIRST
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Environment variables loaded from .env file")
except ImportError:
    print("python-dotenv not installed, using system environment variables only")

import datetime
import os
import allure
import pyscreenrec
import pytest
import psutil
import signal
import time
import time

from pages.pages_case_1.booking_select_page import BookingSelectPage
from pages.pages_case_1.form_passengers_page import FormPassengersPage
from pages.pages_case_1.home_page import HomePage
from pages.pages_case_1.itinerary_page import ItineraryPage
from pages.pages_case_1.payment_page import PaymentPage
from pages.pages_case_1.seat_map_page import SeatMapPage
from pages.pages_case_1.services_page import ServicesPage


from browser_factory import get_driver
from utils.db_utils import store_result, create_db
from logger import get_logger
import logging


VIDEO_DIR = os.path.join(os.getcwd(), "videos")
SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)



get_logger()
logger = logging.getLogger(__name__)
logger.info("Start pytest script")

def cleanup_browser_processes(aggressive=False):
    """
    Clean up any remaining browser processes that might be hanging around.
    This helps prevent the "user data directory already in use" error.
    
    Args:
        aggressive (bool): If True, kills all automation-related processes more aggressively
    """
    try:
        # List of applications to NEVER kill (even if they use Chrome/Edge)
        protected_apps = [
            'teams.exe', 'ms-teams.exe', 'teams', 'ms-teams',
            'slack.exe', 'slack', 'discord.exe', 'discord',
            'whatsapp.exe', 'whatsapp', 'telegram.exe', 'telegram',
            'spotify.exe', 'spotify', 'vscode.exe', 'code.exe',
            'pycharm.exe', 'pycharm64.exe', 'idea.exe', 'idea64.exe'
        ]
        
        killed_processes = []
        
        # Only kill Chrome processes that are likely from our automation
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    # Skip if it's a protected application
                    if any(protected in proc.info['name'].lower() for protected in protected_apps):
                        continue
                        
                    # Check if this is a Chrome process from our automation
                    cmdline = proc.info.get('cmdline', [])
                    cmdline_str = ' '.join(cmdline) if cmdline else ''
                    
                    should_kill = False
                    
                    if aggressive:
                        # In aggressive mode, kill any Chrome process with automation args
                        should_kill = any(arg in cmdline_str for arg in [
                            '--user-data-dir=chrome_user_data_',
                            '--remote-debugging-port=',
                            '--no-sandbox',
                            '--disable-dev-shm-usage',
                            '--disable-extensions',
                            '--disable-gpu',
                            '--disable-web-security',
                            '--disable-features=VizDisplayCompositor'
                        ])
                    else:
                        # In normal mode, only kill sub-processes
                        should_kill = (any(arg in cmdline_str for arg in [
                            '--user-data-dir=chrome_user_data_',
                            '--remote-debugging-port=',
                            '--no-sandbox',
                            '--disable-dev-shm-usage',
                            '--disable-extensions',
                            '--disable-gpu',
                            '--disable-web-security',
                            '--disable-features=VizDisplayCompositor'
                        ]) and '--type=' in cmdline_str)
                    
                    if should_kill:
                        logger.info(f"Killing automation Chrome process: {proc.info['pid']} - {proc.info['name']}")
                        proc.kill()
                        killed_processes.append(f"Chrome-{proc.info['pid']}")
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Only kill Edge processes that are likely from our automation
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'msedge' in proc.info['name'].lower():
                    # Skip if it's a protected application
                    if any(protected in proc.info['name'].lower() for protected in protected_apps):
                        continue
                        
                    # Check if this is an Edge process from our automation
                    cmdline = proc.info.get('cmdline', [])
                    cmdline_str = ' '.join(cmdline) if cmdline else ''
                    
                    should_kill = False
                    
                    if aggressive:
                        # In aggressive mode, kill any Edge process with automation args
                        should_kill = any(arg in cmdline_str for arg in [
                            '--user-data-dir=edge_user_data_',
                            '--remote-debugging-port=',
                            '--no-sandbox',
                            '--disable-dev-shm-usage',
                            '--disable-extensions',
                            '--disable-gpu',
                            '--disable-web-security',
                            '--disable-features=VizDisplayCompositor'
                        ])
                    else:
                        # In normal mode, only kill sub-processes
                        should_kill = (any(arg in cmdline_str for arg in [
                            '--user-data-dir=edge_user_data_',
                            '--remote-debugging-port=',
                            '--no-sandbox',
                            '--disable-dev-shm-usage',
                            '--disable-extensions',
                            '--disable-gpu',
                            '--disable-web-security',
                            '--disable-features=VizDisplayCompositor'
                        ]) and '--type=' in cmdline_str)
                    
                    if should_kill:
                        logger.info(f"Killing automation Edge process: {proc.info['pid']} - {proc.info['name']}")
                        proc.kill()
                        killed_processes.append(f"Edge-{proc.info['pid']}")
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Also kill any remaining WebDriver processes
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and any(driver in proc.info['name'].lower() for driver in [
                    'chromedriver', 'geckodriver', 'msedgedriver'
                ]):
                    logger.info(f"Killing WebDriver process: {proc.info['pid']} - {proc.info['name']}")
                    proc.kill()
                    killed_processes.append(f"WebDriver-{proc.info['pid']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        if killed_processes:
            logger.info(f"Killed {len(killed_processes)} automation processes: {', '.join(killed_processes)}")
        
        time.sleep(1 if aggressive else 0.5)  # Give processes time to terminate
        
    except Exception as e:
        logger.warning(f"Error during browser cleanup: {e}")

def force_cleanup_all_automation_processes():
    """
    Force cleanup all automation-related processes at the end of test session.
    This is more aggressive and should only be called at the end of all tests.
    """
    logger.info("Starting aggressive cleanup of all automation processes...")
    cleanup_browser_processes(aggressive=True)
    
    # Additional cleanup for any remaining automation processes
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and any(keyword in proc.info['name'].lower() for keyword in [
                    'selenium', 'webdriver', 'pytest', 'python'
                ]):
                    cmdline = proc.info.get('cmdline', [])
                    cmdline_str = ' '.join(cmdline) if cmdline else ''
                    
                    # Only kill if it's related to our automation
                    if any(arg in cmdline_str for arg in [
                        'test_av_test_case', 'automation-test', 'pytest'
                    ]):
                        logger.info(f"Force killing automation process: {proc.info['pid']} - {proc.info['name']}")
                        proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception as e:
        logger.warning(f"Error during force cleanup: {e}")
    
    logger.info("Aggressive cleanup completed.")

@pytest.fixture(scope="function")
def booking_context(browser):
    """
    A pytest fixture that sets up the context for booking-related tests.

    This fixture initializes page objects for different pages involved in the booking process,
    including HomePage, FormPassengersPage, ServicesPage, SeatMapPage, PaymentPage, 
    BookingSelectPage, and ItineraryPage, using the provided browser instance. It also 
    includes a set of parameters for the booking process, such as language, currency, 
    origin and destination cities, departure date, and the number of passengers.

    Args:
        browser (WebDriver): A selenium webdriver instance used to interact with web pages.

    Returns:
        dict: A dictionary containing initialized page objects and booking parameters.
    """

    return {
        "page": HomePage(browser),
        "form": FormPassengersPage(browser),
        "services": ServicesPage(browser),
        "seat_map": SeatMapPage(browser),
        "payment_page": PaymentPage(browser),
        "booking_select_page": BookingSelectPage(browser),
        "itinerary_page": ItineraryPage(browser),
        "params": {
            "language": "Español",
            "currency": "Colombia",
            "city_origin": "Medellín",
            "city_destination": "Bogotá",
            "departure_date": {"day": "20", "month": "12", "year": "2025"},
            "arrival_date": {"day": "30", "month": "1", "year": "2025"},
            "passenger_count": 2,
            "young_count": 0,
            "child_count": 0,
            "baby_count": 0
        }
    }

@pytest.fixture(scope="function")
def booking_context_case_2(browser):  
    """
    This fixture initializes page objects for different pages involved in the booking process,
    including HomePage, FormPassengersPage, ServicesPage, SeatMapPage, PaymentPage, 
    BookingSelectPage, and ItineraryPage, using the provided browser instance. It also 
    includes a set of parameters for the booking process, such as language, currency, 
    origin and destination cities, departure date, and the number of passengers.

    Args:
        browser (WebDriver): A selenium webdriver instance used to interact with web pages.

    Returns:
        dict: A dictionary containing initialized page objects and booking parameters.
    """

    return {
        "page": HomePage(browser),
        "form": FormPassengersPage(browser),
        "services": ServicesPage(browser),
        "seat_map": SeatMapPage(browser),
        "payment_page": PaymentPage(browser),
        "booking_select_page": BookingSelectPage(browser),
        "itinerary_page": ItineraryPage(browser),
        "params": {
            "language": "Español",
            "currency": "Colombia",
            "city_origin": "Managua",
            "city_destination": "Medellín",
            "departure_date": {"day": "17", "month": "10", "year": "2025"},
            "arrival_date": {"day": "30", "month": "10", "year": "2025"},

            "passenger_count": 1,
            "young_count": 0,
            "child_count": 0,
            "baby_count": 0,
            "relative_day": "2 days before",
            "a_credits_number": os.getenv("CARD_CREDIT_NUMBER"),
            "a_credits_pin": os.getenv("CREDIT_PIN"),

        }
    }

@pytest.fixture(scope="function")
def booking_context_case_3(browser):  
    """
    This fixture initializes page objects for different pages involved in the booking process,
    including HomePage, FormPassengersPage, ServicesPage, SeatMapPage, PaymentPage, 
    BookingSelectPage, and ItineraryPage, using the provided browser instance. It also 
    includes a set of parameters for the booking process, such as language, currency, 
    origin and destination cities, departure date, and the number of passengers.

    Args:
        browser (WebDriver): A selenium webdriver instance used to interact with web pages.

    Returns:
        dict: A dictionary containing initialized page objects and booking parameters.
    """

    return {
        "page": HomePage(browser),
        "form": FormPassengersPage(browser),
        "services": ServicesPage(browser),
        "seat_map": SeatMapPage(browser),
        "payment_page": PaymentPage(browser),
        "booking_select_page": BookingSelectPage(browser),
        "itinerary_page": ItineraryPage(browser),
        "params": {
            "language": "Français",
            "currency": "France",
            "city_origin": "Managua",
            "city_destination": "Medellín",
            "departure_date": {"day": "14", "month": "11", "year": "2025"},
            "arrival_date": {"day": "30", "month": "11", "year": "2025"},

            "passenger_count": 3,
            "young_count": 1,
            "child_count": 0,
            "baby_count": 0,
            "relative_day": "2 days before",
            "user_name": os.getenv("USER_NAME"),
            "user_password": os.getenv("USER_PASSWORD"),
            "a_credits_number": os.getenv("CARD_CREDIT_NUMBER"),
            "a_credits_pin": os.getenv("CREDIT_PIN"),

        }
    }

def pytest_addoption(parser):
    """
    Registers a pytest command-line option to specify the browser to use.

    This function registers a pytest command-line option to specify the browser
    to use when running tests. The option is named `--browser`, and it accepts
    either "chrome" or "firefox" as its value. The default value is "chrome".

    Parameters:
        parser: The pytest command-line parser object.

    Returns:
        None
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use: chrome, edge or firefox"
    )
    parser.addoption(
        "--headless",
        action="store",
        default="false",
        help="Run tests in headless mode: true or false"
    )
    parser.addoption(
        "--home_url", 
        action="store", 
        default=os.getenv("HOME_URL"), 
        help="Base URL for the tests")
    parser.addoption(
        "--disable-cleanup",
        action="store_true",
        default=False,
        help="Disable browser process cleanup to avoid closing other applications")
    parser.addoption(
        "--aggressive-cleanup",
        action="store_true",
        default=False,
        help="Enable aggressive cleanup mode for better memory management")

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--home_url")

@pytest.fixture(scope="function")
def browser(request):
    """
    A pytest fixture to initialize a web driver for the specified browser.

    This fixture retrieves the browser name from the pytest command-line options,
    initializes the corresponding web driver using the `get_driver` function, and
    yields the driver for use in test functions. After the test function completes,
    the driver is quit to clean up resources.

    Yields:
        WebDriver: An instance of the web driver for the specified browser.
    """
    # Clean up any existing browser processes before starting (only if not disabled)
    disable_cleanup = request.config.getoption("--disable-cleanup")
    aggressive_cleanup = request.config.getoption("--aggressive-cleanup")
    
    if not disable_cleanup:
        cleanup_browser_processes(aggressive=aggressive_cleanup)
    
    browser_name = request.config.getoption("--browser")
    headless_option = request.config.getoption("--headless").lower() == "true"
    
    driver = None
    try:
        driver = get_driver(browser_name, headless_option)
        yield driver
    finally:
        # Ensure driver is properly closed
        if driver is not None:
            try:
                driver.quit()
            except Exception as e:
                logger.warning(f"Error closing driver: {e}")
        
        # Clean up any remaining processes (only if not disabled)
        if not disable_cleanup:
            cleanup_browser_processes(aggressive=aggressive_cleanup)

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):  
    """
    A pytest hook to store test results in a database after each test.

    This hook stores the name of the test and its result in a SQLite database
    after each test is executed. The database is stored in a file named
    'test_results.db' in the current working directory.

    Parameters:
        report (pytest.RunTestProtocol): The pytest report object.

    Returns:
        None
    """
    
    if report.when == 'call':  # it makes sure save it after each test
        store_result(report.nodeid, report.outcome)  # store the name of the test and the result

def pytest_sessionstart(session):
    """
    A pytest setup function to create the 'test_results.db' database file.

    This function creates the 'test_results.db' database file if it does not
    already exist. This database is used to store test results.

    Returns:
        None
    """
    create_db()

def pytest_sessionfinish(session, exitstatus):
    """
    A pytest teardown function that runs after all tests are completed.
    
    This function performs aggressive cleanup of all automation processes
    to prevent memory issues and ensure no processes are left hanging.
    
    Args:
        session: The pytest session object
        exitstatus: The exit status of the test session
    """
    logger.info("Test session finished. Starting aggressive cleanup...")
    
    # Force cleanup all automation processes
    force_cleanup_all_automation_processes()
    
    # Additional memory cleanup
    try:
        import gc
        gc.collect()
        logger.info("Garbage collection completed.")
    except Exception as e:
        logger.warning(f"Error during garbage collection: {e}")
    
    logger.info("Session cleanup completed.")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    A pytest hook to generate and attach test execution reports.

    This hook wraps the test execution process to yield control back to pytest, 
    allowing the test report to be generated. The report is then attached to the 
    test item object with a dynamic attribute based on the test execution phase.

    If the test execution phase is 'call' and the test has failed, a screenshot 
    is captured from the selenium driver instance. The screenshot is saved with 
    a timestamped filename to a designated directory. The screenshot is then 
    attached to the Allure report for the test.

    Args:
        item: The pytest test item object, which represents the test function.
        call: The pytest call object, which contains information about the 
              test execution phase and result.
    """

    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    # attach screenshot if test failed
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            test_id = get_test_file_name(item.nodeid)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{test_id}_{timestamp}.png"            
            screenshot_path = os.path.join(SCREENSHOT_DIR, file_name)
            driver.save_screenshot(screenshot_path)

            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

@pytest.fixture(scope="function", autouse=True)
def record_screen(request):
    """
    A pytest fixture to record the screen during test execution.

    This fixture automatically records the screen for the duration of each test function.
    It starts recording before the test begins and stops recording after the test ends,
    saving the video to a specified directory. The video file is then attached to the
    Allure report for the test.

    Args:
        request: The pytest request object, which provides information about the
                 executing test function.

    Yields:
        None

    After the test function completes, the recording is stopped and attached to the
    Allure report as an MP4 file.
    """
    from config import ENABLE_VIDEO_RECORDING
    
    # Si la grabación de video está deshabilitada, no hacer nada
    if not ENABLE_VIDEO_RECORDING:
        yield
        return

    test_name = get_test_file_name(request.node.nodeid)
    video_path = os.path.join(VIDEO_DIR, f"{test_name}.mp4")

    recorder = pyscreenrec.ScreenRecorder()
    recorder.start_recording(video_path, fps=30)
    yield
    recorder.stop_recording()

    
    with open(video_path, "rb") as f:
        allure.attach(f.read(), name=test_name, attachment_type=allure.attachment_type.MP4)
   
def get_test_file_name(nodeid: str) -> str:
    
    """
    Returns the name of the test file without extension from a given nodeid.

    Args:
        nodeid (str): A pytest nodeid string.

    Returns:
        str: The name of the test file without extension.
    """
    path_part = nodeid.split("::")[0]  # 'tests/test_avtest_case_2.py'
    return os.path.splitext(os.path.basename(path_part))[0]



