#!/bin/bash

# 检查是否安装了Ruff
if ! command -v ruff &> /dev/null
then
    echo "错误: 未找到Ruff命令。请使用 'pip install ruff' 安装Ruff。"
    exit 1
fi

# 显示菜单
show_menu() {
    echo "================ Ruff 工具 ================"
    echo "1. 运行代码检查 (ruff check)"
    echo "2. 自动修复代码问题 (ruff check --fix)"
    echo "3. 格式化代码 (ruff format)"
    echo "4. 查看配置 (查看 ruff.toml)"
    echo "5. 退出"
    echo "=========================================="
}

# 运行代码检查
run_check() {
    echo "正在运行Ruff代码检查..."
    ruff check .
}

# 自动修复代码问题
run_fix() {
    echo "正在自动修复代码问题..."
    ruff check . --fix
}

# 格式化代码
run_format() {
    echo "正在格式化代码..."
    ruff format .
}

# 查看配置
show_config() {
    echo "当前Ruff配置 (ruff.toml):"
    cat ruff.toml
}

# 主程序
export PATH=$PATH:/usr/local/bin  # 确保ruff在PATH中

while true; do
    show_menu
    read -p "请选择操作 [1-5]: " choice
    
    case $choice in
        1)
            run_check
            ;;
        2)
            run_fix
            ;;
        3)
            run_format
            ;;
        4)
            show_config
            ;;
        5)
            echo "退出。"
            exit 0
            ;;
        *)
            echo "无效的选择，请输入1-5。"
            ;;
    esac
    
    echo -e "\n按Enter键继续..."
    read
    clear

done