# meepo project



## 开发须知

本项目基础组件列表：

- Python: 3.11
- 包管理工具：poetry
- mongo odm: beanie
- mysql orm: sqlalchemy, tortoise-orm
- 静态检查：ruff
- 类型检查：mypy
- 单元测试：pytest
- 其他工具：pre-commit

## 快速开始

### 下载代码

```shell
git clone https://github.com/shupfock/meepo.git
```

完成代码下载后，使用IDE打开项目

### 初始环境配置

#### windows开发环境额外操作

如果在windows机器上开发，需要安装`make`到系统，便于后续直接通过makefile完成一些常用命令。

1. 打开**PowerShell** 以管理员身份运行
2.

输入以下命令安装Chocolatey包：`Set-ExecutionPolicy Bypass -Scope Process -Force; iex((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))`

3. 在Powershell中运行命令`choco`查看是否安装成功
4. 运行`choco install make`
5. 运行`make --version`检查make是否安装成功

#### 环境初始化

进入到项目根目录，运行命令`make init`。

此过程帮助创建项目的虚拟环境，并完成`poetry`的安装。

需要注意的是：**windows环境开发的同学，在运行此命令生成`.venv`目录后，重新运行此命令会有权限问题，可以考虑将已有`.venv`目录移除**。

完成上述命令后，在自己使用的IDE中将项目虚拟环境设置为根目录`.venv`。

#### 依赖包安装

进入项目根目录，运行命令`make install`。

此命令会完成项目依赖包的安装。

完成上述命令执行，就可以投入开发了。

如有新的依赖包，请通过`poetry add package_name`完成安装。

#### 启动服务

日常开发可以在虚拟环境中`python main.py`或`make debug`启动服务进程。



## 快速上手

为了便于meepo代码库后续的持续迭代和演进，代码库组织方式和开发有一些要注意的点：

### 代码组织

代码库基础结构如下：

```shell
├─app
│  ├─api
│  │  ├─author
│  │  ├─book
│  │  ├─common
│  │  │  ├─errors
│  │  │  └─middlewares
│  │  └─shop
│  ├─config
│  │  ├─infrastructure
│  │  └─modules
│  ├─modules
│  │  ├─author
│  │  │  ├─application
│  │  │  ├─domain
│  │  │  └─infrastructure
│  │  ├─book
│  │  │  ├─application
│  │  │  ├─domain
│  │  │  └─infrastructure
│  │  └─shop
│  │      ├─application
│  │      ├─domain
│  │      └─infrastructure
│  ├─seedwork
│  │  ├─application
│  │  ├─domain
│  │  └─infrastructure
│  ├─task
│  │  ├─crontab
│  │  └─job
│  ├─tests
│  └─utils
└─settings
```

#### app

日常开发，代码基本上会在`app`中实现，其中各个包的作用如下：

- api 对外提供可调用的api
  - common FastAPI中depend或middleware实现的地方
  - author 业务模块的接口实现，新的业务模块应该创建新的package
- config 实现依赖注入的初始化配置，在提供新的service时，需要在此完成service factory的相关配置
- modules 业务模块代码实现
  - xxxx.application 结合仓储抽象方法作编排当前模块对外提供的模块服务，完成请求解析和返回数据组装，此处不要编写过多的业务逻辑
  - xxxx.domain 当前模块的具体业务逻辑，主要包含业务实体entities、中间态数据value_objects、仓储抽象方法repositories、模块服务services
  - xxxx.infrastructure 仓库基础设施，主要内容是完成仓储抽象方法的实现
- seedwork 模板代码和一些基类，供新增模块实现
- task 异步任务
- tests 当前模块的单元测试
- utils 实用组件

#### settings

应用基础配置，以toml格式书写


### 开发

实际代码开发可参考已有实现模块进行。

当前代码库开发并没有采用传统的三层结构。为了实现模块内的高内聚和模块间的低耦合，代码库实现遵循`依赖倒置`和`控制反转`。

另外引入了[Dependency Injector](https://python-dependency-injector.ets-labs.org/)进行依赖注入，在实际开发之前请最好阅读下该库的相关文档。

### 单元测试

可参考已有代码。结合当前代码的组织方式和依赖关系，单元测试最好直接在`xxxx.application.services`层进行测试。避免过多直接深入到`xxxx.domain`的单元测试。这样做的好处是保证了模块对外提供的服务，又便于`domain`层的改动。

额外需要注意的是：

- 当前项目中大量使用了asyncio，测试方法根据实际情况增加`async`关键字
- 对协程对象进行mock的操作，可参考`tests.TestWithAsyncio.test_asyncio`的具体实现或参考[mock.AsyncMock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.AsyncMock)

### Celery异步任务

目录`task`中包含了celery任务的配置和所有异步任务。

#### 周期任务

`app.task.crontab`为周期执行任务

周期任务样例：`app/task/crontab/example.py`

在完成周期任务代码编写后，请注意在`app/task/crontab/__init__.py`中增加新增任务名称，用于导出到全局任务列表；

在`app/task/config.py`的`CeleryConfig.beat_schedule`中增加响应的周期任务配置。

#### 异步任务

`app.task.job`为周期执行任务，可在`app.module.application.service`中导入并异步执行。

#### 执行

命令`make cron`用于启动周期任务调度器。

命令`make task`用于启动任务worker，消费周期任务或其他异步任务。
