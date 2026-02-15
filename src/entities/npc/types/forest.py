from ..base import BaseNPC
from ..behaviors.quest import QuestBehavior
from ..behaviors.trade import TradeBehavior
from ..behaviors.skill import SkillBehavior
from ..behaviors.repair import RepairBehavior
from ..behaviors.heal import HealBehavior

class ForestNPC(BaseNPC):
    """森林NPC基类"""
    
    def __init__(self, name, x, y, dialogue, has_shop=False, npc_type='普通', function=None):
        """初始化森林NPC"""
        super().__init__(name, x, y, dialogue, has_shop, '森林', npc_type, function)
        
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
            '精灵': ('优雅', '森林的精灵，与自然融为一体', ['射箭', '魔法', '自然之力'], '平静'),
            '德鲁伊': ('神秘', '森林的守护者，能变身为动物', ['变形', '自然魔法', '治疗'], '沉思'),
            '猎人': ('敏锐', '森林的猎人，熟悉每一寸土地', ['狩猎', '追踪', '陷阱'], '专注'),
            '樵夫': ('强壮', '以砍柴为生，力大无穷', ['伐木', '生存', '战斗'], '直率'),
            '隐士': ('孤独', '隐居森林的智者，远离尘世', ['冥想', '知识', '自然'], '平静')
        }
        
        if self.npc_type in personality_types:
            self.personality, self.background, self.skills, self.mood = personality_types[self.npc_type]
        else:
            self.personality = "野性"
            self.background = "森林的居民"
            self.skills = ["生存", "狩猎"]
            self.mood = "平静"
    
    def _initialize_daily_routine(self):
        """初始化日常行为"""
        routines = {
            '精灵': ['早晨冥想', '维护森林', '中午休息', '下午继续维护', '晚上冥想'],
            '德鲁伊': ['早晨与自然交流', '研究魔法', '中午休息', '下午继续研究', '晚上与自然交流'],
            '猎人': ['早晨狩猎', '中午休息', '下午继续狩猎', '晚上处理猎物'],
            '樵夫': ['早晨砍柴', '中午休息', '下午继续砍柴', '晚上整理柴火'],
            '隐士': ['早晨冥想', '研究学问', '中午休息', '下午继续研究', '晚上冥想']
        }
        
        if self.npc_type in routines:
            self.daily_routine = routines[self.npc_type]
        else:
            self.daily_routine = ['早晨活动', '中午休息', '下午活动', '晚上休息']
    
    def _initialize_contextual_dialogue(self):
        """初始化上下文对话"""
        contextual_dialogues = {
            '精灵': {
                'greeting': '欢迎来到森林，人类。',
                'quest': '有一些贪婪的人类在砍伐我们的树木，请阻止他们。',
                'farewell': '愿自然与你同在。',
                'happy': '看到森林生机勃勃，我很欣慰。',
                'sad': '森林的平衡被打破了，我很担心。',
                'angry': '那些破坏森林的家伙，必须受到惩罚！'
            },
            '德鲁伊': {
                'greeting': '你好，旅行者。你对自然有什么疑问吗？',
                'quest': '森林中的水源被污染了，你能帮我找出原因吗？',
                'farewell': '愿自然之力保护你。',
                'happy': '自然的力量是无穷的。',
                'sad': '自然正在遭受破坏，我必须做点什么。',
                'angry': '那些污染自然的人，必将受到惩罚！'
            },
            '猎人': {
                'greeting': '这片森林的每一寸土地我都熟悉。',
                'quest': '森林中的野兽数量过多，请帮我控制它们的数量。',
                'farewell': '祝你狩猎顺利！',
                'happy': '今天的猎物真多！',
                'sad': '最近森林中的猎物越来越少了。',
                'angry': '那些偷猎者，别让我抓住他们！'
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
