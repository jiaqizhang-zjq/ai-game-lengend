class BaseAnimation:
    """基础动画类"""
    
    def __init__(self, name, duration, x, y):
        """初始化动画"""
        self.name = name
        self.duration = duration  # 动画持续时间（毫秒）
        self.start_time = 0
        self.x = x
        self.y = y
        self.active = False
        self.completed = False
    
    def start(self, current_time):
        """开始动画"""
        self.start_time = current_time
        self.active = True
        self.completed = False
    
    def update(self, current_time):
        """更新动画"""
        if not self.active:
            return
        
        elapsed = current_time - self.start_time
        if elapsed >= self.duration:
            self.completed = True
            self.active = False
        
        return self.active
    
    def render(self, screen, camera_offset=(0, 0)):
        """渲染动画"""
        pass
    
    def is_completed(self):
        """检查动画是否完成"""
        return self.completed
    
    def reset(self):
        """重置动画"""
        self.active = False
        self.completed = False
        self.start_time = 0
