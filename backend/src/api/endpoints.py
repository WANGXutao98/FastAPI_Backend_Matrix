import importlib

import fastapi
from src.api.routes import init_modules, modules


def register_routers_modules(router):
    init_modules()
    for module in modules:
        imported_module = importlib.import_module(module)
        if getattr(imported_module, "router", None) is None:
            continue
        router.include_router(getattr(imported_module, "router"))


router = fastapi.APIRouter()

register_routers_modules(router)
