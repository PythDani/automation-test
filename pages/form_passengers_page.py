

import random
from selenium.webdriver.common.by import By
from logger import get_logger
from faker import Faker
from pages.common import Common
import time


class FormPassengersPage(Common):
    # ----------------------------------LOCATORS----------------------------------------------------------
    # Loader that indicate that the page is loading.
    LOADER:                                tuple = (By.CLASS_NAME, "loader")
    # Loader that indicate that the page is loading in some cases.
    LOADER_B:                              tuple = (By.CLASS_NAME, "page-loader")        
    # Container passenger group
    CONTAINERS_PASSENGERS:                 tuple = (By.XPATH, "//personal-data-form-custom")
    # Genre selector"
    GENRE_SELECTOR:                        tuple = (By.XPATH, "//button[@role='combobox' and @aria-haspopup='listbox']")
    # Male button option
    BUTTON_MALE_OPTION:                    tuple = (By.XPATH, "//li[@class='ui-dropdown_item ng-star-inserted']//button[@class='ui-dropdown_item_option']")
    # Input name field
    INPUT_NAME:                            tuple = (By.XPATH, " //*[contains(@name,'IdFirstName')]")
                                                           
    # Input last name field
    INPUT_LAST_NAME:                       tuple = (By.XPATH, "//*[contains(@name,'IdLastName')]")
    # Selector day of birth
    SELECTOR_DAY_OF_BIRTH:                 tuple = (By.XPATH, "//div[@class='ui-dropdown ng-star-inserted']//button[@class='ui-input' and @role='combobox' and @id='dateDayId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_']")
    # Day of birth button
    DAY_OF_BIRTH_BUTTON:                   tuple = (By.XPATH, "//li[@class='ui-dropdown_item ng-star-inserted' and @role='none']//button[@class='ui-dropdown_item_option' and @role='option' and @id='dateDayId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_-26']//span[text()='27']")
    # Selector month of birth
    SELECTOR_MONTH_OF_BIRTH:               tuple = (By.XPATH, "//div[@class='ui-dropdown ng-star-inserted']//button[@class='ui-input' and @role='combobox' and @id='dateMonthId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_']")
    # Month of birth button
    MONTH_OF_BIRTH_BUTTON:                 tuple = (By.XPATH, "//li[@class='ui-dropdown_item ng-star-inserted' and @role='none']//button[@class='ui-dropdown_item_option' and @role='option' and @id='dateMonthId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_-7']//span[text()='8']")
    # Selector year of birth
    SELECTOR_YEAR_OF_BIRTH:                tuple = (By.XPATH, "//div[@class='ui-dropdown ng-star-inserted']//button[@class='ui-input' and @role='combobox' and @id='dateYearId_IdDateOfBirthHidden_7E7E303030312D30312D30317E353334423438324433313244343535383534_']")
    # Year of birth button
    YEAR_OF_BIRTH_BUTTON:                  tuple = (By.XPATH, "//li[contains(@class, 'ui-dropdown_item') and contains(@class, 'ng-star-inserted')]//button[contains(@class, 'ui-dropdown_item_option')]//span[text()='2000']")
    # Selector of Nationality
    SELECTOR_OF_NATIONALITY:               tuple= (By.ID, "IdDocNationality_7E7E303030312D30312D30317E353334423438324433313244343535383534")
    # Nationality button
    NATIONALITY_BUTTON:                    tuple = (By.ID, "IdDocNationality_7E7E303030312D30312D30317E353334423438324433313244343535383534-0")

    #-----------------------------------------------Booking owner form-----------------------------------------------------
    # Phone prefix selector
    PHONE_PREFIX_SELECTOR:                 tuple = (By.ID, "phone_prefixPhoneId")
    # Phone prefix button
    PHONE_PREFIX_BUTTON:                   tuple = (By.ID, "phone_prefixPhoneId-0")
    # Input phone number owner
    INPUT_PHONE_NUMBER_OWNER:              tuple = (By.XPATH, "//input[@id='phone_phoneNumberId']")
    # Input email owner
    INPUT_EMAIL_OWNER:                     tuple = (By.XPATH, "//input[@id='email']")
    # Input confirm email owner
    INPUT_CONFIRM_EMAIL_OWNER:             tuple = (By.XPATH, "//input[@id='confirmEmail']")
    # CHECKBOX
    CHECK_BOX:                             tuple = (By.XPATH, "//input[@id='sendNewsLetter']")
    # Button Continue
    BUTTON_CONTINUE:                       tuple = (By.XPATH, "//button[contains(@class, 'btn-next')]//span[text()='Continuar']")

    def __init__(self, driver):
       super().__init__(driver)
       self.logger = get_logger(self.__class__.__name__)
    
    def fill_passenger_form_method(self):
        faker = Faker()
        
        # Encuentra todos los formularios de pasajeros
        passenger_forms = self.find_all(self.CONTAINERS_PASSENGERS)  
        self.logger.info(f"Se encontraron {len(passenger_forms)} formularios de pasajeros.")

        for index, form in enumerate(passenger_forms, start=1):
            self.logger.info(f"Llenando pasajero #{index}...")
            self.scroll_down_to_element(form).perform()

            # Click en el selector de género
            genre_selector = form.find_element(By.XPATH, ".//button[@role='combobox' and @aria-haspopup='listbox']")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", genre_selector)
            genre_selector.click()
            option_male = self.wait_to_be_clickable(self.BUTTON_MALE_OPTION)
            option_male.click()

            # Nombre aleatorio
            first_name = faker.first_name_male()
            last_name = faker.last_name()

            input_name = form.find_element(By.XPATH, ".//input[contains(@name, 'IdFirstName')]")
            self.wait_for_visibility(input_name)
            input_name.send_keys(first_name)

            input_last_name = form.find_element(By.XPATH, ".//input[contains(@name, 'IdLastName')]")
            self.wait_for_visibility(input_last_name)
            input_last_name.send_keys(last_name)

            # Fecha de nacimiento (día)
            day_button = form.find_element(By.XPATH, ".//button[contains(@id, 'dateDayId_IdDateOfBirthHidden')]")
            day_button.click()
            day_option = form.find_elements(By.XPATH, ".//ul[contains(@id, 'dateDayId_IdDateOfBirthHidden')]/li")[5]
            day_option.click()

            # Mes de nacimiento
            month_button = form.find_element(By.XPATH, ".//button[contains(@id, 'dateMonthId_IdDateOfBirthHidden')]")
            month_button.click()
            month_option = form.find_elements(By.XPATH, ".//ul[contains(@id, 'dateMonthId_IdDateOfBirthHidden')]/li")[5]
            month_option.click()

            # Año de nacimiento
            year_button = form.find_element(By.XPATH, ".//button[contains(@id, 'dateYearId_IdDateOfBirthHidden')]")
            year_button.click()
            year_option = form.find_elements(By.XPATH, ".//ul[contains(@id, 'dateYearId_IdDateOfBirthHidden')]/li")[10]
            year_option.click()

            # Nacionalidad
            nationality_button = form.find_element(By.XPATH, ".//button[contains(@id, 'IdDocNationality')]")
            nationality_button.click()
            nationality_option = form.find_elements(By.XPATH, ".//ul[contains(@id, 'IdDocNationality')]/li")[0]
            nationality_option.click()

            self.logger.info(f"Pasajero #{index} llenado: {first_name} {last_name}")

        # ----------------------------
        # Información de contacto (una sola vez fuera del bucle)
        # ----------------------------
        self.logger.info("Llenando datos de contacto...")

        prefix_button = self.wait_to_be_clickable(self.PHONE_PREFIX_SELECTOR)
        prefix_button.click()
        time.sleep(1)
        prefix_option = self.wait_to_be_clickable(self.PHONE_PREFIX_BUTTON)
        prefix_option.click()

        input_phone_number_owner = self.find(self.INPUT_PHONE_NUMBER_OWNER)
        self.wait_for_visibility(input_phone_number_owner)
        input_phone_number_owner.send_keys("3165555888")

        email = f"{faker.first_name().lower()}{random.randint(100,999)}@gmail.com"
        input_email_owner = self.find(self.INPUT_EMAIL_OWNER)
        self.wait_for_visibility(input_email_owner)
        input_email_owner.send_keys(email)

        confirm_email_elements = self.driver.find_elements(*self.INPUT_CONFIRM_EMAIL_OWNER)
        if confirm_email_elements:
            confirm_email = confirm_email_elements[0]
            self.wait_for_visibility(confirm_email)
            confirm_email.send_keys(email)
            self.logger.info("Confirmación de correo ingresada.")
        else:
            self.logger.info("Campo de confirmación de correo no presente.")

        check_box = self.find(self.CHECK_BOX)
        self.scroll_down_to_element(check_box).perform()
        check_box.click()

        continue_button = self.find((By.XPATH, "//button[contains(@class, 'btn-next')]//span[normalize-space(text())='Continuar']"))
        self.driver.execute_script("arguments[0].click();", continue_button)
        self.logger.info("Formulario completado.")
    def loader_b(self):
        self.wait_for_invisibility(self.LOADER_B)
    def loader_a(self):
        self.wait_for_invisibility(self.LOADER_A)
   