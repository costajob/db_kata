from datetime import datetime

class Val(object):
    '''
    Identifies an abstract class to be implemented by concrete ones.
    Acts as a container for shared functionalities.
    '''

    class RangeError(ValueError):
        '''
        Indicates the value falls within invalid range
        '''


class IntVal(Val):
    '''
    Summary
    -------
    Identifies the datastore column value for integers

    Constructor
    -----------
    >>> IntVal(42, _min=10, _max=1000)
    '''

    MIN = 0
    MAX = 65535

    def __init__(self, val, _min=MIN, _max=MAX):
        self._min = _min
        self._max = _max
        self.val = self._check(val)

    def _check(self, val):
        val = int(val)
        if val < int(self._min) or val > int(self._max):
            raise self.RangeError(f'{val} is outside of permitted range: {self._min},{self._max}')
        return val


class FloatVal(IntVal):
    '''
    Summary
    -------
    Identifies the datastore column value for floats

    Constructor
    -----------
    >>> FloatVal(1.12, _max=3.14)
    '''
    def _check(self, val):
        val = float(val)
        if val < float(self._min) or val > float(self._max):
            raise self.RangeError(f'{val} is outside of permitted range: {self._min},{self._max}')
        return val


class TxtVal(Val):
    '''
    Summary
    -------
    Identifies the datastore column value for text/string

    Constructor
    -----------
    >>> TxtVal('hello', _min=1, _max=7)
    '''

    MIN = 1
    MAX = 64

    def __init__(self, val, _min=MIN, _max=MAX):
        self._min = int(_min)
        self._max = int(_max)
        self.val = self._check(val)

    def _check(self, val):
        val = str(val)
        val_len = len(val)
        if val_len < self._min or val_len > self._max:
            raise self.RangeError(f'{val} length is outside of permitted range: {self._min},{self._max}')
        return val


class DateVal(Val):
    '''
    Summary
    -------
    Identifies the datastore column value for date, supported format is YYYY-MM-DD

    Constructor
    -----------
    >>> DateVal('2017-09-11')
    '''

    FORMAT = '%Y-%m-%d'

    def __init__(self, val):
        self.val = self._check(val)

    def _check(self, val):
        try:
            return datetime.strptime(val, self.FORMAT).date()
        except ValueError:
            raise self.RangeError(f'{val} cannot be converted to a valid date')


class TimeVal(DateVal):
    '''
    Summary
    -------
    Identifies the datastore column value for time, supported format is YYYY-MM-DD HH:MM 

    Constructor
    -----------
    >>> TimeVal('2017-09-11 23:55')
    '''

    FORMAT = '%Y-%m-%d %H:%M'

    def _check(self, val):
        try:
            return datetime.strptime(val, self.FORMAT)
        except ValueError:
            raise self.RangeError(f'{val} cannot be converted to a valid date')
