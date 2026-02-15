import pygame
import math
import os

class BaseNPC:
    """基础NPC类"""
    
    def __init__(self, name, x, y, dialogue, has_shop=False, map_type='村庄', npc_type='普通'):
        """初始化NPC"""
        self.name = name
        self.x, self.y = x, y
        self.dialogue = dialogue
        self.has_shop = has_shop
        self.map_type = map_type  # 地图类型
        self.npc_type = npc_type  # NPC类型
        
        # 个性化属性
        self.personality = "友好"  # 性格
        self.background = "普通村民"  # 背景故事
        self.level = 1  # 等级
        self.skills = []  # 技能
        self.mood = "正常"  # 心情
        self.relationships = {}  # 与玩家的关系
        self.memories = []  # 与玩家的互动记忆
        self.daily_routine = []  # 日常行为
        
        # 多轮对话系统
        self.dialogue_history = []
        self.current_dialogue_index = 0
        self.contextual_dialogue = []  # 上下文相关对话
        
        # 商店物品
        self.shop_items = []
        
        # 精灵素材
        self.sprites = {}
        self.use_default_sprites = True
        
        # 活动区域
        self.activity_area = None
        self.associated_building = None
        
        # 初始化商店物品
        self._initialize_shop_items()
        
        # 设置个性化属性
        self._set_personal_attributes()
        
        # 初始化日常行为
        self._initialize_daily_routine()
        
        # 初始化上下文对话
        self._initialize_contextual_dialogue()
        
        # 加载精灵素材
        self.load_sprites()
    
    def set_activity_area(self, area):
        """设置活动区域"""
        self.activity_area = area
    
    def set_associated_building(self, building):
        """设置关联建筑物"""
        self.associated_building = building
    
    def is_in_activity_area(self, x, y):
        """检查坐标是否在活动区域内"""
        if not self.activity_area:
            return False
        area = self.activity_area
        return area['x1'] <= x <= area['x2'] and area['y1'] <= y <= area['y2']
    
    def _initialize_shop_items(self):
        """初始化商店物品"""
        pass
    
    def _set_personal_attributes(self):
        """设置个性化属性"""
        pass
    
    def _initialize_daily_routine(self):
        """初始化日常行为"""
        self.daily_routine = ['早晨活动', '中午休息', '下午活动', '晚上休息']
    
    def _initialize_contextual_dialogue(self):
        """初始化上下文对话"""
        self.contextual_dialogue = {
            'greeting': '你好，旅行者。',
            'quest': '我需要你的帮助。',
            'farewell': '再见，祝你好运！',
            'happy': '今天真是个好日子！',
            'sad': '今天有点难过。',
            'angry': '我很生气！'
        }
    
    def load_sprites(self):
        """加载精灵素材"""
        # 尝试加载图片，失败则使用默认颜色
        try:
            base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'assets')
            self.sprites = {}
            
            # 首先尝试根据NPC类型加载对应的精灵
            type_to_filename = {
                '村长': '村长.png',
                '武器商': '武器商.png',
                '药店老板': '药店老板.png',
                '防具商': 'shop_npc.png',
                '铁匠': 'shop_npc.png',
                '法师': 'shop_npc.png',
                '牧师': 'shop_npc.png',
                '精灵': 'shop_npc.png',
                '德鲁伊': 'shop_npc.png',
                '猎人': 'shop_npc.png',
                '樵夫': 'shop_npc.png',
                '隐士': 'shop_npc.png',
                '商队首领': 'shop_npc.png',
                '向导': 'shop_npc.png',
                '绿洲守卫': 'shop_npc.png',
                '沙漠商人': 'shop_npc.png',
                '游牧民': 'shop_npc.png',
                '守卫': 'shop_npc.png',
                '狱卒': 'shop_npc.png',
                '盗贼': 'shop_npc.png',
                '骷髅兵': 'shop_npc.png'
            }
            
            npc_sprite_path = None
            
            # 尝试根据NPC类型加载
            if self.npc_type in type_to_filename:
                npc_sprite_path = os.path.join(base_path, f"sprites/npc/{type_to_filename[self.npc_type]}")
            
            # 如果根据类型加载失败，尝试根据NPC名称加载
            if not npc_sprite_path or not os.path.exists(npc_sprite_path):
                npc_sprite_path = os.path.join(base_path, f"sprites/npc/{self.name}.png")
            
            # 最后尝试使用默认的shop_npc.png
            if not os.path.exists(npc_sprite_path):
                npc_sprite_path = os.path.join(base_path, "sprites/npc/shop_npc.png")
            
            if os.path.exists(npc_sprite_path):
                self.sprites['default'] = pygame.image.load(npc_sprite_path).convert_alpha()
                # 缩放精灵到合适大小
                self.sprites['default'] = pygame.transform.scale(self.sprites['default'], (32, 32))
                self.use_default_sprites = False
            else:
                # 对于其他NPC，使用默认的渲染
                self.sprites['default'] = None
                self.use_default_sprites = True
                print(f"未找到NPC素材: {npc_sprite_path}")
        except Exception as e:
            print(f"加载NPC精灵失败: {e}")
            self.use_default_sprites = True
            self.sprites = {'default': None}
    
    def render(self, screen):
        """渲染NPC"""
        if not self.use_default_sprites and self.sprites.get('default'):
            # 使用加载的精灵图片
            sprite = self.sprites['default']
            screen.blit(sprite, (self.x, self.y))
            # 使用白色文字以确保在图片背景上清晰可见
            text_color = (255, 255, 255)
        else:
            # 基础颜色
            base_color = (255, 255, 0)  # 黄色
            
            # 根据心情调整颜色亮度
            mood_brightness = {
                '正常': 1.0,
                '积极': 1.2,
                '温和': 0.9,
                '谨慎': 0.8,
                '直率': 1.1,
                '平静': 0.9,
                '神圣': 1.3,
                '欢快': 1.2,
                '轻松': 1.0,
                '专注': 0.8,
                '冷静': 0.9,
                '灵活': 1.0,
                '严肃': 0.8,
                '沉思': 0.7,
                '警惕': 1.1,
                '阴郁': 0.6,
                '疯狂': 1.3,
                '自豪': 1.2,
                '傲慢': 1.1,
                '自信': 1.1,
                '豪放': 1.2,
                '狂野': 1.3,
                '麻木': 0.5
            }
            
            brightness = mood_brightness.get(self.mood, 1.0)
            # 调整颜色亮度
            color = tuple(min(255, int(c * brightness)) for c in base_color)
            
            # 绘制NPC
            pygame.draw.rect(screen, color, (self.x, self.y, 32, 32))
            
            # 根据心情调整文字颜色
            text_color = color
            if brightness > 1.2:
                text_color = (0, 0, 0)  # 深色背景用黑色文字
        
        # 绘制NPC名字
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
        
        text = font.render(self.name, True, text_color)
        screen.blit(text, (self.x + 8, self.y - 15))
        
        # 绘制NPC类型
        type_text = font.render(self.npc_type, True, (200, 200, 200))
        screen.blit(type_text, (self.x + 8, self.y + 35))
        
        # 绘制NPC个性
        personality_text = font.render(self.personality, True, (150, 150, 150))
        screen.blit(personality_text, (self.x + 8, self.y + 50))
        
        # 绘制心情指示器
        self._draw_mood_indicator(screen)
    
    def _draw_mood_indicator(self, screen):
        """绘制心情指示器"""
        # 根据心情绘制不同的指示器
        mood_indicators = {
            '积极': '😊',
            '温和': '😌',
            '谨慎': '😟',
            '直率': '😀',
            '平静': '😐',
            '神圣': '😇',
            '欢快': '😄',
            '轻松': '😎',
            '专注': '🤔',
            '冷静': '😐',
            '灵活': '🤨',
            '严肃': '😠',
            '沉思': '🧐',
            '警惕': '😨',
            '阴郁': '😔',
            '疯狂': '😈',
            '自豪': '😏',
            '傲慢': '😒',
            '自信': '😎',
            '豪放': '🤠',
            '狂野': '😜',
            '麻木': '😶'
        }
        
        indicator = mood_indicators.get(self.mood, '😐')
        # 绘制心情指示器
        font = pygame.font.Font(None, 16)
        text = font.render(indicator, True, (255, 255, 255))
        screen.blit(text, (self.x + 20, self.y - 15))
    
    def get_dialogue(self):
        """获取对话"""
        return self.dialogue
    
    def get_shop_items(self):
        """获取商店物品"""
        if self.has_shop:
            return self.shop_items
        return []
    
    def is_near_player(self, player_x, player_y):
        """检查是否靠近玩家"""
        dx = player_x - self.x
        dy = player_y - self.y
        distance = (dx**2 + dy**2)**0.5
        return distance < 50
    
    def interact(self, player):
        """与玩家交互"""
        # 从game对象中获取玩家等级
        player_level = getattr(player.game, 'level', 1)
        # 记录交互历史
        interaction = f"与{player.职业}交互，等级{player_level}"
        self.dialogue_history.append(interaction)
        
        # 记录互动记忆
        self.memories.append({
            'player_class': player.职业,
            'player_level': player_level,
            'player_name': getattr(player, 'name', '冒险者'),
            'interaction_type': '对话',
            'timestamp': len(self.memories)
        })
        
        # 更新与玩家的关系
        player_id = f"{player.职业}_{getattr(player, 'name', '冒险者')}"
        if player_id not in self.relationships:
            self.relationships[player_id] = 0
        self.relationships[player_id] += 1
        
        # 根据玩家职业、等级、与NPC的关系、NPC心情生成对话
        dialogue = self._generate_contextual_dialogue(player)
        
        # 随机改变NPC心情
        self._update_mood()
        
        return dialogue
    
    def _generate_contextual_dialogue(self, player):
        """生成基于上下文的对话"""
        # 获取与玩家的关系值
        player_id = f"{player.职业}_{getattr(player, 'name', '冒险者')}"
        relationship = self.relationships.get(player_id, 0)
        
        # 基于玩家等级的对话
        if player.level < 10:
            level_dialogue = "年轻的冒险者，"
        elif player.level < 20:
            level_dialogue = "勇敢的冒险者，"
        else:
            level_dialogue = "强大的冒险者，"
        
        # 基于NPC心情的对话
        mood_dialogue = self._get_mood_dialogue()
        
        # 基于交互次数的对话
        if len(self.dialogue_history) == 1:
            # 第一次交互
            if 'greeting' in self.contextual_dialogue:
                return self.contextual_dialogue['greeting']
            else:
                return f"{level_dialogue}欢迎来到{self.map_type}！我是{self.name}，{self.background}。"
        elif len(self.dialogue_history) < 5:
            # 多次交互
            if 'quest' in self.contextual_dialogue and player.level < 15:
                return self.contextual_dialogue['quest']
            else:
                return f"{level_dialogue}{mood_dialogue}我是{self.name}，{self.background}。"
        else:
            # 熟悉的交互
            if 'farewell' in self.contextual_dialogue:
                return f"{mood_dialogue}很高兴再次见到你，{player.职业}。"
            else:
                return f"{level_dialogue}{mood_dialogue}最近过得怎么样？"
    
    def _get_mood_dialogue(self):
        """根据心情生成对话前缀"""
        mood_prefixes = {
            '正常': '',
            '积极': '今天心情真好！',
            '温和': '慢慢来，',
            '谨慎': '小心点，',
            '直率': '说实话，',
            '平静': '静静地，',
            '神圣': '愿神保佑你，',
            '欢快': '哈哈！',
            '轻松': '放松点，',
            '专注': '认真地说，',
            '冷静': '冷静地，',
            '灵活': '灵活点，',
            '严肃': '严肃地说，',
            '沉思': '思考着，',
            '警惕': '小心！',
            '阴郁': '唉...',
            '疯狂': '哈哈哈哈！',
            '自豪': '骄傲地，',
            '傲慢': '哼，',
            '自信': '自信地，',
            '豪放': '痛快！',
            '狂野': '桀桀桀！',
            '麻木': ''
        }
        return mood_prefixes.get(self.mood, '')
    
    def _update_mood(self):
        """随机更新NPC心情"""
        # 基于性格的心情变化
        mood_changes = {
            '慈祥': ['正常', '积极', '温和'],
            '豪爽': ['积极', '直率', '欢快'],
            '细心': ['温和', '谨慎', '平静'],
            '精明': ['谨慎', '灵活', '自信'],
            '粗犷': ['直率', '豪放', '积极'],
            '神秘': ['平静', '沉思', '谨慎'],
            '虔诚': ['神圣', '平静', '温和'],
            '热情': ['欢快', '积极', '轻松'],
            '悠闲': ['轻松', '平静', '温和'],
            '敏锐': ['专注', '警惕', '冷静'],
            '专业': ['冷静', '专注', '严肃'],
            '博学': ['专注', '沉思', '平静'],
            '圆滑': ['灵活', '自信', '谨慎'],
            '忠诚': ['严肃', '警惕', '正常'],
            '优雅': ['平静', '温和', '正常'],
            '野性': ['豪放', '狂野', '专注'],
            '坚韧': ['严肃', '冷静', '正常'],
            '孤独': ['沉思', '平静', '阴郁'],
            '果断': ['直率', '自信', '严肃'],
            '狡猾': ['警惕', '灵活', '谨慎'],
            '麻木': ['麻木'],
            '荣耀': ['自豪', '严肃', '正常'],
            '傲慢': ['傲慢', '自信', '严肃'],
            '勇敢': ['豪放', '积极', '直率']
        }
        
        possible_moods = mood_changes.get(self.personality, ['正常'])
        if possible_moods:
            self.mood = possible_moods[0] if len(possible_moods) == 1 else possible_moods[len(self.dialogue_history) % len(possible_moods)]
    
    def get_personal_info(self):
        """获取NPC个人信息"""
        return {
            'name': self.name,
            'personality': self.personality,
            'background': self.background,
            'skills': self.skills,
            'map_type': self.map_type,
            'npc_type': self.npc_type
        }
    
    def give_quest(self, player):
        """给予任务"""
        # 默认任务
        return {
            'title': '探索世界',
            'description': '勇敢地探索这个世界，变得更加强大。',
            'reward': {'exp': 50, 'gold': 100, 'items': ['金疮药']},
            'level_requirement': 1,
            'type': 'exploration'
        }
