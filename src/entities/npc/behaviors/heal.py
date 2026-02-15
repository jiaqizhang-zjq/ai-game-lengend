class HealBehavior:
    """NPC治疗行为"""
    
    def __init__(self, npc):
        """初始化治疗行为"""
        self.npc = npc
    
    def heal(self, player):
        """治疗玩家"""
        if self.npc.npc_type not in ['牧师', '医生', '药店老板']:
            return False, '我不会治疗'
        
        # 计算治疗费用
        heal_cost = max(50, (player.max_health - player.health) * 2)
        # 检查玩家是否有足够的金币
        if getattr(player, 'gold', 0) < heal_cost:
            return False, '金币不足'
        
        # 扣除金币
        player.gold -= heal_cost
        # 恢复玩家生命值
        player.health = player.max_health
        # 恢复玩家魔法值
        if hasattr(player, 'mana') and hasattr(player, 'max_mana'):
            player.mana = player.max_mana
        
        return True, f'治疗成功！花费了{heal_cost}金币，生命值已恢复满'
    
    def get_heal_cost(self, player):
        """获取治疗费用"""
        return max(50, (player.max_health - player.health) * 2)
