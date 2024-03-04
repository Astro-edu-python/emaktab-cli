import datetime
from enum import Enum


class MonthFilterRu(Enum):
    january = 'янв'
    february = 'фев'
    march = 'март'
    april = 'апр'
    mai = 'ма'
    june = 'июн'
    july = 'июл'
    august = 'авгу'
    september = 'сентя'
    october = 'октя'
    november = 'ноя'
    december = 'дека'

    @staticmethod
    def convert_to_enum_by_month_name(str_month: str):
        for key, value in MonthFilterRu.__members__.items():
            filter_value = value.value
            if len(str_month) == 3:
                return MonthFilterRu.mai
            if str_month.lower()[:3] in filter_value:
                return getattr(MonthFilterRu, key)


def resolve_month_date(
    date_str: str, delimiter: str,
    datetime_format: str = '%d.%m.%Y'
) -> tuple[datetime.datetime, datetime.datetime]:
    start_str_date, end = date_str.split(delimiter)
    start_str_date: str = start_str_date.strip()
    date_end_str, month_str, end_year = end.strip().split()
    month = MonthFilterRu.convert_to_enum_by_month_name(month_str).name
    if len(start_str_date.split()) == 2:
        prev_date = datetime.datetime.strptime(
            start_str_date + ' ' + end_year, datetime_format
        )
    else:
        prev_date = datetime.datetime.strptime(
            start_str_date + ' ' + month + ' ' + end_year,
            datetime_format
        )
    end_date = datetime.datetime.strptime(
        date_end_str + ' ' + month + ' ' + end_year, datetime_format
    )
    return prev_date, end_date
