import sys

import fastapi

from . import router

@router.get(
    path="/helloworld",
    name="helloworld:helloworld",
)
async def demo(
    message: str = f"Hello world!",
) -> str:
    return message