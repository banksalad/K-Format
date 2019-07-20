from typing import List
from unittest.mock import patch

import pytest

from kformat.exception import UnexpectedTypeError
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

    sth = Something(
        n=123,
        an='k-class',
        other=Other(-456, 'subclass'),
        others=[],
        filler=None,
    )
    assert sth is not None

    one = Other(n=123, an='1')
    assert (one.n[1], one.an[1]) == (123, '1')

    one = Other(123, an='1')
    assert (one.n[1], one.an[1]) == (123, '1')

    one = Other(an='1', n=123)
    assert (one.n[1], one.an[1]) == (123, '1')

    one = Other(123, an='1', n=456)
    assert (one.n[1], one.an[1]) == (456, '1')


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


class TestWrongTypeInit:
    @pytest.fixture(autouse=True)
    def setup(self):
        @kclass
        class Other:
            an: AN(10)
            n: N(5)

        @kclass
        class Something:
            other: Other
            others: List[Other]

        self.other = Other
        self.something = Something

    def test_prop_is_not_kclass(self):
        with pytest.raises(UnexpectedTypeError) as e:
            self.something(1, [1, 2])
        assert str(e.value) == '"Other" is expected, but "int" is given'

    def test_prop_is_not_list(self):
        with pytest.raises(UnexpectedTypeError) as e:
            self.something(self.other(1, 2), 3)
        assert str(e.value) == '"list" is expected, but "int" is given'

    def test_all_items_are_not_kclass(self):
        with pytest.raises(UnexpectedTypeError) as e:
            self.something(self.other(1, 2), [self.other(3, 4), 5])
        assert str(e.value) == '"List[Other]" is expected, but "int" is given'

    def test_prop_is_not_k_property(self):
        with pytest.raises(UnexpectedTypeError) as e:

            @kclass
            class One:
                an: AN(10)
                n: int

        assert str(e.value) == '"KProperty" is expected, but "int" is given'

    def test_prop_is_not_expected_type(self):
        with pytest.raises(UnexpectedTypeError) as e:
            self.other(1, '2')
        assert str(e.value) == '"float, int" is expected, but "str" is given'

        with pytest.raises(UnexpectedTypeError) as e:
            self.other([1], 2)
        assert str(e.value) == (
            '"NoneType, date, float, int, str, time" '
            'is expected, but "list" is given'
        )
