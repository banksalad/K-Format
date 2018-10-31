import unittest
from datetime import date, time

from kformat.kproperty import *


class TestKProperty(unittest.TestCase):

    def test_N_to_bytes(self):
        self.assertEqual(
            N(5).to_bytes(None),
            b'00000'
        )
        self.assertEqual(
            N(5).to_bytes(0),
            b'00000'
        )
        self.assertEqual(
            N(5).to_bytes(3),
            b'00003'
        )
        self.assertEqual(
            N(5).to_bytes(12345),
            b'12345'
        )
        self.assertEqual(
            N(5).to_bytes(-1),
            b'-0001'
        )
        self.assertEqual(
            N(3).to_bytes(-12),
            b'-12'
        )
        self.assertEqual(
            N(10, filler=b'?').to_bytes(3),
            b'?????????3'
        )
        self.assertEqual(
            N(5, filler=b'-').to_bytes(3),
            b'----3'
        )

        with self.assertRaises(ValueError):
            N(3).to_bytes(1234)

        with self.assertRaises(ValueError):
            N(2).to_bytes(-10)

    def test_AN_to_bytes(self):
        self.assertEqual(
            AN(10).to_bytes('sunghyunzz'),
            b'sunghyunzz'
        )
        self.assertEqual(
            AN(10).to_bytes('황성현'),
            b'\xc8\xb2\xbc\xba\xc7\xf6    '
        )
        self.assertEqual(
            AN(10).to_bytes(date(2018, 9, 9)),
            b'20180909  '
        )
        self.assertEqual(
            AN(10).to_bytes(time(15, 47, 0, 0)),
            b'1547000000'
        )
        self.assertEqual(
            AN(12).to_bytes(time(15, 35, 12, 345678)),
            b'1535123456  '
        )
        self.assertEqual(
            AN(5).to_bytes(1),
            b'1    '
        )
        with self.assertRaises(ValueError):
            AN(5).to_bytes(date(2018, 9, 9))
