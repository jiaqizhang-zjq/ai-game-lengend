from .base import BaseMonster
import pygame

class Skeleton(BaseMonster):
    """骷髅怪物"""
    
    def __init__(self, x, y):
        """初始化骷髅"""
        super().__init__("骷髅", x, y)
        
        # 骷髅属性
        self.health = 60
        self.max_health = 60
        self.attack = 15
        self.defense = 5
        self.exp = 30
        self.gold = 15
        
        # 掉落物品
        self.drop_items = [
            {'name': '金疮药', 'quantity': 2, 'chance': 0.4, 'type': 'consumable', 'subtype': 'recovery', 'effect': 'health', 'value': 30},
            {'name': '骷髅骨', 'quantity': 1, 'chance': 0.3, 'type': 'material', 'subtype': 'material'},
            {'name': '生锈的剑', 'quantity': 1, 'chance': 0.2, 'type': 'weapon', 'subtype': 'equipment', 'attack': 8, 'defense': 0, 'magic': 0}
        ]
    
    def render_default(self, screen):
        """渲染骷髅"""
        # 骷髅（传奇风格）
        # 头部
        pygame.draw.circle(screen, (200, 200, 200), (self.x + 16, self.y + 10), 6)
        # 身体
        pygame.draw.line(screen, (200, 200, 200), (self.x + 16, self.y + 16), (self.x + 16, self.y + 26), 2)
        # 四肢
        pygame.draw.line(screen, (200, 200, 200), (self.x + 16, self.y + 18), (self.x + 10, self.y + 24), 2)
        pygame.draw.line(screen, (200, 200, 200), (self.x + 16, self.y + 18), (self.x + 22, self.y + 24), 2)
        pygame.draw.line(screen, (200, 200, 200), (self.x + 16, self.y + 26), (self.x + 10, self.y + 32), 2)
        pygame.draw.line(screen, (200, 200, 200), (self.x + 16, self.y + 26), (self.x + 22, self.y + 32), 2)

class Zombie(BaseMonster):
    """僵尸怪物"""
    
    def __init__(self, x, y):
        """初始化僵尸"""
        super().__init__("僵尸", x, y)
        
        # 僵尸属性
        self.health = 80
        self.max_health = 80
        self.attack = 20
        self.defense = 8
        self.exp = 40
        self.gold = 20
        
        # 掉落物品（使用物品ID）
        self.drop_items = [
            {'item_id': 3001, 'quantity': 3, 'chance': 0.5},  # 金疮药
            {'item_id': 4005, 'quantity': 1, 'chance': 0.3},  # 僵尸牙齿
            {'item_id': 4006, 'quantity': 1, 'chance': 0.4}   # 腐烂的肉
        ]
    
    def render_default(self, screen):
        """渲染僵尸"""
        # 僵尸（传奇风格）
        # 头部
        pygame.draw.rect(screen, (50, 150, 50), (self.x + 12, self.y + 8, 8, 8))
        # 身体
        pygame.draw.rect(screen, (50, 100, 50), (self.x + 10, self.y + 16, 12, 14))
        # 四肢
        pygame.draw.line(screen, (50, 100, 50), (self.x + 10, self.y + 18), (self.x + 6, self.y + 26), 2)
        pygame.draw.line(screen, (50, 100, 50), (self.x + 22, self.y + 18), (self.x + 26, self.y + 26), 2)
        pygame.draw.line(screen, (50, 100, 50), (self.x + 12, self.y + 30), (self.x + 8, self.y + 36), 2)
        pygame.draw.line(screen, (50, 100, 50), (self.x + 20, self.y + 30), (self.x + 24, self.y + 36), 2)

