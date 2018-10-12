from collections import OrderedDict
from hashlib import md5
from db_kata.logger import BASE as logger


class Column:
    '''
    Summary
    -------
    Represents a logical columns within the datastore.

    Arguments
    ---------
    * name: the name of the column
    * value: the kind of the column, one of the instances specified in the values module
    * key: indicates if the column is a unique key
    * desc: an optional description

    Constructor
    -----------
    >>> Column('VERSION', values.IntVal(), key=True, desc='the current version of the file')
    '''

    def __init__(self, name, value, key=False, desc=''):
        self.name = str(name)
        self.value = value
        self.key = key
        self.desc = str(desc)

    def __repr__(self):
        return 'Column(%s, %s, key=%s)' % (self.name, self.value, self.key)


class Table:
    '''
    Summary
    -------
    Represents the data table within the datastore.

    Arguments
    ---------
    * columns: a list of columns objects
    * rows: a dict with 

    Constructor
    -----------
    >>> table = Table([Column('PROJECT', values.TxtVal(), ...), ...])

    Methods
    -------
    Table.factory: factory a table object by raw data, sorting accordingly the columns
    >>> table = Table.factory([['PROJECT', 'SHOT', ...], ['the hobbit', '1', ...],...], COLUMNS)

    append: appends the specified row data, replacing existing ones by combined keys
    >>> table.append(['the hobbit', '1', '64', ...])

    merge: merges the specified list of rows data, relying on append
    >>> table.merge([['the hobbit', '1', ...], ['king kong', '42'], ...])

    +: modify left table by adding tranformed rows from another table object
       rows with same id are replaced by new data
    >>> table + Table.factory(...)

    iter: iterates over the values of rows
    >>> for row in table:
            ...
    '''

    class DataError(ValueError):
        '''
        Indicates invalid data have been tried to be appended to the table
        '''

    @classmethod
    def factory(cls, data, columns):
        table = cls(columns)
        for i, row in enumerate(data): 
            if i == 0:
                table._sort(row)
            else:
                table.append(row)
        return table

    def __init__(self, columns):
        self.columns = columns
        self.rows = OrderedDict()

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        for row in self.rows.values():
            yield tuple(zip(self.column_names, row))
    
    def __contains__(self, _id):
        return _id in self.rows

    def __getitem__(self, _id):
        return self.rows[_id]

    def __add__(self, other):
        self.rows.update(other.rows)

    def __repr__(self):
        names = ', '.join(self.column_names)
        return 'Table(columns=(%s), rows=%d)' % (names, len(self.rows))

    @property
    def column_names(self):
        return tuple(col.name for col in self.columns)

    def merge(self, rows):
        for row in rows:
            self.append(row)

    def append(self, row):
        self._check(row)
        logger.info('appending row: %r', row)
        keys = []
        data = []
        for col, val in zip(self.columns, row):
            val = col.value(val)
            data.append(val)
            self._keys(keys, col, val)
        _id = self._id(keys)
        self.rows[_id] = tuple(data)

    def _check(self, row):
        if len(row) != len(self.columns):
            msg = 'row data does not match column specification'
            logger.error('%s: %r', msg, self.column_names)
            raise self.DataError(msg)

    def _keys(self, keys, column, val):
        if column.key:
            keys.append(str(val))

    def _id(self, keys):
        if keys:
            return md5(''.join(keys).encode()).hexdigest()
    
    def _sort(self, headers):
        logger.info('sorting according to headers: %r', headers)
        columns  = {column.name: column for column in self.columns}
        self.columns = [columns[name] for name in headers]
