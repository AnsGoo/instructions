# 开发命令指南

本项目支持两种方式运行开发命令：通过Python包配置的快捷命令或直接使用Python命令行。为避免添加额外的第三方依赖，推荐直接使用Python命令行方式。

> **注意**：代码质量相关命令（lint、format、fix）需要ruff工具，但脚本会在工具不可用时提供友好提示。

## 直接使用Python命令行（推荐）

这种方式不需要安装项目作为Python包，直接在项目根目录运行：

### 服务器与Django管理命令
- `python -m utils.manage runserver`: 启动Django开发服务器
- `python -m utils.manage migrate`: 应用数据库迁移
- `python -m utils.manage makemigrations`: 创建新的数据库迁移
- `python -m utils.manage check`: 检查Django项目配置
- `python -m utils.manage createsuperuser`: 创建Django超级用户
- `python -m utils.manage shell`: 启动Django交互式shell

### 代码质量与格式化命令
- `python -m utils.manage lint`: 使用Ruff检查代码质量
- `python -m utils.manage format`: 使用Ruff格式化代码
- `python -m utils.manage fix`: 使用Ruff自动修复代码问题

## 使用示例

```bash
# 查看可用命令
python -m utils.manage

# 启动开发服务器
python -m utils.manage runserver

# 格式化代码
python -m utils.manage format

# 创建新的迁移
python -m utils.manage makemigrations

# 应用迁移
python -m utils.manage migrate

# 创建超级用户
python -m utils.manage createsuperuser
```

## 可选：通过Python包配置的快捷命令

如果需要使用快捷命令（如`uv run dev`），需要先安装项目：

```bash
pip install -e .
```

### 可用快捷命令

- `uv run dev`: 启动Django开发服务器
- `uv run runserver`: 同上，启动Django开发服务器
- `uv run check`: 检查Django项目配置
- `uv run migrate`: 应用数据库迁移
- `uv run makemigrations`: 创建新的数据库迁移
- `uv run createsuperuser`: 创建Django超级用户
- `uv run shell`: 启动Django交互式shell
- `uv run manage`: 通用管理命令入口
- `uv run lint`: 使用Ruff检查代码质量
- `uv run format`: 使用Ruff格式化代码
- `uv run fix`: 使用Ruff自动修复代码问题

## 命令实现说明

所有命令都通过`utils/manage.py`模块实现，该模块提供了统一的入口点和错误处理。主要功能包括：

1. 自动切换到正确的工作目录
2. 执行相应的Django管理命令或代码质量工具
3. 保留命令行参数传递
4. 提供友好的帮助信息

## 注意事项
- 确保已激活虚拟环境：`source .venv/bin/activate`
- 所有命令都可以在项目根目录执行
- 命令会自动处理路径，无需手动切换到packages/instructions目录
- 如需查看可用命令列表，可以运行：`python -m utils.manage`