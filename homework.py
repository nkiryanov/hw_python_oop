import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = list()
        self.daily_stats = dict()
        # self.records is used for storing transactions only
        # self.dict for storing dayly stats and for generating weekly stats.
        # dict works faster and easier to use for lot of records in this case.
        # key = date, value = sum of daily amounts

    def add_record(self, record):
        # Add record to records list
        self.records.append(record)

        # Save daily amounts in dict organised by date
        if record.date not in self.daily_stats:
            self.daily_stats[record.date] = record.amount
        else:
            self.daily_stats[record.date] += record.amount

    def get_today_stats(self, today=None):
        # The func returns today stats by dafault
        # If date (today) is givien it return
        # specific date stats
 
        if today is None:
            today = dt.datetime.now()
            today_date = today.date()
        else:
            today_date = today

        if today_date in self.daily_stats:
            return self.daily_stats[today_date]
        else:
            return 0

    def get_week_stats(self):
        # The func return weekly stats
        # It's sum daily stats that stores in dict
        # for 7 days before today

        today = dt.datetime.now()
        today_date = today.date()
        period = dt.timedelta(days=1)
        week_stats = 0

        for i in range(7):
            date_to_sum = today_date - period * i
            week_stats += self.get_today_stats(date_to_sum)

        return week_stats


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с '
                    f'общей калорийностью не '
                    f'более {calories_remained} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 76.0
    EURO_RATE = 92.0

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency='rub'):
        currency_output = {'rub': 'руб',
                           'usd': 'USD',
                           'eur': 'Euro'}
        

        cash_reminded = self.limit - self.get_today_stats()

        if currency == 'usd':
            cash_reminded = cash_reminded / self.USD_RATE
            cash_reminded = float(format(cash_reminded, '.2f'))
        elif currency == 'eur':
            cash_reminded = cash_reminded / self.EURO_RATE
            cash_reminded = float(format(cash_reminded, '.2f'))

        if cash_reminded > 0:
            return (f'На сегодня осталось {cash_reminded} '
                    f'{currency_output[currency]}')
        elif cash_reminded == 0:
            return 'Денег нет, держись'
        else:  # if cash_reminded < 0
            cash_reminded = abs(cash_reminded)
            return (f'Денег нет, держись: твой долг - '
                    f'{cash_reminded} {currency_output[currency]}')


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            now = dt.datetime.now()
            self.date = now.date()
        else:
            date = dt.datetime.strptime(date, '%d.%m.%Y')
            self.date = date.date()

    def __str__(self):
        return f'amount = {self.amount}, date = {self.date}'
