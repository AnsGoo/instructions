#!/usr/bin/env python
"""自定义管理脚本，为项目提供各种快捷命令"""

import os
import subprocess
import sys
from functools import wraps

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTRUCTIONS_DIR = os.path.join(PROJECT_ROOT, 'packages', 'instructions')


def ensure_path(func):
    """装饰器，确保在执行命令前切换到正确的目录"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 保存当前工作目录
        original_dir = os.getcwd()
        try:
            return func(*args, **kwargs)
        finally:
            # 恢复原来的工作目录
            os.chdir(original_dir)

    return wrapper


@ensure_path
def run_django_server():
    """启动Django开发服务器"""
    os.chdir(INSTRUCTIONS_DIR)
    subprocess.run([sys.executable, 'manage.py', 'runserver'], check=True)


@ensure_path
def run_django_command(command):
    """运行Django管理命令"""
    os.chdir(INSTRUCTIONS_DIR)
    # 将额外的命令行参数传递给Django命令
    cmd_args = [sys.executable, 'manage.py', command] + sys.argv[1:]
    subprocess.run(cmd_args, check=True)


@ensure_path
def format_code():
    """使用Ruff格式化代码"""
    try:
        subprocess.run([sys.executable, '-m', 'ruff', 'format', '.'], check=True)
    except FileNotFoundError:
        print('错误: 未找到ruff工具。请安装ruff: pip install ruff')
        sys.exit(1)


@ensure_path
def fix_code():
    """使用Ruff自动修复代码问题"""
    try:
        subprocess.run([sys.executable, '-m', 'ruff', 'check', '--fix', '.'], check=True)
    except FileNotFoundError:
        print('错误: 未找到ruff工具。请安装ruff: pip install ruff')
        sys.exit(1)


@ensure_path
def lint_code():
    """使用Ruff检查代码质量"""
    try:
        subprocess.run([sys.executable, '-m', 'ruff', 'check', '.'], check=True)
    except FileNotFoundError:
        print('错误: 未找到ruff工具。请安装ruff: pip install ruff')
        sys.exit(1)


@ensure_path
def run_arbitrary_command():
    """运行任意命令（保留用于向后兼容）"""
    # 这是原始的dev命令入口点
    run_django_server()


ARGS_NUM = 2


# 命令映射，用于直接执行特定的Django命令
def main():
    """主入口函数，根据命令行参数执行相应的操作"""
    if len(sys.argv) < ARGS_NUM:
        print('用法: python -m utils.manage <command>')
        print('可用命令:')
        print('  runserver    - 启动Django开发服务器')
        print('  migrate      - 应用数据库迁移')
        print('  makemigrations - 创建新的数据库迁移')
        print('  check        - 检查Django项目配置')
        print('  createsuperuser - 创建Django超级用户')
        print('  shell        - 启动Django交互式shell')
        print('  format       - 使用Ruff格式化代码')
        print('  fix          - 使用Ruff自动修复代码问题')
        print('  lint         - 使用Ruff检查代码质量')
        sys.exit(1)

    command = sys.argv[1]
    sys.argv = sys.argv[1:]

    command_map = {
        'runserver': run_django_server,
        'migrate': lambda: run_django_command('migrate'),
        'makemigrations': lambda: run_django_command('makemigrations'),
        'check': lambda: run_django_command('check'),
        'createsuperuser': lambda: run_django_command('createsuperuser'),
        'shell': lambda: run_django_command('shell'),
        'format': format_code,
        'fix': fix_code,
        'lint': lint_code,
    }

    if command in command_map:
        command_map[command]()
    else:
        # 如果没有匹配的命令，假设用户想要运行任意Django命令
        os.chdir(INSTRUCTIONS_DIR)
        cmd_args = [sys.executable, 'manage.py', command] + sys.argv[1:]
        subprocess.run(cmd_args, check=True)


# 为每个命令创建独立的入口函数
def dev():
    """开发服务器入口点"""
    run_django_server()


def runserver():
    """开发服务器入口点"""
    run_django_server()


def migrate():
    """数据库迁移入口点"""
    run_django_command('migrate')


def makemigrations():
    """创建迁移入口点"""
    run_django_command('makemigrations')


def check():
    """检查项目配置入口点"""
    run_django_command('check')


def createsuperuser():
    """创建超级用户入口点"""
    run_django_command('createsuperuser')


def shell():
    """交互式shell入口点"""
    run_django_command('shell')


def format():
    """代码格式化入口点"""
    format_code()


def fix():
    """代码修复入口点"""
    fix_code()


def lint():
    """代码检查入口点"""
    lint_code()


def manage():
    """通用管理命令入口点"""
    main()


if __name__ == '__main__':
    main()
