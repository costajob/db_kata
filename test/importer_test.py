from tempfile import NamedTemporaryFile
import unittest
import datastore as ds
import importer as im
from stubs.constants import COLUMNS, ROWS, TABLE


class TestImporter(unittest.TestCase):
    def setUp(self):
        temp = NamedTemporaryFile(mode='w+', suffix='.pickle')
        self.storage = im.Storage(temp.name)

    def test_parser(self):
        parser = im.Parser('./stubs/sample.txt')
        data = list(parser)
        self.assertEqual(data[0], ('PROJECT', 'SHOT', 'VERSION', 'STATUS', 'FINISH_DATE', 'INTERNAL_BID', 'CREATED_DATE'))
        self.assertEqual(data[-1], ('king kong', '42', '128', 'not required', '2006-07-22', '30.00', '2006-10-15 09:14'))

    def test_storage_filename(self):
        storage = im.Storage('./stubs/projects')
        self.assertTrue(storage.filename.endswith('/weta_python/stubs/projects.pickle'))

    def test_storage_io(self):
        self.storage.write(TABLE)
        table = self.storage.read()
        self.assertEqual(table.rows, TABLE.rows)

    def test_storage_augment(self):
        table = ds.Table(COLUMNS)
        table.merge(ROWS[1:2])
        self.storage.write(table)
        other = ds.Table(COLUMNS)
        other.merge(ROWS[1:4])
        self.storage.write(other)
        table = self.storage.read()
        self.assertEqual(len(table), 3)


if __name__ == '__main__':
    unittest.main()
