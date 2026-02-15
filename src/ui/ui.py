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
        
        # 帮助系统
        self.help_page = 0  # 当前帮助页面
        self.help_pages = ['快捷键说明', '技能系统', '物品系统', '游戏系统']  # 帮助页面
        
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
        
        # 技能界面翻页
        self.skill_page = 0
        self.skills_per_page = 5
        
        # 仓库系统
        self.show_storage = False
        self.storage_items = []  # 公共仓库物品
        self.selected_storage_item = 0
        self.storage_capacity = 50  # 仓库容量
        
        # 商人回收功能
        self.show_recycle = False
        self.selected_recycle_item = 0
        self.recycle_prices = {}  # 物品回收价格
    
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
            max_slots = 20
            for i in range(max_slots):
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
            back_y = 250 + max_slots * 40 + 20
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
        
        # 左侧UI布局
        # 左侧第一排：快捷消耗品
        consumables_x = 20
        consumables_y = self.game.height - 150
        consumables_width = 40
        consumables_height = 40
        consumables_spacing = 10
        
        # 绘制消耗品快捷栏背景
        pygame.draw.rect(self.game.screen, (0, 0, 0), (consumables_x - 5, consumables_y - 5, 6 * (consumables_width + consumables_spacing) + 10, consumables_height + 10))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (consumables_x - 3, consumables_y - 3, 6 * (consumables_width + consumables_spacing) + 6, consumables_height + 6), 2)
        
        # 绘制快捷消耗品
        for i in range(6):
            hotkey = f'F{i+1}'
            item_index = player.item_hotkeys.get(hotkey, -1)
            
            # 绘制消耗品格子
            item_x = consumables_x + i * (consumables_width + consumables_spacing)
            pygame.draw.rect(self.game.screen, (50, 50, 50), (item_x, consumables_y, consumables_width, consumables_height))
            pygame.draw.rect(self.game.screen, (100, 100, 100), (item_x, consumables_y, consumables_width, consumables_height), 1)
            
            # 绘制快捷键标识
            hotkey_text = self.small_font.render(hotkey, True, (255, 215, 0))
            self.game.screen.blit(hotkey_text, (item_x + 2, consumables_y + 2))
            
            # 如果有物品，绘制物品信息
            if item_index >= 0 and item_index < player.item_manager.get_item_count():
                item = player.item_manager.get_item(item_index)
                if item:
                    # 绘制物品名称
                    item_name = item.name[:6]  # 截取前6个字符
                    item_text = self.small_font.render(item_name, True, (255, 255, 255))
                    self.game.screen.blit(item_text, (item_x + 2, consumables_y + 15))
                    
                    # 绘制物品数量
                    quantity_text = self.small_font.render(f'x{item.quantity}', True, (255, 215, 0))
                    self.game.screen.blit(quantity_text, (item_x + 2, consumables_y + 30))
        
        # 左侧第二行：技能快捷键
        skills_x = 20
        skills_y = self.game.height - 90
        skills_width = 40
        skills_height = 40
        skills_spacing = 10
        
        # 绘制技能快捷栏背景
        pygame.draw.rect(self.game.screen, (30, 30, 30), (skills_x - 5, skills_y - 5, 10 * (skills_width + skills_spacing) + 10, skills_height + 10))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (skills_x - 3, skills_y - 3, 10 * (skills_width + skills_spacing) + 6, skills_height + 6), 2)
        
        # 绘制技能快捷键
        for i in range(10):
            hotkey = str(i+1)
            
            # 绘制技能格子
            skill_x = skills_x + i * (skills_width + skills_spacing)
            pygame.draw.rect(self.game.screen, (50, 50, 50), (skill_x, skills_y, skills_width, skills_height))
            pygame.draw.rect(self.game.screen, (100, 100, 100), (skill_x, skills_y, skills_width, skills_height), 1)
            
            # 绘制快捷键标识
            hotkey_text = self.small_font.render(hotkey, True, (255, 215, 0))
            self.game.screen.blit(hotkey_text, (skill_x + 2, skills_y + 2))
            
            # 绘制技能信息
            if hasattr(player, 'skills') and i < len(player.skills):
                skill = player.skills[i]
                skill_level = skill.get('level', 0)
                if skill_level > 0:
                    # 绘制技能名称
                    skill_name = skill.get('name', '未知技能')[:6]  # 截取前6个字符
                    skill_text = self.small_font.render(skill_name, True, (255, 255, 255))
                    self.game.screen.blit(skill_text, (skill_x + 2, skills_y + 15))
        
        # 上方：用户状态
        status_x = 20
        status_y = 20
        status_width = 200
        status_height = 150
        
        # 绘制用户状态背景
        pygame.draw.rect(self.game.screen, (30, 30, 30), (status_x, status_y, status_width, status_height))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (status_x, status_y, status_width, status_height), 2)
        
        # 绘制玩家头像
        import os
        assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
        player_sprite_path = os.path.join(assets_path, 'sprites', 'player', 'player_down.png')
        
        try:
            # 尝试加载玩家头像
            player_avatar = pygame.image.load(player_sprite_path)
            player_avatar = pygame.transform.scale(player_avatar, (50, 50))
            self.game.screen.blit(player_avatar, (status_x + 10, status_y + 10))
        except Exception as e:
            # 如果加载失败，使用默认颜色块
            player_color = (255, 165, 0)  # 战士 - 橙色
            if getattr(player, '职业', '') == '法师':
                player_color = (0, 0, 255)  # 法师 - 蓝色
            elif getattr(player, '职业', '') == '道士':
                player_color = (0, 255, 0)  # 道士 - 绿色
            pygame.draw.rect(self.game.screen, player_color, (status_x + 10, status_y + 10, 50, 50))
        
        # 绘制玩家信息
        player_name = getattr(player, 'name', '玩家')
        name_text = self.small_font.render(player_name, True, (255, 255, 255))
        self.game.screen.blit(name_text, (status_x + 70, status_y + 15))
        
        # 绘制职业信息
        profession_text = self.small_font.render(f'职业: {player.职业}', True, (255, 255, 255))
        self.game.screen.blit(profession_text, (status_x + 70, status_y + 35))
        
        # 绘制等级信息
        level_text = self.small_font.render(f'等级: {self.game.level}', True, (255, 215, 0))
        self.game.screen.blit(level_text, (status_x + 70, status_y + 55))
        
        # 绘制血条
        health_bar_width = 180
        health_ratio = player.health / player.max_health
        pygame.draw.rect(self.game.screen, (0, 0, 0), (status_x + 10, status_y + 70, health_bar_width + 4, 14))
        pygame.draw.rect(self.game.screen, (100, 0, 0), (status_x + 12, status_y + 72, health_bar_width, 10))
        pygame.draw.rect(self.game.screen, (255, 0, 0), (status_x + 12, status_y + 72, health_bar_width * health_ratio, 10))
        health_text = self.small_font.render(f'HP: {player.health}/{player.max_health}', True, (255, 255, 255))
        self.game.screen.blit(health_text, (status_x + 10, status_y + 85))
        
        # 绘制魔法条
        magic_bar_width = 180
        magic_ratio = 0.8  # 临时值
        pygame.draw.rect(self.game.screen, (0, 0, 0), (status_x + 10, status_y + 100, magic_bar_width + 4, 14))
        pygame.draw.rect(self.game.screen, (0, 0, 100), (status_x + 12, status_y + 102, magic_bar_width, 10))
        pygame.draw.rect(self.game.screen, (0, 0, 255), (status_x + 12, status_y + 102, magic_bar_width * magic_ratio, 10))
        magic_text = self.small_font.render(f'MP: {int(magic_ratio * 100)}/100', True, (255, 255, 255))
        self.game.screen.blit(magic_text, (status_x + 10, status_y + 115))
        
        # 上方右侧：目标怪物头像
        if self.selected_monster and not self.selected_monster.is_dead():
            target_x = self.game.width - 220
            target_y = 20
            target_width = 200
            target_height = 80
            
            # 绘制目标怪物背景
            pygame.draw.rect(self.game.screen, (0, 0, 0), (target_x, target_y, target_width, target_height))
            pygame.draw.rect(self.game.screen, (100, 100, 100), (target_x, target_y, target_width, target_height), 2)
            
            # 绘制怪物头像
            import os
            assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
            
            # 根据怪物名称选择对应的图片文件
            monster_name = self.selected_monster.name
            monster_image_map = {
                '稻草人': '稻草人.png',
                '鸡': '鸡.png',
                '鹿': '鹿.png',
                '狼': '狼.png',
                '骷髅': '骷髅.png',
                '僵尸': '僵尸.png',
                '骷髅王': '骷髅王.png',
                '僵尸王': '僵尸王.png',
                '沃玛教主': '沃玛教主.png',
                '祖玛教主': '祖玛教主.png'
            }
            
            monster_image_file = monster_image_map.get(monster_name, '稻草人.png')
            monster_sprite_path = os.path.join(assets_path, 'sprites', 'monster', monster_image_file)
            
            try:
                # 尝试加载怪物头像
                monster_avatar = pygame.image.load(monster_sprite_path)
                monster_avatar = pygame.transform.scale(monster_avatar, (60, 60))
                self.game.screen.blit(monster_avatar, (target_x + 10, target_y + 10))
            except Exception as e:
                # 如果加载失败，使用默认颜色块
                monster_color = (255, 0, 0)
                pygame.draw.rect(self.game.screen, monster_color, (target_x + 10, target_y + 10, 60, 60))
            
            # 绘制怪物信息
            monster_name = self.selected_monster.name
            name_text = self.small_font.render(f'目标: {monster_name}', True, (255, 255, 255))
            self.game.screen.blit(name_text, (target_x + 80, target_y + 15))
            
            # 绘制怪物血条
            health_ratio = self.selected_monster.health / self.selected_monster.max_health
            health_bar_width = 100
            pygame.draw.rect(self.game.screen, (0, 0, 0), (target_x + 80, target_y + 40, health_bar_width + 4, 14))
            pygame.draw.rect(self.game.screen, (100, 0, 0), (target_x + 82, target_y + 42, health_bar_width, 10))
            pygame.draw.rect(self.game.screen, (255, 0, 0), (target_x + 82, target_y + 42, health_bar_width * health_ratio, 10))
            health_text = self.small_font.render(f'HP: {self.selected_monster.health}/{self.selected_monster.max_health}', True, (255, 255, 255))
            self.game.screen.blit(health_text, (target_x + 80, target_y + 60))
        
        # 上方右侧：小地图
        minimap_x = self.game.width - 220
        minimap_y = 120
        minimap_width = 200
        minimap_height = 150
        
        # 根据当前地图类型设置小地图背景色
        current_map = self.game.map_manager.get_current_map()
        map_background_color = (0, 0, 0)
        if current_map:
            map_type = getattr(current_map, 'scene_type', '森林')
            # 根据地图类型设置背景色
            if map_type == '森林':
                map_background_color = (0, 50, 0)  # 深绿色
            elif map_type == '沙漠':
                map_background_color = (139, 69, 19)  # 沙棕色
            elif map_type == '地牢':
                map_background_color = (30, 30, 30)  # 深灰色
            elif map_type == '雪原':
                map_background_color = (200, 200, 255)  # 浅蓝色
            elif map_type == '村庄':
                map_background_color = (80, 140, 90)  # 村庄绿色
            else:
                map_background_color = (80, 140, 90)  # 默认绿色
        
        # 绘制小地图背景
        pygame.draw.rect(self.game.screen, map_background_color, (minimap_x, minimap_y, minimap_width, minimap_height))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (minimap_x, minimap_y, minimap_width, minimap_height), 2)
        
        # 绘制小地图标题
        minimap_title = self.font.render('小地图', True, (255, 215, 0))
        self.game.screen.blit(minimap_title, (minimap_x + 10, minimap_y + 5))
        
        # 绘制小地图内容
        if hasattr(self.game, 'map_manager') and hasattr(self.game.map_manager, 'get_current_map'):
            current_map = self.game.map_manager.get_current_map()
            if current_map:
                # 绘制玩家位置
                player_x = minimap_x + minimap_width // 2
                player_y = minimap_y + minimap_height // 2
                pygame.draw.circle(self.game.screen, (255, 255, 0), (player_x, player_y), 5)
                
                # 绘制怪物位置
                if hasattr(current_map, 'monsters'):
                    for monster in current_map.monsters:
                        if not monster.is_dead():
                            # 计算怪物在小地图上的位置
                            monster_x = minimap_x + minimap_width // 2 + (monster.x - player.x) * 0.05
                            monster_y = minimap_y + minimap_height // 2 + (monster.y - player.y) * 0.05
                            
                            # 确保怪物在小地图范围内
                            if minimap_x < monster_x < minimap_x + minimap_width and minimap_y < monster_y < minimap_y + minimap_height:
                                # 根据怪物ID判断类型
                                from src.core.id_manager import id_manager
                                monster_id = id_manager.get_monster_id_by_name(monster.name)
                                is_boss = False
                                if monster_id:
                                    monster_info = id_manager.get_monster_by_id(monster_id)
                                    if monster_info and monster_info.get('type') == 'boss':
                                        is_boss = True
                                # 同时保留名称判断作为备份
                                elif 'Boss' in monster.name or '王' in monster.name or '教主' in monster.name:
                                    is_boss = True
                                
                                if is_boss:
                                    # Boss怪物突出显示
                                    monster_color = (255, 0, 0)
                                    # 绘制Boss外圈
                                    pygame.draw.circle(self.game.screen, (255, 255, 0), (int(monster_x), int(monster_y)), 6, 2)
                                    # 绘制Boss内圈
                                    pygame.draw.circle(self.game.screen, monster_color, (int(monster_x), int(monster_y)), 4)
                                    # 绘制Boss特殊标识（闪烁效果）
                                    pygame.draw.circle(self.game.screen, (255, 215, 0), (int(monster_x), int(monster_y)), 8, 1)
                                else:
                                    monster_color = (0, 255, 0)
                                    pygame.draw.circle(self.game.screen, monster_color, (int(monster_x), int(monster_y)), 3)
                
                # 绘制NPC位置
                if hasattr(current_map, 'npcs'):
                    for npc in current_map.npcs:
                        # 计算NPC在小地图上的位置
                        npc_x = minimap_x + minimap_width // 2 + (npc.x - player.x) * 0.05
                        npc_y = minimap_y + minimap_height // 2 + (npc.y - player.y) * 0.05
                        
                        # 确保NPC在小地图范围内
                        if minimap_x < npc_x < minimap_x + minimap_width and minimap_y < npc_y < minimap_y + minimap_height:
                            pygame.draw.circle(self.game.screen, (0, 0, 255), (int(npc_x), int(npc_y)), 3)
                
                # 绘制传送点位置
                if hasattr(current_map, 'exits'):
                    for exit in current_map.exits:
                        # 计算传送点中心点
                        exit_center_x = exit['x'] + exit.get('width', 50) // 2
                        exit_center_y = exit['y'] + exit.get('height', 50) // 2
                        
                        # 计算传送点在小地图上的位置
                        exit_x = minimap_x + minimap_width // 2 + (exit_center_x - player.x) * 0.05
                        exit_y = minimap_y + minimap_height // 2 + (exit_center_y - player.y) * 0.05
                        
                        # 确保传送点在小地图范围内
                        if minimap_x - 10 < exit_x < minimap_x + minimap_width + 10 and minimap_y - 10 < exit_y < minimap_y + minimap_height + 10:
                            # 传送点突出显示
                            # 绘制外圈
                            pygame.draw.circle(self.game.screen, (255, 255, 0), (int(exit_x), int(exit_y)), 6, 2)
                            # 绘制内圈
                            pygame.draw.circle(self.game.screen, (255, 215, 0), (int(exit_x), int(exit_y)), 4)
                            # 绘制中心点
                            pygame.draw.circle(self.game.screen, (255, 255, 255), (int(exit_x), int(exit_y)), 2)
        
        # 右下角：系统按钮和聊天框
        # 右下角：系统按钮
        buttons_x = self.game.width - 200
        buttons_y = self.game.height - 300
        buttons_width = 180
        buttons_height = 30
        buttons_spacing = 5
        
        # 绘制系统按钮背景
        pygame.draw.rect(self.game.screen, (0, 0, 0), (buttons_x, buttons_y, buttons_width, 4 * (buttons_height + buttons_spacing)))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (buttons_x, buttons_y, buttons_width, 4 * (buttons_height + buttons_spacing)), 2)
        
        # 系统按钮列表
        system_buttons = [
            ('用户状态', 'status'),
            ('背包装备', 'inventory'),
            ('技能天赋', 'skills'),
            ('任务状态', 'quests')
        ]
        
        # 绘制系统按钮
        for i, (text, action) in enumerate(system_buttons):
            button_y = buttons_y + i * (buttons_height + buttons_spacing)
            # 绘制按钮背景
            pygame.draw.rect(self.game.screen, (50, 50, 50), (buttons_x, button_y, buttons_width, buttons_height))
            pygame.draw.rect(self.game.screen, (100, 100, 100), (buttons_x, button_y, buttons_width, buttons_height), 1)
            # 绘制按钮文本
            button_text = self.small_font.render(text, True, (255, 255, 255))
            text_x = buttons_x + (buttons_width - button_text.get_width()) // 2
            text_y = button_y + (buttons_height - button_text.get_height()) // 2
            self.game.screen.blit(button_text, (text_x, text_y))
        
        # 右下角：聊天框
        chat_x = self.game.width - 350
        chat_y = self.game.height - 200
        chat_width = 330
        chat_height = 180
        
        # 绘制聊天框背景
        pygame.draw.rect(self.game.screen, (255, 255, 255), (chat_x, chat_y, chat_width, chat_height))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (chat_x, chat_y, chat_width, chat_height), 2)
        
        # 绘制聊天框标题
        chat_title = self.font.render('聊天记录', True, (255, 215, 0))
        self.game.screen.blit(chat_title, (chat_x + 10, chat_y + 5))
        
        # 绘制聊天内容
        chat_content_y = chat_y + 30
        chat_line_height = 20
        
        # 显示游戏内消息和击杀记录
        for i, message in enumerate(self.game_messages[-8:]):  # 显示最近8条消息
            text = message.get('message', '')
            color = message.get('color', (255, 255, 255))
            message_text = self.small_font.render(text, True, color)
            self.game.screen.blit(message_text, (chat_x + 10, chat_content_y + i * chat_line_height))
        
        # 绘制金币和经验信息
        gold_text = self.small_font.render(f'金币: {self.game.gold}', True, (255, 215, 0))
        self.game.screen.blit(gold_text, (chat_x + 10, chat_y + chat_height - 40))
        
        exp_ratio = self.game.experience / self.game.experience_to_next_level
        exp_text = self.small_font.render(f'经验: {self.game.experience}/{self.game.experience_to_next_level}', True, (255, 255, 255))
        self.game.screen.blit(exp_text, (chat_x + 10, chat_y + chat_height - 20))
        
        # 绘制经验条
        exp_bar_width = 260
        pygame.draw.rect(self.game.screen, (0, 0, 0), (chat_x + 10, chat_y + chat_height - 15, exp_bar_width + 4, 10))
        pygame.draw.rect(self.game.screen, (100, 100, 0), (chat_x + 12, chat_y + chat_height - 13, exp_bar_width, 6))
        pygame.draw.rect(self.game.screen, (255, 215, 0), (chat_x + 12, chat_y + chat_height - 13, exp_bar_width * exp_ratio, 6))

        

        

        

    
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
                max_slots = 20
                if event.key == pygame.K_UP:
                    self.selected_save_slot = (self.selected_save_slot - 1) % max_slots
                elif event.key == pygame.K_DOWN:
                    self.selected_save_slot = (self.selected_save_slot + 1) % max_slots
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
    
    def handle_hover(self, pos):
        """处理鼠标悬停"""
        # 检测是否悬停在技能快捷栏上
        player = self.game.player
        if hasattr(player, 'skills'):
            skills = player.skills
            for i in range(6):
                skill_x = 20 + i * (40 + 10)
                skill_y = self.game.height - 90
                skill_rect = pygame.Rect(skill_x, skill_y, 40, 40)
                
                if skill_rect.collidepoint(pos):
                    if i < len(skills):
                        return skills[i]
        
        # 检测是否悬停在物品快捷栏上
        if hasattr(player, 'item_hotkeys'):
            for i in range(6):
                hotkey = f'F{i+1}'
                item_index = player.item_hotkeys.get(hotkey, -1)
                
                item_x = 20 + i * (40 + 10)
                item_y = self.game.height - 150
                item_rect = pygame.Rect(item_x, item_y, 40, 40)
                
                if item_rect.collidepoint(pos):
                    if item_index >= 0 and item_index < player.item_manager.get_item_count():
                        item = player.item_manager.get_item(item_index)
                        if item:
                            return item
        return None
    
    def handle_click(self, pos):
        """处理鼠标点击"""
        # 检测是否点击了系统按钮
        if self.handle_system_button_click(pos):
            return True
        
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
    
    def handle_system_button_click(self, pos):
        """处理系统按钮点击"""
        # 系统按钮位置
        buttons_x = self.game.width - 200
        buttons_y = self.game.height - 300
        buttons_width = 180
        buttons_height = 30
        buttons_spacing = 5
        
        # 系统按钮列表
        system_buttons = [
            ('用户状态', 'status'),
            ('背包装备', 'inventory'),
            ('技能天赋', 'skills'),
            ('任务状态', 'quests')
        ]
        
        # 检测是否点击了系统按钮
        for i, (text, action) in enumerate(system_buttons):
            button_y = buttons_y + i * (buttons_height + buttons_spacing)
            button_rect = pygame.Rect(buttons_x, button_y, buttons_width, buttons_height)
            
            if button_rect.collidepoint(pos):
                # 跳转到对应的系统界面
                if action == 'status':
                    self.game.game_state = GameState.CHARACTER
                elif action == 'inventory':
                    self.game.game_state = GameState.INVENTORY
                elif action == 'skills':
                    self.game.game_state = GameState.SKILLS
                elif action == 'quests':
                    self.game.game_state = GameState.CHARACTER
                return True
        
        return False
    
    def handle_skill_hotkey_click(self, pos):
        """处理技能快捷栏点击"""
        try:
            player = self.game.player
            if not hasattr(player, 'skills'):
                return False
            
            # 检查是否点击了技能快捷栏
            for i in range(6):  # 只检查6个技能槽
                skill_x = 20 + i * (40 + 10)
                skill_y = self.game.height - 90
                skill_rect = pygame.Rect(skill_x, skill_y, 40, 40)
                
                if skill_rect.collidepoint(pos):
                    # 点击了技能快捷栏
                    if i < len(player.skills):
                        skill = player.skills[i]
                        skill_level = skill.get('level', 0)
                        if skill_level > 0:
                            # 技能已学习，显示技能信息
                            print(f"技能: {skill['name']}, 等级: {skill_level}, 伤害: {skill.get('damage', 0)}")
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
        except Exception as e:
            print(f"处理技能快捷栏点击错误: {e}")
            import traceback
            traceback.print_exc()
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
            
            # 显示物品快捷键
            if hasattr(self.game.player, 'hotkey_items') and i in self.game.player.hotkey_items:
                hotkey = self.game.player.hotkey_items[i]
                hotkey_text = self.small_font.render(f'快捷键: {hotkey}', True, (255, 215, 0))
                self.game.screen.blit(hotkey_text, (item_x + 5, item_y + 75))
        
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
            elif event.key in [pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6]:
                # 设置物品快捷键（F1-F6）
                hotkey = f'F{event.key - pygame.K_F1 + 1}'
                self.game.player.set_item_hotkey(self.selected_inventory_item, hotkey)
    
    def render_help(self):
        """渲染帮助界面"""
        # 绘制背景
        self.game.screen.fill((50, 50, 50))
        
        # 绘制标题
        # 使用预加载的大字体
        help_text = self.large_font.render('帮助系统', True, (255, 255, 255))
        self.game.screen.blit(help_text, (self.game.width // 2 - help_text.get_width() // 2, 50))
        
        # 绘制当前页面标题
        page_title = self.font.render(f'[{self.help_pages[self.help_page]}]', True, (255, 215, 0))
        self.game.screen.blit(page_title, (self.game.width // 2 - page_title.get_width() // 2, 100))
        
        # 帮助内容背景
        help_width = 600
        help_height = 400
        help_x = self.game.width // 2 - help_width // 2
        help_y = 150
        
        pygame.draw.rect(self.game.screen, (0, 0, 0), (help_x, help_y, help_width, help_height))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (help_x, help_y, help_width, help_height), 2)
        
        # 根据当前页面显示不同内容
        if self.help_page == 0:
            # 页面0：快捷键说明
            shortcuts = [
                ('WASD', '移动'),
                ('Space', '攻击'),
                ('E', '与NPC交互'),
                ('Tab', '打开背包'),
                ('Escape', '返回/关闭菜单'),
                ('H', '打开帮助'),
                ('F1-F6', '使用物品快捷键'),
                ('1-6', '使用技能快捷键')
            ]
            
            # 绘制快捷键说明
            for i, (key, desc) in enumerate(shortcuts):
                key_text = self.font.render(key, True, (255, 215, 0))
                desc_text = self.font.render(desc, True, (255, 255, 255))
                self.game.screen.blit(key_text, (help_x + 50, help_y + 30 + i * 40))
                self.game.screen.blit(desc_text, (help_x + 200, help_y + 30 + i * 40))
        elif self.help_page == 1:
            # 页面1：技能系统
            skill_desc = [
                '技能系统：按F10打开技能界面',
                '技能等级要求：每个技能都有等级要求',
                '技能冷却时间：技能使用后会进入冷却',
                '技能快捷键：在技能界面点击技能，按数字键1-6设置快捷键',
                '技能翻页：在技能界面使用左右箭头键翻页',
                '技能伤害：技能伤害与等级和属性相关',
                '技能范围：不同技能有不同的攻击范围',
                '技能类型：包括攻击、防御、辅助等类型'
            ]
            
            for i, desc in enumerate(skill_desc):
                desc_text = self.font.render(desc, True, (255, 255, 255))
                self.game.screen.blit(desc_text, (help_x + 50, help_y + 30 + i * 40))
        elif self.help_page == 2:
            # 页面2：物品系统
            item_desc = [
                '物品系统：按Tab打开背包界面',
                '消耗品：包括金疮药、魔法药等恢复物品',
                '装备：包括武器、盔甲、头盔、靴子',
                '材料：用于任务或制作的物品',
                '技能书：学习新技能的物品',
                '物品快捷键：在背包界面选择物品，按F1-F6设置',
                '物品使用：按Enter键使用物品或装备',
                '物品掉落：怪物死亡后会掉落物品'
            ]
            
            for i, desc in enumerate(item_desc):
                desc_text = self.font.render(desc, True, (255, 255, 255))
                self.game.screen.blit(desc_text, (help_x + 50, help_y + 30 + i * 40))
        elif self.help_page == 3:
            # 页面3：游戏系统
            game_desc = [
                '装备系统：按Tab打开背包，选择装备物品进行装备',
                '背包系统：存放和管理物品，可以使用消耗品',
                '升级系统：击杀怪物获得经验值，达到一定值自动升级',
                'NPC交互：靠近NPC按E键可以对话或打开商店',
                '任务系统：接受并完成NPC给予的任务',
                '战斗系统：与怪物战斗，使用技能和物品',
                '保存系统：可以保存游戏进度到不同槽位',
                '聊天系统：显示游戏中的各种消息和击杀记录'
            ]
            
            for i, desc in enumerate(game_desc):
                desc_text = self.font.render(desc, True, (255, 255, 255))
                self.game.screen.blit(desc_text, (help_x + 50, help_y + 30 + i * 40))
        
        # 绘制页面导航提示
        nav_text = self.small_font.render('← 左箭头键 切换页面 → 右箭头键', True, (150, 150, 150))
        self.game.screen.blit(nav_text, (self.game.width // 2 - nav_text.get_width() // 2, help_y + help_height + 20))
        
        # 绘制提示
        prompt_text = self.small_font.render('按任意键关闭帮助', True, (150, 150, 150))
        self.game.screen.blit(prompt_text, (self.game.width // 2 - prompt_text.get_width() // 2, self.game.height - 50))
    
    def handle_help_events(self, event):
        """处理帮助事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # 上一页
                self.help_page = max(0, self.help_page - 1)
            elif event.key == pygame.K_RIGHT:
                # 下一页
                self.help_page = min(len(self.help_pages) - 1, self.help_page + 1)
            else:
                # 关闭帮助
                self.game.game_state = GameState.GAME
    
    def handle_skills_events(self, event):
        """处理技能天赋界面事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # 关闭技能天赋界面
                self.game.game_state = GameState.GAME
            elif event.key == pygame.K_LEFT:
                # 上一页
                if hasattr(self, 'skill_page'):
                    self.skill_page = max(0, self.skill_page - 1)
            elif event.key == pygame.K_RIGHT:
                # 下一页
                player = self.game.player
                skills = getattr(player, 'skills', [])
                skills_per_page = getattr(self, 'skills_per_page', 5)
                max_page = max(0, (len(skills) - 1) // skills_per_page)
                if hasattr(self, 'skill_page'):
                    self.skill_page = min(max_page, self.skill_page + 1)
    
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
        """渲染技能天赋界面 - 参考物品栏设计"""
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
        
        # 计算分页
        skills_per_page = getattr(self, 'skills_per_page', 4)
        if not hasattr(self, 'skill_page'):
            self.skill_page = 0
        total_pages = max(1, (len(skills) + skills_per_page - 1) // skills_per_page)
        start_index = self.skill_page * skills_per_page
        end_index = start_index + skills_per_page
        page_skills = skills[start_index:end_index]
        
        # 主动技能区域
        active_area_x = 100
        active_area_y = 100
        active_area_width = 500
        active_area_height = 400
        
        # 绘制主动技能区域背景
        pygame.draw.rect(self.game.screen, (0, 0, 0), (active_area_x, active_area_y, active_area_width, active_area_height))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (active_area_x, active_area_y, active_area_width, active_area_height), 2)
        
        # 主动技能标题
        active_title = self.font.render('主动技能', True, (0, 255, 255))
        self.game.screen.blit(active_title, (active_area_x + 20, active_area_y + 10))
        
        # 显示分页信息
        page_info = self.font.render(f'页 {self.skill_page + 1}/{total_pages}', True, (255, 255, 255))
        self.game.screen.blit(page_info, (active_area_x + active_area_width - page_info.get_width() - 20, active_area_y + 10))
        
        # 技能列表
        for i, skill in enumerate(page_skills):
            try:
                skill_name = skill.get('name', '未知技能')
                skill_level = skill.get('level', 0)
                skill_damage = skill.get('damage', 0)
                skill_heal = skill.get('heal', 0)
                skill_range = skill.get('range', 0)
                skill_cooldown = skill.get('cooldown', 0) / 1000  # 转换为秒
                skill_description = skill.get('description', '无描述')
                skill_damage_type = skill.get('damage_type', 'attack')
                skill_required_level = skill.get('required_level', 1)
                
                # 技能槽位置
                skill_slot_y = active_area_y + 50 + i * 90
                
                # 绘制技能槽背景
                pygame.draw.rect(self.game.screen, (30, 30, 30), (active_area_x + 20, skill_slot_y, active_area_width - 40, 80))
                pygame.draw.rect(self.game.screen, (100, 100, 100), (active_area_x + 20, skill_slot_y, active_area_width - 40, 80), 2)
                
                # 技能名称和等级
                skill_text = self.font.render(f'{skill_name} (等级 {skill_level})', True, (255, 215, 0))
                self.game.screen.blit(skill_text, (active_area_x + 30, skill_slot_y + 10))
                
                # 技能详细信息
                if skill_damage > 0:
                    damage_type_text = '物理' if skill_damage_type == 'attack' else '魔法' if skill_damage_type == 'magic' else '混合'
                    damage_text = f'伤害: {skill_damage} ({damage_type_text})'
                elif skill_heal > 0:
                    damage_text = f'治疗: {skill_heal}'
                else:
                    damage_text = '无伤害'
                
                info_text = self.small_font.render(f'{damage_text}', True, (255, 255, 255))
                self.game.screen.blit(info_text, (active_area_x + 30, skill_slot_y + 35))
                
                # 技能其他信息
                other_info = self.small_font.render(f'范围: {skill_range}, 冷却: {skill_cooldown}秒', True, (200, 200, 200))
                self.game.screen.blit(other_info, (active_area_x + 30, skill_slot_y + 55))
                
                # 技能等级要求
                required_level_text = self.small_font.render(f'等级要求: {skill_required_level}', True, (0, 255, 255))
                self.game.screen.blit(required_level_text, (active_area_x + 300, skill_slot_y + 10))
                
                # 技能描述
                desc_text = self.small_font.render(f'描述: {skill_description}', True, (150, 150, 150))
                self.game.screen.blit(desc_text, (active_area_x + 300, skill_slot_y + 35))
            except Exception as e:
                print(f"渲染技能 {i} 错误: {e}")
        
        # 被动技能区域
        passive_area_x = self.game.width - 600
        passive_area_y = 100
        passive_area_width = 500
        passive_area_height = 400
        
        # 绘制被动技能区域背景
        pygame.draw.rect(self.game.screen, (0, 0, 0), (passive_area_x, passive_area_y, passive_area_width, passive_area_height))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (passive_area_x, passive_area_y, passive_area_width, passive_area_height), 2)
        
        # 被动技能标题
        passive_title = self.font.render('被动技能', True, (255, 165, 0))
        self.game.screen.blit(passive_title, (passive_area_x + 20, passive_area_y + 10))
        
        # 显示被动技能列表
        for i, passive in enumerate(passive_skills):
            try:
                passive_name = passive.get('name', '未知被动技能')
                passive_level = passive.get('level', 0)
                passive_effect = passive.get('effect', '无效果')
                passive_value = passive.get('value', 0)
                passive_description = passive.get('description', '无描述')
                
                # 被动技能槽位置
                passive_slot_y = passive_area_y + 50 + i * 70
                
                # 绘制被动技能槽背景
                pygame.draw.rect(self.game.screen, (30, 30, 30), (passive_area_x + 20, passive_slot_y, passive_area_width - 40, 60))
                pygame.draw.rect(self.game.screen, (100, 100, 100), (passive_area_x + 20, passive_slot_y, passive_area_width - 40, 60), 2)
                
                # 被动技能名称和等级
                passive_text = self.font.render(f'{passive_name} (等级 {passive_level})', True, (255, 255, 255))
                self.game.screen.blit(passive_text, (passive_area_x + 30, passive_slot_y + 10))
                
                # 被动技能详细信息
                passive_info = self.small_font.render(f'效果: {passive_effect}, 值: {passive_value}', True, (200, 200, 200))
                self.game.screen.blit(passive_info, (passive_area_x + 30, passive_slot_y + 35))
            except Exception as e:
                print(f"渲染被动技能 {i} 错误: {e}")
        
        # 绘制提示
        prompt_text = self.small_font.render('按Escape关闭技能天赋 | 按左右箭头键翻页', True, (150, 150, 150))
        self.game.screen.blit(prompt_text, (self.game.width // 2 - prompt_text.get_width() // 2, self.game.height - 50))
        
        # 绘制技能设置提示
        setup_prompt = self.small_font.render('提示: 点击游戏中的技能快捷栏可以设置技能快捷键', True, (100, 200, 100))
        self.game.screen.blit(setup_prompt, (self.game.width // 2 - setup_prompt.get_width() // 2, self.game.height - 25))
    
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

    def handle_character_events(self, event):
        """处理人物状态界面事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # 退出人物状态界面
                self.game.game_state = GameState.GAME

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
            
            # 根据是否为暴击选择颜色和字体大小
            if damage_text['is_critical']:
                color = (255, 215, 0)  # 暴击伤害为金色
                font_size = 28
                # 暴击伤害添加感叹号
                display_text = f"-{damage_text['damage']}!!!"
            else:
                color = (255, 255, 0)  # 普通伤害为黄色
                font_size = 20
                display_text = f"-{damage_text['damage']}"
            
            # 创建字体
            font = pygame.font.Font(None, font_size)
            text = font.render(display_text, True, color)
            
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
    
    def render_storage(self):
        """渲染仓库界面"""
        # 绘制背景
        self.game.screen.fill((50, 50, 50))
        
        # 绘制仓库标题
        storage_text = self.large_font.render('公共仓库', True, (255, 215, 0))
        self.game.screen.blit(storage_text, (self.game.width // 2 - storage_text.get_width() // 2, 50))
        
        # 绘制仓库物品
        storage_width = 800
        storage_height = 400
        storage_x = self.game.width // 2 - storage_width // 2
        storage_y = 120
        
        # 仓库背景
        pygame.draw.rect(self.game.screen, (0, 0, 0), (storage_x, storage_y, storage_width, storage_height))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (storage_x, storage_y, storage_width, storage_height), 2)
        
        # 仓库标题
        storage_title = self.font.render('仓库物品', True, (255, 215, 0))
        self.game.screen.blit(storage_title, (storage_x + 10, storage_y + 10))
        
        # 绘制物品
        items_per_row = 8
        item_width = 90
        item_height = 70
        
        for i, item in enumerate(self.storage_items):
            row = i // items_per_row
            col = i % items_per_row
            item_x = storage_x + 10 + col * (item_width + 10)
            item_y = storage_y + 50 + row * (item_height + 10)
            
            # 选中状态
            if i == self.selected_storage_item:
                pygame.draw.rect(self.game.screen, (255, 215, 0), (item_x, item_y, item_width, item_height), 2)
            else:
                pygame.draw.rect(self.game.screen, (100, 100, 100), (item_x, item_y, item_width, item_height), 1)
            
            # 物品名称
            item_name = self.small_font.render(item['name'], True, (255, 255, 255))
            self.game.screen.blit(item_name, (item_x + 5, item_y + 5))
            
            # 物品数量
            quantity_text = self.small_font.render(f'x{item.get("quantity", 1)}', True, (255, 215, 0))
            self.game.screen.blit(quantity_text, (item_x + 5, item_y + 30))
        
        # 绘制背包物品
        inventory_width = 800
        inventory_height = 200
        inventory_x = self.game.width // 2 - inventory_width // 2
        inventory_y = storage_y + storage_height + 20
        
        # 背包背景
        pygame.draw.rect(self.game.screen, (0, 0, 0), (inventory_x, inventory_y, inventory_width, inventory_height))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (inventory_x, inventory_y, inventory_width, inventory_height), 2)
        
        # 背包标题
        inventory_title = self.font.render('背包物品', True, (255, 215, 0))
        self.game.screen.blit(inventory_title, (inventory_x + 10, inventory_y + 10))
        
        # 确保selected_inventory_item属性存在
        if not hasattr(self, 'selected_inventory_item'):
            self.selected_inventory_item = 0
        
        # 绘制背包物品
        player = self.game.player
        inventory = player.item_manager.get_inventory()
        items_per_row_inventory = 8
        
        for i, item in enumerate(inventory):
            row = i // items_per_row_inventory
            col = i % items_per_row_inventory
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
        
        # 确保选择模式存在
        if not hasattr(self, 'storage_selection_mode'):
            self.storage_selection_mode = 'storage'
        
        # 绘制提示
        current_mode = '仓库' if self.storage_selection_mode == 'storage' else '背包'
        mode_text = self.small_font.render(f'当前模式: {current_mode}', True, (255, 215, 0))
        prompt_text1 = self.small_font.render('操作: 方向键选择物品 | Enter操作 | Tab切换模式 | Escape关闭', True, (150, 150, 150))
        prompt_text2 = self.small_font.render('仓库模式: 取出物品到背包 | 背包模式: 存入物品到仓库', True, (150, 150, 150))
        
        self.game.screen.blit(mode_text, (self.game.width // 2 - mode_text.get_width() // 2, self.game.height - 90))
        self.game.screen.blit(prompt_text1, (self.game.width // 2 - prompt_text1.get_width() // 2, self.game.height - 60))
        self.game.screen.blit(prompt_text2, (self.game.width // 2 - prompt_text2.get_width() // 2, self.game.height - 30))
    
    def handle_storage_events(self, event):
        """处理仓库事件"""
        # 确保选择模式和选中索引存在
        if not hasattr(self, 'storage_selection_mode'):
            self.storage_selection_mode = 'storage'  # 'storage' 或 'inventory'
        if not hasattr(self, 'selected_storage_item'):
            self.selected_storage_item = 0
        if not hasattr(self, 'selected_inventory_item'):
            self.selected_inventory_item = 0
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # 关闭仓库，保存数据
                if hasattr(self.game, 'data_storage'):
                    self.game.data_storage.save_storage_data(self.storage_items)
                self.show_storage = False
                self.game.game_state = GameState.GAME
            elif event.key == pygame.K_TAB:
                # 切换选择模式：仓库物品 <-> 背包物品
                if self.storage_selection_mode == 'storage':
                    self.storage_selection_mode = 'inventory'
                else:
                    self.storage_selection_mode = 'storage'
            elif event.key == pygame.K_UP:
                # 上键：选择当前模式的物品
                if self.storage_selection_mode == 'storage':
                    self.selected_storage_item = max(0, self.selected_storage_item - 8)
                else:
                    self.selected_inventory_item = max(0, self.selected_inventory_item - 8)
            elif event.key == pygame.K_DOWN:
                # 下键：选择当前模式的物品
                if self.storage_selection_mode == 'storage':
                    self.selected_storage_item = min(len(self.storage_items) - 1, self.selected_storage_item + 8)
                else:
                    player = self.game.player
                    inventory = player.item_manager.get_inventory()
                    self.selected_inventory_item = min(len(inventory) - 1, self.selected_inventory_item + 8)
            elif event.key == pygame.K_LEFT:
                # 左键：选择当前模式的物品
                if self.storage_selection_mode == 'storage':
                    self.selected_storage_item = max(0, self.selected_storage_item - 1)
                else:
                    self.selected_inventory_item = max(0, self.selected_inventory_item - 1)
            elif event.key == pygame.K_RIGHT:
                # 右键：选择当前模式的物品
                if self.storage_selection_mode == 'storage':
                    self.selected_storage_item = min(len(self.storage_items) - 1, self.selected_storage_item + 1)
                else:
                    player = self.game.player
                    inventory = player.item_manager.get_inventory()
                    self.selected_inventory_item = min(len(inventory) - 1, self.selected_inventory_item + 1)
            elif event.key == pygame.K_RETURN:
                # 存入或取出物品
                player = self.game.player
                inventory = player.item_manager.get_inventory()
                
                if self.storage_selection_mode == 'storage':
                    # 操作仓库物品（取出到背包）
                    if self.storage_items and 0 <= self.selected_storage_item < len(self.storage_items):
                        item = self.storage_items[self.selected_storage_item]
                        # 从仓库移除
                        self.storage_items.pop(self.selected_storage_item)
                        # 添加到背包
                        player.add_item(item['name'], item.get('quantity', 1))
                        # 更新选中索引
                        self.selected_storage_item = min(self.selected_storage_item, len(self.storage_items) - 1)
                        # 保存数据
                        if hasattr(self.game, 'data_storage'):
                            self.game.data_storage.save_storage_data(self.storage_items)
                else:
                    # 操作背包物品（存入仓库）
                    if inventory and 0 <= self.selected_inventory_item < len(inventory):
                        item = inventory[self.selected_inventory_item]
                        # 从背包移除
                        player.item_manager.remove_item(self.selected_inventory_item)
                        # 添加到仓库
                        self.storage_items.append({'name': item.name, 'quantity': item.quantity})
                        # 更新选中索引
                        self.selected_inventory_item = min(self.selected_inventory_item, len(inventory) - 2)  # 减2因为列表长度减少了1
                        # 保存数据
                        if hasattr(self.game, 'data_storage'):
                            self.game.data_storage.save_storage_data(self.storage_items)
    
    def render_recycle(self):
        """渲染回收界面"""
        # 绘制背景
        self.game.screen.fill((50, 50, 50))
        
        # 绘制回收标题
        recycle_text = self.large_font.render('物品回收', True, (255, 215, 0))
        self.game.screen.blit(recycle_text, (self.game.width // 2 - recycle_text.get_width() // 2, 50))
        
        # 绘制背包物品
        inventory_width = 800
        inventory_height = 400
        inventory_x = self.game.width // 2 - inventory_width // 2
        inventory_y = 120
        
        # 背包背景
        pygame.draw.rect(self.game.screen, (0, 0, 0), (inventory_x, inventory_y, inventory_width, inventory_height))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (inventory_x, inventory_y, inventory_width, inventory_height), 2)
        
        # 背包标题
        inventory_title = self.font.render('背包物品', True, (255, 215, 0))
        self.game.screen.blit(inventory_title, (inventory_x + 10, inventory_y + 10))
        
        # 绘制物品
        items_per_row = 8
        item_width = 90
        item_height = 70
        
        player = self.game.player
        inventory = player.item_manager.get_inventory()
        
        for i, item in enumerate(inventory):
            row = i // items_per_row
            col = i % items_per_row
            item_x = inventory_x + 10 + col * (item_width + 10)
            item_y = inventory_y + 50 + row * (item_height + 10)
            
            # 选中状态
            if i == self.selected_recycle_item:
                pygame.draw.rect(self.game.screen, (255, 215, 0), (item_x, item_y, item_width, item_height), 2)
            else:
                pygame.draw.rect(self.game.screen, (100, 100, 100), (item_x, item_y, item_width, item_height), 1)
            
            # 物品名称
            item_name = self.small_font.render(item.name, True, (255, 255, 255))
            self.game.screen.blit(item_name, (item_x + 5, item_y + 5))
            
            # 物品数量
            quantity_text = self.small_font.render(f'x{item.quantity}', True, (255, 215, 0))
            self.game.screen.blit(quantity_text, (item_x + 5, item_y + 30))
            
            # 回收价格
            recycle_price = self.get_recycle_price(item)
            price_text = self.small_font.render(f'回收价: {recycle_price}金币', True, (0, 255, 0))
            self.game.screen.blit(price_text, (item_x + 5, item_y + 50))
        
        # 绘制提示
        prompt_text = self.small_font.render('按Escape关闭回收 | 按Enter回收物品', True, (150, 150, 150))
        self.game.screen.blit(prompt_text, (self.game.width // 2 - prompt_text.get_width() // 2, self.game.height - 50))
    
    def handle_recycle_events(self, event):
        """处理回收事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # 关闭回收
                self.show_recycle = False
                self.game.game_state = GameState.GAME
            elif event.key == pygame.K_UP:
                self.selected_recycle_item = max(0, self.selected_recycle_item - 8)
            elif event.key == pygame.K_DOWN:
                player = self.game.player
                inventory = player.item_manager.get_inventory()
                self.selected_recycle_item = min(len(inventory) - 1, self.selected_recycle_item + 8)
            elif event.key == pygame.K_LEFT:
                self.selected_recycle_item = max(0, self.selected_recycle_item - 1)
            elif event.key == pygame.K_RIGHT:
                player = self.game.player
                inventory = player.item_manager.get_inventory()
                self.selected_recycle_item = min(len(inventory) - 1, self.selected_recycle_item + 1)
            elif event.key == pygame.K_RETURN:
                # 回收物品
                player = self.game.player
                inventory = player.item_manager.get_inventory()
                
                if inventory and 0 <= self.selected_recycle_item < len(inventory):
                    item = inventory[self.selected_recycle_item]
                    # 计算回收价格
                    recycle_price = self.get_recycle_price(item)
                    # 从背包移除
                    player.item_manager.remove_item(self.selected_recycle_item)
                    # 增加金币
                    self.game.gold += recycle_price
                    # 更新选中索引
                    self.selected_recycle_item = min(self.selected_recycle_item, len(inventory) - 2)  # 减2因为列表长度减少了1
    
    def get_recycle_price(self, item):
        """获取物品回收价格"""
        # 基础回收价格表
        base_prices = {
            '金疮药': 5,
            '魔法药': 5,
            '铁剑': 20,
            '铁甲': 15,
            '木剑': 5,
            '布衣': 3,
            '皮帽': 2,
            '草鞋': 1,
            '骷髅骨': 1,
            '僵尸牙齿': 1,
            '狼皮': 2,
            '腐烂的肉': 1
        }
        
        # 根据物品名称获取基础价格
        base_price = base_prices.get(item.name, 1)
        # 计算总价（数量 * 单价）
        return base_price * item.quantity