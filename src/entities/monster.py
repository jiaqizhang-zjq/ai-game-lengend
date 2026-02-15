# 向后兼容的怪物类，使用新的怪物工厂
from .monsters.factory import MonsterFactory

class Monster:
    """怪物类（向后兼容）"""
    
    def __new__(cls, name, x, y):
        """创建怪物实例，使用怪物工厂"""
        return MonsterFactory.create_monster(name, x, y)
