import datetime

from bs4 import BeautifulSoup, Tag

from .types.class_info import ClassInfo, Pupil
from .types.lessons import Schedule, Lesson
from .utils import resolve_month_date


class EmaktabClassInfoParser:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def parse_school_number(self) -> int:
        return int(self.soup.select_one(
            '.link_blue-with-orange-hover'
        ).text.split('-')[0])

    def parse_class_name(self) -> str:
        return self.soup.select_one(
            '.info h2'
        ).text.split()[1]

    def parse_academic_year(self) -> str:
        return self.soup.select_one(
            '.info p'
        ).text.split()[0]

    def _parse_pupil_info(self, element: Tag) -> str:
        return element.select_one('.tdName a').text

    def parse_pupils_info(self) -> list[Pupil]:
        pupils = self.soup.select('.people tbody tr')
        return [
            Pupil(*self._parse_pupil_info(pupil).split())
            for pupil in pupils
        ]

    def parse_class_info(self) -> ClassInfo:
        school_number = self.parse_school_number()
        class_name = self.parse_class_name()
        year_start, year_end = [
            int(value) for value in
            self.parse_academic_year().split('/')
        ]
        return ClassInfo(
            school_number, class_name, year_start, year_end,
            self.parse_pupils_info()
        )


class EmaktabScheduleLessonsParser:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def parse_quarter(self) -> int:
        return int(self.soup.select_one(
            '.old-tabs__tab.old-tabs__tab_active a'
        ).text.split()[0])

    def parse_week_start_end_date(self) -> tuple[datetime.datetime, datetime.datetime]:
        week_date = self.soup.select_one('.player .inl strong')
        return resolve_month_date(
            week_date.text, '—', '%d %B %Y'
        )

    def parse_lesson(self, tag: Tag, lesson_day: datetime.date) -> Lesson:
        lesson_name = tag.find('a').text
        teacher = tag.find('p').text
        start_time, end_time = tag.select_one('p[data-test-id="time"]').text.split(' - ')
        start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
        end_time = datetime.datetime.strptime(end_time, '%H:%M').time()
        return Lesson(
            lesson_name, teacher,
            datetime.datetime.combine(lesson_day, start_time),
            datetime.datetime.combine(lesson_day, end_time),
        )

    def parse_lessons(self, start_week_date: datetime.datetime) -> list[list[Lesson]]:
        calendar = self.soup.find(attrs={'id': 'editor'})
        all_week_lessons = []
        for index in range(2, 8):
            day_lessons = calendar.select(f'tr td:nth-child({index}) div')
            lessons_list = []
            for lesson in day_lessons:
                lesson_obj = self.parse_lesson(lesson, start_week_date.date())
                lessons_list.append(lesson_obj)
            all_week_lessons.append(lessons_list)
            start_week_date += datetime.timedelta(1)
        return all_week_lessons

    def parse_schedule_lessons(self) -> Schedule:
        date_start, date_end = self.parse_week_start_end_date()
        quarter = self.parse_quarter()
        lessons = self.parse_lessons(date_start)
        return Schedule(date_start, date_end, quarter, lessons)
