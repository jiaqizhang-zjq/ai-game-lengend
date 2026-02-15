from .warrior import Warrior
from .mage import Mage
from .taoist import Taoist

class ProfessionFactory:
    """职业工厂类"""
    
    @staticmethod
    def create_profession(profession_name, player):
        """创建职业实例"""
        if profession_name == "战士":
            return Warrior(player)
        elif profession_name == "法师":
            return Mage(player)
        elif profession_name == "道士":
            return Taoist(player)
        else:
            # 默认创建战士
            return Warrior(player)

# 导出职业类和工厂
__all__ = ["Warrior", "Mage", "Taoist", "ProfessionFactory"]
