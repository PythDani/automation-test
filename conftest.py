import pytest
from pages.booking_select_page import BookingSelectPage
from pages.form_passengers_page import FormPassengersPage
from pages.home_page import HomePage
from pages.itinerary_page import ItineraryPage
from pages.payment_page import PaymentPage
from pages.seat_map_page import SeatMapPage
from pages.services_page import ServicesPage
from utils.browser_factory import get_driver
from utils.db_utils import store_result, create_db
from logger import get_logger
import logging

get_logger()
logger = logging.getLogger(__name__)
logger.info("Start pytest script")

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
            "departure_date": {"day": "14", "month": "5", "year": "2025"},
            "passenger_count": 2,
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

    browser_name = request.config.getoption("--browser")
    headless_option = request.config.getoption("--headless").lower() == "true"
    driver = get_driver(browser_name, headless_option)
    yield driver
    driver.quit()


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


