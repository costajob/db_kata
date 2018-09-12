from hashlib import md5
import values as v


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
        return f'Column({self.name}, {self.value}, key={self.key})'


project = Column('PROJECT', v.TxtVal(), True, desc='the project name or code name of the shot')
shot    = Column('SHOT', v.TxtVal(), True, desc='the name of the shot')
version = Column('VERSION', v.IntVal(), True, desc='the current version of the file')
status  = Column('STATUS', v.TxtVal(_max=32), desc='the current status of the shot')
finish  = Column('FINISH_DATE', v.DateVal(), desc='the date the work on the shot is scheduled to end')
bid     = Column('INTERNAL_BID', v.FloatVal(), desc='the amount of days we estimate the work on this shot will take')
created = Column('CREATED_DATE', v.TimeVal(), desc='the time and date when this record is being added to the system')
COLUMNS = (project, shot, version, status, finish, bid, created)


class Table:
    '''
    Summary
    -------
    Represents the data table within the datastore.

    Arguments
    ---------
    * columns: a list of columns objects

    Constructor
    -----------
    >>> table = Table([Column('PROJECT', values.TxtVal(), ...), ...])

    Methods
    -------
    append: appends the specified row data, replacing existing ones by combined keys
    >>> table.append(['the hobbit', '1', '64', ...])

    merge: merges the specified list of rows data, relying on append
    >>> table.merge([['the hobbit', '1', ...], ['king kong', '42'], ...])

    clear: purge all collected rows
    >>> table.clear()
    '''

    class RowError(ValueError):
        '''
        Indicates an invalid row has been appended to the table
        '''

    def __init__(self, columns=COLUMNS):
        self.columns = columns
        self.rows = {}

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return (row for row in self.rows.values())
    
    def __contains__(self, _id):
        return _id in self.rows

    def __getitem__(self, _id):
        return self.rows[_id]

    def clear(self):
        self.rows.clear()

    def merge(self, rows):
        for row in rows:
            self.append(row)

    def append(self, row):
        self._check(row)
        keys = []
        data = []
        for col, val in zip(self.columns, row):
            val = col.value(val)
            data.append(val)
            self._keys(keys, col, val)
        _id = self._id(keys)
        self.rows[_id] = data

    def _check(self, row):
        if len(row) != len(self.columns):
            raise self.RowError('row data does not match column specification')

    def _keys(self, keys, column, val):
        if column.key:
            keys.append(str(val))

    def _id(self, keys):
        if keys:
            return md5(''.join(keys).encode()).hexdigest()
