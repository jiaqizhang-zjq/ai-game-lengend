import json
import os
import time

class DataStorage:
    """数据存储系统"""
    
    def __init__(self, game):
        """初始化数据存储系统"""
        self.game = game
        self.save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'save')
        self._ensure_save_directory()
        self.max_save_slots = 3  # 最大存档槽位数
    
    def _ensure_save_directory(self):
        """确保保存目录存在"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def get_save_file_path(self, slot):
        """获取指定槽位的存档文件路径"""
        return os.path.join(self.save_dir, f'save_slot_{slot}.json')
    
    def list_saves(self):
        """列出所有存档"""
        saves = []
        for slot in range(1, self.max_save_slots + 1):
            save_file = self.get_save_file_path(slot)
            if os.path.exists(save_file):
                try:
                    with open(save_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    attributes = data.get('attributes', {})
                    save_info = {
                        'slot': slot,
                        'id': f'save_{slot}',
                        'name': data.get('name', '玩家'),
                        '职业': data.get('职业', '战士'),
                        'level': data.get('level', 1),
                        'gold': data.get('gold', 0),
                        'attack': attributes.get('base_attack', 10),
                        'defense': attributes.get('base_defense', 5),
                        'magic': attributes.get('base_magic', 5),
                        'health': attributes.get('base_health', 100),
                        'timestamp': os.path.getmtime(save_file)
                    }
                    saves.append(save_info)
                except Exception:
                    # 存档文件损坏
                    pass
        return saves
    
    def delete_save(self, slot):
        """删除指定槽位的存档"""
        save_file = self.get_save_file_path(slot)
        if os.path.exists(save_file):
            os.remove(save_file)
            print(f"存档槽位 {slot} 已删除！")
            return True
        return False
    
    def save_player_data(self, slot=1):
        """保存玩家数据到指定槽位"""
        import pygame
        current_time = pygame.time.get_ticks()
        
        player = self.game.player
        
        # 收集玩家数据
        # 转换技能冷却时间为相对时间
        skill_cooldowns = {}
        for skill_name, last_used in player.skill_cooldowns.items():
            # 计算相对时间（距离现在的毫秒数）
            relative_time = current_time - last_used
            # 只保存最近使用的技能冷却时间（小于10000毫秒）
            if relative_time < 10000:
                skill_cooldowns[skill_name] = relative_time
        
        player_data = {
            'name': player.name,
            '职业': player.职业,
            'level': self.game.level,
            'experience': self.game.experience,
            'gold': self.game.gold,
            'experience_to_next_level': self.game.experience_to_next_level,
            'map_id': self.game.map_manager.current_map_id,
            'position': {
                'x': player.x,
                'y': player.y
            },
            'attributes': {
                'base_health': player.base_health,
                'base_max_health': player.base_max_health,
                'base_attack': player.base_attack,
                'base_defense': player.base_defense,
                'base_magic': player.base_magic,
                'health': player.health
            },
            'equipment': player.equipment_manager.to_dict(),
            'inventory': [item.to_dict() for item in player.item_manager.get_inventory()],
            'skills': player.skills,
            'learned_skills': player.learned_skills,
            'skill_cooldowns': skill_cooldowns,
            'skill_hotkeys': getattr(player, 'skill_hotkeys', {}),
            'hotkey_skills': getattr(player, 'hotkey_skills', {})
        }
        
        # 保存到文件
        save_file = self.get_save_file_path(slot)
        with open(save_file, 'w', encoding='utf-8') as f:
            json.dump(player_data, f, ensure_ascii=False, indent=2)
        
        print(f"玩家数据已保存到槽位 {slot}！")
        return True
    
    def load_player_data(self, slot=1):
        """从指定槽位加载玩家数据"""
        save_file = self.get_save_file_path(slot)
        if not os.path.exists(save_file):
            print(f"槽位 {slot} 没有找到保存的玩家数据！")
            return False
        
        try:
            with open(save_file, 'r', encoding='utf-8') as f:
                player_data = json.load(f)
            
            # 加载玩家数据
            self._load_player_attributes(player_data)
            self._load_player_equipment(player_data)
            self._load_player_inventory(player_data)
            self._load_player_skills(player_data)
            self._load_game_data(player_data)
            
            print(f"从槽位 {slot} 加载玩家数据成功！")
            return True
        except Exception as e:
            print(f"加载玩家数据失败: {e}")
            return False
    
    def has_saved_data(self, slot=None):
        """检查是否有保存的玩家数据"""
        if slot:
            return os.path.exists(self.get_save_file_path(slot))
        else:
            # 检查是否有任何存档
            for slot_num in range(1, self.max_save_slots + 1):
                if os.path.exists(self.get_save_file_path(slot_num)):
                    return True
            return False
    
    def _load_player_attributes(self, player_data):
        """加载玩家属性"""
        player = self.game.player
        attributes = player_data.get('attributes', {})
        
        # 加载玩家名称
        player.name = player_data.get('name', player.name)
        
        player.base_health = attributes.get('base_health', player.base_health)
        player.base_max_health = attributes.get('base_max_health', player.base_max_health)
        player.base_attack = attributes.get('base_attack', player.base_attack)
        player.base_defense = attributes.get('base_defense', player.base_defense)
        player.base_magic = attributes.get('base_magic', player.base_magic)
        player.health = attributes.get('health', player.health)
        
        # 更新当前属性
        player.calculate_equipment_stats()
    
    def _load_player_equipment(self, player_data):
        """加载玩家装备"""
        from src.items import EquipmentManager
        equipment_data = player_data.get('equipment', {})
        self.game.player.equipment_manager = EquipmentManager.from_dict(equipment_data)
    
    def _load_player_inventory(self, player_data):
        """加载玩家物品栏"""
        inventory_data = player_data.get('inventory', [])
        player = self.game.player
        player.item_manager.clear_inventory()
        
        for item_data in inventory_data:
            from src.items import Item
            item = Item.from_dict(item_data)
            player.item_manager.add_item(item.name, item.quantity, item)
    
    def _load_player_skills(self, player_data):
        """加载玩家技能"""
        import pygame
        current_time = pygame.time.get_ticks()
        
        player = self.game.player
        player.skills = player_data.get('skills', player.skills)
        player.learned_skills = player_data.get('learned_skills', player.learned_skills)
        
        # 加载技能冷却时间
        loaded_cooldowns = player_data.get('skill_cooldowns', {})
        skill_cooldowns = {}
        for skill_name, cooldown_value in loaded_cooldowns.items():
            # 检查cooldown_value是否是相对时间（小于10000），如果是则转换为绝对时间
            if cooldown_value < 10000:
                # 相对时间，转换为绝对时间
                skill_cooldowns[skill_name] = current_time - cooldown_value
            else:
                # 旧的绝对时间值，重置为0（技能不在冷却中）
                # 这样可以避免技能一直显示在冷却中
                pass
        player.skill_cooldowns = skill_cooldowns
        
        # 加载技能快捷键设置
        if hasattr(player, 'skill_hotkeys'):
            loaded_hotkeys = player_data.get('skill_hotkeys', {})
            # 将字符串类型的键转换回数字类型
            skill_hotkeys = {}
            for hotkey_str, skill_index in loaded_hotkeys.items():
                try:
                    hotkey = int(hotkey_str)
                    skill_hotkeys[hotkey] = skill_index
                except ValueError:
                    pass
            player.skill_hotkeys = skill_hotkeys if skill_hotkeys else player.skill_hotkeys
        if hasattr(player, 'hotkey_skills'):
            loaded_hotkey_skills = player_data.get('hotkey_skills', {})
            # 将字符串类型的键转换回数字类型
            hotkey_skills = {}
            for skill_index_str, hotkey in loaded_hotkey_skills.items():
                try:
                    skill_index = int(skill_index_str)
                    hotkey_skills[skill_index] = hotkey
                except ValueError:
                    pass
            player.hotkey_skills = hotkey_skills if hotkey_skills else player.hotkey_skills
    
    def _load_game_data(self, player_data):
        """加载游戏数据"""
        game = self.game
        game.gold = player_data.get('gold', game.gold)
        game.experience = player_data.get('experience', game.experience)
        game.level = player_data.get('level', game.level)
        game.experience_to_next_level = player_data.get('experience_to_next_level', game.experience_to_next_level)
        
        # 加载地图ID
        map_id = player_data.get('map_id', 1)
        
        # 加载玩家位置
        position = player_data.get('position', {})
        player_x = position.get('x', game.player.x)
        player_y = position.get('y', game.player.y)
        
        # 切换到正确的地图
        game.map_manager.switch_map(map_id, player_x, player_y)
        
        # 更新相机位置，确保玩家在屏幕中央
        target_camera_x = game.player.x - game.width // 2
        target_camera_y = game.player.y - game.height // 2
        
        # 限制相机范围，防止超出地图
        current_map = game.map_manager.get_current_map()
        if current_map:
            game.camera_x = max(0, min(current_map.width - game.width, target_camera_x))
            game.camera_y = max(0, min(current_map.height - game.height, target_camera_y))
        else:
            game.camera_x = target_camera_x
            game.camera_y = target_camera_y
        
        print(f"加载玩家位置: ({game.player.x}, {game.player.y})")
        print(f"屏幕尺寸: ({game.width}, {game.height})")
        print(f"更新相机位置: ({game.camera_x}, {game.camera_y})")
