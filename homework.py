import datetime as dt


class Calculator:
    """Basic class for extended calculators.
    
    It's a basic class that stores the records of Record class. 
    Two methods return sums of the daily and weekly amount.
    The parameter 'limit' doesn't use there. It is used in child classes. 
    """

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
        day_week_ago = today - dt.timedelta(days=7)

        return sum(
            record.amount for record in self.records
            if day_week_ago < record.date <= today
            )


class CaloriesCalculator(Calculator):
    """CaloriesCalculator overview.

    In addition to parent class it sums daily calories and returns 
    how much left for today.
    If a limit is reached it reminds about it.
    """

    REMAINED = (
        'Сегодня можно съесть что-нибудь ещё, но с '
        'общей калорийностью не '
        'более {calories_remained} кКал'
    )
    CALORIES_LEFT = (
        'Хватит есть!'
    )

    def get_calories_remained(self):
        calories = self.limit - self.get_today_stats()
        if calories > 0:
            return self.REMAINED.format(calories_remained=calories)
        
        # remained <= 0
        return self.CALORIES_LEFT


class CashCalculator(Calculator):
    """CashCalculator overview.

    In addition to parent class it sums daily cash and returns 
    how much left for today.
    If currency specified an answer returns in that currency.
    If a limit is reached it reminds about it.
    If a limit is exceeded it returns a debt amount.
    """

    USD_RATE = 75.20
    EURO_RATE = 88.90
    RUB_RATE = 1

    REMAINED = (
        'На сегодня осталось {cash_remained} {currency_name}'
    )
    EXCEEDED = (
        'Денег нет, держись: твой долг - '
        '{cash_remained} {currency_name}'
    )
    CASH_LEFT = (
        'Денег нет, держись'
    )

    def get_today_cash_remained(self, currency='rub'):
        """Why CURRENCIES on method level.
        
        Dictionary with CURRENCIES on class level works well, but it 
        doesn't pass pytest tests.
        """
        
        CURRENCIES = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
        }

        name, rate = CURRENCIES[currency]
        cash = self.limit - self.get_today_stats()
        
        if cash == 0:
            return self.CASH_LEFT

        cash = round(cash / rate, 2)
        if cash > 0:
            return self.REMAINED.format(
                cash_remained=cash,
                currency_name=name,
                )
        
        # cash < 0
        cash = abs(cash)
        return self.EXCEEDED.format(
            cash_remained=cash,
            currency_name=name,
            )
        

class Record:
    """Stores records in a convenient form for calculator purposes."""

    DATE_FORMAT = '%d.%m.%Y'
    
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment

        if date is None:
            self.date = dt.date.today()
        else:
            date = dt.datetime.strptime(date, self.DATE_FORMAT)
            self.date = date.date()
