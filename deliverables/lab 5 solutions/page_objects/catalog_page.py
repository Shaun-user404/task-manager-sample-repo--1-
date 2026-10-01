"""Page Object for catalogue search."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait


class CatalogPage:
    SEARCH_INPUT = (By.ID, "catalog-search")
    SEARCH_BUTTON = (By.ID, "search-submit")
    RESULTS = (By.CSS_SELECTOR, ".book-result")
    STATUS = (By.ID, "search-status")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 5)

    def open(self):
        self.driver.get(self.base_url)
        self.wait.until(expected.presence_of_element_located(self.SEARCH_INPUT))
        return self

    def search(self, query):
        field = self.wait.until(expected.element_to_be_clickable(self.SEARCH_INPUT))
        field.clear()
        field.send_keys(query)
        self.driver.find_element(*self.SEARCH_BUTTON).click()
        self.wait.until(lambda driver: driver.find_element(*self.STATUS).text != "")
        return self

    def result_texts(self):
        return [element.text for element in self.driver.find_elements(*self.RESULTS)]

    def status_text(self):
        return self.driver.find_element(*self.STATUS).text
