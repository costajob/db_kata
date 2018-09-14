from datetime import date, datetime
import unittest
import query as qy
from stubs.constants import TABLE


class TestQuery(unittest.TestCase):
    def test_selector(self):
        selector = qy.Selector('PROJECT,SHOT,VERSION')
        data = list(selector(TABLE))
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], (('PROJECT', 'the hobbit'), ('SHOT', '1'), ('VERSION', 64)))

    def test_sorter(self):
        sorter = qy.Sorter('FINISH_DATE,INTERNAL_BID')
        data = list(sorter(TABLE))
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], (('PROJECT', 'lotr'), ('SHOT', '3'), ('VERSION', 16), ('STATUS', 'finished'), ('FINISH_DATE', date(2001, 5, 15)), ('INTERNAL_BID', 15.0), ('CREATED_DATE', datetime(2001, 4, 1, 6, 47))))
        self.assertEqual(data[-1], (('PROJECT', 'the hobbit'), ('SHOT', '1'), ('VERSION', 64), ('STATUS', 'scheduled'), ('FINISH_DATE', date(2010, 5, 15)), ('INTERNAL_BID', 45.0), ('CREATED_DATE', datetime(2010, 4, 1, 13, 35))))

    def test_filter(self):
        _filter = qy.Filter('FINISH_DATE=2006-07-22')
        data = list(_filter(TABLE))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], (('PROJECT', 'king kong'), ('SHOT', '42'), ('VERSION', 128), ('STATUS', 'not required'), ('FINISH_DATE', date(2006, 7, 22)), ('INTERNAL_BID', 30.0), ('CREATED_DATE', datetime(2006, 10, 15, 9, 14))))

    def test_bulk_none(self):
        bulk = qy.Bulk(None, None, None)
        data = list(bulk(TABLE))
        self.assertEqual(len(data), 4)

    def test_bulk_all(self):
        _filter = qy.Filter('FINISH_DATE=2006-07-22')
        sorter = qy.Sorter('FINISH_DATE,INTERNAL_BID')
        selector = qy.Selector('PROJECT,SHOT,VERSION')
        bulk = qy.Bulk(_filter, sorter, selector)
        data = list(bulk(TABLE))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], ('king kong', '42', 128))


if __name__ == '__main__':
    unittest.main()
