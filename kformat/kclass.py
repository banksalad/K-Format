from .exception import UnexpectedTypeError
from .kproperty import KProperty

__all__ = ['kclass']


KCLASS_ANNOTATION = '__kclass__'


def _is_prop_kclass(prop) -> bool:
    return getattr(prop, KCLASS_ANNOTATION, False)


def _is_prop_list(prop) -> bool:
    return hasattr(prop, '__origin__') and prop.__origin__ == list


def _is_valid_child_prop(prop) -> bool:
    return (
        _is_prop_kclass(prop)
        or _is_prop_list(prop)
        or isinstance(prop, KProperty)
    )


def _combine_params(props, args, kwargs):
    for i, (field_name, field_type) in enumerate(props):
        try:
            value = kwargs[field_name]
        except KeyError:
            value = args[i]
        yield field_name, field_type, value


def _kclass(cls):
    setattr(cls, KCLASS_ANNOTATION, True)

    props = list(cls.__annotations__.items())

    for _, prop in props:
        if not _is_valid_child_prop(prop):
            raise UnexpectedTypeError(KProperty, prop.__name__)

    @property
    def to_bytes(self):
        return b''.join(self._bytes)

    def init(self, *args, **kwargs):
        prop_bytes = []

        for k, prop, v in _combine_params(props, args, kwargs):
            if _is_prop_kclass(prop):
                if not isinstance(v, prop):
                    raise UnexpectedTypeError(prop, type(v))
                prop_bytes.append(v.bytes)
            elif _is_prop_list(prop):
                if not isinstance(v, list):
                    raise UnexpectedTypeError(list, type(v))
                for item in v:
                    if not _is_prop_kclass(item):
                        raise UnexpectedTypeError(
                            f'List[{prop.__args__[0].__name__}]', type(item)
                        )
                prop_bytes.extend(c.bytes for c in v)
            else:
                if type(v) not in prop.expected_types:
                    expected_types = ', '.join(
                        sorted(t.__name__ for t in prop.expected_types)
                    )
                    raise UnexpectedTypeError(expected_types, type(v))
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
