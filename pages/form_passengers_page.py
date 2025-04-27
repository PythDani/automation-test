

from selenium.webdriver.common.by import By
from pages.common import Common
import time


class FormPassengersPage(Common):
    # ----------------------------------LOCATORS----------------------------------------------------------
    # Loader that indicate that the page is loading.
    LOADER: tuple = (By.CLASS_NAME, "loader")
    # Loader that indicate that the page is loading in some cases.
    LOADER_B: tuple = (By.CLASS_NAME, "page-loader")        
    # Container first passenger
    CONTAINER_FIRST_PASSENGER: tuple = (By.XPATH, "//*[@id='maincontent']/div/div[3]/div/div/passenger-details-container/personal-data-custom/div/div/div[1]/personal-data-form-custom")    
    # Container passenger group
    CONTAINERS_PASSENGERS: tuple = (By.XPATH, "//personal-data-form-custom")
    # Genre selector"
    GENRE_SELECTOR: tuple = (By.XPATH, "//button[@role='combobox' and @aria-haspopup='listbox']")
    # Male button option
    BUTTON_MALE_OPTION: tuple = (By.XPATH, "//li[@class='ui-dropdown_item ng-star-inserted']//button[@class='ui-dropdown_item_option']")
    # Input name field
    INPUT_NAME: tuple = (By.XPATH, "//div[@class='ui-input_wrap']//input[@name='IdFirstName7E7E303030312D30312D30317E353334423438324433313244343535383534']")
    # Input last name field
    INPUT_LAST_NAME: tuple = (By.XPATH, "//div[@class='ui-input_wrap']//input[@name='IdLastName7E7E303030312D30312D30317E353334423438324433313244343535383534']")
    # Selector day of birth
    SELECTOR_DAY_OF_BIRTH:tuple = (By.XPATH, "//div[@class='ui-dropdown ng-star-inserted']//button[@class='ui-input' and @role='combobox' and @id='dateDayId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_']")
    # Day of birth button
    DAY_OF_BIRTH_BUTTON: tuple = (By.XPATH, "//li[@class='ui-dropdown_item ng-star-inserted' and @role='none']//button[@class='ui-dropdown_item_option' and @role='option' and @id='dateDayId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_-26']//span[text()='27']")
    # Selector month of birth
    SELECTOR_MONTH_OF_BIRTH: tuple = (By.XPATH, "//div[@class='ui-dropdown ng-star-inserted']//button[@class='ui-input' and @role='combobox' and @id='dateMonthId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_']")
    # Month of birth button
    MONTH_OF_BIRTH_BUTTON: tuple = (By.XPATH, "//li[@class='ui-dropdown_item ng-star-inserted' and @role='none']//button[@class='ui-dropdown_item_option' and @role='option' and @id='dateMonthId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_-7']//span[text()='8']")
    # Selector year of birth
    SELECTOR_YEAR_OF_BIRTH: tuple = (By.XPATH, "//div[@class='ui-dropdown ng-star-inserted']//button[@class='ui-input' and @role='combobox' and @id='dateYearId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_']")
    # Year of birth button
    YEAR_OF_BIRTH_BUTTON: tuple = (By.XPATH, "//li[contains(@class, 'ui-dropdown_item') and contains(@class, 'ng-star-inserted')]//button[contains(@class, 'ui-dropdown_item_option')]//span[text()='2000']")
    # Selector of Nationality
    SELECTOR_OF_NATIONALITY: tuple= (By.ID, "IdDocNationality_7E7E303030312D30312D30317E353334423438324433313244343535383534")
    # Nationality button
    NATIONALITY_BUTTON: tuple = (By.ID, "IdDocNationality_7E7E303030312D30312D30317E353334423438324433313244343535383534-0")

    #-----------------------------------------------Booking owner form-----------------------------------------------------
    # Phone prefix selector
    PHONE_PREFIX_SELECTOR: tuple = (By.ID, "phone_prefixPhoneId")
    # Phone prefix button
    PHONE_PREFIX_BUTTON: tuple = (By.ID, "phone_prefixPhoneId-0")
    # Input phone number owner
    INPUT_PHONE_NUMBER_OWNER: tuple = (By.XPATH, "//input[@id='phone_phoneNumberId']")
    # Input email owner
    INPUT_EMAIL_OWNER: tuple = (By.XPATH, "//input[@id='email']")
    # Input confirm email owner
    INPUT_CONFIRM_EMAIL_OWNER: tuple = (By.XPATH, "//input[@id='confirmEmail']")
    # CHECKBOX
    CHECK_BOX: tuple = (By.XPATH, "//input[@id='sendNewsLetter']")
    # Button Continue
    BUTTON_CONTINUE: tuple = (By.XPATH, "//button[contains(@class, 'btn-next')]//span[text()='Continuar']")

    def __init__(self, driver):
       super().__init__(driver)
    
    def fill_passenger_form_method(self):
        container_first_passenger = self.find(self.CONTAINER_FIRST_PASSENGER)
        self.scroll_down_to_element(container_first_passenger).perform()

        # All forms passengers
        passenger_forms = self.find_all(self.CONTAINERS_PASSENGERS)  
        print(f"Se encontraron {len(passenger_forms)} formularios de pasajeros.")

        for index, form in enumerate(passenger_forms, start=1):
            print(f"Llenando pasajero #{index}...")
            self.scroll_down_to_element(form).perform()

            # --- Dentro del contenedor 'form' ---
            # Click genre selector
            genre_selector = form.find_element(By.XPATH, ".//button[@role='combobox' and @aria-haspopup='listbox']")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", genre_selector)
            self.wait_to_be_clickable((By.XPATH, ".//button[@role='combobox' and @aria-haspopup='listbox']"))
            genre_selector.click()
            
            option_male = self.wait_to_be_clickable(self.BUTTON_MALE_OPTION)
            option_male.click()

            # Input first name
            input_name = form.find_element(By.XPATH, ".//div[@class='ui-input_wrap']//input[contains(@name, 'IdFirstName')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_name)
            self.wait_for_visibility(input_name)
            input_name.send_keys(f"Andres")

            # Input last name
            input_last_name = form.find_element(By.XPATH, ".//div[@class='ui-input_wrap']//input[contains(@name, 'IdLastName')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_last_name)
            self.wait_for_visibility(input_last_name)
            input_last_name.send_keys(f"Perez")

            # Day of birth
            day_of_birth = form.find_element(By.XPATH, ".//button[contains(@id, 'dateDayId_IdDateOfBirthHidden')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", day_of_birth)
            day_of_birth.click()

            if index == 1:
                day_of_birth_option = self.wait_to_be_clickable(self.DAY_OF_BIRTH_BUTTON)
                day_of_birth_option.click()
            else:
                day_of_birth_option = form.find_element(By.ID, "dateDayId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433323244343535383534_-26")
                day_of_birth_option.click()

            # Month of birth
            month_of_birth = form.find_element(By.XPATH, ".//button[contains(@id, 'dateMonthId_IdDateOfBi" \
            "rthHidden')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", month_of_birth)
            self.wait_to_be_clickable(month_of_birth)
            month_of_birth.click()

            if index == 1:
                month_of_birth_option = self.wait_to_be_clickable(self.MONTH_OF_BIRTH_BUTTON)
                month_of_birth_option.click()
            else:
                month_of_birth_option = form.find_element(By.ID, "dateMonthId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433323244343535383534_-7")
                month_of_birth_option.click()

            # Year of birth
            year_of_birth = form.find_element(By.XPATH, ".//button[contains(@id, 'dateYearId_IdDateOfBirthHidden')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", year_of_birth)
            self.wait_to_be_clickable(year_of_birth)
            year_of_birth.click()

            year_of_birth_option = self.wait_to_be_clickable(self.YEAR_OF_BIRTH_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", year_of_birth_option)
            year_of_birth_option.click()
           

            # Nationality
            if index == 1:
                nationality = form.find_element(*self.SELECTOR_OF_NATIONALITY)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nationality)
                self.wait_for_visibility(nationality)
                nationality.click()

                nationality_option = self.wait_to_be_clickable(self.NATIONALITY_BUTTON)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nationality_option)
                nationality_option.click()
            else:
                nationality = form.find_element(By.ID, "IdDocNationality_7E7E303030312D30312D30317E353334423438324433323244343535383534")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nationality)
                self.wait_for_visibility(nationality)
                nationality.click()

                nationality_option = form.find_element(By.ID, "IdDocNationality_7E7E303030312D30312D30317E353334423438324433323244343535383534-0")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nationality_option)
                nationality_option.click()

            print(f"Pasajero #{index} llenado.")
        
        # Click on prefix button to show prefix phone list
        prefix_button = self.wait_to_be_clickable(self.PHONE_PREFIX_SELECTOR)
        prefix_button.click()
        time.sleep(3)
        print("Listado de prefixes mostrado.")

        # Select prefix
        self.driver.execute_script("window.scrollBy(0, 300);")
        prefix_option = self.wait_to_be_clickable(self.PHONE_PREFIX_BUTTON)
        prefix_option.click()
        print("Prefix seleccionado.")

        # Input phone number owner
        input_phone_number_owner = form.find_element(*self.INPUT_PHONE_NUMBER_OWNER)
        self.wait_for_visibility(input_phone_number_owner)
        self.scroll_down_to_element(input_phone_number_owner).perform()
        input_phone_number_owner.send_keys("3165555888")
        print("Número de telefono ingresado.")

        # Input email owner
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        input_email_owner = form.find_element(*self.INPUT_EMAIL_OWNER)
        self.wait_for_visibility(input_email_owner)
        self.scroll_down_to_element(input_email_owner).perform()
        input_email_owner.send_keys(f"andres{index}@gmail.com")
        print("Correo ingresado.")

       # Intentar encontrar el campo de confirmación del correo electrónico
        input_confirm_email_owner_elements = form.find_elements(*self.INPUT_CONFIRM_EMAIL_OWNER)

        # Verificar si el elemento existe
        if input_confirm_email_owner_elements:
            print("El campo de confirmación de correo electrónico fue encontrado.")
            input_confirm_email_owner = input_confirm_email_owner_elements[0]
            self.wait_for_visibility(input_confirm_email_owner)
            self.scroll_down_to_element(input_confirm_email_owner).perform()
            input_confirm_email_owner.send_keys(f"andres{index}@gmail.com")
        else:
            print("El campo de confirmación de correo electrónico no está presente en esta versión.")
        

        # Click on checkbox
        check_box = self.find(self.CHECK_BOX)
        self.scroll_down_to_element(check_box).perform()
        check_box.click()
        print("Checkbox de terminos y condiciones clickeado.")

        # Click on continue button
        continue_button = self.find((By.XPATH, "//button[contains(@class, 'btn-next')]//span[normalize-space(text())='Continuar']"))
        self.driver.execute_script("arguments[0].click();", continue_button)        
        print("Botón de continuar clickeado.")