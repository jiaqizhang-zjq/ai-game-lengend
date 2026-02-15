from enum import Enum


class GameState(Enum):
    """游戏状态枚举"""
    MENU = 0         # 菜单
    GAME = 1         # 游戏中
    BATTLE = 2       # 战斗
    SHOP = 3         # 商店
    DIALOGUE = 4     # 对话
    INVENTORY = 5    # 背包和装备
    CHARACTER = 6    # 人物状态和任务
    SKILLS = 7       # 技能天赋
    HELP = 8         # 帮助