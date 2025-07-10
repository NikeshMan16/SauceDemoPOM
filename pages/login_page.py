import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import alert_is_present
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import allure


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.USERNAME_FIELD = (By.ID, "user-name")
        self.PASSWORD_FIELD = (By.ID, "password")
        self.LOGIN_BUTTON = (By.ID, "login-button")
        self.ERROR_MESSAGE = (By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')


    @allure.step("Login process is executed")
    def login(self, username, password):
        self.logger.log_action("Login process executed")
        self.enter_text(self.username_input, username)
        self.enter_text(self.password_input, password)
        self.click(self.login_button)
        self.logger.info("Login process completed.")
        self.wait.until(EC.url_contains('inventory.html'))

    @allure.step("Get error validation message")
    def get_error_message(self):
        self.wait.until(EC.visibility_of_element_located(self.error_message))
        return self.get_text(self.error_message)





