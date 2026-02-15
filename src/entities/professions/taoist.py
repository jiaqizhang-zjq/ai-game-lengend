from .base_profession import BaseProfession

class Taoist(BaseProfession):
    """道士职业类"""
    
    def __init__(self, player):
        """初始化道士职业"""
        super().__init__("道士", player)
        self.stat_growth = {
            'health': 12,
            'attack': 3,
            'defense': 2,
            'magic': 5
        }
    
    def initialize_skills(self):
        """初始化道士技能"""
        self.skills = [
            # 基础技能
            {
                'name': "灵魂火符",
                'level': 1,
                'max_level': 3,
                'damage': 2.2,
                'cooldown': 600,
                'range': 100,
                'description': "道士的基础攻击技能",
                'damage_type': "mixed",
                'animation': "soul_symbol",
                'required_level': 1,
                'level_bonus': {
                    1: {'damage': 2.2, 'cooldown': 600, 'range': 100},
                    2: {'damage': 2.8, 'cooldown': 550, 'range': 110},
                    3: {'damage': 3.4, 'cooldown': 500, 'range': 120}
                }
            },
            {
                'name': "治愈术",
                'level': 1,
                'max_level': 3,
                'heal': 30,
                'cooldown': 900,
                'range': 0,
                'description': "治疗技能",
                'damage_type': "magic",
                'animation': "heal",
                'required_level': 1,
                'level_bonus': {
                    1: {'heal': 30, 'cooldown': 900},
                    2: {'heal': 45, 'cooldown': 800},
                    3: {'heal': 60, 'cooldown': 700}
                }
            },
            # 中级技能
            {
                'name': "召唤骷髅",
                'level': 0,
                'max_level': 3,
                'cooldown': 2500,
                'range': 0,
                'description': "召唤骷髅协助战斗",
                'damage_type': "magic",
                'animation': "summon_skull",
                'required_level': 15,
                'summon_effect': True,
                'level_bonus': {
                    1: {'cooldown': 2500, 'summon_strength': 1.2},
                    2: {'cooldown': 2300, 'summon_strength': 1.6},
                    3: {'cooldown': 2000, 'summon_strength': 2.0}
                }
            },
            {
                'name': "隐身术",
                'level': 0,
                'max_level': 3,
                'cooldown': 3000,
                'duration': 15000,
                'range': 0,
                'description': "使自己隐身一段时间",
                'damage_type': "magic",
                'animation': "invisibility",
                'required_level': 20,
                'stealth_effect': True,
                'level_bonus': {
                    1: {'cooldown': 3000, 'duration': 15000},
                    2: {'cooldown': 2900, 'duration': 20000},
                    3: {'cooldown': 2700, 'duration': 25000}
                }
            },
            # 高级技能
            {
                'name': "群体治愈术",
                'level': 0,
                'max_level': 3,
                'heal': 45,
                'cooldown': 1500,
                'range': 80,
                'description': "范围治疗技能",
                'damage_type': "magic",
                'animation': "group_heal",
                'required_level': 25,
                'level_bonus': {
                    1: {'heal': 45, 'cooldown': 1500, 'range': 80},
                    2: {'heal': 60, 'cooldown': 1400, 'range': 90},
                    3: {'heal': 75, 'cooldown': 1200, 'range': 100}
                }
            },
            {
                'name': "召唤神兽",
                'level': 0,
                'max_level': 3,
                'cooldown': 3600,
                'range': 0,
                'description': "召唤强大的神兽协助战斗",
                'damage_type': "magic",
                'animation': "summon_beast",
                'required_level': 30,
                'summon_effect': True,
                'level_bonus': {
                    1: {'cooldown': 3600, 'summon_strength': 1.3},
                    2: {'cooldown': 3500, 'summon_strength': 1.8},
                    3: {'cooldown': 3300, 'summon_strength': 2.3}
                }
            },
            {
                'name': "施毒术",
                'level': 0,
                'max_level': 3,
                'damage': 1.2,
                'cooldown': 1200,
                'range': 120,
                'description': "对敌人施加毒药，持续造成伤害",
                'damage_type': "magic",
                'animation': "poison",
                'required_level': 10,
                'poison_effect': True,
                'level_bonus': {
                    1: {'damage': 1.2, 'cooldown': 1200, 'range': 120},
                    2: {'damage': 1.5, 'cooldown': 1100, 'range': 130},
                    3: {'damage': 1.8, 'cooldown': 900, 'range': 140}
                }
            },
            {
                'name': "道符连击",
                'level': 0,
                'max_level': 3,
                'damage': 2.5,
                'cooldown': 1800,
                'range': 100,
                'description': "连续发射多个道符，造成高额伤害",
                'damage_type': "mixed",
                'animation': "symbol_volley",
                'required_level': 35,
                'level_bonus': {
                    1: {'damage': 2.5, 'cooldown': 1800, 'range': 100},
                    2: {'damage': 3.0, 'cooldown': 1700, 'range': 110},
                    3: {'damage': 3.5, 'cooldown': 1500, 'range': 120}
                }
            }
        ]
    
    def initialize_passive_skills(self):
        """初始化道士被动技能"""
        self.passive_skills = [
            {
                'name': "道术精通",
                'level': 1,
                'max_level': 3,
                'effect': "增加道术伤害",
                'value': 0.1,
                'description': "每级增加10%道术伤害"
            },
            {
                'name': "生命恢复",
                'level': 1,
                'max_level': 3,
                'effect': "增加生命回复速度",
                'value': 0.05,
                'description': "每级增加5%生命回复速度"
            },
            {
                'name': "精神力",
                'level': 1,
                'max_level': 3,
                'effect': "增加魔法值上限",
                'value': 0.08,
                'description': "每级增加8%魔法值上限"
            },
            {
                'name': "召唤强化",
                'level': 0,
                'max_level': 3,
                'effect': "增强召唤物能力",
                'value': 0.1,
                'description': "每级增加10%召唤物能力，需要等级20"
            },
            {
                'name': "神圣之力",
                'level': 0,
                'max_level': 3,
                'effect': "增加治疗效果",
                'value': 0.1,
                'description': "每级增加10%治疗效果，需要等级30"
            }
        ]
    
    def level_up(self):
        """道士升级时的处理"""
        # 检查是否可以学习新技能
        for skill in self.skills:
            if skill['level'] == 0 and skill.get('required_level', 1) <= self.player.game.level:
                skill['level'] = 1
                print(f"道士学会了新技能：{skill['name']}")
        
        # 检查被动技能升级
        for passive in self.passive_skills:
            if passive.get('required_level', 1) <= self.player.game.level:
                if passive['level'] < passive['max_level']:
                    passive['level'] += 1
                    print(f"道士被动技能升级：{passive['name']} - 等级 {passive['level']}")
    
    def use_skill(self, skill_name, target=None):
        """使用道士技能"""
        # 这里可以添加道士特有的技能使用逻辑
        pass
