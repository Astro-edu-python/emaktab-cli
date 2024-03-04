import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


class EMaktabClicker:
    LOGIN_EMAKTAB_PAGE = 'https://login.emaktab.uz/'

    def __init__(self, browser: Chrome, login: str, password: str):
        self.browser = browser
        self.__login = login
        self.__password = password

    def login(self):
        self.browser.get(self.LOGIN_EMAKTAB_PAGE)
        time.sleep(2)
        self.browser.find_element(
            By.CSS_SELECTOR, ".login__body .login-body__field-wrapper input[name='login']"
        ).send_keys(self.__login)
        self.browser.find_element(
            By.CSS_SELECTOR, ".login__body .login-body__field-wrapper input[name='password']"
        ).send_keys(self.__password)
        self.browser.find_element(
            By.CSS_SELECTOR, '.login__submit'
        ).click()

    def class_info(self):
        self.browser.find_element(
            By.CSS_SELECTOR,
            'ul.header-menu .header-submenu_active '
            '.header-submenu__item:nth-child(2) a'
        ).click()
        time.sleep(1)
        self.browser.find_element(
            By.ID,
            'TabMembers'
        ).click()

    def week_lessons_schedule(self):
        self.browser.find_element(
            By.CSS_SELECTOR,
            'ul.header-menu .header-submenu_active '
            '.header-submenu__item:nth-child(4) a'
        ).click()
