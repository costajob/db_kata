from datetime import date, datetime
import unittest
import datastore as ds
from stubs import ROWS


class TestDatastore(unittest.TestCase):
    def setUp(self):
        self.table = ds.Table()

    def test_column_repr(self):
        self.assertEqual(str(ds.COLUMNS[0]), 'Column(PROJECT, TxtVal(1-64), key=True)')

    def test_table_data(self):
        self.assertTrue(self.table.columns, ds.COLUMNS)
        self.assertFalse(self.table.rows)

    def test_append_row(self):
        _id = '7889a3193abeffbc23ee75d431226a8a'
        self.table.append(ROWS[0])
        self.assertEqual(len(self.table), 1)
        self.assertIn(_id, self.table)
        self.assertEqual(self.table[_id], ['the hobbit', '1', 64, 'scheduled', date(2010, 5, 15), 45.00, datetime(2010, 4, 1, 13, 35)])

    def test_merge_rows(self):
        _id = '70d72c0c1a323dd355d22961ea77857e'
        self.table.merge(ROWS)
        self.assertEqual(len(self.table), 4)
        self.assertIn(_id, self.table)
        self.assertEqual(self.table[_id], ['king kong', '42', 128, 'not required', date(2006, 7, 22), 30.0, datetime(2006, 10, 15, 9, 14)])

    def test_append_row_error(self):
        with self.assertRaises(ds.Table.RowError):
            self.table.append([1,2,3])

    def test_clear_rows(self):
        self.table.merge(ROWS)
        self.table.clear()
        self.assertFalse(self.table.rows)


if __name__ == '__main__':
    unittest.main()
