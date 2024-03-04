from dataclasses import dataclass


@dataclass
class Pupil:
    last_name: str
    first_name: str
    surname: str | None = None


@dataclass
class ClassInfo:
    school_number: int
    pupil_class: str
    academic_start_year: int
    academic_end_year: int
    pupils: list[Pupil]

    @property
    def pupils_count(self) -> int:
        return len(self.pupils)
