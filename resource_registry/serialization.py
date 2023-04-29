import typing
import yaml
import pickle


class Serializer(typing.Protocol):
    def write(self, data: typing.Collection, path: str):
        ...

    def load(self, path: str) -> typing.Collection:
        ...


class Serializable(typing.Protocol):
    def serialize(self, path: str, serializer: Serializer):
        ...

    def parse(self, path: str, serializer: Serializer):
        ...


class PickleSerializer:
    def __init__(self, file_extension=".pickle") -> None:
        self._file_extension = file_extension

    def _validate_path(self, path: str):
        return (
            path + self._file_extension
            if not path.endswith(self._file_extension)
            else path
        )

    def write(self, data: typing.Collection, path: str):
        path = self._validate_path(path)
        with open(path, "wb") as file:
            pickle.dump(data, file)

    def load(self, path: str) -> typing.Collection:
        path = self._validate_path(path)
        with open(path, "rb") as file:
            return pickle.load(file)


class YamlSerializer:
    def __init__(self, file_extension=".yaml") -> None:
        self._file_extension = file_extension

    def _validate_path(self, path: str):
        return (
            path + self._file_extension
            if not path.endswith(self._file_extension)
            else path
        )

    def write(self, data: typing.Collection, path: str):
        path = self._validate_path(path)
        with open(path, "w") as file:
            yaml.dump(data, file)

    def load(self, path: str) -> typing.Collection:
        path = self._validate_path(path)
        with open(path, "r") as file:
            return yaml.load(file, yaml.FullLoader)
