from unittest.mock import patch
from typing import List

import pytest

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
        with pytest.raises(AssertionError) as e:
            self.something(1, [1, 2])
        assert str(e.value) == 'int is not type of Other'

    def test_prop_is_not_list(self):
        with pytest.raises(AssertionError) as e:
            self.something(self.other(1, 2), 3)
        assert str(e.value) == 'int is not List'

    def test_all_items_are_not_kclass(self):
        with pytest.raises(AssertionError) as e:
            self.something(self.other(1, 2), [self.other(3, 4), 5])
        assert str(e.value) == 'All of list items should be type of K-Class'

    def test_prop_is_not_k_property(self):
        @kclass
        class One:
            an: AN(10)
            n: int

        with pytest.raises(AssertionError) as e:
            One(1, 2)
        assert str(e.value) == 'int is not subtype of KProperty'

    def test_prop_is_not_expected_type(self):
        with pytest.raises(AssertionError) as e:
            self.other(1, '2')
        assert str(e.value) == 'N cannot accept str type'

        with pytest.raises(AssertionError) as e:
            self.other([1], 2)
        assert str(e.value) == 'AN cannot accept list type'
