class SkillBehavior:
    """NPC技能传授行为"""
    
    def __init__(self, npc):
        """初始化技能传授行为"""
        self.npc = npc
    
    def teach_skill(self, player, skill_name):
        """传授技能给玩家"""
        # 检查NPC是否可以传授技能
        if self.npc.npc_type not in ['法师', '战士', '道士', '教师']:
            return False, '我不会传授技能'
        
        # 检查玩家职业是否有对应技能
        if player.职业 not in self._get_skills():
            return False, '你的职业没有可学习的技能'
        
        # 查找技能
        for skill in self._get_skills()[player.职业]:
            if skill['name'] == skill_name:
                # 检查玩家等级
                if player.level < skill['level_requirement']:
                    return False, f'等级不足，需要{skill["level_requirement"]}级'
                # 检查玩家是否有足够的金币
                if getattr(player, 'gold', 0) < skill['cost']:
                    return False, '金币不足'
                # 检查玩家是否已经学会了这个技能
                if not hasattr(player, 'skills'):
                    player.skills = []
                if any(s['name'] == skill_name for s in player.skills):
                    return False, '你已经学会了这个技能'
                # 扣除金币
                player.gold -= skill['cost']
                # 学习技能
                player.skills.append({
                    'name': skill_name,
                    'description': skill['description'],
                    'level': 1,
                    'max_level': 10
                })
                return True, f'学会了{skill_name}！'
        
        return False, '技能不存在'
    
    def _get_skills(self):
        """获取技能数据库"""
        return {
            '法师': [
                {'name': '火球术', 'description': '发射一个火球攻击敌人', 'cost': 500, 'level_requirement': 5},
                {'name': '冰箭术', 'description': '发射一支冰箭攻击敌人', 'cost': 600, 'level_requirement': 8},
                {'name': '闪电术', 'description': '释放闪电攻击敌人', 'cost': 800, 'level_requirement': 12},
                {'name': '魔法护盾', 'description': '创造一个魔法护盾保护自己', 'cost': 1000, 'level_requirement': 15}
            ],
            '战士': [
                {'name': '猛击', 'description': '用力攻击敌人', 'cost': 400, 'level_requirement': 3},
                {'name': '冲锋', 'description': '快速冲向敌人', 'cost': 500, 'level_requirement': 6},
                {'name': '旋风斩', 'description': '旋转攻击周围的敌人', 'cost': 700, 'level_requirement': 10},
                {'name': '嘲讽', 'description': '吸引敌人的注意力', 'cost': 800, 'level_requirement': 13}
            ],
            '道士': [
                {'name': '治愈术', 'description': '治疗自己或队友', 'cost': 300, 'level_requirement': 2},
                {'name': '隐身术', 'description': '暂时隐身', 'cost': 500, 'level_requirement': 7},
                {'name': '召唤骷髅', 'description': '召唤一个骷髅战士', 'cost': 600, 'level_requirement': 11},
                {'name': '群体治愈', 'description': '治疗周围的队友', 'cost': 900, 'level_requirement': 14}
            ]
        }
    
    def get_available_skills(self, player):
        """获取玩家可以学习的技能"""
        available_skills = []
        player_class = getattr(player, '职业', '战士')
        player_level = getattr(player, 'level', 1)
        player_gold = getattr(player, 'gold', 0)
        
        if player_class in self._get_skills():
            for skill in self._get_skills()[player_class]:
                if player_level >= skill['level_requirement'] and player_gold >= skill['cost']:
                    # 检查玩家是否已经学会了这个技能
                    if not hasattr(player, 'skills') or not any(s['name'] == skill['name'] for s in player.skills):
                        available_skills.append(skill)
        
        return available_skills
