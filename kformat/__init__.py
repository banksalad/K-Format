

class KProp:
    length: int

    def __init__(self, length: int) -> None:
        self.length = length


class A(KProp):
    pass


class AN(KProp):
    pass


def _kclass(cls):

    props = [(k, prop) for (k, prop) in cls.__annotations__.items()]

    def init(self, *args):
        for ((k, prop), v) in zip(props, args):
            # TODO: type checking
            setattr(self, k, (prop, v))

    setattr(cls, '__init__', init)

    return cls


def kclass(_cls=None):
    return _kclass(_cls)


@kclass
class Sth:
    name: A(50)
    age: AN(3)


print(Sth(1, 2).name)
