<h1 align=center><strong>FastAPI Backend Application Template - Base Python 3.9.12</strong></h1>

## 项目介绍

本套框架forked自[github]  https://github.com/Aeternalis-Ingenium/FastAPI-Backend-Template, 这是一套基于FastApi开发框架，同时集成一系列开箱即用的组件，包括Redis,Kafka,MySQL,
以及智研相关的工具组件。

框架依赖的相关知识点：

* 🐳 [Dockerized](https://www.docker.com/)
* 🐍 [FastAPI](https://fastapi.tiangolo.com/)
* 🙆 [Pydantic](https://docs.pydantic.dev/latest/)
* 🎯 [Gunicorn](https://docs.gunicorn.org/en/stable/index.html)

智研组件自动接入：
...

## 快速上手

### 服务依赖

1. 运行环境：Docker/tlinux、Python 3.9.12

2. 开源组件：Postgres、MySQL、Redis、Kafka（可在配置文件中按需启用）

3. 智研组件：...

### 开发环境搭建
   
1. 推荐拉取已经构建好的镜像手动运行容器
    
    `docker pull mirrors.tencent.com/davidxwangdev/fastapi-matrix-base:v0.1`


2. 也可执行docker目录run_docker.sh构建镜像并运行容器，直接进入容器内部 （不推荐）
    
    `./docker/run_docker.sh`


3. 执行tools目录下run_uvicorn.sh启动服务

    `./tools/run_uvicorn.sh`

4. 观察logs目录下的日志启动记录

### 简单测试

1. 算法调用模型及异步处理逻辑推荐放在src/service目录下， 接口层逻辑推荐放在/api/routes目录


### 接口说明

1. 接口定义在src/api/routes目录下，按文件夹存放独立的api服务，注意文件夹名即为最终url路径的组成部分之一。在文件夹下增加__init__.py，此文件负责初始化路由，可参考helloworld目录的示例

2. 接口可通过SwaggerUI验证

- Backend Application (API docs):
    
    Swagger http://localhost:8888/docs
    
    Redocly http://localhost:8888/redoc

- Backend Application （API inference）:
    
    Demo http://localhost:8888/api/demo

### 配置说明

1. 该框架支持通过.env文件、环境变量三种方式来加载需要的配置源，.env文件可以复制.env.example模板生成，如果存在多份配置源，优先级:本地.env文件>七彩石>环境变量。本地的.env在config中的配置会覆盖backend/.env的配置，用来做七彩石配置发布

2. 自定义配置，自动扫描config目录下的toml文件，使用toml格式的配置文件兼顾易读性和方便使用，比如adaptor是存放第三方调用服务的一些地址和key

### api鉴权客户端代码参考

框架代码内置了支持对称加密签名鉴权，具体客户端使用方法参考如下

```python
import hmac
import time
import uuid

import requests

timestamp = str(int(time.time()))
access_key = "YOUR_ACCESS_KEY" #类似appid，标识是哪个应用，由后台分发
security_key = "YOUR_SECURITY_KEY"  # 私钥，后台分发，不可暴露
nonce = str(uuid.uuid4())
message = f"{timestamp}{security_key}{nonce}{timestamp}"
signature = hmac.new(security_key.encode(), message.encode(), "sha1").hexdigest().upper()

headers = {
    "ailab-access-key": access_key,
    "ailab-timestamp": timestamp,
    "ailab-nonce": nonce,
    "ailab-signature": signature,
}


url = "http://YOUR_SERVER_HOST:YOUR_SERVER_PORT/helloworld"

data = {"a": 2}
response = requests.post(url, json=data, headers=headers)

ret = response.json()
print(ret)

```

### 开源组件说明

框架集成了Postgres、MySQL、Redis、Kafka组件，可在配置文件中按需启动

组件的具体配置可在.env文件中配置

示例：
- `DB_REDIS_ENABLE=True` 开启redis组件
- `DB_REDIS_HOST=redis`
- `DB_REDIS_PORT=6379`
- `DB_REDIS_PASSWORD=YOUR_REDIS_PASSWORD`
- `DB_REDIS_DB=0`

