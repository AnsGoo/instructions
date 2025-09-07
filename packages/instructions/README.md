# Instructions 应用程序

`instructions` 是整个指令管理系统的主应用程序，实现了指令内容的管理、API接口的提供等核心功能。它依赖于`ext_model`基础模型库。

## 项目概述

此应用程序的主要功能包括：
- 指令内容的创建、编辑、删除和查询
- API接口的提供，支持指令内容的CRUD操作
- 用户权限管理
- 基于`ext_model`的扩展模型应用

## 技术栈

- Python 3.12+
- Django 5.2.5+
- Django REST Framework 3.16.1+
- Django Filter 25.1+
- Markdown 3.8.2+
- PostgreSQL (生产环境) / SQLite (开发环境)
- dotenv 0.9.9+

## 项目结构

```
├── .env             # 环境变量配置文件
├── .python-version  # Python版本指定
├── pyproject.toml   # 项目配置文件
├── README.md        # 项目说明文档
├── content/         # 内容相关应用
├── instructions/    # 主应用配置
└── manage.py        # Django管理脚本
```

## 安装和使用

作为工作区的一部分，此应用程序通常通过主项目的依赖管理进行安装：

```bash
# 在项目根目录执行
uv install
```

### 数据库配置

开发环境默认使用SQLite数据库。对于生产环境，可以在`.env`文件中配置PostgreSQL连接信息。

### 运行应用程序

可以使用项目根目录下的快捷命令启动开发服务器：

```bash
# 在项目根目录执行
python -m utils.manage runserver
```

## 核心功能模块

### content 模块

`content`模块是应用程序的核心，负责管理指令内容，包括：
- 指令的创建、编辑和删除
- 指令内容的存储和检索
- 指令的版本控制

## API接口

应用程序提供了RESTful API接口，可以通过Django REST Framework访问。API端点包括：
- 指令内容的CRUD操作
- 用户认证和授权
- 过滤和排序功能

## 开发工作流程

1. 创建数据库迁移：
   ```bash
   python -m utils.manage makemigrations
   ```

2. 应用数据库迁移：
   ```bash
   python -m utils.manage migrate
   ```

3. 创建超级用户：
   ```bash
   python -m utils.manage createsuperuser
   ```

4. 启动开发服务器：
   ```bash
   python -m utils.manage runserver
   ```

## 配置文件

主要配置文件包括：
- `settings.py`：Django应用程序配置
- `.env`：环境变量配置
- `pyproject.toml`：项目依赖和元数据

## 依赖关系

- Django核心框架
- Django REST Framework
- Markdown
- dotenv
- ext_model (工作区内依赖)

## 许可证

[在此添加许可证信息]