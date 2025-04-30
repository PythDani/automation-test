from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
from logger import get_logger
from .common import Common
class HomePage(Common):
    # ----------------------------------LOCATORS----------------------------------------------------------
    #Loader that indicate that the page is loading.
    LOADER:                                         tuple = (By.CLASS_NAME, "loader")
    #Loader that indicate that the page is loading in some cases.
    LOADER_B:                                       tuple = (By.CLASS_NAME, "page-loader")
    #Button that indicate the language selectioned 
    BUTTON_LANGUAGE:                                tuple = (By.XPATH, "//span[@class='dropdown_trigger_value' and contains(text(), 'Español')]") 
    #Radio button that indicate one way flight 
    RADIO_ONE_WAY:                                  tuple = (By.ID, "journeytypeId_1")
    #Button in the origin city field 
    BUTTON_ORIGIN:                                  tuple = (By.ID, "originBtn")
    #Input field of the origin city 
    FIELD_ORIGIN:                                   tuple = (By.XPATH, "//input[@class='control_field_input' and @placeholder='Origen']")
    #Search result of the origin city 
    OPTION_CITY_ORIGIN:                             tuple = (By.XPATH, "//li[contains(@class, 'station-control-list_item')]//span[contains(@class, 'station-control-list_item_link-city') and contains(., 'Medellín')]")
    #Input field of the destination city 
    FIELD_DESTINATION:                              tuple = (By.XPATH, "//input[@class='control_field_input' and @placeholder='Hacia']")
    #Search result of the destination city 
    OPTION_CITY_DESTINATION:                        tuple = (By.XPATH, "//li[contains(@class, 'station-control-list_item')]//span[contains(@class, 'station-control-list_item_link-city') and contains(., 'Bogotá')]")
    #Button to select the date  
    DATEPICKER_BUTTON:                              tuple = (By.XPATH, "//*[@id='ngbStartDatepickerId']/div[2]/div[2]/ngb-datepicker-month-view/div[2]/div[1]/span/div[1]")
    #DatePicker control month button
    DATEPICKER_CONTROL_MONTH_BUTTON:                tuple = (By.XPATH, "//*[@id='searchContentId_OW']/div[2]/date-control-custom/div/div[2]/div/div[2]/date-picker-custom/div/button[2]")
    #  Adult + button
    ADULT_PLUS_BUTTON:                              tuple = (By.XPATH, "//*[@id='paxControlSearchId']/div/div[2]/div/ul/li[1]/div[2]/ibe-minus-plus/div/button[2]")
    #Confirm button
    CONFIRM_BUTTON:                                 tuple = (By.XPATH, "//*[@id='paxControlSearchId']/div/div[2]/div/div/button")
    #Search button
    SEARCH_BUTTON:                                  tuple = (By.ID, "searchButton")
    #Flight button
    FLIGHT_BUTTON:                                  tuple = (By.XPATH, "//button[contains(@class, 'journey_price_button') and .//span[contains(text(), 'Seleccionar de tarifa')]]")
    # BASIC_FARE_BUTTON 
    BASIC_FARE_BUTTON:                              tuple = (By.XPATH, "//div[@role='button' and contains(@class, 'fare-control') and .//span[contains(text(), 'basic')]]")
    # Continue button
    CONTINUE_BUTTON:                                tuple = (By.XPATH, "//*[@id='maincontent']/div/div[2]/div/div/button-container/div/div/button")
   
    def __init__(self, driver):
        """
        Initialize an HomePage instance.

        Args:
            driver (selenium.webdriver): A selenium webdriver instance.
        """       
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)
        
    def load(self):
        """
        load home page.

        """
        try:
            self.logger.info(f"Loading URL: {self.URL}")
            self.driver.get(self.URL)    
            #We wait unitll the page loader disapear.
            self.logger.info("Waiting for page to load disappear...")
            self.wait_for_invisibility(self.LOADER)
            self.logger.info("Page loaded correctly.")
        except TimeoutException as e:
            raise Exception(f"Timeout Exception trying to load {self.__class__.__name__}") from e    

    def loader_b(self):
        self.wait_for_invisibility(self.LOADER_B)

    def loader_a(self):
        self.wait_for_invisibility(self.LOADER)

    def button_continue_to_move_to_passenger_form(self):
        continue_button = self.find(self.CONTINUE_BUTTON)

        #Scroll down to move to the button       
        ActionChains(self.driver).move_to_element(continue_button).perform()              
        continue_button.click()
        self.logger.info("Button continue clicked.") 

    def click_on_fare_flight(self):
        basic_fare_button = self.wait_to_be_clickable(self.BASIC_FARE_BUTTON)        
        ActionChains(self.driver).move_to_element(basic_fare_button).perform()        
        basic_fare_button.click()
        self.logger.info("Fee selected") 

    def click_drop_down_flight(self):
        flight_button = self.wait_to_be_clickable(self.FLIGHT_BUTTON)        
        ActionChains(self.driver).move_to_element(flight_button).perform()        
        flight_button.click()
        self.logger.info("Flight selected") 
        time.sleep(3)

    def click_search_flight_button(self):
        search_button = self.wait_to_be_clickable(self.SEARCH_BUTTON)
        search_button.click()
        self.logger.info("Search button clicked.") 

    def confirm_button_passengers_quantity(self):
        confirm_button = self.wait_to_be_clickable(self.CONFIRM_BUTTON)
        confirm_button.click()
        self.logger.info("Confirm button  passenger clicked.") 

    def select_date_departure(self):
        """
        Selects the departure date by clicking on the date picker button.

        Logs the actions performed, and raises an exception if the button
        is not found or clickable within the timeout period.
        """
        try:
            self.logger.info("Clicking on date picker button...")
            day_element = self.wait_to_be_clickable(self.DATEPICKER_BUTTON)
            day_element.click()       
            self.logger.info("Departure date selected")
        except TimeoutException as e:
            raise Exception("Timeout Exception trying to select departure date") from e

    def select_one_way_radio_button(self):
        """
        Select the one way radio button in the page.

        If the radio button is not selected, it will be clicked.
        """
        self.logger.info("Waiting visibility of one way radio button...")
        self.wait_for(self.RADIO_ONE_WAY)
        self.logger.info("Waiting clickability of one way radio button...")
        self.wait_for(self.RADIO_ONE_WAY)
        self.logger.info("Selecting one way radio button...")
        select_radio = self.wait_for(self.RADIO_ONE_WAY)
        if not select_radio.is_selected():            
            select_radio.click()
            self.logger.info("One way radio button selected.") 

    def is_one_way_selected(self):
        """
        Return True if the one way radio button is selected, False otherwise.
        """
        select_radio = self.find(self.RADIO_ONE_WAY)
        return select_radio.is_selected()   
                                                            
    def select_origin(self):
        """
        Select the origin city in the page.

        Args:
            wait (selenium.webdriver.support.ui.WebDriverWait): A WebDriverWait instance.
            button_origin (tuple): A tuple of (By, str) to locate the origin button.
            field_origin (tuple): A tuple of (By, str) to locate the origin field.
            option_city_origin (tuple): A tuple of (By, str) to locate the city option.
        """
        self.logger.info("Waiting for origin button...") 
        origin_button = self.find(self.BUTTON_ORIGIN)
        origin_button.click()
        self.logger.info("Origin button clicked") 

        self.select_city_origin(self.FIELD_ORIGIN, "Medellín")

        # Wait till the city option appears
        self.logger.info("Waiting for city option...") 
        city_option = self.wait_to_be_clickable(self.OPTION_CITY_ORIGIN)

        # Click on the option selected
        city_option.click()
        self.logger.info("Origin city selected.") 

    def select_destination(self):
        """
        Select the destination city in the page.

        Args:
            wait (selenium.webdriver.support.ui.WebDriverWait): A WebDriverWait instance.
            field_destination (tuple): A tuple of (By, str) to locate the destination field.
            option_city_destination (tuple): A tuple of (By, str) to locate the city option.
        """

        self.logger.info("Waiting for destination field...") 
        destination_input = self.wait_to_be_clickable(self.FIELD_DESTINATION)
        
        self.logger.info("Clearing destination field...") 
        destination_input.clear()

        self.select_city_destination(self.OPTION_CITY_DESTINATION, destination_input)

    def select_city_destination(self, option_city_destination, destination_input):
        """
        Select the destination city in the page.

        Args:            
            option_city_destination (tuple): A tuple of (By, str) to locate the city option.
            destination_input (selenium.webdriver.remote.webelement.WebElement): The destination input field.
        """
        self.logger.info("Writing destination...") 
        destination_input.send_keys("Bogotá")

        # Wait till the city option appears
        self.logger.info("Waiting for destination city option...") 
        city_option = self.wait_to_be_clickable(option_city_destination)

        # Click on the option        
        city_option.click()
        self.logger.info("Destination city selected.") 

    def select_city_origin(self, field_city, city_name):
        """
        Select the origin city in the page.

        Args:
            field_city (tuple): A tuple of (By, str) to locate the origin field.
            city_name (str): The name of the city to select.
        """
        self.logger.info("Waiting for origin field...") 
        input_origin_city = self.find(field_city)

        # Click on the input field
        input_origin_city.click()
        # Write the city name
        input_origin_city.send_keys(city_name)

    def click_plus_adult(self, times, wait_between_clicks=0.5):
        """
        Clicks multiple times on the same element.
        
        :param times: Number of times you want to click.
        :param wait_between_clicks: Wait time between clicks in seconds.
        """
        element = self.wait_to_be_clickable(self.ADULT_PLUS_BUTTON)                
        
        for _ in range(times - 1):
            element.click()
            self.logger.info("Selecting passenger.") 
            time.sleep(wait_between_clicks)

    def select_random_month(self, times=1, wait_between_clicks=0.5):
        """
        Clicks multiple times on the same element.

        :param locator: Your type locator (By.XPATH, "xpath of the button")
        :param times: Number of times you want to click.
        :param wait_between_clicks: Wait time between clicks in seconds.
        """
        element = self.wait_to_be_clickable(self.DATEPICKER_CONTROL_MONTH_BUTTON)        
        
        for _ in range(times):
            element.click()
            self.logger.info("Selecting departure month.") 
            time.sleep(wait_between_clicks)





       
