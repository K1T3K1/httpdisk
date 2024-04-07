from typing import Any, Iterable, AsyncGenerator, TypeVar, ParamSpec, Callable
import logging

logger = logging.getLogger(__name__)

_T = TypeVar("_T")
_P = ParamSpec("_P")

def Dependency() -> Any:
    return

class Injector:
    _contexts: list[AsyncGenerator[None, None]] = []

    @staticmethod
    def initialize(self, dependencies: Iterable[Any]):
        for d in dependencies:
            if hasattr(d.do, "context") and callable(d.do.context ):
                Injector._contexts.append(d.do.context())
            name_to_set = "_" + repr(d)
            setattr(Injector, name_to_set, d)

    @staticmethod
    async def _application_startup() -> None:
        for context in Injector._contexts:
            await context.asend()
        logger.info("Application started")

            
    @staticmethod
    async def _application_shutdown() -> None:
        for context in Injector._contexts:
            try:
                await context.asend()
            except StopAsyncIteration:
                pass
            except Exception as e:
                logger.error(f"Error shutting down context: {e}")
        logger.info("Application shutdown")

    @staticmethod
    def user_repository(fn: Callable[_P, _T]) -> Callable[_P, _T]:
        def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            kwargs.update({"user_repository": Injector._user_repository})
            return fn(*args, **kwargs)
        return wrapped 