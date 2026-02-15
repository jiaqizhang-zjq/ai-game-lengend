from ..base import BaseNPC
from ..behaviors.quest import QuestBehavior
from ..behaviors.trade import TradeBehavior
from ..behaviors.skill import SkillBehavior
from ..behaviors.repair import RepairBehavior
from ..behaviors.heal import HealBehavior

class VillageNPC(BaseNPC):
    """村庄NPC基类"""
    
    def __init__(self, name, x, y, dialogue, has_shop=False, npc_type='普通', function=None):
        """初始化村庄NPC"""
        super().__init__(name, x, y, dialogue, has_shop, '村庄', npc_type, function)
        
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
            '村长': ('慈祥', '村庄的领导者，德高望重', ['领导', '外交'], '正常'),
            '武器商': ('豪爽', '曾经是一名战士，现在改行做生意', ['锻造', '战斗'], '积极'),
            '药店老板': ('细心', '精通草药学，为人善良', ['草药学', '医术'], '温和'),
            '防具商': ('精明', '来自大城市的商人，眼光独到', ['经商', '裁缝'], '谨慎'),
            '铁匠': ('粗犷', '世代打铁，手艺精湛', ['锻造', '修理'], '直率'),
            '法师': ('神秘', '来自远方的魔法师，知识渊博', ['魔法', '占卜'], '平静'),
            '牧师': ('虔诚', '村庄教堂的牧师，信仰坚定', ['治愈', '祝福'], '神圣'),
            '厨师': ('热情', '村庄酒馆的厨师，擅长烹饪', ['烹饪', '酿酒'], '欢快'),
            '渔夫': ('悠闲', '以捕鱼为生，性格开朗', ['钓鱼', '游泳'], '轻松'),
            '猎人': ('敏锐', '村庄的猎人，熟悉山林', ['狩猎', '追踪'], '专注'),
            '医生': ('专业', '村庄的医生，救死扶伤', ['医术', '诊断'], '冷静'),
            '教师': ('博学', '村庄的教师，教书育人', ['知识', '教育'], '温和'),
            '商人': ('圆滑', '游走各地的商人，见多识广', ['经商', '谈判'], '灵活'),
            '卫兵': ('忠诚', '村庄的守卫，尽职尽责', ['战斗', '警戒'], '严肃')
        }
        
        if self.npc_type in personality_types:
            self.personality, self.background, self.skills, self.mood = personality_types[self.npc_type]
        else:
            self.personality = "友好"
            self.background = "村庄的居民"
            self.skills = ["生存"]
            self.mood = "正常"
    
    def _initialize_daily_routine(self):
        """初始化日常行为"""
        routines = {
            '村长': ['早晨巡视村庄', '处理村务', '中午休息', '下午继续工作', '晚上在家'],
            '武器商': ['早晨开店', '制作武器', '中午休息', '下午营业', '晚上关门'],
            '药店老板': ['早晨采集草药', '制作药品', '中午休息', '下午营业', '晚上研究草药'],
            '防具商': ['早晨开店', '制作防具', '中午休息', '下午营业', '晚上关门'],
            '铁匠': ['早晨开始打铁', '中午休息', '下午继续打铁', '晚上整理工具'],
            '法师': ['早晨冥想', '研究魔法', '中午休息', '下午继续研究', '晚上冥想'],
            '牧师': ['早晨祈祷', '主持仪式', '中午休息', '下午帮助村民', '晚上祈祷'],
            '厨师': ['早晨准备食材', '烹饪', '中午营业', '下午继续烹饪', '晚上关门'],
            '渔夫': ['早晨捕鱼', '中午休息', '下午继续捕鱼', '晚上整理渔网'],
            '猎人': ['早晨狩猎', '中午休息', '下午继续狩猎', '晚上处理猎物'],
            '医生': ['早晨出诊', '中午休息', '下午继续出诊', '晚上研究医术'],
            '教师': ['早晨上课', '中午休息', '下午继续上课', '晚上备课'],
            '商人': ['早晨进货', '中午营业', '下午继续营业', '晚上算账'],
            '卫兵': ['早晨巡逻', '中午休息', '下午继续巡逻', '晚上值班']
        }
        
        if self.npc_type in routines:
            self.daily_routine = routines[self.npc_type]
        else:
            self.daily_routine = ['早晨活动', '中午休息', '下午活动', '晚上休息']
    
    def _initialize_contextual_dialogue(self):
        """初始化上下文对话"""
        contextual_dialogues = {
            '村长': {
                'greeting': '欢迎回来，冒险者！村庄最近一切安好。',
                'quest': '我们的村庄需要你的帮助，最近附近的怪物越来越多了。',
                'farewell': '祝你好运，勇敢的冒险者！',
                'happy': '看到村庄繁荣，我真是太高兴了！',
                'sad': '最近村庄的收成不太好，真是让人担心。',
                'angry': '那些怪物竟敢骚扰我们的村民，必须给他们点颜色看看！'
            },
            '武器商': {
                'greeting': '嘿，兄弟！来看点好货吗？',
                'quest': '我需要一些铁矿石来打造更好的武器，你能帮我收集吗？',
                'farewell': '有空再来，我这里永远有最好的武器！',
                'happy': '最近生意不错，多亏了像你这样的勇士！',
                'sad': '最近铁矿石的价格涨了，生意不太好做。',
                'angry': '那些偷我武器的小贼，别让我抓住他们！'
            },
            '药店老板': {
                'greeting': '你好，需要点什么药吗？',
                'quest': '我需要一些稀有草药来制作特效药，你能帮我找到吗？',
                'farewell': '祝你健康，冒险者！',
                'happy': '看到我的药能帮助到你，我很开心。',
                'sad': '最近草药的产量下降了，我很担心。',
                'angry': '那些破坏草药的野兽，真是太可恶了！'
            },
            '牧师': {
                'greeting': '愿神保佑你，冒险者！',
                'quest': '村庄附近有邪恶的气息，请净化这些邪恶。',
                'farewell': '愿神与你同在！',
                'happy': '看到村民们健康快乐，我很欣慰。',
                'sad': '最近邪恶的力量在增长，我很担心。',
                'angry': '那些亵渎神灵的家伙，必将受到惩罚！'
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