class Wolf(BaseMonster):
    """狼怪物"""
    
    def __init__(self, x, y):
        """初始化狼"""
        super().__init__("狼", x, y)
        
        # 狼属性
        self.health = 70
        self.max_health = 70
        self.attack = 18
        self.defense = 4
        self.exp = 35
        self.gold = 18
        self.speed = 3  # 狼跑得更快
        
        # 掉落物品
        self.drop_items = [
            {'name': '金疮药', 'quantity': 2, 'chance': 0.4, 'type': 'consumable', 'subtype': 'recovery', 'effect': 'health', 'value': 30},
            {'name': '狼皮', 'quantity': 1, 'chance': 0.3, 'type': 'material', 'subtype': 'material'},
            {'name': '狼牙', 'quantity': 1, 'chance': 0.2, 'type': 'material', 'subtype': 'material'}
        ]
    
    def render_default(self, screen):
        """渲染狼"""
        # 狼（传奇风格）
        # 头部
        pygame.draw.circle(screen, (100, 100, 100), (self.x + 16, self.y + 12), 6)
        # 身体
        pygame.draw.ellipse(screen, (100, 100, 100), (self.x + 10, self.y + 14, 14, 10))
        # 四肢
        pygame.draw.line(screen, (100, 100, 100), (self.x + 12, self.y + 24), (self.x + 10, self.y + 30), 2)
        pygame.draw.line(screen, (100, 100, 100), (self.x + 20, self.y + 24), (self.x + 22, self.y + 30), 2)
        pygame.draw.line(screen, (100, 100, 100), (self.x + 14, self.y + 24), (self.x + 12, self.y + 30), 2)
        pygame.draw.line(screen, (100, 100, 100), (self.x + 18, self.y + 24), (self.x + 20, self.y + 30), 2)
        # 尾巴
        pygame.draw.line(screen, (100, 100, 100), (self.x + 24, self.y + 18), (self.x + 28, self.y + 16), 2)

class Warrior(BaseMonster):
    """沃玛卫士怪物"""
    
    def __init__(self, x, y):
        """初始化沃玛卫士"""
        super().__init__("沃玛卫士", x, y)
        
        # 沃玛卫士属性
        self.health = 150
        self.max_health = 150
        self.attack = 30
        self.defense = 15
        self.exp = 100
        self.gold = 50
        
        # 掉落物品
        self.drop_items = [
            {'name': '金疮药', 'quantity': 5, 'chance': 0.6, 'type': 'consumable', 'subtype': 'recovery', 'effect': 'health', 'value': 30},
            {'name': '魔法药', 'quantity': 3, 'chance': 0.5, 'type': 'consumable', 'subtype': 'recovery', 'effect': 'magic', 'value': 20},
            {'name': '沃玛号角', 'quantity': 1, 'chance': 0.2, 'type': 'material', 'subtype': 'material'},
            {'name': '雷电术技能书', 'quantity': 1, 'chance': 0.1, 'type': 'skill_book', 'subtype': 'skill', 'skill_name': '雷电术', 'skill_level': 1, 'required_profession': 'mage'},
            {'name': '召唤骷髅技能书', 'quantity': 1, 'chance': 0.1, 'type': 'skill_book', 'subtype': 'skill', 'skill_name': '召唤骷髅', 'skill_level': 1, 'required_profession': 'taoist'}
        ]
    
    def render_default(self, screen):
        """渲染沃玛卫士"""
        # 沃玛卫士（传奇风格）
        # 头部
        pygame.draw.rect(screen, (200, 50, 50), (self.x + 12, self.y + 8, 8, 8))
        # 身体
        pygame.draw.rect(screen, (150, 40, 40), (self.x + 10, self.y + 16, 12, 14))
        # 四肢
        pygame.draw.line(screen, (150, 40, 40), (self.x + 10, self.y + 18), (self.x + 6, self.y + 26), 3)
        pygame.draw.line(screen, (150, 40, 40), (self.x + 22, self.y + 18), (self.x + 26, self.y + 26), 3)
        pygame.draw.line(screen, (150, 40, 40), (self.x + 12, self.y + 30), (self.x + 8, self.y + 36), 3)
        pygame.draw.line(screen, (150, 40, 40), (self.x + 20, self.y + 30), (self.x + 24, self.y + 36), 3)
        # 武器
        pygame.draw.line(screen, (100, 100, 100), (self.x + 6, self.y + 22), (self.x + 2, self.y + 18), 2)

