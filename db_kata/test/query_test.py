from datetime import date, datetime
import unittest
from db_kata.query import Bulk, Filter, Operator, Selector, Sorter
from stubs.constants import TABLE


class TestQuery(unittest.TestCase):
    def test_selector(self):
        selector = Selector('PROJECT,VERSION,SHOT')
        data = list(selector(TABLE))
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], (('PROJECT', 'the hobbit'), ('VERSION', 64), ('SHOT', '1')))
        
    def test_grouping(self):
        selector = Selector('PROJECT,VERSION:max,INTERNAL_BID:sum,SHOT:collect,STATUS:count', 'PROJECT')
        data = list(selector(TABLE))
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], (('PROJECT', 'the hobbit'), ('VERSION', 64), ('INTERNAL_BID', 67.8), ('SHOT', '[1,40]'), ('STATUS', '(2)')))

    def test_grouping_error(self):
        selector = Selector('PROJECT,INTERNAL_BID:reduce', 'PROJECT')
        with self.assertRaises(Operator.AggregateError):
            list(selector(TABLE))

    def test_sorter(self):
        sorter = Sorter('FINISH_DATE,INTERNAL_BID')
        data = list(sorter(TABLE))
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], (('PROJECT', 'lotr'), ('SHOT', '3'), ('VERSION', 16), ('STATUS', 'finished'), ('FINISH_DATE', date(2001, 5, 15)), ('INTERNAL_BID', 15.0), ('CREATED_DATE', datetime(2001, 4, 1, 6, 47))))
        self.assertEqual(data[-1], (('PROJECT', 'the hobbit'), ('SHOT', '1'), ('VERSION', 64), ('STATUS', 'scheduled'), ('FINISH_DATE', date(2010, 5, 15)), ('INTERNAL_BID', 45.0), ('CREATED_DATE', datetime(2010, 4, 1, 13, 35))))

    def test_filter_date(self):
        _filter = Filter('FINISH_DATE=2006-07-22')
        data = list(_filter(TABLE))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], (('PROJECT', 'king kong'), ('SHOT', '42'), ('VERSION', 128), ('STATUS', 'not required'), ('FINISH_DATE', date(2006, 7, 22)), ('INTERNAL_BID', 30.0), ('CREATED_DATE', datetime(2006, 10, 15, 9, 14))))

    def test_filter_or(self):
        _filter = Filter('PROJECT="the hobbit" OR PROJECT="lotr"')
        data = list(_filter(TABLE))
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], (('PROJECT', 'the hobbit'), ('SHOT', '1'), ('VERSION', 64), ('STATUS', 'scheduled'), ('FINISH_DATE', date(2010, 5, 15)), ('INTERNAL_BID', 45.0), ('CREATED_DATE', datetime(2010, 4, 1, 13, 35))))
        self.assertEqual(data[1], (('PROJECT', 'lotr'), ('SHOT', '3'), ('VERSION', 16), ('STATUS', 'finished'), ('FINISH_DATE', date(2001, 5, 15)), ('INTERNAL_BID', 15.0), ('CREATED_DATE', datetime(2001, 4, 1, 6, 47))))

    def test_filter_combo(self):
        _filter = Filter('PROJECT="the hobbit" AND (SHOT=1 OR SHOT=40)')
        data = list(_filter(TABLE))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], (('PROJECT', 'the hobbit'), ('SHOT', '1'), ('VERSION', 64), ('STATUS', 'scheduled'), ('FINISH_DATE', date(2010, 5, 15)), ('INTERNAL_BID', 45.0), ('CREATED_DATE', datetime(2010, 4, 1, 13, 35))))
        self.assertEqual(data[1], (('PROJECT', 'the hobbit'), ('SHOT', '40'), ('VERSION', 32), ('STATUS', 'finished'), ('FINISH_DATE', date(2010, 5, 15)), ('INTERNAL_BID', 22.8), ('CREATED_DATE', datetime(2010, 3, 22, 1, 10))))

    def test_bulk_none(self):
        bulk = Bulk(None, None, None)
        data = list(bulk(TABLE))
        self.assertEqual(len(data), 4)

    def test_bulk_all(self):
        _filter = Filter('FINISH_DATE=2006-07-22')
        sorter = Sorter('FINISH_DATE,INTERNAL_BID')
        selector = Selector('PROJECT,SHOT,VERSION')
        bulk = Bulk(_filter, sorter, selector)
        data = list(bulk(TABLE))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], ('king kong', '42', 128))


if __name__ == '__main__':
    unittest.main()
