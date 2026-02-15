class RepairBehavior:
    """NPC装备修理行为"""
    
    def __init__(self, npc):
        """初始化修理行为"""
        self.npc = npc
    
    def repair_equipment(self, player, equipment_name):
        """修理装备"""
        if self.npc.npc_type not in ['铁匠', '防具商']:
            return False, '我不会修理装备'
        
        # 检查玩家是否有该装备
        if not hasattr(player, 'equipment'):
            return False, '你没有装备'
        
        # 查找装备
        for equipment in player.equipment:
            if equipment['name'] == equipment_name:
                # 计算修理费用
                repair_cost = equipment.get('price', 100) // 2
                # 检查玩家是否有足够的金币
                if getattr(player, 'gold', 0) < repair_cost:
                    return False, '金币不足'
                # 扣除金币
                player.gold -= repair_cost
                # 修复装备耐久度
                equipment['durability'] = equipment.get('max_durability', 100)
                return True, f'修理成功！花费了{repair_cost}金币'
        
        return False, '装备不存在'
    
    def get_repair_cost(self, equipment):
        """获取修理费用"""
        return equipment.get('price', 100) // 2