class ZombieKing(BaseMonster):
    """僵尸王怪物"""
    
    def __init__(self, x, y):
        """初始化僵尸王"""
        super().__init__("僵尸王", x, y)
        
        # 僵尸王属性
        self.health = 200
        self.max_health = 200
        self.attack = 35
        self.defense = 20
        self.exp = 150
        self.gold = 75
        
        # 掉落物品（使用物品ID）
        self.drop_items = [
            {'item_id': 3003, 'quantity': 3, 'chance': 0.6},  # 超级金疮药
            {'item_id': 3004, 'quantity': 2, 'chance': 0.5},  # 超级魔法药
            {'item_id': 4005, 'quantity': 2, 'chance': 0.4},  # 僵尸牙齿
            {'item_id': 5004, 'quantity': 1, 'chance': 0.1},  # 半月弯刀技能书
            {'item_id': 5005, 'quantity': 1, 'chance': 0.1}   # 魔法盾技能书
        ]
    
    def render_default(self, screen):
        """渲染僵尸王"""
        # 僵尸王（传奇风格）
        # 头部
        pygame.draw.rect(screen, (30, 100, 30), (self.x + 10, self.y + 6, 12, 10))
        # 身体
        pygame.draw.rect(screen, (20, 80, 20), (self.x + 8, self.y + 16, 16, 16))
        # 四肢
        pygame.draw.line(screen, (20, 80, 20), (self.x + 8, self.y + 20), (self.x + 4, self.y + 28), 3)
        pygame.draw.line(screen, (20, 80, 20), (self.x + 24, self.y + 20), (self.x + 28, self.y + 28), 3)
        pygame.draw.line(screen, (20, 80, 20), (self.x + 12, self.y + 32), (self.x + 8, self.y + 40), 3)
        pygame.draw.line(screen, (20, 80, 20), (self.x + 20, self.y + 32), (self.x + 24, self.y + 40), 3)

class SkeletonKing(BaseMonster):
    """骷髅王怪物"""
    
    def __init__(self, x, y):
        """初始化骷髅王"""
        super().__init__("骷髅王", x, y)
        
        # 骷髅王属性
        self.health = 250
        self.max_health = 250
        self.attack = 40
        self.defense = 10
        self.exp = 200
        self.gold = 100
        
        # 掉落物品
        self.drop_items = [
            {'name': '超级金疮药', 'quantity': 4, 'chance': 0.7, 'type': 'consumable', 'subtype': 'recovery', 'effect': 'health', 'value': 80},
            {'name': '超级魔法药', 'quantity': 3, 'chance': 0.6, 'type': 'consumable', 'subtype': 'recovery', 'effect': 'magic', 'value': 60},
            {'name': '骷髅骨', 'quantity': 3, 'chance': 0.5, 'type': 'material', 'subtype': 'material'},
            {'name': '烈火剑法技能书', 'quantity': 1, 'chance': 0.15, 'type': 'skill_book', 'subtype': 'skill', 'skill_name': '烈火剑法', 'skill_level': 1, 'required_profession': 'warrior'},
            {'name': '群体治愈术技能书', 'quantity': 1, 'chance': 0.1, 'type': 'skill_book', 'subtype': 'skill', 'skill_name': '群体治愈术', 'skill_level': 1, 'required_profession': 'taoist'}
        ]
    
    def render_default(self, screen):
        """渲染骷髅王"""
        # 骷髅王（传奇风格）
        # 头部
        pygame.draw.circle(screen, (220, 220, 220), (self.x + 16, self.y + 10), 8)
        # 身体
        pygame.draw.line(screen, (220, 220, 220), (self.x + 16, self.y + 18), (self.x + 16, self.y + 30), 3)
        # 四肢
        pygame.draw.line(screen, (220, 220, 220), (self.x + 16, self.y + 20), (self.x + 10, self.y + 28), 3)
        pygame.draw.line(screen, (220, 220, 220), (self.x + 16, self.y + 20), (self.x + 22, self.y + 28), 3)
        pygame.draw.line(screen, (220, 220, 220), (self.x + 16, self.y + 30), (self.x + 10, self.y + 38), 3)
        pygame.draw.line(screen, (220, 220, 220), (self.x + 16, self.y + 30), (self.x + 22, self.y + 38), 3)
        # 皇冠
        pygame.draw.line(screen, (255, 215, 0), (self.x + 12, self.y + 8), (self.x + 20, self.y + 8), 2)
        pygame.draw.line(screen, (255, 215, 0), (self.x + 14, self.y + 6), (self.x + 18, self.y + 6), 2)

