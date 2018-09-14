from datetime import datetime


class Val(object):
    '''
    Summary
    -------
    An abstract class representing a general value object, to be implemented
    by concrete ones.

    Arguments
    ---------
    * _min: the minimum value accepted
    * _max: the maximum value accepted
    '''

    def __init__(self, _min, _max):
        self._min = _min
        self._max = _max

    def __repr__(self):
        name = self.__class__.__name__
        return f'{name}({self._min}-{self._max})'


class IntVal(Val):
    '''
    Summary
    -------
    Identifies the datastore column value for integers.

    Constructor
    -----------
    >>> ival = IntVal(_min=10, _max=1000)

    Methods
    -------
    call: computes the value as an integer within the valid range, raise an exception otherwise:
    >>> ival('42')
    42
    '''

    MIN = 0
    MAX = 65535

    def __init__(self, _min=MIN, _max=MAX):
        super().__init__(_min, _max)

    def __call__(self, val):
        val = int(val)
        if val < int(self._min) or val > int(self._max):
            raise ValueError(f'{val} is outside of permitted range: {self._min},{self._max}')
        return val


class FloatVal(IntVal):
    '''
    Summary
    -------
    Identifies the datastore column value for floats

    Constructor
    -----------
    >>> fval = FloatVal(_max=3.14)

    Methods
    -------
    call: computes the value as a float within the valid range, raise an exception otherwise:
    >>> fval('2.15')
    2.15
    '''
    def __call__(self, val):
        val = float(val)
        if val < float(self._min) or val > float(self._max):
            raise ValueError(f'{val} is outside of permitted range: {self._min},{self._max}')
        return val


class TxtVal(Val):
    '''
    Summary
    -------
    Identifies the datastore column value for text/string

    Arguments
    ---------
    * _min: the minimum length accepted
    * _max: the maximum length accepted

    Constructor
    -----------
    >>> tval = TxtVal(_min=1, _max=7)

    Methods
    -------
    call: computes the value as a text within the valid range, raise an exception otherwise:
    >>> tval(10000)
    '10000'
    '''

    MIN = 1
    MAX = 64

    def __init__(self, _min=MIN, _max=MAX):
        super().__init__(_min, _max)

    def __call__(self, val):
        val = str(val)
        val_len = len(val)
        if val_len < int(self._min) or val_len > int(self._max):
            raise ValueError(f'{val} length is outside of permitted range: {self._min},{self._max}')
        return val


class DateVal(Val):
    '''
    Summary
    -------
    Identifies the datastore column value for date, supported format is YYYY-MM-DD

    Constructor
    -----------
    >>> dval = DateVal()

    Methods
    -------
    call: computes the value as a date object by parsing accepted format:
    >>> dval('2017-09-11')
    date(2017, 9, 11)
    '''

    REPR = 'YYYY-MM-DD'
    FORMAT = '%Y-%m-%d'

    def __init__(self):
        pass

    def __call__(self, val):
        try:
            return datetime.strptime(val, self.FORMAT).date()
        except ValueError:
            raise ValueError(f'{val} cannot be converted to a valid date')

    def __repr__(self):
        name = self.__class__.__name__
        return f'{name}({self.REPR})'


class TimeVal(DateVal):
    '''
    Summary
    -------
    Identifies the datastore column value for time, supported format is YYYY-MM-DD HH:MM 

    Constructor
    -----------
    >>> tval = TimeVal()

    Methods
    -------
    call: computes the value as a datetime object by parsing accepted format:
    >>> tval('2017-09-11 23:55')
    datetime(2017, 9, 11, 23, 55)
    '''

    REPR = 'YYYY-MM-DD HH:MM'
    FORMAT = '%Y-%m-%d %H:%M'

    def __call__(self, val):
        try:
            return datetime.strptime(val, self.FORMAT)
        except ValueError:
            raise ValueError(f'{val} cannot be converted to a valid datetime')
