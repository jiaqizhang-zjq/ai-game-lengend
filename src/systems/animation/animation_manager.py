import pygame
from .skill_animations import FireBallAnimation, LightningAnimation, HealAnimation, SwordSlashAnimation, SummonAnimation

class AnimationManager:
    """动画管理器"""
    
    def __init__(self):
        """初始化动画管理器"""
        self.animations = []
    
    def add_animation(self, animation):
        """添加动画"""
        self.animations.append(animation)
    
    def create_skill_animation(self, skill_name, x, y, target_x=None, target_y=None, direction=None, target=None):
        """创建技能动画"""
        animation = None
        
        # 根据技能名称创建对应的动画
        if skill_name == "火球术" or skill_name == "fire_ball":
            animation = FireBallAnimation(x, y, target_x, target_y, target)
        elif skill_name == "闪电术" or skill_name == "lightning":
            animation = LightningAnimation(x, y, target_x, target_y, target)
        elif skill_name == "治愈术" or skill_name == "heal":
            animation = HealAnimation(x, y)
        elif skill_name == "基本剑术" or skill_name == "sword_basic":
            animation = SwordSlashAnimation(x, y, direction)
        elif skill_name == "攻杀剑术" or skill_name == "sword_power":
            animation = SwordSlashAnimation(x, y, direction)
        elif skill_name == "半月弯刀" or skill_name == "sword_area":
            animation = SwordSlashAnimation(x, y, direction)
        elif skill_name == "召唤骷髅" or skill_name == "summon_skull":
            animation = SummonAnimation(x, y)
        elif skill_name == "召唤神兽" or skill_name == "summon_beast":
            animation = SummonAnimation(x, y)
        # 战士技能动画
        elif skill_name == "charge" or skill_name == "野蛮冲撞":
            animation = SwordSlashAnimation(x, y, direction)
        elif skill_name == "fire_sword" or skill_name == "烈火剑法":
            animation = FireBallAnimation(x, y, target_x, target_y, target)
        elif skill_name == "slash" or skill_name == "逐日剑法":
            animation = SwordSlashAnimation(x, y, direction)
        # 法师技能动画
        elif skill_name == "fire_area" or skill_name == "地狱火":
            animation = FireBallAnimation(x, y, target_x, target_y, target)
        elif skill_name == "ice_storm" or skill_name == "冰咆哮":
            animation = FireBallAnimation(x, y, target_x, target_y, target)
        elif skill_name == "magic_shield" or skill_name == "魔法盾":
            animation = HealAnimation(x, y)
        elif skill_name == "purple_lightning" or skill_name == "狂龙紫电":
            animation = LightningAnimation(x, y, target_x, target_y, target)
        elif skill_name == "fire_blast" or skill_name == "灭天火":
            animation = FireBallAnimation(x, y, target_x, target_y, target)
        # 道士技能动画
        elif skill_name == "soul_symbol" or skill_name == "灵魂火符":
            animation = FireBallAnimation(x, y, target_x, target_y, target)
        elif skill_name == "invisibility" or skill_name == "隐身术":
            animation = HealAnimation(x, y)
        elif skill_name == "group_heal" or skill_name == "群体治愈术":
            animation = HealAnimation(x, y)
        elif skill_name == "poison" or skill_name == "施毒术":
            animation = FireBallAnimation(x, y, target_x, target_y, target)
        elif skill_name == "symbol_volley" or skill_name == "道符连击":
            animation = FireBallAnimation(x, y, target_x, target_y, target)
        
        if animation:
            self.add_animation(animation)
            return animation
        return None
    
    def update(self):
        """更新所有动画"""
        current_time = pygame.time.get_ticks()
        active_animations = []
        
        for animation in self.animations:
            if animation.active:
                # 无论动画是否完成，都调用update方法
                animation.update(current_time)
                # 只有未完成的动画才保留
                if not animation.completed:
                    active_animations.append(animation)
            elif not animation.completed:
                # 启动未激活且未完成的动画
                animation.start(current_time)
                # 调用update方法
                animation.update(current_time)
                # 只有未完成的动画才保留
                if not animation.completed:
                    active_animations.append(animation)
        
        self.animations = active_animations
    
    def render(self, screen, camera_offset=(0, 0)):
        """渲染所有动画"""
        for animation in self.animations:
            # 渲染所有动画，无论是否激活
            # 因为有些动画可能在这一帧刚被创建，还没被激活
            animation.render(screen, camera_offset)
    
    def clear(self):
        """清空所有动画"""
        self.animations = []
    
    def get_animation_count(self):
        """获取动画数量"""
        return len(self.animations)
