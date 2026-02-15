from .base_profession import BaseProfession

class Mage(BaseProfession):
    """法师职业类"""
    
    def __init__(self, player):
        """初始化法师职业"""
        super().__init__("法师", player)
        self.stat_growth = {
            'health': 8,
            'attack': 2,
            'defense': 1,
            'magic': 8
        }
    
    def initialize_skills(self):
        """初始化法师技能"""
        self.skills = [
            # 基础技能
            {
                'name': "火球术",
                'level': 1,
                'max_level': 3,
                'damage': 2.2,
                'cooldown': 600,
                'range': 150,
                'description': "法师的基础攻击技能",
                'damage_type': "magic",
                'animation': "fire_ball",
                'required_level': 1,
                'burn_effect': True,
                'level_bonus': {
                    'damage': 0.5,
                    'cooldown_reduction': 0.15,
                    'range': 25
                }
            },
            # 中级技能
            {
                'name': "闪电术",
                'level': 0,
                'max_level': 3,
                'damage': 2.8,
                'cooldown': 900,
                'range': 180,
                'description': "强力的单体攻击技能",
                'damage_type': "magic",
                'animation': "lightning",
                'required_level': 10,
                'stun_effect': True,
                'level_bonus': {
                    'damage': 0.6,
                    'cooldown_reduction': 0.2,
                    'range': 35
                }
            },
            {
                'name': "地狱火",
                'level': 0,
                'max_level': 3,
                'damage': 2.6,
                'cooldown': 1500,
                'range': 120,
                'description': "范围攻击技能",
                'damage_type': "magic",
                'animation': "fire_area",
                'required_level': 15,
                'burn_effect': True,
                'level_bonus': {
                    'damage': 0.5,
                    'cooldown_reduction': 0.25,
                    'range': 30
                }
            },
            # 高级技能
            {
                'name': "冰咆哮",
                'level': 0,
                'max_level': 3,
                'damage': 2.7,
                'cooldown': 1200,
                'range': 100,
                'description': "范围冰系攻击，有减速效果",
                'damage_type': "magic",
                'animation': "ice_storm",
                'required_level': 20,
                'slow_effect': True,
                'level_bonus': {
                    'damage': 0.5,
                    'cooldown_reduction': 0.2,
                    'range': 25
                }
            },
            {
                'name': "魔法盾",
                'level': 0,
                'max_level': 3,
                'defense': 2.5,
                'cooldown': 2500,
                'duration': 10000,
                'description': "创建魔法护盾，增加防御力",
                'damage_type': "magic",
                'animation': "magic_shield",
                'required_level': 25,
                'level_bonus': {
                    'defense': 0.8,
                    'cooldown_reduction': 0.25,
                    'duration': 3000
                }
            },
            {
                'name': "狂龙紫电",
                'level': 0,
                'max_level': 3,
                'damage': 3.5,
                'cooldown': 1800,
                'range': 200,
                'description': "强力的单体魔法攻击",
                'damage_type': "magic",
                'animation': "purple_lightning",
                'required_level': 30,
                'stun_effect': True,
                'level_bonus': {
                    'damage': 0.8,
                    'cooldown_reduction': 0.25,
                    'range': 45
                }
            },
            {
                'name': "灭天火",
                'level': 0,
                'max_level': 3,
                'damage': 3.2,
                'cooldown': 1500,
                'range': 150,
                'description': "高伤害的火系攻击",
                'damage_type': "magic",
                'animation': "fire_blast",
                'required_level': 35,
                'burn_effect': True,
                'level_bonus': {
                    'damage': 0.6,
                    'cooldown_reduction': 0.25,
                    'range': 35
                }
            }
        ]
    
    def initialize_passive_skills(self):
        """初始化法师被动技能"""
        self.passive_skills = [
            {
                'name': "魔法精通",
                'level': 1,
                'max_level': 5,
                'effect': "增加魔法值上限",
                'value': 50,
                'description': "每级增加10%魔法值上限"
            },
            {
                'name': "元素掌握",
                'level': 1,
                'max_level': 5,
                'effect': "增加魔法伤害",
                'value': 0.1,
                'description': "每级增加10%魔法伤害"
            },
            {
                'name': "施法速度",
                'level': 1,
                'max_level': 5,
                'effect': "减少技能冷却",
                'value': 0.05,
                'description': "每级减少5%技能冷却时间"
            },
            {
                'name': "魔法回复",
                'level': 0,
                'max_level': 5,
                'effect': "增加魔法回复速度",
                'value': 0.1,
                'description': "每级增加10%魔法回复速度，需要等级20"
            },
            {
                'name': "元素抗性",
                'level': 0,
                'max_level': 5,
                'effect': "增加元素抗性",
                'value': 0.1,
                'description': "每级增加10%元素抗性，需要等级30"
            }
        ]
    
    def level_up(self):
        """法师升级时的处理"""
        # 检查是否可以学习新技能
        for skill in self.skills:
            if skill['level'] == 0 and skill.get('required_level', 1) <= self.player.game.level:
                skill['level'] = 1
                print(f"法师学会了新技能：{skill['name']}")
        
        # 检查被动技能升级
        for passive in self.passive_skills:
            if passive.get('required_level', 1) <= self.player.game.level:
                if passive['level'] < passive['max_level']:
                    passive['level'] += 1
                    print(f"法师被动技能升级：{passive['name']} - 等级 {passive['level']}")
    
    def use_skill(self, skill_name, target=None):
        """使用法师技能"""
        # 这里可以添加法师特有的技能使用逻辑
        pass
