from ..base import BaseNPC
from ..behaviors.quest import QuestBehavior
from ..behaviors.trade import TradeBehavior
from ..behaviors.skill import SkillBehavior
from ..behaviors.repair import RepairBehavior
from ..behaviors.heal import HealBehavior

class DungeonNPC(BaseNPC):
    """地牢NPC基类"""
    
    def __init__(self, name, x, y, dialogue, has_shop=False, npc_type='普通'):
        """初始化地牢NPC"""
        super().__init__(name, x, y, dialogue, has_shop, '地牢', npc_type)
        
        # 初始化行为模块
        self.quest_behavior = QuestBehavior(self)
        self.trade_behavior = TradeBehavior(self)
        self.skill_behavior = SkillBehavior(self)
        self.repair_behavior = RepairBehavior(self)
        self.heal_behavior = HealBehavior(self)
        
        # 设置个性化属性
        self._set_personal_attributes()
    
    def _set_personal_attributes(self):
        """设置个性化属性"""
        personality_types = {
            '守卫': ('严肃', '地牢的守卫，恪尽职守', ['战斗', '警戒', '侦查'], '警惕'),
            '狱卒': ('冷酷', '地牢的狱卒，铁石心肠', ['战斗', '审讯', '警戒'], '阴郁'),
            '法师': ('疯狂', '在地牢中研究黑暗魔法的法师', ['黑暗魔法', '召唤', '诅咒'], '疯狂'),
            '盗贼': ('狡猾', '躲在地牢中的盗贼', ['潜行', '开锁', '偷窃'], '警惕'),
            '骷髅兵': ('麻木', '被魔法复活的骷髅兵', ['战斗', '不死'], '麻木')
        }
        
        if self.npc_type in personality_types:
            self.personality, self.background, self.skills, self.mood = personality_types[self.npc_type]
        else:
            self.personality = "阴郁"
            self.background = "地牢的居民"
            self.skills = ["战斗", "警戒"]
            self.mood = "警惕"
    
    def _initialize_daily_routine(self):
        """初始化日常行为"""
        routines = {
            '守卫': ['早晨换班', '巡逻地牢', '中午休息', '下午继续巡逻', '晚上值班'],
            '狱卒': ['早晨检查牢房', '看管囚犯', '中午休息', '下午继续看管', '晚上值班'],
            '法师': ['早晨研究魔法', '进行实验', '中午休息', '下午继续研究', '晚上进行仪式'],
            '盗贼': ['早晨休息', '中午活动', '下午寻找机会', '晚上偷窃'],
            '骷髅兵': ['全天站岗', '执行命令', '没有休息']
        }
        
        if self.npc_type in routines:
            self.daily_routine = routines[self.npc_type]
        else:
            self.daily_routine = ['早晨活动', '中午休息', '下午活动', '晚上休息']
    
    def _initialize_contextual_dialogue(self):
        """初始化上下文对话"""
        contextual_dialogues = {
            '守卫': {
                'greeting': '站住！这里是禁地，未经许可不得入内。',
                'quest': '地牢里有囚犯逃跑了，你能帮我把他们抓回来吗？',
                'farewell': '离开这里，不要再来了。',
                'happy': '今天地牢很安静，真是难得。',
                'sad': '地牢的条件越来越差了。',
                'angry': '那些囚犯竟敢反抗，真是不知死活！'
            },
            '法师': {
                'greeting': '哈哈，又有新的实验品来了！',
                'quest': '我需要一些灵魂石来增强我的魔法，你能帮我找到吗？',
                'farewell': '滚吧，等我需要你的时候会再找你！',
                'happy': '我的实验进展顺利，真是太好了！',
                'sad': '我的实验失败了，又要从头开始。',
                'angry': '那些破坏我实验的人，我要让他们付出代价！'
            },
            '盗贼': {
                'greeting': '嘿，想不想发笔横财？',
                'quest': '地牢里有一个宝库，你能帮我打开它吗？',
                'farewell': '小心点，别被守卫发现了！',
                'happy': '今天偷到了不少好东西！',
                'sad': '最近守卫越来越严了。',
                'angry': '那些守卫，总是坏我的好事！'
            }
        }
        
        if self.npc_type in contextual_dialogues:
            self.contextual_dialogue = contextual_dialogues[self.npc_type]
        else:
            super()._initialize_contextual_dialogue()
    
    def give_quest(self, player):
        """给予任务"""
        return self.quest_behavior.give_quest(player)
    
    def trade(self, player, item_name, quantity=1):
        """与玩家交易"""
        return self.trade_behavior.trade(player, item_name, quantity)
    
    def teach_skill(self, player, skill_name):
        """传授技能给玩家"""
        return self.skill_behavior.teach_skill(player, skill_name)
    
    def repair_equipment(self, player, equipment_name):
        """修理装备"""
        return self.repair_behavior.repair_equipment(player, equipment_name)
    
    def heal(self, player):
        """治疗玩家"""
        return self.heal_behavior.heal(player)
