import pytest
import allure
from utils.config import Config
from utils.webdriver_initializer import WebDriverInitializer
from selenium.common.exceptions import WebDriverException
from utils.logger_instance import logger


@pytest.fixture(scope="function")
def driver():
    """Fixture to initialize and yield a WebDriver instance."""
    logger.log_method_entry("The Driver Fixture")
    webdriver = None
    try:
        logger.info("Initializing WebDriver...")
        webdriver_initializer = WebDriverInitializer()
        webdriver = webdriver_initializer.initialize_webdriver()
        webdriver.maximize_window()
        logger.info("WebDriver initialized successfully.")
        yield webdriver
    except WebDriverException as e:
        logger.error("Failed to initialize the WebDriver.")
        raise WebDriverException(f"An error occurred while trying to initialize the webdriver. Error: {e}")
    finally:
        if webdriver is not None:
            logger.info("Quitting WebDriver...")
            webdriver.quit()
            logger.info("WebDriver quit successfully.")




@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(), name="Failure Screenshot", attachment_type=allure.attachment_type.PNG
            )


# @pytest.fixture(scope="session", autouse=True)
# def clear_results():
#     path = os.path.join(os.getcwd(), "reports", "allure-results")
#     if os.path.exists(path):
#         shutil.rmtree(path)
#     os.makedirs(path, exist_ok=True)
