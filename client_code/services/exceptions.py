from anvil.server import AnvilWrappedError, _register_exception_type


class NamedError(AnvilWrappedError):
    """A base class for custom error classes

    In order to register a custom error class, a name is required. This base class
    ensures that a 'name' class attribute exists with a default value for use by
    portable_exception.

    It can be overridden in any subclass that requires a customised name.
    """

    name = None


def portable_exception(cls):
    """A decorator to register a class as an exception"""
    try:
        name = cls.name or f"{__name__}.{cls.__name__}"
    except AttributeError:
        raise ValueError("Class to register must have a 'name' attribute")
    _register_exception_type(name, cls)
    return cls


@portable_exception
class ChildExists(NamedError):
    pass


@portable_exception
class KeyExists(NamedError):
    pass