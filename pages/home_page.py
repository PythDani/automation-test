from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import HOME_URL
import time
class HomePage:
    # ----------------------------------LOCATORS----------------------------------------------------------
    #Button that indicate the language selectioned 
    BUTTON_LANGUAGE = (By.XPATH, "//span[@class='dropdown_trigger_value' and contains(text(), 'Español')]") 
    #Radio button that indicate one way flight 
    RADIO_ONE_WAY = (By.ID, "journeytypeId_1")
    #Button in the origin city field 
    BUTTON_ORIGIN = (By.ID, "originBtn")
    #Input field of the origin city 
    FIELD_ORIGIN = (By.XPATH, "//input[@class='control_field_input' and @placeholder='Origen']")
    #Search result of the origin city 
    OPTION_CITY_ORIGIN = (By.XPATH, "//li[contains(@class, 'station-control-list_item')]//span[contains(@class, 'station-control-list_item_link-city') and contains(., 'Medellín')]")
    #Input field of the destination city 
    FIELD_DESTINATION = (By.XPATH, "//input[@class='control_field_input' and @placeholder='Hacia']")
    #Search result of the destination city 
    OPTION_CITY_DESTINATION = (By.XPATH, "//li[contains(@class, 'station-control-list_item')]//span[contains(@class, 'station-control-list_item_link-city') and contains(., 'Bogotá')]")
    #Button to select the date  
    DATEPICKER_BUTTON = (By.XPATH, "//*[@id='ngbStartDatepickerId']/div[2]/div[1]/ngb-datepicker-month-view/div[2]/div[5]")
    #DatePicker control month button
    DATEPICKER_CONTROL_MONTH_BUTTON = (By.XPATH, "//*[@id='searchContentId_OW']/div[2]/date-control-custom/div/div[2]/div/div[2]/date-picker-custom/div/button[2]")
    #  Adult + button
    ADULT_PLUS_BUTTON = (By.XPATH, "//*[@id='paxControlSearchId']/div/div[2]/div/ul/li[1]/div[2]/ibe-minus-plus/div/button[2]")
    #Confirm button
    CONFIRM_BUTTON = (By.XPATH, "//*[@id='paxControlSearchId']/div/div[2]/div/div/button")
    #Search button
    SEARCH_BUTTON = (By.ID, "searchButton")
    def __init__(self, driver):
        """
        Initialize an HomePage instance.

        Args:
            driver (selenium.webdriver): A selenium webdriver instance.
        """
        # We initialize the driver
        self.driver = driver
        #We load the home page url
        self.URL = HOME_URL

    def load(self):
        """
        load home page.

        """
        print(f"URL a la que vamos a navegar: {self.URL}")
        self.driver.get(self.URL)
        # We wait 10 secodns untill the page load completely.
        wait = WebDriverWait(self.driver, 10) 
        #We wait unitll the page loader disapear.
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "page-loader"))) 
    
    
    def select_one_way_flight(self):
        
        """
        Tests that we do when we have one way booking scenario

        """
        
        wait = WebDriverWait(self.driver, 10)
        #Select the language button.
        language_button = self.driver.find_element(*self.BUTTON_LANGUAGE) 
        #Validate if the language is Spanish.
        assert "Español" in language_button.text, "El idioma no está en Español" 
        select_radio = self.driver.find_element(*self.RADIO_ONE_WAY)
        if not select_radio.is_selected():
            select_radio.click()

       # Select Origin city
        self.select_origin(wait, self.BUTTON_ORIGIN, self.FIELD_ORIGIN, self.OPTION_CITY_ORIGIN)

       # Select destination city 
        self.select_destination(wait, self.FIELD_DESTINATION, self.OPTION_CITY_DESTINATION)

        #Select a month randomly
        self.click_multiple_times(self.DATEPICKER_CONTROL_MONTH_BUTTON, 3)    

        # Click on the datepicker button.
        day_element = wait.until(EC.element_to_be_clickable((self.DATEPICKER_BUTTON)))
        day_element.click()
        # print(day_element.text)
        print("Fecha 02/05/2025 seleccionada.")        

        #Select 3 adults 
        self.click_multiple_times(self.ADULT_PLUS_BUTTON, 1)

        # Confirm button and click
        confirm_button = wait.until(EC.element_to_be_clickable((self.CONFIRM_BUTTON)))
        confirm_button.click()
        print("Confirmado.")        

        #Click on search button
        search_button = wait.until(EC.element_to_be_clickable((self.SEARCH_BUTTON)))
        search_button.click()
        print("Busqueda realizada.")
        time.sleep(10)
                                                                        

    def select_origin(self, wait, button_origin, field_origin, option_city_origin):
        """
        Select the origin city in the page.

        Args:
            wait (selenium.webdriver.support.ui.WebDriverWait): A WebDriverWait instance.
            button_origin (tuple): A tuple of (By, str) to locate the origin button.
            field_origin (tuple): A tuple of (By, str) to locate the origin field.
            option_city_origin (tuple): A tuple of (By, str) to locate the city option.
        """
        print("Esperando que el botón de origen esté disponible...")
        origin_button = self.driver.find_element(*button_origin)
        origin_button.click()
        print("Botón de origen clickeado.")

        self.select_city_origin(field_origin, "Medellín")

        # Wait till the city option appears
        print("Esperando la opción de Medellín en la lista...")
        city_option = wait.until(EC.element_to_be_clickable(option_city_origin))

        # Click on the option
        city_option.click()
        print("Opción 'Medellín' seleccionada.")

    def select_destination(self, wait, field_destination, option_city_destination):
        """
        Select the destination city in the page.

        Args:
            wait (selenium.webdriver.support.ui.WebDriverWait): A WebDriverWait instance.
            field_destination (tuple): A tuple of (By, str) to locate the destination field.
            option_city_destination (tuple): A tuple of (By, str) to locate the city option.
        """

        print("Esperando que el campo de destino esté disponible...")
        destination_input = wait.until(EC.visibility_of_element_located(field_destination))
        
        print("Limpiando campo de destino...")
        destination_input.clear()

        self.select_city_destination(wait, option_city_destination, destination_input)

    def select_city_destination(self, wait, option_city_destination, destination_input):
        """
        Select the destination city in the page.

        Args:
            wait (selenium.webdriver.support.ui.WebDriverWait): A WebDriverWait instance.
            option_city_destination (tuple): A tuple of (By, str) to locate the city option.
            destination_input (selenium.webdriver.remote.webelement.WebElement): The destination input field.
        """
        print("Escribiendo 'Bogotá' en el campo de destino...")
        destination_input.send_keys("Bogotá")

        # Wait till the city option appears
        print("Esperando que aparezca la opción de 'Bogotá' en la lista...")
        city_option = wait.until(EC.element_to_be_clickable(option_city_destination))

        # Click on the option
        print("Seleccionando la opción 'Bogotá'...")
        city_option.click()
        print("Ciudad de destino 'Bogotá' seleccionada exitosamente.")


    def select_city_origin(self, field_city, city_name):
        """
        Select the origin city in the page.

        Args:
            field_city (tuple): A tuple of (By, str) to locate the origin field.
            city_name (str): The name of the city to select.
        """
        print("Esperando que el campo de origen esté visible...")
        input_origin_city = self.driver.find_element(*field_city)

        # Clear the input field
        input_origin_city.click()
        input_origin_city.send_keys(city_name)

    def click_multiple_times(self, locator, times=1, wait_between_clicks=0.5):
        """
        Clicks multiple times on the same element.

        :param locator: Your type locator (By.XPATH, "xpath of the button")
        :param times: Number of times you want to click.
        :param wait_between_clicks: Wait time between clicks in seconds.
        """
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
        
        for _ in range(times):
            element.click()
            time.sleep(wait_between_clicks)





       
