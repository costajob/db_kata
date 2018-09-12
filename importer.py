from os import path
import datastore as ds
import values as v


class Worker:
    '''
    Summary
    -------
    Imports a pipe separated file with first row serving as header and each subsequent
    ones representing the dataset.

    Arguments
    ---------
    * src: the path to the raw data file
    * table: the table object used to transform raw data on load, read and write

    Constructor
    -----------
    >>> worker = Worker('./sample.txt', Table(COLUMNS))

    Methods
    -------
    write: store transformed and reduced data to the specified txt file
    >>> worker.write('./datastore.txt')

    read: read data back from stored file
    >>> worker.read('./datastore.txt')
    '''

    SEPARATOR = '|'

    def __init__(self, src, table=ds.Table()):
        self.table = table
        self.headers, self.raw = self._load(src)

    def write(self, filename):
        self._sort_columns()
        self.table.merge(self.raw)
        with open(path.abspath(filename), 'w+') as f:
            print(self.SEPARATOR.join(self.headers), file=f)
            for row in self.table:
                print(self.SEPARATOR.join(self._val(v) for v in row), file=f)

    def read(self, filename):
        headers, raw = self._load(filename)
        self._sort_columns(headers)
        self.table.clear()
        self.table.merge(raw)
        return list(self.table)

    def _val(self, val):
        if hasattr(val, 'strptime'):
            val = val.strftime(v.TimeVal.FORMAT)
        return str(val)

    def _sort_columns(self, headers=None):
        headers = headers or self.headers
        columns  = {column.name: column for column in self.table.columns}
        self.table.columns = [columns[name] for name in headers]

    def _load(self, src=None):
        src = src or self.src
        with open(path.abspath(src), 'r') as f:
            data = [l.strip().split(self.SEPARATOR) for l in f]
            return data.pop(0), data
