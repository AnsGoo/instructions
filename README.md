# Instructions 项目

这是一个基于Django的指令管理系统，包含两个主要子项目：`ext_model`（基础模型库）和`instructions`（主应用程序）。

## 项目结构

```
├── packages/
│   ├── ext_model/    # 基础模型库，提供通用数据模型定义
│   └── instructions/ # 主应用程序，实现指令管理功能
├── utils/            # 通用工具和快捷命令
├── pyproject.toml    # 项目配置文件
└── DEVELOPMENT.md    # 开发指南
```

## 技术栈

- Python 3.12+
- Django 5.2.5+
- Django REST Framework 3.16.1+
- PostgreSQL (生产环境) / SQLite (开发环境)
- Ruff (代码质量和格式化)

## 快速开始

### 环境准备

1. 确保安装了Python 3.12或更高版本
2. 安装UV包管理器
   ```bash
   pip install uv
   ```
3. 克隆项目代码

### 安装依赖

```bash
uv install
```

### 开发命令

项目提供了多种快捷命令来简化开发流程。详细信息请查看[DEVELOPMENT.md](DEVELOPMENT.md)文件。

主要命令：

```bash
# 启动开发服务器
python -m utils.manage runserver

# 应用数据库迁移
python -m utils.manage migrate

# 创建新的数据库迁移
python -m utils.manage makemigrations

# 格式化代码
python -m utils.manage format
```

## 子项目说明

- **ext_model**：提供属性模型和扩展模型的定义，是整个系统的基础组件
- **instructions**：主应用程序，实现指令管理功能，包含内容管理、API接口等

## 配置文件

- 主项目配置：`pyproject.toml`
- 开发指南：`DEVELOPMENT.md`
- 子项目配置：`packages/*/pyproject.toml`

## 贡献指南

1. 确保代码符合项目的代码规范
2. 使用Ruff格式化代码：`python -m utils.manage format`
3. 提交前运行检查：`python -m utils.manage check`

## 许可证

[在此添加许可证信息]