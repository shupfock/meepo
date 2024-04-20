import os
from typing import Any, List, Set

from dependency_injector import containers
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cantor.config.base import Container
from cantor.config.init import ContainerInitializer, mongo_init, redis_init


class App(FastAPI):
    base_container: Container


def find_api_handler_modules(path: str) -> Set[str]:
    from pkgutil import iter_modules

    from setuptools import find_packages

    modules = set()
    for pkg in find_packages(path):
        modules.add(pkg)
        package_path = f"{path}/{pkg.replace('.', '/')}"
        for info in iter_modules(package_path):
            if info.ispkg:
                modules.add(f"{pkg}.{info.name}")

    return modules


def find_api_handlers() -> List[str]:
    api_module_path = os.path.dirname(os.path.abspath(__file__))
    module_in_package = find_api_handler_modules(api_module_path)
    router_modules = []
    for module in module_in_package:
        if module.endswith("handler"):
            router_modules.append(f"cantor.api.{module}")

    return router_modules


def container_wire_to_router(router_module: Any, containers_to_wire: List[containers.DeclarativeContainer]) -> None:
    for container_type in containers_to_wire:
        container_name = str(container_type.__name__)
        target_container = ContainerInitializer.get_container_instance_by_name(container_name)
        if target_container:
            target_container.wire(modules=[router_module])


def auto_include_routers(app: App) -> None:
    import importlib
    import inspect

    api_router_modules = find_api_handlers()
    for router in api_router_modules:
        router_module = importlib.import_module(router)
        all_member = inspect.getmembers(router_module)
        containers_to_wire = []
        for _, value in all_member:
            if isinstance(value, APIRouter):
                app.include_router(value)
            if containers.is_container(value):
                containers_to_wire.append(value)
        container_wire_to_router(router_module, containers_to_wire)


def add_middlewares(app: App) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def container_init(app: App) -> None:
    app.base_container = Container()


async def init_connect(app: App) -> None:
    await mongo_init(app.base_container)
    await redis_init(app.base_container)


def make_up_app(app: App) -> App:
    auto_include_routers(app)
    add_middlewares(app)
    container_init(app)

    return app


async def on_app_setup(app: App) -> None:
    await init_connect(app)
