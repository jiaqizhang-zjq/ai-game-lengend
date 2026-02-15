#!/bin/bash

# 一键启动游戏脚本

echo "================================"
echo "传奇风格游戏启动脚本"
echo "================================"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到Python 3，请先安装Python 3.7+"
    exit 1
fi

# 检查Python版本
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "检测到Python版本：$PYTHON_VERSION"

# 检查pip是否安装
if ! command -v pip3 &> /dev/null; then
    echo "错误：未找到pip3，请先安装pip"
    exit 1
fi

# 检查是否在项目目录中
if [ ! -f "src/main.py" ]; then
    echo "错误：请在项目根目录运行此脚本"
    exit 1
fi

# 检查并安装依赖
echo "检查游戏依赖..."
if ! python3 -c "import pygame" &> /dev/null; then
    echo "未找到pygame，正在安装..."
    pip3 install pygame==2.5.2
    if [ $? -ne 0 ]; then
        echo "错误：安装pygame失败，请手动安装：pip3 install pygame==2.5.2"
        exit 1
    fi
    echo "pygame安装成功！"
else
    echo "pygame已安装，跳过安装步骤"
fi

# 运行游戏
echo "================================"
echo "启动游戏..."
echo "================================"
python3 src/main.py

# 检查游戏是否正常启动
if [ $? -ne 0 ]; then
    echo "错误：游戏启动失败，请检查错误信息"
    exit 1
fi
