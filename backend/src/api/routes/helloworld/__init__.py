import os

import fastapi

prefix = os.path.split(os.path.dirname(__file__))[-1]

router = fastapi.APIRouter(prefix=f"/{prefix}", tags=[prefix])