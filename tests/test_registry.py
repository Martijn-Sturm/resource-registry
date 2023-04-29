from resource_registry import registry
import pytest
import typing


def formatting_func(args: typing.Dict[str, str]):
    return f"{args['a']}-{args['b']}-c"


def test_name_registry_can_be_instantiated():
    registry.NameRegistry(formatting_func, {"a": "arg a", "b": "arg b"})


def test_name_registry_instantiation_fails_if_arg_of_function_missing():
    with pytest.raises(registry.ArgumentMismatch, match="argument with key missing:"):
        registry.NameRegistry(formatting_func, {"a": "arg a"})
