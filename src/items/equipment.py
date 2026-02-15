class Equipment:
    """装备类"""
    
    def __init__(self, name, equipment_type, attack=0, defense=0, magic=0, range=30, description=""):
        """初始化装备"""
        self.name = name
        self.type = equipment_type  # weapon, armor, helmet, boots
        self.attack = attack
        self.defense = defense
        self.magic = magic
        self.range = range  # 攻击范围
        self.description = description
    
    def to_dict(self):
        """转换为字典"""
        return {
            "name": self.name,
            "type": self.type,
            "attack": self.attack,
            "defense": self.defense,
            "magic": self.magic,
            "range": self.range,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建装备"""
        return cls(
            name=data["name"],
            equipment_type=data["type"],
            attack=data.get("attack", 0),
            defense=data.get("defense", 0),
            magic=data.get("magic", 0),
            range=data.get("range", 30),
            description=data.get("description", "")
        )


class EquipmentManager:
    """装备管理器"""
    
    def __init__(self):
        """初始化装备管理器"""
        # 装备槽位
        self.slots = {
            "weapon": None,   # 武器
            "armor": None,    # 盔甲
            "helmet": None,   # 头盔
            "boots": None     # 靴子
        }
    
    def equip(self, item):
        """装备物品"""
        if item.type in self.slots:
            # 获取当前装备
            current_equipment = self.slots[item.type]
            
            # 创建装备实例
            equipment = Equipment(
                name=item.name,
                equipment_type=item.type,
                attack=item.attack,
                defense=item.defense,
                magic=item.magic,
                range=item.range,
                description=item.description
            )
            
            # 装备新物品
            self.slots[item.type] = equipment
            
            # 返回旧装备
            return current_equipment
        return None
    
    def unequip(self, slot_type):
        """卸下装备"""
        if slot_type in self.slots:
            equipment = self.slots[slot_type]
            self.slots[slot_type] = None
            return equipment
        return None
    
    def get_equipment(self, slot_type):
        """获取装备"""
        return self.slots.get(slot_type, None)
    
    def get_equipped_item(self, slot_type):
        """获取已装备的物品"""
        return self.get_equipment(slot_type)
    
    def get_all_equipment(self):
        """获取所有装备"""
        return self.slots
    
    def calculate_stats(self, base_attack, base_defense, base_magic):
        """计算装备属性加成"""
        attack = base_attack
        defense = base_defense
        magic = base_magic
        
        for slot, equipment in self.slots.items():
            if equipment:
                attack += equipment.attack
                defense += equipment.defense
                magic += equipment.magic
        
        return attack, defense, magic
    
    def get_weapon_range(self):
        """获取武器攻击范围"""
        weapon = self.slots.get("weapon")
        if weapon:
            return weapon.range
        return 60  # 默认攻击范围
    
    def has_equipment(self, slot_type):
        """检查是否有装备"""
        return self.slots.get(slot_type, None) is not None
    
    def clear_all(self):
        """清空所有装备"""
        for slot in self.slots:
            self.slots[slot] = None
    
    def to_dict(self):
        """转换为字典"""
        equipment_dict = {}
        for slot, equipment in self.slots.items():
            if equipment:
                equipment_dict[slot] = equipment.to_dict()
            else:
                equipment_dict[slot] = None
        return equipment_dict
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建装备管理器"""
        manager = cls()
        for slot, equipment_data in data.items():
            if equipment_data:
                manager.slots[slot] = Equipment.from_dict(equipment_data)
        return manager
