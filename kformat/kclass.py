from . import kproperty
from .exception import WrongTypeError

__all__ = ['kclass']


KCLASS_ANNOTATION = '__kclass__'


def _is_prop_kclass(prop) -> bool:
    return getattr(prop, KCLASS_ANNOTATION, False)


def _is_prop_list(prop) -> bool:
    return hasattr(prop, '__origin__') and prop.__origin__ == list


def _kclass(cls):
    setattr(cls, KCLASS_ANNOTATION, True)

    props = list(cls.__annotations__.items())

    for _, prop in props:
        if (
            not _is_prop_kclass(prop)
            and not _is_prop_list(prop)
            and not isinstance(prop, kproperty.KProperty)
        ):
            raise WrongTypeError(kproperty.KProperty, prop.__name__)

    @property
    def to_bytes(self):
        return b''.join(self._bytes)

    def init(self, *args):
        prop_bytes = []

        for ((k, prop), v) in zip(props, args):
            if _is_prop_kclass(prop):
                if not isinstance(v, prop):
                    raise WrongTypeError(prop, type(v))
                prop_bytes.append(v.bytes)
            elif _is_prop_list(prop):
                if not isinstance(v, list):
                    raise WrongTypeError(list, type(v))
                for item in v:
                    if not getattr(item, KCLASS_ANNOTATION, False):
                        raise WrongTypeError(
                            f'List[{prop.__args__[0].__name__}]', type(item)
                        )
                prop_bytes.extend(c.bytes for c in v)
            else:
                if type(v) not in prop.expected_types:
                    expects = ', '.join(
                        sorted(t.__name__ for t in prop.expected_types)
                    )
                    raise WrongTypeError(expects, type(v))
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
