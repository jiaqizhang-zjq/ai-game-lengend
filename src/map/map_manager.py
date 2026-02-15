import pygame
from src.map.map import Map

class MapManager:
    """地图管理器类"""
    
    def __init__(self, game):
        """初始化地图管理器"""
        self.game = game
        self.maps = {}
        self.current_map_id = 1
        self.initialize_maps()
    
    def initialize_maps(self):
        """初始化所有地图"""
        # 创建村庄地图（默认地图）
        self.maps[1] = Map(map_id=1, scene_type='村庄', game=self.game)
        # 创建森林地图
        self.maps[2] = Map(map_id=2, scene_type='森林', game=self.game)
        # 创建沙漠地图
        self.maps[3] = Map(map_id=3, scene_type='沙漠', game=self.game)
        # 创建地牢地图
        self.maps[4] = Map(map_id=4, scene_type='地牢', game=self.game)
        # 创建雪原地图
        self.maps[5] = Map(map_id=5, scene_type='雪原', game=self.game)
    
    def get_current_map(self):
        """获取当前地图"""
        return self.maps.get(self.current_map_id)
    
    def switch_map(self, map_id, player_x, player_y):
        """切换地图"""
        if map_id in self.maps:
            # 保存当前地图的玩家引用
            current_map = self.get_current_map()
            if current_map:
                current_map.player = None
            
            # 切换到新地图
            self.current_map_id = map_id
            new_map = self.get_current_map()
            
            # 设置新地图的玩家引用
            if new_map:
                new_map.set_player(self.game.player)
                # 更新玩家位置
                self.game.player.x = player_x
                self.game.player.y = player_y
                # 更新相机位置
                self.game.camera_x = max(0, min(new_map.width - self.game.width, self.game.player.x - self.game.width // 2))
                self.game.camera_y = max(0, min(new_map.height - self.game.height, self.game.player.y - self.game.height // 2))
                map_message = f"切换到地图 {map_id} ({new_map.scene_type})，位置: ({player_x}, {player_y})"
                print(map_message)
                # 在游戏内显示地图切换消息
                if hasattr(self.game, 'ui') and hasattr(self.game.ui, 'add_game_message'):
                    self.game.ui.add_game_message(map_message, (255, 255, 0), 3000)
                    
                    # 显示当前地图的Boss信息
                    current_map = self.get_current_map()
                    if current_map:
                        # 查找地图中的Boss
                        boss_monsters = [monster for monster in current_map.monsters if hasattr(monster, 'name') and ('王' in monster.name or '教主' in monster.name)]
                        for boss in boss_monsters:
                            boss_message = f"[Boss刷新] {boss.name} 在 {current_map.scene_type} 出现了！坐标: ({int(boss.x)}, {int(boss.y)})"
                            print(boss_message)
                            self.game.ui.add_game_message(boss_message, (255, 0, 0), 5000)
                return True
        return False
    
    def update(self):
        """更新当前地图"""
        current_map = self.get_current_map()
        if current_map:
            current_map.update()
            # 检查玩家是否进入了地图出口
            exit_info = current_map.check_exit(self.game.player)
            if exit_info:
                # 切换到目标地图
                self.switch_map(exit_info['target_map'], exit_info['target_x'], exit_info['target_y'])
    
    def render(self, screen):
        """渲染当前地图"""
        current_map = self.get_current_map()
        if current_map:
            current_map.render(screen, int(self.game.camera_x), int(self.game.camera_y))
    
    def set_player(self, player):
        """设置玩家引用到所有地图"""
        for map in self.maps.values():
            map.set_player(player)