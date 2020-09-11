import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = list()

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(
            record.amount for record in self.records
            if record.date == today
            )

    def get_week_stats(self):
        today = dt.date.today()
        day_week_ago = today - dt.timedelta(days=6)

        return sum(
            record.amount for record in self.records
            if day_week_ago <= record.date <= today
            )


class CaloriesCalculator(Calculator):
    POSITIVE_CALORIES_REMAINED = (
        'Сегодня можно съесть что-нибудь ещё, но с '
        'общей калорийностью не '
        'более {calories_remained} кКал'
    )
    NO_CALORIES_REMAINED = (
        'Хватит есть!'
    )

    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained > 0:
            return self.POSITIVE_CALORIES_REMAINED.format(
                calories_remained=calories_remained
                )
        else:
            return self.NO_CALORIES_REMAINED


class CashCalculator(Calculator):
    USD_RATE = 75.20
    EURO_RATE = 88.90
    RUB_RATE = 1

    POSITIVE_CASH_REMAINED = (
        'На сегодня осталось {cash_remained} {currency_name}'
    )
    NEGATIVE_CASH_REMAINED = (
        'Денег нет, держись: твой долг - '
        '{cash_remained} {currency_name}'
    )
    ZERO_CASH_REMAINED = (
        'Денег нет, держись'
    )

    def get_today_cash_remained(self, currency='rub'):
        """Why CURRENCIES on method level.
        
        Dictionary with CURRENCIES on class level works well, but it 
        doesn't pass pytest tests.
        """
        
        CURRENCIES = {
            'rub': ['руб', self.RUB_RATE],
            'usd': ['USD', self.USD_RATE],
            'eur': ['Euro', self.EURO_RATE],
        }

        currency_name, currency_rate = CURRENCIES[currency]
        cash_remained = self.limit - self.get_today_stats()
        
        if cash_remained == 0:
            return self.ZERO_CASH_REMAINED

        cash_remained = round(cash_remained / currency_rate, 2)
        if cash_remained > 0:
            return self.POSITIVE_CASH_REMAINED.format(
                cash_remained=cash_remained,
                currency_name=currency_name,
                )
        else:  # if cash_remained < 0
            cash_remained = abs(cash_remained)
            return self.NEGATIVE_CASH_REMAINED.format(
                cash_remained=cash_remained,
                currency_name=currency_name,
                )
        

class Record:
    DATE_FORMAT = '%d.%m.%Y'
    
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment

        if date is None:
            self.date = dt.date.today()
        else:
            date = dt.datetime.strptime(date, self.DATE_FORMAT)
            self.date = date.date()
