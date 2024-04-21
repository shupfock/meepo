from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter as _APIRouter
from fastapi import Depends


def dependency(provider):
    """Turns DI provider into FastAPI dependency"""
    return Depends(Provide[provider])


class APIRouter(_APIRouter):
    """Auto inject"""

    def api_route(self, path, *_, **kwargs):
        def decorator(func):
            func = inject(func)
            self.add_api_route(path, func, **kwargs)

            return func

        return decorator
