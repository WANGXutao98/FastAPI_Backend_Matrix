import importlib.util
import os

from src.models.db.app_group import *
from src.models.db.dataset import *
from src.repository.table import Base

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# def import_module_from_file(file_path: str) -> None:
#     module_name = os.path.splitext(os.path.basename(file_path))[0]
#     spec = importlib.util.spec_from_file_location(module_name, file_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)


# for root, _, files in os.walk(src_db_path):
#     for file in files:
#         if file.endswith(".py"):
#             file_path = os.path.join(root, file)
#             import_module_from_file(file_path)
