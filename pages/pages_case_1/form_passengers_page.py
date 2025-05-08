

import random
from selenium.webdriver.common.by import By
from logger import get_logger
from faker import Faker
from pages.common import Common
import time

from utils.exception import catch_exceptions


class FormPassengersPage(Common):
    # ----------------------------------LOCATORS----------------------------------------------------------
    # Loader that indicate that the page is loading in some cases.
    LOADER_B:                              tuple = (By.CLASS_NAME, "page-loader")        
    # Container passenger group
    CONTAINERS_PASSENGERS:                 tuple = (By.XPATH, "//personal-data-form-custom")    
    # Male button option
    BUTTON_MALE_OPTION:                    tuple = (By.XPATH, "//li[@class='ui-dropdown_item ng-star-inserted']//button[@class='ui-dropdown_item_option']")     

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
    BUTTON_CONTINUE:                       tuple = (By.XPATH, "//button[contains(@class, 'btn-next')]//span[normalize-space(text())='Continuar']")

    @catch_exceptions()
    def __init__(self, driver):

       """
       Initialize a FormPassengersPage instance.   
       Args:
           driver (selenium.webdriver): A selenium webdriver instance.
       """


       super().__init__(driver)
       self.logger = get_logger(self.__class__.__name__)
    
    @catch_exceptions()
    def fill_passenger_form_method(self):

        """
        Fills out the passenger form with fake data.

        This method fills out all passenger forms it can find on the page with
        fake data. It also fills out the contact information at the end.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: If there is an error during any of the operations.
        """

        faker = Faker()
        
        # Find all passenger forms
        passenger_forms = self.find_all(self.CONTAINERS_PASSENGERS)  
        self.logger.info(f"It was found {len(passenger_forms)} passenger forms.")

        for index, form in enumerate(passenger_forms, start=1):
            self.logger.info(f"Filling passenger form #{index}...")
            self.scroll_down_to_element(form).perform()

            # Gender
            genre_selector = form.find_element(By.XPATH, ".//button[@role='combobox' and @aria-haspopup='listbox']")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", genre_selector)
            genre_selector.click()
            option_male = self.wait_to_be_clickable(self.BUTTON_MALE_OPTION)
            option_male.click()

            # Names

            # Use "Test" only for the first passenger
            if index == 1:
                first_name = "Test"
                last_name = "Test"
            else:
                first_name = faker.first_name_male()
                last_name = faker.last_name()

            time.sleep(1)

            input_name = form.find_element(By.XPATH, ".//input[contains(@name, 'IdFirstName')]")
            self.wait_for_visibility(input_name)
            input_name.send_keys(first_name)

            input_last_name = form.find_element(By.XPATH, ".//input[contains(@name, 'IdLastName')]")
            self.wait_for_visibility(input_last_name)
            input_last_name.send_keys(last_name)

             # Year of birth
            year_button = form.find_element(By.XPATH, ".//button[contains(@id, 'dateYearId_IdDateOfBirthHidden')]")
            year_button.click()
            year_options = form.find_elements(By.XPATH, ".//ul[contains(@id, 'dateYearId_IdDateOfBirthHidden')]/li")
            if len(year_options) > 10:
                year_options[10].click()                
            elif year_options:
                year_options[0].click()                
            else:
                self.logger.warning(f"No year options found for passenger #{index}")

            # Day of birth
            day_button = form.find_element(By.XPATH, ".//button[contains(@id, 'dateDayId_IdDateOfBirthHidden')]")
            day_button.click()
            day_options = form.find_elements(By.XPATH, ".//ul[contains(@id, 'dateDayId_IdDateOfBirthHidden')]/li")
            if len(day_options) > 5:
                day_options[5].click()                
            elif day_options:
                day_options[0].click()               
            else:
                self.logger.warning(f"No day options found for passenger #{index}")

            # Month of birth
            month_button = form.find_element(By.XPATH, ".//button[contains(@id, 'dateMonthId_IdDateOfBirthHidden')]")
            month_button.click()
            month_options = form.find_elements(By.XPATH, ".//ul[contains(@id, 'dateMonthId_IdDateOfBirthHidden')]/li")
            if len(month_options) > 5:
                month_options[5].click()                
            elif month_options:
                month_options[0].click()                
            else:
                self.logger.warning(f"No month options found for passenger #{index}")           

            # Nationality
            nationality_button = form.find_element(By.XPATH, ".//button[contains(@id, 'IdDocNationality')]")
            nationality_button.click()
            nationality_options = form.find_elements(By.XPATH, ".//ul[contains(@id, 'IdDocNationality')]/li")
            if nationality_options:
                nationality_options[0].click()
            else:
                self.logger.warning(f"No nationality options found for passenger #{index}")

            # Optional: Document type
            doc_type_buttons = form.find_elements(By.XPATH, ".//button[contains(@id,'IdDocType_')]")
            if doc_type_buttons:
                doc_type_button = doc_type_buttons[0]
                doc_type_button.click()
                doc_type_options = form.find_elements(By.XPATH, ".//ul[contains(@id,'listId_IdDocType_')]/li")
                if len(doc_type_options) >= 3:
                    doc_type_options[0].click()  # 3rd option (index 2)
                elif doc_type_options:
                    doc_type_options[0].click()
                else:
                    self.logger.warning(f"No document type options found for passenger #{index}")
            else:
                self.logger.info(f"Document type button not present for passenger #{index}")

            # Optional: Document number
            doc_number_inputs = form.find_elements(By.XPATH, ".//input[contains(@name,'IdDocNum_')]")
            if doc_number_inputs:
                doc_number_input = doc_number_inputs[0]
                self.wait_for_visibility(doc_number_input)
                doc_number = faker.random_number(digits=8, fix_len=True)
                doc_number_input.send_keys(str(doc_number))
                self.logger.info(f"Passenger #{index} filled: {first_name} {last_name} - Doc#: {doc_number}")
            else:
                self.logger.info(f"Document number input not present for passenger #{index}")        

        # Fill contact info after all passengers
        self._fill_contact_information(faker)

    @catch_exceptions()
    def _fill_contact_information(self, faker):         
        """
        Fills out the contact information form with fake data.

        This method fills out the contact information form with fake data. It
        selects a phone prefix, fills out the phone number, fills out an email
        address, and checks a checkbox. It then clicks the continue button to
        move on to the next step.

        Args:
            faker (Faker): A faker instance used to generate fake data.

        Returns:
            None

        Raises:
            Exception: If there is an error during any of the operations.
        """

        self.logger.info("Filling contact information...")

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
            self.logger.info("Email confirmation field filled.")
        else:
            self.logger.info("Field confirm email not found.")

        check_box = self.find(self.CHECK_BOX)
        self.scroll_down_to_element(check_box).perform()
        check_box.click()

        continue_button = self.find(self.BUTTON_CONTINUE)
        self.driver.execute_script("arguments[0].click();", continue_button)
        self.logger.info("form filled.")
    
    @catch_exceptions()
    def loader_b(self):

        """
        Waits for the loader B to disappear.

        This method waits until the loader B element becomes invisible.
        If the loader B does not disappear within the timeout period, a 
        TimeoutException is raised.
        """


        self.wait_for_invisibility(self.LOADER_B)
    
    @catch_exceptions()
    def loader_a(self):
        """
        Waits for the loader A to disappear.

        This method waits until the loader A element becomes invisible.
        If the loader A does not disappear within the timeout period, a 
        TimeoutException is raised.
        """

        self.wait_for_invisibility(self.LOADER_A)
   