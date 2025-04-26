import pytest
from utils.browser_factory import get_driver
from utils.db_utils import store_result, create_db

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
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use: chrome or firefox")

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
    driver = get_driver(browser_name)
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