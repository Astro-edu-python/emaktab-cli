import time

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

from .clicker import EMaktabClicker
from .parser import EmaktabClassInfoParser, EmaktabScheduleLessonsParser
from .types.class_info import ClassInfo
from .types.lessons import Schedule


class EmaktabManager:
    def __init__(self, clicker: EMaktabClicker):
        self.clicker = clicker
        self.__logged_in = False

    def log_in_if_anonym(self):
        if not self.__logged_in:
            self.clicker.login()
            self.__logged_in = True
            time.sleep(2)

    def disable_popup_if_exists(self):
        try:
            popup = self.clicker.browser.find_element(By.ID, 'feedback_popup_overlay')
            if not popup or not popup.is_displayed():
                return
            try:
                popup.find_element(By.CLASS_NAME, 'feedback_popup_cross').click()
            except ElementClickInterceptedException:
                return
        except NoSuchElementException:
            return

    def get_page_soup(self, parser_type: str = 'html.parser') -> BeautifulSoup:
        return BeautifulSoup(self.clicker.browser.page_source, parser_type)

    def parse_class_info(self) -> ClassInfo:
        self.log_in_if_anonym()
        time.sleep(2)
        self.disable_popup_if_exists()
        self.clicker.class_info()
        time.sleep(1)
        soup = self.get_page_soup()
        class_info_parser = EmaktabClassInfoParser(soup)
        return class_info_parser.parse_class_info()

    def parse_week_lessons(self) -> Schedule:
        self.log_in_if_anonym()
        time.sleep(2)
        self.disable_popup_if_exists()
        self.clicker.week_lessons_schedule()
        time.sleep(1)
        soup = self.get_page_soup()
        schedule_parser = EmaktabScheduleLessonsParser(soup)
        return schedule_parser.parse_schedule_lessons()
