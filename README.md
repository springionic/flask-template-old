.  
├── app # 项目主目录  
│   ├── __init__.py  
│   ├── components # 组件，主要存放一些业务无关的自定义组件，方便重用  
│   ├── config # 配置  
│   │   ├── __init__.py  
│   │   ├── const.py # 常量，存放可能全局用到的常量值  
│   │   ├── enums.py # 枚举，存放 model 中的枚举，或者其他需要用到的枚举类  
│   │   ├── env.py # 环境变量，存放数据库用户名、密码等，需要不同环境不同值的变量  
│   │   ├── error_codes.py # 错误码  
│   │   └── exceptions.py # 异常，所有自定义异常存放在此  
│   ├── db # 数据库相关  
│   │   ├── __init__.py  
│   │   └── models.py # 所有 model 定义  
│   ├── handlers # 处理器，接收请求，并进行参数校验、调用对应业务处理 service，并响应请求  
│   │   ├── __init__.py  
│   │   ├── base_handler.py # 基础程序，所有新增接口 handler 均继承此类  
│   │   ├── error_handler.py # 全局异常处理器  
│   │   └──* user_handler.py # 示例：用户相关请求 handler  
│   ├── schemas # shema  
│   │   ├── __init__.py  
│   │   ├── model_schemas.py # 存放所有 model 对应的 schema  
│   │   ├── req_schemas.py # 存放所有请求参数 schema  
│   │   └── resp_schemas.py # 存放所有接口响应数据 schema  
│   ├── services # 服务，处理所有业务逻辑  
│   │   ├── __init__.py  
│   │   ├── base_service.py # 基础 service，处理所有业务逻辑  
│   │   └──* user_service.py # 示例：用户服务  
│   └── utils # 工具类  
├── migrations # migration  
│   └── versions # 存放所有 migration 版本  
├── tests # 所有单元测试等所有测试相关源代码  
│   └── __init__.py  
├── logs # 日志目录，存放此项目所有输出日志文件，但是不会提交到 git 仓库，已被 .gitignore 掉  
│   ├── .gitkeep # 保证此目录可以提交到 git，无其他用处  
│   └──* app.log # 示例：日志文件  
├── .gitignore # git ignore 文件规则配置  
├── .gitlab-ci.yml # gitlab CI 脚本文件  
├── Dockerfile # Docker 镜像文件  
├── middlewares.py # 中间件（请求和响应拦截）  
├── README.md # 书写项目说明，如何启动等最快上手的一些操作  
├── requirements.txt # 所有依赖管理  
├── routes.py # 路由，配置请求路径到 handler 的映射  
└── run.py # 入口程序  
