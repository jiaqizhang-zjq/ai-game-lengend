import pygame
import random
import os

class BaseMonster:
    """基础怪物类"""
    
    def __init__(self, name, x, y):
        """初始化怪物"""
        # 基本信息
        self.name = name
        self.x, self.y = x, y
        
        # 刷新点（初始位置）
        self.spawn_point = (x, y)
        # 活动范围（以刷新点为中心的半径）
        if '王' in name or '教主' in name:
            # Boss类型怪物活动范围更大
            self.activity_range = 500
        elif name in ['狼', '僵尸', '骷髅']:
            # 普通怪物
            self.activity_range = 300
        else:
            # 小型怪物
            self.activity_range = 200
        
        # 速度
        self.speed = 1.5
        self.wander_speed = self.speed  # 初始化为正常速度
        
        # 方向
        self.direction = random.randint(0, 3)
        
        # 动画状态
        self.animation_frame = 0
        self.animation_speed = 0.05
        
        # 基本属性（由子类覆盖）
        self.health = 50
        self.max_health = 50
        self.attack = 10
        self.defense = 5
        self.exp = 20
        self.gold = 10
        self.drop_items = []  # 掉落物品
        self.sound_effects = {}  # 声音效果
        
        # 加载声音效果
        self.load_sound_effects()
        
        # AI状态
        self.state = 'wandering'
        self.target = None
        self.wander_timer = 0
        self.wander_duration = random.randint(60, 120)
        
        # 仇恨系统
        self.aggro_list = {}  # 仇恨列表 {player: aggro_value}
        self.aggro_range = 150  # 仇恨范围
        self.attack_range = 30  # 攻击范围
        self.aggro_decay_rate = 0.5  # 仇恨衰减率
        self.last_aggro_time = {}  # 最后获得仇恨的时间
        self.attack_cooldown = 60  # 攻击冷却时间（帧数）
        self.last_attack_time = 0  # 最后攻击时间
        self.combat_state = False  # 战斗状态
        
        # 加载精灵素材
        self.load_sprites()
    
    def update(self, player):
        """更新怪物状态"""
        # 计算与玩家的距离
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx**2 + dy**2)**0.5
        
        # 检查边界并处理
        boundary_breach = False
        
        # 检查是否接近或超出活动区域边界
        if hasattr(self, 'activity_area'):
            area = self.activity_area
            # 计算到边界的距离
            dist_to_left = self.x - area['x1']
            dist_to_right = area['x2'] - self.x
            dist_to_top = self.y - area['y1']
            dist_to_bottom = area['y2'] - self.y
            
            # 检查是否超出边界
            if self.x < area['x1'] or self.x > area['x2'] or self.y < area['y1'] or self.y > area['y2']:
                # 超出边界，执行平滑引导回归
                self.smooth_return_to_area(area)
                boundary_breach = True
            elif min(dist_to_left, dist_to_right, dist_to_top, dist_to_bottom) < 50:
                # 接近边界，触发预警减速
                self.wander_speed = self.speed * 0.7  # 减速
            else:
                # 正常区域，恢复正常速度
                self.wander_speed = self.speed
        else:
            # 使用传统的活动范围检查
            spawn_dx = self.x - self.spawn_point[0]
            spawn_dy = self.y - self.spawn_point[1]
            spawn_distance = (spawn_dx**2 + spawn_dy**2)**0.5
            
            if spawn_distance > self.activity_range:
                # 超出活动范围，执行平滑引导回归
                self.smooth_return_to_spawn()
                boundary_breach = True
            elif spawn_distance > self.activity_range * 0.8:
                # 接近边界，触发预警减速
                self.wander_speed = self.speed * 0.7  # 减速
            else:
                # 正常区域，恢复正常速度
                self.wander_speed = self.speed
        
        # 仇恨系统更新
        if not boundary_breach:
            # 更新仇恨值
            self.update_aggro(player, distance)
            
            # 决定当前目标
            self.update_target()
            
            # 根据状态执行不同行为
            if self.target:
                # 有目标，追击并攻击
                target_distance = ((self.target.x - self.x)**2 + (self.target.y - self.y)**2)**0.5
                
                if target_distance <= self.attack_range:
                    # 攻击范围内，执行攻击
                    self.state = 'attacking'
                    self.attack_target(self.target)
                else:
                    # 追击目标
                    self.state = 'chasing'
                    self.chase(self.target)
            else:
                # 无目标，随机漫游
                self.state = 'wandering'
                self.wander()
        
        # 限制位置
        self.x = max(0, min(2400 - 32, self.x))
        self.y = max(0, min(1800 - 32, self.y))
        
    def wander(self):
        """随机漫游"""
        self.wander_timer += 1
        if self.wander_timer >= self.wander_duration:
            self.direction = random.randint(0, 3)
            self.wander_timer = 0
            self.wander_duration = random.randint(60, 120)
        
        # 移动
        if self.direction == 0:
            self.y -= self.wander_speed
        elif self.direction == 1:
            self.x += self.wander_speed
        elif self.direction == 2:
            self.y += self.wander_speed
        elif self.direction == 3:
            self.x -= self.wander_speed
    
    def smooth_return_to_area(self, area):
        """平滑返回活动区域"""
        # 计算区域中心
        area_center_x = (area['x1'] + area['x2']) // 2
        area_center_y = (area['y1'] + area['y2']) // 2
        
        # 计算到区域中心的方向
        dx = area_center_x - self.x
        dy = area_center_y - self.y
        distance = (dx**2 + dy**2)**0.5
        
        if distance > 0:
            # 平滑向区域中心移动
            move_speed = self.speed * 1.2  # 加速返回
            self.x += (dx / distance) * move_speed
            self.y += (dy / distance) * move_speed
            
            # 更新方向
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.direction = 1
                else:
                    self.direction = 3
            else:
                if dy > 0:
                    self.direction = 2
                else:
                    self.direction = 0
    
    def smooth_return_to_spawn(self):
        """平滑返回刷新点"""
        # 计算到刷新点的方向
        spawn_dx = self.spawn_point[0] - self.x
        spawn_dy = self.spawn_point[1] - self.y
        
        # 归一化方向向量
        distance = (spawn_dx**2 + spawn_dy**2)**0.5
        if distance > 0:
            # 平滑向刷新点移动
            move_speed = self.speed * 1.2  # 加速返回
            self.x += (spawn_dx / distance) * move_speed
            self.y += (spawn_dy / distance) * move_speed
            
            # 更新方向
            if abs(spawn_dx) > abs(spawn_dy):
                if spawn_dx > 0:
                    self.direction = 1
                else:
                    self.direction = 3
            else:
                if spawn_dy > 0:
                    self.direction = 2
                else:
                    self.direction = 0
    
    def load_sprites(self):
        """加载精灵素材"""
        # 尝试加载图片，失败则使用默认颜色
        try:
            base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'assets')
            self.sprites = {}
            
            # 根据怪物名称加载对应的精灵
            monster_sprite_path = os.path.join(base_path, f"sprites/monster/{self.name}.png")
            
            # 特殊处理：鸡和鹿的素材文件名
            if self.name == '鸡':
                monster_sprite_path = os.path.join(base_path, "sprites/monster/鸡.png")
            elif self.name == '鹿':
                monster_sprite_path = os.path.join(base_path, "sprites/monster/鹿.png")
            
            if os.path.exists(monster_sprite_path):
                self.sprites['default'] = pygame.image.load(monster_sprite_path).convert_alpha()
                # 缩放精灵到合适大小（根据怪物类型调整大小，符合盛大传奇风格）
                if self.name in ['狼', '僵尸', '骷髅']:
                    # 较大的怪物
                    self.sprites['default'] = pygame.transform.scale(self.sprites['default'], (30, 30))
                elif self.name in ['稻草人', '鸡', '鹿']:
                    # 较小的怪物
                    self.sprites['default'] = pygame.transform.scale(self.sprites['default'], (24, 24))
                else:
                    # 默认大小
                    self.sprites['default'] = pygame.transform.scale(self.sprites['default'], (28, 28))
                self.use_default_sprites = False
            else:
                # 对于其他怪物，使用默认的渲染
                self.sprites['default'] = None
                self.use_default_sprites = True
                print(f"未找到怪物素材: {monster_sprite_path}")
        except Exception as e:
            print(f"加载怪物精灵失败: {e}")
            self.use_default_sprites = True
            self.sprites = {'default': None}
    
    def chase(self, player):
        """追击玩家"""
        # 计算方向
        if abs(player.x - self.x) > abs(player.y - self.y):
            if player.x > self.x:
                self.x += self.speed
                self.direction = 1
            else:
                self.x -= self.speed
                self.direction = 3
        else:
            if player.y > self.y:
                self.y += self.speed
                self.direction = 2
            else:
                self.y -= self.speed
                self.direction = 0
    
    def return_to_spawn(self):
        """返回刷新点"""
        # 计算到刷新点的方向
        spawn_dx = self.spawn_point[0] - self.x
        spawn_dy = self.spawn_point[1] - self.y
        
        # 归一化方向向量
        distance = (spawn_dx**2 + spawn_dy**2)**0.5
        if distance > 0:
            # 向刷新点移动
            self.x += (spawn_dx / distance) * self.speed * 1.5  # 加速返回
            self.y += (spawn_dy / distance) * self.speed * 1.5
            
            # 更新方向
            if abs(spawn_dx) > abs(spawn_dy):
                if spawn_dx > 0:
                    self.direction = 1
                else:
                    self.direction = 3
            else:
                if spawn_dy > 0:
                    self.direction = 2
                else:
                    self.direction = 0
    
    def render(self, screen):
        """渲染怪物"""
        if not self.use_default_sprites and self.sprites.get('default'):
            # 使用加载的精灵图片
            sprite = self.sprites['default']
            screen.blit(sprite, (self.x, self.y))
        else:
            # 绘制默认怪物
            self.render_default(screen)
        
        # 绘制怪物名字
        self.render_name(screen)
        
        # 绘制血条
        self.render_health_bar(screen)
    
    def render_default(self, screen):
        """渲染默认怪物"""
        # 默认怪物（传奇风格）
        if self.name in ['狼', '僵尸', '骷髅']:
            # 较大的怪物
            pygame.draw.rect(screen, (150, 50, 50), (self.x + 5, self.y + 5, 20, 20))
        elif self.name in ['稻草人', '鸡', '鹿']:
            # 较小的怪物
            pygame.draw.rect(screen, (150, 50, 50), (self.x + 4, self.y + 4, 16, 16))
        else:
            # 默认大小
            pygame.draw.rect(screen, (150, 50, 50), (self.x + 4, self.y + 4, 20, 20))
    
    def render_name(self, screen):
        """渲染怪物名字"""
        # 绘制怪物名字（传奇风格，红色）
        try:
            font = pygame.font.SysFont('hiraginosansgb', 12)
        except:
            try:
                font = pygame.font.SysFont('songti', 12)
            except:
                try:
                    font = pygame.font.SysFont('arialunicode', 12)
                except:
                    font = pygame.font.Font(None, 12)
        text = font.render(self.name, True, (255, 0, 0))
        screen.blit(text, (self.x + 8, self.y - 15))
    
    def render_health_bar(self, screen):
        """渲染血条"""
        # 绘制血条（传奇风格）
        health_bar_width = 32
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y - 10, health_bar_width + 2, 4))
        pygame.draw.rect(screen, (100, 0, 0), (self.x + 1, self.y - 9, health_bar_width, 2))
        pygame.draw.rect(screen, (255, 0, 0), (self.x + 1, self.y - 9, health_bar_width * health_ratio, 2))
    
    def take_damage(self, damage, attacker=None):
        """受到伤害"""
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        
        # 播放受伤声音
        self.play_sound('hurt')
        
        # 如果有攻击者，增加仇恨
        if attacker:
            self.add_aggro(attacker, damage * 2)  # 伤害产生的仇恨值是伤害的2倍
        
        # 如果怪物死亡，播放死亡声音
        if self.is_dead():
            self.play_sound('death')
        
        return actual_damage
    
    def add_aggro(self, target, amount):
        """增加仇恨值"""
        if target not in self.aggro_list:
            self.aggro_list[target] = 0
        
        self.aggro_list[target] += amount
        self.last_aggro_time[target] = pygame.time.get_ticks()
        self.combat_state = True
    
    def update_aggro(self, player, distance):
        """更新仇恨值"""
        # 检查玩家是否在仇恨范围内
        if distance <= self.aggro_range:
            # 基础仇恨值（玩家在范围内）
            self.add_aggro(player, 1)
        
        # 衰减仇恨值
        current_time = pygame.time.get_ticks()
        to_remove = []
        
        for target, aggro in self.aggro_list.items():
            # 检查目标是否还在仇恨范围内
            target_distance = ((target.x - self.x)**2 + (target.y - self.y)**2)**0.5
            
            if target_distance > self.aggro_range * 1.5:
                # 目标超出范围，清除仇恨
                to_remove.append(target)
            else:
                # 衰减仇恨值
                time_since_last_aggro = current_time - self.last_aggro_time.get(target, current_time)
                if time_since_last_aggro > 1000:  # 1秒
                    self.aggro_list[target] = max(0, self.aggro_list[target] - self.aggro_decay_rate)
                    if self.aggro_list[target] <= 0:
                        to_remove.append(target)
        
        # 移除没有仇恨的目标
        for target in to_remove:
            del self.aggro_list[target]
            if target in self.last_aggro_time:
                del self.last_aggro_time[target]
        
        # 如果没有仇恨目标，退出战斗状态
        if not self.aggro_list:
            self.combat_state = False
    
    def update_target(self):
        """更新当前目标"""
        if not self.aggro_list:
            self.target = None
            return
        
        # 选择仇恨值最高的目标
        self.target = max(self.aggro_list.items(), key=lambda x: x[1])[0]
    
    def attack_target(self, target):
        """攻击目标"""
        current_time = pygame.time.get_ticks()
        
        # 检查攻击冷却
        if current_time - self.last_attack_time > self.attack_cooldown * 16:  # 16ms per frame
            # 执行攻击
            damage = self.attack
            target.take_damage(damage, self)
            
            # 播放攻击声音
            self.play_sound('attack')
            
            # 更新最后攻击时间
            self.last_attack_time = current_time
    
    def is_dead(self):
        """是否死亡"""
        return self.health <= 0
    
    def get_drops(self):
        """获取掉落物品"""
        return self.drop_items
    
    def collides_with(self, other):
        """检测是否与其他游戏元素碰撞"""
        # 简化碰撞检测，只返回是否碰撞
        # 为了避免穿模，使用较小的碰撞盒
        if self.name in ['狼', '僵尸', '骷髅']:
            # 较大的怪物
            self_rect = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
        elif self.name in ['稻草人', '鸡', '鹿']:
            # 较小的怪物
            self_rect = pygame.Rect(self.x + 4, self.y + 4, 16, 16)
        else:
            # 默认大小
            self_rect = pygame.Rect(self.x + 4, self.y + 4, 20, 20)
        
        # 根据其他对象类型调整碰撞盒
        if hasattr(other, 'name') and other.name == '玩家':
            # 玩家碰撞盒
            other_rect = pygame.Rect(other.x + 4, other.y + 6, 16, 24)
        else:
            # 默认碰撞盒
            other_rect = pygame.Rect(other.x + 4, other.y + 4, 20, 20)
        
        return self_rect.colliderect(other_rect)
    
    def handle_collision(self, other):
        """处理碰撞"""
        # 不进行推挤，只检测碰撞
        pass
    
    def load_sound_effects(self):
        """加载声音效果"""
        try:
            import os
            base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'assets')
            sound_path = os.path.join(base_path, 'sounds')
            
            # 为不同类型的声音效果设置默认路径
            sound_types = ['attack', 'hurt', 'death']
            
            for sound_type in sound_types:
                # 尝试加载怪物特定的声音
                monster_sound_path = os.path.join(sound_path, f"{self.name.lower().replace(' ', '_')}_{sound_type}.wav")
                if os.path.exists(monster_sound_path):
                    try:
                        self.sound_effects[sound_type] = pygame.mixer.Sound(monster_sound_path)
                    except:
                        pass
                else:
                    # 尝试加载通用声音
                    generic_sound_path = os.path.join(sound_path, f"{sound_type}.wav")
                    if os.path.exists(generic_sound_path):
                        try:
                            self.sound_effects[sound_type] = pygame.mixer.Sound(generic_sound_path)
                        except:
                            pass
        except Exception as e:
            print(f"加载声音效果失败: {e}")
    
    def play_sound(self, sound_type):
        """播放声音效果"""
        if sound_type in self.sound_effects:
            try:
                self.sound_effects[sound_type].play()
            except:
                pass
