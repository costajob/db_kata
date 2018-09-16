from collections import defaultdict
from numbers import Number
from operator import itemgetter


class Operator(object):
    '''
    Summary
    -------
    An abstract class representing a general operator on data, to be implemented
    by concrete ones.

    Arguments
    ---------
    * query: the columns names followed by a colon and the
      aggregate name (if any), than a comma before the next column name
    '''

    SPLITTER = ','
    AGGREGATOR = ':'

    class AggregateError(ValueError):
        '''
        Indicates an invalid aggregate has been specified
        '''

    def __init__(self, query):
        self.query = dict(self._query(query))
        self.names = tuple(self.query.keys())
        self.aggregates = {name[4:] for name in dir(self) if name.startswith('_ag_')}

    def _query(self, query):
        for name in str(query).split(self.SPLITTER):
            if self.AGGREGATOR in name:
                yield(name.strip().split(self.AGGREGATOR))
            else:
                yield(name.strip(), None)

    def _check_aggregate(self):
        for aggregate in self.query.values():
            if aggregate and aggregate not in self.aggregates:
                raise self.AggregateError(f'{aggregate} is not a valid aggregate: {",".join(self.aggregates)}')


class Selector(Operator):
    '''
    Summary
    -------
    Selects the specified data by column names.

    Optionally groups by specified column name and the available aggregates:
    * min: select the minimum value from a column 
    * max: select the maximum value from a column 
    * sum: select the summation of all numeric values in a column 
    * count: count the distinct values in a column
    * collect: collect the distinct values in a column

    Methods
    -------
    call: return a generator with the data selected by the specified 
          tuple of pairs, if group is specified, group them by available
          aggregates
    >>> selector = Selector('PROJECT,SHOT,VERSION')
    >>> selector(Table(...))
    >>> # grouping by PROJECT, aggregating SHOT and VERSION
    >>> selector = Selector('PROJECT,SHOT:count,VERSION:collect')
    >>> selector(Table(...), 'PROJECT')
    '''

    def __init__(self, query, group=None):
        super().__init__(query)
        self.group = group
    
    def __call__(self, data):
        if self.group:
            yield from self._group_by(data)
        else:
            yield from self._select(data)

    def _select(self, data):
        for row in data:
            selected = {}
            for qname in self.names:
                for name, value in row:
                    if qname == name:
                        selected[name] = value
            yield(tuple(selected.items()))

    def _group_by(self, data):
        self._check_aggregate()
        for group in self._groups(data).values():
            if len(group) == 1:
                yield(group[0])
            else:
                yield(self._aggregate(group))

    def _groups(self, data):
        groups = defaultdict(list)
        for row in self._select(data):
            for name, value in row:
                if name == self.group:
                    groups[value].append(row)
        return groups

    def _aggregate(self, group):
        reduced = {}
        for data in group:
            for name, value in data:
                aggregate = self.query[name]
                if aggregate:
                    fn = getattr(self, f'_ag_{aggregate}')
                    fn(name, dict(data), reduced)
                else:
                    reduced[name] = value
        return self._transform(reduced)

    def _transform(self, reduced):
        for name, value in reduced.items():
            if isinstance(value, set):
                aggregate = self.query[name]
                if aggregate == 'collect':
                    items = ','.join(sorted(str(e) for e in value))
                    reduced[name] = f'[{items}]'
                elif aggregate == 'count':
                    reduced[name] = len(value)
        return tuple(reduced.items())

    def _ag_max(self, name, data, reduced):
        if name not in reduced:
            reduced[name] = data[name]
        if reduced[name] < data[name]:
            reduced[name] = data[name]

    def _ag_min(self, name, data, reduced):
        if name not in reduced:
            reduced[name] = data[name]
        if reduced[name] > data[name]:
            reduced[name] = data[name]

    def _ag_sum(self, name, data, reduced):
        if isinstance(data[name], Number):
            if name not in reduced:
                reduced[name] = 0
            reduced[name] += data[name]

    def _ag_collect(self, name, data, reduced):
        if name not in reduced:
            reduced[name] = set()
        reduced[name].add(data[name])
    
    def _ag_count(self, name, data, reduced):
        self._ag_collect(name, data, reduced)


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
        for row in sorted(data, key=itemgetter(*self.names)):
            yield(tuple(row.items()))


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
