from typing import Type

__all__ = ['KFormatError', 'WrongTypeError', 'TooLongValueError']


def _name(type_: Type) -> str:
    return type_.__name__ if hasattr(type_, '__name__') else str(type_)


class KFormatError(Exception):
    pass


class WrongTypeError(KFormatError):
    def __init__(self, expect: Type, value):
        super().__init__()
        self.expect = expect
        self.value = value

    def __str__(self) -> str:
        return f'Should be "{_name(self.expect)}" instead of "{_name(self.value)}"'


class TooLongValueError(KFormatError):
    def __init__(self, length: int):
        super().__init__()
        self.length = length

    def __str__(self) -> str:
        return f'Too long value is given(max: {self.length})'
