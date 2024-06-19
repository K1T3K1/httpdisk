from typing import Any, Iterable, AsyncGenerator, TypeVar, ParamSpec, Callable
import logging
from pydantic import BaseModel
import datetime

logger = logging.getLogger(__name__)

_T = TypeVar("_T")
_P = ParamSpec("_P")


def Dependency() -> Any:
    return


class DependencyProvider(BaseModel):
    instance: Any
    name: str


class Injector:
    _contexts: list[AsyncGenerator[None, None]] = []

    @staticmethod
    def initialize(dependencies: Iterable[DependencyProvider]):
        for d in dependencies:
            if hasattr(d.instance, "context") and callable(d.instance.context):
                Injector._contexts.append(d.instance.context())
            name_to_set = "_" + d.name
            setattr(Injector, name_to_set, d.instance)

    @staticmethod
    async def _application_startup() -> None:
        for context in Injector._contexts:
            await context.asend(None)
        logger.info({"time": datetime.datetime.now(), "message": "Application started"})

    @staticmethod
    async def _application_shutdown() -> None:
        for context in Injector._contexts:
            try:
                await context.asend(None)
            except StopAsyncIteration:
                pass
            except Exception as e:
                logger.error({"time": datetime.datetime.now(), "message": f"Error shutting down application: {e}"})
        logger.info({"time": datetime.datetime.now(), "message": "Application shutdown"})

    @staticmethod
    def user_repository(fn: Callable[_P, _T]) -> Callable[_P, _T]:
        def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            kwargs.update({"user_repository": Injector._user_repository})
            return fn(*args, **kwargs)

        return wrapped

    @staticmethod
    def disk_manager(fn: Callable[_P, _T]) -> Callable[_P, _T]:
        def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            kwargs.update({"disk_manager": Injector._disk_manager})
            return fn(*args, **kwargs)

        return wrapped

    @staticmethod
    def disk_repository(fn: Callable[_P, _T]) -> Callable[_P, _T]:
        def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            kwargs.update({"disk_repository": Injector._disk_repository})
            return fn(*args, **kwargs)

        return wrapped

    @staticmethod
    def file_repository(fn: Callable[_P, _T]) -> Callable[_P, _T]:
        def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            kwargs.update({"file_repository": Injector._file_repository})
            return fn(*args, **kwargs)

        return wrapped