class WomaBoss(BaseMonster):
    """沃玛教主boss"""
    
    def __init__(self, x, y):
        """初始化沃玛教主"""
        super().__init__("沃玛教主", x, y)
        
        # 沃玛教主属性
        self.health = 500
        self.max_health = 500
        self.attack = 60
        self.defense = 30
        self.exp = 500
        self.gold = 300
        
        # 掉落物品（使用物品ID）
        self.drop_items = [
            {'item_id': 3003, 'quantity': 10, 'chance': 0.9},  # 超级金疮药
            {'item_id': 3004, 'quantity': 8, 'chance': 0.9},  # 超级魔法药
            {'item_id': 4008, 'quantity': 2, 'chance': 0.5},  # 沃玛号角
            {'item_id': 5006, 'quantity': 1, 'chance': 0.3},  # 野蛮冲撞技能书
            {'item_id': 5007, 'quantity': 1, 'chance': 0.3},  # 冰咆哮技能书
            {'item_id': 5008, 'quantity': 1, 'chance': 0.3}   # 召唤神兽技能书
        ]
    
    def render_default(self, screen):
        """渲染沃玛教主"""
        # 沃玛教主（传奇风格）
        # 头部
        pygame.draw.circle(screen, (255, 50, 50), (self.x + 16, self.y + 10), 10)
        # 身体
        pygame.draw.ellipse(screen, (200, 40, 40), (self.x + 8, self.y + 20, 16, 14))
        # 四肢
        pygame.draw.line(screen, (200, 40, 40), (self.x + 8, self.y + 24), (self.x + 4, self.y + 32), 4)
        pygame.draw.line(screen, (200, 40, 40), (self.x + 24, self.y + 24), (self.x + 28, self.y + 32), 4)
        pygame.draw.line(screen, (200, 40, 40), (self.x + 12, self.y + 34), (self.x + 8, self.y + 42), 4)
        pygame.draw.line(screen, (200, 40, 40), (self.x + 20, self.y + 34), (self.x + 24, self.y + 42), 4)
        # 翅膀
        pygame.draw.line(screen, (255, 100, 100), (self.x + 8, self.y + 20), (self.x + 4, self.y + 12), 3)
        pygame.draw.line(screen, (255, 100, 100), (self.x + 24, self.y + 20), (self.x + 28, self.y + 12), 3)

