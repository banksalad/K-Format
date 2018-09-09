import abc
from datetime import date, time
from typing import Optional, Set

__all__ = ['AN', 'N']


TYPES = Set[type]


class KProperty(metaclass=abc.ABCMeta):

    def __init__(
        self,
        length: int,
        expected_types: TYPES,
        filler: bytes
    ) -> None:
        self.length = length
        self.expected_types = expected_types
        self.filler = filler

    @abc.abstractmethod
    def to_bytes(self, v: Optional) -> bytes:
        pass


class N(KProperty):

    EXPECTED_TYPES = {int, float}
    FILLER = b'0'
    ENCODING = 'ascii'

    def __init__(
        self,
        length: int,
        *,
        filler: Optional[bytes]=None
    ) -> None:
        super().__init__(
            length,
            N.EXPECTED_TYPES,
            filler or N.FILLER
        )

    def to_bytes(self, v: Optional) -> bytes:
        s = str(int(v)) if v is not None else ''
        try:
            b = bytes(s, encoding=N.ENCODING).rjust(self.length, self.filler)
            assert len(b) <= self.length
            return b
        except AssertionError:
            raise ValueError(f'Too long value is given(max: {self.length})')


class AN(KProperty):

    EXPECTED_TYPES = N.EXPECTED_TYPES | {str, date, time, type(None)}
    FILLER = b' '
    ENCODING = 'euc-kr'
    DATE_FORMAT = '%Y%m%d'
    TIME_FORMAT = '%H%M%S%f'
    TIME_FORMAT_SLICE = 0, -2

    def __init__(
        self,
        length: int,
        *,
        filler: Optional[bytes]=None
    ) -> None:
        super().__init__(
            length,
            AN.EXPECTED_TYPES,
            filler or AN.FILLER
        )

    def to_bytes(self, v: Optional) -> bytes:
        if v is None or isinstance(v, str):
            s = v if v else ''
        elif isinstance(v, date):
            s = v.strftime(AN.DATE_FORMAT)
        elif isinstance(v, time):
            s = v.strftime(AN.TIME_FORMAT)[slice(*AN.TIME_FORMAT_SLICE)]
        else:
            s = str(int(v))

        try:
            b = bytes(s, encoding=AN.ENCODING).ljust(self.length, self.filler)
            assert len(b) <= self.length
            return b
        except AssertionError:
            raise ValueError(f'Too long value is given(max: {self.length})')

