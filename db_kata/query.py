from collections import OrderedDict
import datetime # used by eval
from numbers import Number
from operator import itemgetter
import re
from db_kata.logger import BASE as logger


class Operator(object):
    '''
    Summary
    -------
    An abstract class representing a general operator on data, to be implemented
    by concrete ones.

    Arguments
    ---------
    * query: the columns names, followed by a colon and the aggregate 
      name (if any), separated by comma
    '''

    SPLITTER = ','
    AGGREGATOR = ':'

    class AggregateError(ValueError):
        '''
        Indicates an invalid aggregate has been specified
        '''

    def __init__(self, query):
        self.query = OrderedDict(self._query(query))
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
                valid = ','.join(self.aggregates)
                msg = '%s is not a valid aggregate: %s' % (aggregate, valid)
                logger.error(msg)
                raise self.AggregateError(msg)


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
    call: return a generator with the data selected by specified names
    >>> selector = Selector('PROJECT,SHOT,VERSION')
    >>> selector(Table(...))

    call: if group is specified, group data by available aggregates
    >>> selector = Selector('PROJECT,SHOT:count,VERSION:collect', 'PROJECT')
    >>> selector(Table(...))
    '''

    def __init__(self, query, group=None):
        super().__init__(query)
        self.group = group
    
    def __call__(self, data):
        if self.group:
            logger.info('grouping data by: %r', self.names)
            yield from self._group_by(data)
        else:
            logger.info('selecting data by: %r', self.names)
            yield from self._select(data)

    def _select(self, data):
        for row in data:
            selected = OrderedDict()
            for qname in self.names:
                for name, value in row:
                    if qname == name:
                        selected[name] = value
            yield(tuple(selected.items()))

    def _group_by(self, data):
        self._check_aggregate()
        for group in self._groups(data).values():
            yield(self._aggregate(group))

    def _groups(self, data):
        groups = OrderedDict()
        for row in self._select(data):
            for name, value in row:
                if name == self.group:
                    if value not in groups:
                        groups[value] = []
                    groups[value].append(row)
        return groups

    def _aggregate(self, group):
        reduced = OrderedDict()
        for row in group:
            for name, value in row:
                aggregate = self.query[name]
                if aggregate:
                    logger.debug('aggergating by %s', aggregate)
                    fn = getattr(self, '_ag_%s' % aggregate)
                    fn(name, OrderedDict(row), reduced)
                else:
                    reduced[name] = value
        return self._transform(reduced)

    def _transform(self, reduced):
        for name, value in reduced.items():
            if isinstance(value, set):
                aggregate = self.query[name]
                if aggregate == 'collect':
                    items = ','.join(sorted(str(e) for e in value))
                    reduced[name] = '[%s]' % items
                elif aggregate == 'count':
                    reduced[name] = '(%d)' % len(value)
        return tuple(reduced.items())

    def _ag_max(self, name, row, reduced):
        if name not in reduced:
            reduced[name] = row[name]
        if reduced[name] < row[name]:
            reduced[name] = row[name]

    def _ag_min(self, name, row, reduced):
        if name not in reduced:
            reduced[name] = row[name]
        if reduced[name] > row[name]:
            reduced[name] = row[name]

    def _ag_sum(self, name, row, reduced):
        if isinstance(row[name], Number):
            if name not in reduced:
                reduced[name] = 0
            reduced[name] += row[name]

    def _ag_collect(self, name, row, reduced):
        if name not in reduced:
            reduced[name] = set()
        reduced[name].add(row[name])
    
    def _ag_count(self, name, row, reduced):
        self._ag_collect(name, row, reduced)


class Sorter(Operator):
    '''
    Summary
    -------
    Sort the specified data by columns name.

    Methods
    -------
    call: return a generator with data sorted by specified names
    >>> sorter = Sorter('PROJECT,SHOT,VERSION')
    >>> sorter(Table(...))
    '''

    def __call__(self, data):
        logger.info('sorting data by: %r', self.names)
        data = (OrderedDict(row) for row in data)
        for row in sorted(data, key=itemgetter(*self.names)):
            yield(tuple(row.items()))


class Filter(Operator):
    '''
    Summary
    -------
    Filter the specified data by specified query language which 
    evaluates boolean AND and OR expressions in the following format:
    >>> 'PROJECT="the hobbit" AND SHOT=1 OR SHOT=40'

    AND has higher precedence than OR, parentheses can be used to 
    change this:
    >>> 'PROJECT="the hobbit" AND (SHOT=1 OR SHOT=40)'

    Arguments
    ---------
    * query: the filtering query language

    Methods
    -------
    call: return a generator with the filtered data by specified query
    >>> fil = Filter('PROJECT="the hobbit" OR PROJECT="lotr"')
    >>> fil(Table(...))
    '''

    REGEX = re.compile(r'(\bAND\b|\bOR\b|=|\(|\))')
    OPERANDS = {'OR', 'AND', '(', ')'}
    EQUAL = '='

    def __init__(self, query):
        self.tokens = list(self._tokenize(query))

    def __call__(self, table):
        logger.info('filtering data by: %s', ' '.join(self.tokens))
        translation = self._translate(table)
        for row in table:
            evaluation = translation
            for name, value in row:
                evaluation = evaluation.replace(name, repr(value))
            logger.info('evaluating expression: %s', evaluation)
            if(eval(evaluation)):
                yield(row)
    
    def _translate(self, table):
        translation = []
        names = table.column_names
        for token in self.tokens:
            if token in names:
                translation.append(token)
                col = [col for col in table.columns if col.name == token][0]
            elif token == self.EQUAL:
                translation.append('==')
            elif token in self.OPERANDS:
                translation.append(token.lower())
            else:
                if col:
                    translation.append(repr(col.value(token)))
        return ' '.join(translation)

    def _tokenize(self, query):
        for token in self.REGEX.split(query):
            token = token.strip()
            token = token.replace('"', '')
            if token:
                yield(token)


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
            logger.debug('yielding row: %r', row)
            yield(tuple(value for _, value in row))
