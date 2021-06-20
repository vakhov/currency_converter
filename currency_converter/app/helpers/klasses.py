from typing import Any, Dict


class Singleton(type):
    _instances: Dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Environ(metaclass=Singleton):
    def __init__(self) -> None:
        import os
        self.environ = os.environ

    def __getitem__(self, item: str) -> Any:
        return self.environ.get(item)
