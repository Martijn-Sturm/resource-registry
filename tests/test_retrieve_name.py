from resource_registry import registry
import pytest
import typing


def formatting_func(kwargs: typing.Dict[str, str]):
    return f"{kwargs['a']}-{kwargs['b']}-c"


def test_name_registry_cannot_retrieve_if_not_registered():
    test_registry = registry.NameRegistry(
        formatting_func, {"a": "a description", "b": "b description"}
    )
    test_registry.register({"a": "won't be retrieved", "b": "won't be retrieved"})
    with pytest.raises(registry.ResourceNotRegistered):
        test_registry.retrieve({"a": "a", "b": "b"})


def test_name_registry_can_retrieve_after_registered():
    test_registry = registry.NameRegistry(
        formatting_func, {"a": "a description", "b": "b description"}
    )
    test_registry.register({"a": "a", "b": "b"})

    assert test_registry.retrieve({"a": "a", "b": "b"}) == "a-b-c"


def test_name_registry_retrieve_fails_if_wrong_arg():
    test_registry = registry.NameRegistry(
        formatting_func, {"a": "a description", "b": "b description"}
    )

    with pytest.raises(
        registry.ArgumentMismatch, match=r"Arguments received but not defined"
    ):
        test_registry.retrieve(
            {
                "a": "a",
                "b": "b",
                # c not defined in formatting func
                "c": "c",
            }
        )


def test_name_registry_retrieve_fails_if_missing_arg():
    test_registry = registry.NameRegistry(
        formatting_func, {"a": "a description", "b": "b description"}
    )

    with pytest.raises(registry.ArgumentMismatch, match=r"Arguments missing in call"):
        test_registry.retrieve(
            {"a": "a"}
            # b misses
        )
