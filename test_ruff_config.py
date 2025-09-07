#!/usr/bin/env python3
import os
import subprocess
import sys

# 设置工作目录为项目根目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 函数：运行Ruff检查


def run_ruff_check():
    """运行Ruff检查并显示结果"""
    print('正在运行Ruff代码检查...')

    try:
        # 检查是否安装了Ruff
        subprocess.run(['which', 'ruff'], check=True, capture_output=True)

        # 运行Ruff检查（使用--show-files参数显示检查的文件）
        result = subprocess.run(
            ['ruff', 'check', '.', '--show-files'], check=False, capture_output=True, text=True
        )

        # 输出检查的文件列表
        print('\nRuff检查的文件:')
        print(result.stdout)

        # 如果有错误输出
        if result.stderr:
            print('\nRuff错误输出:')
            print(result.stderr)

        # 运行Ruff格式化检查
        print('\n正在运行Ruff格式化检查...')
        format_result = subprocess.run(
            ['ruff', 'format', '.', '--check'], check=False, capture_output=True, text=True
        )

        if format_result.stdout:
            print('\nRuff格式化检查结果:')
            print(format_result.stdout)

        if format_result.stderr:
            print('\nRuff格式化错误输出:')
            print(format_result.stderr)

        print('\nRuff配置测试完成！')

    except subprocess.CalledProcessError:
        print("\n错误：未找到Ruff命令。请使用 'pip install ruff' 安装Ruff。")
    except Exception as e:
        print(f'\n运行Ruff检查时出错: {str(e)}')


# 函数：显示当前Ruff配置


def show_ruff_config():
    """显示当前的Ruff配置"""
    print('\n当前Ruff配置概览:')
    print('=====================================')
    print('1. 行长度限制: 100字符')
    print('2. 缩进设置: 4个空格')
    print('3. 启用的主要规则集:')
    print('   - E, F, W: 基础PEP 8规则和代码质量')
    print('   - B: flake8-bugbear (高级错误检测)')
    print('   - C: flake8-comprehensions (列表推导式优化)')
    print('   - I: isort (导入排序)')
    print('   - DJ: flake8-django (Django特定规则)')
    print('   - PL: pylint精选规则')
    print('   - UP: pyupgrade (Python版本升级建议)')
    print('4. 忽略的规则:')
    print('   - F401: 未使用的导入 (在__init__.py中允许)')
    print('   - DJ001, DJ006: 某些Django特定规则')
    print('5. 导入排序配置已设置，适配项目结构')
    print('6. 格式化配置采用Black兼容样式')
    print('=====================================')


if __name__ == '__main__':
    print('Ruff配置测试工具')
    print('=' * 40)

    show_ruff_config()
    run_ruff_check()

    print('\n提示：')
    print("- 运行 'ruff check .' 检查代码问题")
    print("- 运行 'ruff format .' 自动格式化代码")
    print('- 如需自定义配置，请编辑 ruff.toml 文件')
