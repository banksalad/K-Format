from . import kproperty


__all__ = ['kclass']


KCLASS_ANNOTATION = '__kclass__'


def _kclass(cls):
    setattr(cls, KCLASS_ANNOTATION, True)

    props = [(k, prop) for (k, prop) in cls.__annotations__.items()]

    @property
    def to_bytes(self):
        return b''.join(self._bytes)

    def init(self, *args):
        prop_bytes = []

        for ((k, prop), v) in zip(props, args):
            if hasattr(prop, KCLASS_ANNOTATION) and prop.__kclass__:
                assert isinstance(v, prop), \
                    f'{type(v).__name__} is not type of {prop.__name__}'
                prop_bytes.append(v.bytes)
            elif hasattr(prop, '__origin__') and prop.__origin__ == list:
                assert isinstance(v, list), f'{type(v).__name__} is not List'
                assert all(
                    getattr(item, KCLASS_ANNOTATION, False) for item in v
                ), f'All of list items should be type of K-Class'
                prop_bytes.extend(c.bytes for c in v)
            else:
                assert isinstance(prop, kproperty.KProperty), \
                    f'{prop.__name__} is not subtype of KProperty'
                assert type(v) in prop.expected_types, \
                    f'{prop.__class__.__name__} cannot ' \
                    f'accept {type(v).__name__} type'
                prop_bytes.append(prop.to_bytes(v))

            setattr(self, k, (prop, v))

        setattr(self, '_bytes', prop_bytes)

    setattr(cls, 'bytes', to_bytes)

    setattr(cls, '__init__', init)

    return cls


def kclass(_cls=None):
    def wrap(cls):
        return _kclass(cls)

    if _cls is None:
        return wrap

    return wrap(_cls)
