from typing import Type

__all__ = ['KFormatError', 'TooLongValueError']


class KFormatError(Exception):
    pass


class TooLongValueError(KFormatError):
    def __init__(self, length: int):
        super().__init__()
        self.length = length

    def __str__(self) -> str:
        return f'Too long value is given(max: {self.length})'
