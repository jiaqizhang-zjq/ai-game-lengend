class BaseProfession:
    """基础职业类"""
    
    def __init__(self, name, player):
        """初始化职业"""
        self.name = name
        self.player = player
        self.skills = []
        self.passive_skills = []
        self.stat_growth = {
            'health': 10,
            'attack': 3,
            'defense': 2,
            'magic': 1
        }
        self.initialize_skills()
        self.initialize_passive_skills()
    
    def initialize_skills(self):
        """初始化技能"""
        pass
    
    def initialize_passive_skills(self):
        """初始化被动技能"""
        pass
    
    def get_skills(self):
        """获取技能列表"""
        return self.skills
    
    def get_passive_skills(self):
        """获取被动技能列表"""
        return self.passive_skills
    
    def get_stat_growth(self):
        """获取属性成长率"""
        return self.stat_growth
    
    def level_up(self):
        """升级时的处理"""
        pass
    
    def use_skill(self, skill_name, target=None):
        """使用技能"""
        pass
    
    def get_profession_info(self):
        """获取职业信息"""
        return {
            'name': self.name,
            'skills': [skill['name'] for skill in self.skills],
            'passive_skills': [skill['name'] for skill in self.passive_skills],
            'stat_growth': self.stat_growth
        }
