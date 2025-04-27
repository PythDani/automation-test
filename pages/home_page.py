from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from config import HOME_URL
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
    #Flight button
    FLIGHT_BUTTON = (By.XPATH, "//button[contains(@class, 'journey_price_button') and .//span[contains(text(), 'Seleccionar de tarifa')]]")
    # BASIC_FARE_BUTTON 
    BASIC_FARE_BUTTON = (By.XPATH, "//div[@role='button' and contains(@class, 'fare-control') and .//span[contains(text(), 'basic')]]")
    # Continue button
    CONTINUE_BUTTON = (By.XPATH, "//*[@id='maincontent']/div/div[2]/div/div/button-container/div/div/button")

    #------------------------------------------PASSENGERS----------------------------------------------------
    #Container first passenger
    CONTAINER_FIRST_PASSENGER = (By.XPATH, "//*[@id='maincontent']/div/div[3]/div/div/passenger-details-container/personal-data-custom/div/div/div[1]/personal-data-form-custom")    
    #Container passenger group
    CONTAINERS_PASSENGERS = (By.XPATH, "//personal-data-form-custom")
    # Genre selector"
    GENRE_SELECTOR = (By.XPATH, "//button[@role='combobox' and @aria-haspopup='listbox']")
    # Male button option
    BUTTON_MALE_OPTION = (By.XPATH, "//li[@class='ui-dropdown_item ng-star-inserted']//button[@class='ui-dropdown_item_option']")
    # Input name field
    INPUT_NAME = (By.XPATH, "//div[@class='ui-input_wrap']//input[@name='IdFirstName7E7E303030312D30312D30317E353334423438324433313244343535383534']")
    # Input last name field
    INPUT_LAST_NAME = (By.XPATH, "//div[@class='ui-input_wrap']//input[@name='IdLastName7E7E303030312D30312D30317E353334423438324433313244343535383534']")
    #Selector day of birth
    SELECTOR_DAY_OF_BIRTH = (By.XPATH, "//div[@class='ui-dropdown ng-star-inserted']//button[@class='ui-input' and @role='combobox' and @id='dateDayId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_']")
    # Day of birth button
    DAY_OF_BIRTH_BUTTON = (By.XPATH, "//li[@class='ui-dropdown_item ng-star-inserted' and @role='none']//button[@class='ui-dropdown_item_option' and @role='option' and @id='dateDayId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_-26']//span[text()='27']")
    #Selector month of birth
    SELECTOR_MONTH_OF_BIRTH = (By.XPATH, "//div[@class='ui-dropdown ng-star-inserted']//button[@class='ui-input' and @role='combobox' and @id='dateMonthId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_']")
    # Month of birth button
    MONTH_OF_BIRTH_BUTTON = (By.XPATH, "//li[@class='ui-dropdown_item ng-star-inserted' and @role='none']//button[@class='ui-dropdown_item_option' and @role='option' and @id='dateMonthId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_-7']//span[text()='8']")
    #Selector year of birth
    SELECTOR_YEAR_OF_BIRTH = (By.XPATH, "//div[@class='ui-dropdown ng-star-inserted']//button[@class='ui-input' and @role='combobox' and @id='dateYearId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_']")
    # Year of birth button
    YEAR_OF_BIRTH_BUTTON = (By.XPATH, "//li[contains(@class, 'ui-dropdown_item') and contains(@class, 'ng-star-inserted')]//button[contains(@class, 'ui-dropdown_item_option')]//span[text()='2000']")
    # Selector of Nationality
    SELECTOR_OF_NATIONALITY= (By.ID, "IdDocNationality_7E7E303030312D30312D30317E353334423438324433313244343535383534")
    # Nationality button
    NATIONALITY_BUTTON = (By.ID, "IdDocNationality_7E7E303030312D30312D30317E353334423438324433313244343535383534-0")

    #-----------------------------------------------Booking owner-----------------------------------------------------
    # Phone prefix selector
    PHONE_PREFIX_SELECTOR = (By.ID, "phone_prefixPhoneId")
    # Phone prefix button
    PHONE_PREFIX_BUTTON = (By.ID, "phone_prefixPhoneId-0")
    #Input phone number owner
    INPUT_PHONE_NUMBER_OWNER = (By.XPATH, "//input[@id='phone_phoneNumberId']")
    # Input email owner
    INPUT_EMAIL_OWNER = (By.XPATH, "//input[@id='email']")
    # Input confirm email owner
    INPUT_CONFIRM_EMAIL_OWNER = (By.XPATH, "//input[@id='confirmEmail']")
    #CHECKBOX
    CHECK_BOX = (By.XPATH, "//input[@id='sendNewsLetter']")
    # Button Continue
    BUTTON_CONTINUE = (By.XPATH, "//button[contains(@class, 'btn-next')]//span[text()='Continuar']")

    # Email selector

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

        #Select 1 adults 
        self.click_multiple_times(self.ADULT_PLUS_BUTTON, 1)

        # Confirm button and click
        confirm_button = wait.until(EC.element_to_be_clickable((self.CONFIRM_BUTTON)))
        confirm_button.click()
        print("Confirmado.")        

        #Click on search button
        search_button = wait.until(EC.element_to_be_clickable((self.SEARCH_BUTTON)))
        search_button.click()
        print("Busqueda realizada.")

        #We wait unitll the page loader disapear.
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "page-loader")))         

        #Click on flight selected button
        flight_button = wait.until(EC.element_to_be_clickable(self.FLIGHT_BUTTON))        
        ActionChains(self.driver).move_to_element(flight_button).perform()        
        flight_button.click()
        print("Vuelo seleccionado.")
        time.sleep(3)

        #Click on basic fare button
        basic_fare_button = wait.until(EC.element_to_be_clickable(self.BASIC_FARE_BUTTON))        
        ActionChains(self.driver).move_to_element(basic_fare_button).perform()        
        basic_fare_button.click()
        print("Tarifa seleccionada.")

        #We wait unitll the page loader disapear.
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "page-loader")))

        #Click on continue button
        continue_button = self.driver.find_element(*(self.CONTINUE_BUTTON))

        #Scroll down to move to the button       
        ActionChains(self.driver).move_to_element(continue_button).perform()              
        continue_button.click()
        print("Continuar.")

        #We wait unitll the page loader disapear.
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "page-loader")))

        #-----------------Fill out PASSENGERS form---------------------
        #Find container first passenger
        container_first_passenger = self.driver.find_element(*(self.CONTAINER_FIRST_PASSENGER))
        ActionChains(self.driver).move_to_element(container_first_passenger).perform()

        # All forms passengers
        passenger_forms = self.driver.find_elements(*(self.CONTAINERS_PASSENGERS))       
        print(f"Se encontraron {len(passenger_forms)} formularios de pasajeros.")

        for index, form in enumerate(passenger_forms, start=1):
            print(f"Llenando pasajero #{index}...")
            ActionChains(self.driver).move_to_element(form).perform()

            # --- Dentro del contenedor 'form' ---
            # Click genre selector
            genre_selector = form.find_element(By.XPATH, ".//button[@role='combobox' and @aria-haspopup='listbox']")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", genre_selector)
            wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@role='combobox' and @aria-haspopup='listbox']")))
            genre_selector.click()
            
            option_male = wait.until(EC.element_to_be_clickable(self.BUTTON_MALE_OPTION))
            option_male.click()

            # Input first name
            input_name = form.find_element(By.XPATH, ".//div[@class='ui-input_wrap']//input[contains(@name, 'IdFirstName')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_name)
            wait.until(EC.visibility_of(input_name))
            input_name.send_keys(f"Andres")

            # Input last name
            input_last_name = form.find_element(By.XPATH, ".//div[@class='ui-input_wrap']//input[contains(@name, 'IdLastName')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_last_name)
            wait.until(EC.visibility_of(input_last_name))
            input_last_name.send_keys(f"Perez")

            # Day of birth
            day_of_birth = form.find_element(By.XPATH, ".//button[contains(@id, 'dateDayId_IdDateOfBirthHidden')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", day_of_birth)
            # wait.until(EC.element_to_be_clickable(day_of_birth))
            day_of_birth.click()

            if index == 1:
                day_of_birth_option = wait.until(EC.element_to_be_clickable(self.DAY_OF_BIRTH_BUTTON))
                day_of_birth_option.click()
            else:
                day_of_birth_option = form.find_element(By.ID, "dateDayId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433323244343535383534_-26")
                day_of_birth_option.click()

            # Month of birth
            month_of_birth = form.find_element(By.XPATH, ".//button[contains(@id, 'dateMonthId_IdDateOfBi" \
            "rthHidden')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", month_of_birth)
            wait.until(EC.element_to_be_clickable(month_of_birth))
            month_of_birth.click()

            if index == 1:
                month_of_birth_option = wait.until(EC.element_to_be_clickable(self.MONTH_OF_BIRTH_BUTTON))
                month_of_birth_option.click()
            else:
                month_of_birth_option = form.find_element(By.ID, "dateMonthId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433323244343535383534_-7")
                month_of_birth_option.click()

            # Year of birth
            year_of_birth = form.find_element(By.XPATH, ".//button[contains(@id, 'dateYearId_IdDateOfBirthHidden')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", year_of_birth)
            wait.until(EC.element_to_be_clickable(year_of_birth))
            year_of_birth.click()

            year_of_birth_option = wait.until(EC.element_to_be_clickable(self.YEAR_OF_BIRTH_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", year_of_birth_option)
            year_of_birth_option.click()
           

            # Nationality
            if index == 1:
                nationality = form.find_element(*self.SELECTOR_OF_NATIONALITY)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nationality)
                wait.until(EC.visibility_of(nationality))
                nationality.click()

                nationality_option = wait.until(EC.element_to_be_clickable(self.NATIONALITY_BUTTON))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nationality_option)
                nationality_option.click()
            else:
                nationality = form.find_element(By.ID, "IdDocNationality_7E7E303030312D30312D30317E353334423438324433323244343535383534")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nationality)
                wait.until(EC.visibility_of(nationality))
                nationality.click()

                nationality_option = form.find_element(By.ID, "IdDocNationality_7E7E303030312D30312D30317E353334423438324433323244343535383534-0")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nationality_option)
                nationality_option.click()

            print(f"Pasajero #{index} llenado.")
        
        # Click on prefix button to show prefix phone list
        prefix_button = wait.until(EC.element_to_be_clickable(self.PHONE_PREFIX_SELECTOR))
        prefix_button.click()
        time.sleep(3)
        print("Listado de prefixes mostrado.")

        # Select prefix
        prefix_option = wait.until(EC.element_to_be_clickable(self.PHONE_PREFIX_BUTTON))
        prefix_option.click()
        print("Prefix seleccionado.")

        # Input phone number owner
        input_phone_number_owner = form.find_element(*self.INPUT_PHONE_NUMBER_OWNER)
        wait.until(EC.visibility_of(input_phone_number_owner))
        ActionChains(self.driver).move_to_element(input_phone_number_owner).perform()
        input_phone_number_owner.send_keys("3165555888")
        print("Número de telefono ingresado.")

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Input email owner
        input_email_owner = form.find_element(*self.INPUT_EMAIL_OWNER)
        wait.until(EC.visibility_of(input_email_owner))
        ActionChains(self.driver).move_to_element(input_email_owner).perform()
        input_email_owner.send_keys(f"andres{index}@gmail.com")
        print("Correo ingresado.")

       # Intentar encontrar el campo de confirmación del correo electrónico
        input_confirm_email_owner_elements = form.find_elements(*self.INPUT_CONFIRM_EMAIL_OWNER)

        # Verificar si el elemento existe
        if input_confirm_email_owner_elements:
            print("El campo de confirmación de correo electrónico fue encontrado.")
            input_confirm_email_owner = input_confirm_email_owner_elements[0]
            wait.until(EC.visibility_of(input_confirm_email_owner))
            ActionChains(self.driver).move_to_element(input_confirm_email_owner).perform()
            input_confirm_email_owner.send_keys(f"andres{index}@gmail.com")
        else:
            print("El campo de confirmación de correo electrónico no está presente.")
        

        # Click on checkbox
        check_box = self.driver.find_element(*self.CHECK_BOX)
        ActionChains(self.driver).move_to_element(check_box).perform()
        check_box.click()
        print("Checkbox de terminos y condiciones clickeado.")

        # Click on continue button
        # continue_button = self.driver.find_element(*self.BUTTON_CONTINUE)
        # ActionChains(self.driver).move_to_element(continue_button).perform()
        continue_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'btn-next')]//span[normalize-space(text())='Continuar']")
        self.driver.execute_script("arguments[0].click();", continue_button)
        # continue_button.click()
        print("Botón de continuar clickeado.")
      
          
                                                                        

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





       
