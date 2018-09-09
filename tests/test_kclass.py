import unittest

from kformat.kclass import kclass
from kformat.kproperty import AN, N


class TestKClass(unittest.TestCase):

    def test_kclass_init(self):

        @kclass
        class Something:
            n: N(10)
            an: AN(20)
            filler: AN(100)

        sth = Something(123, "k-class", None)
        self.assertIsNotNone(sth)

    def test_kclass_to_bytes(self):
        _n, N.to_bytes = N.to_bytes, lambda s, v: b'N'
        _an, AN.to_bytes = AN.to_bytes, lambda s, v: b'AN'

        @kclass
        class Something:
            a: N(10)
            b: AN(20)
            c: N(5)
            d: AN(10)

        sth = Something(1, 2, 3, 4)
        self.assertEqual(sth.bytes, b'NANNAN')

        # Reset to_bytes funcs to default
        N.to_bytes = _n
        AN.to_bytes = _an
