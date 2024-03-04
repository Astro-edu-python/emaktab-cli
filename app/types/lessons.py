from dataclasses import dataclass
from datetime import datetime


@dataclass
class Lesson:
    name: str
    teacher: str
    start_date: datetime
    end_date: datetime


@dataclass
class Schedule:
    date_start: datetime
    date_end: datetime
    quarter: int
    lessons: list[list[Lesson]]

    @property
    def lessons_count(self):
        return len(self.lessons)
