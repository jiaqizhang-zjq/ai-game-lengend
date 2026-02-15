from .base import BaseNPC
from .types.village import VillageNPC
from .types.forest import ForestNPC
from .types.desert import DesertNPC
from .types.dungeon import DungeonNPC
from .behaviors.quest import QuestBehavior
from .behaviors.trade import TradeBehavior
from .behaviors.skill import SkillBehavior
from .behaviors.repair import RepairBehavior
from .behaviors.heal import HealBehavior

# 导出所有类
__all__ = [
    'BaseNPC',
    'VillageNPC',
    'ForestNPC',
    'DesertNPC',
    'DungeonNPC',
    'QuestBehavior',
    'TradeBehavior',
    'SkillBehavior',
    'RepairBehavior',
    'HealBehavior'
]

# 创建NPC工厂函数
def create_npc(name, x, y, dialogue, has_shop=False, map_type='村庄', npc_type='普通', function=None):
    """创建NPC的工厂函数"""
    if map_type == '村庄':
        return VillageNPC(name, x, y, dialogue, has_shop, npc_type, function)
    elif map_type == '森林':
        return ForestNPC(name, x, y, dialogue, has_shop, npc_type, function)
    elif map_type == '沙漠':
        return DesertNPC(name, x, y, dialogue, has_shop, npc_type, function)
    elif map_type == '地牢':
        return DungeonNPC(name, x, y, dialogue, has_shop, npc_type, function)
    else:
        return BaseNPC(name, x, y, dialogue, has_shop, map_type, npc_type, function)
