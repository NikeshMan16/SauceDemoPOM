from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
    ElementNotInteractableException,
    UnexpectedTagNameException,
    InvalidArgumentException,
    NoSuchFrameException,
    NoSuchWindowException,
)
from utils.logger_instance import logger


class BasePage:
    IS_LOADING_OVERLAY = (By.ID, "loading")
    DATE_PICKER = (By.ID, "ui-datepicker-div")
    MONTH_SELECTOR = (By.XPATH, "//div[@id='ui-datepicker-div']//select[@class='ui-datepicker-month']")
    YEAR_SELECTOR = (By.XPATH, "//div[@id='ui-datepicker-div']//select[@class='ui-datepicker-year']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.logger = logger
        self.wait = WebDriverWait(driver, timeout)
        self.action = ActionChains(driver)

    def navigate_to(self, url):
        """Navigates to the specified URL"""
        self.logger.log_method_entry(self.navigate_to.__name__)
        try:
            self.logger.info(f"Navigating to this URL: {url}")
            self.driver.get(url)
            self.logger.info(f"Successfully navigated to this URL: {url}")
        except WebDriverException as e:
            self.logger.error(f"An error occurred while trying to navigate to this URL: {url}. Error: {e}")
            raise WebDriverException(f"Failed to navigate to this URL: {url}.")

    def find_element(self, locator, timeout=10):
        self.logger.log_method_entry(self.find_element.__name__)
        try:
            self.logger.info(f"Finding a WebElement that has this locator: {locator}")
            web_element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            self.logger.info(f"Successfully found the WebElement that has this locator: {locator}")
            return web_element
        except TimeoutException as e:
            self.logger.error(
                f"Timeout occurred while trying to find the WebElement that has this locator: {locator} "
                f"within {timeout} seconds. Error: {e}"
            )
            raise TimeoutException(
                f"The WebElement that has this locator: {locator} wasn't found or wasn't visible "
                f"within {timeout} seconds."
            )
        except NoSuchElementException as e:
            self.logger.error(
                f"The WebElement that has this locator: {locator} couldn't be found in the DOM. Error: {e}"
            )
            raise NoSuchElementException(f"No such a WebElement that has this locator: {locator} in the DOM.")
        except ElementNotInteractableException as e:
            self.logger.error(
                f"The WebElement that has this locator: {locator} was present in the DOM, but wasn't "
                f"interactable. Error: {e}"
            )
            raise ElementNotInteractableException(
                f"The WebElement that has this locator: {locator} wasn't interactable. Error: {e}"
            )
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to find the WebElement that has this locator: {locator}. Error: {e}"
            )
            raise WebDriverException(f"Unable to find the WebElement that has this locator: {locator}.")

    def find_elements(self, locator, timeout=10):
        self.logger.log_method_entry(self.find_elements.__name__)
        try:
            self.logger.info(f"Finding WebElements that have this locator: {locator}")
            web_elements = WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))
            self.logger.info(f"Successfully found the WebElements that have this locator: {locator}")
            return web_elements
        except TimeoutException as e:
            self.logger.error(
                f"Timeout occurred while trying to find WebElements that have this locator: {locator} "
                f"within {timeout} seconds. Error: {e}."
            )
            raise TimeoutException(
                f"No WebElements that have this locator: {locator} were found or weren't visible "
                f"within {timeout} seconds."
            )
        except NoSuchElementException as e:
            self.logger.error(
                f"The WebElements that have this locator: {locator} couldn't be found in the DOM. Error: {e}"
            )
            raise NoSuchElementException(f"No such WebElements that have this locator: {locator} found in the DOM.")
        except ElementNotInteractableException as e:
            self.logger.error(
                f"The WebElements that have this locator: {locator} were present in the DOM, but weren't"
                f" interactable. Error: {e}"
            )
            raise ElementNotInteractableException(
                f"The WebElements that have this locator: {locator} weren't interactable."
            )
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to find the WebElements that have this locator: {locator}. Error: {e}"
            )
            raise WebDriverException(f"Unable to find the WebElements that have this locator: {locator}.")

    def get_text(self, locator, timeout=10):
        self.logger.log_method_entry(self.get_text.__name__)
        try:
            self.logger.info(f"Getting text from element with locator: {locator}")
            element = self.find_element(locator, timeout)

            tag_name = element.tag_name.lower()
            if tag_name == "input" or tag_name == "textarea":
                text = element.get_attribute("value")
            else:
                text = element.text.strip()
                if not text:
                    text = element.get_attribute("textContent").strip()
                    if not text:
                        locator_type, locator_value = locator
                        if locator_type == By.ID:
                            text = self.driver.execute_script(
                                f"return document.getElementById('{locator_value}').value;"
                            )

            text = element.text.strip()
            self.logger.info(f"Successfully got text: {text}")
            return text
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException, WebDriverException) as e:
            self.logger.error(f"An error occurred while getting text from element with locator: {locator}. Error: {e}")
            raise

    def wait_for_element_disappear(self, locator, timeout=10):
        """Waits until the element specified by the locator disappears (becomes invisible)."""
        self.logger.log_method_entry(self.wait_for_element_disappear.__name__)
        try:
            self.logger.info(f"Waiting for element to disappear: {locator}")
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            self.logger.info(f"Element disappeared: {locator}")
        except TimeoutException as e:
            self.logger.error(
                f"Timeout occurred while waiting for element to disappear: {locator} within {timeout} seconds. Error: {e}"
            )
            raise TimeoutException(f"Element with locator {locator} did not disappear within {timeout} seconds.")
        except WebDriverException as e:
            self.logger.error(f"An error occurred while waiting for element to disappear: {locator}. Error: {e}")
            raise WebDriverException(f"Unable to wait for element to disappear: {locator}.")

    def is_invisible(self, locator, timeout=10):
        """Returns True if the element is not visible (either not in DOM or not displayed)."""
        self.logger.log_method_entry(self.is_invisible.__name__)
        try:
            self.logger.info(f"Checking if element is invisible: {locator}")
            element = self.find_element(locator, timeout)
            invisible = not element.is_displayed()
            self.logger.info(f"Element visibility: {not invisible}")
            return invisible
        except (NoSuchElementException, TimeoutException):
            self.logger.info(f"Element is not present or timed out: {locator}. Considering it invisible.")
            return True
        except (ElementNotInteractableException, WebDriverException) as e:
            self.logger.error(f"Unexpected error while checking visibility of element {locator}: {e}")
            return False

    def select_date(self, locator, date):
        """Selects a date from a date picker widget."""
        self.logger.log_method_entry(self.select_date.__name__)
        try:
            self.logger.info(f"Selecting date {date}")
            year, month, day = date.split("-")

            self.click(locator)
            self.find_element(self.DATE_PICKER)
            self.find_element(self.MONTH_SELECTOR)
            self.find_element(self.YEAR_SELECTOR)

            self.select_dropdown_by_visible_text(self.YEAR_SELECTOR, year)
            self.select_dropdown_by_visible_text(self.MONTH_SELECTOR, month)
            self.click((By.XPATH, f"(//div[@id='ui-datepicker-div']/table//td[@onclick]/a)[{day}]"))
            self.logger.info(f"Successfully selected date {date}")
        except (
            TimeoutException,
            NoSuchElementException,
            ElementNotInteractableException,
            WebDriverException,
        ) as e:
            self.logger.error(f"An error occurred while selecting date {date}. Error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while selecting date {date}: {e}")
            raise

    def wait_for_page_load(self):
        self.logger.log_method_entry(self.wait_for_page_load.__name__)
        try:
            self.logger.info("Waiting for loading overlay to disappear.")
            self.wait_for_element_disappear(self.IS_LOADING_OVERLAY)
            self.logger.info("Loading overlay disappeared.")
        except TimeoutException as e:
            self.logger.warning(f"Loading overlay did not disappear within the expected time. Error: {e}")
        except WebDriverException as e:
            self.logger.error(f"WebDriver error while waiting for loading overlay to disappear. Error: {e}")
            raise

    def wait_for_url_to_be(self, expected_url, timeout=None):
        """Waits until the current URL is equal to the expected URL."""
        timeout = timeout or self.timeout
        try:
            self.logger.info(f"Waiting for the URL to be: {expected_url}")
            WebDriverWait(self.driver, timeout).until(EC.url_to_be(expected_url))
            self.logger.info(f"Successfully reached the expected URL: {expected_url}")
        except TimeoutException:
            self.logger.error(f"Timeout exceeded! Expected URL '{expected_url}' but got '{self.driver.current_url}'")
            raise AssertionError(
                f"Expected URL to be '{expected_url}', but got '{self.driver.current_url}' after {timeout} seconds."
            )
        except Exception as e:
            self.logger.error(f"An error occurred while waiting for the URL: {str(e)}")
            raise

    def get_message(self, locator):
        """Returns the text of the element if visible, False if not visible, and asserts if not present."""
        self.logger.log_method_entry(self.get_message.__name__)
        try:
            self.logger.info(f"Getting message from element with locator: {locator}")
            element = self.find_element(locator)
            if element.is_displayed():
                text = element.text.strip()
                self.logger.info(f"Successfully got message: {text}")
                return text
            else:
                self.logger.warning(f"Element with locator {locator} is not visible.")
                return False
        except (TimeoutException, NoSuchElementException):
            self.logger.error(f"Element with locator {locator} not found or not visible.")
            assert False, f"Element with locator {locator} is not displayed."
        except Exception as e:
            self.logger.error(f"Error while getting message: {e}")
            raise

    def get_validation_msg(self, locator):
        """Returns the validation message for a field if present, False if not present."""
        self.logger.log_method_entry(self.get_validation_msg.__name__)
        try:
            self.logger.info(f"Getting validation message from element with locator: {locator}")
            element = self.find_element(locator)
            if element.is_displayed():
                text = element.text.strip()
                self.logger.info(f"Successfully got validation message: {text}")
                return text
            else:
                self.logger.warning(f"Element with locator {locator} is not visible.")
                return False
        except (TimeoutException, NoSuchElementException):
            self.logger.error(f"Element with locator {locator} not found or not visible.")
            assert False, f"Element with locator {locator} is not displayed."
        except Exception as e:
            self.logger.error(f"Error while getting validation message: {e}")
            raise

    def get_notification_error_msg(self):
        """Returns the error message from a notification if present, False if not present."""
        pass

    def get_notification_success_msg(self):
        """Returns the success message from a notification if present, False if not present."""
        pass

    def get_current_url(self):
        """Returns the current URL of the browser."""
        self.logger.log_method_entry(self.get_current_url.__name__)
        try:
            self.logger.info("Getting the current URL")
            current_url = self.driver.current_url
            self.logger.info(f"Successfully got the current URL: {current_url}")
            return current_url
        except WebDriverException as e:
            self.logger.error(f"An error occurred while trying to get the current URL. Error: {e}")
            raise WebDriverException("Unable to get the current URL.")

    def go_back(self):
        """Navigates back to the previous page in the browser history."""
        self.logger.log_method_entry(self.go_back.__name__)
        try:
            self.logger.info("Navigating back to the previous page")
            self.driver.back()
            self.logger.info("Successfully navigated back to the previous page")
        except WebDriverException as e:
            self.logger.error(f"An error occurred while trying to navigate to the previous page. Error: {e}")
            raise WebDriverException("Unable to navigate to the previous page.")

    def go_forward(self):
        """Navigates forward to the next page in the browser history."""
        self.logger.log_method_entry(self.go_forward.__name__)
        try:
            self.logger.info("Navigating forward to the next page")
            self.driver.forward()
            self.logger.info("Successfully navigated forward to the next page")
        except WebDriverException as e:
            self.logger.error(f"An error occurred while trying to navigate to the next page. Error: {e}")
            raise WebDriverException("Unable to navigate to the next page")

    def refresh(self):
        """Refreshes the current page."""
        self.logger.log_method_entry(self.refresh.__name__)
        try:
            self.logger.info("Refreshing the current page")
            self.driver.refresh()
            self.logger.info("Successfully refreshed the current page")
        except WebDriverException as e:
            self.logger.error(f"An error occurred while trying to refresh the current page. Error: {e}")
            raise WebDriverException("Unable to refresh the current page.")

    def get_title(self):
        """Returns the title of the current page."""
        self.logger.log_method_entry(self.get_title.__name__)
        try:
            self.logger.info("Getting the title of the current page")
            title = self.driver.title
            self.logger.info(f"Successfully got the title of the current page. The title is: {title}")
            return title
        except WebDriverException as e:
            self.logger.error(f"An error occurred while trying to get the title of the current page. Error: {e}")
            raise WebDriverException("Unable to get the title of the current page.")

    def force_click(self, locator, timeout=10):
        """Forcefully clicks on a WebElement using ActionChains, bypassing some standard interactability restrictions."""
        self.logger.log_method_entry(self.force_click.__name__)
        try:
            self.logger.info(f"Force-clicking using ActionChains on a WebElement with locator: {locator}")
            element = self.wait.until(EC.presence_of_element_located(locator))

            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

            self.action.move_to_element(element).click().perform()

            self.logger.info(f"Successfully force-clicked using ActionChains on the WebElement with locator: {locator}")
        except NoSuchElementException as e:
            self.logger.error(f"The WebElement with locator: {locator} couldn't be found in the DOM. Error: {e}")
            raise NoSuchElementException(f"No WebElement with locator: {locator} found in the DOM.")
        except ElementNotInteractableException as e:
            self.logger.error(f"The WebElement with locator: {locator} was present but not interactable. Error: {e}")
            raise ElementNotInteractableException(f"The WebElement with locator: {locator} wasn't interactable.")
        except WebDriverException as e:
            self.logger.error(
                f"WebDriver error occurred during force-click using ActionChains for locator: {locator}. Error: {e}"
            )
            raise WebDriverException(f"ActionChains force-click failed for locator: {locator}.")

    def click(self, locator, timeout=10, retry_on_intercept=True):
        """Clicks on a WebElement, retrying if intercepted by another element."""
        self.logger.log_method_entry(self.click.__name__)
        try:
            self.logger.info(f"Clicking on a WebElement that has this locator: {locator}")
            web_element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            web_element.click()
            self.logger.info(f"Successfully clicked on a WebElement that has this locator: {locator}")
        except TimeoutException as e:
            self.logger.error(
                f"Timeout occurred while trying to click on a WebElement that has this locator: {locator} "
                f"within {timeout} seconds. Error: {e}"
            )
            raise TimeoutException(
                f"No WebElement that has this locator: {locator} was found or wasn't clickable "
                f"within {timeout} seconds."
            )
        except NoSuchElementException as e:
            self.logger.error(
                f"The WebElement that has this locator: {locator} couldn't be found in the DOM. Error: {e}"
            )
            raise NoSuchElementException(f"No such WebElement with this locator: {locator} found in the DOM.")
        except ElementNotInteractableException as e:
            self.logger.error(
                f"The WebElement that has this locator: {locator} was present but wasn't interactable. Error: {e}"
            )
            raise ElementNotInteractableException(f"The WebElement with locator: {locator} wasn't interactable.")
        except ElementClickInterceptedException as e:
            self.logger.warning(f"Click was intercepted for the WebElement with locator: {locator}. Error: {e}")
            if retry_on_intercept:
                try:
                    self.logger.info("Retrying click after scrolling the element into view.")
                    web_element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", web_element)
                    WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()
                    self.logger.info("Click successful on retry after intercept.")
                except Exception as retry_exception:
                    self.logger.error(
                        f"Retry failed for clicking WebElement with locator: {locator}. Error: {retry_exception}"
                    )
                    raise ElementClickInterceptedException(
                        f"The WebElement with locator: {locator} couldn't be clicked even after retry."
                    )
            else:
                raise ElementClickInterceptedException(
                    f"The WebElement with locator: {locator} couldn't be clicked due to interception."
                )
        except WebDriverException as e:
            self.logger.error(
                f"An unexpected WebDriver error occurred while trying to click on locator: {locator}. Error: {e}"
            )
            raise WebDriverException(f"Unable to click on the WebElement with locator: {locator}.")

    def send_keys(self, locator, text):
        """Enters text into a WebElement."""
        self.logger.log_method_entry(self.send_keys.__name__)
        try:
            self.logger.info(f"Sending this text: {text} into a WebElement that has this locator: {locator}")
            web_element = self.find_element(locator)
            web_element.clear()
            web_element.send_keys(text)
            self.logger.info(f"Successfully sent the text: {text} into a WebElement that has this locator: {locator}.")
        except NoSuchElementException as e:
            self.logger.error(
                f"The WebElement that has this locator: {locator} couldn't be found in the DOM. Error: {e}"
            )
            raise NoSuchElementException(f"No such a WebElement that has this locator: {locator} found in the DOM.")
        except ElementNotInteractableException as e:
            self.logger.error(
                f"The WebElement that has this locator: {locator} was present in the DOM but wasn't "
                f"interactable. Error: {e}"
            )
            raise ElementNotInteractableException(
                f"The WebElement that has this locator: {locator} wasn't interactable."
            )
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to send this text: {text} into a WebElement that has "
                f"this locator: {locator}. Error: {e}"
            )
            raise WebDriverException(
                f"Unable to send this text: {text} into a WebElement that has this locator: {locator}."
            )

    def quit(self):
        """Closes all browser windows and ends the WebDriver session."""
        self.logger.log_method_entry(self.quit.__name__)
        try:
            self.logger.info("Closing all browser windows and ending the WebDriver session.")
            self.driver.quit()
            self.logger.info("Successfully closed all browser windows and ending the WebDriver session.")
        except WebDriverException as e:
            self.logger.error(
                "An error occurred while trying to close all browser windows and ending the WebDriver "
                f"session. Error: {e}"
            )
            raise WebDriverException("Unable to close all browser windows and ending the WebDriver session.")

    def close(self):
        """Closes the current browser window."""
        self.logger.log_method_entry(self.close.__name__)
        try:
            self.logger.info("Closing the current browser window.")
            self.driver.close()
            self.logger.info("Successfully closed the current browser window.")
        except WebDriverException as e:
            self.logger.error(f"An error occurred while trying to close the current window. Error: {e}")
            raise WebDriverException("Unable to close the current window.")

    def is_dropdown_multiple_selections(self, locator):
        """Checks if the dropdown supports multiple selections."""
        self.logger.log_method_entry(self.is_dropdown_multiple_selections.__name__)
        try:
            self.logger.info("Checking if the dropdown supports multiple selections.")
            web_element = self.find_element(locator)
            dropdown = Select(web_element)
            if dropdown.is_multiple:
                self.logger.info("The dropdown supports multiple selections.")
            else:
                self.logger.info("The dropdown doesn't support multiple selections.")
            return dropdown.is_multiple
        except UnexpectedTagNameException as e:
            self.logger.error(f"The Select class didn't get an expected WebElement. Error: {e}")
            raise UnexpectedTagNameException(
                f"The Select class received an unexpected WebElement that has this locator: {locator}."
            )
        except WebDriverException as e:
            self.logger.error(
                "An error occurred while trying to check if the dropdown supports multiple selections "
                f"or not. Error: {e}"
            )
            raise WebDriverException("Unable to check if the dropdown supports multiple selections or not.")

    def select_dropdown_by_visible_text(self, locator, text):
        """Selects a dropdown option by a visible text."""
        self.logger.log_method_entry(self.select_dropdown_by_visible_text.__name__)
        try:
            self.logger.info(f"Selecting a dropdown option by this visible text: {text}.")
            web_element = self.find_element(locator)
            drop_down = Select(web_element)
            drop_down.select_by_visible_text(text)
            self.logger.info(f"Successfully selected a dropdown option by this visible text: {text}.")
        except UnexpectedTagNameException as e:
            self.logger.error(f"The Select class didn't get an expected WebElement. Error: {e}")
            raise UnexpectedTagNameException(
                f"The Select class received an unexpected WebElement that has this locator: {locator}."
            )
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to select a dropdown option by this visible text: {text}. Error: {e} "
            )
            raise WebDriverException(f"Unable to select a dropdown option by this visible text: {text}.")

    def select_dropdown_by_value(self, locator, value):
        """Selects a dropdown option by its value attribute."""
        self.logger.log_method_entry(self.select_dropdown_by_value.__name__)
        try:
            self.logger.info(f"Selecting a dropdown option by this value: {value}.")
            web_element = self.find_element(locator)
            drop_down = Select(web_element)
            drop_down.select_by_value(value)
            self.logger.info(f"Successfully selected a dropdown option by this value: {value}.")
        except UnexpectedTagNameException as e:
            self.logger.error(f"The Select class didn't get an expected WebElement. Error: {e}")
            raise UnexpectedTagNameException(
                f"The Select class received an unexpected WebElement that has this locator: {locator}."
            )
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to select a dropdown option by this value: {value}. Error: {e}"
            )
            raise WebDriverException(f"Unable to select a dropdown option by this value: {value}.")

    def select_dropdown_by_index(self, locator, index):
        """Selects a dropdown option by its index."""
        self.logger.log_method_entry(self.select_dropdown_by_index.__name__)
        try:
            self.logger.info(f"Selecting a dropdown option by this index: {index}.")
            self.logger.info("Checking if the index is negative or not.")
            if index < 0:
                self.logger.error("Index cannot be negative.")
                raise ValueError("Index must be a non-negative integer.")
            web_element = self.find_element(locator)
            drop_down = Select(web_element)
            drop_down.select_by_index(index)
            self.logger.info(f"Successfully selected a dropdown option by this index: {index}.")
        except UnexpectedTagNameException as e:
            self.logger.error(f"The Select class didn't get an expected WebElement. Error: {e}")
            raise UnexpectedTagNameException(
                f"The Select class received an unexpected WebElement that has this locator: {locator}."
            )
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to select a dropdown option by this index: {index}. Error: {e}"
            )
            raise WebDriverException(f"Unable to select a dropdown option by this index{index}.")

    def get_all_dropdown_options(self, locator):
        """Returns all options in a dropdown as a list of strings."""
        self.logger.log_method_entry(self.get_all_dropdown_options.__name__)
        try:
            self.logger.info("Getting all dropdown options.")
            web_element = self.find_element(locator)
            drop_down = Select(web_element)
            options = [option.text for option in drop_down.options]
            self.logger.info(f"Successfully got all dropdown options. Options are: {options}")
            return options
        except UnexpectedTagNameException as e:
            self.logger.error(f"The Select class didn't get an expected WebElement. Error: {e}")
            raise UnexpectedTagNameException(
                f"The Select class received an unexpected WebElement that has this locator: {locator}."
            )
        except WebDriverException as e:
            self.logger.error(f"An error occurred while trying to get all dropdown options. Error: {e}")
            raise WebDriverException("Unable to get all dropdown options.")

    def get_selected_dropdown_option(self, locator):
        """Returns the currently selected option in a dropdown."""
        self.logger.log_method_entry(self.get_selected_dropdown_option.__name__)
        try:
            self.logger.info("Getting the currently selected dropdown option.")
            web_element = self.find_element(locator)
            drop_down = Select(web_element)
            self.logger.info(
                "Successfully got the currently selected dropdown option. The currently selected option "
                f"is: {drop_down.first_selected_option.text}"
            )
            return drop_down.first_selected_option.text
        except UnexpectedTagNameException as e:
            self.logger.error(f"The Select class didn't get an expected WebElement. Error: {e}")
            raise UnexpectedTagNameException(
                f"The Select class received an unexpected WebElement that has this locator: {locator}."
            )
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to get the currently selected dropdown option. Error: {e}"
            )
            raise WebDriverException("Unable to get the currently selected dropdown option.")

    def deselect_all_dropdown_options(self, locator):
        """Deselects all selected options in a multi-select dropdown."""
        self.logger.log_method_entry(self.deselect_all_dropdown_options.__name__)
        try:
            self.logger.info("Deselecting all selected options in a multi-select dropdown.")
            self.logger.info("Checking if the dropdown is a multi-select dropdown or not.")
            if not self.is_dropdown_multiple_selections(locator):
                self.logger.error("The dropdown isn't a multi-select dropdown.")
                raise InvalidArgumentException("The dropdown isn't supported the multi-select option.")
            web_element = self.find_element(locator)
            drop_down = Select(web_element)
            drop_down.deselect_all()
            self.logger.info("Successfully deselected all selected options in the multi-select dropdown.")
        except UnexpectedTagNameException as e:
            self.logger.error(f"The Select class didn't get an expected WebElement. Error: {e}")
            raise UnexpectedTagNameException(
                f"The Select class received an unexpected WebElement that has this locator: {locator}."
            )
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to deselect all selected options in the multi-select "
                f"dropdown. Error: {e}"
            )
            raise WebDriverException("Unable to deselect all selected options in the multi-select dropdown.")

    def deselect_dropdown_by_index(self, locator, index):
        """Deselects a dropdown option by its index in a multi-select dropdown."""
        self.logger.log_method_entry(self.deselect_dropdown_by_index.__name__)
        try:
            self.logger.info(f"Deselecting an option in the multi-select dropdown by this index: {index}.")
            self.logger.info("Checking if the dropdown supports multiple selections or not.")
            if not self.is_dropdown_multiple_selections(locator):
                self.logger.error("The dropdown doesn't support the multi-select option.")
                raise InvalidArgumentException("The dropdown is not a multi-select dropdown.")
            web_element = self.find_element(locator)
            drop_down = Select(web_element)
            drop_down.deselect_by_index(index)
            self.logger.info(f"Successfully deselected a dropdown option by the index: {index}.")
        except UnexpectedTagNameException as e:
            self.logger.error(f"The Select class didn't get an expected WebElement. Error: {e}")
            raise UnexpectedTagNameException(
                f"The Select class received an unexpected WebElement that has this locator: {locator}."
            )
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to deselect a dropdown option by this index: {index}. Error: {e}."
            )
            raise WebDriverException(f"Unable to deselect a dropdown option by this index: {index}.")

    def deselect_dropdown_by_value(self, locator, value):
        """Deselects a dropdown option by its value attribute in a multi-select dropdown."""
        self.logger.log_method_entry(self.deselect_dropdown_by_value.__name__)
        try:
            self.logger.info(f"Deselecting an option in the multi-select dropdown by this value: {value}.")
            self.logger.info("Checking if the dropdown supports multiple selections or not.")
            if not self.is_dropdown_multiple_selections(locator):
                self.logger.error("The dropdown doesn't support the multi-select option.")
                raise InvalidArgumentException("The dropdown is not a multi-select dropdown.")
            web_element = self.find_element(locator)
            drop_down = Select(web_element)
            drop_down.deselect_by_value(value)
            self.logger.info(f"Successfully deselected an option by the value: {value}.")
        except UnexpectedTagNameException as e:
            self.logger.error(f"The Select class didn't get an expected WebElement. Error: {e}")
            raise UnexpectedTagNameException(
                f"The Select class received an unexpected WebElement that has this locator: {locator}."
            )
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to deselect an option by this value: {value}. Error: {e}"
            )
            raise WebDriverException(f"Unable to deselect a dropdown option by this value: {value}.")

    def deselect_dropdown_by_visible_text(self, locator, text):
        """Deselects a dropdown option by its visible text in a multi-select dropdown."""
        self.logger.log_method_entry(self.deselect_dropdown_by_visible_text.__name__)
        try:
            self.logger.info(f"Deselecting an option in the multi-select dropdown by this visible text: {text}.")
            self.logger.info("Checking if the dropdown supports multiple selections or not.")
            if not self.is_dropdown_multiple_selections(locator):
                self.logger.error("The dropdown doesn't support the multi-select option.")
                raise InvalidArgumentException("The dropdown is not a multi-select dropdown.")
            web_element = self.find_element(locator)
            drop_down = Select(web_element)
            drop_down.deselect_by_visible_text(text)
            self.logger.info(f"Successfully deselected an option by the visible text: {text}.")
        except UnexpectedTagNameException as e:
            self.logger.error(f"The Select class didn't get an expected WebElement. Error: {e}")
            raise UnexpectedTagNameException(
                f"The Select class received an unexpected WebElement that has this locator: {locator}."
            )
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to deselect an option by this visible text: {text}. Error: {e}"
            )
            raise WebDriverException(f"Unable to select a dropdown option by this visible text: {text}.")

    def switch_to_iframe(self, locator, timeout=10):
        """Switches the WebDriver's context to the specified IFrame."""
        self.logger.log_method_entry(self.switch_to_iframe.__name__)
        try:
            self.logger.info(f"Switching to a IFrame that has this locator: {locator}.")
            WebDriverWait(self.driver, timeout).until(EC.frame_to_be_available_and_switch_to_it(locator))
            self.logger.info(f"Successfully switched to the IFrame that has this locator: {locator}.")
        except TimeoutException as e:
            self.logger.error(
                f"Timeout occurred while trying to switch to a IFrame that has this locator: {locator}. Error: {e}."
            )
            raise TimeoutException(f"The IFrame wasn't available within {timeout} seconds.")
        except NoSuchFrameException as e:
            self.logger.error(f"The IFrame that has this locator: {locator} couldn't be found in the DOM. Error: {e}.")
            raise NoSuchFrameException(f"No such an IFrame that has this locator: {locator} in the DOM.")
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to switch to a IFrame that has this locator: {locator}. Error: {e}."
            )
            raise WebDriverException(f"Unable to switch to IFrame that has this locator: {locator}.")

    def switch_to_default_content(self):
        """Switches the WebDriver's context back to the default content (outside the IFrame)."""
        self.logger.log_method_entry(self.switch_to_default_content.__name__)
        try:
            self.logger.info("Switching back to the default content.")
            self.driver.switch_to.default_content()
            self.logger.info("Successfully switched back to the default content.")
        except WebDriverException as e:
            self.logger.error(f"An error occurred while trying to switch back to the default content. Error: {e}.")
            raise WebDriverException("Unable to switch back to the default content.")

    def get_current_window_handle(self):
        """Returns the handle of the current window."""
        self.logger.log_method_entry(self.get_current_window_handle.__name__)
        try:
            self.logger.info("Getting the current window handle.")
            current_window_handle = self.driver.current_window_handle
            self.logger.info(
                "Successfully retrieved the current window handle. The current window handle is: "
                f"{current_window_handle}."
            )
            return current_window_handle
        except NoSuchWindowException as e:
            self.logger.error(f"The current window handle does not exist or is closed. Error: {e}.")
            raise NoSuchWindowException("No such opened window to get its handle.")
        except WebDriverException as e:
            self.logger.error(f"An error occurred while trying to retrieve the current window handle. Error: {e}.")
            raise WebDriverException("Unable to get the current window handle.")

    def get_all_window_handles(self):
        """Returns a list of all window handles."""
        self.logger.log_method_entry(self.get_all_window_handles.__name__)
        try:
            self.logger.info("Getting the all window handles.")
            all_window_handles = self.driver.window_handles
            self.logger.info(
                f"Successfully retrieved the all window handles. The all window handles are: {all_window_handles}."
            )
            return all_window_handles
        except NoSuchWindowException as e:
            self.logger.error(f"No opened windows to retrieve their handles. Error: {e}.")
            raise NoSuchWindowException("No windows were opened.")
        except WebDriverException as e:
            self.logger.error(f"An error occurred while trying to retrieve all window handles. Error: {e}.")
            raise WebDriverException("Unable to get all window handles.")

    def switch_to_window(self, handle):
        """Switches the WebDriver's context to the specified window."""
        self.logger.log_method_entry(self.switch_to_window.__name__)
        try:
            self.logger.info(f"Switching to the {handle} window.")
            self.driver.switch_to.window(handle)
            self.logger.info(f"Successfully switched to this {handle} window.")
        except NoSuchWindowException as e:
            self.logger.error(f"The {handle} window does not exist or is closed. Error: {e}.")
            raise NoSuchWindowException("The specified window didn't exist or was closed.")
        except WebDriverException as e:
            self.logger.error(f"An error occurred while trying to switch {handle} window. Error: {e}.")
            raise WebDriverException(f"Unable to switch to this {handle} window.")

    def switch_to_next_tab(self):
        """Switches to the next browser tab (assuming it was newly opened)."""
        self.logger.log_method_entry(self.switch_to_next_tab.__name__)
        try:
            self.logger.info("Attempting to switch to the next browser tab.")
            original_handle = self.driver.current_window_handle
            all_handles = self.driver.window_handles
            new_handles = [h for h in all_handles if h != original_handle]

            if not new_handles:
                self.logger.error("No new tab found to switch to.")
                raise NoSuchWindowException("No new tab was found to switch to.")

            self.driver.switch_to.window(new_handles[0])
            self.logger.info(f"Switched to next tab with handle: {new_handles[0]}")
        except WebDriverException as e:
            self.logger.error(f"Failed to switch to next tab. Error: {e}")
            raise WebDriverException(f"Failed to switch to next tab. Error: {e}")

    def get_table_row_values(self, locater):
        """Returns a list of values from each row in a table."""
        self.logger.log_method_entry(self.get_table_row_values.__name__)
        try:
            self.logger.info(f"Getting the values from each row in the table that has this locator: {locater}.")
            table = self.find_elements(locater)
            val = [el.text for el in table]
            self.logger.info(f"Successfully retrieved the values from each row in the table. The values are: {val}.")
            return val
        except NoSuchElementException as e:
            self.logger.error(f"The table with this locator: {locater} was not found. Error: {e}.")
            raise NoSuchElementException(f"The table with this locator: {locater} was not found.")
        except WebDriverException as e:
            self.logger.error(
                f"An error occurred while trying to get the values from each row in the table. Error: {e}."
            )
            raise WebDriverException("Unable to get the values from each row in the table.")
