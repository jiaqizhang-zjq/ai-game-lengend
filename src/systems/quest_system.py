class Quest:
    """任务类"""
    
    def __init__(self, id, name, description, npc_name, requirements, rewards):
        """初始化任务"""
        self.id = id
        self.name = name
        self.description = description
        self.npc_name = npc_name
        self.requirements = requirements  # 任务要求，如{'kill': {'稻草人': 5}}
        self.rewards = rewards  # 任务奖励，如{'exp': 100, 'gold': 50, 'items': [{'name': '金疮药', 'quantity': 2}]}
        self.completed = False
        self.progress = {'kill': {}}  # 任务进度
        
        # 初始化进度
        if 'kill' in self.requirements:
            for monster_type, count in self.requirements['kill'].items():
                self.progress['kill'][monster_type] = 0
    
    def update_progress(self, progress_type, target, count=1):
        """更新任务进度"""
        if progress_type in self.progress:
            if target in self.progress[progress_type]:
                self.progress[progress_type][target] += count
                # 检查是否完成
                self.check_completion()
    
    def check_completion(self):
        """检查任务是否完成"""
        if 'kill' in self.requirements:
            for monster_type, required_count in self.requirements['kill'].items():
                if self.progress['kill'].get(monster_type, 0) < required_count:
                    return False
            self.completed = True
            return True
        return False
    
    def get_progress_text(self):
        """获取任务进度文本"""
        if 'kill' in self.requirements:
            text = ""
            for monster_type, required_count in self.requirements['kill'].items():
                current_count = self.progress['kill'].get(monster_type, 0)
                text += f"{monster_type}: {current_count}/{required_count}\n"
            return text
        return ""


class QuestSystem:
    """任务系统"""
    
    def __init__(self, game):
        """初始化任务系统"""
        self.game = game
        self.quests = []
        self.initialize_quests()
    
    def initialize_quests(self):
        """初始化任务"""
        # 添加初始任务
        quest1 = Quest(
            id=1,
            name="消灭稻草人",
            description="村长需要你消灭5个稻草人，它们在村庄周围作乱。",
            npc_name="村长",
            requirements={'kill': {'稻草人': 5}},
            rewards={'exp': 100, 'gold': 50, 'items': [{'name': '金疮药', 'quantity': 2}]}
        )
        
        quest2 = Quest(
            id=2,
            name="杀鸡任务",
            description="药店老板需要一些鸡肉来制作药水，帮他杀10只鸡。",
            npc_name="药店老板",
            requirements={'kill': {'鸡': 10}},
            rewards={'exp': 150, 'gold': 80, 'items': [{'name': '魔法药', 'quantity': 3}]}
        )
        
        self.quests.append(quest1)
        self.quests.append(quest2)
    
    def update_quest_progress(self, progress_type, target, count=1):
        """更新所有任务的进度"""
        for quest in self.quests:
            if not quest.completed:
                quest.update_progress(progress_type, target, count)
    
    def get_quests_for_npc(self, npc_name):
        """获取指定NPC的任务"""
        return [quest for quest in self.quests if quest.npc_name == npc_name]
    
    def get_active_quests(self):
        """获取活跃任务"""
        return [quest for quest in self.quests if not quest.completed]
    
    def get_completed_quests(self):
        """获取已完成任务"""
        return [quest for quest in self.quests if quest.completed]
    
    def complete_quest(self, quest_id):
        """完成任务"""
        for quest in self.quests:
            if quest.id == quest_id and quest.completed:
                # 给予奖励
                if 'exp' in quest.rewards:
                    self.game.experience += quest.rewards['exp']
                if 'gold' in quest.rewards:
                    self.game.gold += quest.rewards['gold']
                if 'items' in quest.rewards:
                    for item in quest.rewards['items']:
                        self.game.player.add_item(item['name'], item['quantity'])
                return True
        return False