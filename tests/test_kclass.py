from unittest.mock import patch
from typing import List

from kformat.kclass import kclass
from kformat.kproperty import AN, N


def test_kclass_init():
    @kclass
    class Other:
        n: N(5)
        an: AN(10)

    @kclass
    class Something:
        n: N(10)
        an: AN(20)
        other: Other
        others: List[Other]
        filler: AN(100)

    sth = Something(123, 'k-class', Other(-456, 'subclass'), [], None)
    assert sth is not None


@patch('kformat.kproperty.AN.to_bytes', lambda s, v: b'AN')
@patch('kformat.kproperty.N.to_bytes', lambda s, v: b'N')
def test_kclass_to_bytes():
    @kclass
    class Other:
        an: AN(10)
        n: N(5)

    @kclass
    class Something:
        a: N(10)
        b: AN(20)
        other: Other
        others: List[Other]
        c: N(5)
        d: AN(10)

    sth = Something(1, 2, Other(3, 4), [Other(1, 1), Other(1, 1)], 5, 6)
    assert sth.bytes == b'NANANNANNANNNAN'


def test_list_of_kclass_creation():
    @kclass
    class Something:
        n: N(1)

    some_list = [Something(1), Something(2), Something(3)]
    assert b''.join(s.bytes for s in some_list) == b'123'
