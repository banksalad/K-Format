from datetime import date, time

import pytest

from kformat.exception import InvalidLengthError, UnsupportedUnicodeError
from kformat.kproperty import AN, N, Errors


@pytest.mark.parametrize(
    'length, value, expected',
    [
        (5, None, b'00000'),
        (5, 0, b'00000'),
        (5, 3, b'00003'),
        (5, 12345, b'12345'),
        (5, -1, b'-0001'),
        (3, -12, b'-12'),
    ],
)
def test_N_to_bytes(length, value, expected):
    assert N(length).to_bytes(value) == expected


@pytest.mark.parametrize(
    'length, filler, value, expected',
    [(10, b'?', 3, b'?????????3'), (5, b'-', 3, b'----3')],
)
def test_N_to_bytes_with_filler(length, filler, value, expected):
    assert N(length, filler=filler).to_bytes(value) == expected


@pytest.mark.parametrize('length, value', [(3, 1234), (2, -10)])
def test_N_to_bytes_with_invalid_length(length, value):
    with pytest.raises(InvalidLengthError) as e:
        assert N(length).to_bytes(value)
    assert 'Invalid length of value is given' in str(e.value)


@pytest.mark.parametrize(
    'length, value, expected',
    [
        (10, 'sunghyunzz', b'sunghyunzz'),
        (10, '황성현', b'\xc8\xb2\xbc\xba\xc7\xf6    '),
        (10, date(2018, 9, 9), b'20180909  '),
        (10, time(15, 47, 0, 0), b'1547000000'),
        (12, time(15, 35, 12, 345678), b'1535123456  '),
        (5, 1, b'1    '),
    ],
)
def test_AN_to_bytes(length, value, expected):
    assert AN(length).to_bytes(value) == expected


def test_AN_to_bytes_with_invalid_length():
    with pytest.raises(InvalidLengthError) as e:
        assert AN(5).to_bytes(date(2018, 9, 9))
    assert 'Invalid length of value is given' in str(e.value)


def test_AN_to_bytes_with_unicode_error_strict():
    with pytest.raises(UnsupportedUnicodeError) as e:
        AN(30, errors=Errors.STRICT).to_bytes("동아・한신아파트")
    assert "codec can't encode character" in str(e.value)


def test_AN_to_bytes_with_unicode_error_ignore():
    assert (
        AN(16, errors=Errors.IGNORE).to_bytes("동아・한신아파트")
        == b"\xb5\xbf\xbe\xc6\xc7\xd1\xbd\xc5\xbe\xc6\xc6\xc4\xc6\xae  "
    )


def test_AN_to_bytes_with_unicode_error_replace():
    assert (
        AN(16, errors=Errors.REPLACE).to_bytes("동아・한신아파트")
        == b"\xb5\xbf\xbe\xc6?\xc7\xd1\xbd\xc5\xbe\xc6\xc6\xc4\xc6\xae "
    )
