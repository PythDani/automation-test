from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import HOME_URL 

class AvtestPage:
    # URL=HOME_URL
    BUTTON_LANGUAGE = (By.XPATH, "//span[@class='dropdown_trigger_value' and contains(text(), 'Español')]") #languageListTriggerId_17
    RADIO_ONE_WAY = (By.ID, "journeytypeId_1")
    BUTTON_ORIGIN = (By.ID, "originBtn")
    FIELD_ORIGIN = (By.XPATH, "//input[@class='control_field_input' and @placeholder='Origen']")
    OPTION_CITY_ORIGIN = (By.XPATH, "//li[contains(@class, 'station-control-list_item')]//span[contains(@class, 'station-control-list_item_link-city') and contains(., 'Medellín')]")
    BUTTON_DESTINATION = (By.XPATH, "//div[contains(@class,'control_field-inbound')]//button[contains(@class,'control_field_button')]")
    FIELD_DESTINATION = (By.XPATH, "//input[@class='control_field_input' and @placeholder='Hacia']")
    OPTION_CITY_DESTINATION = (By.XPATH, "//li[contains(@class, 'station-control-list_item')]//span[contains(@class, 'station-control-list_item_link-city') and contains(., 'Bogotá')]")
    def __init__(self, driver):
        """
        Initialize an AvtestPage instance.

        Args:
            driver (selenium.webdriver): A selenium webdriver instance.
        """

        self.driver = driver
        self.URL = HOME_URL

    def load(self):
        """
        load home page.

        """
        print(f"URL a la que vamos a navegar: {self.URL}")
        self.driver.get(self.URL)
        wait = WebDriverWait(self.driver, 10) # We wait 10 secodns untill the page load completely.
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "page-loader"))) #We wait unitll the page loader disapear.
    
    
    def select_one_way_flight(self):
        
        wait = WebDriverWait(self.driver, 10)
        language_button = self.driver.find_element(*self.BUTTON_LANGUAGE) #Select the language button.
        assert "Español" in language_button.text, "El idioma no está en Español" #Validate if the language is Spanish.
        select_radio = self.driver.find_element(*self.RADIO_ONE_WAY)
        if not select_radio.is_selected():
            select_radio.click()
       # --- SELECT ORIGEN ---
        self.select_origin(wait, self.BUTTON_ORIGIN, self.FIELD_ORIGIN, self.OPTION_CITY_ORIGIN)
       # --- SELECT DESTINATION ---
        self.select_destination(wait, self.FIELD_DESTINATION, self.OPTION_CITY_DESTINATION)

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

        self.select_city(field_origin, "Medellín")

        # Wait till the city option appears
        print("Esperando la opción de Medellín en la lista...")
        city_option = wait.until(EC.element_to_be_clickable(option_city_origin))

        # Click on the option
        city_option.click()
        print("Opción 'Medellín' seleccionada.")

    def select_destination(self, wait, field_destination, option_city_destination):
        print("Esperando que el campo de destino esté disponible...")
        destination_input = wait.until(EC.visibility_of_element_located(field_destination))
        
        print("Limpiando campo de destino...")
        destination_input.clear()

        print("Escribiendo 'Bogotá' en el campo de destino...")
        destination_input.send_keys("Bogotá")

        # Esperar que aparezca la opción "Bogotá" en la lista de sugerencias
        print("Esperando que aparezca la opción de 'Bogotá' en la lista...")
        city_option = wait.until(EC.element_to_be_clickable(option_city_destination))

        # Hacer click en la opción de la ciudad
        print("Seleccionando la opción 'Bogotá'...")
        city_option.click()
        print("Ciudad de destino 'Bogotá' seleccionada exitosamente.")


    def select_city(self, field_city, city_name):
        """
        Select the origin city in the page.

        Args:
            field_city (tuple): A tuple of (By, str) to locate the origin field.
            city_name (str): The name of the city to select.
        """
        print("Esperando que el campo de origen esté visible...")
        input_origin_city = self.driver.find_element(*field_city)

        # Ahora sí click, limpiar y escribir
        input_origin_city.click()
        input_origin_city.send_keys(city_name)





       
