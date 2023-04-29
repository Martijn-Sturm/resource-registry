import typing
import sys

Kwargs = typing.Dict[str, str]


def python_is_lower_than_3_point_7():
    major = sys.version_info.major
    minor = sys.version_info.minor

    return False if major >= 3 and minor >= 7 else False


class ArgumentMismatch(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__("mismatch in expected versus received args", *args)


class ResourceAlreadyRegistered(ValueError):
    def __init__(self, kwargs: Kwargs, registry_key: tuple, *args: object) -> None:
        super().__init__(
            "Resource has already been registered by exact combination of args",
            "Use force overwrite if you want to update",
            "args:",
            kwargs,
            "expected registry key",
            registry_key,
            *args,
        )


class ResourceNotRegistered(ValueError):
    def __init__(self, kwargs: Kwargs, registry_key: tuple, *args: object) -> None:
        super().__init__(
            "Resource has not been registered yet",
            "args:",
            kwargs,
            "expected registry key",
            registry_key,
            *args,
        )


class NameRegistry:
    def __init__(
        self,
        formatting_function: typing.Callable[[Kwargs], str],
        args_description: Kwargs,
    ) -> None:
        self._formatting_func = formatting_function
        self._args = [arg for arg in args_description]
        self._args_description = args_description
        self._registry = {}
        self._validate_instantiation()

    def register(self, args: Kwargs, force_overwrite: bool = False):
        self._check_kwargs_is_consistent(args)
        registry_key = self._args_to_tuple(args)
        if not force_overwrite:
            try:
                self.retrieve(args)
            except ResourceNotRegistered:
                pass
            else:
                raise ResourceAlreadyRegistered(args, registry_key)

        self._registry.update({registry_key: self._formatting_func(args)})

    def retrieve(self, args: Kwargs):
        self._check_kwargs_is_consistent(args)
        registry_key = self._args_to_tuple(args)
        try:
            return self._registry[registry_key]
        except KeyError:
            raise ResourceNotRegistered(args, registry_key)

    @staticmethod
    def _args_to_tuple(args: Kwargs) -> tuple:
        if python_is_lower_than_3_point_7():
            raise RuntimeError(
                "We assume that dictionary is ordered",
                "this is only the case from Python3.7",
                "Upgrade your Python version",
            )
        return tuple([value for value in args.values()])

    def _check_kwargs_is_consistent(self, args: Kwargs):
        expected_args = set(self._args)
        received_args = set([arg for arg in args])

        if lacking_args := expected_args - received_args:
            raise ArgumentMismatch("Arguments missing in call:", lacking_args)
        if undefined_args := received_args - expected_args:
            raise ArgumentMismatch(
                f"Arguments received but not defined in {self.__class__} definition:",
                undefined_args,
            )

    def _validate_instantiation(self):
        try:
            self._formatting_func(self._args_description)
        except KeyError as err:
            raise ArgumentMismatch(
                "mismatch between formatter func expected args, and provided kwargs description in definition",
                "argument with key missing:",
                *err.args,
            )
