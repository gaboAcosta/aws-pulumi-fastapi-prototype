import importlib
import os

from fastapi import APIRouter

base_router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)

public_routes_dir = 'routes/public'
private_routes_dir = 'routes/private'


def load_routes(routes_dir: str) -> APIRouter:
    router = APIRouter(
        prefix="/v1",
    )
    root_dir = os.path.dirname(__file__)
    path = f'{root_dir}/{routes_dir}'
    files = os.listdir(path)
    python_files = [file for file in files if file.endswith('.py')]
    for file in sorted(python_files):
        module_name = file[:-3]  # Remove the .py extension
        full_module_name = f'api/{routes_dir}/{module_name}'.replace('/', '.')
        route_module = importlib.import_module(full_module_name)
        if not route_module or not route_module.router:
            raise Exception(f"Error loading app routes, Module {full_module_name} does not have a router")
        router.include_router(route_module.router)

    return router


base_router.include_router(load_routes(public_routes_dir))
base_router.include_router(load_routes(private_routes_dir))
