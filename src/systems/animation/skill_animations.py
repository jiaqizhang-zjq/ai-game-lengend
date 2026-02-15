import pygame
import math
from .base_animation import BaseAnimation

class FireBallAnimation(BaseAnimation):
    """火球术动画"""
    
    def __init__(self, x, y, target_x, target_y, target=None):
        super().__init__("fire_ball", 300, x, y)  # 减少持续时间，提高飞行速度
        # 如果目标位置为None，使用默认位置
        self.target = target
        self.target_x = target_x if target_x is not None else x + 100
        self.target_y = target_y if target_y is not None else y
        self.size = 10
        self.max_size = 20
        # 保存初始位置
        self.start_x = x
        self.start_y = y
        # 技能速度
        self.speed = 15  # 提高飞行速度
    
    def update(self, current_time):
        if not self.active:
            return False
        
        elapsed = current_time - self.start_time
        
        # 实时更新目标位置
        if self.target and hasattr(self.target, 'x') and hasattr(self.target, 'y'):
            # 根据怪物类型调整目标中心点
            if hasattr(self.target, 'name'):
                if self.target.name in ['狼', '僵尸', '骷髅']:
                    self.target_x = self.target.x + 15
                    self.target_y = self.target.y + 15
                elif self.target.name in ['稻草人', '鸡', '鹿']:
                    self.target_x = self.target.x + 12
                    self.target_y = self.target.y + 12
                else:
                    self.target_x = self.target.x + 14
                    self.target_y = self.target.y + 14
            else:
                self.target_x = self.target.x + 14
                self.target_y = self.target.y + 14
        
        # 计算方向向量
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx**2 + dy**2)**0.5
        
        if distance > 0:
            # 向目标移动
            move_x = (dx / distance) * self.speed
            move_y = (dy / distance) * self.speed
            self.x += move_x
            self.y += move_y
        
        # 检查是否到达目标
        if distance < 10:
            self.completed = True
            return False
        
        # 计算大小变化
        progress = min(elapsed / self.duration, 1.0)
        self.size = 10 + (self.max_size - 10) * progress
        
        return super().update(current_time)
    
    def render(self, screen, camera_offset=(0, 0)):
        if not self.active:
            return
        
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])
        
        # 绘制火球
        pygame.draw.circle(screen, (255, 100, 0), (screen_x, screen_y), int(self.size))
        pygame.draw.circle(screen, (255, 200, 0), (screen_x, screen_y), int(self.size * 0.7))
        pygame.draw.circle(screen, (255, 255, 100), (screen_x, screen_y), int(self.size * 0.4))

class LightningAnimation(BaseAnimation):
    """闪电术动画"""
    
    def __init__(self, x, y, target_x, target_y, target=None):
        super().__init__("lightning", 200, x, y)  # 减少持续时间，提高速度
        # 如果目标位置为None，使用默认位置
        self.target = target
        self.target_x = target_x if target_x is not None else x + 100
        self.target_y = target_y if target_y is not None else y
        self.segments = []
        self.create_segments()
    
    def create_segments(self):
        """创建闪电段"""
        self.segments = []
        steps = 15  # 增加步数，使闪电更流畅
        for i in range(steps + 1):
            progress = i / steps
            segment_x = self.x + (self.target_x - self.x) * progress
            segment_y = self.y + (self.target_y - self.y) * progress
            # 添加随机偏移
            if i > 0 and i < steps:
                segment_x += (math.random() - 0.5) * 15  # 减少偏移，使闪电更集中
                segment_y += (math.random() - 0.5) * 15
            self.segments.append((segment_x, segment_y))
    
    def update(self, current_time):
        if not self.active:
            return False
        
        # 实时更新目标位置
        if self.target and hasattr(self.target, 'x') and hasattr(self.target, 'y'):
            # 根据怪物类型调整目标中心点
            if hasattr(self.target, 'name'):
                if self.target.name in ['狼', '僵尸', '骷髅']:
                    self.target_x = self.target.x + 15
                    self.target_y = self.target.y + 15
                elif self.target.name in ['稻草人', '鸡', '鹿']:
                    self.target_x = self.target.x + 12
                    self.target_y = self.target.y + 12
                else:
                    self.target_x = self.target.x + 14
                    self.target_y = self.target.y + 14
            else:
                self.target_x = self.target.x + 14
                self.target_y = self.target.y + 14
        
        # 每帧重新创建闪电段以产生闪烁效果和实时追踪
        self.create_segments()
        
        return super().update(current_time)
    
    def render(self, screen, camera_offset=(0, 0)):
        if not self.active:
            return
        
        # 绘制闪电
        for i in range(len(self.segments) - 1):
            x1, y1 = self.segments[i]
            x2, y2 = self.segments[i + 1]
            screen_x1 = int(x1 - camera_offset[0])
            screen_y1 = int(y1 - camera_offset[1])
            screen_x2 = int(x2 - camera_offset[0])
            screen_y2 = int(y2 - camera_offset[1])
            
            # 主闪电
            pygame.draw.line(screen, (200, 200, 255), (screen_x1, screen_y1), (screen_x2, screen_y2), 3)
            # 闪电辉光
            pygame.draw.line(screen, (255, 255, 255), (screen_x1, screen_y1), (screen_x2, screen_y2), 1)

