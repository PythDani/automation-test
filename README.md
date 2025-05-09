
# Automated Web Testing Project with Selenium and Pytest

## 📑 Table of Contents
- [Introduction](#introduction)
- [Purpose](#purpose)
- [Installation](#installation)
  - [Windows](#windows)
  - [Linux](#linux)
  - [macOS](#macos)
- [Project Structure](#project-structure)
- [Page Object Model (POM)](#page-object-model-pom)
- [How It Works](#how-it-works)
- [Libraries Used](#libraries-used)
- [Setting up tests](#setting-up-tests)
- [Running the Tests](#running-the-tests)
- [Generating the Report](#generating-the-report)
- [Test Result Storage with SQLite](#test-result-storage-with-sqlite)

---

## Introduction

This repository contains a robust and scalable test automation framework for a flight booking web application using Python, Pytest, and Selenium. The design follows the Page Object Model (POM) and includes integration with Allure for reporting.

---

## Purpose

> This technical test aims to evaluate my skills in automated testing and the use of tools such as Selenium WebDriver with Python.

This automation framework is intended to showcase your understanding and application of modern testing tools and methodologies. It provides a scalable foundation for developing, executing, and reporting on end-to-end automated tests.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Git
- Google Chrome (or another supported browser)

Clone the repository:

```bash
git clone https://github.com/your-username/automation-test.git
cd automation-test
```

Create and activate a virtual environment:

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
automation-test/
├── conftest.py
├── config.py
├── logger.py
├── browser_factory.py
├── pytest.ini
├── test_results.db
├── test_log/
├── requirements.txt
├── .gitignore
├── pages/
│   ├── pages_case_1/
│   │   ├── home_page.py
│   │   ├── booking_select_page.py
│   │   ├── form_passengers_page.py
│   │   ├── services_page.py
│   │   ├── seat_map_page.py
│   │   ├── payment_page.py
│   │   └── itinerary_page.py
│   └── common.py
├── tests/
│   ├── test_avtest_case_1.py
│   ├── test_avtest_case_2.py
│   └── test_avtest_case_3.py
├── utils/
│   ├── db_utils.py
│   └── exception.py
├── allure-report/
├── allure-results/
├── videos/
├── screenshots/
└── .env
```

---

## Page Object Model (POM)

This project follows the **Page Object Model (POM)** design pattern. It promotes modular, reusable, and maintainable test code by encapsulating page-specific logic into separate classes.

Each page class:

- Represents a single page or component of the web application.
- Contains locators and methods that interact with the page.
- Is imported and used in test files to perform end-to-end user actions.

For instance:

```python
# Example: pages/pages_case_1/home_page.py

class HomePage:
  DEPLOY_PASSENGERS_BUTTON: tuple (By.XPATH, "//*[contains(@class,'control_field')]")
  ADULT_PLUS_BUTTON:        tuple = (By.XPATH, "//*[contains(@id,'paxControlSearchId')]")

    def __init__(self, driver):             
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)
    
    @catch_exceptions() 
    def click_plus_adult(self, times, wait_between_clicks=0.5):
        
        self.logger.info("Click on passengers button...")
        button = self.wait_to_be_clickable(self.DEPLOY_PASSENGERS_BUTTON)
        button.click()    

        self.logger.info(f"Adding {times} adults...")                    
        adultt_button = self.wait_to_be_clickable(self.ADULT_PLUS_BUTTON)          
        for _ in range(times - 1):
            adultt_button.click()            
            self.logger.info("Selecting adults.") 
            time.sleep(wait_between_clicks)
```

This structure allows changes in UI elements to be localized to page classes, reducing maintenance costs.

---

## How It Works

1. **Tests** are defined in the `tests/` directory and follow the Pytest naming convention.
2. **Pages** use the Page Object Model (POM) for abstraction and reuse. It separates tests from logic.
3. The **browser is initialized** using Selenium WebDriver via `browser_factory.py`.
4. Tests are run using **Pytest**, optionally in parallel using `pytest-xdist`.
5. **Allure** is used to generate interactive HTML test reports.
6. Screenshots and videos of test executions are saved for debugging purposes.

---

## Libraries Used

| Library               | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| selenium==4.31.0       | Web automation library to control browsers like Chrome or Firefox           |
| pytest                | Testing framework for writing and running test cases                        |
| allure-pytest         | Plugin to generate Allure test reports from pytest results                  |
| pytest-xdist          | Enables running tests in parallel using pytest                              |
| webdriver-manager     | Automatically downloads and manages browser drivers                         |
| python-dotenv         | Loads environment variables from a .env file                                |
| faker==24.8.0         | Generates fake data (e.g. names, addresses) for testing                     |
| pyscreenrec           | Library to record screen during test execution                              |
| selenium-wire         | Extension of Selenium to capture and modify HTTP requests and responses     |
| blinker==1.4          | Provides support for signal/event dispatching                               |
| setuptools==80.3.1    | Package development and distribution tool, required for many packages       |

---

## Setting up tests

In this project, test configurations and contextual setups are centralized in the `conftest.py` file. This structure ensures **modularity**, **scalability**, and **clear separation of concerns**, which are essential qualities in automated testing frameworks.

### 🔧 Fixtures for Context Initialization

Within `conftest.py`, three `@pytest.fixture`-decorated functions are defined, each responsible for providing the environment and parameters required for a specific test case scenario.

These fixtures initialize **Page Object Model (POM)** components and prepare input parameters to simulate user behavior for flight bookings. This design abstracts away the test setup from the test logic, improving test readability and reuse.

#### `booking_context(browser)`

Sets up the environment for **Case 1**: a basic one-way booking.  
Initializes page objects like `HomePage`, `FormPassengersPage`, `ServicesPage`, `SeatMapPage`, etc., along with test parameters like origin/destination cities, departure date, passenger count, etc.

```python

# e.g: conftest.py

@pytest.fixture(scope="function")
def booking_context(browser):   

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
            "arrival_date": {"day": "30", "month": "5", "year": "2025"},
            "passenger_count": 2,
            "young_count": 2,
            "child_count": 0,
            "baby_count": 0
        }
    }
```

#### `booking_context_case_2(browser)`

Sets up **Case 2**, involving a more complex booking scenario with additional parameters such as `relative_day`, and a dummy `a_credits_number` and `a_credits_pin`.

```python
# e.g: conftest.py

@pytest.fixture(scope="function")
def booking_context_case_2(browser): 

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
            "departure_date": {"day": "14", "month": "5", "year": "2025"},
            "arrival_date": {"day": "30", "month": "5", "year": "2025"},

            "passenger_count": 4,
            "young_count": 0,
            "child_count": 0,
            "baby_count": 0,
            "relative_day": "2 days before",
            "a_credits_number": "41414141414141414",
            "a_credits_pin": "111111",

        }
    }
```

#### `booking_context_case_3(browser)`

Initializes the booking flow for **Case 3**, extending the test input further with child, baby, and young passenger counts, and additional fields like `user_name` and `user_password`.

```python
# e.g: conftest.py

@pytest.fixture(scope="function")
def booking_context_case_3(browser): 


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
            "departure_date": {"day": "14", "month": "5", "year": "2025"},
            "arrival_date": {"day": "30", "month": "5", "year": "2025"},

            "passenger_count": 3,
            "young_count": 3,
            "child_count": 3,
            "baby_count": 3,
            "relative_day": "2 days before",
            "user_name": "1111111111",
            "user_password": "111111",
            "a_credits_number": "1111111111",
            "a_credits_pin": "1111111111",

        }
    }
```

Each fixture returns a `dict` structure that includes:
- Fully instantiated Page Object classes.
- Parameterized test data that guides the booking flow.

This approach enables each test to call a single fixture and access all required components without redefining the setup for each individual test.

NOTE: At this point we could have used only one configuration method and avoided repeating code, but for the sake of clarity, we decided to create all three.

###  Test Invocation and Modularity

Each test uses one of the above fixtures as a parameter, automatically injecting the test context thanks to Pytest's fixture resolution. Example:

```python
@allure.title("Automated case 1: One way booking")
@allure.severity(allure.severity_level.NORMAL)
def test_avtest_case_1(booking_context):
    page = booking_context["page"]
    form = booking_context["form"]
    services = booking_context["services"]
    seat_map = booking_context["seat_map"]
    payment_page = booking_context["payment_page"]
    booking_select_page = booking_context["booking_select_page"]
    itinerary_page = booking_context["itinerary_page"]
    params = booking_context["params"]

    with allure.step("Test Home page"):
        page.load()
        page.select_language(params["language"])
        page.select_currency(params["currency"])
        page.select_one_way_radio_button()
        page.select_origin(params["city_origin"])
        page.select_destination(params["city_destination"])
        page.select_deaperture_date(**params["departure_date"])
        page.click_plus_adult(times=params["passenger_count"])
        page.confirm_button_passengers_quantity()
        page.click_search_flight_button()

    page.loader_a()
    ...
```

This method improves:
- **Readability**: Each step is encapsulated and labeled using `allure.step(...)`.
- **Maintainability**: Common setups live in one place, easy to update when parameters or page flows change.
- **Reusability**: Multiple tests can share the same context or define specific ones when variations are needed.

This architecture aligns with industry-standard practices and is especially valuable when scaling the test suite for multiple scenarios.

## Running the Tests

To execute all test cases:

```bash
pytest tests/
```

To run tests in parallel (e.g. 3 workers):

```bash
pytest -n 3 tests/
```

To record the screen during test execution, ensure `pyscreenrec` is installed and properly configured in your test logic.

---

## Generating the Report

Generate the Allure test report after a test run:

This will open the report in your default browser. 

```bash
allure generate allure-results -o allure-report --clean
```

Open serve to see the reports

```bash
allure open allure-report
```

```bash
allure serve reports
```

---

## 📦 Test Result Storage with SQLite

This test framework also integrates a lightweight **SQLite** database to store the result of each test run.

### How It Works

- A file named `test_results.db` is used as the database.
- A table `test_results` is created (if it doesn't exist) using the utility function `create_db()` from `utils/db_utils.py`.
- Each time a test finishes, the result is saved automatically using the function `store_result()`.

The structure of the table is:

| Column     | Type      | Description                         |
|------------|-----------|-------------------------------------|
| id         | INTEGER   | Primary key                         |
| test_name  | TEXT      | The name of the test case           |
| result     | TEXT      | Result of the test ('passed', etc.) |
| timestamp  | DATETIME  | Automatically set to current time   |

```python
# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS test_results (
    id INTEGER PRIMARY KEY,
    test_name TEXT,
    result TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
  )
)
```
---