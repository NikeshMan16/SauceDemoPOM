import allure
import pytest
from conftest import user_login_page
from pages.login_page import LoginPage
from utils.utils import get_test_data


TEST_DATA_FILE_NAME = "login_data.json"
FEATURE = allure.feature("SauceDemo | Login Page")


@FEATURE
@allure.story("Login using invalid credentials")
@pytest.mark.parametrize(
    ("username", "password"),
    get_test_data(TEST_DATA_FILE_NAME, "invalid_credentials", ["username", "password"], key_val=True),
)
def test_invalid_credentials(driver, username, password):
    page = LoginPage(driver)
    page.enter_username(username)
    page.enter_password(password)
    page.click_login_btn()
    assert page.get_error_message() == "Epic sadface: Username and password do not match any user in this service", (
        f"Error {username} | {password} : {page.get_error_message()}"
    )
