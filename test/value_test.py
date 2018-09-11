from datetime import date, datetime
import unittest
import value

class TestDatastore(unittest.TestCase):
    def test_valid_int(self):
        ival = value.IntVal(42, _max=42)
        self.assertEqual(ival.val, 42)

    def test_valid_int_by_txt(self):
        ival = value.IntVal('42')
        self.assertEqual(ival.val, 42)

    def test_invalid_int(self):
        with self.assertRaises(value.Val.RangeError):
            value.IntVal(42, 0, 10)

    def test_valid_float(self):
        fval = value.FloatVal(3.14, _min=3.14)
        self.assertEqual(fval.val, 3.14)

    def test_valid_float_by_str(self):
        fval = value.FloatVal('3.14')
        self.assertEqual(fval.val, 3.14)

    def test_invalid_float(self):
        with self.assertRaises(value.Val.RangeError):
            value.FloatVal(3.14, _min=9.99)

    def test_valid_txt(self):
        tval = value.TxtVal('here come the sun', _max=64)
        self.assertEqual(tval.val, 'here come the sun')

    def test_valid_txt_by_int(self):
        tval = value.TxtVal(9999)
        self.assertEqual(tval.val, '9999')

    def test_invalid_txt(self):
        with self.assertRaises(value.Val.RangeError):
            value.TxtVal('here come the sun', _min=100)

    def test_valid_date(self):
        dval = value.DateVal('2017-09-11')
        self.assertEqual(dval.val, date(2017, 9, 11))

    def test_invalid_date_value(self):
        with self.assertRaises(value.Val.RangeError):
            value.DateVal('2017-09-31')

    def test_invalid_date_format(self):
        with self.assertRaises(value.Val.RangeError):
            value.DateVal('11th of Spetember')

    def test_valid_time(self):
        tval = value.TimeVal('2017-09-11 23:55')
        self.assertEqual(tval.val, datetime(2017, 9, 11, 23, 55))

    def test_invalid_time(self):
        with self.assertRaises(value.Val.RangeError):
            value.DateVal('11th of Spetember 23 hours and 55 minutes')


if __name__ == '__main__':
    unittest.main()
