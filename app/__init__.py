from undetected_chromedriver import Chrome
from termcolor import colored

from .config import EMAKTAB_LOGIN, EMAKTAB_PASSWORD
from .clicker import EMaktabClicker
from .core import EmaktabManager
from .parser import EmaktabClassInfoParser, EmaktabScheduleLessonsParser
from .types.class_info import Pupil


def run():
    commands = [
        'Парсинг информации о классе(школа/класс/учебный год/ученики)',
        'Парсинг расписания'
    ]
    command = int(input(
        colored(
            'Добро пожаловать на EMaktab!\nВведите номер команды:\n',
            'yellow', attrs=['bold'], force_color=True
        ) + colored(
            '\n'.join((
                f'\t{idx}: {value}'
                for idx, value in enumerate(commands, start=1)
            )) + '\nВвод: ', 'green', force_color=True
        )))
    if command > len(commands):
        print(colored('Команда не существует!', 'red', attrs=['bold'], force_color=True))
        return
    emaktab_clicker = EMaktabClicker(
        Chrome(headless=True),
        EMAKTAB_LOGIN,
        EMAKTAB_PASSWORD
    )
    manager = EmaktabManager(emaktab_clicker)
    match command:
        case 1:
            class_info = manager.parse_class_info()
            first_header = colored(
                f'ШКОЛА №{class_info.school_number}',
                'red', attrs=['bold'], force_color=True
            )
            academic_year = colored(
                f'Учебный год: {class_info.academic_start_year}/'
                f'{class_info.academic_end_year} г.',
                'yellow', force_color=True
            )
            class_ = colored(
                f'Класс ученика: {class_info.pupil_class}',
                'blue', force_color=True
            )
            pupils_info = "\n".join(map(
                lambda tup_: f'{tup_[0]}: {tup_[1].last_name} {tup_[1].first_name} {tup_[1].surname}',
                enumerate(class_info.pupils, start=1)
            ))
            pupils = colored(
                f'Ученики класса:\n{pupils_info}\nОбщ. кол-во учеников {class_info.pupils_count} шт.',
                'light_blue', force_color=True
            )
            print(first_header, academic_year, class_, pupils, sep='\n')
        case 2:
            print(manager.parse_week_lessons())
