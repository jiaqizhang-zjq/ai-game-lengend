import pygame
import math
from src.items.item import ItemManager
from src.items.equipment import EquipmentManager
from src.entities.professions import ProfessionFactory


class Player:
    """玩家类"""
    
    def __init__(self, game=None,职业=None):
        """初始化玩家"""
        # 位置
        self.x, self.y = 400, 300
        
        # 速度
        self.speed = 5
        
        # 方向（0:上, 1:右, 2:下, 3:左）
        self.direction = 2
        
        # 玩家名称
        self.name = "玩家"
        
        # 动画状态
        self.animation_frame = 0
        self.animation_speed = 0.1
        # 攻击状态
        self.is_attacking = False
        self.attack_frame = 0
        self.attack_speed = 0.3
        
        # 精灵尺寸（盛大传奇风格）
        self.width = 24
        self.height = 36
        
        # 职业系统
        self.职业 = 职业 or "战士"
        
        # 根据职业设置基础属性
        if self.职业 == "战士":
            self.base_health = 120
            self.base_max_health = 120
            self.base_attack = 25
            self.base_defense = 15
            self.base_magic = 10
        elif self.职业 == "法师":
            self.base_health = 80
            self.base_max_health = 80
            self.base_attack = 15
            self.base_defense = 8
            self.base_magic = 30
        elif self.职业 == "道士":
            self.base_health = 100
            self.base_max_health = 100
            self.base_attack = 20
            self.base_defense = 12
            self.base_magic = 20
        else:
            # 默认职业
            self.base_health = 100
            self.base_max_health = 100
            self.base_attack = 20
            self.base_defense = 10
            self.base_magic = 15
        
        # 当前属性（基础属性 + 装备属性）
        self.health = self.base_health
        self.max_health = self.base_max_health
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.magic = self.base_magic
        
        # 初始化物品管理器
        self.item_manager = ItemManager()
        
        # 初始化装备管理器
        self.equipment_manager = EquipmentManager()
        
        # 技能快捷键系统
        self.skill_hotkeys = {}  # 存储技能快捷键映射 {hotkey: skill_index}
        self.hotkey_skills = {}  # 反向映射 {skill_index: hotkey}
        
        # 初始化物品栏 - 参考盛大传奇设计
        from src.core.id_manager import id_manager
        
        # 基础物品
        items_to_add = [
            (3001, 5),  # 金疮药
            (3002, 3),  # 魔法药
            (3003, 2),  # 超级金疮药
            (3004, 2),  # 超级魔法药
            (1001, 1),  # 木剑
            (2001, 1),  # 布衣
            (2002, 1),  # 铁甲
            (2003, 1),  # 皮帽
            (2004, 1),  # 草鞋
            (4004, 0),  # 骷髅骨
            (4005, 0),  # 僵尸牙齿
            (4003, 0)   # 狼皮
        ]
        
        for item_id, quantity in items_to_add:
            item_info = id_manager.get_item_by_id(item_id)
            if item_info:
                self.item_manager.add_item(item_info['name'], quantity)
        
        # 根据职业添加职业专属武器
        if self.职业 == "战士":
            item_info = id_manager.get_item_by_id(1002)  # 铁剑
            if item_info:
                self.item_manager.add_item(item_info['name'], 1)
        elif self.职业 == "法师":
            item_info = id_manager.get_item_by_id(1004)  # 木杖
            if item_info:
                self.item_manager.add_item(item_info['name'], 1)
        elif self.职业 == "道士":
            item_info = id_manager.get_item_by_id(1005)  # 桃木剑
            if item_info:
                self.item_manager.add_item(item_info['name'], 1)
        
        # 初始装备 - 根据物品名称装备
        inventory = self.item_manager.get_inventory()
        weapon_index = -1
        armor_index = -1
        helmet_index = -1
        boots_index = -1
        
        for i, item in enumerate(inventory):
            if item.name == "木剑":
                weapon_index = i
            elif item.name == "布衣":
                armor_index = i
            elif item.name == "皮帽":
                helmet_index = i
            elif item.name == "草鞋":
                boots_index = i
        
        # 装备物品
        if weapon_index != -1:
            self.equipment_manager.equip(inventory[weapon_index])
            self.item_manager.remove_item(weapon_index)
        if armor_index != -1:
            self.equipment_manager.equip(inventory[armor_index])
            self.item_manager.remove_item(armor_index)
        if helmet_index != -1:
            self.equipment_manager.equip(inventory[helmet_index])
            self.item_manager.remove_item(helmet_index)
        if boots_index != -1:
            self.equipment_manager.equip(inventory[boots_index])
            self.item_manager.remove_item(boots_index)
        
        # 地图引用
        self.map = None
        
        # 游戏引用
        self.game = game
        
        # 集成职业系统
        self.profession = ProfessionFactory.create_profession(self.职业, self)
        self.skills = self.profession.get_skills()
        self.passive_skills = self.profession.get_passive_skills()
        self.learned_skills = [skill['name'] for skill in self.skills if skill['level'] > 0]
        self.skill_cooldowns = {}
        
        # 加载精灵素材
        self.load_sprites()
        
        # 计算装备属性
        self.calculate_equipment_stats()
        
        # 显示职业信息
        self.show_profession_info()
    
    def load_sprites(self):
        """加载精灵素材"""
        # 尝试加载图片，失败则使用默认颜色
        try:
            # 加载实际的图片文件
            import os
            base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
            self.sprites = {
                "up": pygame.image.load(os.path.join(base_path, "sprites/player/player_up.png")),
                "down": pygame.image.load(os.path.join(base_path, "sprites/player/player_down.png")),
                "left": pygame.image.load(os.path.join(base_path, "sprites/player/player_left.png")),
                "right": pygame.image.load(os.path.join(base_path, "sprites/player/player_right.png"))
            }
            # 缩放到合适的游戏尺寸（48x72，符合盛大传奇风格）
            for key in self.sprites:
                self.sprites[key] = pygame.transform.scale(self.sprites[key], (48, 72))
            self.use_default_sprites = False
        except Exception as e:
            print(f"加载精灵失败: {e}")
            self.use_default_sprites = True
    
    def calculate_equipment_stats(self):
        """计算装备属性加成"""
        # 使用装备管理器计算属性
        self.attack, self.defense, self.magic = self.equipment_manager.calculate_stats(
            self.base_attack, self.base_defense, self.base_magic
        )
        
        # 确保生命值不超过最大值
        self.health = min(self.health, self.max_health)
    
    def update(self):
        """更新玩家状态"""
        # 处理键盘输入
        keys = pygame.key.get_pressed()
        
        # 移动（改为WASD键）
        moved = False
        if keys[pygame.K_w]:
            self.y -= self.speed
            self.direction = 0
            self.animation_frame += self.animation_speed
            moved = True
        elif keys[pygame.K_s]:
            self.y += self.speed
            self.direction = 2
            self.animation_frame += self.animation_speed
            moved = True
        elif keys[pygame.K_a]:
            self.x -= self.speed
            self.direction = 1  # 交换方向值
            self.animation_frame += self.animation_speed
            moved = True
        elif keys[pygame.K_d]:
            self.x += self.speed
            self.direction = 3  # 交换方向值
            self.animation_frame += self.animation_speed
            moved = True
        
        # 处理攻击动画
        if self.is_attacking:
            self.attack_frame += self.attack_speed
            if self.attack_frame >= 4:
                self.is_attacking = False
                self.attack_frame = 0
        
        # 限制位置在地图范围内
        if self.map:
            # 确保地图有宽度和高度属性
            map_width = getattr(self.map, 'width', 800)
            map_height = getattr(self.map, 'height', 600)
            # 限制玩家位置
            self.x = max(0, min(map_width - self.width, self.x))
            self.y = max(0, min(map_height - self.height, self.y))
        else:
            # 如果没有地图引用，使用默认边界
            self.x = max(0, min(800 - self.width, self.x))
            self.y = max(0, min(600 - self.height, self.y))
    
    def render(self, screen, camera_offset=(0, 0)):
        """渲染玩家（盛大传奇风格，立体效果）"""
        # 应用相机偏移
        screen_x = self.x - camera_offset[0]
        screen_y = self.y - camera_offset[1]
        
        if self.use_default_sprites:
            # 使用盛大传奇风格的立体渲染
            # 头部（盛大传奇风格，圆形样式）
            head_color = (255, 200, 200)
            pygame.draw.circle(screen, (200, 150, 150), (screen_x + 16, screen_y + 12), 4)
            pygame.draw.circle(screen, head_color, (screen_x + 16, screen_y + 12), 3)
            
            # 默认不显示装备，装备显示放到背包系统
            # 身体（立体矩形）
            body_color = (0, 100, 200)  # 布衣（默认）
            
            # 立体身体
            pygame.draw.rect(screen, body_color, (screen_x + 10, screen_y + 18, 12, 16))
            # 添加阴影效果
            pygame.draw.rect(screen, (0, 0, 0, 30), (screen_x + 10, screen_y + 18, 12, 16), 1)
            
            # 布衣纹理（默认）
            pygame.draw.line(screen, (100, 140, 200), (screen_x + 12, screen_y + 22), (screen_x + 20, screen_y + 22), 1)
            pygame.draw.line(screen, (100, 140, 200), (screen_x + 12, screen_y + 28), (screen_x + 20, screen_y + 28), 1)
            
            # 四肢（立体线条）
            limb_color = (255, 200, 200)
            
            # 攻击动画偏移量
            attack_offset = int(self.attack_frame * 2) if self.is_attacking else 0
            
            # 根据方向绘制立体四肢
            if self.direction == 0:  # 上
                # 手臂（立体效果）
                pygame.draw.line(screen, limb_color, (screen_x + 12, screen_y + 18), (screen_x + 8, screen_y + 24 - attack_offset), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 12, screen_y + 18), (screen_x + 8, screen_y + 24 - attack_offset), 1)
                pygame.draw.line(screen, limb_color, (screen_x + 20, screen_y + 18), (screen_x + 24, screen_y + 24 - attack_offset), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 20, screen_y + 18), (screen_x + 24, screen_y + 24 - attack_offset), 1)
                # 腿（立体效果）
                pygame.draw.line(screen, limb_color, (screen_x + 12, screen_y + 34), (screen_x + 12, screen_y + 40), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 12, screen_y + 34), (screen_x + 12, screen_y + 40), 1)
                pygame.draw.line(screen, limb_color, (screen_x + 20, screen_y + 34), (screen_x + 20, screen_y + 40), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 20, screen_y + 34), (screen_x + 20, screen_y + 40), 1)
            elif self.direction == 1:  # 左
                # 手臂（立体效果）
                pygame.draw.line(screen, limb_color, (screen_x + 12, screen_y + 18), (screen_x + 4 - attack_offset, screen_y + 18), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 12, screen_y + 18), (screen_x + 4 - attack_offset, screen_y + 18), 1)
                pygame.draw.line(screen, limb_color, (screen_x + 20, screen_y + 18), (screen_x + 20, screen_y + 24), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 20, screen_y + 18), (screen_x + 20, screen_y + 24), 1)
                # 腿（立体效果）
                pygame.draw.line(screen, limb_color, (screen_x + 12, screen_y + 34), (screen_x + 4 - attack_offset, screen_y + 40), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 12, screen_y + 34), (screen_x + 4 - attack_offset, screen_y + 40), 1)
                pygame.draw.line(screen, limb_color, (screen_x + 20, screen_y + 34), (screen_x + 20, screen_y + 40), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 20, screen_y + 34), (screen_x + 20, screen_y + 40), 1)
            elif self.direction == 2:  # 下
                # 手臂（立体效果）
                pygame.draw.line(screen, limb_color, (screen_x + 12, screen_y + 18), (screen_x + 8, screen_y + 24), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 12, screen_y + 18), (screen_x + 8, screen_y + 24), 1)
                pygame.draw.line(screen, limb_color, (screen_x + 20, screen_y + 18), (screen_x + 24, screen_y + 24), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 20, screen_y + 18), (screen_x + 24, screen_y + 24), 1)
                # 腿（立体效果）
                pygame.draw.line(screen, limb_color, (screen_x + 12, screen_y + 34), (screen_x + 8, screen_y + 42 + attack_offset), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 12, screen_y + 34), (screen_x + 8, screen_y + 42 + attack_offset), 1)
                pygame.draw.line(screen, limb_color, (screen_x + 20, screen_y + 34), (screen_x + 24, screen_y + 42 + attack_offset), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 20, screen_y + 34), (screen_x + 24, screen_y + 42 + attack_offset), 1)
            elif self.direction == 3:  # 右
                # 手臂（立体效果）
                pygame.draw.line(screen, limb_color, (screen_x + 20, screen_y + 18), (screen_x + 28 + attack_offset, screen_y + 18), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 20, screen_y + 18), (screen_x + 28 + attack_offset, screen_y + 18), 1)
                pygame.draw.line(screen, limb_color, (screen_x + 12, screen_y + 18), (screen_x + 12, screen_y + 24), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 12, screen_y + 18), (screen_x + 12, screen_y + 24), 1)
                # 腿（立体效果）
                pygame.draw.line(screen, limb_color, (screen_x + 12, screen_y + 34), (screen_x + 12, screen_y + 40), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 12, screen_y + 34), (screen_x + 12, screen_y + 40), 1)
                pygame.draw.line(screen, limb_color, (screen_x + 20, screen_y + 34), (screen_x + 28 + attack_offset, screen_y + 40), 3)
                pygame.draw.line(screen, (200, 150, 150), (screen_x + 20, screen_y + 34), (screen_x + 28 + attack_offset, screen_y + 40), 1)
            
            # 默认不显示武器，武器显示放到背包系统
            # 默认不显示靴子，靴子显示放到背包系统
            # 这里只显示默认的四肢

        else:
            # 使用加载的精灵图片
            direction_map = {0: "up", 1: "right", 2: "down", 3: "left"}  # 交换左右映射，使left和right素材正确对应
            direction = direction_map.get(self.direction, "down")
            sprite = self.sprites[direction]
            
            # 攻击动画效果
            if self.is_attacking:
                # 根据攻击帧和方向调整精灵位置，模拟攻击动作
                if self.direction == 0:  # 上
                    offset_y = int(self.attack_frame * -2)
                    screen.blit(sprite, (screen_x, screen_y + offset_y))
                elif self.direction == 1:  # 左
                    offset_x = int(self.attack_frame * 2)
                    screen.blit(sprite, (screen_x + offset_x, screen_y))
                elif self.direction == 2:  # 下
                    offset_y = int(self.attack_frame * 2)
                    screen.blit(sprite, (screen_x, screen_y + offset_y))
                elif self.direction == 3:  # 右
                    offset_x = int(self.attack_frame * -2)
                    screen.blit(sprite, (screen_x + offset_x, screen_y))
            else:
                # 正常状态
                screen.blit(sprite, (screen_x, screen_y))
        
        # 绘制玩家名字（盛大传奇风格，白色）
        try:
            font = pygame.font.SysFont("hiraginosansgb", 12)
        except:
            try:
                font = pygame.font.SysFont("songti", 12)
            except:
                try:
                    font = pygame.font.SysFont("arialunicode", 12)
                except:
                    font = pygame.font.Font(None, 12)
        text = font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (screen_x + 8, screen_y - 15))
        
        # 绘制血条（盛大传奇风格，立体血条）
        health_bar_width = 36
        health_ratio = self.health / self.max_health
        # 血条背景
        pygame.draw.rect(screen, (100, 100, 100), (screen_x + 4, screen_y - 12, health_bar_width + 2, 6))
        # 血条边框
        pygame.draw.rect(screen, (150, 50, 50), (screen_x + 5, screen_y - 11, health_bar_width, 4))
        # 血条填充
        pygame.draw.rect(screen, (255, 0, 0), (screen_x + 5, screen_y - 11, health_bar_width * health_ratio, 4))
    
    def take_damage(self, damage, attacker=None):
        """受到伤害"""
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage
    
    def heal(self, amount):
        """治疗"""
        self.health = min(self.max_health, self.health + amount)
    
    def add_item(self, item_identifier, quantity=1, item_data=None):
        """添加物品
        
        Args:
            item_identifier: 物品名称或物品ID
            quantity: 物品数量
            item_data: 物品数据
        """
        # 导入ID管理器
        from src.core.id_manager import id_manager
        
        # 检查是否是物品ID
        if isinstance(item_identifier, int):
            # 通过ID获取物品信息
            item_info = id_manager.get_item_by_id(item_identifier)
            if item_info:
                item_name = item_info['name']
                # 如果没有提供物品数据，使用ID管理器中的信息
                if not item_data:
                    item_data = item_info.copy()
                self.item_manager.add_item(item_name, quantity, item_data)
            else:
                print(f"物品ID不存在: {item_identifier}！")
        else:
            # 保持向后兼容，使用物品名称
            self.item_manager.add_item(item_identifier, quantity, item_data)
    
    def use_item(self, item_index):
        """使用物品"""
        item = self.item_manager.get_item(item_index)
        if item:
            item_type = item.type
            item_subtype = item.subtype
            
            if item_type == "consumable":
                if item_subtype == "recovery":
                    # 回复类物品
                    effect = item.effect
                    value = item.value
                    
                    if effect == "health":
                        # 恢复生命值
                        self.heal(value)
                        print(f"使用{item.name}，恢复了{value}点生命值！")
                    elif effect == "magic":
                        # 恢复魔法值（这里可以添加魔法值系统）
                        print(f"使用{item.name}，恢复了{value}点魔法值！")
                    
                    # 减少物品数量
                    self.item_manager.remove_item(item_index, 1)
                    return True
            elif item_type in ["weapon", "armor", "helmet", "boots"]:
                # 装备物品
                self.equip_item(item_index)
                return True
            elif item_type == "material":
                # 材料类物品
                print(f"{item.name}是材料，不能直接使用！")
                return False
            elif item_type == "skill_book":
                # 技能书
                skill_name = item.skill_name
                if skill_name:
                    if self.learn_skill(skill_name):
                        # 减少物品数量
                        self.item_manager.remove_item(item_index, 1)
                        return True
                    else:
                        return False
                else:
                    print(f"{item.name}不是有效的技能书！")
                    return False
            elif "技能书" in item.name:
                # 兼容旧版本的技能书
                # 从技能书名称中提取技能名称
                skill_name = item.name.replace("技能书", "").strip()
                if skill_name:
                    if self.learn_skill(skill_name):
                        # 减少物品数量
                        self.item_manager.remove_item(item_index, 1)
                        return True
                    else:
                        return False
                else:
                    print(f"{item.name}不是有效的技能书！")
                    return False
            else:
                # 其他物品
                print(f"{item.name}不能直接使用！")
                return False
        return False
    
    def equip_item(self, item_index):
        """装备物品"""
        item = self.item_manager.get_item(item_index)
        if item:
            item_type = item.type
            
            # 检查物品类型是否对应装备槽位
            if item_type in ["weapon", "armor", "helmet", "boots"]:
                # 检查职业限制
                required_class = getattr(item, "required_class", "all")
                
                # 转换玩家职业为英文
                class_map = {
                    "战士": "warrior",
                    "法师": "mage",
                    "道士": "taoist"
                }
                player_class = class_map.get(self.职业, "all")
                
                # 检查是否可以装备
                if required_class != "all" and required_class != player_class:
                    # 转换职业名称为中文提示
                    class_name_map = {
                        "warrior": "战士",
                        "mage": "法师",
                        "taoist": "道士"
                    }
                    required_class_name = class_name_map.get(required_class, "特定职业")
                    print(f"这件装备只能由{required_class_name}装备！")
                    return False
                
                # 将当前装备放回背包
                current_equipment = self.equipment_manager.equip(item)
                if current_equipment:
                    # 将卸下的装备放回背包
                    self.item_manager.add_item(current_equipment.name, 1, current_equipment.to_dict())
                
                # 从背包中移除物品
                self.item_manager.remove_item(item_index, 1)
                
                # 重新计算装备属性
                self.calculate_equipment_stats()
                print(f"装备了 {item.name}！")
                return True
        return False
    
    def unequip_item(self, item_type):
        """卸下装备"""
        # 从装备栏中取下装备
        unequipped_item = self.equipment_manager.unequip(item_type)
        if unequipped_item:
            # 将卸下的装备放回背包
            self.item_manager.add_item(unequipped_item.name, 1, unequipped_item.to_dict())
            
            # 重新计算装备属性
            self.calculate_equipment_stats()
            print(f"卸下了 {unequipped_item.name}！")
            return True
        return False
    
    def show_profession_info(self):
        """显示职业信息"""
        print(f"{self.职业}职业初始化:")
        print(f"  基础属性: 生命值={self.base_health}, 攻击力={self.base_attack}, 防御力={self.base_defense}, 魔法力={self.base_magic}")
        
        # 显示技能
        print("  初始技能:")
        for skill in self.skills:
            if skill.get("level", 0) > 0:
                print(f"    - {skill['name']} (等级 {skill['level']}): {skill['description']}")
        
        # 显示被动技能
        passive_skills = self.profession.get_passive_skills()
        print("  被动技能:")
        for passive in passive_skills:
            if passive.get("level", 0) > 0:
                print(f"    - {passive['name']} (等级 {passive['level']}): {passive['description']}")
        
        print("技能使用提示: 按1、2、3键使用对应技能！")
    
    def collides_with(self, other):
        """检测是否与其他游戏元素碰撞"""
        # 玩家的碰撞盒（根据新的大小调整）
        self_size = 16
        self_rect = pygame.Rect(self.x + 4, self.y + 6, self_size, self_size)
        
        # 为其他元素设置合适的碰撞盒
        if hasattr(other, 'name'):
            if other.name in ['狼', '僵尸', '骷髅']:
                # 较大的怪物
                other_size = 20
                other_rect = pygame.Rect(other.x + 5, other.y + 5, other_size, other_size)
            elif other.name in ['稻草人', '鸡', '鹿']:
                # 较小的怪物
                other_size = 16
                other_rect = pygame.Rect(other.x + 4, other.y + 4, other_size, other_size)
            else:
                # 默认大小
                other_size = 20
                other_rect = pygame.Rect(other.x + 4, other.y + 4, other_size, other_size)
        else:
            # 默认大小
            other_size = 20
            other_rect = pygame.Rect(other.x + 4, other.y + 4, other_size, other_size)
        
        return self_rect.colliderect(other_rect)
    
    def initialize_skills(self):
        """根据职业初始化技能"""
        # 使用职业系统的技能
        self.skills = self.profession.get_skills()
        self.learned_skills = [skill['name'] for skill in self.skills if skill['level'] > 0]
    
    def learn_skill(self, skill_name):
        """学习技能"""
        for skill in self.skills:
            if skill["name"] == skill_name:
                if skill.get("required_level", 1) <= getattr(self.game, "level", 1):
                    if skill_name not in self.learned_skills:
                        self.learned_skills.append(skill_name)
                        skill["level"] = 1
                        print(f"学会了技能: {skill_name}！")
                        return True
                    else:
                        print(f"已经学会了技能: {skill_name}！")
                        return False
                else:
                    print(f"等级不足，无法学习技能: {skill_name}！")
                    return False
        print(f"技能不存在: {skill_name}！")
        return False
    
    def use_skill(self, skill_name, target=None):
        """使用技能"""
        try:
            import pygame
            current_time = pygame.time.get_ticks()
            
            # 触发攻击动画
            self.is_attacking = True
            self.attack_frame = 0
            
            # 检查技能是否已学习
            if skill_name not in self.learned_skills:
                print(f"还没有学会技能: {skill_name}！")
                return False
            
            # 找到技能
            skill = None
            for s in self.skills:
                if s["name"] == skill_name:
                    skill = s
                    break
            
            if not skill:
                print(f"技能不存在: {skill_name}！")
                return False
            
            # 检查冷却时间
            cooldown = skill.get("cooldown", 1000)
            if skill_name in self.skill_cooldowns:
                last_used = self.skill_cooldowns[skill_name]
                # 检查last_used是否是相对时间（小于10000），如果是则转换为绝对时间
                if last_used < 10000:
                    # 相对时间，转换为绝对时间
                    last_used = current_time - last_used
                    self.skill_cooldowns[skill_name] = last_used
                
                if current_time - last_used < cooldown:
                    print(f"技能{skill_name}还在冷却中！")
                    return False
            
            # 创建技能动画
            if hasattr(self.game, 'animation_manager') and self.game.animation_manager:
                animation_name = skill.get('animation', skill_name)
                try:
                    if target:
                        # 根据怪物类型调整目标中心点
                        if hasattr(target, 'name'):
                            if target.name in ['狼', '僵尸', '骷髅']:
                                target_center_x = target.x + 15
                                target_center_y = target.y + 15
                            elif target.name in ['稻草人', '鸡', '鹿']:
                                target_center_x = target.x + 12
                                target_center_y = target.y + 12
                            else:
                                target_center_x = target.x + 14
                                target_center_y = target.y + 14
                        else:
                            target_center_x = target.x + 14
                            target_center_y = target.y + 14
                        
                        self.game.animation_manager.create_skill_animation(
                            animation_name, 
                            self.x + 24, 
                            self.y + 32, 
                            target_center_x, 
                            target_center_y,
                            self.direction,
                            target=target
                        )
                    else:
                        self.game.animation_manager.create_skill_animation(
                            animation_name, 
                            self.x + 24, 
                            self.y + 32,
                            direction=self.direction
                        )
                except Exception as e:
                    print(f"创建技能动画失败: {e}")
            
            # 使用技能
            if "damage" in skill:
                # 攻击技能
                # 获取技能攻击范围
                skill_range = skill.get("range", 100)
                
                if target:
                    # 检查目标是否在技能范围内
                    # 使用中心点计算距离
                    # 使用与get_monsters_near_player一致的计算方式
                    player_center_x = self.x + self.width // 2
                    player_center_y = self.y + self.height // 2
                    
                    # 计算怪物中心点（根据怪物类型调整尺寸）
                    if hasattr(target, 'name'):
                        if target.name in ['狼', '僵尸', '骷髅']:
                            monster_width, monster_height = 36, 36
                        elif target.name in ['稻草人', '鸡', '鹿']:
                            monster_width, monster_height = 28, 28
                        else:
                            monster_width, monster_height = 32, 32
                    else:
                        monster_width, monster_height = 32, 32
                    
                    monster_center_x = target.x + monster_width // 2
                    monster_center_y = target.y + monster_height // 2
                    
                    dx = player_center_x - monster_center_x
                    dy = player_center_y - monster_center_y
                    distance = math.sqrt(dx**2 + dy**2)
                    
                    if distance > skill_range:
                        print(f"目标太远了！{skill_name}的攻击范围是{skill_range}，当前距离是{int(distance)}")
                        return False
                    
                    # 根据伤害类型计算伤害
                    damage_type = skill.get("damage_type", "attack")
                    if damage_type == "magic":
                        damage = int(self.magic * skill["damage"])
                    elif damage_type == "mixed":
                        damage = int((self.attack + self.magic) // 2 * skill["damage"])
                    else:  # attack
                        damage = int(self.attack * skill["damage"])
                    
                    actual_damage = target.take_damage(damage)
                    print(f"使用{skill_name}，对{target.name}造成{actual_damage}点伤害！")
                    
                    # 显示伤害值
                    if self.game and hasattr(self.game, 'ui') and hasattr(self.game.ui, 'add_damage_text'):
                        # 计算伤害值显示的位置（目标的位置）
                        damage_x = target.x + 16  # 目标中心位置
                        damage_y = target.y + 16
                        # 技能伤害更容易触发暴击（20%概率）
                        import random
                        is_critical = random.random() < 0.2
                        self.game.ui.add_damage_text(actual_damage, damage_x, damage_y, is_critical)
                    
                    # 检查怪物是否死亡
                    if target.is_dead():
                        # 给予经验和金币
                        exp = getattr(target, 'exp', 10)
                        gold = getattr(target, 'gold', 5)
                        
                        # 添加经验和金币
                        if self.game:
                            if hasattr(self.game, 'add_exp'):
                                self.game.add_exp(exp)
                            self.game.gold += gold
                        
                        # 处理物品掉落
                        dropped_items = []
                        if hasattr(target, "drop_items"):
                            import random
                            from src.core.id_manager import id_manager
                            for item in target.drop_items:
                                if random.random() < item.get("chance", 0):
                                    # 物品掉落
                                    if "item_id" in item:
                                        # 使用物品ID
                                        item_id = item["item_id"]
                                        quantity = item.get("quantity", 1)
                                        item_info = id_manager.get_item_by_id(item_id)
                                        if item_info:
                                            item_name = item_info["name"]
                                            self.add_item(item_id, quantity)
                                            dropped_items.append(f"{item_name}×{quantity}")
                                            
                                            # 添加掉落物品提示
                                            if hasattr(self, 'game') and hasattr(self.game, "ui") and hasattr(self.game.ui, "add_item_drop"):
                                                self.game.ui.add_item_drop(item_name, quantity, target.x, target.y)
                                    else:
                                        # 保持向后兼容，使用物品名称
                                        item_name = item["name"]
                                        quantity = item.get("quantity", 1)
                                        self.add_item(item_name, quantity)
                                        dropped_items.append(f"{item_name}×{quantity}")
                                        
                                        # 添加掉落物品提示
                                        if hasattr(self, 'game') and hasattr(self.game, "ui") and hasattr(self.game.ui, "add_item_drop"):
                                            self.game.ui.add_item_drop(item_name, quantity, target.x, target.y)
                        
                        # 显示掉落信息
                        if dropped_items:
                            drop_info = "，".join(dropped_items)
                            print(f"杀死了{target.name}，获得{exp}经验、{gold}金币和物品：{drop_info}！")
                        else:
                            print(f"杀死了{target.name}，获得{exp}经验和{gold}金币！")
                else:
                    # 范围攻击
                    current_map = None
                    if self.map:
                        current_map = self.map
                    elif self.game and hasattr(self.game, 'map_manager'):
                        current_map = self.game.map_manager.get_current_map()
                    
                    if current_map:
                        # 使用技能的攻击范围
                        near_monsters = current_map.get_monsters_near_player(self, distance=skill_range)
                        
                        if not near_monsters:
                            print(f"范围内没有怪物！{skill_name}的攻击范围是{skill_range}")
                            # 打印所有怪物的位置，用于调试
                            print(f"地图上的怪物数量: {len(current_map.monsters)}")
                            for i, monster in enumerate(current_map.monsters):
                                if not monster.is_dead():
                                    dx = self.x - monster.x
                                    dy = self.y - monster.y
                                    distance = math.sqrt(dx**2 + dy**2)
                                    print(f"怪物 {i}: {monster.name} 在 ({monster.x}, {monster.y}), 距离: {int(distance)}")
                        else:
                            # 根据伤害类型计算伤害
                            damage_type = skill.get("damage_type", "attack")
                            for monster in near_monsters:
                                if damage_type == "magic":
                                    damage = int(self.magic * skill["damage"])
                                elif damage_type == "mixed":
                                    damage = int((self.attack + self.magic) // 2 * skill["damage"])
                                else:  # attack
                                    damage = int(self.attack * skill["damage"])
                                
                                actual_damage = monster.take_damage(damage)
                                print(f"使用{skill_name}，对{monster.name}造成{actual_damage}点伤害！")
                                
                                # 显示伤害值
                                if self.game and hasattr(self.game, 'ui') and hasattr(self.game.ui, 'add_damage_text'):
                                    # 计算伤害值显示的位置（怪物的位置）
                                    damage_x = monster.x + 16  # 怪物中心位置
                                    damage_y = monster.y + 16
                                    # 技能伤害更容易触发暴击（20%概率）
                                    import random
                                    is_critical = random.random() < 0.2
                                    self.game.ui.add_damage_text(actual_damage, damage_x, damage_y, is_critical)
                                
                                # 检查怪物是否死亡
                                if monster.is_dead():
                                    # 给予经验和金币
                                    exp = getattr(monster, 'exp', 10)
                                    gold = getattr(monster, 'gold', 5)
                                    
                                    # 添加经验和金币
                                    if self.game:
                                        if hasattr(self.game, 'add_exp'):
                                            self.game.add_exp(exp)
                                        self.game.gold += gold
                                    
                                    # 处理物品掉落
                                    dropped_items = []
                                    if hasattr(monster, "drop_items"):
                                        import random
                                        from src.core.id_manager import id_manager
                                        for item in monster.drop_items:
                                            if random.random() < item.get("chance", 0):
                                                # 物品掉落
                                                if "item_id" in item:
                                                    # 使用物品ID
                                                    item_id = item["item_id"]
                                                    quantity = item.get("quantity", 1)
                                                    item_info = id_manager.get_item_by_id(item_id)
                                                    if item_info:
                                                        item_name = item_info["name"]
                                                        self.add_item(item_id, quantity)
                                                        dropped_items.append(f"{item_name}×{quantity}")
                                                        
                                                        # 添加掉落物品提示
                                                        if hasattr(self, 'game') and hasattr(self.game, "ui") and hasattr(self.game.ui, "add_item_drop"):
                                                            self.game.ui.add_item_drop(item_name, quantity, monster.x, monster.y)
                                                else:
                                                    # 保持向后兼容，使用物品名称
                                                    item_name = item["name"]
                                                    quantity = item.get("quantity", 1)
                                                    self.add_item(item_name, quantity)
                                                    dropped_items.append(f"{item_name}×{quantity}")
                                                    
                                                    # 添加掉落物品提示
                                                    if hasattr(self, 'game') and hasattr(self.game, "ui") and hasattr(self.game.ui, "add_item_drop"):
                                                        self.game.ui.add_item_drop(item_name, quantity, monster.x, monster.y)
                                    
                                    # 显示掉落信息
                                    if dropped_items:
                                        drop_info = "，".join(dropped_items)
                                        print(f"杀死了{monster.name}，获得{exp}经验、{gold}金币和物品：{drop_info}！")
                                    else:
                                        print(f"杀死了{monster.name}，获得{exp}经验和{gold}金币！")
                    else:
                        print(f"无法获取当前地图！{skill_name}无法使用范围攻击")
            elif "heal" in skill:
                # 治疗技能
                heal_amount = skill["heal"] + int(self.magic * 0.5)
                self.heal(heal_amount)
                print(f"使用{skill_name}，恢复了{heal_amount}点生命值！")
            elif skill_name == "召唤骷髅" or skill_name == "召唤神兽":
                # 召唤技能
                print(f"使用{skill_name}，召唤出一个助手协助战斗！")
                # 这里可以添加召唤的具体逻辑
            
            # 设置冷却时间
            self.skill_cooldowns[skill_name] = current_time
            return True
        except Exception as e:
            print(f"使用技能时出错: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def update_skills(self):
        """更新技能状态"""
        # 这里可以添加技能效果的持续时间管理等
        pass
    
    def attack_monsters(self, map):
        """攻击附近的怪物"""
        # 根据职业使用不同的攻击逻辑
        if self.职业 == "法师":
            # 法师：远程魔法攻击
            attack_range = 150  # 法师攻击范围更大
            damage_base = self.magic  # 法师使用魔法值计算伤害
            attack_type = "魔法攻击"
        elif self.职业 == "道士":
            # 道士：中距离攻击，使用魔法
            attack_range = 100  # 道士攻击范围适中
            damage_base = (self.attack + self.magic) // 2  # 道士平衡攻击和魔法
            attack_type = "道术攻击"
        else:
            # 战士：近战物理攻击
            attack_range = self.equipment_manager.get_weapon_range()
            damage_base = self.attack
            attack_type = "物理攻击"
        
        # 找到附近的怪物
        near_monsters = map.get_monsters_near_player(self, distance=attack_range)
        
        if near_monsters:
            # 攻击第一个怪物
            target_monster = near_monsters[0]
            print(f"攻击怪物: {target_monster.name}, 攻击范围: {attack_range}, 基础伤害: {damage_base}")
            self._attack_target(target_monster, damage_base, attack_type)
        else:
            print(f"附近没有怪物可以攻击！攻击范围: {attack_range}, 当前位置: ({self.x}, {self.y})")
            # 打印所有怪物的位置，用于调试
            print(f"地图上的怪物数量: {len(map.monsters)}")
            for i, monster in enumerate(map.monsters):
                if not monster.is_dead():
                    dx = self.x - monster.x
                    dy = self.y - monster.y
                    distance = math.sqrt(dx**2 + dy**2)
                    print(f"怪物 {i}: {monster.name} 在 ({monster.x}, {monster.y}), 距离: {int(distance)}")
    
    def attack_monster(self, target_monster):
        """攻击指定的怪物"""
        if not target_monster:
            print("请先选择攻击目标！")
            return
        
        # 触发攻击动画
        self.is_attacking = True
        self.attack_frame = 0
        
        # 计算攻击范围
        if self.职业 == "法师":
            # 法师：远程魔法攻击
            attack_range = 150  # 法师攻击范围更大
            damage_base = self.magic  # 法师使用魔法值计算伤害
            attack_type = "魔法攻击"
        elif self.职业 == "道士":
            # 道士：中距离攻击，使用魔法
            attack_range = 100  # 道士攻击范围适中
            damage_base = (self.attack + self.magic) // 2  # 道士平衡攻击和魔法
            attack_type = "道术攻击"
        else:
            # 战士：近战物理攻击
            attack_range = self.equipment_manager.get_weapon_range()
            damage_base = self.attack
            attack_type = "物理攻击"
        
        # 检查怪物是否在攻击范围内
        # 使用中心点计算距离
        player_center_x = self.x + self.width // 2
        player_center_y = self.y + self.height // 2
        
        # 计算怪物中心点（根据怪物类型调整尺寸）
        if hasattr(target_monster, 'name'):
            if target_monster.name in ['狼', '僵尸', '骷髅']:
                monster_width, monster_height = 30, 30
            elif target_monster.name in ['稻草人', '鸡', '鹿']:
                monster_width, monster_height = 24, 24
            else:
                monster_width, monster_height = 28, 28
        else:
            monster_width, monster_height = 28, 28
        
        monster_center_x = target_monster.x + monster_width // 2
        monster_center_y = target_monster.y + monster_height // 2
        
        dx = player_center_x - monster_center_x
        dy = player_center_y - monster_center_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > attack_range:
            print(f"目标太远了！{self.职业}的攻击范围是{attack_range}，当前距离是{int(distance)}")
            return
        
        # 攻击目标怪物
        self._attack_target(target_monster, damage_base, attack_type)
    
    def _attack_target(self, target_monster, damage_base, attack_type):
        """攻击目标怪物的内部方法"""
        # 计算伤害
        damage = damage_base
        print(f"攻击目标: {target_monster.name}, 基础伤害: {damage}, 怪物防御: {target_monster.defense}")
        actual_damage = target_monster.take_damage(damage)
        print(f"实际伤害: {actual_damage}, 怪物当前生命值: {target_monster.health}/{target_monster.max_health}")
        
        # 显示伤害值
        if self.game and hasattr(self.game, 'ui') and hasattr(self.game.ui, 'add_damage_text'):
            # 计算伤害值显示的位置（怪物的位置）
            damage_x = target_monster.x + 16  # 怪物中心位置
            damage_y = target_monster.y + 16
            # 随机判断是否为暴击（10%概率）
            import random
            is_critical = random.random() < 0.1
            self.game.ui.add_damage_text(actual_damage, damage_x, damage_y, is_critical)
        
        # 检查怪物是否死亡
        if target_monster.is_dead():
            # 给予经验和金币
            exp = target_monster.exp
            gold = target_monster.gold
            
            # 添加经验和金币
            if self.game:
                self.game.experience += exp
                self.game.gold += gold
                
                # 更新任务进度
                if hasattr(self.game, "quest_system"):
                    self.game.quest_system.update_quest_progress("kill", target_monster.name)
            
            # 处理物品掉落
            dropped_items = []
            if hasattr(target_monster, "drop_items"):
                import random
                from src.core.id_manager import id_manager
                for item in target_monster.drop_items:
                    if random.random() < item.get("chance", 0):
                        # 物品掉落
                        if "item_id" in item:
                            # 使用物品ID
                            item_id = item["item_id"]
                            quantity = item.get("quantity", 1)
                            item_info = id_manager.get_item_by_id(item_id)
                            if item_info:
                                item_name = item_info["name"]
                                self.add_item(item_id, quantity)
                                dropped_items.append(f"{item_name}×{quantity}")
                                
                                # 添加掉落物品提示
                                if self.game and hasattr(self.game, "ui") and hasattr(self.game.ui, "add_item_drop"):
                                    self.game.ui.add_item_drop(item_name, quantity, target_monster.x, target_monster.y)
                        else:
                            # 保持向后兼容，使用物品名称
                            item_name = item["name"]
                            quantity = item.get("quantity", 1)
                            self.add_item(item_name, quantity)
                            dropped_items.append(f"{item_name}×{quantity}")
                            
                            # 添加掉落物品提示
                            if self.game and hasattr(self.game, "ui") and hasattr(self.game.ui, "add_item_drop"):
                                self.game.ui.add_item_drop(item_name, quantity, target_monster.x, target_monster.y)
            
            # 显示掉落信息
            if dropped_items:
                drop_info = "，".join(dropped_items)
                print(f"杀死了{target_monster.name}，获得{exp}经验、{gold}金币和物品：{drop_info}！")
            else:
                print(f"杀死了{target_monster.name}，获得{exp}经验和{gold}金币！")
        else:
            pass
    
    def set_skill_hotkey(self, skill_index, hotkey):
        """设置技能快捷键
        
        Args:
            skill_index: 技能索引
            hotkey: 快捷键（1-10）
        """
        if not hasattr(self, 'skills'):
            return False
        
        if 0 <= skill_index < len(self.skills):
            skill = self.skills[skill_index]
            skill_name = skill['name']
            
            # 检查快捷键是否已被其他技能使用
            if hasattr(self, 'skill_hotkeys') and hotkey in self.skill_hotkeys:
                # 移除旧的映射
                old_skill_index = self.skill_hotkeys[hotkey]
                if hasattr(self, 'hotkey_skills') and old_skill_index in self.hotkey_skills:
                    del self.hotkey_skills[old_skill_index]
            
            # 初始化快捷键映射字典
            if not hasattr(self, 'skill_hotkeys'):
                self.skill_hotkeys = {}
            if not hasattr(self, 'hotkey_skills'):
                self.hotkey_skills = {}
            
            # 设置新的映射
            self.skill_hotkeys[hotkey] = skill_index
            self.hotkey_skills[skill_index] = hotkey
            
            print(f"已设置{skill_name}的快捷键为{hotkey}")
            return True
        return False
    
    def use_skill_by_hotkey(self, hotkey):
        """通过快捷键使用技能
        
        Args:
            hotkey: 快捷键（1-10）
            
        Returns:
            bool: 技能是否成功使用
        """
        if not hasattr(self, 'skill_hotkeys') or hotkey not in self.skill_hotkeys:
            return False
        
        skill_index = self.skill_hotkeys[hotkey]
        if 0 <= skill_index < len(self.skills):
            skill = self.skills[skill_index]
            skill_name = skill['name']
            
            # 尝试自动找到目标
            target = None
            current_map = None
            if hasattr(self, 'game') and hasattr(self.game, 'map_manager'):
                current_map = self.game.map_manager.get_current_map()
            
            if current_map:
                # 使用技能的攻击范围找到最近的怪物作为目标
                skill_range = skill.get('range', 100)
                near_monsters = current_map.get_monsters_near_player(self, distance=skill_range)
                if near_monsters:
                    target = near_monsters[0]
            
            # 使用技能
            return self.use_skill(skill_name, target)
        return False
    
    def attack_monsters(self, map):
        """攻击附近的怪物"""
        # 根据职业使用不同的攻击逻辑
        if self.职业 == "法师":
            # 法师：远程魔法攻击
            attack_range = 150  # 法师攻击范围更大
            damage_base = self.magic  # 法师使用魔法值计算伤害
            attack_type = "魔法攻击"
        elif self.职业 == "道士":
            # 道士：中距离攻击，使用魔法
            attack_range = 100  # 道士攻击范围适中
            damage_base = (self.attack + self.magic) // 2  # 道士平衡攻击和魔法
            attack_type = "道术攻击"
        else:
            # 战士：近战物理攻击
            attack_range = self.equipment_manager.get_weapon_range()
            damage_base = self.attack
            attack_type = "物理攻击"
        
        # 找到附近的怪物
        near_monsters = map.get_monsters_near_player(self, distance=attack_range)
        
        if near_monsters:
            # 攻击第一个怪物
            target_monster = near_monsters[0]
            print(f"攻击怪物: {target_monster.name}, 攻击范围: {attack_range}, 基础伤害: {damage_base}")
            self._attack_target(target_monster, damage_base, attack_type)
        else:
            print(f"附近没有怪物可以攻击！攻击范围: {attack_range}, 当前位置: ({self.x}, {self.y})")
            # 打印所有怪物的位置，用于调试
            print(f"地图上的怪物数量: {len(map.monsters)}")
            for i, monster in enumerate(map.monsters):
                if not monster.is_dead():
                    dx = self.x - monster.x
                    dy = self.y - monster.y
                    distance = math.sqrt(dx**2 + dy**2)
                    print(f"怪物 {i}: {monster.name} 在 ({monster.x}, {monster.y}), 距离: {int(distance)}")
    
    def _attack_target(self, target_monster, damage_base, attack_type):
        """攻击目标怪物"""
        # 计算实际伤害（考虑怪物防御）
        if hasattr(target_monster, "defense"):
            actual_damage = max(1, damage_base - target_monster.defense)
        else:
            actual_damage = damage_base
        
        # 造成伤害
        if hasattr(target_monster, "take_damage"):
            actual_damage = target_monster.take_damage(actual_damage)
        
        # 显示攻击信息
        print(f"{attack_type}了{target_monster.name}，造成{actual_damage}点伤害！")
        
        # 显示伤害值
        if hasattr(self, 'game') and hasattr(self.game, 'ui') and hasattr(self.game.ui, 'add_damage_text'):
            # 计算伤害值显示的位置（目标的位置）
            damage_x = target_monster.x + 16  # 目标中心位置
            damage_y = target_monster.y + 16
            # 普通攻击暴击率较低（5%概率）
            import random
            is_critical = random.random() < 0.05
            self.game.ui.add_damage_text(actual_damage, damage_x, damage_y, is_critical)
        
        # 检查怪物是否死亡
        if hasattr(target_monster, "is_dead") and target_monster.is_dead():
            # 处理怪物死亡
            exp = getattr(target_monster, "exp", 10)
            gold = getattr(target_monster, "gold", 5)
            
            # 增加经验和金币
            if hasattr(self, 'game') and hasattr(self.game, 'add_exp'):
                self.game.add_exp(exp)
                self.game.gold += gold
            
            # 处理物品掉落
            dropped_items = []
            if hasattr(target_monster, "drop_items"):
                import random
                from src.core.id_manager import id_manager
                for item in target_monster.drop_items:
                    if random.random() < item.get("chance", 0):
                        # 物品掉落
                        if "item_id" in item:
                            # 使用物品ID
                            item_id = item["item_id"]
                            quantity = item.get("quantity", 1)
                            item_info = id_manager.get_item_by_id(item_id)
                            if item_info:
                                item_name = item_info["name"]
                                self.add_item(item_id, quantity)
                                dropped_items.append(f"{item_name}×{quantity}")
                                
                                # 添加掉落物品提示
                                if hasattr(self, 'game') and hasattr(self.game, "ui") and hasattr(self.game.ui, "add_item_drop"):
                                    self.game.ui.add_item_drop(item_name, quantity, target_monster.x, target_monster.y)
                        else:
                            # 保持向后兼容，使用物品名称
                            item_name = item["name"]
                            quantity = item.get("quantity", 1)
                            self.add_item(item_name, quantity)
                            dropped_items.append(f"{item_name}×{quantity}")
                            
                            # 添加掉落物品提示
                            if hasattr(self, 'game') and hasattr(self.game, "ui") and hasattr(self.game.ui, "add_item_drop"):
                                self.game.ui.add_item_drop(item_name, quantity, target_monster.x, target_monster.y)
            
            # 显示掉落信息
            if dropped_items:
                drop_info = "，".join(dropped_items)
                print(f"杀死了{target_monster.name}，获得{exp}经验、{gold}金币和物品：{drop_info}！")
            else:
                print(f"杀死了{target_monster.name}，获得{exp}经验和{gold}金币！")
        else:
            print(f"{attack_type}了{target_monster.name}，造成{actual_damage}点伤害！")
