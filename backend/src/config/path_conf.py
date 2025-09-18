import os
from pathlib import Path

# 获取项目根目录
# 或使用绝对路径，指到backend目录为止，例如windows：BasePath = D:\git_project\fastapi_mysql\backend
BasePath = Path(__file__).resolve().parent.parent.parent


# 日志文件路径
LogPath = os.path.join(BasePath, "logs")

if not os.path.exists(LogPath):
    os.mkdir(LogPath)

# 数据文件路径
FilePath = os.path.join(BasePath, "storage")

if not os.path.exists(FilePath):
    os.mkdir(FilePath)
