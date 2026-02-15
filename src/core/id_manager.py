# ID管理模块
# 为游戏中的所有元素建立统一的ID索引系统

class IDManager:
    """ID管理器"""
    
    def __init__(self):
        """初始化ID管理器"""
        # 地图ID索引
        self.map_ids = {
            1: {"name": "村庄", "scene_type": "村庄"},
            2: {"name": "森林", "scene_type": "森林"},
            3: {"name": "沙漠", "scene_type": "沙漠"},
            4: {"name": "地牢", "scene_type": "地牢"},
            5: {"name": "雪原", "scene_type": "雪原"}
        }
        
        # 职业ID索引
        self.profession_ids = {
            1: {"name": "战士", "english_name": "warrior"},
            2: {"name": "法师", "english_name": "mage"},
            3: {"name": "道士", "english_name": "taoist"}
        }
        
        # 怪物ID索引
        self.monster_ids = {
            1: {"name": "稻草人", "type": "normal", "level": 1},
            2: {"name": "鸡", "type": "normal", "level": 1},
            3: {"name": "鹿", "type": "normal", "level": 2},
            4: {"name": "狼", "type": "normal", "level": 3},
            5: {"name": "骷髅", "type": "advanced", "level": 4},
            6: {"name": "僵尸", "type": "advanced", "level": 5},
            7: {"name": "骷髅王", "type": "boss", "level": 10},
            8: {"name": "僵尸王", "type": "boss", "level": 12},
            9: {"name": "沃玛教主", "type": "boss", "level": 15},
            10: {"name": "祖玛教主", "type": "boss", "level": 20}
        }
        
        # 技能ID索引
        self.skill_ids = {
            # 战士技能
            101: {"name": "基本剑术", "profession": "战士", "level": 1},
            102: {"name": "攻杀剑术", "profession": "战士", "level": 10},
            103: {"name": "半月弯刀", "profession": "战士", "level": 15},
            104: {"name": "野蛮冲撞", "profession": "战士", "level": 20},
            105: {"name": "烈火剑法", "profession": "战士", "level": 25},
            106: {"name": "逐日剑法", "profession": "战士", "level": 30},
            107: {"name": "开天斩", "profession": "战士", "level": 35},
            
            # 法师技能
            201: {"name": "火球术", "profession": "法师", "level": 1},
            202: {"name": "闪电术", "profession": "法师", "level": 10},
            203: {"name": "地狱火", "profession": "法师", "level": 15},
            204: {"name": "冰咆哮", "profession": "法师", "level": 20},
            205: {"name": "魔法盾", "profession": "法师", "level": 25},
            206: {"name": "狂龙紫电", "profession": "法师", "level": 30},
            207: {"name": "灭天火", "profession": "法师", "level": 35},
            
            # 道士技能
            301: {"name": "灵魂火符", "profession": "道士", "level": 1},
            302: {"name": "治愈术", "profession": "道士", "level": 1},
            303: {"name": "施毒术", "profession": "道士", "level": 10},
            304: {"name": "召唤骷髅", "profession": "道士", "level": 15},
            305: {"name": "隐身术", "profession": "道士", "level": 20},
            306: {"name": "群体治愈术", "profession": "道士", "level": 25},
            307: {"name": "召唤神兽", "profession": "道士", "level": 30},
            308: {"name": "道符连击", "profession": "道士", "level": 35}
        }
        
        # 物品ID索引
        self.item_ids = {
            # 武器
            1001: {"name": "木剑", "type": "weapon", "profession": "all", "level": 1, "attack": 5, "range": 50},
            1002: {"name": "铁剑", "type": "weapon", "profession": "战士", "level": 5, "attack": 10, "range": 60},
            1003: {"name": "铜剑", "type": "weapon", "profession": "战士", "level": 10, "attack": 15, "range": 70},
            1004: {"name": "木杖", "type": "weapon", "profession": "法师", "level": 5, "attack": 3, "magic": 8, "range": 120},
            1005: {"name": "桃木剑", "type": "weapon", "profession": "道士", "level": 5, "attack": 5, "magic": 5, "range": 90},
            
            # 防具
            2001: {"name": "布衣", "type": "armor", "profession": "all", "level": 1, "defense": 2},
            2002: {"name": "铁甲", "type": "armor", "profession": "战士", "level": 5, "defense": 5},
            2003: {"name": "皮帽", "type": "helmet", "profession": "all", "level": 1, "defense": 1},
            2004: {"name": "草鞋", "type": "boots", "profession": "all", "level": 1, "defense": 1},
            
            # 药水
            3001: {"name": "金疮药", "type": "consumable", "effect": "health", "value": 20},
            3002: {"name": "魔法药", "type": "consumable", "effect": "magic", "value": 15},
            3003: {"name": "超级金疮药", "type": "consumable", "effect": "health", "value": 50},
            3004: {"name": "超级魔法药", "type": "consumable", "effect": "magic", "value": 40},
            
            # 材料
            4001: {"name": "鸡毛", "type": "material"},
            4002: {"name": "鹿角", "type": "material"},
            4003: {"name": "狼皮", "type": "material"},
            4004: {"name": "骷髅骨", "type": "material"},
            4005: {"name": "僵尸牙齿", "type": "material"},
            
            # 技能书
            5001: {"name": "攻杀剑术技能书", "type": "skill_book", "skill_id": 102},
            5002: {"name": "闪电术技能书", "type": "skill_book", "skill_id": 202},
            5003: {"name": "召唤骷髅技能书", "type": "skill_book", "skill_id": 304},
            5004: {"name": "半月弯刀技能书", "type": "skill_book", "skill_id": 103},
            5005: {"name": "魔法盾技能书", "type": "skill_book", "skill_id": 205},
            5006: {"name": "野蛮冲撞技能书", "type": "skill_book", "skill_id": 104},
            5007: {"name": "冰咆哮技能书", "type": "skill_book", "skill_id": 204},
            5008: {"name": "召唤神兽技能书", "type": "skill_book", "skill_id": 307},
            5009: {"name": "开天斩技能书", "type": "skill_book", "skill_id": 107},
            5010: {"name": "狂龙紫电技能书", "type": "skill_book", "skill_id": 206},
            5011: {"name": "道符连击技能书", "type": "skill_book", "skill_id": 308},
            
            # 材料
            4006: {"name": "腐烂的肉", "type": "material"},
            4007: {"name": "稻草人之心", "type": "material"},
            4008: {"name": "沃玛号角", "type": "material"},
            4009: {"name": "祖玛头像", "type": "material"}
        }
        
        # NPC ID索引
        self.npc_ids = {
            1: {"name": "村长", "type": "village", "function": "quest"},
            2: {"name": "武器商", "type": "village", "function": "trade"},
            3: {"name": "药店老板", "type": "village", "function": "trade"},
            4: {"name": "防具商", "type": "village", "function": "trade"},
            5: {"name": "铁匠", "type": "village", "function": "repair"},
            6: {"name": "法师", "type": "village", "function": "skill"},
            7: {"name": "牧师", "type": "village", "function": "heal"},
            8: {"name": "精灵守卫", "type": "forest", "function": "dialogue"},
            9: {"name": "德鲁伊", "type": "forest", "function": "skill"},
            10: {"name": "商队首领", "type": "desert", "function": "trade"},
            11: {"name": "沙漠向导", "type": "desert", "function": "dialogue"},
            12: {"name": "地牢守卫", "type": "dungeon", "function": "dialogue"},
            13: {"name": "黑暗法师", "type": "dungeon", "function": "skill"}
        }
    
    def get_map_by_id(self, map_id):
        """根据ID获取地图信息"""
        return self.map_ids.get(map_id)
    
    def get_profession_by_id(self, profession_id):
        """根据ID获取职业信息"""
        return self.profession_ids.get(profession_id)
    
    def get_monster_by_id(self, monster_id):
        """根据ID获取怪物信息"""
        return self.monster_ids.get(monster_id)
    
    def get_skill_by_id(self, skill_id):
        """根据ID获取技能信息"""
        return self.skill_ids.get(skill_id)
    
    def get_item_by_id(self, item_id):
        """根据ID获取物品信息"""
        return self.item_ids.get(item_id)
    
    def get_npc_by_id(self, npc_id):
        """根据ID获取NPC信息"""
        return self.npc_ids.get(npc_id)
    
    def get_map_id_by_name(self, map_name):
        """根据名称获取地图ID"""
        for id, info in self.map_ids.items():
            if info['name'] == map_name:
                return id
        return None
    
    def get_profession_id_by_name(self, profession_name):
        """根据名称获取职业ID"""
        for id, info in self.profession_ids.items():
            if info['name'] == profession_name:
                return id
        return None
    
    def get_monster_id_by_name(self, monster_name):
        """根据名称获取怪物ID"""
        for id, info in self.monster_ids.items():
            if info['name'] == monster_name:
                return id
        return None
    
    def get_skill_id_by_name(self, skill_name):
        """根据名称获取技能ID"""
        for id, info in self.skill_ids.items():
            if info['name'] == skill_name:
                return id
        return None
    
    def get_item_id_by_name(self, item_name):
        """根据名称获取物品ID"""
        for id, info in self.item_ids.items():
            if info['name'] == item_name:
                return id
        return None
    
    def get_npc_id_by_name(self, npc_name):
        """根据名称获取NPC ID"""
        for id, info in self.npc_ids.items():
            if info['name'] == npc_name:
                return id
        return None

# 创建全局ID管理器实例
id_manager = IDManager()