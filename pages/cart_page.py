from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from variables import id_item_to_be_added


class CartPage(BasePage):


    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

        self.button_item_to_be_added_to_cart = (By.ID,id_item_to_be_added)
        self.checkout_button = (By.ID,'checkout')
        self.checkout_info_form = (By.CLASS_NAME,'checkout_info')
        self.checkout_fname = (By.ID,'first-name')
        self.checkout_lname = (By.ID,'last-name')
        self.checkout_zip_code = (By.ID,'postal-code')
        self.continue_button_one = (By.ID,'continue')
        self.finish_button = (By.ID,'finish')
        self.complete_display_message = (By.XPATH,'//*[@id="checkout_complete_container"]/h2')
        self.back_home_button = (By.ID,'back-to-products')


    def proceed_to_checkout(self):
        self.wait.until(EC.visibility_of_element_located(self.checkout_button)).click()

    def confirm_order_details(self,fname,lname,zip):
        self.wait.until(EC.visibility_of_element_located(self.checkout_info_form))
        self.enter_text(self.checkout_fname,fname)
        self.enter_text(self.checkout_lname,lname)
        self.enter_text(self.checkout_zip_code,zip)
        self.wait.until(EC.element_to_be_clickable(self.continue_button_one)).click()

    def proceed_to_finish(self):
        self.wait.until(EC.element_to_be_clickable(self.finish_button)).click()

    def get_order_complete_message(self):
        self.wait.until(EC.visibility_of_element_located(self.complete_display_message))
        order_complete_message = self.get_text(self.complete_display_message)
        return order_complete_message

    def add_item_to_cart(self):
        self.wait.until(EC.visibility_of_element_located(self.button_item_to_be_added_to_cart)).click()






