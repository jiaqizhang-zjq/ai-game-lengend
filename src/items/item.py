class Item:
    """物品类"""
    
    def __init__(self, name, item_type, subtype="", quantity=1, **kwargs):
        """初始化物品"""
        self.name = name
        self.type = item_type  # weapon, armor, helmet, boots, consumable, material, skill_book
        self.subtype = subtype  # recovery, equipment, material, skill
        self.quantity = quantity
        self.description = kwargs.get("description", "")
        
        # 物品属性
        self.attack = kwargs.get("attack", 0)
        self.defense = kwargs.get("defense", 0)
        self.magic = kwargs.get("magic", 0)
        self.range = kwargs.get("range", 30)  # 攻击范围
        self.required_class = kwargs.get("required_class", "all")  # 职业要求
        
        # 消耗品属性
        self.effect = kwargs.get("effect", "")  # health, magic
        self.value = kwargs.get("value", 0)  # 效果值
        
        # 技能书属性
        self.skill_name = kwargs.get("skill_name", "")  # 技能名称
        self.skill_level = kwargs.get("skill_level", 1)  # 技能等级
        self.required_profession = kwargs.get("required_profession", "all")  # 要求职业
    
    def to_dict(self):
        """转换为字典"""
        return {
            "name": self.name,
            "type": self.type,
            "subtype": self.subtype,
            "quantity": self.quantity,
            "description": self.description,
            "attack": self.attack,
            "defense": self.defense,
            "magic": self.magic,
            "range": self.range,
            "required_class": self.required_class,
            "effect": self.effect,
            "value": self.value,
            "skill_name": getattr(self, "skill_name", ""),
            "skill_level": getattr(self, "skill_level", 1),
            "required_profession": getattr(self, "required_profession", "all")
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建物品"""
        return cls(
            name=data["name"],
            item_type=data["type"],
            subtype=data.get("subtype", ""),
            quantity=data.get("quantity", 1),
            description=data.get("description", ""),
            attack=data.get("attack", 0),
            defense=data.get("defense", 0),
            magic=data.get("magic", 0),
            range=data.get("range", 30),
            required_class=data.get("required_class", "all"),
            effect=data.get("effect", ""),
            value=data.get("value", 0),
            skill_name=data.get("skill_name", ""),
            skill_level=data.get("skill_level", 1),
            required_profession=data.get("required_profession", "all")
        )


class ItemManager:
    """物品管理器"""
    
    def __init__(self):
        """初始化物品管理器"""
        self.inventory = []
        self.item_types = {
            "金疮药": {"type": "consumable", "subtype": "recovery", "effect": "health", "value": 30, "description": "恢复30点生命值"},
            "魔法药": {"type": "consumable", "subtype": "recovery", "effect": "magic", "value": 20, "description": "恢复20点魔法值"},
            "超级金疮药": {"type": "consumable", "subtype": "recovery", "effect": "health", "value": 80, "description": "恢复80点生命值"},
            "超级魔法药": {"type": "consumable", "subtype": "recovery", "effect": "magic", "value": 60, "description": "恢复60点魔法值"},
            # 基础武器
            "木剑": {"type": "weapon", "subtype": "equipment", "attack": 5, "defense": 0, "magic": 0, "range": 30, "description": "攻击力+5，攻击范围30，基础武器", "required_class": "all"},
            "铁剑": {"type": "weapon", "subtype": "equipment", "attack": 10, "defense": 0, "magic": 0, "range": 40, "description": "攻击力+10，攻击范围40，战士的常用武器", "required_class": "warrior"},
            "生锈的剑": {"type": "weapon", "subtype": "equipment", "attack": 6, "defense": 0, "magic": 0, "range": 35, "description": "攻击力+6，攻击范围35，生锈的剑", "required_class": "all"},
            # 法师武器
            "木杖": {"type": "weapon", "subtype": "equipment", "attack": 2, "defense": 0, "magic": 8, "range": 150, "description": "魔法力+8，攻击范围150，法师的基础武器", "required_class": "mage"},
            "法杖": {"type": "weapon", "subtype": "equipment", "attack": 3, "defense": 0, "magic": 15, "range": 180, "description": "魔法力+15，攻击范围180，法师的强力武器", "required_class": "mage"},
            # 道士武器
            "桃木剑": {"type": "weapon", "subtype": "equipment", "attack": 4, "defense": 0, "magic": 4, "range": 100, "description": "攻击力+4，魔法力+4，攻击范围100，道士的基础武器", "required_class": "taoist"},
            "拂尘": {"type": "weapon", "subtype": "equipment", "attack": 6, "defense": 0, "magic": 8, "range": 120, "description": "攻击力+6，魔法力+8，攻击范围120，道士的常用武器", "required_class": "taoist"},
            # 基础防具
            "布衣": {"type": "armor", "subtype": "equipment", "attack": 0, "defense": 2, "magic": 0, "description": "防御力+2，基础盔甲", "required_class": "all"},
            "铁甲": {"type": "armor", "subtype": "equipment", "attack": 0, "defense": 5, "magic": 0, "description": "防御力+5，提供良好的防护", "required_class": "warrior"},
            "皮帽": {"type": "helmet", "subtype": "equipment", "attack": 0, "defense": 1, "magic": 0, "description": "防御力+1，基础头盔", "required_class": "all"},
            "草鞋": {"type": "boots", "subtype": "equipment", "attack": 0, "defense": 1, "magic": 0, "description": "防御力+1，基础靴子", "required_class": "all"},
            # 职业防具
            "法师长袍": {"type": "armor", "subtype": "equipment", "attack": 0, "defense": 1, "magic": 5, "description": "魔法力+5，防御力+1，法师的专用防具", "required_class": "mage"},
            "道士道袍": {"type": "armor", "subtype": "equipment", "attack": 0, "defense": 2, "magic": 3, "description": "魔法力+3，防御力+2，道士的专用防具", "required_class": "taoist"},
            "战士头盔": {"type": "helmet", "subtype": "equipment", "attack": 0, "defense": 3, "magic": 0, "description": "防御力+3，战士的专用头盔", "required_class": "warrior"},
            "法师头巾": {"type": "helmet", "subtype": "equipment", "attack": 0, "defense": 1, "magic": 3, "description": "魔法力+3，防御力+1，法师的专用头巾", "required_class": "mage"},
            "道士冠": {"type": "helmet", "subtype": "equipment", "attack": 0, "defense": 2, "magic": 2, "description": "魔法力+2，防御力+2，道士的专用道冠", "required_class": "taoist"},
            "战士战靴": {"type": "boots", "subtype": "equipment", "attack": 0, "defense": 2, "magic": 0, "description": "防御力+2，战士的专用战靴", "required_class": "warrior"},
            "法师鞋": {"type": "boots", "subtype": "equipment", "attack": 0, "defense": 1, "magic": 2, "description": "魔法力+2，防御力+1，法师的专用鞋", "required_class": "mage"},
            "道士靴": {"type": "boots", "subtype": "equipment", "attack": 0, "defense": 1, "magic": 1, "description": "魔法力+1，防御力+1，道士的专用靴", "required_class": "taoist"},
            # 沙漠特有物品
            "弯刀": {"type": "weapon", "subtype": "equipment", "attack": 12, "defense": 0, "magic": 0, "range": 45, "description": "攻击力+12，攻击范围45，沙漠地区的特色武器，适合近战", "required_class": "all"},
            "沙漠之靴": {"type": "boots", "subtype": "equipment", "attack": 0, "defense": 3, "magic": 0, "description": "防御力+3，沙漠地区的特色靴子，提供良好的防护", "required_class": "all"},
            "防晒头巾": {"type": "helmet", "subtype": "equipment", "attack": 0, "defense": 2, "magic": 1, "description": "防御力+2，魔法力+1，沙漠地区的防晒头巾，同时提供防护", "required_class": "all"},
            "水袋": {"type": "consumable", "subtype": "recovery", "effect": "health", "value": 20, "description": "恢复20点生命值，沙漠中必备的补给品"},
            # 材料
            "骷髅骨": {"type": "material", "subtype": "material", "description": "任务材料，用于制作或兑换物品"},
            "僵尸牙齿": {"type": "material", "subtype": "material", "description": "任务材料，用于制作或兑换物品"},
            "狼皮": {"type": "material", "subtype": "material", "description": "任务材料，用于制作或兑换物品"},
            "腐烂的肉": {"type": "material", "subtype": "material", "description": "任务材料，用于制作或兑换物品"},
            "狼牙": {"type": "material", "subtype": "material", "description": "任务材料，用于制作或兑换物品"},
            # 其他商店物品
            "精灵之弓": {"type": "weapon", "subtype": "equipment", "attack": 8, "defense": 0, "magic": 0, "range": 200, "description": "攻击力+8，攻击范围200，精灵的传统武器，适合远程攻击", "required_class": "all"},
            "自然之戒": {"type": "ring", "subtype": "equipment", "attack": 0, "defense": 0, "magic": 5, "description": "魔法力+5，精灵制作的魔法戒指", "required_class": "all"},
            "自然药水": {"type": "consumable", "subtype": "recovery", "effect": "health", "value": 40, "description": "恢复40点生命值，精灵制作的天然药水"},
            "祝福药水": {"type": "consumable", "subtype": "recovery", "effect": "magic", "value": 30, "description": "恢复30点魔法值，带有祝福效果的药水"},
            "斧头": {"type": "weapon", "subtype": "equipment", "attack": 7, "defense": 0, "magic": 0, "range": 35, "description": "攻击力+7，攻击范围35，樵夫使用的工具，也可作为武器", "required_class": "all"},
            "柴火": {"type": "material", "subtype": "material", "description": "任务材料，用于生火或制作"},
            "丝绸": {"type": "material", "subtype": "material", "description": "贵重的布料，可用于制作高级装备"},
            "香料": {"type": "material", "subtype": "material", "description": "沙漠特产的香料，具有特殊功效"},
            "珠宝": {"type": "material", "subtype": "material", "description": "贵重的珠宝，可用于交易或制作"},
            "黑暗魔法书": {"type": "skill_book", "subtype": "skill", "skill_name": "黑暗魔法", "skill_level": 1, "required_profession": "mage", "description": "学习黑暗魔法技能，法师的高级技能"},
            "灵魂石": {"type": "material", "subtype": "material", "description": "蕴含灵魂力量的石头，用于魔法研究"},
            "诅咒卷轴": {"type": "consumable", "subtype": "scroll", "description": "带有诅咒力量的卷轴，使用后可对敌人造成伤害"},
            "短剑": {"type": "weapon", "subtype": "equipment", "attack": 9, "defense": 0, "magic": 0, "range": 30, "description": "攻击力+9，攻击范围30，盗贼常用的武器", "required_class": "all"},
            "开锁器": {"type": "material", "subtype": "tool", "description": "盗贼使用的工具，用于开锁"},
            "潜行药水": {"type": "consumable", "subtype": "scroll", "description": "使用后可增加隐蔽性，适合潜行"},
            "面包": {"type": "consumable", "subtype": "recovery", "effect": "health", "value": 10, "description": "恢复10点生命值，基础食物"},
            "烤肉": {"type": "consumable", "subtype": "recovery", "effect": "health", "value": 15, "description": "恢复15点生命值，美味的烤肉"},
            "葡萄酒": {"type": "consumable", "subtype": "recovery", "effect": "health", "value": 25, "description": "恢复25点生命值，高级饮品"},
            # 战士技能书
            "烈火剑法技能书": {"type": "skill_book", "subtype": "skill", "skill_name": "烈火剑法", "skill_level": 1, "required_profession": "warrior", "description": "学习烈火剑法技能，战士的高级攻击技能"},
            "半月弯刀技能书": {"type": "skill_book", "subtype": "skill", "skill_name": "半月弯刀", "skill_level": 1, "required_profession": "warrior", "description": "学习半月弯刀技能，战士的范围攻击技能"},
            "野蛮冲撞技能书": {"type": "skill_book", "subtype": "skill", "skill_name": "野蛮冲撞", "skill_level": 1, "required_profession": "warrior", "description": "学习野蛮冲撞技能，战士的特殊技能"},
            "开天斩技能书": {"type": "skill_book", "subtype": "skill", "skill_name": "开天斩", "skill_level": 1, "required_profession": "warrior", "description": "学习开天斩技能，战士的终极技能"},
            # 法师技能书
            "雷电术技能书": {"type": "skill_book", "subtype": "skill", "skill_name": "雷电术", "skill_level": 1, "required_profession": "mage", "description": "学习雷电术技能，法师的基础攻击技能"},
            "魔法盾技能书": {"type": "skill_book", "subtype": "skill", "skill_name": "魔法盾", "skill_level": 1, "required_profession": "mage", "description": "学习魔法盾技能，法师的防御技能"},
            "冰咆哮技能书": {"type": "skill_book", "subtype": "skill", "skill_name": "冰咆哮", "skill_level": 1, "required_profession": "mage", "description": "学习冰咆哮技能，法师的高级范围攻击技能"},
            "狂龙紫电技能书": {"type": "skill_book", "subtype": "skill", "skill_name": "狂龙紫电", "skill_level": 1, "required_profession": "mage", "description": "学习狂龙紫电技能，法师的终极技能"},
            # 道士技能书
            "召唤骷髅技能书": {"type": "skill_book", "subtype": "skill", "skill_name": "召唤骷髅", "skill_level": 1, "required_profession": "taoist", "description": "学习召唤骷髅技能，道士的召唤技能"},
            "群体治愈术技能书": {"type": "skill_book", "subtype": "skill", "skill_name": "群体治愈术", "skill_level": 1, "required_profession": "taoist", "description": "学习群体治愈术技能，道士的范围治疗技能"},
            "召唤神兽技能书": {"type": "skill_book", "subtype": "skill", "skill_name": "召唤神兽", "skill_level": 1, "required_profession": "taoist", "description": "学习召唤神兽技能，道士的高级召唤技能"},
            "道符连击技能书": {"type": "skill_book", "subtype": "skill", "skill_name": "道符连击", "skill_level": 1, "required_profession": "taoist", "description": "学习道符连击技能，道士的高级攻击技能"}
        }
    
    def add_item(self, item_name, quantity=1, item_data=None):
        """添加物品"""
        # 查找是否已有相同名称的物品
        for item in self.inventory:
            if item.name == item_name:
                item.quantity += quantity
                return
        
        # 如果提供了物品数据，使用完整数据
        if item_data:
            if isinstance(item_data, dict):
                new_item = Item.from_dict(item_data)
                new_item.quantity = quantity
            else:
                new_item = item_data
                new_item.quantity = quantity
        else:
            # 使用物品类型数据
            if item_name in self.item_types:
                item_info = self.item_types[item_name]
                new_item = Item(
                    name=item_name,
                    item_type=item_info["type"],
                    subtype=item_info.get("subtype", ""),
                    quantity=quantity,
                    description=item_info.get("description", ""),
                    attack=item_info.get("attack", 0),
                    defense=item_info.get("defense", 0),
                    magic=item_info.get("magic", 0),
                    range=item_info.get("range", 30),
                    effect=item_info.get("effect", ""),
                    value=item_info.get("value", 0),
                    skill_name=item_info.get("skill_name", ""),
                    skill_level=item_info.get("skill_level", 1),
                    required_profession=item_info.get("required_profession", "all")
                )
            else:
                # 创建基本物品
                new_item = Item(
                    name=item_name,
                    item_type="material",
                    subtype="material",
                    quantity=quantity
                )
        
        self.inventory.append(new_item)
    
    def remove_item(self, item_index, quantity=1):
        """移除物品"""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            item.quantity -= quantity
            if item.quantity <= 0:
                self.inventory.pop(item_index)
            return True
        return False
    
    def get_item(self, item_index):
        """获取物品"""
        if 0 <= item_index < len(self.inventory):
            return self.inventory[item_index]
        return None
    
    def get_inventory(self):
        """获取物品栏"""
        return self.inventory
    
    def clear_inventory(self):
        """清空物品栏"""
        self.inventory = []
    
    def get_item_count(self):
        """获取物品数量"""
        return len(self.inventory)
    
    def has_item(self, item_name):
        """检查是否有指定物品"""
        for item in self.inventory:
            if item.name == item_name and item.quantity > 0:
                return True
        return False
    
    def get_item_quantity(self, item_name):
        """获取指定物品的数量"""
        for item in self.inventory:
            if item.name == item_name:
                return item.quantity
        return 0
    
    def use_skill_book(self, item_index, player):
        """使用技能书"""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            
            # 检查是否是技能书
            if item.type != "skill_book":
                return False, "这不是技能书"
            
            # 检查职业匹配
            if item.required_profession != "all" and item.required_profession != player.profession.name:
                return False, f"这是{self._get_profession_name(item.required_profession)}的技能书，你无法使用"
            
            # 查找技能
            target_skill = None
            for skill in player.profession.skills:
                if skill['name'] == item.skill_name:
                    target_skill = skill
                    break
            
            if not target_skill:
                return False, "你还没有这个技能的基础等级"
            
            # 检查技能等级
            if target_skill['level'] >= target_skill['max_level']:
                return False, "该技能已经达到最高等级"
            
            # 升级技能
            target_skill['level'] = item.skill_level
            
            # 消耗技能书
            self.remove_item(item_index, 1)
            
            return True, f"成功学习{item.skill_name}技能，当前等级：{target_skill['level']}"
        return False, "物品不存在"
    
    def _get_profession_name(self, profession_code):
        """获取职业名称"""
        profession_names = {
            "warrior": "战士",
            "mage": "法师",
            "taoist": "道士"
        }
        return profession_names.get(profession_code, profession_code)
