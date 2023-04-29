from resource_registry import registry
import pytest
import typing


def create_test_registry():
    return registry.NameRegistry(formatting_func, {"a": "arg a", "b": "arg b"})


def formatting_func(args: typing.Dict[str, str]):
    return f"{args['a']}-{args['b']}-c"


def test_register_fails_if_already_exists():
    test_registry = create_test_registry()

    test_registry.register({"a": "a", "b": "b"}, force_overwrite=False)

    # Again with the same properties:
    with pytest.raises(registry.ResourceAlreadyRegistered):
        test_registry.register({"a": "a", "b": "b"}, force_overwrite=False)


def test_register_passes_if_overwrites():
    test_registry = create_test_registry()

    test_registry.register({"a": "a", "b": "b"}, force_overwrite=False)

    # Again with the same properties:
    test_registry.register({"a": "a", "b": "b"}, force_overwrite=True)
