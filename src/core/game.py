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
        
        # 设置窗口大小和标题
        self.width, self.height = 1024, 768  # 增大默认窗口大小
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
            
            # 处理保存提示事件
            if self.ui.show_save_prompt:
                self.ui.handle_save_prompt_events(event)
            elif self.ui.show_name_input:
                # 处理角色名称输入事件
                self.ui.handle_name_input_events(event)
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
                    if hasattr(self.player, 'set_skill_hotkey') and self.ui.selected_skill_index < len(self.player.skills):
                        self.player.set_skill_hotkey(self.ui.selected_skill_index, hotkey)
                        # 保存技能快捷键设置
                        if hasattr(self, 'data_storage'):
                            try:
                                # 保存快捷键设置到玩家数据
                                # 直接调用save_player_data，它会自动保存所有玩家数据
                                self.data_storage.save_player_data(1)
                            except Exception as e:
                                print(f"保存技能快捷键设置失败: {e}")
                
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
                
                if hasattr(self.player, 'use_skill_by_hotkey'):
                    if self.player.use_skill_by_hotkey(hotkey):
                        # 技能使用成功
                        pass
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
                
                if hasattr(npc, 'has_shop') and npc.has_shop:
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
        # 根据游戏状态更新
        if self.game_state == GameState.GAME:
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
        
    def render(self):
        """渲染游戏"""
        # 填充背景，确保清除所有之前的渲染内容
        self.screen.fill((0, 0, 0))
        
        # 渲染保存提示
        if self.ui.show_save_prompt:
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
        elif self.ui.show_name_input:
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