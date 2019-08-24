from typing import Type

__all__ = ['KFormatError', 'UnexpectedTypeError', 'InvalidLengthError', 'UnsupportedUnicodeError']


def _name(type_: Type) -> str:
    return type_.__name__ if hasattr(type_, '__name__') else str(type_)


class KFormatError(Exception):
    pass


class UnexpectedTypeError(KFormatError):
    def __init__(self, expected: Type, value):
        super().__init__()
        self.expected = expected
        self.value = value

    def __str__(self) -> str:
        return (
            f'"{_name(self.expected)}" is expected, '
            f'but "{_name(self.value)}" is given'
        )


class InvalidLengthError(KFormatError):
    def __init__(self, length: int):
        super().__init__()
        self.length = length

    def __str__(self) -> str:
        return f'Invalid length of value is given(expected: {self.length})'


class UnsupportedUnicodeError(KFormatError, UnicodeError):
    def __init__(self, msg: str):
        super().__init__()
        self.msg = msg

    def __str__(self) -> str:
        return self.msg
