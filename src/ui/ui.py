import pygame
import time

from src.core.states import GameState
from src.entities.player import Player


class UI:
    """用户界面类"""
    
    def __init__(self, game):
        """初始化UI"""
        self.game = game
        
        # 字体文件路径
        import os
        base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
        font_path = os.path.join(base_path, 'fonts', 'NotoSansCJKsc-Regular.otf')
        
        # 强制使用字体文件，不使用系统字体
        try:
            # 加载主字体
            self.font = pygame.font.Font(font_path, 24)
            # 加载小字体
            self.small_font = pygame.font.Font(font_path, 16)
            # 加载标题字体
            self.title_font = pygame.font.Font(font_path, 48)
            # 加载大字体（用于界面标题）
            self.large_font = pygame.font.Font(font_path, 36)
        except Exception as e:
            print('字体加载失败:', e)
            # 如果字体文件加载失败，使用默认字体
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 16)
            self.title_font = pygame.font.Font(None, 48)
            self.large_font = pygame.font.Font(None, 36)
        
        # 菜单选项
        self.menu_options = ['返回游戏', '任务状态', '背包装备', '技能天赋', '保存游戏', '退出游戏']
        self.selected_menu_option = 0
        
        # 职业选择
        self.class_options = ['战士', '法师', '道士']
        self.selected_class_option = 0
        self.show_class_selection = False
        
        # 存档选择
        self.show_save_selection = False
        self.show_load_selection = False
        self.selected_save_slot = 0
        
        # 保存提示
        self.show_save_prompt = False
        self.save_prompt_options = ['保存并退出', '直接退出', '取消']
        self.selected_save_prompt_option = 0
        self.selected_load_slot = 0
        
        # 战斗选项
        self.battle_options = ['攻击', '物品', '防御', '逃跑']
        self.selected_battle_option = 0
        
        # 对话
        self.current_dialogue = ''
        self.current_npc = None
        
        # 商店
        self.current_shop_items = []
        self.selected_shop_item = 0
        
        # 背包
        self.selected_inventory_item = 0
        
        # 掉落物品提示
        self.item_drops = []
        
        # 伤害值显示
        self.damage_texts = []
        
        # 游戏内消息显示
        self.game_messages = []
        
        # 选中的怪物
        self.selected_monster = None
        
        # 技能快捷栏设置
        self.skill_hotkeys = []  # 存储技能快捷键对应关系
        self.is_setting_skill = False
        self.selected_skill_index = -1
        
        # 角色名称输入
        self.show_name_input = False
        self.name_input = ""
        self.name_input_active = False
    
    def render_menu(self):
        """渲染菜单"""
        # 绘制背景
        self.game.screen.fill((50, 50, 50))
        
        # 绘制标题
        # 使用预加载的标题字体
        title = self.title_font.render('传奇游戏', True, (255, 215, 0))
        title_x = self.game.width // 2 - title.get_width() // 2
        title_y = 100
        self.game.screen.blit(title, (title_x, title_y))
        
        # 绘制菜单选项、职业选择或存档选择
        if self.show_class_selection:
            # 绘制职业选择
            class_title = self.large_font.render('选择职业', True, (255, 255, 255))
            class_title_x = self.game.width // 2 - class_title.get_width() // 2
            class_title_y = 180
            self.game.screen.blit(class_title, (class_title_x, class_title_y))
            
            # 绘制职业选项
            for i, class_name in enumerate(self.class_options):
                color = (255, 255, 255) if i == self.selected_class_option else (150, 150, 150)
                text = self.font.render(class_name, True, color)
                text_x = self.game.width // 2 - text.get_width() // 2
                text_y = 250 + i * 60
                self.game.screen.blit(text, (text_x, text_y))
                
                # 职业描述
                if class_name == '战士':
                    desc = '高攻击高防御，适合近战'
                elif class_name == '法师':
                    desc = '高魔法伤害，远程攻击'
                elif class_name == '道士':
                    desc = '平衡型，可治疗可召唤'
                desc_text = self.small_font.render(desc, True, (200, 200, 200))
                desc_x = self.game.width // 2 - desc_text.get_width() // 2
                desc_y = text_y + 25
                self.game.screen.blit(desc_text, (desc_x, desc_y))
        elif self.show_load_selection:
            # 绘制加载存档选择
            load_title = self.large_font.render('选择存档', True, (255, 255, 255))
            load_title_x = self.game.width // 2 - load_title.get_width() // 2
            load_title_y = 180
            self.game.screen.blit(load_title, (load_title_x, load_title_y))
            
            # 获取所有存档
            saves = self.game.data_storage.list_saves()
            
            # 绘制存档选项
            if saves:
                for i, save in enumerate(saves):
                    color = (255, 255, 255) if i == self.selected_load_slot else (150, 150, 150)
                    save_info = f"存档 {save['id']} (槽位 {save['slot']}): {save['name']} (等级 {save['level']}, {save['职业']})"
                    text = self.font.render(save_info, True, color)
                    text_x = self.game.width // 2 - text.get_width() // 2
                    text_y = 250 + i * 80
                    self.game.screen.blit(text, (text_x, text_y))
                    
                    # 存档详情
                    details = f"攻击力: {save.get('attack', 10)}, 防御力: {save.get('defense', 5)}, 魔法力: {save.get('magic', 5)}"
                    detail_text = self.small_font.render(details, True, (200, 200, 200))
                    detail_x = self.game.width // 2 - detail_text.get_width() // 2
                    detail_y = text_y + 25
                    self.game.screen.blit(detail_text, (detail_x, detail_y))
                    
                    # 更多详情
                    more_details = f"生命值: {save.get('health', 100)}, 金币: {save['gold']}, 上次保存: {time.strftime('%Y-%m-%d %H:%M', time.localtime(save['timestamp']))}"
                    more_detail_text = self.small_font.render(more_details, True, (150, 150, 150))
                    more_detail_x = self.game.width // 2 - more_detail_text.get_width() // 2
                    more_detail_y = detail_y + 20
                    self.game.screen.blit(more_detail_text, (more_detail_x, more_detail_y))
            else:
                # 没有存档
                no_save_text = self.font.render('没有找到存档', True, (150, 150, 150))
                no_save_x = self.game.width // 2 - no_save_text.get_width() // 2
                no_save_y = 250
                self.game.screen.blit(no_save_text, (no_save_x, no_save_y))
            
            # 绘制返回选项
            back_text = self.font.render('返回', True, (200, 200, 200))
            back_x = self.game.width // 2 - back_text.get_width() // 2
            back_y = 250 + max(len(saves), 1) * 40 + 20
            self.game.screen.blit(back_text, (back_x, back_y))
        elif self.show_save_selection:
            # 绘制保存存档选择
            save_title = self.large_font.render('选择保存槽位', True, (255, 255, 255))
            save_title_x = self.game.width // 2 - save_title.get_width() // 2
            save_title_y = 180
            self.game.screen.blit(save_title, (save_title_x, save_title_y))
            
            # 获取所有存档
            saves = self.game.data_storage.list_saves()
            save_slots = {save['slot']: save for save in saves}
            
            # 绘制存档槽位
            for i in range(3):
                slot = i + 1
                color = (255, 255, 255) if i == self.selected_save_slot else (150, 150, 150)
                
                if slot in save_slots:
                    save = save_slots[slot]
                    slot_info = f"槽位 {slot}: {save['name']} (等级 {save['level']}, {save['职业']})"
                else:
                    slot_info = f"槽位 {slot}: 空"
                
                text = self.font.render(slot_info, True, color)
                text_x = self.game.width // 2 - text.get_width() // 2
                text_y = 250 + i * 40
                self.game.screen.blit(text, (text_x, text_y))
            
            # 绘制返回选项
            back_text = self.font.render('返回', True, (200, 200, 200))
            back_x = self.game.width // 2 - back_text.get_width() // 2
            back_y = 250 + 3 * 40 + 20
            self.game.screen.blit(back_text, (back_x, back_y))
        else:
            # 绘制菜单选项
            # 使用中文选项
            # 检查是否已经在游戏中（通过检查player是否存在）
            in_game = hasattr(self.game, 'player') and self.game.player is not None
            
            if not in_game:
                # 进游戏前的菜单，只显示基本选项
                basic_options = ['开始游戏', '继续游戏', '退出游戏']
                for i, option in enumerate(basic_options):
                    color = (255, 255, 255) if i == self.selected_menu_option else (150, 150, 150)
                    text = self.font.render(option, True, color)
                    text_x = self.game.width // 2 - text.get_width() // 2
                    text_y = 200 + i * 50
                    self.game.screen.blit(text, (text_x, text_y))
            else:
                # 进游戏后的菜单，显示所有选项
                for i, option in enumerate(self.menu_options):
                    color = (255, 255, 255) if i == self.selected_menu_option else (150, 150, 150)
                    text = self.font.render(option, True, color)
                    text_x = self.game.width // 2 - text.get_width() // 2
                    text_y = 200 + i * 50
                    self.game.screen.blit(text, (text_x, text_y))
    
    def render_game_ui(self):
        """渲染游戏UI"""
        player = self.game.player
        
        # 左上角玩家头像框
        # 头像框背景
        pygame.draw.rect(self.game.screen, (0, 0, 0), (10, 10, 80, 90))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (12, 12, 76, 86))
        
        # 玩家头像（使用素材缩略图）
        try:
            import os
            base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
            player_sprite_path = os.path.join(base_path, 'sprites', 'player', 'player_down.png')
            if os.path.exists(player_sprite_path):
                player_avatar = pygame.image.load(player_sprite_path)
                # 缩放到合适的头像大小
                player_avatar = pygame.transform.scale(player_avatar, (50, 50))
                # 显示头像
                self.game.screen.blit(player_avatar, (30, 20))
            else:
                # 加载失败时使用默认颜色
                player_color = (255, 165, 0)  # 战士 - 橙色
                if getattr(player, '职业', '') == '法师':
                    player_color = (0, 0, 255)  # 法师 - 蓝色
                elif getattr(player, '职业', '') == '道士':
                    player_color = (0, 255, 0)  # 道士 - 绿色
                pygame.draw.rect(self.game.screen, player_color, (30, 20, 50, 50))
        except Exception as e:
            print(f"加载玩家头像失败: {e}")
            # 异常时使用默认颜色
            player_color = (255, 165, 0)
            pygame.draw.rect(self.game.screen, player_color, (30, 20, 50, 50))
        
        # 玩家名称
        player_name = getattr(player, 'name', '玩家')
        # 确保文本渲染正确
        try:
            name_text = self.small_font.render(player_name, True, (255, 255, 255))
            # 绘制背景矩形，确保文本可见
            pygame.draw.rect(self.game.screen, (0, 0, 0), (10, 70, 70, 20))
            self.game.screen.blit(name_text, (15, 75))
        except Exception as e:
            print(f"渲染玩家姓名失败: {e}")
            # 使用默认字体和颜色作为后备
            fallback_font = pygame.font.Font(None, 16)
            name_text = fallback_font.render(player_name, True, (255, 255, 255))
            pygame.draw.rect(self.game.screen, (0, 0, 0), (10, 70, 70, 20))
            self.game.screen.blit(name_text, (15, 75))
        
        # 血条
        health_bar_width = 150
        health_ratio = player.health / player.max_health
        pygame.draw.rect(self.game.screen, (0, 0, 0), (100, 10, health_bar_width + 4, 14))
        pygame.draw.rect(self.game.screen, (100, 0, 0), (102, 12, health_bar_width, 10))
        pygame.draw.rect(self.game.screen, (255, 0, 0), (102, 12, health_bar_width * health_ratio, 10))
        
        # 魔法条
        magic_bar_width = 150
        magic_ratio = 0.8  # 临时值
        pygame.draw.rect(self.game.screen, (0, 0, 0), (100, 26, magic_bar_width + 4, 14))
        pygame.draw.rect(self.game.screen, (0, 0, 100), (102, 28, magic_bar_width, 10))
        pygame.draw.rect(self.game.screen, (0, 0, 255), (102, 28, magic_bar_width * magic_ratio, 10))
        
        # 玩家信息
        level_text = self.small_font.render(f'等级: {self.game.level}', True, (255, 255, 255))
        self.game.screen.blit(level_text, (260, 10))
        
        gold_text = self.small_font.render(f'金币: {self.game.gold}', True, (255, 215, 0))
        self.game.screen.blit(gold_text, (260, 30))
        
        # 经验值
        exp_ratio = self.game.experience / self.game.experience_to_next_level
        exp_bar_width = 150
        pygame.draw.rect(self.game.screen, (0, 0, 0), (100, 42, exp_bar_width + 4, 10))
        pygame.draw.rect(self.game.screen, (100, 100, 0), (102, 44, exp_bar_width, 6))
        pygame.draw.rect(self.game.screen, (255, 215, 0), (102, 44, exp_bar_width * exp_ratio, 6))
        exp_text = self.small_font.render(f'经验: {self.game.experience}/{self.game.experience_to_next_level}', True, (255, 215, 0))
        self.game.screen.blit(exp_text, (260, 42))
        
        # 地图坐标
        if hasattr(player, 'x') and hasattr(player, 'y'):
            coord_text = self.small_font.render(f'坐标: ({int(player.x)}, {int(player.y)})', True, (255, 255, 255))
            self.game.screen.blit(coord_text, (170, 55))
        
        # 右上角小地图（调整位置，避免与怪物头像框重叠）
        minimap_y = 110  # 向下移动100像素，避免与怪物头像框重叠
        pygame.draw.rect(self.game.screen, (0, 0, 0), (self.game.width - 164, minimap_y, 154, 154))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (self.game.width - 160, minimap_y + 4, 146, 146))
        
        # 获取当前地图
        current_map = None
        if hasattr(self.game, 'map_manager'):
            current_map = self.game.map_manager.get_current_map()
        
        # 绘制小地图内容
        if current_map:
            # 使用当前地图的实际数据绘制缩略图
            minimap_width = 146
            minimap_height = 146
            
            # 获取地图尺寸
            map_width = getattr(current_map, 'width', 2400)
            map_height = getattr(current_map, 'height', 1800)
            
            # 计算缩放比例
            scale_x = minimap_width / map_width
            scale_y = minimap_height / map_height
            
            # 绘制地图地形
            # 简单实现：根据地图类型绘制不同的背景
            map_name = getattr(current_map, 'name', '未知地图')
            
            # 根据地图名称设置背景颜色
            if '雪原' in map_name:
                # 雪原地图 - 白色背景
                pygame.draw.rect(self.game.screen, (200, 200, 255), (self.game.width - 160, minimap_y + 4, minimap_width, minimap_height))
            elif '森林' in map_name:
                # 森林地图 - 绿色背景
                pygame.draw.rect(self.game.screen, (100, 150, 100), (self.game.width - 160, minimap_y + 4, minimap_width, minimap_height))
            elif '沙漠' in map_name:
                # 沙漠地图 - 黄色背景
                pygame.draw.rect(self.game.screen, (200, 180, 120), (self.game.width - 160, minimap_y + 4, minimap_width, minimap_height))
            else:
                # 默认地图 - 棕色背景
                pygame.draw.rect(self.game.screen, (150, 120, 80), (self.game.width - 160, minimap_y + 4, minimap_width, minimap_height))
            
            # 绘制网格线
            for x in range(0, minimap_width, 20):
                pygame.draw.line(self.game.screen, (80, 80, 80), (self.game.width - 160 + x, minimap_y + 4), (self.game.width - 160 + x, minimap_y + 4 + minimap_height))
            for y in range(0, minimap_height, 20):
                pygame.draw.line(self.game.screen, (80, 80, 80), (self.game.width - 160, minimap_y + 4 + y), (self.game.width - 160 + minimap_width, minimap_y + 4 + y))
            
            # 绘制玩家位置
            if hasattr(self.game.player, 'x') and hasattr(self.game.player, 'y'):
                # 计算玩家在小地图上的位置
                player_minimap_x = int(self.game.player.x * scale_x)
                player_minimap_y = int(self.game.player.y * scale_y)
                
                # 确保位置在小地图范围内
                player_minimap_x = max(3, min(minimap_width - 3, player_minimap_x))
                player_minimap_y = max(3, min(minimap_height - 3, player_minimap_y))
                
                # 绘制玩家位置
                pygame.draw.circle(self.game.screen, (255, 0, 0), (self.game.width - 160 + player_minimap_x, minimap_y + 4 + player_minimap_y), 5)
                
                # 绘制玩家方向指示器
                player_direction = getattr(self.game.player, 'direction', 0)
                direction_offset = {
                    0: (0, -3),  # 上
                    1: (3, 0),   # 右
                    2: (0, 3),   # 下
                    3: (-3, 0)   # 左
                }.get(player_direction, (0, 0))
                pygame.draw.circle(self.game.screen, (255, 255, 0), 
                                 (self.game.width - 160 + player_minimap_x + direction_offset[0], 
                                  minimap_y + 4 + player_minimap_y + direction_offset[1]), 2)
            
            # 绘制怪物位置
            if hasattr(current_map, 'monsters'):
                for monster in current_map.monsters:
                    if not monster.is_dead():
                        # 计算怪物在小地图上的位置
                        monster_x = int(monster.x * scale_x)
                        monster_y = int(monster.y * scale_y)
                        
                        # 确保位置在小地图范围内
                        if 0 <= monster_x < minimap_width and 0 <= monster_y < minimap_height:
                            # 检查是否是boss
                            is_boss = hasattr(monster, 'name') and ('王' in monster.name or '教主' in monster.name)
                            if is_boss:
                                # 绘制boss位置（使用红色大圆点）
                                pygame.draw.circle(self.game.screen, (255, 0, 0), 
                                                 (self.game.width - 160 + monster_x, minimap_y + 4 + monster_y), 4)
                            else:
                                # 绘制普通怪物位置
                                pygame.draw.circle(self.game.screen, (255, 100, 100), 
                                                 (self.game.width - 160 + monster_x, minimap_y + 4 + monster_y), 2)
            
            # 绘制传动点位置（地图出口）
            if hasattr(current_map, 'exits'):
                for exit in current_map.exits:
                    # 计算出口中心在小地图上的位置
                    exit_center_x = int((exit['x'] + exit['width'] // 2) * scale_x)
                    exit_center_y = int((exit['y'] + exit['height'] // 2) * scale_y)
                    
                    # 确保位置在小地图范围内
                    if 0 <= exit_center_x < minimap_width and 0 <= exit_center_y < minimap_height:
                        # 绘制传动点位置（使用蓝色菱形）
                        points = [
                            (self.game.width - 160 + exit_center_x, minimap_y + 4 + exit_center_y - 4),
                            (self.game.width - 160 + exit_center_x + 4, minimap_y + 4 + exit_center_y),
                            (self.game.width - 160 + exit_center_x, minimap_y + 4 + exit_center_y + 4),
                            (self.game.width - 160 + exit_center_x - 4, minimap_y + 4 + exit_center_y)
                        ]
                        pygame.draw.polygon(self.game.screen, (0, 0, 255), points)
            
            # 绘制地图名称
            map_name_text = self.small_font.render(map_name, True, (255, 255, 255))
            self.game.screen.blit(map_name_text, (self.game.width - 160 + 5, minimap_y + 4 + 5))
        else:
            # 没有地图数据，显示默认网格
            for x in range(0, 146, 20):
                for y in range(0, 146, 20):
                    color = (120, 150, 120)
                    pygame.draw.rect(self.game.screen, color, (self.game.width - 160 + x, minimap_y + 4 + y, 20, 20))
            
            # 默认玩家位置
            pygame.draw.circle(self.game.screen, (255, 0, 0), (self.game.width - 160 + 73, minimap_y + 4 + 73), 5)
            
            # 显示"未知地图"
            unknown_text = self.small_font.render('未知地图', True, (255, 255, 255))
            self.game.screen.blit(unknown_text, (self.game.width - 160 + 5, minimap_y + 4 + 5))
        
        # 怪物头像框（当选中怪物时）
        if self.selected_monster:
            monster = self.selected_monster
            # 怪物头像框背景
            pygame.draw.rect(self.game.screen, (0, 0, 0), (self.game.width - 190, 10, 180, 90))
            pygame.draw.rect(self.game.screen, (100, 0, 0), (self.game.width - 188, 12, 176, 86))
            
            # 怪物头像（使用素材缩略图）
            try:
                import os
                base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
                monster_name = getattr(monster, 'name', '怪物')
                # 根据怪物名称选择对应的素材图片
                monster_sprite_map = {
                    '稻草人': '稻草人.png',
                    '鸡': '鸡.png',
                    '僵尸': '僵尸.png',
                    '骷髅': '骷髅.png',
                    '狼': '狼.png',
                    '鹿': '鹿.png'
                }
                sprite_file = monster_sprite_map.get(monster_name, '狼.png')  # 默认使用狼的图片
                monster_sprite_path = os.path.join(base_path, 'sprites', 'monster', sprite_file)
                
                if os.path.exists(monster_sprite_path):
                    monster_avatar = pygame.image.load(monster_sprite_path)
                    # 缩放到合适的头像大小
                    monster_avatar = pygame.transform.scale(monster_avatar, (30, 30))
                    # 显示头像
                    self.game.screen.blit(monster_avatar, (self.game.width - 115, 25))
                else:
                    # 加载失败时使用默认颜色
                    pygame.draw.rect(self.game.screen, (100, 0, 0), (self.game.width - 115, 25, 30, 30))
                    pygame.draw.rect(self.game.screen, (200, 50, 50), (self.game.width - 113, 27, 26, 26))
            except Exception as e:
                print(f"加载怪物头像失败: {e}")
                # 异常时使用默认颜色
                pygame.draw.rect(self.game.screen, (100, 0, 0), (self.game.width - 115, 25, 30, 30))
                pygame.draw.rect(self.game.screen, (200, 50, 50), (self.game.width - 113, 27, 26, 26))
            
            # 怪物名称
            monster_name = getattr(monster, 'name', '怪物')
            monster_name_text = self.small_font.render(monster_name, True, (255, 255, 255))
            self.game.screen.blit(monster_name_text, (self.game.width - 185, 75))
            
            # 怪物血条
            monster_health_ratio = getattr(monster, 'health', 0) / getattr(monster, 'max_health', 1)
            pygame.draw.rect(self.game.screen, (0, 0, 0), (self.game.width - 188, 12, 176, 10))
            pygame.draw.rect(self.game.screen, (100, 0, 0), (self.game.width - 186, 14, 172, 6))
            pygame.draw.rect(self.game.screen, (255, 0, 0), (self.game.width - 186, 14, 172 * monster_health_ratio, 6))
            
            # 怪物等级
            monster_level = getattr(monster, 'level', 1)
            level_text = self.small_font.render(f'等级: {monster_level}', True, (255, 215, 0))
            self.game.screen.blit(level_text, (self.game.width - 185, 55))
        

        
        # 下方技能栏和物品栏
        # 技能栏背景
        pygame.draw.rect(self.game.screen, (0, 0, 0), (10, self.game.height - 84, self.game.width - 20, 74))
        # 技能格子
        skills = getattr(player, 'skills', [])
        learned_skills = getattr(player, 'learned_skills', [])
        skill_cooldowns = getattr(player, 'skill_cooldowns', {})
        current_time = pygame.time.get_ticks() / 1000
        
        for i in range(10):
            skill_x = 20 + i * 60
            skill_y = self.game.height - 74
            pygame.draw.rect(self.game.screen, (100, 100, 100), (skill_x, skill_y, 50, 50))
            
            # 显示技能图标和名称
            if i < len(skills):
                skill = skills[i]
                skill_name = skill.get('name', '')
                skill_level = skill.get('level', 0)
                skill_damage = skill.get('damage', 0)
                skill_cooldown = skill.get('cooldown', 0) / 1000  # 转换为秒
                
                if skill_level > 0:
                    # 技能已学习，显示技能图标和名称
                    # 根据技能类型设置不同的颜色
                    if 'damage' in skill:
                        # 攻击技能
                        if skill.get('damage_type') == 'magic':
                            color = (0, 0, 255)  # 魔法攻击 - 蓝色
                        elif skill.get('damage_type') == 'mixed':
                            color = (255, 165, 0)  # 混合攻击 - 橙色
                        else:
                            color = (255, 0, 0)  # 物理攻击 - 红色
                    elif 'heal' in skill:
                        color = (0, 255, 0)  # 治疗技能 - 绿色
                    elif 'summon' in skill.get('name', ''):
                        color = (128, 0, 128)  # 召唤技能 - 紫色
                    else:
                        color = (128, 128, 128)  # 其他技能 - 灰色
                    
                    # 绘制技能图标（盛大传奇风格，圆形样式）
                    pygame.draw.circle(self.game.screen, (50, 50, 50), (skill_x + 25, skill_y + 25), 20)
                    pygame.draw.circle(self.game.screen, color, (skill_x + 25, skill_y + 25), 17)
                    
                    # 绘制技能等级
                    level_text = self.small_font.render(f'{skill_level}', True, (255, 255, 255))
                    self.game.screen.blit(level_text, (skill_x + 40, skill_y + 35))
                    
                    # 绘制技能名称（缩写）
                    if skill_name:
                        short_name = skill_name[:2]  # 只显示前两个字
                        name_text = self.small_font.render(short_name, True, (255, 255, 255))
                        self.game.screen.blit(name_text, (skill_x + 15, skill_y + 15))
                    
                    # 显示技能冷却时间
                    if skill_name in skill_cooldowns:
                        last_used = skill_cooldowns[skill_name]
                        elapsed = current_time - last_used
                        remaining_cooldown = max(0, skill_cooldown - elapsed)
                        if remaining_cooldown > 0:
                            # 绘制冷却时间覆盖
                            cooldown_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
                            cooldown_surface.fill((0, 0, 0, 128))
                            self.game.screen.blit(cooldown_surface, (skill_x, skill_y))
                            # 绘制冷却时间文本
                            cooldown_text = self.small_font.render(f'{int(remaining_cooldown)}s', True, (255, 255, 255))
                            cooldown_rect = cooldown_text.get_rect(center=(skill_x + 25, skill_y + 25))
                            self.game.screen.blit(cooldown_text, cooldown_rect)
                    
                    # 显示技能伤害
                    if skill_damage > 0:
                        damage_text = self.small_font.render(f'{skill_damage}', True, (255, 0, 0))
                        self.game.screen.blit(damage_text, (skill_x + 5, skill_y + 35))
                else:
                    # 技能未学习，显示灰色图标（圆形样式）
                    pygame.draw.circle(self.game.screen, (30, 30, 30), (skill_x + 25, skill_y + 25), 20)
                    pygame.draw.circle(self.game.screen, (50, 50, 50), (skill_x + 25, skill_y + 25), 17)
                    lock_text = self.small_font.render('?', True, (100, 100, 100))
                    self.game.screen.blit(lock_text, (skill_x + 20, skill_y + 18))
            else:
                # 空技能槽（圆形样式）
                pygame.draw.circle(self.game.screen, (20, 20, 20), (skill_x + 25, skill_y + 25), 20)
                pygame.draw.circle(self.game.screen, (30, 30, 30), (skill_x + 25, skill_y + 25), 17)
        
        # 物品栏
        for i in range(6):
            pygame.draw.rect(self.game.screen, (100, 100, 100), (self.game.width - 340 + i * 50, self.game.height - 74, 40, 40))
            # 物品图标（临时）
            inventory = player.item_manager.get_inventory()
            if i < len(inventory):
                item = inventory[i]
                if item.name == '金疮药':
                    pygame.draw.circle(self.game.screen, (255, 0, 0), (self.game.width - 340 + i * 50 + 20, self.game.height - 74 + 20), 15)
                elif item.name == '魔法药':
                    pygame.draw.circle(self.game.screen, (0, 0, 255), (self.game.width - 340 + i * 50 + 20, self.game.height - 74 + 20), 15)
        
        # 聊天框
        pygame.draw.rect(self.game.screen, (0, 0, 0), (10, self.game.height - 134, self.game.width - 20, 50))
        # 聊天内容（临时）
        chat_text = self.small_font.render('欢迎来到传奇世界！', True, (255, 255, 255))
        self.game.screen.blit(chat_text, (20, self.game.height - 124))
        

    
    def render_battle(self):
        """渲染战斗界面"""
        # 绘制背景
        self.game.screen.fill((50, 50, 50))
        
        # 绘制战斗信息
        # 使用预加载的大字体
        battle_text = self.large_font.render('战斗', True, (255, 255, 255))
        self.game.screen.blit(battle_text, (self.game.width // 2 - battle_text.get_width() // 2, 50))
        
        # 绘制战斗选项
        for i, option in enumerate(self.battle_options):
            color = (255, 255, 255) if i == self.selected_battle_option else (150, 150, 150)
            text = self.font.render(option, True, color)
            self.game.screen.blit(text, (self.game.width // 2 - text.get_width() // 2, 200 + i * 50))
    
    def render_shop(self):
        """渲染商店界面"""
        # 绘制背景
        self.game.screen.fill((100, 100, 100))
        
        # 绘制商店标题
        # 使用预加载的大字体
        shop_text = self.large_font.render('商店', True, (255, 215, 0))
        self.game.screen.blit(shop_text, (self.game.width // 2 - shop_text.get_width() // 2, 50))
        
        # 绘制商店物品
        for i, item in enumerate(self.current_shop_items):
            color = (255, 255, 255) if i == self.selected_shop_item else (150, 150, 150)
            item_text = self.font.render(f'{item["name"]} - {item["price"]}金币', True, color)
            self.game.screen.blit(item_text, (self.game.width // 2 - item_text.get_width() // 2, 150 + i * 40))
        
        # 绘制金币数量
        gold_text = self.font.render(f'金币: {self.game.gold}', True, (255, 215, 0))
        self.game.screen.blit(gold_text, (10, 10))
    
    def render_dialogue(self):
        """渲染对话界面"""
        # 绘制背景
        dialogue_box = pygame.Rect(50, self.game.height - 150, self.game.width - 100, 120)
        pygame.draw.rect(self.game.screen, (0, 0, 0), dialogue_box)
        pygame.draw.rect(self.game.screen, (255, 255, 255), dialogue_box, 2)
        
        # 绘制对话
        dialogue_text = self.font.render(self.current_dialogue, True, (255, 255, 255))
        self.game.screen.blit(dialogue_text, (70, self.game.height - 120))
        
        # 绘制提示
        prompt_text = self.small_font.render('按任意键继续...', True, (150, 150, 150))
        self.game.screen.blit(prompt_text, (self.game.width - 150, self.game.height - 40))
    
    def handle_menu_events(self, event):
        """处理菜单事件"""
        if event.type == pygame.KEYDOWN:
            if self.show_class_selection:
                # 处理职业选择事件
                if event.key == pygame.K_UP:
                    self.selected_class_option = (self.selected_class_option - 1) % len(self.class_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_class_option = (self.selected_class_option + 1) % len(self.class_options)
                elif event.key == pygame.K_RETURN:
                    # 选择职业
                    selected_class = self.class_options[self.selected_class_option]
                    self.game.selected_class = selected_class
                    # 初始化玩家
                    self.game.player = Player(self.game,职业=selected_class)
                    # 设置玩家名称
                    if hasattr(self, 'name_input') and self.name_input:
                        self.game.player.name = self.name_input
                    # 设置玩家引用到地图管理器
                    self.game.map_manager.set_player(self.game.player)
                    # 开始游戏
                    self.game.game_state = GameState.GAME
                    self.show_class_selection = False
                elif event.key == pygame.K_ESCAPE:
                    # 取消职业选择
                    self.show_class_selection = False
            elif self.show_load_selection:
                # 处理加载存档选择事件
                saves = self.game.data_storage.list_saves()
                if event.key == pygame.K_UP:
                    self.selected_load_slot = (self.selected_load_slot - 1) % max(len(saves), 1)
                elif event.key == pygame.K_DOWN:
                    self.selected_load_slot = (self.selected_load_slot + 1) % max(len(saves), 1)
                elif event.key == pygame.K_RETURN:
                    # 选择存档加载
                    if saves and 0 <= self.selected_load_slot < len(saves):
                        selected_save = saves[self.selected_load_slot]
                        # 先创建player对象
                        profession = selected_save.get('职业', '战士')
                        self.game.player = Player(self.game,职业=profession)
                        # 然后加载玩家数据
                        if self.game.data_storage.load_player_data(selected_save['slot']):
                            self.game.game_state = GameState.GAME
                            # 设置玩家引用到地图管理器
                            self.game.map_manager.set_player(self.game.player)
                            self.show_load_selection = False
                    else:
                        # 没有存档，返回主菜单
                        self.show_load_selection = False
                elif event.key == pygame.K_ESCAPE:
                    # 取消加载存档
                    self.show_load_selection = False
            elif self.show_save_selection:
                # 处理保存存档选择事件
                if event.key == pygame.K_UP:
                    self.selected_save_slot = (self.selected_save_slot - 1) % 3
                elif event.key == pygame.K_DOWN:
                    self.selected_save_slot = (self.selected_save_slot + 1) % 3
                elif event.key == pygame.K_RETURN:
                    # 选择存档槽位保存
                    slot = self.selected_save_slot + 1
                    if self.game.data_storage.save_player_data(slot):
                        self.show_save_selection = False
                elif event.key == pygame.K_ESCAPE:
                    # 取消保存存档
                    self.show_save_selection = False
            else:
                # 处理主菜单事件
                if event.key == pygame.K_UP:
                    # 检查是否已经在游戏中（通过检查player是否存在）
                    in_game = hasattr(self.game, 'player') and self.game.player is not None
                    if not in_game:
                        # 进游戏前的菜单，只显示3个基本选项
                        self.selected_menu_option = (self.selected_menu_option - 1) % 3
                    else:
                        # 进游戏后的菜单，显示所有选项
                        self.selected_menu_option = (self.selected_menu_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    # 检查是否已经在游戏中（通过检查player是否存在）
                    in_game = hasattr(self.game, 'player') and self.game.player is not None
                    if not in_game:
                        # 进游戏前的菜单，只显示3个基本选项
                        self.selected_menu_option = (self.selected_menu_option + 1) % 3
                    else:
                        # 进游戏后的菜单，显示所有选项
                        self.selected_menu_option = (self.selected_menu_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    # 检查是否已经在游戏中（通过检查player是否存在）
                    in_game = hasattr(self.game, 'player') and self.game.player is not None
                    
                    if not in_game:
                        # 进游戏前的菜单，只处理基本选项
                        if self.selected_menu_option == 0:
                            # 开始游戏 - 显示角色名称输入
                            self.show_name_input = True
                            self.name_input = ""
                            self.name_input_active = True
                        elif self.selected_menu_option == 1:
                            # 继续游戏
                            # 从启动菜单选择继续游戏，显示存档选择
                            self.show_load_selection = True
                            self.selected_load_slot = 0
                        elif self.selected_menu_option == 2:
                            # 退出游戏
                            self.game.running = False
                    else:
                        # 进游戏后的菜单，处理所有选项
                        if self.selected_menu_option == 0:
                            # 返回游戏
                            self.game.game_state = GameState.GAME
                        elif self.selected_menu_option == 1:
                            # 任务状态
                            print("显示任务状态和人物信息")
                            self.game.game_state = GameState.CHARACTER
                        elif self.selected_menu_option == 2:
                            # 背包装备
                            print("显示背包和装备")
                            self.game.game_state = GameState.INVENTORY
                        elif self.selected_menu_option == 3:
                            # 技能天赋
                            print("显示技能天赋")
                            self.game.game_state = GameState.SKILLS
                        elif self.selected_menu_option == 4:
                            # 保存游戏
                            print("保存游戏")
                            self.show_save_selection = True
                            self.selected_save_slot = 0
                        elif self.selected_menu_option == 5:
                            # 退出游戏
                            # 显示保存提示
                            self.show_save_prompt = True
    
    def handle_battle_events(self, event):
        """处理战斗事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_battle_option = (self.selected_battle_option - 1) % len(self.battle_options)
            elif event.key == pygame.K_DOWN:
                self.selected_battle_option = (self.selected_battle_option + 1) % len(self.battle_options)
            elif event.key == pygame.K_RETURN:
                if self.selected_battle_option == 0:
                    # 攻击
                    pass
                elif self.selected_battle_option == 1:
                    # 物品
                    pass
                elif self.selected_battle_option == 2:
                    # 防御
                    pass
                elif self.selected_battle_option == 3:
                    # 逃跑
                    self.game.game_state = GameState.GAME
    
    def handle_shop_events(self, event):
        """处理商店事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_shop_item = (self.selected_shop_item - 1) % len(self.current_shop_items)
            elif event.key == pygame.K_DOWN:
                self.selected_shop_item = (self.selected_shop_item + 1) % len(self.current_shop_items)
            elif event.key == pygame.K_RETURN:
                # 购买物品
                if self.current_shop_items:
                    item = self.current_shop_items[self.selected_shop_item]
                    if self.game.gold >= item['price']:
                        self.game.gold -= item['price']
                        self.game.player.add_item(item['name'], 1)
            elif event.key == pygame.K_ESCAPE:
                # 退出商店
                self.game.game_state = GameState.GAME
    
    def handle_dialogue_events(self, event):
        """处理对话事件"""
        if event.type == pygame.KEYDOWN:
            # 继续对话或退出
            self.game.game_state = GameState.GAME
    
    def handle_click(self, pos):
        """处理鼠标点击"""
        # 检测是否点击了技能快捷栏
        if self.handle_skill_hotkey_click(pos):
            return True
        
        # 检测是否点击了怪物
        current_map = self.game.map_manager.get_current_map()
        if current_map and hasattr(current_map, 'monsters'):
            # 转换屏幕坐标到游戏世界坐标
            world_x = pos[0] + self.game.camera_x
            world_y = pos[1] + self.game.camera_y
            
            # 检查是否点击了怪物
            for monster in current_map.monsters:
                if not monster.is_dead():
                    monster_rect = pygame.Rect(
                        monster.x - 20,
                        monster.y - 20,
                        40,
                        40
                    )
                    if monster_rect.collidepoint(world_x, world_y):
                        self.selected_monster = monster
                        return True
        
        # 暂时返回False，表示没有点击UI元素
        return False
    
    def handle_skill_hotkey_click(self, pos):
        """处理技能快捷栏点击"""
        player = self.game.player
        if not hasattr(player, 'skills'):
            return False
        
        # 检查是否点击了技能快捷栏
        for i in range(10):
            skill_x = 20 + i * 60
            skill_y = self.game.height - 74
            skill_rect = pygame.Rect(skill_x, skill_y, 50, 50)
            
            if skill_rect.collidepoint(pos):
                # 点击了技能快捷栏
                if i < len(player.skills):
                    skill = player.skills[i]
                    if skill.get('level', 0) > 0:
                        # 技能已学习，显示技能信息
                        print(f"技能: {skill['name']}, 等级: {skill['level']}, 伤害: {skill.get('damage', 0)}")
                        # 开始设置技能快捷键
                        print(f"请按数字键1-10设置{skill['name']}的快捷键")
                        self.is_setting_skill = True
                        self.selected_skill_index = i
                    else:
                        print("技能未解锁")
                else:
                    print("空技能槽")
                return True
        
        return False
    
    def start_dialogue(self, npc, dialogue):
        """开始对话"""
        self.current_dialogue = dialogue
        self.current_npc = npc
        self.game.game_state = GameState.DIALOGUE
    
    def open_shop(self, shop_items):
        """打开商店"""
        self.current_shop_items = shop_items
        self.selected_shop_item = 0
        self.game.game_state = GameState.SHOP
    
    def add_game_message(self, message, color=(255, 255, 255), duration=5000):
        """添加游戏内消息
        
        Args:
            message: 消息内容
            color: 消息颜色
            duration: 消息持续时间（毫秒）
        """
        self.game_messages.append({
            'message': message,
            'color': color,
            'duration': duration,
            'start_time': pygame.time.get_ticks()
        })
        
        # 限制消息数量
        if len(self.game_messages) > 10:
            self.game_messages.pop(0)
    
    def render_inventory(self):
        """渲染背包界面（整合装备系统）"""
        # 绘制背景
        self.game.screen.fill((50, 50, 50))
        
        # 绘制标题
        # 使用预加载的大字体
        inventory_text = self.large_font.render('背包装备', True, (255, 255, 255))
        self.game.screen.blit(inventory_text, (self.game.width // 2 - inventory_text.get_width() // 2, 50))
        
        player = self.game.player
        
        # 绘制装备栏
        equipment_width = 800
        equipment_height = 100
        equipment_x = self.game.width // 2 - equipment_width // 2
        equipment_y = 120
        
        # 装备栏背景
        pygame.draw.rect(self.game.screen, (0, 0, 0), (equipment_x, equipment_y, equipment_width, equipment_height))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (equipment_x, equipment_y, equipment_width, equipment_height), 2)
        
        # 装备栏标题
        equipment_title = self.font.render('装备栏', True, (255, 215, 0))
        self.game.screen.blit(equipment_title, (equipment_x + 10, equipment_y + 10))
        
        # 装备位置
        equipment_slots = [
            ('武器', 'weapon', equipment_x + 120, equipment_y + 40),
            ('盔甲', 'armor', equipment_x + 270, equipment_y + 40),
            ('头盔', 'helmet', equipment_x + 420, equipment_y + 40),
            ('靴子', 'boots', equipment_x + 570, equipment_y + 40)
        ]
        
        # 绘制装备槽
        for slot_name, slot_type, slot_x, slot_y in equipment_slots:
            # 装备槽背景
            pygame.draw.rect(self.game.screen, (50, 50, 50), (slot_x - 45, slot_y - 35, 90, 70))
            pygame.draw.rect(self.game.screen, (100, 100, 100), (slot_x - 45, slot_y - 35, 90, 70), 2)
            
            # 装备槽名称
            slot_text = self.small_font.render(slot_name, True, (255, 255, 255))
            self.game.screen.blit(slot_text, (slot_x - 20, slot_y - 25))
            
            # 显示当前装备
            equipped_item = player.equipment_manager.get_equipped_item(slot_type)
            if equipped_item:
                # 装备名称
                item_text = self.small_font.render(equipped_item.name, True, (0, 255, 0))
                self.game.screen.blit(item_text, (slot_x - 40, slot_y))
                
                # 装备属性
                if equipped_item.attack > 0:
                    attr_text = self.small_font.render(f'攻击+{equipped_item.attack}', True, (255, 0, 0))
                    self.game.screen.blit(attr_text, (slot_x - 40, slot_y + 20))
                if equipped_item.defense > 0:
                    attr_text = self.small_font.render(f'防御+{equipped_item.defense}', True, (0, 255, 0))
                    self.game.screen.blit(attr_text, (slot_x - 40, slot_y + 20))
            else:
                # 空装备槽
                empty_text = self.small_font.render('未装备', True, (100, 100, 100))
                self.game.screen.blit(empty_text, (slot_x - 20, slot_y))
        
        # 绘制物品栏
        inventory_width = 800
        inventory_height = 300
        inventory_x = self.game.width // 2 - inventory_width // 2
        inventory_y = 240
        
        # 物品栏背景
        pygame.draw.rect(self.game.screen, (0, 0, 0), (inventory_x, inventory_y, inventory_width, inventory_height))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (inventory_x, inventory_y, inventory_width, inventory_height), 2)
        
        # 物品栏标题
        inventory_title = self.font.render('物品栏', True, (255, 215, 0))
        self.game.screen.blit(inventory_title, (inventory_x + 10, inventory_y + 10))
        
        # 绘制物品
        items_per_row = 8
        item_width = 90
        item_height = 70
        
        inventory = player.item_manager.get_inventory()
        for i, item in enumerate(inventory):
            row = i // items_per_row
            col = i % items_per_row
            item_x = inventory_x + 10 + col * (item_width + 10)
            item_y = inventory_y + 50 + row * (item_height + 10)
            
            # 选中状态
            if i == self.selected_inventory_item:
                pygame.draw.rect(self.game.screen, (255, 215, 0), (item_x, item_y, item_width, item_height), 2)
            else:
                pygame.draw.rect(self.game.screen, (100, 100, 100), (item_x, item_y, item_width, item_height), 1)
            
            # 物品名称
            item_name = self.small_font.render(item.name, True, (255, 255, 255))
            self.game.screen.blit(item_name, (item_x + 5, item_y + 5))
            
            # 物品数量
            quantity_text = self.small_font.render(f'x{item.quantity}', True, (255, 215, 0))
            self.game.screen.blit(quantity_text, (item_x + 5, item_y + 30))
            
            # 物品属性
            if item.attack > 0:
                attack_text = self.small_font.render(f'攻击+{item.attack}', True, (255, 0, 0))
                self.game.screen.blit(attack_text, (item_x + 5, item_y + 45))
            if item.defense > 0:
                defense_text = self.small_font.render(f'防御+{item.defense}', True, (0, 255, 0))
                self.game.screen.blit(defense_text, (item_x + 60, item_y + 45))
            
            # 物品类型说明
            item_type = item.type
            type_description = {
                'weapon': '武器',
                'armor': '盔甲',
                'helmet': '头盔',
                'boots': '靴子',
                'consumable': '消耗品',
                'material': '材料'
            }.get(item_type, '材料')
            type_text = self.small_font.render(f'{type_description}', True, (200, 200, 200))
            self.game.screen.blit(type_text, (item_x + 5, item_y + 60))
        
        # 绘制选中物品的详细说明
        inventory = player.item_manager.get_inventory()
        if inventory and 0 <= self.selected_inventory_item < len(inventory):
            selected_item = inventory[self.selected_inventory_item]
            description_x = inventory_x
            description_y = inventory_y + inventory_height + 20
            description_width = inventory_width
            
            # 绘制说明背景
            pygame.draw.rect(self.game.screen, (0, 0, 0), (description_x, description_y, description_width, 60))
            pygame.draw.rect(self.game.screen, (100, 100, 100), (description_x, description_y, description_width, 60), 2)
            
            # 物品作用说明
            item_name = selected_item.name
            item_description = {
                '金疮药': '恢复30点生命值',
                '魔法药': '恢复魔法值',
                '铁剑': '攻击力+10，战士的常用武器',
                '铁甲': '防御力+5，提供良好的防护',
                '木剑': '攻击力+5，基础武器',
                '布衣': '防御力+2，基础盔甲',
                '皮帽': '防御力+1，基础头盔',
                '草鞋': '防御力+1，基础靴子',
                '骷髅骨': '任务材料，用于制作或兑换物品',
                '僵尸牙齿': '任务材料，用于制作或兑换物品',
                '狼皮': '任务材料，用于制作或兑换物品',
                '腐烂的肉': '任务材料，用于制作或兑换物品'
            }.get(item_name, selected_item.description)
            
            description_text = self.small_font.render(f'作用: {item_description}', True, (255, 255, 255))
            self.game.screen.blit(description_text, (description_x + 10, description_y + 10))
            
            # 物品类型说明
            item_type = selected_item.type
            if item_type in ['weapon', 'armor', 'helmet', 'boots']:
                equip_text = self.small_font.render('按Enter装备，按R卸下', True, (0, 255, 0))
            else:
                equip_text = self.small_font.render('按Enter使用', True, (255, 0, 0))
            self.game.screen.blit(equip_text, (description_x + 10, description_y + 35))
        
        # 绘制提示
        prompt_text = self.small_font.render('按Escape关闭背包', True, (150, 150, 150))
        self.game.screen.blit(prompt_text, (self.game.width // 2 - prompt_text.get_width() // 2, self.game.height - 50))
    
    def handle_inventory_events(self, event):
        """处理背包事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # 关闭背包
                self.game.game_state = GameState.GAME
            elif event.key == pygame.K_UP:
                self.selected_inventory_item = max(0, self.selected_inventory_item - 8)
            elif event.key == pygame.K_DOWN:
                inventory = self.game.player.item_manager.get_inventory()
                self.selected_inventory_item = min(len(inventory) - 1, self.selected_inventory_item + 8)
            elif event.key == pygame.K_LEFT:
                self.selected_inventory_item = max(0, self.selected_inventory_item - 1)
            elif event.key == pygame.K_RIGHT:
                inventory = self.game.player.item_manager.get_inventory()
                self.selected_inventory_item = min(len(inventory) - 1, self.selected_inventory_item + 1)
            elif event.key == pygame.K_RETURN:
                # 使用或装备物品
                inventory = self.game.player.item_manager.get_inventory()
                if inventory:
                    selected_item = inventory[self.selected_inventory_item]
                    if selected_item.type in ['weapon', 'armor', 'helmet', 'boots']:
                        # 装备物品
                        self.game.player.equip_item(self.selected_inventory_item)
                    else:
                        # 使用物品
                        self.game.player.use_item(self.selected_inventory_item)
            elif event.key == pygame.K_r:
                # 卸下装备
                inventory = self.game.player.item_manager.get_inventory()
                if inventory:
                    selected_item = inventory[self.selected_inventory_item]
                    if selected_item.type in ['weapon', 'armor', 'helmet', 'boots']:
                        # 卸下对应类型的装备
                        self.game.player.unequip_item(selected_item.type)
    
    def render_help(self):
        """渲染帮助界面"""
        # 绘制背景
        self.game.screen.fill((50, 50, 50))
        
        # 绘制标题
        # 使用预加载的大字体
        help_text = self.large_font.render('帮助系统', True, (255, 255, 255))
        self.game.screen.blit(help_text, (self.game.width // 2 - help_text.get_width() // 2, 50))
        
        # 绘制快捷键说明
        shortcuts = [
            ('WASD', '移动'),
            ('Space', '攻击'),
            ('E', '与NPC交互'),
            ('Tab', '打开背包'),
            ('Escape', '返回/关闭菜单'),
            ('H', '打开帮助')
        ]
        
        # 帮助内容背景
        help_width = 600
        help_height = 400
        help_x = self.game.width // 2 - help_width // 2
        help_y = 120
        
        pygame.draw.rect(self.game.screen, (0, 0, 0), (help_x, help_y, help_width, help_height))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (help_x, help_y, help_width, help_height), 2)
        
        # 绘制快捷键说明
        for i, (key, desc) in enumerate(shortcuts):
            key_text = self.font.render(key, True, (255, 215, 0))
            desc_text = self.font.render(desc, True, (255, 255, 255))
            self.game.screen.blit(key_text, (help_x + 50, help_y + 30 + i * 40))
            self.game.screen.blit(desc_text, (help_x + 200, help_y + 30 + i * 40))
        
        # 绘制其他系统说明
        system_title = self.font.render('系统说明', True, (255, 255, 255))
        self.game.screen.blit(system_title, (help_x + 50, help_y + 280))
        
        system_desc = [
            '装备系统：按Tab打开背包，选择装备物品进行装备',
            '背包系统：存放和管理物品，可以使用消耗品',
            '升级系统：击杀怪物获得经验值，达到一定值自动升级',
            'NPC交互：靠近NPC按E键可以对话或打开商店'
        ]
        
        for i, desc in enumerate(system_desc):
            desc_text = self.small_font.render(desc, True, (200, 200, 200))
            self.game.screen.blit(desc_text, (help_x + 50, help_y + 320 + i * 25))
        
        # 绘制提示
        prompt_text = self.small_font.render('按任意键关闭帮助', True, (150, 150, 150))
        self.game.screen.blit(prompt_text, (self.game.width // 2 - prompt_text.get_width() // 2, self.game.height - 50))
    
    def handle_help_events(self, event):
        """处理帮助事件"""
        if event.type == pygame.KEYDOWN:
            # 关闭帮助
            self.game.game_state = GameState.GAME
    
    def handle_character_events(self, event):
        """处理人物状态界面事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # 关闭人物状态界面
                self.game.game_state = GameState.GAME
    
    def handle_skills_events(self, event):
        """处理技能天赋界面事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # 关闭技能天赋界面
                self.game.game_state = GameState.GAME
    
    def render_character(self):
        """渲染人物状态和任务界面"""
        # 绘制背景
        self.game.screen.fill((50, 50, 50))
        
        # 绘制标题
        title = self.large_font.render('人物状态', True, (255, 215, 0))
        title_x = self.game.width // 2 - title.get_width() // 2
        title_y = 50
        self.game.screen.blit(title, (title_x, title_y))
        
        # 显示详细人物属性
        player = self.game.player
        attributes = [
            ('职业', getattr(player, '职业', '战士')),
            ('等级', self.game.level),
            ('生命值', f'{player.health}/{player.max_health}'),
            ('攻击力', player.attack),
            ('防御力', player.defense),
            ('魔法力', player.magic),
            ('基础攻击', player.base_attack),
            ('基础防御', player.base_defense),
            ('基础魔法', player.base_magic),
            ('金币', self.game.gold),
            ('经验', f'{self.game.experience}/{self.game.experience_to_next_level}')
        ]
        
        for i, (attr_name, attr_value) in enumerate(attributes):
            attr_text = self.font.render(f'{attr_name}: {attr_value}', True, (255, 255, 255))
            self.game.screen.blit(attr_text, (200, 150 + i * 40))
        
        # 显示任务状态
        quest_title = self.font.render('任务状态', True, (255, 215, 0))
        self.game.screen.blit(quest_title, (600, 150))
        
        # 显示任务列表
        quests = getattr(self.game, 'quest_system', None)
        if quests and hasattr(quests, 'active_quests'):
            for i, quest in enumerate(quests.active_quests):
                quest_text = self.small_font.render(f'{quest.name}: {quest.status}', True, (255, 255, 255))
                self.game.screen.blit(quest_text, (600, 200 + i * 30))
        else:
            no_quests_text = self.small_font.render('无活动任务', True, (150, 150, 150))
            self.game.screen.blit(no_quests_text, (600, 200))
        
        # 绘制提示
        prompt_text = self.small_font.render('按Escape关闭人物状态', True, (150, 150, 150))
        self.game.screen.blit(prompt_text, (self.game.width // 2 - prompt_text.get_width() // 2, self.game.height - 50))
    
    def render_skills(self):
        """渲染技能天赋界面"""
        # 绘制背景
        self.game.screen.fill((50, 50, 50))
        
        # 绘制标题
        title = self.large_font.render('技能天赋', True, (255, 215, 0))
        title_x = self.game.width // 2 - title.get_width() // 2
        title_y = 50
        self.game.screen.blit(title, (title_x, title_y))
        
        # 显示主动技能列表
        player = self.game.player
        skills = getattr(player, 'skills', [])
        passive_skills = getattr(player, 'passive_skills', [])
        
        # 主动技能标题
        active_title = self.font.render('主动技能', True, (0, 255, 255))
        self.game.screen.blit(active_title, (200, 100))
        
        for i, skill in enumerate(skills):
            skill_name = skill.get('name', '未知技能')
            skill_level = skill.get('level', 0)
            skill_damage = skill.get('damage', 0)
            skill_heal = skill.get('heal', 0)
            skill_range = skill.get('range', 0)
            skill_cooldown = skill.get('cooldown', 0) / 1000  # 转换为秒
            skill_description = skill.get('description', '无描述')
            skill_damage_type = skill.get('damage_type', 'attack')
            
            # 技能名称和等级
            skill_text = self.font.render(f'{skill_name} (等级 {skill_level})', True, (255, 255, 255))
            self.game.screen.blit(skill_text, (200, 150 + i * 80))
            
            # 技能详细信息
            if skill_damage > 0:
                damage_text = f'伤害: {skill_damage} ({"物理" if skill_damage_type == "attack" else "魔法" if skill_damage_type == "magic" else "混合"})'
            elif skill_heal > 0:
                damage_text = f'治疗: {skill_heal}'
            else:
                damage_text = '无伤害'
            
            info_text = self.small_font.render(f'{damage_text}, 范围: {skill_range}, 冷却: {skill_cooldown}秒', True, (200, 200, 200))
            self.game.screen.blit(info_text, (220, 180 + i * 80))
            
            # 技能描述
            desc_text = self.small_font.render(f'描述: {skill_description}', True, (150, 150, 150))
            self.game.screen.blit(desc_text, (220, 205 + i * 80))
        
        # 被动技能标题
        passive_title = self.font.render('被动技能', True, (255, 165, 0))
        self.game.screen.blit(passive_title, (600, 100))
        
        # 显示被动技能列表
        for i, passive in enumerate(passive_skills):
            passive_name = passive.get('name', '未知被动技能')
            passive_level = passive.get('level', 0)
            passive_effect = passive.get('effect', '无效果')
            passive_value = passive.get('value', 0)
            passive_description = passive.get('description', '无描述')
            
            # 被动技能名称和等级
            passive_text = self.font.render(f'{passive_name} (等级 {passive_level})', True, (255, 255, 255))
            self.game.screen.blit(passive_text, (600, 150 + i * 60))
            
            # 被动技能详细信息
            passive_info = self.small_font.render(f'效果: {passive_effect}, 值: {passive_value}', True, (200, 200, 200))
            self.game.screen.blit(passive_info, (620, 180 + i * 60))
            
            # 被动技能描述
            passive_desc = self.small_font.render(f'描述: {passive_description}', True, (150, 150, 150))
            self.game.screen.blit(passive_desc, (620, 205 + i * 60))
        
        # 绘制提示
        prompt_text = self.small_font.render('按Escape关闭技能天赋', True, (150, 150, 150))
        self.game.screen.blit(prompt_text, (self.game.width // 2 - prompt_text.get_width() // 2, self.game.height - 50))
    
    def handle_save_prompt_events(self, event):
        """处理保存提示事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_save_prompt_option = (self.selected_save_prompt_option - 1) % len(self.save_prompt_options)
            elif event.key == pygame.K_DOWN:
                self.selected_save_prompt_option = (self.selected_save_prompt_option + 1) % len(self.save_prompt_options)
            elif event.key == pygame.K_RETURN:
                if self.selected_save_prompt_option == 0:
                    # 保存并退出
                    self.game.data_storage.save_player_data(1)
                    self.game.running = False
                elif self.selected_save_prompt_option == 1:
                    # 直接退出 - 不保存
                    self.game.running = False
                elif self.selected_save_prompt_option == 2:
                    # 取消
                    self.show_save_prompt = False
    
    def handle_name_input_events(self, event):
        """处理角色名称输入事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # 确认输入
                if self.name_input:
                    # 进入职业选择
                    self.show_name_input = False
                    self.show_class_selection = True
            elif event.key == pygame.K_BACKSPACE:
                # 删除字符
                self.name_input = self.name_input[:-1]
            else:
                # 添加字符（限制长度为10）
                if len(self.name_input) < 10:
                    # 只允许输入中文、英文和数字
                    if event.unicode.isalnum() or '\u4e00' <= event.unicode <= '\u9fff':
                        self.name_input += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 点击输入框激活
            input_box = pygame.Rect(self.game.width // 2 - 150, 250, 300, 40)
            if input_box.collidepoint(event.pos):
                self.name_input_active = True
            else:
                self.name_input_active = False
    
    def add_item_drop(self, item_name, quantity, x, y):
        """添加掉落物品提示"""
        self.item_drops.append({
            'name': item_name,
            'quantity': quantity,
            'x': x,
            'y': y,
            'time': pygame.time.get_ticks(),
            'duration': 3000  # 提示持续3秒
        })
    
    def add_damage_text(self, damage, x, y, is_critical=False):
        """添加伤害值显示"""
        self.damage_texts.append({
            'damage': damage,
            'x': x,
            'y': y,
            'time': pygame.time.get_ticks(),
            'duration': 2000,  # 伤害值显示持续2秒
            'is_critical': is_critical,
            'y_offset': 0  # 向上飘动的偏移量
        })
    
    def update_item_drops(self):
        """更新掉落物品提示"""
        current_time = pygame.time.get_ticks()
        self.item_drops = [drop for drop in self.item_drops if current_time - drop['time'] < drop['duration']]
    
    def update_damage_texts(self):
        """更新伤害值显示"""
        current_time = pygame.time.get_ticks()
        # 过滤掉过期的伤害值显示
        self.damage_texts = [text for text in self.damage_texts if current_time - text['time'] < text['duration']]
        # 更新伤害值显示的位置（向上飘动效果）
        for text in self.damage_texts:
            text['y_offset'] = (current_time - text['time']) * 0.1  # 向上飘动的速度
    
    def update_game_messages(self):
        """更新游戏内消息"""
        current_time = pygame.time.get_ticks()
        # 过滤掉过期的消息
        self.game_messages = [msg for msg in self.game_messages if current_time - msg['start_time'] < msg['duration']]
    
    def render_item_drops(self):
        """渲染掉落物品提示"""
        current_time = pygame.time.get_ticks()
        for drop in self.item_drops:
            # 计算提示的位置（向上飘移动画）
            elapsed_time = current_time - drop['time']
            float_offset = min(50, elapsed_time * 0.016)  # 向上飘动50像素
            alpha = max(0, 255 - (elapsed_time * 0.085))  # 逐渐透明
            
            # 创建文本
            text = self.font.render(f"获得: {drop['name']} × {drop['quantity']}", True, (255, 215, 0))
            
            # 创建一个临时表面用于设置透明度
            temp_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
            temp_surface.fill((255, 215, 0, alpha))
            temp_surface.blit(text, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # 计算屏幕位置（考虑相机偏移）
            screen_x = drop['x'] - self.game.camera_x
            screen_y = drop['y'] - self.game.camera_y - float_offset
            
            # 渲染提示
            self.game.screen.blit(temp_surface, (screen_x, screen_y))
    
    def render_damage_texts(self):
        """渲染伤害值显示"""
        current_time = pygame.time.get_ticks()
        for damage_text in self.damage_texts:
            # 计算透明度
            elapsed_time = current_time - damage_text['time']
            alpha = max(0, 255 - (elapsed_time * 0.128))  # 逐渐透明
            
            # 根据是否为暴击选择颜色
            if damage_text['is_critical']:
                color = (255, 0, 0)  # 暴击伤害为红色
                font_size = 24
            else:
                color = (255, 255, 0)  # 普通伤害为黄色
                font_size = 20
            
            # 创建字体
            font = pygame.font.Font(None, font_size)
            text = font.render(f"-{damage_text['damage']}", True, color)
            
            # 创建一个临时表面用于设置透明度
            temp_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
            temp_surface.fill((color[0], color[1], color[2], alpha))
            temp_surface.blit(text, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # 计算屏幕位置（考虑相机偏移和向上飘动）
            screen_x = damage_text['x'] - self.game.camera_x - text.get_width() // 2
            screen_y = damage_text['y'] - self.game.camera_y - damage_text['y_offset'] - 20
            
            # 渲染伤害值
            self.game.screen.blit(temp_surface, (screen_x, screen_y))
    
    def render_game_messages(self):
        """渲染游戏内消息"""
        current_time = pygame.time.get_ticks()
        message_y = 100  # 消息显示的起始Y坐标
        line_height = 25  # 每条消息的高度
        
        for i, message in enumerate(self.game_messages):
            # 计算透明度
            elapsed_time = current_time - message['start_time']
            alpha = max(0, 255 - (elapsed_time * 0.0512))  # 逐渐透明
            
            # 创建文本
            text_surface = self.font.render(message['message'], True, message['color'])
            
            # 创建一个临时表面用于设置透明度
            temp_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            temp_surface.fill(message['color'] + (alpha,))
            temp_surface.blit(text_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # 计算屏幕位置（顶部居中显示）
            screen_x = self.game.width // 2 - text_surface.get_width() // 2
            screen_y = message_y + i * line_height
            
            # 渲染消息
            self.game.screen.blit(temp_surface, (screen_x, screen_y))
    
    def render_save_prompt(self):
        """渲染保存提示对话框"""
        # 对话框背景
        prompt_bg = pygame.Rect(300, 250, 400, 250)
        pygame.draw.rect(self.game.screen, (0, 0, 0), prompt_bg)
        pygame.draw.rect(self.game.screen, (255, 255, 255), prompt_bg, 2)
        
        # 提示标题
        title_text = self.font.render('退出游戏', True, (255, 255, 255))
        self.game.screen.blit(title_text, (450, 270))
        
        # 提示内容
        content_text = self.small_font.render('是否保存游戏进度？', True, (255, 255, 255))
        self.game.screen.blit(content_text, (350, 320))
        
        # 选项按钮
        for i, option in enumerate(self.save_prompt_options):
            button_rect = pygame.Rect(350, 360 + i * 50, 300, 40)
            if i == self.selected_save_prompt_option:
                pygame.draw.rect(self.game.screen, (100, 100, 255), button_rect)
            else:
                pygame.draw.rect(self.game.screen, (50, 50, 100), button_rect)
            pygame.draw.rect(self.game.screen, (255, 255, 255), button_rect, 2)
            
            button_text = self.font.render(option, True, (255, 255, 255))
            self.game.screen.blit(button_text, (400, 365 + i * 50))
    
    def render_name_input(self):
        """渲染角色名称输入界面"""
        # 绘制背景
        self.game.screen.fill((50, 50, 50))
        
        # 标题
        title_text = self.title_font.render('创建角色', True, (255, 255, 255))
        self.game.screen.blit(title_text, (self.game.width // 2 - title_text.get_width() // 2, 100))
        
        # 提示文字
        prompt_text = self.font.render('请输入角色名称:', True, (255, 255, 255))
        self.game.screen.blit(prompt_text, (self.game.width // 2 - prompt_text.get_width() // 2, 200))
        
        # 输入框
        input_box = pygame.Rect(self.game.width // 2 - 150, 250, 300, 40)
        pygame.draw.rect(self.game.screen, (0, 0, 0), input_box)
        pygame.draw.rect(self.game.screen, (255, 255, 255), input_box, 2)
        
        # 输入文字
        input_text = self.font.render(self.name_input, True, (255, 255, 255))
        self.game.screen.blit(input_text, (input_box.x + 10, input_box.y + 5))
        
        # 光标
        if self.name_input_active:
            cursor_x = input_box.x + 10 + input_text.get_width()
            pygame.draw.line(self.game.screen, (255, 255, 255), (cursor_x, input_box.y + 10), (cursor_x, input_box.y + 30), 2)
        
        # 提示信息
        info_text = self.small_font.render('按Enter确认，按Backspace删除，最多10个字符', True, (150, 150, 150))
        self.game.screen.blit(info_text, (self.game.width // 2 - info_text.get_width() // 2, 320))