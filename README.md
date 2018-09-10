# K-Format

[![Build Status](https://travis-ci.org/Rainist/K-Format.svg?branch=master)](https://travis-ci.org/Rainist/K-Format) [![PyPI](https://img.shields.io/pypi/v/K-Format.svg)](https://badge.fury.io/py/K-Format) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/K-Format.svg)](https://badge.fury.io/py/K-Format) [![Rainist](https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%99%A5%20by-Rainist-blue.svg)](https://rainist.com/recruit)

K-Format is a Python library designed for dealing with KCB K-Format in a convenient way. 

## Getting Started

```python
from kformat import *


@kclass
class Item:
    sth: N(2)


@kclass
class Base:
    birthday: AN(8)
    name: AN(10)
    grade: N(3)
    items: List[Item]


base = Base(date(1980, 8, 12), '홍길동', 1, [Item(3), Item(4)])
assert base.bytes == b'19800812\xc8\xab\xb1\xe6\xb5\xbf    0010304'
```

## Installation

```bash
pip install K-Format
```
