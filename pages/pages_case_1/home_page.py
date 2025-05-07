from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from logger import get_logger
from utils.exception import catch_exceptions
from pages.common import Common

class HomePage(Common):
    # ----------------------------------LOCATORS----------------------------------------------------------
    #Loader that indicate that the page is loading.
    LOADER:                                         tuple = (By.XPATH, "//*[contains(@class, 'loader') or contains(@class, 'loading')]")
    #Loader that indicate that the page is loading in some cases.
    LOADER_B:                                       tuple = (By.CLASS_NAME, "page-loader")
    #Button that indicate the language selectioned 
    BUTTON_LANGUAGE:                                tuple = (By.XPATH, "//button[.//span[normalize-space(.)='{}']]")
    #Button to deploy the language options
    DEPLOY_LANGUAGE_BUTTON:                         tuple = (By.XPATH, "//button[contains(@id, 'languageListTriggerId')]") 
    #currency_button
    BUTTON_CURRENCY:                                tuple = (By.XPATH, "//*[contains(@id, 'pointOfSaleSelectorId')]")
    #Button _to deploy the currency options
    SELECT_CURRENCY_COUNTRY:                        tuple = (By.XPATH, "//*[@id= 'pointOfSaleListId']//*[@class= 'points-of-sale_list_item ng-star-inserted']//*[@class= 'points-of-sale_list_item_label' and contains(.,'{}')]")
    #Button to apply currency selection
    CONFIRM_CURRENCY_BUTTON:                        tuple = (By.XPATH, "//*[@class='button points-of-sale_footer_action_button']//*[@class='button_label']")
    #Radio button that indicate one way flight 
    RADIO_ONE_WAY:                                  tuple = (By.ID, "journeytypeId_1")
    #Button in the origin city field 
    BUTTON_ORIGIN:                                  tuple = (By.ID, "originBtn")
    #Input field of the origin city 
    FIELD_ORIGIN:                                   tuple = (By.XPATH, "//*[contains(@class,'control_field_input')]")
    #Search result of the origin city 
    OPTION_CITY_ORIGIN:                             tuple =  (By.XPATH, "//li[contains(@class, 'station-control-list_item')]//span[contains(@class, 'station-control-list_item_link-city') and contains(., '{}')]")
    #Input field of the destination city 
    FIELD_DESTINATION:                              tuple = (By.XPATH, "//*[contains(@class,'control_field control_field-inbound is-focused')]//*[@class='control_field_input']")
    #Search result of the destination city 
    OPTION_CITY_DESTINATION:                        tuple = (By.XPATH, "//li[contains(@class, 'station-control-list_item')]//span[contains(@class, 'station-control-list_item_link-city') and contains(., '{}')]")
    #Button to select the date  
    DATEPICKER_BUTTON:                              tuple = (By.XPATH, "//*[@id='ngbStartDatepickerId']/div[2]/div[2]/ngb-datepicker-month-view/div[2]/div[1]/span/div[1]")
    #DatePicker control month button
    DATEPICKER_CONTROL_MONTH_BUTTON:                tuple = (By.XPATH, "//*[@id='searchContentId_OW']/div[2]/date-control-custom/div/div[2]/div/div[2]/date-picker-custom/div/button[2]")
    # Deploy passengers
    DEPLOY_PASSENGERS_BUTTON:                       tuple = (By.XPATH, "//*[@class='control_field']")
    # Adult + button
    ADULT_PLUS_BUTTON:                              tuple = (By.XPATH, "//*[@id='paxControlSearchId']/div/div[2]/div/ul/li[1]/div[2]/ibe-minus-plus/div/button[2]")
    # Young + button
    YOUNG_PLUS_BUTTON:                              tuple = (By.XPATH, "//*[@id='paxControlSearchId']/div/div[2]/div/ul/li[2]/div[2]/ibe-minus-plus/div/button[2]")
    # Child + button
    CHILD_PLUS_BUTTON:                              tuple = (By.XPATH, "//*[@id='paxControlSearchId']/div/div[2]/div/ul/li[3]/div[2]/ibe-minus-plus/div/button[2]")
    # Infant + button
    INFANT_PLUS_BUTTON:                             tuple = (By.XPATH, "//*[@id='paxControlSearchId']/div/div[2]/div/ul/li[4]/div[2]/ibe-minus-plus/div/button[2]")
    #Confirm button
    CONFIRM_BUTTON:                                 tuple = (By.XPATH, "//*[@id='paxControlSearchId']/div/div[2]/div/div/button")
    #Search button
    SEARCH_BUTTON:                                  tuple = (By.ID, "searchButton")    
   
    def __init__(self, driver):
        """
        Initialize an HomePage instance.

        Args:
            driver (selenium.webdriver): A selenium webdriver instance.
        """       
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)

    @catch_exceptions()    
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
    
    @catch_exceptions() 
    def select_language(self, language):
        """
        Selects a language from the language dropdown.

        This method clicks on the language dropdown button, waits for the options to be
        clickable, and selects the specified language.

        Args:
            language (str): The language to select from the dropdown.
        """

        self.logger.info(f"Selecting language {language} in URL: {self.URL}")
        laguage_options =self.wait_to_be_clickable(self.DEPLOY_LANGUAGE_BUTTON)
        laguage_options.click()
        tuple_language = ( self.BUTTON_LANGUAGE[0],  self.BUTTON_LANGUAGE[1].format(language))
        button_language = self.wait_to_be_clickable(tuple_language)
        button_language.click()
        self.logger.info(f"Language {language} selected.")
    
    @catch_exceptions() 
    def select_currency(self, currency):
        """
        Selects a currency from the currency dropdown.

        This method clicks on the currency dropdown button, waits for the options to be
        clickable, and selects the specified currency.

        Args:
            currency (str): The currency to select from the dropdown.
        """
        if(currency == "Colombia"):
            self.logger.info(f"{currency} currency aleady selected")
        else:        
            self.logger.info(f"Selecting currency {currency}")
            self.driver.maximize_window()
            self.logger.info(f"Deploying currency options...")
            currency_options =self.wait_to_be_clickable(self.BUTTON_CURRENCY)
            currency_options.click()
            self.logger.info(f"Selecting currency from the list...")
            tuple_currency = ( self.SELECT_CURRENCY_COUNTRY[0],  self.SELECT_CURRENCY_COUNTRY[1].format(currency))
            
            button_currency = self.wait_to_be_clickable(tuple_currency)        
            button_currency.click()
            self.logger.info(f"Confirm currency {currency}")
            confirm_currency =self.wait_to_be_clickable(self.CONFIRM_CURRENCY_BUTTON)    

            confirm_currency.click()
            self.logger.info(f"Currency {currency} selected.")
    
    @catch_exceptions() 
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

    @catch_exceptions() 
    def select_origin(self, city_origin):         
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
         self._select_city_origin(self.FIELD_ORIGIN, city_origin)
         # Wait till the city option appears
         self.logger.info("Waiting for city option...")
         city= (self.OPTION_CITY_ORIGIN [0], self.OPTION_CITY_ORIGIN [1].format(city_origin))
         city_option = self.wait_to_be_clickable(city)
         # Click on the option selected
         city_option.click()
         self.logger.info("Origin city selected.") 

    @catch_exceptions() 
    def select_destination(self, city_destination):
        """
        Select the destination city in the page.

        Args:
            wait (selenium.webdriver.support.ui.WebDriverWait): A WebDriverWait instance.
            field_destination (tuple): A tuple of (By, str) to locate the destination field.
            option_city_destination (tuple): A tuple of (By, str) to locate the city option.
        """

        self.logger.info("Waiting for destination field...")
        time.sleep(0.5)   
        destination_input = self.find(self.FIELD_DESTINATION)      
  
        self._select_city_destination(city_destination, destination_input)
        
    @catch_exceptions() 
    def select_deaperture_date(self, day: str, month: str, year: str):
        self.logger.info("Selecting departure date...")

        # Delete leading zeros from date 
        day = str(int(day)).zfill(2)
        month = str(int(month)).zfill(2)
        year = str(year)

        # Format required by the input
        formatted_date = f"{day}/{month}/{year}"
        self.logger.info(f"Formatted deaperturedate to input: {formatted_date}")

        # Execute JS to remove readonly from input
        self.driver.execute_script("document.getElementById('departureInputDatePickerId').removeAttribute('readonly');")

        # Wait for input to be present
        input_elem =self.wait_for((By.ID, "departureInputDatePickerId"))
        

        # Clean and write the date
        input_elem.clear()
        input_elem.send_keys(formatted_date)

        self.logger.info("Departure date input completed.")

    @catch_exceptions() 
    def select_arrival_date(self, day: str, month: str, year: str):
        self.logger.info("Selecting arrival date...")

        # Delete leading zeros from date 
        day = str(int(day)).zfill(2)
        month = str(int(month)).zfill(2)
        year = str(year)

        # Format required by the input
        formatted_date = f"{day}/{month}/{year}"
        self.logger.info(f"Formatted arrival date to input: {formatted_date}")

        # Execute JS to remove readonly from input
        self.driver.execute_script("document.getElementById('arrivalInputDatePickerId').removeAttribute('readonly');")

        # Wait for input to be present
        input_elem =self.wait_for((By.ID, "arrivalInputDatePickerId"))
        

        # Clean and write the date
        input_elem.clear()
        input_elem.send_keys(formatted_date)

        self.logger.info("Arrival date input completed.")

    @catch_exceptions() 
    def click_plus_adult(self, times, wait_between_clicks=0.5):
        """
        Clicks multiple times on the same element.
        
        :param times: Number of times you want to click.
        :param wait_between_clicks: Wait time between clicks in seconds.
        """
        self.logger.info("Click on passengers button...")
        button = self.wait_to_be_clickable(self.DEPLOY_PASSENGERS_BUTTON)
        button.click()    

        self.logger.info(f"Adding {times} adults...")                    
        adultt_button = self.wait_to_be_clickable(self.ADULT_PLUS_BUTTON)          
        for _ in range(times - 1):
            adultt_button.click()            
            self.logger.info("Selecting adults.") 
            time.sleep(wait_between_clicks)

    @catch_exceptions() 
    def click_plus_young(self, times, wait_between_clicks=0.5):     
        """
        Clicks multiple times on the same element.
        
        :param times: Number of times you want to click.
        :param wait_between_clicks: Wait time between clicks in seconds.
        """
        self.logger.info(f"Adding {times} Young...")
        young_button = self.wait_to_be_clickable(self.YOUNG_PLUS_BUTTON)             
        for _ in range(times):            
            young_button.click()           
            self.logger.info("Selecting youngers.") 
            time.sleep(wait_between_clicks)

    @catch_exceptions() 
    def click_plus_child(self, times, wait_between_clicks=0.5):                  
        """
        Clicks multiple times on the same element.
        
        :param times: Number of times you want to click.
        :param wait_between_clicks: Wait time between clicks in seconds.
        """
        self.logger.info(f"Adding {times} child...")
        child_button = self.wait_to_be_clickable(self.CHILD_PLUS_BUTTON)      
                
        for _ in range(times):           
            child_button.click()
            self.logger.info("Selecting children.") 
            time.sleep(wait_between_clicks)

    @catch_exceptions() 
    def click_plus_infant(self, times, wait_between_clicks=0.5):                
        """
        Clicks multiple times on the same element.
        
        :param times: Number of times you want to click.
        :param wait_between_clicks: Wait time between clicks in seconds.
        """
        
        self.logger.info(f"Adding {times} infants...")
        baby_button = self.wait_to_be_clickable(self.INFANT_PLUS_BUTTON)      
                
        for _ in range(times):           
            baby_button.click()
            self.logger.info("Selecting infants.") 
            time.sleep(wait_between_clicks)

    @catch_exceptions() 
    def confirm_button_passengers_quantity(self):
        confirm_button = self.wait_to_be_clickable(self.CONFIRM_BUTTON)
        confirm_button.click()
        self.logger.info("Confirm button  passenger clicked.") 

    @catch_exceptions() 
    def click_search_flight_button(self):
        """
        Clicks the search flight button on the home page.

        This method waits for the search button to become clickable, 
        clicks it, and logs the action for tracking purposes.
        """
        search_button = self.wait_to_be_clickable(self.SEARCH_BUTTON)
        search_button.click()
        self.logger.info("Search button clicked.") 

    @catch_exceptions() 
    def is_one_way_selected(self):
        """
        Return True if the one way radio button is selected, False otherwise.
        """
        select_radio = self.find(self.RADIO_ONE_WAY)
        return select_radio.is_selected()   
                                                            
    @catch_exceptions() 
    def _select_city_destination(self, option_city_destination, destination_input):
        """
        Select the destination city in the page.

        Args:            
            option_city_destination (tuple): A tuple of (By, str) to locate the city option.
            destination_input (selenium.webdriver.remote.webelement.WebElement): The destination input field.
        """
        self.logger.info("Writing destination...") 
        destination_input.send_keys(option_city_destination)

        # Wait till the city option appears
        self.logger.info("Waiting for destination city option...")
        city= (self.OPTION_CITY_DESTINATION [0], self.OPTION_CITY_DESTINATION [1].format(option_city_destination))
        city_option = self.wait_to_be_clickable(city)

        # Click on the option        
        city_option.click()
        self.logger.info("Destination city selected.") 

    @catch_exceptions() 
    def _select_city_origin(self, field_city, city_name):
        """
        Select the origin city in the page.

        Args:
            field_city (tuple): A tuple of (By, str) to locate the origin field.
            city_name (str): The name of the city to select.
        """
        self.logger.info("Waiting for origin field...") 
        input_origin_city = self.find(field_city)
        self.logger.info("clicking on origin field...") 
        # Click on the input field
        # input_origin_city.click()
        # Write the city name
        input_origin_city.send_keys(city_name)
    
    @catch_exceptions() 
    def loader_a(self):
        self.wait_for_invisibility(self.LOADER)

    @catch_exceptions() 
    def loader_b(self):
        self.wait_for_invisibility(self.LOADER_B)




       
