from . import kproperty


__all__ = ['kclass']


def _kclass(cls):

    props = [(k, prop) for (k, prop) in cls.__annotations__.items()]

    def init(self, *args):
        prop_bytes = []

        for ((k, prop), v) in zip(props, args):
            assert isinstance(prop, kproperty.KProperty)
            assert type(v) in prop.expected_types

            setattr(self, k, (prop, v))
            prop_bytes.append(prop.to_bytes(v))

        setattr(cls, 'bytes', b''.join(prop_bytes))

    setattr(cls, '__init__', init)

    return cls


def kclass(_cls=None):
    def wrap(cls):
        return _kclass(cls)

    if _cls is None:
        return wrap

    return wrap(_cls)