class HealAnimation(BaseAnimation):
    """治愈术动画"""
    
    def __init__(self, x, y):
        super().__init__("heal", 1500, x, y)
        self.radius = 0
        self.max_radius = 60
        self.alpha = 255
    
    def update(self, current_time):
        if not self.active:
            return False
        
        elapsed = current_time - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        
        # 计算半径和透明度
        self.radius = self.max_radius * progress
        self.alpha = 255 - int(255 * progress)
        
        return super().update(current_time)
    
    def render(self, screen, camera_offset=(0, 0)):
        if not self.active:
            return
        
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])
        
        # 创建半透明表面
        surface = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        
        # 绘制治愈光环
        for i in range(3):
            ring_radius = self.radius * (0.3 + i * 0.3)
            if ring_radius > 0:
                ring_alpha = int(self.alpha * (0.8 - i * 0.2))
                pygame.draw.circle(surface, (0, 255, 100, ring_alpha), (self.max_radius, self.max_radius), int(ring_radius), 2)
        
        # 绘制中心光点
        pygame.draw.circle(surface, (100, 255, 150, self.alpha), (self.max_radius, self.max_radius), int(self.radius * 0.2))
        
        # 绘制到屏幕
        screen.blit(surface, (screen_x - self.max_radius, screen_y - self.max_radius))

class SwordSlashAnimation(BaseAnimation):
    """剑术动画"""
    
    def __init__(self, x, y, direction):
        super().__init__("sword_slash", 500, x, y)
        self.direction = direction  # 0:上, 1:右, 2:下, 3:左
        self.angle = 0
        self.max_angle = math.pi / 2
        self.length = 40
    
    def update(self, current_time):
        if not self.active:
            return False
        
        elapsed = current_time - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        
        # 计算角度
        self.angle = self.max_angle * progress
        
        return super().update(current_time)
    
    def render(self, screen, camera_offset=(0, 0)):
        if not self.active:
            return
        
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])
        
        # 计算剑气位置
        if self.direction == 0:  # 上
            start_x = screen_x
            start_y = screen_y
            end_x = screen_x
            end_y = screen_y - int(self.length * math.sin(self.angle))
        elif self.direction == 1:  # 右
            start_x = screen_x
            start_y = screen_y
            end_x = screen_x + int(self.length * math.cos(self.angle))
            end_y = screen_y
        elif self.direction == 2:  # 下
            start_x = screen_x
            start_y = screen_y
            end_x = screen_x
            end_y = screen_y + int(self.length * math.sin(self.angle))
        else:  # 左
            start_x = screen_x
            start_y = screen_y
            end_x = screen_x - int(self.length * math.cos(self.angle))
            end_y = screen_y
        
        # 绘制剑气
        pygame.draw.line(screen, (255, 200, 0), (start_x, start_y), (end_x, end_y), 3)
        pygame.draw.line(screen, (255, 255, 200), (start_x, start_y), (end_x, end_y), 1)

class SummonAnimation(BaseAnimation):
    """召唤动画"""
    
    def __init__(self, x, y):
        super().__init__("summon", 2000, x, y)
        self.radius = 0
        self.max_radius = 80
        self.alpha = 255
    
    def update(self, current_time):
        if not self.active:
            return False
        
        elapsed = current_time - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        
        # 计算半径和透明度
        if progress < 0.5:
            self.radius = self.max_radius * (progress * 2)
            self.alpha = 255
        else:
            self.radius = self.max_radius
            self.alpha = 255 - int(255 * (progress - 0.5) * 2)
        
        return super().update(current_time)
    
    def render(self, screen, camera_offset=(0, 0)):
        if not self.active:
            return
        
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])
        
        # 创建半透明表面
        surface = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        
        # 绘制召唤阵
        pygame.draw.circle(surface, (100, 0, 200, self.alpha), (self.max_radius, self.max_radius), int(self.radius), 3)
        pygame.draw.circle(surface, (150, 50, 255, self.alpha), (self.max_radius, self.max_radius), int(self.radius * 0.8), 2)
        pygame.draw.circle(surface, (200, 100, 255, self.alpha), (self.max_radius, self.max_radius), int(self.radius * 0.6), 2)
        
        # 绘制星形图案
        for i in range(8):
            angle = (math.pi * 2 / 8) * i
            star_x = self.max_radius + int(math.cos(angle) * self.radius)
            star_y = self.max_radius + int(math.sin(angle) * self.radius)
            pygame.draw.circle(surface, (255, 200, 255, self.alpha), (star_x, star_y), 3)
        
        # 绘制到屏幕
        screen.blit(surface, (screen_x - self.max_radius, screen_y - self.max_radius))
