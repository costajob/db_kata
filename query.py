from operator import itemgetter


class Operator(object):
    '''
    Summary
    -------
    An abstract class representing a general operator on data, to be implemented
    by concrete ones.

    Arguments
    ---------
    * query: the columns names, separated by comma
    '''

    def __init__(self, query):
        self.query = self._query(query)

    def _query(self, query):
        return tuple(name.strip() for name in str(query).split(','))



class Selector(Operator):
    '''
    Summary
    -------
    Selects the specified data by columns name.

    Methods
    -------
    call: return a generator with the data selected by the specified tuple of pairs
    >>> selector = Selector('PROJECT,SHOT,VERSION')
    >>> selector(Table(...))
    '''

    def __call__(self, data):
        for row in data:
            yield(tuple((name, value) for name, value in row if name in self.query))


class Sorter(Operator):
    '''
    Summary
    -------
    Sort the specified data by columns name.

    Methods
    -------
    call: return a generator with the sorted data by the specified tuple of pairs
    >>> sorter = Sorter('PROJECT,SHOT,VERSION')
    >>> sorter(Table(...))
    '''

    def __call__(self, data):
        data = (dict(row) for row in data)
        for row in sorted(data, key=itemgetter(*self.query)):
            pairs = tuple((k, v) for k, v in row.items())
            yield(pairs)

class Filter:
    '''
    Summary
    -------
    Filter the specified data by specified column value.

    Arguments
    ---------
    * query: the column name and value, separated by equal character

    Methods
    -------
    call: return a generator with the filtered data by the specified table
    >>> fil = Filter('FINISH_DATE=2006-07-22')
    >>> fil(Table(...))
    '''

    def __init__(self, query):
        self.name, self.value = self._query(query)

    def __call__(self, table):
        qname, qvalue = self._convert(table)
        for row in table:
            for name, value in row:
                if name == qname and value == qvalue:
                    yield(row)

    def _query(self, query):
        return tuple(name.strip() for name in str(query).split('='))
    
    def _convert(self, table):
        columns = [col for col in table.columns if col.name == self.name]
        if columns:
            col = columns[0]
            return self.name, col.value(self.value)


class Bulk:
    '''
    Summary
    -------
    Applies multiple operators to the specified table object


    Arguments
    ---------
    * _filter: the filtering operator, a callable accepting a single data argument
    * order: the sorter operator, a callable accepting a single data argument
    * select: the selector operator, a callable accepting a single data argument

    Constructor
    -----------
    >>> bulk = Bulk(_filter=Filter(...), order=Sorter(...), select=Selector(...))

    Methods
    -------
    call: return a generator by apply the operators to the table data
    >>> bulk(Table(...))
    '''

    PLAIN = lambda _, x: x

    def __init__(self, _filter, order, select):
        _filter = _filter or self.PLAIN
        order = order or self.PLAIN
        select = select or self.PLAIN
        self.operators = (_filter, order, select)

    def __call__(self, data):
        for op in self.operators:
            data = op(data)
        for row in data:
            yield(tuple(value for _, value in row))
