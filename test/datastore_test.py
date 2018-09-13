from datetime import date, datetime
import unittest
import datastore as ds
from stubs.constants import COLUMNS, ROWS, SHUFFLE, TABLE


class TestDatastore(unittest.TestCase):
    def test_column_repr(self):
        self.assertEqual(str(COLUMNS[0]), 'Column(PROJECT, TxtVal(1-64), key=True)')

    def test_columns_sorting(self):
        table = ds.Table.factory(SHUFFLE, COLUMNS)
        headers = [c.name for c in table.columns]
        self.assertEqual(headers, SHUFFLE[0])

    def test_table_factory(self):
        _id = '70d72c0c1a323dd355d22961ea77857e'
        table = ds.Table.factory(ROWS, COLUMNS)
        self.assertEqual(len(table), 4)
        self.assertIn(_id, table)
        self.assertEqual(table[_id], ['king kong', '42', 128, 'not required', date(2006, 7, 22), 30.0, datetime(2006, 10, 15, 9, 14)])

    def test_table_repr(self):
        self.assertEqual(str(TABLE), 'Table(columns=(PROJECT, SHOT, VERSION, STATUS, FINISH_DATE, INTERNAL_BID, CREATED_DATE), rows=4)')

    def test_table_data(self):
        table = ds.Table(COLUMNS)
        self.assertTrue(table.columns, COLUMNS)
        self.assertFalse(table)

    def test_append_row(self):
        _id = '7889a3193abeffbc23ee75d431226a8a'
        TABLE.append(ROWS[1])
        self.assertEqual(len(TABLE), 1)
        self.assertIn(_id, TABLE)
        self.assertEqual(TABLE[_id], ['the hobbit', '1', 64, 'scheduled', date(2010, 5, 15), 45.00, datetime(2010, 4, 1, 13, 35)])

    def test_merge_rows(self):
        _id = '70d72c0c1a323dd355d22961ea77857e'
        TABLE.merge(ROWS[1:])
        self.assertEqual(len(TABLE), 4)
        self.assertIn(_id, TABLE)
        self.assertEqual(TABLE[_id], ['king kong', '42', 128, 'not required', date(2006, 7, 22), 30.0, datetime(2006, 10, 15, 9, 14)])

    def test_append_row_error(self):
        with self.assertRaises(ds.Table.DataError):
            TABLE.append([1,2,3])

    def test_tables_addition(self):
        table = ds.Table(COLUMNS)
        table.merge(ROWS[1:2])
        other = ds.Table(COLUMNS)
        other.merge(ROWS[1:4])
        table + other
        self.assertEqual(len(table), 3)


if __name__ == '__main__':
    unittest.main()
