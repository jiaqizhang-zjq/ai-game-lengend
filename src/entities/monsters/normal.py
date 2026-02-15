from .base import BaseMonster
import pygame

class Scarecrow(BaseMonster):
    """稻草人怪物"""
    
    def __init__(self, x, y):
        """初始化稻草人"""
        super().__init__("稻草人", x, y)
        
        # 稻草人属性
        self.health = 30
        self.max_health = 30
        self.attack = 5
        self.defense = 2
        self.exp = 10
        self.gold = 5
        
        # 掉落物品（使用物品ID）
        self.drop_items = [
            {'item_id': 3001, 'quantity': 1, 'chance': 0.3},  # 金疮药
            {'item_id': 4007, 'quantity': 1, 'chance': 0.1}   # 稻草人之心
        ]
    
    def render_default(self, screen):
        """渲染稻草人"""
        # 稻草人（传奇风格）
        # 头部
        pygame.draw.rect(screen, (100, 200, 100), (self.x + 12, self.y + 6, 8, 8))
        # 身体
        pygame.draw.rect(screen, (150, 100, 50), (self.x + 14, self.y + 14, 4, 16))
        # 四肢
        pygame.draw.line(screen, (150, 100, 50), (self.x + 14, self.y + 14), (self.x + 8, self.y + 20), 2)
        pygame.draw.line(screen, (150, 100, 50), (self.x + 18, self.y + 14), (self.x + 24, self.y + 20), 2)
        pygame.draw.line(screen, (150, 100, 50), (self.x + 14, self.y + 30), (self.x + 8, self.y + 36), 2)
        pygame.draw.line(screen, (150, 100, 50), (self.x + 18, self.y + 30), (self.x + 24, self.y + 36), 2)
        # 稻草细节
        pygame.draw.line(screen, (120, 160, 120), (self.x + 12, self.y + 6), (self.x + 16, self.y + 2), 1)
        pygame.draw.line(screen, (120, 160, 120), (self.x + 20, self.y + 6), (self.x + 16, self.y + 2), 1)

class Chicken(BaseMonster):
    """鸡怪物"""
    
    def __init__(self, x, y):
        """初始化鸡"""
        super().__init__("鸡", x, y)
        
        # 鸡属性
        self.health = 20
        self.max_health = 20
        self.attack = 3
        self.defense = 1
        self.exp = 5
        self.gold = 2
        
        # 掉落物品
        self.drop_items = [
            {'name': '鸡肉', 'quantity': 1, 'chance': 0.5},
            {'name': '鸡毛', 'quantity': 1, 'chance': 0.3}
        ]
    
    def render_default(self, screen):
        """渲染鸡"""
        # 鸡（传奇风格）
        # 头部
        pygame.draw.circle(screen, (255, 200, 100), (self.x + 16, self.y + 12), 6)
        # 身体
        pygame.draw.ellipse(screen, (255, 220, 120), (self.x + 10, self.y + 14, 12, 10))
        # 翅膀
        pygame.draw.line(screen, (255, 220, 120), (self.x + 10, self.y + 16), (self.x + 6, self.y + 20), 2)
        pygame.draw.line(screen, (255, 220, 120), (self.x + 22, self.y + 16), (self.x + 26, self.y + 20), 2)
        # 腿
        pygame.draw.line(screen, (255, 180, 80), (self.x + 14, self.y + 24), (self.x + 14, self.y + 30), 2)
        pygame.draw.line(screen, (255, 180, 80), (self.x + 18, self.y + 24), (self.x + 18, self.y + 30), 2)
        # 鸡冠
        pygame.draw.line(screen, (255, 0, 0), (self.x + 16, self.y + 12), (self.x + 16, self.y + 8), 2)

class Deer(BaseMonster):
    """鹿怪物"""
    
    def __init__(self, x, y):
        """初始化鹿"""
        super().__init__("鹿", x, y)
        
        # 鹿属性
        self.health = 40
        self.max_health = 40
        self.attack = 8
        self.defense = 3
        self.exp = 15
        self.gold = 8
        
        # 掉落物品
        self.drop_items = [
            {'name': '鹿肉', 'quantity': 1, 'chance': 0.4},
            {'name': '鹿皮', 'quantity': 1, 'chance': 0.2},
            {'name': '鹿茸', 'quantity': 1, 'chance': 0.1}
        ]
    
    def render_default(self, screen):
        """渲染鹿"""
        # 鹿（传奇风格）
        # 头部
        pygame.draw.circle(screen, (150, 100, 50), (self.x + 16, self.y + 10), 7)
        # 角
        pygame.draw.line(screen, (100, 80, 40), (self.x + 16, self.y + 3), (self.x + 12, self.y - 2), 2)
        pygame.draw.line(screen, (100, 80, 40), (self.x + 16, self.y + 3), (self.x + 20, self.y - 2), 2)
        # 身体
        pygame.draw.rect(screen, (180, 130, 80), (self.x + 12, self.y + 16, 10, 12))
        # 四肢
        pygame.draw.line(screen, (150, 100, 50), (self.x + 12, self.y + 28), (self.x + 10, self.y + 34), 2)
        pygame.draw.line(screen, (150, 100, 50), (self.x + 22, self.y + 28), (self.x + 24, self.y + 34), 2)
        pygame.draw.line(screen, (150, 100, 50), (self.x + 12, self.y + 28), (self.x + 10, self.y + 34), 2)
        pygame.draw.line(screen, (150, 100, 50), (self.x + 22, self.y + 28), (self.x + 24, self.y + 34), 2)
