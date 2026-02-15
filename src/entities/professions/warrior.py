from .base_profession import BaseProfession

class Warrior(BaseProfession):
    """战士职业类"""
    
    def __init__(self, player):
        """初始化战士职业"""
        super().__init__("战士", player)
        self.stat_growth = {
            'health': 15,
            'attack': 5,
            'defense': 3,
            'magic': 1
        }
    
    def initialize_skills(self):
        """初始化战士技能"""
        self.skills = [
            # 基础技能
            {
                'name': "基本剑术",
                'level': 1,
                'max_level': 3,
                'damage': 2.0,
                'cooldown': 600,
                'range': 45,
                'description': "战士的基础攻击技能",
                'damage_type': "attack",
                'animation': "sword_basic",
                'required_level': 1,
                'level_bonus': {
                    'damage': 0.5,
                    'cooldown_reduction': 0.15
                }
            },
            # 中级技能
            {
                'name': "攻杀剑术",
                'level': 0,
                'max_level': 3,
                'damage': 2.8,
                'cooldown': 900,
                'range': 50,
                'description': "强力的单体攻击技能",
                'damage_type': "attack",
                'animation': "sword_power",
                'required_level': 10,
                'level_bonus': {
                    'damage': 0.6,
                    'cooldown_reduction': 0.2
                }
            },
            {
                'name': "半月弯刀",
                'level': 0,
                'max_level': 3,
                'damage': 2.5,
                'cooldown': 1200,
                'range': 55,
                'description': "范围攻击技能",
                'damage_type': "attack",
                'animation': "sword_area",
                'required_level': 15,
                'level_bonus': {
                    'damage': 0.5,
                    'cooldown_reduction': 0.15,
                    'range': 10
                }
            },
            # 高级技能
            {
                'name': "野蛮冲撞",
                'level': 0,
                'max_level': 3,
                'damage': 2.2,
                'cooldown': 1500,
                'range': 30,
                'description': "冲撞前方敌人，造成伤害并击退",
                'damage_type': "attack",
                'animation': "charge",
                'required_level': 20,
                'knockback': True,
                'level_bonus': {
                    'damage': 0.5,
                    'cooldown_reduction': 0.25,
                    'range': 8
                }
            },
            {
                'name': "烈火剑法",
                'level': 0,
                'max_level': 3,
                'damage': 4.0,
                'cooldown': 1800,
                'range': 55,
                'description': "释放火焰剑气，造成高额伤害",
                'damage_type': "attack",
                'animation': "fire_sword",
                'required_level': 25,
                'burn_effect': True,
                'level_bonus': {
                    'damage': 0.8,
                    'cooldown_reduction': 0.25
                }
            },
            {
                'name': "逐日剑法",
                'level': 0,
                'max_level': 3,
                'damage': 3.5,
                'cooldown': 2500,
                'range': 70,
                'description': "远程剑气攻击，可攻击远处敌人",
                'damage_type': "attack",
                'animation': "slash",
                'required_level': 30,
                'level_bonus': {
                    'damage': 0.6,
                    'cooldown_reduction': 0.25,
                    'range': 15
                }
            },
            # 终极技能
            {
                'name': "开天斩",
                'level': 0,
                'max_level': 3,
                'damage': 5.0,
                'cooldown': 3000,
                'range': 80,
                'description': "战士终极技能，释放强大剑气，对目标造成巨额伤害",
                'damage_type': "attack",
                'animation': "heaven_chopper",
                'required_level': 35,
                'level_bonus': {
                    'damage': 1.0,
                    'cooldown_reduction': 0.3,
                    'range': 20
                }
            }
        ]
    
    def initialize_passive_skills(self):
        """初始化战士被动技能"""
        self.passive_skills = [
            {
                'name': "强壮",
                'level': 1,
                'max_level': 5,
                'effect': "增加生命值上限",
                'value': 50,
                'description': "每级增加10%生命值上限"
            },
            {
                'name': "钢铁意志",
                'level': 1,
                'max_level': 5,
                'effect': "增加防御力",
                'value': 5,
                'description': "每级增加5点防御力"
            },
            {
                'name': "武器精通",
                'level': 1,
                'max_level': 5,
                'effect': "增加武器伤害",
                'value': 0.1,
                'description': "每级增加10%武器伤害"
            },
            {
                'name': "战意",
                'level': 0,
                'max_level': 5,
                'effect': "增加攻击速度",
                'value': 0.05,
                'description': "每级增加5%攻击速度，需要等级20"
            },
            {
                'name': "致命一击",
                'level': 0,
                'max_level': 5,
                'effect': "增加暴击率",
                'value': 0.02,
                'description': "每级增加2%暴击率，需要等级30"
            }
        ]
    
    def level_up(self):
        """战士升级时的处理"""
        # 检查是否可以学习新技能
        for skill in self.skills:
            if skill['level'] == 0 and skill.get('required_level', 1) <= self.player.game.level:
                skill['level'] = 1
                print(f"战士学会了新技能：{skill['name']}")
        
        # 检查被动技能升级
        for passive in self.passive_skills:
            if passive.get('required_level', 1) <= self.player.game.level:
                if passive['level'] < passive['max_level']:
                    passive['level'] += 1
                    print(f"战士被动技能升级：{passive['name']} - 等级 {passive['level']}")
    
    def use_skill(self, skill_name, target=None):
        """使用战士技能"""
        # 这里可以添加战士特有的技能使用逻辑
        pass