class ZumaGuard(BaseMonster):
    """祖玛卫士怪物"""
    
    def __init__(self, x, y):
        """初始化祖玛卫士"""
        super().__init__("祖玛卫士", x, y)
        
        # 祖玛卫士属性
        self.health = 300
        self.max_health = 300
        self.attack = 45
        self.defense = 25
        self.exp = 250
        self.gold = 150
        
        # 掉落物品
        self.drop_items = [
            {'name': '超级金疮药', 'quantity': 5, 'chance': 0.7, 'type': 'consumable', 'subtype': 'recovery', 'effect': 'health', 'value': 80},
            {'name': '超级魔法药', 'quantity': 4, 'chance': 0.6, 'type': 'consumable', 'subtype': 'recovery', 'effect': 'magic', 'value': 60},
            {'name': '祖玛头像', 'quantity': 1, 'chance': 0.3, 'type': 'material', 'subtype': 'material'},
            {'name': '开天斩技能书', 'quantity': 1, 'chance': 0.1, 'type': 'skill_book', 'subtype': 'skill', 'skill_name': '开天斩', 'skill_level': 1, 'required_profession': 'warrior'},
            {'name': '狂龙紫电技能书', 'quantity': 1, 'chance': 0.1, 'type': 'skill_book', 'subtype': 'skill', 'skill_name': '狂龙紫电', 'skill_level': 1, 'required_profession': 'mage'}
        ]
    
    def render_default(self, screen):
        """渲染祖玛卫士"""
        # 祖玛卫士（传奇风格）
        # 头部
        pygame.draw.rect(screen, (255, 150, 50), (self.x + 11, self.y + 8, 10, 8))
        # 身体
        pygame.draw.rect(screen, (200, 120, 40), (self.x + 9, self.y + 16, 14, 14))
        # 四肢
        pygame.draw.line(screen, (200, 120, 40), (self.x + 9, self.y + 20), (self.x + 5, self.y + 28), 3)
        pygame.draw.line(screen, (200, 120, 40), (self.x + 23, self.y + 20), (self.x + 27, self.y + 28), 3)
        pygame.draw.line(screen, (200, 120, 40), (self.x + 13, self.y + 30), (self.x + 9, self.y + 38), 3)
        pygame.draw.line(screen, (200, 120, 40), (self.x + 19, self.y + 30), (self.x + 23, self.y + 38), 3)
        # 武器
        pygame.draw.line(screen, (255, 215, 0), (self.x + 5, self.y + 24), (self.x + 1, self.y + 20), 2)

class ZumaBoss(BaseMonster):
    """祖玛教主boss"""
    
    def __init__(self, x, y):
        """初始化祖玛教主"""
        super().__init__("祖玛教主", x, y)
        
        # 祖玛教主属性
        self.health = 800
        self.max_health = 800
        self.attack = 80
        self.defense = 40
        self.exp = 1000
        self.gold = 500
        
        # 掉落物品（使用物品ID）
        self.drop_items = [
            {'item_id': 3003, 'quantity': 15, 'chance': 0.95},  # 超级金疮药
            {'item_id': 3004, 'quantity': 12, 'chance': 0.95},  # 超级魔法药
            {'item_id': 4009, 'quantity': 3, 'chance': 0.7},   # 祖玛头像
            {'item_id': 5009, 'quantity': 1, 'chance': 0.5},   # 开天斩技能书
            {'item_id': 5010, 'quantity': 1, 'chance': 0.5},   # 狂龙紫电技能书
            {'item_id': 5011, 'quantity': 1, 'chance': 0.5}    # 道符连击技能书
        ]
    
    def render_default(self, screen):
        """渲染祖玛教主"""
        # 祖玛教主（传奇风格）
        # 头部
        pygame.draw.circle(screen, (255, 200, 100), (self.x + 16, self.y + 12), 12)
        # 身体
        pygame.draw.ellipse(screen, (200, 150, 80), (self.x + 6, self.y + 22, 20, 16))
        # 四肢
        pygame.draw.line(screen, (200, 150, 80), (self.x + 6, self.y + 28), (self.x + 2, self.y + 36), 4)
        pygame.draw.line(screen, (200, 150, 80), (self.x + 26, self.y + 28), (self.x + 30, self.y + 36), 4)
        pygame.draw.line(screen, (200, 150, 80), (self.x + 12, self.y + 38), (self.x + 8, self.y + 46), 4)
        pygame.draw.line(screen, (200, 150, 80), (self.x + 20, self.y + 38), (self.x + 24, self.y + 46), 4)
        # 装饰
        pygame.draw.circle(screen, (255, 215, 0), (self.x + 16, self.y + 12), 4)
        pygame.draw.circle(screen, (255, 215, 0), (self.x + 12, self.y + 26), 3)
        pygame.draw.circle(screen, (255, 215, 0), (self.x + 20, self.y + 26), 3)
