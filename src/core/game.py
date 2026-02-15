import pygame
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.states import GameState
from src.entities.player import Player
from src.map.map_manager import MapManager
from src.ui.ui import UI
from src.systems.data_storage import DataStorage
from src.systems.quest_system import Quest


class Game:
    """游戏核心类"""
    
    def __init__(self):
        """初始化游戏"""
        # 初始化pygame
        print("Initializing pygame...")
        pygame.init()
        print("Pygame initialized successfully")
        
        # 初始化声音系统
        pygame.mixer.init()
        print("Sound system initialized successfully")
        
        # 设置窗口大小和标题
        self.width, self.height = 1280, 800  # 增大默认窗口大小
        # 创建可调整大小的窗口
        print(f"Creating window: {self.width}x{self.height}")
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("传奇游戏")
        print("Window created successfully")
        
        # 设置时钟
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # 游戏状态
        self.running = True
        self.game_state = GameState.MENU
        
        # 职业选择（默认战士）
        self.selected_class = "战士"
        
        # 初始化游戏元素
        # 暂时不创建player对象，等用户选择开始游戏后再创建
        self.player = None  # 初始化为None
        self.map_manager = MapManager(self)  # 使用地图管理器
        self.ui = UI(self)
        
        # 游戏数据
        self.gold = 1000
        self.experience = 0
        self.level = 1
        self.experience_to_next_level = 100  # 升级所需经验值
        
        # 相机位置
        self.camera_x = 0
        self.camera_y = 0
        
        # 初始化任务系统
        from src.systems.quest_system import QuestSystem
        self.quest_system = QuestSystem(self)
        
        # 初始化动画系统
        from src.systems.animation import AnimationManager
        self.animation_manager = AnimationManager()
        
        # 初始化数据存储系统
        self.data_storage = DataStorage(self)
        
        # 初始化鼠标悬停信息
        self.hovered_item = None
        
        # 商人菜单
        self.show_merchant_menu = False
        self.current_merchant = None
        self.selected_merchant_option = 0
        self.merchant_options = ["打开商店", "物品回收"]
        
        # 注释掉自动存档选择，让用户在主菜单中手动选择继续游戏
        # if self.data_storage.has_saved_data():
        #     # 有存档，显示存档选择界面
        #     self.ui.show_load_selection = True
        #     self.ui.selected_load_slot = 0
        
        # 显示当前地图的Boss信息
        current_map = self.map_manager.get_current_map()
        if current_map and hasattr(self, 'ui') and hasattr(self.ui, 'add_game_message'):
            # 查找地图中的Boss
            boss_monsters = [monster for monster in current_map.monsters if hasattr(monster, 'name') and ('王' in monster.name or '教主' in monster.name)]
            for boss in boss_monsters:
                boss_message = f"[Boss刷新] {boss.name} 在 {current_map.scene_type} 出现了！坐标: ({int(boss.x)}, {int(boss.y)})"
                print(boss_message)
                self.ui.add_game_message(boss_message, (255, 0, 0), 5000)
    
    def add_exp(self, amount):
        """添加经验值
        
        Args:
            amount: 要添加的经验值
        """
        self.experience += amount
        
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 显示保存提示
                self.ui.show_save_prompt = True
            elif event.type == pygame.VIDEORESIZE:
                # 处理窗口大小调整
                self.width, self.height = event.w, event.h
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEMOTION:
                # 处理鼠标移动，更新悬停信息
                if self.game_state == GameState.GAME:
                    pos = pygame.mouse.get_pos()
                    self.hovered_item = self.ui.handle_hover(pos)
            
            # 处理保存提示事件
            if hasattr(self.ui, 'show_save_prompt') and self.ui.show_save_prompt:
                self.ui.handle_save_prompt_events(event)
            elif hasattr(self.ui, 'show_name_input') and self.ui.show_name_input:
                # 处理角色名称输入事件
                self.ui.handle_name_input_events(event)
            elif hasattr(self.ui, 'show_storage') and self.ui.show_storage:
                # 处理仓库事件
                self.ui.handle_storage_events(event)
            elif hasattr(self.ui, 'show_recycle') and self.ui.show_recycle:
                # 处理回收事件
                self.ui.handle_recycle_events(event)
            elif hasattr(self, 'show_merchant_menu') and self.show_merchant_menu:
                # 处理商人菜单事件
                self.handle_merchant_menu_events(event)
            else:
                # 根据游戏状态处理事件
                if self.game_state == GameState.MENU:
                    self.ui.handle_menu_events(event)
                elif self.game_state == GameState.GAME:
                    self.handle_game_events(event)
                elif self.game_state == GameState.BATTLE:
                    self.ui.handle_battle_events(event)
                elif self.game_state == GameState.SHOP:
                    self.ui.handle_shop_events(event)
                elif self.game_state == GameState.DIALOGUE:
                    self.ui.handle_dialogue_events(event)
                elif self.game_state == GameState.INVENTORY:
                    self.ui.handle_inventory_events(event)
                elif self.game_state == GameState.CHARACTER:
                    self.ui.handle_character_events(event)
                elif self.game_state == GameState.SKILLS:
                    self.ui.handle_skills_events(event)
                elif self.game_state == GameState.HELP:
                    self.ui.handle_help_events(event)
    
    def handle_game_events(self, event):
        """处理游戏中的事件"""
        # 鼠标点击
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # 转换鼠标位置到游戏世界坐标
            world_x = pos[0] + int(self.camera_x)
            world_y = pos[1] + int(self.camera_y)
            # 检查是否点击了怪物
            current_map = self.map_manager.get_current_map()
            if current_map:
                clicked_monster = current_map.get_monster_at_position(world_x, world_y)
                if clicked_monster:
                    # 更新UI选中的怪物
                    self.ui.selected_monster = clicked_monster
                    # 攻击选中的怪物
                    self.player.attack_monster(clicked_monster)
                else:
                    # 检查是否点击了地面
                    # 处理UI点击
                    ui_clicked = self.ui.handle_click(pos)
                    if not ui_clicked:
                        # 点击了空白区域
                        print("请点击怪物进行攻击，或按1-3键使用技能！")
        
        # 键盘按下
        if event.type == pygame.KEYDOWN:
            if self.ui.is_setting_skill:
                # 处理技能快捷键设置
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                    # 将0键映射为10
                    hotkey = event.key - pygame.K_0
                    if hotkey == 0:
                        hotkey = 10
                    
                    # 设置技能快捷键
                    if self.ui.selected_skill_index < len(self.player.skills):
                        # 直接设置技能快捷键映射
                        self.player.skill_hotkeys[str(hotkey)] = self.ui.selected_skill_index
                        self.player.hotkey_skills[self.ui.selected_skill_index] = str(hotkey)
                        
                        # 保存技能快捷键设置
                        if hasattr(self, 'data_storage'):
                            try:
                                # 保存快捷键设置到玩家数据
                                self.data_storage.save_player_data(1)
                            except Exception as e:
                                print(f"保存技能快捷键设置失败: {e}")
                        
                        # 显示技能设置成功消息
                        skill = self.player.skills[self.ui.selected_skill_index]
                        skill_name = skill.get('name', '未知技能')
                        print(f"技能快捷键设置成功: {skill_name} -> {hotkey}")
                        
                        # 添加技能设置消息到聊天框
                        if hasattr(self, 'ui') and hasattr(self.ui, 'add_game_message'):
                            message = f"技能快捷键设置成功: {skill_name} -> {hotkey}"
                            self.ui.add_game_message(message, (255, 215, 0), 3000)
                
                # 结束设置状态
                self.ui.is_setting_skill = False
                self.ui.selected_skill_index = -1
            elif event.key == pygame.K_ESCAPE:
                self.game_state = GameState.MENU
            elif event.key == pygame.K_SPACE:
                current_map = self.map_manager.get_current_map()
                if current_map:
                    self.player.attack_monsters(current_map)
            elif event.key == pygame.K_TAB:
                # 打开背包
                self.game_state = GameState.INVENTORY
            elif event.key == pygame.K_e:
                # 与附近的NPC交互
                self.interact_with_npcs()
            elif event.key == pygame.K_h:
                # 打开帮助
                self.game_state = GameState.HELP
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # 保存游戏 - 显示存档选择 (Ctrl+S组合键)
                self.ui.show_save_selection = True
                self.ui.selected_save_slot = 0
                self.game_state = GameState.MENU
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                # 通过快捷键使用技能
                hotkey = event.key - pygame.K_0
                if hotkey == 0:
                    hotkey = 10
                
                # 使用技能快捷键映射
                hotkey_str = str(hotkey)
                if hotkey_str in self.player.skill_hotkeys:
                    skill_index = self.player.skill_hotkeys[hotkey_str]
                    if 0 <= skill_index < len(self.player.skills):
                        skill = self.player.skills[skill_index]
                        skill_name = skill['name']
                        # 尝试自动找到目标
                        current_map = self.map_manager.get_current_map()
                        if current_map:
                            # 使用技能的实际范围找到最近的怪物作为目标
                            skill_range = skill.get('range', 100)
                            near_monsters = current_map.get_monsters_near_player(self.player, distance=skill_range)
                            if near_monsters:
                                target = near_monsters[0]
                                if self.player.use_skill(skill_name, target):
                                    print(f"按{hotkey}键使用技能: {skill_name}！")
                            else:
                                # 没有目标，使用技能（可能是范围技能）
                                if self.player.use_skill(skill_name):
                                    print(f"按{hotkey}键使用技能: {skill_name}！")
                else:
                    # 兼容旧版本：直接使用技能索引
                    skill_index = hotkey - 1
                    if 0 <= skill_index < len(self.player.skills):
                        skill = self.player.skills[skill_index]
                        skill_name = skill['name']
                        # 尝试自动找到目标
                        current_map = self.map_manager.get_current_map()
                        if current_map:
                            # 使用技能的实际范围找到最近的怪物作为目标
                            skill_range = skill.get('range', 100)
                            near_monsters = current_map.get_monsters_near_player(self.player, distance=skill_range)
                            if near_monsters:
                                target = near_monsters[0]
                                if self.player.use_skill(skill_name, target):
                                    print(f"按{hotkey}键使用技能: {skill_name}！")
                            else:
                                # 没有目标，使用技能（可能是范围技能）
                                if self.player.use_skill(skill_name):
                                    print(f"按{hotkey}键使用技能: {skill_name}！")
            elif event.key == pygame.K_F8:
                # F8显示任务状态+人物显示
                print("显示任务状态和人物信息")
                # 打开任务状态界面
                self.game_state = GameState.CHARACTER
            elif event.key == pygame.K_F9:
                # F9显示背包和装备
                print("显示背包和装备")
                self.game_state = GameState.INVENTORY
            elif event.key == pygame.K_F10:
                # F10显示技能天赋
                print("显示技能天赋")
                self.game_state = GameState.SKILLS
    
    def interact_with_npcs(self):
        """与附近的NPC交互"""
        try:
            # 获取当前地图
            current_map = self.map_manager.get_current_map()
            if not current_map:
                print("当前没有地图！")
                return
            
            # 获取附近的NPC
            near_npcs = current_map.get_npcs_near_player(self.player, distance=50)
            
            if near_npcs:
                # 与第一个NPC交互
                npc = near_npcs[0]
                
                # 检查NPC功能类型
                npc_function = getattr(npc, 'function', None)
                
                if npc_function == 'storage':
                    # 加载公共仓库数据
                    if hasattr(self, 'data_storage'):
                        storage_items = self.data_storage.load_storage_data()
                        self.ui.storage_items = storage_items
                    # 打开仓库界面
                    self.ui.show_storage = True
                    print(f"打开了{npc.name}的公共仓库")
                elif npc_function == 'recycle' or (hasattr(npc, 'has_shop') and npc.has_shop):
                    # 先显示选项菜单，让玩家选择是打开商店还是回收
                    self.show_merchant_menu = True
                    self.current_merchant = npc
                    print(f"与{npc.name}对话，选择操作：")
                    print("1. 打开商店")
                    print("2. 物品回收")
                else:
                    # 开始对话
                    dialogue = npc.interact(self.player)
                    self.ui.start_dialogue(npc, dialogue)
                    
                    # 检查是否有任务可以发放或完成
                    if hasattr(npc, 'give_quest'):
                        # 检查是否有可完成的任务
                        completed_quests = self.quest_system.get_completed_quests()
                        npc_completed_quests = [quest for quest in completed_quests if quest.npc_name == npc.name]
                        
                        if npc_completed_quests:
                            # 完成任务
                            for quest in npc_completed_quests:
                                if self.quest_system.complete_quest(quest.id):
                                    print(f"你完成了任务：{quest.name}")
                                    print(f"获得奖励：经验{quest.rewards.get('exp', 0)}，金币{quest.rewards.get('gold', 0)}")
                                    if 'items' in quest.rewards:
                                        for item in quest.rewards['items']:
                                            print(f"获得物品：{item['name']}×{item['quantity']}")
                        else:
                            # 发放新任务
                            quest = npc.give_quest(self.player)
                            if quest:
                                print(f"{npc.name}给了你一个任务：{quest['title']}")
                                print(f"任务描述：{quest['description']}")
                                print(f"任务奖励：经验{quest['reward'].get('exp', 0)}，金币{quest['reward'].get('gold', 0)}")
                                if 'items' in quest['reward']:
                                    for item in quest['reward']['items']:
                                        print(f"获得物品：{item}")
                                # 创建任务对象并添加到任务系统
                                new_quest = Quest(
                                    id=len(self.quest_system.quests) + 1,
                                    name=quest['title'],
                                    description=quest['description'],
                                    npc_name=npc.name,
                                    requirements={'kill': {quest.get('target', '稻草人'): quest.get('count', 5)}},
                                    rewards=quest['reward']
                                )
                                self.quest_system.quests.append(new_quest)
            else:
                print("附近没有NPC可以交互！")
        except Exception as e:
            print(f"交互错误: {e}")
            import traceback
            traceback.print_exc()
    
    def check_level_up(self):
        """检查升级"""
        while self.experience >= self.experience_to_next_level:
            # 升级
            self.level += 1
            self.experience -= self.experience_to_next_level
            
            # 计算下一级所需经验值
            self.experience_to_next_level = int(self.experience_to_next_level * 1.5)
            
            # 获取职业成长率
            growth_rates = self.player.profession.get_stat_growth()
            
            # 提升属性
            self.player.base_health += growth_rates["health"]
            self.player.base_max_health += growth_rates["health"]
            self.player.base_attack += growth_rates["attack"]
            self.player.base_defense += growth_rates["defense"]
            self.player.base_magic += growth_rates["magic"]
            
            # 恢复生命值
            self.player.health = self.player.base_max_health
            
            # 调用职业的升级方法
            self.player.profession.level_up()
            
            # 更新技能列表
            self.player.skills = self.player.profession.get_skills()
            self.player.learned_skills = [skill['name'] for skill in self.player.skills if skill['level'] > 0]
            
            # 重新计算装备属性
            self.player.calculate_equipment_stats()
            
            # 显示升级信息
            print(f"恭喜升级！现在是{self.level}级！")
            print(f"职业: {self.player.职业}")
            print(f"生命值: {self.player.health}/{self.player.max_health}")
            print(f"攻击力: {self.player.attack}")
            print(f"防御力: {self.player.defense}")
            print(f"魔法力: {self.player.magic}")
    
    def update(self):
        """更新游戏状态"""
        # 检查是否有特殊界面打开
        has_special_ui = False
        if hasattr(self.ui, 'show_storage') and self.ui.show_storage:
            has_special_ui = True
        elif hasattr(self.ui, 'show_recycle') and self.ui.show_recycle:
            has_special_ui = True
        elif hasattr(self, 'show_merchant_menu') and self.show_merchant_menu:
            has_special_ui = True
        elif hasattr(self.ui, 'show_save_prompt') and self.ui.show_save_prompt:
            has_special_ui = True
        elif hasattr(self.ui, 'show_name_input') and self.ui.show_name_input:
            has_special_ui = True
        
        # 根据游戏状态更新
        if self.game_state == GameState.GAME and not has_special_ui:
            self.player.update()
            self.player.update_skills()  # 更新技能状态
            self.map_manager.update()  # 更新地图管理器
            
            # 更新动画
            self.animation_manager.update()
            
            # 更新掉落物品提示
            self.ui.update_item_drops()
            # 更新伤害值显示
            self.ui.update_damage_texts()
            # 更新游戏内消息
            self.ui.update_game_messages()
            
            # 检查升级
            self.check_level_up()
            
            # 更新相机位置，跟随玩家（添加平滑过渡效果）
            target_camera_x = self.player.x - self.width // 2
            target_camera_y = self.player.y - self.height // 2
            
            # 平滑相机移动
            self.camera_x += (target_camera_x - self.camera_x) * 0.1
            self.camera_y += (target_camera_y - self.camera_y) * 0.1
            
            # 限制相机范围，防止超出地图
            current_map = self.map_manager.get_current_map()
            if current_map:
                self.camera_x = max(0, min(current_map.width - self.width, self.camera_x))
                self.camera_y = max(0, min(current_map.height - self.height, self.camera_y))
        else:
            # 特殊界面打开时，只更新必要的UI元素
            self.ui.update_item_drops()
            self.ui.update_damage_texts()
            self.ui.update_game_messages()
        
    def render(self):
        """渲染游戏"""
        # 填充背景，确保清除所有之前的渲染内容
        self.screen.fill((0, 0, 0))
        
        # 优先渲染特殊界面
        if hasattr(self.ui, 'show_storage') and self.ui.show_storage:
            # 渲染仓库界面
            self.ui.render_storage()
        elif hasattr(self.ui, 'show_recycle') and self.ui.show_recycle:
            # 渲染回收界面
            self.ui.render_recycle()
        elif hasattr(self, 'show_merchant_menu') and self.show_merchant_menu:
            # 渲染商人菜单
            self.render_merchant_menu()
        elif hasattr(self.ui, 'show_save_prompt') and self.ui.show_save_prompt:
            # 渲染保存提示
            # 先渲染当前游戏状态
            if self.game_state == GameState.GAME:
                # 渲染地图（背景）
                # 使用地图管理器渲染当前地图
                self.map_manager.render(self.screen)
                
                # 渲染玩家（在地图之后，UI之前）
                self.player.render(self.screen, (self.camera_x, self.camera_y))
                
                # 渲染动画效果
                self.animation_manager.render(self.screen, (self.camera_x, self.camera_y))
                
                # 渲染UI（UI不受相机影响）
                self.ui.render_game_ui()
                
                # 渲染掉落物品提示
                self.ui.render_item_drops()
                # 渲染伤害值显示
                self.ui.render_damage_texts()
                # 渲染游戏内消息
                self.ui.render_game_messages()
                
                # 渲染鼠标悬停信息
                if hasattr(self, 'hovered_item') and self.hovered_item:
                    pos = pygame.mouse.get_pos()
                    hover_x, hover_y = pos
                    hover_x += 10
                    hover_y -= 100  # 大幅向上偏移，确保显示在鼠标上方且不会被遮挡
                    
                    # 绘制悬停信息背景
                    if isinstance(self.hovered_item, dict) and 'name' in self.hovered_item:
                        # 技能悬停信息
                        skill_name = self.hovered_item.get('name', '未知技能')
                        skill_level = self.hovered_item.get('level', 0)
                        skill_damage = self.hovered_item.get('damage', 0)
                        skill_range = self.hovered_item.get('range', 0)
                        skill_cooldown = self.hovered_item.get('cooldown', 0) / 1000  # 转换为秒
                        skill_description = self.hovered_item.get('description', '无描述')
                        
                        # 使用UI中已经加载的支持中文的字体
                        small_font = self.ui.small_font
                        
                        # 计算文本宽度
                        max_width = max(
                            small_font.size(skill_name)[0],
                            small_font.size(f'等级: {skill_level}')[0],
                            small_font.size(f'伤害: {skill_damage}')[0],
                            small_font.size(f'范围: {skill_range}')[0],
                            small_font.size(f'冷却: {skill_cooldown}秒')[0],
                            small_font.size(skill_description)[0]
                        )
                        
                        # 计算背景高度
                        background_height = 110
                        
                        # 调整悬停信息位置，确保不会超出窗口
                        if hover_y - background_height < 0:
                            hover_y = pos[1] + 20  # 如果上方空间不够，显示在鼠标下方
                        else:
                            hover_y -= background_height
                        
                        # 确保信息不会超出窗口右侧
                        if hover_x + max_width + 20 > self.width:
                            hover_x = self.width - max_width - 30
                        
                        # 绘制半透明背景
                        background_rect = pygame.Rect(hover_x, hover_y, max_width + 20, background_height)
                        # 创建半透明表面
                        transparent_surface = pygame.Surface((max_width + 20, background_height), pygame.SRCALPHA)
                        # 填充半透明黑色
                        transparent_surface.fill((30, 30, 30, 180))  # 最后一个参数是透明度，180表示半透明
                        # 绘制边框
                        pygame.draw.rect(transparent_surface, (100, 100, 100, 255), (0, 0, max_width + 20, background_height), 2)
                        # 绘制到屏幕
                        self.screen.blit(transparent_surface, (hover_x, hover_y))
                        
                        # 绘制技能信息
                        name_text = small_font.render(skill_name, True, (255, 215, 0))
                        self.screen.blit(name_text, (hover_x + 10, hover_y + 10))
                        
                        level_text = small_font.render(f'等级: {skill_level}', True, (255, 255, 255))
                        self.screen.blit(level_text, (hover_x + 10, hover_y + 30))
                        
                        damage_text = small_font.render(f'伤害: {skill_damage}', True, (255, 0, 0))
                        self.screen.blit(damage_text, (hover_x + 10, hover_y + 50))
                        
                        range_text = small_font.render(f'范围: {skill_range}', True, (0, 255, 0))
                        self.screen.blit(range_text, (hover_x + 10, hover_y + 70))
                        
                        cooldown_text = small_font.render(f'冷却: {skill_cooldown}秒', True, (0, 0, 255))
                        self.screen.blit(cooldown_text, (hover_x + 10, hover_y + 90))
                    elif hasattr(self.hovered_item, 'name'):
                        # 物品悬停信息
                        item_name = self.hovered_item.name
                        item_quantity = getattr(self.hovered_item, 'quantity', 1)
                        item_type = getattr(self.hovered_item, 'type', '未知')
                        item_description = getattr(self.hovered_item, 'description', '无描述')
                        
                        # 使用UI中已经加载的支持中文的字体
                        small_font = self.ui.small_font
                        
                        # 计算文本宽度
                        max_width = max(
                            small_font.size(item_name)[0],
                            small_font.size(f'数量: {item_quantity}')[0],
                            small_font.size(f'类型: {item_type}')[0],
                            small_font.size(item_description)[0]
                        )
                        
                        # 计算背景高度
                        background_height = 80
                        
                        # 调整悬停信息位置，确保不会超出窗口
                        if hover_y - background_height < 0:
                            hover_y = pos[1] + 20  # 如果上方空间不够，显示在鼠标下方
                        else:
                            hover_y -= background_height
                        
                        # 确保信息不会超出窗口右侧
                        if hover_x + max_width + 20 > self.width:
                            hover_x = self.width - max_width - 30
                        
                        # 绘制半透明背景
                        background_rect = pygame.Rect(hover_x, hover_y, max_width + 20, background_height)
                        # 创建半透明表面
                        transparent_surface = pygame.Surface((max_width + 20, background_height), pygame.SRCALPHA)
                        # 填充半透明黑色
                        transparent_surface.fill((30, 30, 30, 180))  # 最后一个参数是透明度，180表示半透明
                        # 绘制边框
                        pygame.draw.rect(transparent_surface, (100, 100, 100, 255), (0, 0, max_width + 20, background_height), 2)
                        # 绘制到屏幕
                        self.screen.blit(transparent_surface, (hover_x, hover_y))
                        
                        # 绘制物品信息
                        name_text = small_font.render(item_name, True, (255, 215, 0))
                        self.screen.blit(name_text, (hover_x + 10, hover_y + 10))
                        
                        quantity_text = small_font.render(f'数量: {item_quantity}', True, (255, 255, 255))
                        self.screen.blit(quantity_text, (hover_x + 10, hover_y + 25))
                        
                        type_text = small_font.render(f'类型: {item_type}', True, (255, 255, 255))
                        self.screen.blit(type_text, (hover_x + 10, hover_y + 40))
                        
                        desc_text = small_font.render(item_description, True, (200, 200, 200))
                        self.screen.blit(desc_text, (hover_x + 10, hover_y + 55))
            elif self.game_state == GameState.MENU:
                self.ui.render_menu()
                # 渲染游戏内消息
                self.ui.render_game_messages()
            elif self.game_state == GameState.BATTLE:
                self.ui.render_battle()
            elif self.game_state == GameState.SHOP:
                self.ui.render_shop()
            elif self.game_state == GameState.DIALOGUE:
                self.ui.render_dialogue()
            elif self.game_state == GameState.INVENTORY:
                self.ui.render_inventory()
            elif self.game_state == GameState.CHARACTER:
                # 渲染人物状态和任务界面
                self.ui.render_character()
            elif self.game_state == GameState.SKILLS:
                # 渲染技能天赋界面
                self.ui.render_skills()
            elif self.game_state == GameState.HELP:
                self.ui.render_help()
            
            # 渲染保存提示对话框
            self.ui.render_save_prompt()
        elif hasattr(self.ui, 'show_name_input') and self.ui.show_name_input:
            # 渲染角色名称输入界面
            self.ui.render_name_input()
        else:
            # 根据游戏状态渲染
            if self.game_state == GameState.MENU:
                self.ui.render_menu()
            elif self.game_state == GameState.GAME:
                # 渲染地图（背景）
                # 使用地图管理器渲染当前地图
                self.map_manager.render(self.screen)
                
                # 渲染玩家（在地图之后，UI之前）
                self.player.render(self.screen, (self.camera_x, self.camera_y))
                
                # 渲染动画效果
                self.animation_manager.render(self.screen, (self.camera_x, self.camera_y))
                
                # 渲染UI（UI不受相机影响）
                self.ui.render_game_ui()
                
                # 渲染掉落物品提示
                self.ui.render_item_drops()
                # 渲染伤害值显示
                self.ui.render_damage_texts()
                # 渲染游戏内消息
                self.ui.render_game_messages()
                
                # 渲染鼠标悬停信息
                if hasattr(self, 'hovered_item') and self.hovered_item:
                    pos = pygame.mouse.get_pos()
                    hover_x, hover_y = pos
                    hover_x += 10
                    hover_y -= 100  # 大幅向上偏移，确保显示在鼠标上方且不会被遮挡
                    
                    # 绘制悬停信息背景
                    if isinstance(self.hovered_item, dict) and 'name' in self.hovered_item:
                        # 技能悬停信息
                        skill_name = self.hovered_item.get('name', '未知技能')
                        skill_level = self.hovered_item.get('level', 0)
                        skill_damage = self.hovered_item.get('damage', 0)
                        skill_range = self.hovered_item.get('range', 0)
                        skill_cooldown = self.hovered_item.get('cooldown', 0) / 1000  # 转换为秒
                        skill_description = self.hovered_item.get('description', '无描述')
                        
                        # 使用UI中已经加载的支持中文的字体
                        small_font = self.ui.small_font
                        
                        # 计算文本宽度
                        max_width = max(
                            small_font.size(skill_name)[0],
                            small_font.size(f'等级: {skill_level}')[0],
                            small_font.size(f'伤害: {skill_damage}')[0],
                            small_font.size(f'范围: {skill_range}')[0],
                            small_font.size(f'冷却: {skill_cooldown}秒')[0],
                            small_font.size(skill_description)[0]
                        )
                        
                        # 计算背景高度
                        background_height = 110
                        
                        # 调整悬停信息位置，确保不会超出窗口
                        if hover_y - background_height < 0:
                            hover_y = pos[1] + 20  # 如果上方空间不够，显示在鼠标下方
                        else:
                            hover_y -= background_height
                        
                        # 确保信息不会超出窗口右侧
                        if hover_x + max_width + 20 > self.width:
                            hover_x = self.width - max_width - 30
                        
                        # 绘制半透明背景
                        background_rect = pygame.Rect(hover_x, hover_y, max_width + 20, background_height)
                        # 创建半透明表面
                        transparent_surface = pygame.Surface((max_width + 20, background_height), pygame.SRCALPHA)
                        # 填充半透明黑色
                        transparent_surface.fill((30, 30, 30, 180))  # 最后一个参数是透明度，180表示半透明
                        # 绘制边框
                        pygame.draw.rect(transparent_surface, (100, 100, 100, 255), (0, 0, max_width + 20, background_height), 2)
                        # 绘制到屏幕
                        self.screen.blit(transparent_surface, (hover_x, hover_y))
                        
                        # 绘制技能信息
                        name_text = small_font.render(skill_name, True, (255, 215, 0))
                        self.screen.blit(name_text, (hover_x + 10, hover_y + 10))
                        
                        level_text = small_font.render(f'等级: {skill_level}', True, (255, 255, 255))
                        self.screen.blit(level_text, (hover_x + 10, hover_y + 30))
                        
                        damage_text = small_font.render(f'伤害: {skill_damage}', True, (255, 0, 0))
                        self.screen.blit(damage_text, (hover_x + 10, hover_y + 50))
                        
                        range_text = small_font.render(f'范围: {skill_range}', True, (0, 255, 0))
                        self.screen.blit(range_text, (hover_x + 10, hover_y + 70))
                        
                        cooldown_text = small_font.render(f'冷却: {skill_cooldown}秒', True, (0, 0, 255))
                        self.screen.blit(cooldown_text, (hover_x + 10, hover_y + 90))
                    elif hasattr(self.hovered_item, 'name'):
                        # 物品悬停信息
                        item_name = self.hovered_item.name
                        item_quantity = getattr(self.hovered_item, 'quantity', 1)
                        item_type = getattr(self.hovered_item, 'type', '未知')
                        item_description = getattr(self.hovered_item, 'description', '无描述')
                        
                        # 使用UI中已经加载的支持中文的字体
                        small_font = self.ui.small_font
                        
                        # 计算文本宽度
                        max_width = max(
                            small_font.size(item_name)[0],
                            small_font.size(f'数量: {item_quantity}')[0],
                            small_font.size(f'类型: {item_type}')[0],
                            small_font.size(item_description)[0]
                        )
                        
                        # 计算背景高度
                        background_height = 80
                        
                        # 调整悬停信息位置，确保不会超出窗口
                        if hover_y - background_height < 0:
                            hover_y = pos[1] + 20  # 如果上方空间不够，显示在鼠标下方
                        else:
                            hover_y -= background_height
                        
                        # 确保信息不会超出窗口右侧
                        if hover_x + max_width + 20 > self.width:
                            hover_x = self.width - max_width - 30
                        
                        # 绘制半透明背景
                        background_rect = pygame.Rect(hover_x, hover_y, max_width + 20, background_height)
                        # 创建半透明表面
                        transparent_surface = pygame.Surface((max_width + 20, background_height), pygame.SRCALPHA)
                        # 填充半透明黑色
                        transparent_surface.fill((30, 30, 30, 180))  # 最后一个参数是透明度，180表示半透明
                        # 绘制边框
                        pygame.draw.rect(transparent_surface, (100, 100, 100, 255), (0, 0, max_width + 20, background_height), 2)
                        # 绘制到屏幕
                        self.screen.blit(transparent_surface, (hover_x, hover_y))
                        
                        # 绘制物品信息
                        name_text = small_font.render(item_name, True, (255, 215, 0))
                        self.screen.blit(name_text, (hover_x + 10, hover_y + 10))
                        
                        quantity_text = small_font.render(f'数量: {item_quantity}', True, (255, 255, 255))
                        self.screen.blit(quantity_text, (hover_x + 10, hover_y + 25))
                        
                        type_text = small_font.render(f'类型: {item_type}', True, (255, 255, 255))
                        self.screen.blit(type_text, (hover_x + 10, hover_y + 40))
                        
                        desc_text = small_font.render(item_description, True, (200, 200, 200))
                        self.screen.blit(desc_text, (hover_x + 10, hover_y + 55))
            elif self.game_state == GameState.BATTLE:
                self.ui.render_battle()
            elif self.game_state == GameState.SHOP:
                self.ui.render_shop()
            elif self.game_state == GameState.DIALOGUE:
                self.ui.render_dialogue()
            elif self.game_state == GameState.INVENTORY:
                self.ui.render_inventory()
            elif self.game_state == GameState.CHARACTER:
                # 渲染人物状态和任务界面
                self.ui.render_character()
            elif self.game_state == GameState.SKILLS:
                # 渲染技能天赋界面
                self.ui.render_skills()
            elif self.game_state == GameState.HELP:
                self.ui.render_help()
        
        # 更新显示
        pygame.display.flip()
        
    def handle_merchant_menu_events(self, event):
        """处理商人菜单事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # 取消，关闭菜单
                self.show_merchant_menu = False
            elif event.key == pygame.K_UP:
                # 上一个选项
                self.selected_merchant_option = (self.selected_merchant_option - 1) % len(self.merchant_options)
            elif event.key == pygame.K_DOWN:
                # 下一个选项
                self.selected_merchant_option = (self.selected_merchant_option + 1) % len(self.merchant_options)
            elif event.key == pygame.K_RETURN:
                # 确认选择
                if self.current_merchant:
                    npc = self.current_merchant
                    if self.selected_merchant_option == 0:
                        # 打开商店，使用NPC自己的商店物品
                        shop_items = []
                        if hasattr(npc, 'shop_items') and npc.shop_items:
                            from src.core.id_manager import id_manager
                            for item in npc.shop_items:
                                # 尝试获取物品ID
                                item_id = id_manager.get_item_id_by_name(item['name'])
                                item_info = None
                                if item_id:
                                    item_info = id_manager.get_item_by_id(item_id)
                                shop_items.append({"id": item_id, "name": item['name'], "price": item['price'], "quantity": item['quantity'], "info": item_info})
                        else:
                            # 默认商店物品
                            from src.core.id_manager import id_manager
                            shop_item_ids = [1001, 2001, 2003, 2004, 3001, 3002]
                            for item_id in shop_item_ids:
                                item_info = id_manager.get_item_by_id(item_id)
                                if item_info:
                                    # 根据物品类型设置价格
                                    if item_info['type'] == 'weapon':
                                        price = 100 if item_id == 1001 else 200
                                    elif item_info['type'] == 'armor':
                                        price = 50
                                    elif item_info['type'] == 'helmet':
                                        price = 30
                                    elif item_info['type'] == 'boots':
                                        price = 20
                                    elif item_info['type'] == 'consumable':
                                        price = 10 if item_id == 3001 else 15
                                    else:
                                        price = 50
                                    shop_items.append({"id": item_id, "name": item_info['name'], "price": price, "quantity": 99, "info": item_info})
                        
                        # 打开商店界面
                        self.ui.open_shop(shop_items)
                        print(f"打开了{npc.name}的商店")
                    elif self.selected_merchant_option == 1:
                        # 打开回收界面
                        self.ui.show_recycle = True
                        print(f"打开了{npc.name}的物品回收")
                # 关闭菜单
                self.show_merchant_menu = False
    
    def render_merchant_menu(self):
        """渲染商人菜单"""
        # 绘制菜单背景
        menu_width = 400
        menu_height = 200
        menu_x = self.width // 2 - menu_width // 2
        menu_y = self.height // 2 - menu_height // 2
        
        # 绘制背景
        pygame.draw.rect(self.screen, (0, 0, 0), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(self.screen, (100, 100, 100), (menu_x, menu_y, menu_width, menu_height), 2)
        
        # 使用UI中已经加载的支持中文的字体
        title_font = self.ui.large_font
        option_font = self.ui.font
        prompt_font = self.ui.small_font
        
        # 绘制标题
        if self.current_merchant:
            title = title_font.render(f"与{self.current_merchant.name}对话", True, (255, 215, 0))
            self.screen.blit(title, (menu_x + 20, menu_y + 20))
        
        # 绘制选项
        for i, option in enumerate(self.merchant_options):
            color = (255, 255, 255) if i == self.selected_merchant_option else (150, 150, 150)
            text = option_font.render(f"{i+1}. {option}", True, color)
            self.screen.blit(text, (menu_x + 40, menu_y + 80 + i * 40))
        
        # 绘制提示
        prompt = prompt_font.render("按上下键选择，Enter确认，Escape取消", True, (150, 150, 150))
        self.screen.blit(prompt, (menu_x + 40, menu_y + 160))

        # 控制帧率
        self.clock.tick(self.fps)


# 运行游戏
if __name__ == "__main__":
    game = Game()
    print("Game initialized, entering main loop...")
    while game.running:
        game.handle_events()
        game.update()
        game.render()
    print("Game exited")
    pygame.quit()
    sys.exit()