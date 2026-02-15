class TradeBehavior:
    """NPC交易行为"""
    
    def __init__(self, npc):
        """初始化交易行为"""
        self.npc = npc
        self._initialize_shop_items()
    
    def _initialize_shop_items(self):
        """初始化商店物品"""
        if self.npc.has_shop:
            map_type = self.npc.map_type
            npc_type = self.npc.npc_type
            
            shop_items = {
                '村庄': {
                    '武器商': [
                        {'name': '木剑', 'price': 100, 'quantity': 1},
                        {'name': '铁剑', 'price': 300, 'quantity': 1},
                        {'name': '铜剑', 'price': 500, 'quantity': 1},
                        {'name': '金疮药', 'price': 50, 'quantity': 99},
                        {'name': '魔法药', 'price': 80, 'quantity': 99}
                    ],
                    '药店老板': [
                        {'name': '金疮药', 'price': 40, 'quantity': 99},
                        {'name': '魔法药', 'price': 70, 'quantity': 99},
                        {'name': '超级金疮药', 'price': 100, 'quantity': 99},
                        {'name': '超级魔法药', 'price': 150, 'quantity': 99}
                    ],
                    '防具商': [
                        {'name': '布衣', 'price': 150, 'quantity': 1},
                        {'name': '铁甲', 'price': 400, 'quantity': 1},
                        {'name': '铜甲', 'price': 600, 'quantity': 1},
                        {'name': '皮帽', 'price': 80, 'quantity': 1},
                        {'name': '铁头盔', 'price': 200, 'quantity': 1},
                        {'name': '草鞋', 'price': 50, 'quantity': 1},
                        {'name': '铁靴', 'price': 150, 'quantity': 1}
                    ],
                    '厨师': [
                        {'name': '面包', 'price': 10, 'quantity': 99},
                        {'name': '烤肉', 'price': 20, 'quantity': 99},
                        {'name': '葡萄酒', 'price': 50, 'quantity': 99}
                    ]
                },
                '森林': {
                    '精灵': [
                        {'name': '精灵之弓', 'price': 800, 'quantity': 1},
                        {'name': '自然之戒', 'price': 500, 'quantity': 1},
                        {'name': '自然药水', 'price': 120, 'quantity': 99}
                    ],
                    '德鲁伊': [
                        {'name': '魔法书', 'price': 600, 'quantity': 1},
                        {'name': '自然药水', 'price': 100, 'quantity': 99},
                        {'name': '祝福药水', 'price': 80, 'quantity': 99}
                    ],
                    '樵夫': [
                        {'name': '斧头', 'price': 200, 'quantity': 1},
                        {'name': '柴火', 'price': 10, 'quantity': 99}
                    ]
                },
                '沙漠': {
                    '商队首领': [
                        {'name': '弯刀', 'price': 400, 'quantity': 1},
                        {'name': '沙漠之靴', 'price': 250, 'quantity': 1},
                        {'name': '防晒头巾', 'price': 150, 'quantity': 1},
                        {'name': '魔法药', 'price': 60, 'quantity': 99},
                        {'name': '水袋', 'price': 30, 'quantity': 99}
                    ],
                    '沙漠商人': [
                        {'name': '丝绸', 'price': 300, 'quantity': 1},
                        {'name': '香料', 'price': 200, 'quantity': 99},
                        {'name': '珠宝', 'price': 500, 'quantity': 1}
                    ]
                },
                '地牢': {
                    '法师': [
                        {'name': '黑暗魔法书', 'price': 1000, 'quantity': 1},
                        {'name': '灵魂石', 'price': 200, 'quantity': 99},
                        {'name': '诅咒卷轴', 'price': 300, 'quantity': 1}
                    ],
                    '盗贼': [
                        {'name': '短剑', 'price': 250, 'quantity': 1},
                        {'name': '开锁器', 'price': 50, 'quantity': 99},
                        {'name': '潜行药水', 'price': 150, 'quantity': 99}
                    ]
                }
            }
            
            # 根据地图类型和NPC类型设置商店物品
            if map_type in shop_items:
                if npc_type in shop_items[map_type]:
                    self.npc.shop_items = shop_items[map_type][npc_type]
                    return
            
            # 默认商店物品
            self.npc.shop_items = [
                {'name': '金疮药', 'price': 50, 'quantity': 99},
                {'name': '魔法药', 'price': 80, 'quantity': 99},
                {'name': '木剑', 'price': 100, 'quantity': 1},
                {'name': '布衣', 'price': 150, 'quantity': 1}
            ]
        else:
            self.npc.shop_items = []
    
    def trade(self, player, item_name, quantity=1):
        """与玩家交易"""
        if not self.npc.has_shop:
            return False, '我没有商店'
        
        # 查找商品
        for item in self.npc.shop_items:
            if item['name'] == item_name and item['quantity'] >= quantity:
                # 计算价格
                total_price = item['price'] * quantity
                # 检查玩家是否有足够的金币
                if getattr(player, 'gold', 0) >= total_price:
                    # 扣除玩家金币
                    player.gold -= total_price
                    # 减少商品数量
                    item['quantity'] -= quantity
                    # 给玩家物品
                    if not hasattr(player, 'inventory'):
                        player.inventory = []
                    # 添加物品到玩家背包
                    for i in range(quantity):
                        player.inventory.append({'name': item_name, 'type': 'consumable' if '药' in item_name else 'weapon'})
                    return True, f'购买成功！花费了{total_price}金币'
                else:
                    return False, '金币不足'
        return False, '商品不存在或数量不足'
    
    def get_shop_items(self):
        """获取商店物品"""
        return self.npc.shop_items
