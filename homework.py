import datetime as dt
from typing import Optional, Union

date_format = '%d.%m.%Y'


class Record:
    def __init__(self, amount: int, comment: str, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format)


class Calculator:
    def __init__(self, limit: Union[float, int]):
        self.records: list[Record] = []
        self.limit = limit

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) -> Union[float, int]:
        return sum(
            record.amount for record in self.records
            if record.date == dt.date.today()
        )

    def get_week_stats(self) -> Union[float, int]:
        today = dt.date.today()
        week_start = today - dt.timedelta(days=7)
        return sum(
            record.amount for record in self.records
            if week_start <= record.date <= today
        )

    def get_limit_today(self) -> Union[float, int]:
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        return (
            f'Please eat yet = {limit_today}'
            if (limit_today := self.get_limit_today()) > 0
            else 'Do not eat!)'
        )


class CashCalculator(Calculator):
    USD_RATE: float = 93.0
    EUR_RATE: float = 102.1
    RUB_RATE: float = 1.0
    CALC_ACCURACY: int = 2

    def get_today_cash_remained(self, currency: str) -> str:
        money: dict[str, tuple[float, str]] = {
            'usd': (self.USD_RATE, '$'),
            'eur': (self.EUR_RATE, '€'),
            'rub': (self.RUB_RATE, '₽')
        }

        if currency not in money:
            return 'Currency is not in [usd, eur, rub]'

        limit_today = self.get_limit_today()

        if limit_today == 0:
            return 'No money!)'

        rate, currency_icon = money[currency]

        cash_today = round(limit_today / rate, self.CALC_ACCURACY)

        if limit_today > 0:
            return f'for coast is {cash_today}{currency_icon}'
        return f'your dolg is {cash_today}{currency_icon}'


def main() -> None:
    """Главная функция."""
    # для CashCalculator
    r1 = Record(amount=145, comment='Безудержный шопинг')
    r2 = Record(amount=1568, comment='Наполнение потребительской корзины')
    r3 = Record(amount=691, comment='Катание на такси', date='08.03.2019')

    # для CaloriesCalculator
    r4 = Record(amount=1186, comment='Кусок тортика. И ещё один.',
                date='24.02.2019')
    r5 = Record(amount=84, comment='Йогурт.')
    r6 = Record(amount=1140, comment='Баночка чипсов.', date='24.02.2019')

    # create classes
    cash_calculator = CashCalculator(3000)
    calories_calculator = CaloriesCalculator(3000)

    cash_calculator.add_record(r1)
    cash_calculator.add_record(r2)
    cash_calculator.add_record(r3)

    calories_calculator.add_record(r4)
    calories_calculator.add_record(r5)
    calories_calculator.add_record(r6)

    #   print(cash_calculator.get_limit_today())
    #   print(cash_calculator.get_today_cash_remained('eur'))
    print(calories_calculator.get_limit_today())
    print(calories_calculator.get_calories_remained())


if __name__ == '__main__':
    main()
