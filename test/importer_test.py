from datetime import date, datetime
from tempfile import NamedTemporaryFile
import unittest
import importer as im


class TestImporter(unittest.TestCase):
    def setUp(self):
        self.worker = im.Worker('./sample.txt')
        self.temp = NamedTemporaryFile(mode='w+', suffix='.txt')

    def test_worker_data(self):
        self.assertEqual(self.worker.headers, ['PROJECT', 'SHOT', 'VERSION', 'STATUS', 'FINISH_DATE', 'INTERNAL_BID', 'CREATED_DATE'])
        self.assertEqual(self.worker.raw[-1], ['king kong', '42', '128', 'not required', '2006-07-22', '30.00', '2006-10-15 09:14'])

    def test_worker_write(self):
        self.worker.write(self.temp.name)
        lines = [l for l in self.temp]
        self.assertEqual(lines[0], 'PROJECT|SHOT|VERSION|STATUS|FINISH_DATE|INTERNAL_BID|CREATED_DATE\n')
        self.assertEqual(lines[-1], 'the hobbit|40|32|finished|2010-05-15|22.8|2010-03-22 01:10\n')

    def test_worker_read(self):
        self.worker.write(self.temp.name)
        data = self.worker.read(self.temp.name)
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], ['the hobbit', '1', 64, 'scheduled', date(2010, 5, 15), 45.0, datetime(2010, 4, 1, 13, 35)])
        self.assertEqual(data[-1], ['the hobbit', '40', 32, 'finished', date(2010, 5, 15), 22.8, datetime(2010, 3, 22, 1, 10)])


if __name__ == '__main__':
    unittest.main()
