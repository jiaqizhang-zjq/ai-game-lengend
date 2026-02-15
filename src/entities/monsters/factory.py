from .normal import Scarecrow, Chicken, Deer
from .advanced import Skeleton, Zombie, Wolf, Warrior, ZombieKing, SkeletonKing, WomaBoss, ZumaGuard, ZumaBoss

class MonsterFactory:
    """怪物工厂类，用于创建怪物实例"""
    
    @staticmethod
    def create_monster(name, x, y):
        """根据名称创建怪物实例
        
        Args:
            name: 怪物名称
            x: x坐标
            y: y坐标
            
        Returns:
            怪物实例
        """
        if name == "稻草人":
            return Scarecrow(x, y)
        elif name == "鸡":
            return Chicken(x, y)
        elif name == "鹿":
            return Deer(x, y)
        elif name == "骷髅":
            return Skeleton(x, y)
        elif name == "僵尸":
            return Zombie(x, y)
        elif name == "狼":
            return Wolf(x, y)
        elif name == "沃玛卫士":
            return Warrior(x, y)
        elif name == "僵尸王":
            return ZombieKing(x, y)
        elif name == "骷髅王":
            return SkeletonKing(x, y)
        elif name == "沃玛教主":
            return WomaBoss(x, y)
        elif name == "祖玛卫士":
            return ZumaGuard(x, y)
        elif name == "祖玛教主":
            return ZumaBoss(x, y)
        else:
            # 默认返回基础怪物
            from .base import BaseMonster
            return BaseMonster(name, x, y)
    
    @staticmethod
    def create_monster_by_id(monster_id, x, y):
        """根据ID创建怪物实例
        
        Args:
            monster_id: 怪物ID
            x: x坐标
            y: y坐标
            
        Returns:
            怪物实例
        """
        from core.id_manager import id_manager
        monster_info = id_manager.get_monster_by_id(monster_id)
        if monster_info:
            return MonsterFactory.create_monster(monster_info['name'], x, y)
        else:
            # 默认返回基础怪物
            from .base import BaseMonster
            return BaseMonster("未知怪物", x, y)
    
    @staticmethod
    def get_available_monsters():
        """获取可用的怪物类型
        
        Returns:
            怪物类型列表
        """
        return ["稻草人", "鸡", "鹿", "骷髅", "僵尸", "狼", "沃玛卫士", "僵尸王", "骷髅王", "沃玛教主", "祖玛卫士", "祖玛教主"]
