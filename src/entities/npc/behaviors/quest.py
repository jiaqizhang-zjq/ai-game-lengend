class QuestBehavior:
    """NPC任务行为"""
    
    def __init__(self, npc):
        """初始化任务行为"""
        self.npc = npc
    
    def give_quest(self, player):
        """给予任务"""
        # 根据地图类型和NPC类型生成不同的任务
        quests = self._get_quests()
        
        # 筛选玩家等级可以接受的任务
        player_level = getattr(player, 'level', 1)
        suitable_quests = [quest for quest in quests if quest['level_requirement'] <= player_level]
        
        if suitable_quests:
            # 优先选择等级要求最接近玩家等级的任务
            suitable_quests.sort(key=lambda x: x['level_requirement'], reverse=True)
            return suitable_quests[0]
        
        # 默认任务
        return {
            'title': '探索世界',
            'description': '勇敢地探索这个世界，变得更加强大。',
            'reward': {'exp': 50, 'gold': 100, 'items': ['金疮药']},
            'level_requirement': 1,
            'type': 'exploration'
        }
    
    def _get_quests(self):
        """获取任务列表"""
        map_type = self.npc.map_type
        npc_type = self.npc.npc_type
        
        quests = {
            '村庄': {
                '村长': [
                    {
                        'title': '消灭附近的怪物',
                        'description': '村庄附近的怪物越来越多，威胁到了村民的安全。请消灭10只怪物。',
                        'reward': {'exp': 100, 'gold': 500, 'items': ['铁剑']},
                        'level_requirement': 1,
                        'type': 'combat'
                    },
                    {
                        'title': '保护村庄',
                        'description': '村庄即将遭受怪物袭击，请做好准备保护村民。',
                        'reward': {'exp': 200, 'gold': 1000, 'items': ['铁甲', '金疮药']},
                        'level_requirement': 10,
                        'type': 'defense'
                    }
                ],
                '武器商': [
                    {
                        'title': '收集铁矿石',
                        'description': '我需要一些铁矿石来打造武器。请收集10块铁矿石。',
                        'reward': {'exp': 80, 'gold': 300, 'items': ['铁剑']},
                        'level_requirement': 3,
                        'type': 'collection'
                    },
                    {
                        'title': '寻找稀有金属',
                        'description': '我需要一些稀有金属来打造高级武器。请收集5块秘银。',
                        'reward': {'exp': 150, 'gold': 800, 'items': ['秘银剑']},
                        'level_requirement': 15,
                        'type': 'collection'
                    }
                ],
                '药店老板': [
                    {
                        'title': '收集草药',
                        'description': '我需要一些草药来制作药水。请收集15株草药。',
                        'reward': {'exp': 70, 'gold': 250, 'items': ['金疮药', '魔法药']},
                        'level_requirement': 2,
                        'type': 'collection'
                    },
                    {
                        'title': '寻找稀有草药',
                        'description': '我需要一些稀有草药来制作高级药水。请收集8株千年灵芝。',
                        'reward': {'exp': 180, 'gold': 900, 'items': ['超级金疮药', '超级魔法药']},
                        'level_requirement': 12,
                        'type': 'collection'
                    }
                ],
                '牧师': [
                    {
                        'title': '净化邪恶',
                        'description': '村庄附近有邪恶的气息，请净化5个邪恶的祭坛。',
                        'reward': {'exp': 120, 'gold': 400, 'items': ['祝福药水']},
                        'level_requirement': 5,
                        'type': 'purification'
                    }
                ]
            },
            '森林': {
                '精灵': [
                    {
                        'title': '保护森林',
                        'description': '有贪婪的人类在砍伐森林，请阻止他们。',
                        'reward': {'exp': 150, 'gold': 600, 'items': ['精灵之弓']},
                        'level_requirement': 8,
                        'type': 'protection'
                    },
                    {
                        'title': '寻找森林之心',
                        'description': '森林之心被盗，请找回它。',
                        'reward': {'exp': 250, 'gold': 1200, 'items': ['自然之戒']},
                        'level_requirement': 18,
                        'type': 'recovery'
                    }
                ],
                '德鲁伊': [
                    {
                        'title': '净化水源',
                        'description': '森林的水源被污染了，请找出污染源并净化它。',
                        'reward': {'exp': 130, 'gold': 500, 'items': ['自然药水']},
                        'level_requirement': 6,
                        'type': 'purification'
                    }
                ],
                '猎人': [
                    {
                        'title': '猎取野兽',
                        'description': '森林中的野兽数量过多，请猎取15只狼。',
                        'reward': {'exp': 110, 'gold': 350, 'items': ['猎人之弓']},
                        'level_requirement': 4,
                        'type': 'hunting'
                    }
                ]
            },
            '沙漠': {
                '商队首领': [
                    {
                        'title': '保护商队',
                        'description': '商队将穿越沙漠，请保护它免受强盗袭击。',
                        'reward': {'exp': 180, 'gold': 800, 'items': ['沙漠之靴']},
                        'level_requirement': 10,
                        'type': 'escort'
                    },
                    {
                        'title': '寻找失落的商队',
                        'description': '一支商队在沙漠中失踪了，请找到它。',
                        'reward': {'exp': 220, 'gold': 1000, 'items': ['沙漠之盾']},
                        'level_requirement': 16,
                        'type': 'search'
                    }
                ],
                '向导': [
                    {
                        'title': '寻找绿洲',
                        'description': '沙漠中需要新的水源，请找到一个新的绿洲。',
                        'reward': {'exp': 140, 'gold': 550, 'items': ['水袋']},
                        'level_requirement': 7,
                        'type': 'exploration'
                    }
                ]
            },
            '地牢': {
                '守卫': [
                    {
                        'title': '捉拿逃犯',
                        'description': '地牢中有囚犯逃跑了，请将他们抓回来。',
                        'reward': {'exp': 160, 'gold': 650, 'items': ['锁链']},
                        'level_requirement': 9,
                        'type': 'capture'
                    }
                ],
                '法师': [
                    {
                        'title': '收集灵魂石',
                        'description': '我需要一些灵魂石来增强我的魔法，请收集8个灵魂石。',
                        'reward': {'exp': 200, 'gold': 900, 'items': ['魔法书']},
                        'level_requirement': 14,
                        'type': 'collection'
                    }
                ]
            }
        }
        
        # 根据地图类型和NPC类型获取任务
        if map_type in quests:
            if npc_type in quests[map_type]:
                return quests[map_type][npc_type]
        
        return []
