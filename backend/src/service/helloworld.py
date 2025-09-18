import os,sys
# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取上级目录
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.dirname(parent_dir)
# 将上级目录添加到 sys.path
sys.path.append(src_dir)
import loguru
import fastapi

if __name__ == "__main__":
    loguru.logger.info("Hello World")
    
    