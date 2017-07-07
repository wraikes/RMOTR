from decimal import Decimal


class Book():
    def __init__(self, title, authors, price_amount, price_currency):
        self.title = title
        self.authors = authors
        self.price_amount = price_amount
        self.price_currency = price_currency
        

    @property
    def price(self):
        # create an instance of `Price`, using the book's attributes
        self.price = Price(self.price_amount)
        return self.price

    def __str__(self):

        return '{0} (by {1}) - {2}${3}'.format(self.title, 
                                               self.authors,
                                               self.price_currency,
                                               self.price_amount)

class Price():
    EXCHANGE_RATES = {
        'USD': {
            'EUR': Decimal('0.89'),
            'YEN': Decimal('109.8')
        },
        'EUR': {
            'USD': Decimal('1.13'),
            'YEN': Decimal('123.6')
        },
        'YEN': {
            'USD': Decimal('0.0091'),
            'EUR': Decimal('0.0081')
        },
    }

    def __init__(self, amount, currency='USD'):
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return "{} {}".format(self.amount, self.currency)

    def get_currency(self):
        return self.currency

    def __add__(self, other):
        # return a new `Price` instance, representing the sum of
        # both given ones
        new_amount = self.amount + other.get_value(self.currency)
        
        return Price(new_amount, self.currency)

    def __eq__(self, other):
        # compare if two prices are equal. Keep in mind that both prices
        # might have different currencies. Use the `.get_value()` function
        # to transform prices to a comparable currency.
        return self.amount == other.get_value(self.currency)

    def __ne__(self, other):
        # opposite to __eq__
        return self.amount != other.get_value(self.currency)

    def get_value(self, currency=None):
        # if no currency is given, returns the current price amount. If a
        # different currency is given, handles the price convertion to the
        # given currency. Use the `EXCHANGE_RATES` dict for that.
        if not currency or currency == self.currency:
            return self.amount
        
        else:
            conv_metric = self.EXCHANGE_RATES[self.currency][currency] 
            return self.amount * conv_metric

class BookIterator():
    def __init__(self, file_path):
        self.lines = read_file_line_by_line(file_path)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # make sure each execution of __next__ returns an instance
        # of the `Book` class.        
        try:
            line = self.lines[self.index]
            result = Book(line[0], line[1], line[2], line[3])
            self.index += 1
            
        except IndexError:
            raise StopIteration

        return result
        
    next = __next__


def read_file_line_by_line(file_path):
    file_lines = []
    file_obj = open(file_path, 'r')
    try:
        line = file_obj.readline()
        while line:
            book_data = [l.strip() for l in line.split(',')]
            file_lines.append(book_data)
            line = file_obj.readline()
    finally:
        file_obj.close()
    return file_lines
