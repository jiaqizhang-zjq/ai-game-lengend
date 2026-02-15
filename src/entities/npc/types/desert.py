from ..base import BaseNPC
from ..behaviors.quest import QuestBehavior
from ..behaviors.trade import TradeBehavior
from ..behaviors.skill import SkillBehavior
from ..behaviors.repair import RepairBehavior
from ..behaviors.heal import HealBehavior

class DesertNPC(BaseNPC):
    """沙漠NPC基类"""
    
    def __init__(self, name, x, y, dialogue, has_shop=False, npc_type='普通'):
        """初始化沙漠NPC"""
        super().__init__(name, x, y, dialogue, has_shop, '沙漠', npc_type)
        
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
            '商队首领': ('果断', '沙漠商队的首领，经验丰富', ['领导', '导航', '交易'], '自信'),
            '向导': ('坚韧', '熟悉沙漠的向导，能在沙漠中找到路', ['导航', '生存', '侦查'], '谨慎'),
            '绿洲守卫': ('忠诚', '绿洲的守护者，保护水源', ['战斗', '警戒', '生存'], '严肃'),
            '沙漠商人': ('精明', '在沙漠中做生意的商人', ['经商', '谈判', '生存'], '圆滑'),
            '游牧民': ('自由', '沙漠中的游牧民，逐水草而居', ['放牧', '生存', '马术'], '开朗')
        }
        
        if self.npc_type in personality_types:
            self.personality, self.background, self.skills, self.mood = personality_types[self.npc_type]
        else:
            self.personality = "坚韧"
            self.background = "沙漠的居民"
            self.skills = ["生存", "导航"]
            self.mood = "谨慎"
    
    def _initialize_daily_routine(self):
        """初始化日常行为"""
        routines = {
            '商队首领': ['早晨整队', '带领商队出发', '中午休息', '下午继续前进', '晚上扎营'],
            '向导': ['早晨确定路线', '带领队伍', '中午休息', '下午继续前进', '晚上警戒'],
            '绿洲守卫': ['早晨巡逻', '中午休息', '下午继续巡逻', '晚上值班'],
            '沙漠商人': ['早晨准备货物', '寻找顾客', '中午休息', '下午继续交易', '晚上整理货物'],
            '游牧民': ['早晨放牧', '中午休息', '下午继续放牧', '晚上扎营']
        }
        
        if self.npc_type in routines:
            self.daily_routine = routines[self.npc_type]
        else:
            self.daily_routine = ['早晨活动', '中午休息', '下午活动', '晚上休息']
    
    def _initialize_contextual_dialogue(self):
        """初始化上下文对话"""
        contextual_dialogues = {
            '商队首领': {
                'greeting': '你好，旅行者！要加入我们的商队吗？',
                'quest': '我们的商队被沙漠强盗袭击了，你能帮我们找回货物吗？',
                'farewell': '祝你旅途愉快，小心沙漠的危险！',
                'happy': '商队一切顺利，真是太好了！',
                'sad': '沙漠的环境越来越恶劣了。',
                'angry': '那些沙漠强盗，别让我再碰到他们！'
            },
            '向导': {
                'greeting': '你好，需要沙漠向导吗？',
                'quest': '我的指南针坏了，你能帮我找到新的吗？',
                'farewell': '小心沙漠的沙暴，它们很危险！',
                'happy': '今天的天气不错，适合旅行。',
                'sad': '沙漠的水源越来越少了。',
                'angry': '那些浪费水资源的人，真是太可恶了！'
            },
            '沙漠商人': {
                'greeting': '看看我的宝贝，都是从远方带来的！',
                'quest': '我需要一些稀有物品来丰富我的商品，你能帮我找到吗？',
                'farewell': '欢迎下次再来，我这里总有好东西！',
                'happy': '今天的生意真好！',
                'sad': '最近沙漠的商队越来越少了。',
                'angry': '那些强盗，竟敢抢我的货物！'
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
