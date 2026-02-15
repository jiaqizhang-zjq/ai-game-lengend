# 传奇风格游戏项目

一个基于 Pygame 开发的传奇风格游戏项目。

## 功能特性

- 三大职业系统：战士、法师、道士
- 技能系统：包含各种职业技能
- 物品系统：武器、防具、药水、技能书
- 怪物系统：普通怪物和 Boss
- 地图系统：多个场景地图
- 任务系统：可接受和完成任务
- 商店系统：与 NPC 交易物品
- 技能快捷键系统：可自定义技能快捷键
- 存档系统：保存游戏进度

## 技术栈

- Python 3.7+
- Pygame 2.5.2

## 安装

### 方法一：使用 pip 安装

```bash
# 克隆仓库
git clone git@github.com:jiaqizhang-zjq/ai-game-lengend.git
cd ai-game-lengend

# 安装依赖
pip install -r requirements.txt

# 或使用 setup.py 安装
pip install -e .
```

### 方法二：直接运行

```bash
# 克隆仓库
git clone git@github.com:jiaqizhang-zjq/ai-game-lengend.git
cd ai-game-lengend

# 安装依赖
pip install pygame==2.5.2

# 运行游戏
python src/main.py
```

## 运行游戏

### 使用命令行工具

如果使用 `pip install -e .` 安装了项目，可以直接使用命令：

```bash
legend-game
```

### 直接运行

```bash
python src/main.py
```

## 游戏操作

- **WASD**：移动角色
- **鼠标点击**：攻击怪物
- **空格键**：自动攻击附近怪物
- **1-0**：使用技能快捷键
- **Tab**：打开背包
- **E**：与附近 NPC 交互
- **ESC**：打开菜单
- **Ctrl+S**：保存游戏

## 项目结构

```
legend-game/
├── assets/           # 游戏资源
│   ├── fonts/        # 字体文件
│   ├── sprites/      # 精灵图片
│   └── terrain/      # 地形图片
├── src/              # 源代码
│   ├── core/         # 核心系统
│   ├── entities/     # 游戏实体
│   ├── items/        # 物品系统
│   ├── map/          # 地图系统
│   ├── systems/      # 游戏系统
│   ├── ui/           # 用户界面
│   └── main.py       # 主入口
├── save/             # 存档文件
├── .gitignore        # Git 忽略文件
├── LICENSE           # 许可证
├── README.md         # 项目说明
├── requirements.txt  # 依赖文件
└── setup.py          # 安装配置
```

## 许可证

MIT License
