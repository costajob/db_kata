from datetime import date, datetime
import unittest
from weta_db.values import DateVal, FloatVal, IntVal, TimeVal, TxtVal


class TestValues(unittest.TestCase):
    def test_valid_int(self):
        ival = IntVal(_min=42)
        self.assertEqual(ival(42), 42)

    def test_valid_int_by_str(self):
        ival = IntVal(_max=42)
        self.assertEqual(ival('42'), 42)

    def test_int_repr(self):
        ival = IntVal(_max=42)
        self.assertEqual(str(ival), 'IntVal(0-42)')

    def test_invalid_int(self):
        ival = IntVal(_max=10)
        with self.assertRaises(ValueError):
            ival(42)

    def test_valid_float(self):
        fval = FloatVal(_min=3.14)
        self.assertEqual(fval(3.14), 3.14)

    def test_valid_float_by_str(self):
        fval = FloatVal(_max=3.14)
        self.assertEqual(fval('3.14'), 3.14)

    def test_float_repr(self):
        fval = FloatVal(_min=1.1, _max=3.14)
        self.assertEqual(str(fval), 'FloatVal(1.1-3.14)')

    def test_invalid_float(self):
        fval = FloatVal(_min=9.99)
        with self.assertRaises(ValueError):
            fval(3.14)

    def test_valid_txt(self):
        tval = TxtVal(_max=64)
        self.assertEqual(tval('here come the sun'), 'here come the sun')

    def test_valid_txt_by_int(self):
        tval = TxtVal()
        self.assertEqual(tval(9999), '9999')

    def test_txt_repr(self):
        tval = TxtVal()
        self.assertEqual(str(tval), 'TxtVal(1-64)')

    def test_invalid_txt(self):
        tval = TxtVal(_max=5)
        with self.assertRaises(ValueError):
            tval('here come the sun')

    def test_valid_date(self):
        dval = DateVal()
        self.assertEqual(dval('2017-09-11'), date(2017, 9, 11))

    def test_date_repr(self):
        dval = DateVal()
        self.assertEqual(str(dval), 'DateVal(YYYY-MM-DD)')

    def test_invalid_date_value(self):
        dval = DateVal()
        with self.assertRaises(ValueError):
            dval('2017-09-31')

    def test_invalid_date_format(self):
        dval = DateVal()
        with self.assertRaises(ValueError):
            dval('11th of Spetember')

    def test_valid_time(self):
        tval = TimeVal()
        self.assertEqual(tval('2017-09-11 23:55'), datetime(2017, 9, 11, 23, 55))

    def test_time_repr(self):
        tval = TimeVal()
        self.assertEqual(str(tval), 'TimeVal(YYYY-MM-DD HH:MM)')

    def test_invalid_time(self):
        tval = TimeVal()
        with self.assertRaises(ValueError):
            tval('11th of Spetember 23 hours and 55 minutes')


if __name__ == '__main__':
    unittest.main()
