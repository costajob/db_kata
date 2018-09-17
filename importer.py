import gzip
import pickle
from os import path, stat


class Parser:
    '''
    Summary
    -------
    Parse a pipe separated file with first row serving as header and each subsequent
    ones representing the dataset.

    Arguments
    ---------
    * filename: the path to the pipe separated file data file

    Constructor
    -----------
    >>>  parser = Parser('./sample.txt')

    Methods
    -------
    iter: return a generator with the file contents splitted by separator characters
    >>> for line in parser:
    >>>   ...
    '''

    SEPARATOR = '|'

    def __init__(self, filename):
        self.filename = path.abspath(filename)

    def __iter__(self):
        with open(self.filename, 'r') as f:
            for line in f:
                yield tuple(line.strip().split(self.SEPARATOR))


class Storage:
    '''
    Summary
    -------
    Writes and reads transformed data by un/pickling and un/gzipping them accordingly

    Arguments
    ---------
    * filename: the name of the file that store the data, the '.pickle' extension
      is suffixed if missing

    Constructor
    -----------
    >>> storage = Storage('./projects')

    Methods
    -------
    write: write table data to the specified compressed file, if file exists, read data
           before writing and replace file with merged data (mandatory to keep unique keys)
    >>> worker.write(Table(...))

    read: read the compressed file and return a table object filled by data
    >>> worker.read()
    '''

    EXT = '.pickle'

    def __init__(self, filename):
        self.filename = self._filename(filename)

    def write(self, table):
        table = self._table(table)
        with gzip.open(self.filename, 'wb') as f:
            pickle.dump(table, f)

    def read(self):
        with gzip.open(self.filename, 'rb') as f:
            return pickle.load(f)

    def _filename(self, filename):
        if not filename.endswith(self.EXT):
            filename = '%s%s' % (filename, self.EXT)
        return path.abspath(filename)

    def _table(self, table):
        if self._exist():
            existing = self.read()
            existing + table
            table = existing
        return table

    def _exist(self):
        return path.isfile(self.filename) and stat(self.filename).st_size
