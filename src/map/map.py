import pygame
import random
import os
import math

from src.entities.monster import Monster
from src.entities.npc import create_npc


class Map:
    """地图类"""
    
    def __init__(self, map_id=1, scene_type='村庄', game=None):
        """初始化地图"""
        # 地图ID
        self.id = map_id
        # 增大地图尺寸
        self.width = 2400
        self.height = 1800
        
        # 场景类型
        self.scene_type = scene_type
        
        # 游戏引用
        self.game = game
        
        # 地图出口（连接到其他地图的位置）
        self.exits = []
        self._initialize_exits()
        
        # 怪物列表
        self.monsters = []
        
        # NPC列表
        self.npcs = []
        
        # 初始化怪物和NPC
        self.initialize_entities()
        
        # 地形元素
        self.terrain_elements = []
        self.initialize_terrain()
        
        # 初始化坐标系统
        self._initialize_coordinate_system()
        
        # 加载地图素材
        self.load_map_assets()
    
    def _initialize_coordinate_system(self):
        """初始化地图坐标系统"""
        # 地图特定的坐标原点和度量标准
        coordinate_configs = {
            '村庄': {'origin_lat': 35.0, 'origin_lon': 105.0, 'scale': 0.001},  # 中国中心位置
            '森林': {'origin_lat': 36.0, 'origin_lon': 106.0, 'scale': 0.0012},
            '沙漠': {'origin_lat': 37.0, 'origin_lon': 107.0, 'scale': 0.0015},
            '地牢': {'origin_lat': 38.0, 'origin_lon': 108.0, 'scale': 0.0008},
            '雪原': {'origin_lat': 39.0, 'origin_lon': 109.0, 'scale': 0.0018}
        }
        
        config = coordinate_configs.get(self.scene_type, coordinate_configs['村庄'])
        self.origin_latitude = config['origin_lat']
        self.origin_longitude = config['origin_lon']
        self.coordinate_scale = config['scale']
    
    def pixel_to_latlon(self, x, y):
        """将像素坐标转换为经纬度坐标"""
        latitude = self.origin_latitude + (y * self.coordinate_scale)
        longitude = self.origin_longitude + (x * self.coordinate_scale)
        return {'latitude': latitude, 'longitude': longitude}
    
    def latlon_to_pixel(self, latitude, longitude):
        """将经纬度坐标转换为像素坐标"""
        x = int((longitude - self.origin_longitude) / self.coordinate_scale)
        y = int((latitude - self.origin_latitude) / self.coordinate_scale)
        return {'x': x, 'y': y}
    
    def convert_coordinates_to_map(self, target_map_id, x, y):
        """将当前地图的坐标转换到目标地图"""
        # 先转换为经纬度
        latlon = self.pixel_to_latlon(x, y)
        
        # 获取目标地图的坐标配置
        target_coordinate_configs = {
            '村庄': {'origin_lat': 35.0, 'origin_lon': 105.0, 'scale': 0.001},
            '森林': {'origin_lat': 36.0, 'origin_lon': 106.0, 'scale': 0.0012},
            '沙漠': {'origin_lat': 37.0, 'origin_lon': 107.0, 'scale': 0.0015},
            '地牢': {'origin_lat': 38.0, 'origin_lon': 108.0, 'scale': 0.0008},
            '雪原': {'origin_lat': 39.0, 'origin_lon': 109.0, 'scale': 0.0018}
        }
        
        # 根据目标地图ID获取场景类型
        map_scene_types = {
            1: '村庄',
            2: '森林',
            3: '沙漠',
            4: '地牢',
            5: '雪原'
        }
        
        target_scene = map_scene_types.get(target_map_id, '村庄')
        target_config = target_coordinate_configs.get(target_scene, target_coordinate_configs['村庄'])
        
        # 转换经纬度到目标地图的像素坐标
        target_x = int((latlon['longitude'] - target_config['origin_lon']) / target_config['scale'])
        target_y = int((latlon['latitude'] - target_config['origin_lat']) / target_config['scale'])
        
        # 确保坐标在目标地图范围内
        target_x = max(32, min(2368, target_x))  # 2400 - 32
        target_y = max(32, min(1768, target_y))  # 1800 - 32
        
        return {'x': target_x, 'y': target_y}
    
    def initialize_terrain(self):
        """初始化地形元素 - 使用自然集群分布算法"""
        # 地形特定的环境元素配置
        terrain_configs = {
            '村庄': {
                'clusters': [
                    {'type': 'residential', 'center': (800, 500), 'radius': 300, 'density': 0.8},
                    {'type': 'market', 'center': (1200, 400), 'radius': 200, 'density': 0.7},
                    {'type': 'religious', 'center': (1500, 800), 'radius': 150, 'density': 0.6}
                ],
                'elements': {
                    'house': {'count': 10, 'cluster_weight': {'residential': 0.8, 'market': 0.2}},
                    'well': {'count': 2, 'cluster_weight': {'residential': 0.7, 'market': 0.3}},
                    'tree': {'count': 20, 'cluster_weight': {'residential': 0.4, 'market': 0.3, 'religious': 0.3}},
                    'rock': {'count': 10, 'cluster_weight': {'residential': 0.3, 'market': 0.2, 'religious': 0.5}}
                }
            },
            '森林': {
                'clusters': [
                    {'type': 'dense_forest', 'center': (600, 600), 'radius': 400, 'density': 0.9},
                    {'type': 'clearing', 'center': (1200, 900), 'radius': 250, 'density': 0.4},
                    {'type': 'edge', 'center': (1800, 600), 'radius': 300, 'density': 0.6}
                ],
                'elements': {
                    'tree': {'count': 120, 'cluster_weight': {'dense_forest': 0.8, 'clearing': 0.1, 'edge': 0.5}},
                    'rock': {'count': 30, 'cluster_weight': {'dense_forest': 0.3, 'clearing': 0.6, 'edge': 0.4}}
                }
            },
            '沙漠': {
                'clusters': [
                    {'type': 'oasis', 'center': (1000, 500), 'radius': 200, 'density': 0.7},
                    {'type': 'dunes', 'center': (400, 800), 'radius': 350, 'density': 0.6},
                    {'type': 'wasteland', 'center': (1800, 800), 'radius': 400, 'density': 0.4}
                ],
                'elements': {
                    'rock': {'count': 40, 'cluster_weight': {'oasis': 0.3, 'dunes': 0.6, 'wasteland': 0.4}},
                    'tree': {'count': 10, 'cluster_weight': {'oasis': 0.9, 'dunes': 0.1, 'wasteland': 0.0}}
                }
            },
            '地牢': {
                'clusters': [
                    {'type': 'chamber', 'center': (800, 600), 'radius': 250, 'density': 0.7},
                    {'type': 'corridor', 'center': (1400, 900), 'radius': 200, 'density': 0.5}
                ],
                'elements': {
                    'rock': {'count': 30, 'cluster_weight': {'chamber': 0.6, 'corridor': 0.4}}
                }
            },
            '雪原': {
                'clusters': [
                    {'type': 'frozen_lake', 'center': (1000, 700), 'radius': 300, 'density': 0.5},
                    {'type': 'snowy_forest', 'center': (600, 400), 'radius': 250, 'density': 0.6},
                    {'type': 'mountain_edge', 'center': (1800, 500), 'radius': 350, 'density': 0.7}
                ],
                'elements': {
                    'tree': {'count': 50, 'cluster_weight': {'snowy_forest': 0.8, 'mountain_edge': 0.4}},
                    'rock': {'count': 40, 'cluster_weight': {'frozen_lake': 0.3, 'mountain_edge': 0.7}}
                }
            }
        }
        
        # 获取当前地形的配置
        config = terrain_configs.get(self.scene_type, terrain_configs['村庄'])
        clusters = config['clusters']
        elements = config['elements']
        
        # 生成环境元素
        for element_type, element_config in elements.items():
            count = element_config['count']
            cluster_weights = element_config['cluster_weight']
            
            for _ in range(count):
                # 基于权重选择集群
                cluster_choices = [c for c in clusters if c['type'] in cluster_weights]
                cluster_weights_filtered = [cluster_weights[c['type']] for c in cluster_choices]
                
                if cluster_choices:
                    # 选择一个集群
                    selected_cluster = random.choices(cluster_choices, weights=cluster_weights_filtered, k=1)[0]
                    
                    # 在集群内生成元素位置（使用高斯分布实现自然集群）
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.gauss(0, selected_cluster['radius'] * 0.4)  # 高斯分布，更集中在中心
                    distance = min(abs(distance), selected_cluster['radius'])  # 限制在集群半径内
                    
                    x = selected_cluster['center'][0] + int(distance * math.cos(angle))
                    y = selected_cluster['center'][1] + int(distance * math.sin(angle))
                    
                    # 确保位置在地图范围内
                    x = max(32, min(self.width - 32, x))
                    y = max(32, min(self.height - 32, y))
                    
                    # 检查是否在NPC活动区域内
                    in_npc_area = False
                    for npc_area in getattr(self, 'npc_activity_areas', []):
                        area = npc_area.get('area', {})
                        if 'x1' in area and 'y1' in area and 'x2' in area and 'y2' in area:
                            if area['x1'] - 50 <= x <= area['x2'] + 50 and area['y1'] - 50 <= y <= area['y2'] + 50:
                                in_npc_area = True
                                break
                    
                    # 检查是否在建筑物位置附近
                    in_building_area = False
                    for npc_area in getattr(self, 'npc_activity_areas', []):
                        building = npc_area.get('building', {})
                        if building is not None and 'x' in building and 'y' in building:
                            dx = x - building['x']
                            dy = y - building['y']
                            distance = math.sqrt(dx**2 + dy**2)
                            if distance < 80:
                                in_building_area = True
                                break
                    
                    # 只有不在NPC活动区域和建筑物附近的元素才添加
                    if not in_npc_area and not in_building_area:
                        self.terrain_elements.append({'type': element_type, 'x': x, 'y': y})
        
        # 为特定地形添加特殊元素
        if self.scene_type == '村庄':
            # 村庄添加祭坛（避开NPC活动区域）
            altar_x, altar_y = 1500, 800
            in_npc_area = False
            for npc_area in getattr(self, 'npc_activity_areas', []):
                area = npc_area.get('area', {})
                if 'x1' in area and 'y1' in area and 'x2' in area and 'y2' in area:
                    if area['x1'] - 100 <= altar_x <= area['x2'] + 100 and area['y1'] - 100 <= altar_y <= area['y2'] + 100:
                        in_npc_area = True
                        break
            if not in_npc_area:
                self.terrain_elements.append({'type': 'altar', 'x': altar_x, 'y': altar_y})
        elif self.scene_type == '森林':
            # 森林添加神秘祭坛
            self.terrain_elements.append({'type': 'altar', 'x': 1200, 'y': 600})
        elif self.scene_type == '沙漠':
            # 沙漠添加绿洲水井
            self.terrain_elements.append({'type': 'well', 'x': 1000, 'y': 500})
        elif self.scene_type == '雪原':
            # 雪原添加冰雕
            self.terrain_elements.append({'type': 'altar', 'x': 1000, 'y': 700})
    
    def initialize_entities(self):
        """初始化怪物和NPC"""
        # 导入ID管理器
        from src.core.id_manager import id_manager
        
        # 定义地图固定怪物刷新点和活动区域
        monster_spawns = {
            '村庄': {
                'normal': [
                    {'monster_id': 1, 'name': '稻草人', 'x': 200, 'y': 600, 'activity_area': {'x1': 100, 'y1': 500, 'x2': 300, 'y2': 700}},
                    {'monster_id': 1, 'name': '稻草人', 'x': 1000, 'y': 800, 'activity_area': {'x1': 900, 'y1': 700, 'x2': 1100, 'y2': 900}},
                    {'monster_id': 1, 'name': '稻草人', 'x': 1800, 'y': 600, 'activity_area': {'x1': 1700, 'y1': 500, 'x2': 1900, 'y2': 700}},
                    {'monster_id': 2, 'name': '鸡', 'x': 400, 'y': 400, 'activity_area': {'x1': 300, 'y1': 300, 'x2': 500, 'y2': 500}},
                    {'monster_id': 2, 'name': '鸡', 'x': 1200, 'y': 400, 'activity_area': {'x1': 1100, 'y1': 300, 'x2': 1300, 'y2': 500}},
                    {'monster_id': 2, 'name': '鸡', 'x': 2000, 'y': 400, 'activity_area': {'x1': 1900, 'y1': 300, 'x2': 2100, 'y2': 500}},
                    {'monster_id': 3, 'name': '鹿', 'x': 600, 'y': 1000, 'activity_area': {'x1': 500, 'y1': 900, 'x2': 700, 'y2': 1100}},
                    {'monster_id': 3, 'name': '鹿', 'x': 1400, 'y': 1000, 'activity_area': {'x1': 1300, 'y1': 900, 'x2': 1500, 'y2': 1100}},
                    {'monster_id': 3, 'name': '鹿', 'x': 2200, 'y': 1000, 'activity_area': {'x1': 2100, 'y1': 900, 'x2': 2300, 'y2': 1100}}
                ]
            },
            '森林': {
                'normal': [
                    {'monster_id': 4, 'name': '狼', 'x': 400, 'y': 400, 'activity_area': {'x1': 300, 'y1': 300, 'x2': 500, 'y2': 500}},
                    {'monster_id': 4, 'name': '狼', 'x': 1200, 'y': 600, 'activity_area': {'x1': 1100, 'y1': 500, 'x2': 1300, 'y2': 700}},
                    {'monster_id': 4, 'name': '狼', 'x': 2000, 'y': 400, 'activity_area': {'x1': 1900, 'y1': 300, 'x2': 2100, 'y2': 500}},
                    {'monster_id': 3, 'name': '鹿', 'x': 600, 'y': 800, 'activity_area': {'x1': 500, 'y1': 700, 'x2': 700, 'y2': 900}},
                    {'monster_id': 3, 'name': '鹿', 'x': 1400, 'y': 800, 'activity_area': {'x1': 1300, 'y1': 700, 'x2': 1500, 'y2': 900}},
                    {'monster_id': 1, 'name': '稻草人', 'x': 800, 'y': 1200, 'activity_area': {'x1': 700, 'y1': 1100, 'x2': 900, 'y2': 1300}},
                    {'monster_id': 1, 'name': '稻草人', 'x': 1600, 'y': 1200, 'activity_area': {'x1': 1500, 'y1': 1100, 'x2': 1700, 'y2': 1300}}
                ],
                'boss': [
                    {'monster_id': 7, 'name': '骷髅王', 'x': 1000, 'y': 500, 'activity_area': {'x1': 800, 'y1': 300, 'x2': 1200, 'y2': 700}},
                    {'monster_id': 8, 'name': '僵尸王', 'x': 1000, 'y': 1000, 'activity_area': {'x1': 800, 'y1': 800, 'x2': 1200, 'y2': 1200}}]
            },
            '沙漠': {
                'normal': [
                    {'monster_id': 4, 'name': '狼', 'x': 400, 'y': 400, 'activity_area': {'x1': 300, 'y1': 300, 'x2': 500, 'y2': 500}},
                    {'monster_id': 4, 'name': '狼', 'x': 1200, 'y': 400, 'activity_area': {'x1': 1100, 'y1': 300, 'x2': 1300, 'y2': 500}},
                    {'monster_id': 4, 'name': '狼', 'x': 2000, 'y': 400, 'activity_area': {'x1': 1900, 'y1': 300, 'x2': 2100, 'y2': 500}},
                    {'monster_id': 5, 'name': '骷髅', 'x': 600, 'y': 800, 'activity_area': {'x1': 500, 'y1': 700, 'x2': 700, 'y2': 900}},
                    {'monster_id': 5, 'name': '骷髅', 'x': 1400, 'y': 800, 'activity_area': {'x1': 1300, 'y1': 700, 'x2': 1500, 'y2': 900}},
                    {'monster_id': 5, 'name': '骷髅', 'x': 800, 'y': 1200, 'activity_area': {'x1': 700, 'y1': 1100, 'x2': 900, 'y2': 1300}},
                    {'monster_id': 5, 'name': '骷髅', 'x': 1600, 'y': 1200, 'activity_area': {'x1': 1500, 'y1': 1100, 'x2': 1700, 'y2': 1300}}
                ],
                'boss': [
                    {'monster_id': 7, 'name': '骷髅王', 'x': 1000, 'y': 600, 'activity_area': {'x1': 800, 'y1': 400, 'x2': 1200, 'y2': 800}},
                    {'monster_id': 9, 'name': '沃玛教主', 'x': 1000, 'y': 1000, 'activity_area': {'x1': 800, 'y1': 800, 'x2': 1200, 'y2': 1200}}]
            },
            '地牢': {
                'normal': [
                    {'monster_id': 5, 'name': '骷髅', 'x': 400, 'y': 400, 'activity_area': {'x1': 300, 'y1': 300, 'x2': 500, 'y2': 500}},
                    {'monster_id': 5, 'name': '骷髅', 'x': 1200, 'y': 400, 'activity_area': {'x1': 1100, 'y1': 300, 'x2': 1300, 'y2': 500}},
                    {'monster_id': 5, 'name': '骷髅', 'x': 2000, 'y': 400, 'activity_area': {'x1': 1900, 'y1': 300, 'x2': 2100, 'y2': 500}},
                    {'monster_id': 6, 'name': '僵尸', 'x': 600, 'y': 800, 'activity_area': {'x1': 500, 'y1': 700, 'x2': 700, 'y2': 900}},
                    {'monster_id': 6, 'name': '僵尸', 'x': 1400, 'y': 800, 'activity_area': {'x1': 1300, 'y1': 700, 'x2': 1500, 'y2': 900}},
                    {'monster_id': 6, 'name': '僵尸', 'x': 800, 'y': 1200, 'activity_area': {'x1': 700, 'y1': 1100, 'x2': 900, 'y2': 1300}},
                    {'monster_id': 6, 'name': '僵尸', 'x': 1600, 'y': 1200, 'activity_area': {'x1': 1500, 'y1': 1100, 'x2': 1700, 'y2': 1300}}
                ],
                'boss': [
                    {'monster_id': 8, 'name': '僵尸王', 'x': 1000, 'y': 600, 'activity_area': {'x1': 800, 'y1': 400, 'x2': 1200, 'y2': 800}},
                    {'monster_id': 9, 'name': '沃玛教主', 'x': 1000, 'y': 1000, 'activity_area': {'x1': 800, 'y1': 800, 'x2': 1200, 'y2': 1200}},
                    {'monster_id': 10, 'name': '祖玛教主', 'x': 1000, 'y': 1400, 'activity_area': {'x1': 800, 'y1': 1200, 'x2': 1200, 'y2': 1600}}]
            },
            '雪原': {
                'normal': [
                    {'monster_id': 1, 'name': '稻草人', 'x': 400, 'y': 400, 'activity_area': {'x1': 300, 'y1': 300, 'x2': 500, 'y2': 500}},
                    {'monster_id': 1, 'name': '稻草人', 'x': 1200, 'y': 400, 'activity_area': {'x1': 1100, 'y1': 300, 'x2': 1300, 'y2': 500}},
                    {'monster_id': 1, 'name': '稻草人', 'x': 2000, 'y': 400, 'activity_area': {'x1': 1900, 'y1': 300, 'x2': 2100, 'y2': 500}},
                    {'monster_id': 2, 'name': '鸡', 'x': 600, 'y': 800, 'activity_area': {'x1': 500, 'y1': 700, 'x2': 700, 'y2': 900}},
                    {'monster_id': 2, 'name': '鸡', 'x': 1400, 'y': 800, 'activity_area': {'x1': 1300, 'y1': 700, 'x2': 1500, 'y2': 900}},
                    {'monster_id': 3, 'name': '鹿', 'x': 800, 'y': 1200, 'activity_area': {'x1': 700, 'y1': 1100, 'x2': 900, 'y2': 1300}},
                    {'monster_id': 3, 'name': '鹿', 'x': 1600, 'y': 1200, 'activity_area': {'x1': 1500, 'y1': 1100, 'x2': 1700, 'y2': 1300}}
                ],
                'boss': [
                    {'monster_id': 7, 'name': '骷髅王', 'x': 1000, 'y': 500, 'activity_area': {'x1': 800, 'y1': 300, 'x2': 1200, 'y2': 700}},
                    {'monster_id': 8, 'name': '僵尸王', 'x': 1000, 'y': 1000, 'activity_area': {'x1': 800, 'y1': 800, 'x2': 1200, 'y2': 1200}}
                ]
            }
        }
        
        # 为NPC分配活动区域并创建禁止怪物生成的区域
        self.npc_activity_areas = []
        
        # 生成普通怪物
        if self.scene_type in monster_spawns:
            spawn_data = monster_spawns[self.scene_type]
            if 'normal' in spawn_data:
                for spawn in spawn_data['normal']:
                    # 检查刷新点是否在NPC活动区域内
                    in_npc_area = False
                    for npc_area in self.npc_activity_areas:
                        area = npc_area['area']
                        if area['x1'] <= spawn['x'] <= area['x2'] and area['y1'] <= spawn['y'] <= area['y2']:
                            in_npc_area = True
                            break
                    
                    # 只有不在NPC活动区域内的刷新点才生成怪物
                    if not in_npc_area:
                        monster = Monster(spawn['name'], spawn['x'], spawn['y'])
                        # 添加活动区域信息
                        monster.activity_area = spawn['activity_area']
                        self.monsters.append(monster)
        
        # 生成Boss
        if self.scene_type in monster_spawns:
            spawn_data = monster_spawns[self.scene_type]
            if 'boss' in spawn_data:
                for spawn in spawn_data['boss']:
                    # 检查刷新点是否在NPC活动区域内
                    in_npc_area = False
                    for npc_area in self.npc_activity_areas:
                        area = npc_area['area']
                        if area['x1'] <= spawn['x'] <= area['x2'] and area['y1'] <= spawn['y'] <= area['y2']:
                            in_npc_area = True
                            break
                    
                    # 只有不在NPC活动区域内的刷新点才生成Boss
                    if not in_npc_area:
                        boss = Monster(spawn['name'], spawn['x'], spawn['y'])
                        # 添加活动区域信息
                        boss.activity_area = spawn['activity_area']
                        self.monsters.append(boss)
                        # 显示Boss刷新消息
                        boss_message = f"[Boss刷新] {spawn['name']} 在 {self.scene_type} 出现了！坐标: ({spawn['x']}, {spawn['y']})"
                        print(boss_message)
                        # 暂时只在控制台显示，游戏内消息将在UI初始化后显示
        
        # 根据地图类型生成特定的NPC
        if self.scene_type == '村庄':
            # 村庄NPC及其活动区域
            village_npcs = [
                {'id': 1, 'x': 100, 'y': 100, 'dialogue': '欢迎来到传奇世界！', 'has_shop': False, 'type': '村庄', 'role': '村长', 'activity_area': {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150}, 'building': {'x': 800, 'y': 400}},
                {'id': 2, 'x': 200, 'y': 200, 'dialogue': '需要购买武器吗？', 'has_shop': True, 'type': '村庄', 'role': '武器商', 'activity_area': {'x1': 150, 'y1': 150, 'x2': 250, 'y2': 250}, 'building': {'x': 1200, 'y': 600}},
                {'id': 3, 'x': 300, 'y': 300, 'dialogue': '这里有最好的药水！', 'has_shop': True, 'type': '村庄', 'role': '药店老板', 'activity_area': {'x1': 250, 'y1': 250, 'x2': 350, 'y2': 350}, 'building': {'x': 1600, 'y': 400}},
                {'id': 4, 'x': 400, 'y': 400, 'dialogue': '来看看最新的防具！', 'has_shop': True, 'type': '村庄', 'role': '防具商', 'activity_area': {'x1': 350, 'y1': 350, 'x2': 450, 'y2': 450}, 'building': {'x': 800, 'y': 400}},
                {'id': 5, 'x': 500, 'y': 200, 'dialogue': '我可以帮你修理装备！', 'has_shop': False, 'type': '村庄', 'role': '铁匠', 'activity_area': {'x1': 450, 'y1': 150, 'x2': 550, 'y2': 250}, 'building': {'x': 1200, 'y': 600}},
                {'id': 6, 'x': 700, 'y': 300, 'dialogue': '学习魔法吗？', 'has_shop': True, 'type': '村庄', 'role': '法师', 'activity_area': {'x1': 650, 'y1': 250, 'x2': 750, 'y2': 350}, 'building': {'x': 1600, 'y': 400}},
                {'id': 7, 'x': 600, 'y': 500, 'dialogue': '愿神保佑你！', 'has_shop': True, 'type': '村庄', 'role': '牧师', 'activity_area': {'x1': 550, 'y1': 450, 'x2': 650, 'y2': 550}, 'building': {'x': 800, 'y': 400}},
                {'id': 8, 'x': 800, 'y': 300, 'dialogue': '欢迎使用公共仓库！', 'has_shop': False, 'type': '村庄', 'role': '仓库管理员', 'activity_area': {'x1': 750, 'y1': 250, 'x2': 850, 'y2': 350}, 'building': {'x': 1200, 'y': 600}}
            ]
            for npc_data in village_npcs:
                npc_info = id_manager.get_npc_by_id(npc_data['id'])
                if npc_info:
                    # 根据NPC类型设置功能
                    function = None
                    if npc_data['role'] == '仓库管理员':
                        function = 'storage'
                    elif npc_data['has_shop']:
                        function = 'recycle'
                    
                    npc = create_npc(
                        npc_info['name'],
                        npc_data['x'],
                        npc_data['y'],
                        npc_data['dialogue'],
                        npc_data['has_shop'],
                        npc_data['type'],
                        npc_data['role'],
                        function
                    )
                    # 设置活动区域
                    npc.set_activity_area(npc_data['activity_area'])
                    # 设置关联建筑物
                    npc.set_associated_building(npc_data['building'])
                    self.npcs.append(npc)
                    # 添加到NPC活动区域列表，用于后续怪物生成时避开这些区域
                    self.npc_activity_areas.append({
                        'area': npc_data['activity_area'],
                        'npc': npc,
                        'building': npc_data['building']
                    })
        elif self.scene_type == '森林':
            # 森林NPC及其活动区域
            forest_npcs = [
                {'id': 8, 'x': 400, 'y': 300, 'dialogue': '人类，你为何进入精灵的领地？', 'has_shop': False, 'type': '森林', 'role': '精灵', 'activity_area': {'x1': 350, 'y1': 250, 'x2': 450, 'y2': 350}, 'building': None},
                {'id': 9, 'x': 600, 'y': 500, 'dialogue': '自然的平衡需要维护。', 'has_shop': True, 'type': '森林', 'role': '德鲁伊', 'activity_area': {'x1': 550, 'y1': 450, 'x2': 650, 'y2': 550}, 'building': None}
            ]
            for npc_data in forest_npcs:
                npc_info = id_manager.get_npc_by_id(npc_data['id'])
                if npc_info:
                    npc = create_npc(
                        npc_info['name'],
                        npc_data['x'],
                        npc_data['y'],
                        npc_data['dialogue'],
                        npc_data['has_shop'],
                        npc_data['type'],
                        npc_data['role']
                    )
                    # 设置活动区域
                    npc.set_activity_area(npc_data['activity_area'])
                    # 设置关联建筑物
                    npc.set_associated_building(npc_data['building'])
                    self.npcs.append(npc)
                    # 添加到NPC活动区域列表
                    self.npc_activity_areas.append({
                        'area': npc_data['activity_area'],
                        'npc': npc,
                        'building': npc_data['building']
                    })
        elif self.scene_type == '沙漠':
            # 沙漠NPC及其活动区域
            desert_npcs = [
                {'id': 10, 'x': 400, 'y': 300, 'dialogue': '加入我们的商队，穿越沙漠！', 'has_shop': True, 'type': '沙漠', 'role': '商队首领', 'activity_area': {'x1': 350, 'y1': 250, 'x2': 450, 'y2': 350}, 'building': None},
                {'id': 11, 'x': 600, 'y': 500, 'dialogue': '在沙漠中，我就是你的指南针。', 'has_shop': False, 'type': '沙漠', 'role': '向导', 'activity_area': {'x1': 550, 'y1': 450, 'x2': 650, 'y2': 550}, 'building': None}
            ]
            for npc_data in desert_npcs:
                npc_info = id_manager.get_npc_by_id(npc_data['id'])
                if npc_info:
                    npc = create_npc(
                        npc_info['name'],
                        npc_data['x'],
                        npc_data['y'],
                        npc_data['dialogue'],
                        npc_data['has_shop'],
                        npc_data['type'],
                        npc_data['role']
                    )
                    # 设置活动区域
                    npc.set_activity_area(npc_data['activity_area'])
                    # 设置关联建筑物
                    npc.set_associated_building(npc_data['building'])
                    self.npcs.append(npc)
                    # 添加到NPC活动区域列表
                    self.npc_activity_areas.append({
                        'area': npc_data['activity_area'],
                        'npc': npc,
                        'building': npc_data['building']
                    })
        elif self.scene_type == '地牢':
            # 地牢NPC及其活动区域
            dungeon_npcs = [
                {'id': 12, 'x': 400, 'y': 300, 'dialogue': '站住！这里是禁地！', 'has_shop': False, 'type': '地牢', 'role': '守卫', 'activity_area': {'x1': 350, 'y1': 250, 'x2': 450, 'y2': 350}, 'building': None},
                {'id': 13, 'x': 800, 'y': 400, 'dialogue': '哈哈，新的实验品来了！', 'has_shop': True, 'type': '地牢', 'role': '法师', 'activity_area': {'x1': 750, 'y1': 350, 'x2': 850, 'y2': 450}, 'building': None}
            ]
            for npc_data in dungeon_npcs:
                npc_info = id_manager.get_npc_by_id(npc_data['id'])
                if npc_info:
                    npc = create_npc(
                        npc_info['name'],
                        npc_data['x'],
                        npc_data['y'],
                        npc_data['dialogue'],
                        npc_data['has_shop'],
                        npc_data['type'],
                        npc_data['role']
                    )
                    # 设置活动区域
                    npc.set_activity_area(npc_data['activity_area'])
                    # 设置关联建筑物
                    npc.set_associated_building(npc_data['building'])
                    self.npcs.append(npc)
                    # 添加到NPC活动区域列表
                    self.npc_activity_areas.append({
                        'area': npc_data['activity_area'],
                        'npc': npc,
                        'building': npc_data['building']
                    })
        elif self.scene_type == '雪原':
            # 雪原NPC及其活动区域
            snow_npcs = [
                {'id': 14, 'x': 400, 'y': 300, 'dialogue': '欢迎来到雪原，旅行者。', 'has_shop': True, 'type': '雪原', 'role': '商人', 'activity_area': {'x1': 350, 'y1': 250, 'x2': 450, 'y2': 350}, 'building': None},
                {'id': 15, 'x': 600, 'y': 500, 'dialogue': '雪原的危险超出你的想象。', 'has_shop': False, 'type': '雪原', 'role': '猎人', 'activity_area': {'x1': 550, 'y1': 450, 'x2': 650, 'y2': 550}, 'building': None}
            ]
            for npc_data in snow_npcs:
                npc_info = id_manager.get_npc_by_id(npc_data['id'])
                if npc_info:
                    npc = create_npc(
                        npc_info['name'],
                        npc_data['x'],
                        npc_data['y'],
                        npc_data['dialogue'],
                        npc_data['has_shop'],
                        npc_data['type'],
                        npc_data['role']
                    )
                    # 设置活动区域
                    npc.set_activity_area(npc_data['activity_area'])
                    # 设置关联建筑物
                    npc.set_associated_building(npc_data['building'])
                    self.npcs.append(npc)
                    # 添加到NPC活动区域列表
                    self.npc_activity_areas.append({
                        'area': npc_data['activity_area'],
                        'npc': npc,
                        'building': npc_data['building']
                    })
        else:
            # 默认NPC
            default_npcs = [
                {'id': 1, 'x': 100, 'y': 100, 'dialogue': '欢迎来到传奇世界！', 'has_shop': False},
                {'id': 2, 'x': 200, 'y': 200, 'dialogue': '需要购买武器吗？', 'has_shop': True},
                {'id': 3, 'x': 300, 'y': 300, 'dialogue': '这里有最好的药水！', 'has_shop': True},
                {'id': 4, 'x': 400, 'y': 400, 'dialogue': '来看看最新的防具！', 'has_shop': True},
                {'id': 6, 'x': 700, 'y': 300, 'dialogue': '学习魔法吗？', 'has_shop': True}
            ]
            for npc_data in default_npcs:
                npc_info = id_manager.get_npc_by_id(npc_data['id'])
                if npc_info:
                    self.npcs.append(create_npc(
                        npc_info['name'],
                        npc_data['x'],
                        npc_data['y'],
                        npc_data['dialogue'],
                        npc_data['has_shop']
                    ))
    
    def _initialize_exits(self):
        """初始化地图出口"""
        if self.scene_type == '村庄':
            # 村庄地图出口
            self.exits = [
                {'x': 800, 'y': 0, 'width': 200, 'height': 50, 'target_map': 2, 'target_x': 800, 'target_y': 1000, 'direction': 'north'},
                {'x': 1550, 'y': 600, 'width': 50, 'height': 200, 'target_map': 3, 'target_x': 100, 'target_y': 600, 'direction': 'east'},
                {'x': 800, 'y': 1150, 'width': 200, 'height': 50, 'target_map': 4, 'target_x': 800, 'target_y': 100, 'direction': 'south'},
                {'x': 0, 'y': 600, 'width': 50, 'height': 200, 'target_map': 5, 'target_x': 1450, 'target_y': 600, 'direction': 'west'}
            ]
        elif self.scene_type == '森林':
            # 森林地图出口
            self.exits = [
                {'x': 800, 'y': 1150, 'width': 200, 'height': 50, 'target_map': 1, 'target_x': 800, 'target_y': 100, 'direction': 'south'},
                {'x': 1550, 'y': 600, 'width': 50, 'height': 200, 'target_map': 5, 'target_x': 100, 'target_y': 600, 'direction': 'east'}
            ]
        elif self.scene_type == '沙漠':
            # 沙漠地图出口
            self.exits = [
                {'x': 50, 'y': 600, 'width': 50, 'height': 200, 'target_map': 1, 'target_x': 1450, 'target_y': 600, 'direction': 'west'},
                {'x': 800, 'y': 0, 'width': 200, 'height': 50, 'target_map': 5, 'target_x': 800, 'target_y': 1000, 'direction': 'north'}
            ]
        elif self.scene_type == '地牢':
            # 地牢地图出口
            self.exits = [
                {'x': 800, 'y': 50, 'width': 200, 'height': 50, 'target_map': 1, 'target_x': 800, 'target_y': 1000, 'direction': 'north'},
                {'x': 0, 'y': 600, 'width': 50, 'height': 200, 'target_map': 5, 'target_x': 1450, 'target_y': 600, 'direction': 'west'}
            ]
        elif self.scene_type == '雪原':
            # 雪原地图出口 - 修复连接问题，添加通往其他区域的道路
            self.exits = [
                {'x': 0, 'y': 600, 'width': 50, 'height': 200, 'target_map': 1, 'target_x': 1450, 'target_y': 600, 'direction': 'west'},
                {'x': 1550, 'y': 600, 'width': 50, 'height': 200, 'target_map': 2, 'target_x': 100, 'target_y': 600, 'direction': 'east'},
                {'x': 800, 'y': 1150, 'width': 200, 'height': 50, 'target_map': 3, 'target_x': 800, 'target_y': 100, 'direction': 'south'},
                {'x': 800, 'y': 0, 'width': 200, 'height': 50, 'target_map': 4, 'target_x': 800, 'target_y': 1000, 'direction': 'north'},
                # 添加功能性传送点
                {'x': 1200, 'y': 800, 'width': 100, 'height': 100, 'target_map': 1, 'target_x': 1000, 'target_y': 600, 'direction': 'teleport', 'name': '雪原传送点'}
            ]
        else:
            # 默认出口
            self.exits = []

    def load_map_assets(self):
        """加载地图素材"""
        # 尝试加载外部地图素材，失败则使用默认生成
        try:
            base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
            self.map_assets = {
                'terrain': {},
                'objects': {}
            }
            
            # 加载地形素材
            terrain_path = os.path.join(base_path, 'sprites', 'terrain')
            if os.path.exists(terrain_path):
                # 加载树素材
                tree_path = os.path.join(terrain_path, 'tree.png')
                if os.path.exists(tree_path):
                    self.map_assets['terrain']['tree'] = pygame.image.load(tree_path)
                
                # 加载岩石素材
                rock_path = os.path.join(terrain_path, 'rock.png')
                if os.path.exists(rock_path):
                    self.map_assets['terrain']['rock'] = pygame.image.load(rock_path)
                
                # 加载房子素材
                house_path = os.path.join(terrain_path, 'house.png')
                if os.path.exists(house_path):
                    self.map_assets['terrain']['house'] = pygame.image.load(house_path)
            
            self.use_default_assets = False if self.map_assets['terrain'] else True
        except Exception as e:
            print(f"加载地图素材失败: {e}")
            self.use_default_assets = True
            self.map_assets = {'terrain': {}, 'objects': {}}
    
    def update(self):
        """更新地图状态"""
        # 更新怪物
        for monster in self.monsters:
            if not monster.is_dead():
                monster.update(self.player)
        
        # 移除死亡的怪物
        self.monsters = [monster for monster in self.monsters if not monster.is_dead()]
        
        # 处理碰撞检测
        self.handle_collisions()
        
        # 随机生成新怪物
        if len(self.monsters) < 15:
            if random.random() < 0.01:
                # 导入ID管理器
                from src.core.id_manager import id_manager
                
                # 根据地图类型选择怪物
                if self.scene_type == '村庄':
                    monster_ids = [1, 2, 3]  # 稻草人、鸡、鹿
                elif self.scene_type == '森林':
                    monster_ids = [4, 3, 1]  # 狼、鹿、稻草人
                elif self.scene_type == '沙漠':
                    monster_ids = [4, 5]  # 狼、骷髅
                elif self.scene_type == '地牢':
                    monster_ids = [5, 6]  # 骷髅、僵尸
                else:
                    monster_ids = [1, 2, 3, 5, 6, 4]  # 稻草人、鸡、鹿、骷髅、僵尸、狼
                
                # 低概率生成Boss
                boss_spawned = False
                if random.random() < 0.05:  # 5%概率生成Boss
                    if self.scene_type == '沙漠':
                        boss_id = 7  # 骷髅王
                        boss_info = id_manager.get_monster_by_id(boss_id)
                        if boss_info:
                            boss_type = boss_info['name']
                            x = random.randint(0, self.width - 32)
                            y = random.randint(0, self.height - 32)
                            self.monsters.append(Monster(boss_type, x, y))
                            # 显示Boss刷新消息
                            boss_message = f"[Boss刷新] {boss_type} 在 {self.scene_type} 出现了！坐标: ({x}, {y})"
                            print(boss_message)
                            # 在游戏内显示消息
                            if self.game and hasattr(self.game, 'ui') and hasattr(self.game.ui, 'add_game_message'):
                                self.game.ui.add_game_message(boss_message, (255, 0, 0), 5000)
                            boss_spawned = True
                    elif self.scene_type == '地牢':
                        boss_id = random.choice([8, 9])  # 僵尸王或沃玛教主
                        boss_info = id_manager.get_monster_by_id(boss_id)
                        if boss_info:
                            boss_type = boss_info['name']
                            x = random.randint(0, self.width - 32)
                            y = random.randint(0, self.height - 32)
                            self.monsters.append(Monster(boss_type, x, y))
                            # 显示Boss刷新消息
                            boss_message = f"[Boss刷新] {boss_type} 在 {self.scene_type} 出现了！坐标: ({x}, {y})"
                            print(boss_message)
                            # 在游戏内显示消息
                            if self.game and hasattr(self.game, 'ui') and hasattr(self.game.ui, 'add_game_message'):
                                self.game.ui.add_game_message(boss_message, (255, 0, 0), 5000)
                            boss_spawned = True
                
                # 如果没有生成Boss，生成普通怪物
                if not boss_spawned:
                    monster_id = random.choice(monster_ids)
                    monster_info = id_manager.get_monster_by_id(monster_id)
                    if monster_info:
                        monster_type = monster_info['name']
                        x = random.randint(0, self.width - 32)
                        y = random.randint(0, self.height - 32)
                        self.monsters.append(Monster(monster_type, x, y))
    
    def handle_collisions(self):
        """处理碰撞检测"""
        if hasattr(self, 'player') and self.player:
            # 检测玩家与地形元素的碰撞
            self.handle_terrain_collisions()
            # 检测玩家与怪物的碰撞
            self.handle_monster_collisions()
            # 检测玩家与NPC的碰撞
            self.handle_npc_collisions()
    
    def handle_terrain_collisions(self):
        """处理玩家与地形元素的碰撞"""
        if not self.player:
            return
        
        # 玩家碰撞盒
        player_rect = pygame.Rect(
            self.player.x + 4, 
            self.player.y + 6, 
            self.player.width - 8, 
            self.player.height - 12
        )
        
        # 检测与地形元素的碰撞
        for element in self.terrain_elements:
            # 地形元素碰撞盒
            terrain_rect = pygame.Rect(
                element['x'] - 16, 
                element['y'] - 16, 
                32, 
                32
            )
            
            if player_rect.colliderect(terrain_rect):
                # 碰撞发生，将玩家移回碰撞前的位置
                # 这里使用简单的碰撞响应，将玩家推出碰撞区域
                dx = (self.player.x + self.player.width//2) - (element['x'])
                dy = (self.player.y + self.player.height//2) - (element['y'])
                
                if abs(dx) > abs(dy):
                    # 水平碰撞
                    if dx > 0:
                        self.player.x = element['x'] + 20
                    else:
                        self.player.x = element['x'] - self.player.width - 4
                else:
                    # 垂直碰撞
                    if dy > 0:
                        self.player.y = element['y'] + 20
                    else:
                        self.player.y = element['y'] - self.player.height - 4
    
    def handle_monster_collisions(self):
        """处理玩家与怪物的碰撞"""
        if not self.player:
            return
        
        for monster in self.monsters:
            if not monster.is_dead() and self.player.collides_with(monster):
                # 防止玩家被怪物推着走，只让玩家保持原位，怪物反弹
                # 计算玩家中心点
                player_center_x = self.player.x + self.player.width // 2
                player_center_y = self.player.y + self.player.height // 2
                
                # 计算怪物中心点（根据怪物类型调整）
                if hasattr(monster, 'name'):
                    if monster.name in ['狼', '僵尸', '骷髅']:
                        monster_center_x = monster.x + 15
                        monster_center_y = monster.y + 15
                    elif monster.name in ['稻草人', '鸡', '鹿']:
                        monster_center_x = monster.x + 12
                        monster_center_y = monster.y + 12
                    else:
                        monster_center_x = monster.x + 14
                        monster_center_y = monster.y + 14
                else:
                    monster_center_x = monster.x + 14
                    monster_center_y = monster.y + 14
                
                dx = player_center_x - monster_center_x
                dy = player_center_y - monster_center_y
                
                # 计算碰撞深度
                if hasattr(monster, 'name'):
                    if monster.name in ['狼', '僵尸', '骷髅']:
                        overlap_x = (self.player.width//2 + 15) - abs(dx)
                        overlap_y = (self.player.height//2 + 15) - abs(dy)
                    elif monster.name in ['稻草人', '鸡', '鹿']:
                        overlap_x = (self.player.width//2 + 12) - abs(dx)
                        overlap_y = (self.player.height//2 + 12) - abs(dy)
                    else:
                        overlap_x = (self.player.width//2 + 14) - abs(dx)
                        overlap_y = (self.player.height//2 + 14) - abs(dy)
                else:
                    overlap_x = (self.player.width//2 + 14) - abs(dx)
                    overlap_y = (self.player.height//2 + 14) - abs(dy)
                
                if abs(dx) > abs(dy):
                    # 水平碰撞
                    if dx > 0:
                        # 玩家在怪物右侧，怪物向左移动
                        monster.x -= overlap_x
                    else:
                        # 玩家在怪物左侧，怪物向右移动
                        monster.x += overlap_x
                else:
                    # 垂直碰撞
                    if dy > 0:
                        # 玩家在怪物下方，怪物向上移动
                        monster.y -= overlap_y
                    else:
                        # 玩家在怪物上方，怪物向下移动
                        monster.y += overlap_y
    
    def handle_npc_collisions(self):
        """处理玩家与NPC的碰撞"""
        if not self.player:
            return
        
        for npc in self.npcs:
            # NPC碰撞盒
            npc_rect = pygame.Rect(npc.x - 12, npc.y - 12, 24, 24)
            player_rect = pygame.Rect(
                self.player.x + 4, 
                self.player.y + 4, 
                self.player.width - 8, 
                self.player.height - 8
            )
            
            if player_rect.colliderect(npc_rect):
                # 简单的碰撞响应
                dx = self.player.x - npc.x
                dy = self.player.y - npc.y
                distance = (dx**2 + dy**2)**0.5
                if distance > 0:
                    push_distance = 1
                    self.player.x += (dx / distance) * push_distance
                    self.player.y += (dy / distance) * push_distance
    
    def render(self, screen, camera_x, camera_y):
        """渲染地图"""
        # 绘制背景（参考传奇游戏的像素风格）
        if self.scene_type == '村庄':
            # 村庄背景，使用更真实的草地纹理
            screen.fill((80, 140, 90))
            # 绘制草地纹理（只绘制可见区域）
            start_x = max(0, camera_x // 32) * 32
            end_x = min(self.width, (camera_x + 1024) // 32 * 32 + 32)
            start_y = max(0, camera_y // 32) * 32
            end_y = min(self.height, (camera_y + 768) // 32 * 32 + 32)
            
            for x in range(start_x, end_x, 32):
                for y in range(start_y, end_y, 32):
                    # 使用基于坐标的固定模式，避免闪烁
                    grass_type = (x // 32 + y // 32) % 4
                    if grass_type == 0:
                        color = (90, 150, 100)  # 深绿色
                    elif grass_type == 1:
                        color = (100, 160, 110)  # 中绿色
                    elif grass_type == 2:
                        color = (110, 170, 120)  # 浅绿色
                    else:
                        color = (85, 145, 95)  # 暗绿色
                    pygame.draw.rect(screen, color, (x - camera_x, y - camera_y, 32, 32))
                    # 添加固定的草地细节
                    if (x // 64 + y // 64) % 2 == 0:
                        detail_color = (70, 130, 80)
                        detail_size = 6
                        detail_x = (x // 32) % 24
                        detail_y = (y // 32) % 24
                        pygame.draw.rect(screen, detail_color, (x - camera_x + detail_x, y - camera_y + detail_y, detail_size, detail_size))
            
            # 绘制区域标识
            regions = [
                {"name": "村庄中心", "x": 500, "y": 300, "color": (255, 215, 0)},
                {"name": "武器店区域", "x": 200, "y": 200, "color": (255, 165, 0)},
                {"name": "药店区域", "x": 300, "y": 300, "color": (0, 255, 0)},
                {"name": "防具店区域", "x": 400, "y": 400, "color": (0, 191, 255)},
                {"name": "教堂区域", "x": 600, "y": 500, "color": (255, 105, 180)}
            ]
            
            for region in regions:
                # 检查区域是否在可见范围内
                if camera_x - 200 < region["x"] < camera_x + 1024 and camera_y - 100 < region["y"] < camera_y + 768:
                    # 绘制区域名称
                    try:
                        font = pygame.font.SysFont('hiraginosansgb', 18)
                    except:
                        try:
                            font = pygame.font.SysFont('songti', 18)
                        except:
                            try:
                                font = pygame.font.SysFont('arialunicode', 18)
                            except:
                                font = pygame.font.Font(None, 18)
                    
                    text = font.render(region["name"], True, region["color"])
                    text_rect = text.get_rect()
                    text_x = region["x"] - text_rect.width // 2 - camera_x
                    text_y = region["y"] - 30 - camera_y
                    
                    # 绘制文字背景
                    bg_rect = pygame.Rect(text_x - 5, text_y - 5, text_rect.width + 10, text_rect.height + 10)
                    pygame.draw.rect(screen, (0, 0, 0, 150), bg_rect, border_radius=5)
                    # 绘制文字
                    screen.blit(text, (text_x, text_y))
                    
                    # 绘制区域范围指示器
                    indicator_rect = pygame.Rect(region["x"] - 100 - camera_x, region["y"] - 100 - camera_y, 200, 200)
                    pygame.draw.rect(screen, region["color"], indicator_rect, 1, border_radius=10)
        elif self.scene_type == '森林':
            # 森林背景
            screen.fill((60, 100, 70))
            # 绘制森林纹理（只绘制可见区域）
            start_x = max(0, camera_x // 32) * 32
            end_x = min(self.width, (camera_x + 1024) // 32 * 32 + 32)
            start_y = max(0, camera_y // 32) * 32
            end_y = min(self.height, (camera_y + 768) // 32 * 32 + 32)
            
            for x in range(start_x, end_x, 32):
                for y in range(start_y, end_y, 32):
                    # 使用基于坐标的固定模式，避免闪烁
                    forest_type = (x // 32 + y // 32) % 3
                    if forest_type == 0:
                        color = (70, 110, 80)  # 深林色
                    elif forest_type == 1:
                        color = (80, 120, 90)  # 中林色
                    else:
                        color = (65, 105, 75)  # 暗林色
                    pygame.draw.rect(screen, color, (x - camera_x, y - camera_y, 32, 32))
                    # 添加固定的落叶细节
                    if (x // 48 + y // 48) % 2 == 0:
                        leaf_color = (180, 100, 50) if (x // 32) % 2 == 0 else (160, 80, 40)
                        leaf_size = 4
                        leaf_x = (x // 32) % 28
                        leaf_y = (y // 32) % 28
                        pygame.draw.rect(screen, leaf_color, (x - camera_x + leaf_x, y - camera_y + leaf_y, leaf_size, leaf_size))
            
            # 绘制树木（只绘制可见区域）
            for x in range(100, self.width, 150):
                for y in range(100, self.height, 150):
                    # 检查树木是否在可见区域内
                    if camera_x - 100 < x < camera_x + 1124 and camera_y - 100 < y < camera_y + 868:
                        # 更真实的树干
                        trunk_color = (100, 60, 20)
                        pygame.draw.rect(screen, trunk_color, (x - 12 - camera_x, y - 40 - camera_y, 24, 60))
                        # 添加树干纹理
                        for i in range(0, 60, 8):
                            texture_color = (90, 50, 15)
                            pygame.draw.line(screen, texture_color, (x - 12 - camera_x, y - 40 + i - camera_y), (x + 11 - camera_x, y - 40 + i - camera_y), 2)
                        # 更真实的树叶
                        leaf_color = (40, 90, 50)
                        pygame.draw.circle(screen, leaf_color, (x - camera_x, y - 50 - camera_y), 40)
                        # 添加树叶细节
                        for i in range(8):
                            detail_color = (30, 80, 40)
                            detail_radius = random.randint(12, 20)
                            offset_x = random.randint(-30, 30)
                            offset_y = random.randint(-30, 30)
                            pygame.draw.circle(screen, detail_color, (x + offset_x - camera_x, y - 50 + offset_y - camera_y), detail_radius)
        elif self.scene_type == '沙漠':
            # 沙漠背景
            screen.fill((170, 150, 110))
            # 绘制沙地纹理（只绘制可见区域）
            start_x = max(0, camera_x // 32) * 32
            end_x = min(self.width, (camera_x + 1024) // 32 * 32 + 32)
            start_y = max(0, camera_y // 32) * 32
            end_y = min(self.height, (camera_y + 768) // 32 * 32 + 32)
            
            for x in range(start_x, end_x, 32):
                for y in range(start_y, end_y, 32):
                    # 使用基于坐标的固定模式，避免闪烁
                    desert_type = (x // 32 + y // 32) % 4
                    if desert_type == 0:
                        color = (180, 160, 120)  # 亮沙色
                    elif desert_type == 1:
                        color = (170, 150, 110)  # 中沙色
                    elif desert_type == 2:
                        color = (160, 140, 100)  # 暗沙色
                    else:
                        color = (175, 155, 115)  # 浅沙色
                    pygame.draw.rect(screen, color, (x - camera_x, y - camera_y, 32, 32))
                    # 添加固定的沙子细节
                    if (x // 48 + y // 48) % 2 == 0:
                        detail_color = (160, 140, 100)
                        detail_size = 4
                        detail_x = (x // 32) % 24
                        detail_y = (y // 32) % 24
                        pygame.draw.rect(screen, detail_color, (x - camera_x + detail_x, y - camera_y + detail_y, detail_size, detail_size))
        elif self.scene_type == '地牢':
            # 地牢背景
            screen.fill((50, 50, 50))
            # 绘制砖块纹理（只绘制可见区域）
            start_x = max(0, camera_x // 32) * 32
            end_x = min(self.width, (camera_x + 1024) // 32 * 32 + 32)
            start_y = max(0, camera_y // 32) * 32
            end_y = min(self.height, (camera_y + 768) // 32 * 32 + 32)
            
            for x in range(start_x, end_x, 32):
                for y in range(start_y, end_y, 32):
                    # 使用基于坐标的固定模式，避免闪烁
                    brick_type = (x // 32 + y // 32) % 3
                    if brick_type == 0:
                        color = (60, 60, 60)  # 亮砖色
                    elif brick_type == 1:
                        color = (50, 50, 50)  # 中砖色
                    else:
                        color = (40, 40, 40)  # 暗砖色
                    pygame.draw.rect(screen, color, (x - camera_x, y - camera_y, 32, 32))
                    # 添加砖块纹理
                    mortar_color = (30, 30, 30)
                    pygame.draw.rect(screen, mortar_color, (x - camera_x, y - camera_y, 32, 3))
                    pygame.draw.rect(screen, mortar_color, (x - camera_x, y + 29 - camera_y, 32, 3))
                    pygame.draw.rect(screen, mortar_color, (x - camera_x, y - camera_y, 3, 32))
                    pygame.draw.rect(screen, mortar_color, (x + 29 - camera_x, y - camera_y, 3, 32))
        elif self.scene_type == '雪原':
            # 雪原背景
            screen.fill((200, 220, 240))
            # 绘制雪地纹理（只绘制可见区域）
            start_x = max(0, camera_x // 32) * 32
            end_x = min(self.width, (camera_x + 1024) // 32 * 32 + 32)
            start_y = max(0, camera_y // 32) * 32
            end_y = min(self.height, (camera_y + 768) // 32 * 32 + 32)
            
            for x in range(start_x, end_x, 32):
                for y in range(start_y, end_y, 32):
                    # 使用基于坐标的固定模式，避免闪烁
                    snow_type = (x // 32 + y // 32) % 4
                    if snow_type == 0:
                        color = (210, 230, 250)  # 亮雪色
                    elif snow_type == 1:
                        color = (200, 220, 240)  # 中雪色
                    elif snow_type == 2:
                        color = (190, 210, 230)  # 暗雪色
                    else:
                        color = (205, 225, 245)  # 浅雪色
                    pygame.draw.rect(screen, color, (x - camera_x, y - camera_y, 32, 32))
                    # 添加固定的雪花细节
                    if (x // 48 + y // 48) % 2 == 0:
                        snow_color = (255, 255, 255)
                        snow_size = 4
                        snow_x = (x // 32) % 30
                        snow_y = (y // 32) % 30
                        pygame.draw.circle(screen, snow_color, (x - camera_x + snow_x, y - camera_y + snow_y), snow_size)
        
        # 绘制道路（更真实的道路）
        road_left = 350 - camera_x
        road_top = 0 - camera_y
        road_width = 150
        road_height = self.height
        if road_left < 1024 and road_left + road_width > 0 and road_top < 768 and road_top + road_height > 0:
            # 道路基础色
            road_color = (140, 120, 90)
            pygame.draw.rect(screen, road_color, (road_left, road_top, road_width, road_height))
            # 道路纹理
            for x in range(350, 500, 32):
                for y in range(0, self.height, 32):
                    # 检查道路纹理是否在可见区域内
                    if camera_x < x < camera_x + 1024 and camera_y < y < camera_y + 768:
                        # 使用基于坐标的固定模式，避免闪烁
                        road_type = (x // 32 + y // 32) % 3
                        if road_type == 0:
                            color = (150, 130, 100)  # 亮路色
                        elif road_type == 1:
                            color = (140, 120, 90)  # 中路色
                        else:
                            color = (130, 110, 80)  # 暗路色
                        pygame.draw.rect(screen, color, (x - camera_x, y - camera_y, 32, 32))
                        # 添加固定的道路细节
                        if (x // 48 + y // 48) % 2 == 0:
                            detail_color = (120, 100, 70)
                            detail_size = 6
                            detail_x = (x // 32) % 24
                            detail_y = (y // 32) % 24
                            pygame.draw.rect(screen, detail_color, (x - camera_x + detail_x, y - camera_y + detail_y, detail_size, detail_size))
            
            # 绘制道路文字说明
            try:
                road_font = pygame.font.SysFont('hiraginosansgb', 16)
            except:
                try:
                    road_font = pygame.font.SysFont('songti', 16)
                except:
                    try:
                        road_font = pygame.font.SysFont('arialunicode', 16)
                    except:
                        road_font = pygame.font.Font(None, 16)
            
            # 道路名称
            road_name = "中央大道"
            road_text = road_font.render(road_name, True, (255, 255, 255))
            road_text_rect = road_text.get_rect()
            road_text_x = 350 + road_width // 2 - road_text_rect.width // 2 - camera_x
            road_text_y = 100 - camera_y
            
            # 绘制文字背景
            bg_rect = pygame.Rect(road_text_x - 10, road_text_y - 5, road_text_rect.width + 20, road_text_rect.height + 10)
            pygame.draw.rect(screen, (100, 80, 60, 180), bg_rect, border_radius=5)
            # 绘制文字
            screen.blit(road_text, (road_text_x, road_text_y))
            
            # 道路方向指示
            directions = [
                ("向北: 森林", 200),
                ("向南: 地牢", 1000),
                ("向东: 沙漠", 600),
                ("向西: 雪原", 600)
            ]
            
            for direction_text, y_pos in directions:
                if camera_y - 50 < y_pos < camera_y + 768:
                    dir_text = road_font.render(direction_text, True, (255, 255, 255))
                    dir_text_rect = dir_text.get_rect()
                    dir_text_x = 350 + road_width // 2 - dir_text_rect.width // 2 - camera_x
                    dir_text_y = y_pos - camera_y
                    
                    # 绘制文字背景
                    dir_bg_rect = pygame.Rect(dir_text_x - 8, dir_text_y - 4, dir_text_rect.width + 16, dir_text_rect.height + 8)
                    pygame.draw.rect(screen, (100, 80, 60, 150), dir_bg_rect, border_radius=3)
                    # 绘制文字
                    screen.blit(dir_text, (dir_text_x, dir_text_y))
        
        # 绘制地形元素
        for element in self.terrain_elements:
            # 检查元素是否在可见区域内
            if camera_x - 80 < element['x'] < camera_x + 880 and camera_y - 80 < element['y'] < camera_y + 680:
                if element['type'] == 'tree':
                    # 使用树素材
                    if not self.use_default_assets and 'tree' in self.map_assets['terrain']:
                        tree_image = self.map_assets['terrain']['tree']
                        # 计算树的绘制位置（居中）
                        tree_rect = tree_image.get_rect(center=(element['x'] - camera_x, element['y'] - camera_y))
                        screen.blit(tree_image, tree_rect)
                    else:
                        # 回退到默认绘制
                        trunk_color = (100, 60, 20)
                        pygame.draw.rect(screen, trunk_color, (element['x'] - 5 - camera_x, element['y'] - 20 - camera_y, 10, 30))
                        leaf_color = (0, 120, 0)
                        pygame.draw.circle(screen, leaf_color, (element['x'] - camera_x, element['y'] - 25 - camera_y), 20)
                elif element['type'] == 'rock':
                    # 使用岩石素材
                    if not self.use_default_assets and 'rock' in self.map_assets['terrain']:
                        rock_image = self.map_assets['terrain']['rock']
                        # 计算岩石的绘制位置（居中）
                        rock_rect = rock_image.get_rect(center=(element['x'] - camera_x, element['y'] - camera_y))
                        screen.blit(rock_image, rock_rect)
                    else:
                        # 回退到默认绘制
                        rock_color = (100, 100, 100)
                        pygame.draw.circle(screen, rock_color, (element['x'] - camera_x, element['y'] - camera_y), 15)
                elif element['type'] == 'house':
                    # 使用房子素材
                    if not self.use_default_assets and 'house' in self.map_assets['terrain']:
                        house_image = self.map_assets['terrain']['house']
                        # 计算房子的绘制位置（居中）
                        house_rect = house_image.get_rect(center=(element['x'] - camera_x, element['y'] - camera_y))
                        screen.blit(house_image, house_rect)
                    else:
                        # 回退到默认绘制
                        wall_color = (150, 100, 50)
                        pygame.draw.rect(screen, wall_color, (element['x'] - 30 - camera_x, element['y'] - 20 - camera_y, 60, 40))
                        roof_color = (200, 150, 100)
                        pygame.draw.polygon(screen, roof_color, [(element['x'] - 35 - camera_x, element['y'] - 20 - camera_y), (element['x'] + 35 - camera_x, element['y'] - 20 - camera_y), (element['x'] - camera_x, element['y'] - 50 - camera_y)])
                elif element['type'] == 'well':
                    # 更真实的水井
                    # 水井底座
                    base_color = (100, 100, 100)
                    pygame.draw.circle(screen, base_color, (element['x'] - camera_x, element['y'] - camera_y), 18)
                    # 水井边缘
                    edge_color = (120, 120, 120)
                    pygame.draw.circle(screen, edge_color, (element['x'] - camera_x, element['y'] - camera_y), 18, 2)
                    # 水井水面
                    water_color = (0, 0, 120)
                    pygame.draw.circle(screen, water_color, (element['x'] - camera_x, element['y'] - camera_y), 12)
                    # 水井辘轳
                    pulley_color = (80, 80, 80)
                    pygame.draw.rect(screen, pulley_color, (element['x'] - 25 - camera_x, element['y'] - 10 - camera_y, 50, 8))
                    pygame.draw.circle(screen, pulley_color, (element['x'] - camera_x, element['y'] - 6 - camera_y), 6)
                    # 水井绳子
                    rope_color = (100, 80, 60)
                    pygame.draw.line(screen, rope_color, (element['x'] - camera_x, element['y'] - 6 - camera_y), (element['x'] - camera_x, element['y'] - camera_y), 1)
                elif element['type'] == 'altar':
                    # 更真实的祭坛
                    # 祭坛底座
                    base_color = (180, 180, 180)
                    pygame.draw.rect(screen, base_color, (element['x'] - 30 - camera_x, element['y'] - 20 - camera_y, 60, 35))
                    # 祭坛顶部
                    top_color = (200, 200, 200)
                    pygame.draw.rect(screen, top_color, (element['x'] - 25 - camera_x, element['y'] - 25 - camera_y, 50, 10))
                    # 祭坛宝石
                    gem_color = (255, 215, 0)
                    pygame.draw.circle(screen, gem_color, (element['x'] - camera_x, element['y'] - 10 - camera_y), 12)
                    # 添加祭坛纹理
                    for i in range(0, 35, 5):
                        texture_color = (160, 160, 160)
                        pygame.draw.line(screen, texture_color, (element['x'] - 30 - camera_x, element['y'] - 20 + i - camera_y), (element['x'] + 29 - camera_x, element['y'] - 20 + i - camera_y), 1)
                    # 添加宝石光芒
                    for i in range(4):
                        glow_color = (255, 235, 100)
                        glow_radius = 15 + i * 3
                        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                        pygame.draw.circle(glow_surface, (glow_color[0], glow_color[1], glow_color[2], 30 - i * 5), (glow_radius, glow_radius), glow_radius)
                        screen.blit(glow_surface, (element['x'] - glow_radius - camera_x, element['y'] - glow_radius - 10 - camera_y))
        
        # 绘制NPC（只绘制可见区域）
        for npc in self.npcs:
            # 检查NPC是否在可见区域内
            if camera_x - 50 < npc.x < camera_x + 850 and camera_y - 50 < npc.y < camera_y + 650:
                # 保存NPC的原始位置
                original_x, original_y = npc.x, npc.y
                # 应用相机偏移
                npc.x -= camera_x
                npc.y -= camera_y
                # 渲染NPC
                npc.render(screen)
                # 恢复NPC的原始位置
                npc.x, npc.y = original_x, original_y
        
        # 绘制怪物（只绘制可见区域）
        for monster in self.monsters:
            if not monster.is_dead():
                # 检查怪物是否在可见区域内
                if camera_x - 50 < monster.x < camera_x + 850 and camera_y - 50 < monster.y < camera_y + 650:
                    # 保存怪物的原始位置
                    original_x, original_y = monster.x, monster.y
                    # 应用相机偏移
                    monster.x -= camera_x
                    monster.y -= camera_y
                    # 渲染怪物
                    monster.render(screen)
                    # 恢复怪物的原始位置
                    monster.x, monster.y = original_x, original_y
        
        # 绘制传送点标识
        try:
            font = pygame.font.SysFont('hiraginosansgb', 20)
        except:
            try:
                font = pygame.font.SysFont('songti', 20)
            except:
                try:
                    font = pygame.font.SysFont('arialunicode', 20)
                except:
                    font = pygame.font.Font(None, 20)
        
        for exit in self.exits:
            # 检查传送点是否在可见区域内
            if camera_x - 150 < exit['x'] < camera_x + 1174 and camera_y - 100 < exit['y'] < camera_y + 868:
                # 根据方向获取传送点名称
                direction_map = {
                    'north': '北部森林',
                    'east': '东部沙漠',
                    'south': '南部地牢',
                    'west': '西部荒野'
                }
                destination = direction_map.get(exit['direction'], '未知区域')
                
                # 绘制传送点地面标记（更明显的效果）
                marker_x = exit['x'] + exit['width'] // 2 - 50 - camera_x
                marker_y = exit['y'] + exit['height'] // 2 - 25 - camera_y
                
                # 绘制发光效果
                glow_surface = pygame.Surface((100, 50), pygame.SRCALPHA)
                for i in range(3):
                    alpha = 40 - i * 10
                    pygame.draw.rect(glow_surface, (255, 215, 0, alpha), (i*2, i*2, 100 - i*4, 50 - i*4), border_radius=5)
                screen.blit(glow_surface, (marker_x, marker_y))
                
                # 绘制传送点边框
                pygame.draw.rect(screen, (255, 215, 0), (marker_x, marker_y, 100, 50), 2, border_radius=5)
                # 绘制传送点背景
                pygame.draw.rect(screen, (120, 100, 80, 150), (marker_x, marker_y, 100, 50), border_radius=5)
                
                # 绘制传送点文字
                text = font.render(f'传送至: {destination}', True, (255, 255, 255))
                text_rect = text.get_rect()
                text_x = exit['x'] + exit['width'] // 2 - text_rect.width // 2 - camera_x
                text_y = exit['y'] + exit['height'] // 2 - text_rect.height // 2 - camera_y
                screen.blit(text, (text_x, text_y))
                
                # 绘制方向指示箭头
                arrow_font = pygame.font.Font(None, 24)
                arrow_text = arrow_font.render('↓', True, (255, 215, 0))
                arrow_rect = arrow_text.get_rect()
                arrow_x = exit['x'] + exit['width'] // 2 - arrow_rect.width // 2 - camera_x
                arrow_y = exit['y'] + exit['height'] // 2 + text_rect.height // 2 + 5 - camera_y
                screen.blit(arrow_text, (arrow_x, arrow_y))
    
    def set_player(self, player):
        """设置玩家引用"""
        self.player = player
        player.map = self  # 设置玩家的地图引用
    
    def get_monsters_near_player(self, player, distance=100):
        """获取靠近玩家的怪物"""
        near_monsters = []
        # 计算玩家中心点
        player_center_x = player.x + player.width // 2
        player_center_y = player.y + player.height // 2
        
        for monster in self.monsters:
            # 计算怪物中心点（根据怪物类型调整尺寸）
            if hasattr(monster, 'name'):
                if monster.name in ['狼', '僵尸', '骷髅']:
                    monster_width, monster_height = 36, 36
                elif monster.name in ['稻草人', '鸡', '鹿']:
                    monster_width, monster_height = 28, 28
                else:
                    monster_width, monster_height = 32, 32
            else:
                monster_width, monster_height = 32, 32
            
            monster_center_x = monster.x + monster_width // 2
            monster_center_y = monster.y + monster_height // 2
            
            # 使用中心点计算距离
            dx = player_center_x - monster_center_x
            dy = player_center_y - monster_center_y
            dist = (dx**2 + dy**2)**0.5
            if dist < distance:
                near_monsters.append(monster)
        return near_monsters
    
    def get_npcs_near_player(self, player, distance=50):
        """获取靠近玩家的NPC"""
        near_npcs = []
        for npc in self.npcs:
            dx = player.x - npc.x
            dy = player.y - npc.y
            dist = (dx**2 + dy**2)**0.5
            if dist < distance:
                near_npcs.append(npc)
        return near_npcs
    
    def get_monster_at_position(self, x, y, distance=30):
        """根据位置获取怪物
        
        Args:
            x: 世界坐标X
            y: 世界坐标Y
            distance: 检测距离
            
        Returns:
            Monster对象或None
        """
        # 优先检测Boss怪物
        for monster in self.monsters:
            if not monster.is_dead():
                # 检查是否是Boss怪物
                is_boss = False
                if hasattr(monster, 'name'):
                    if '王' in monster.name or '教主' in monster.name:
                        is_boss = True
                
                # 为Boss使用更大的检测距离
                if is_boss:
                    boss_distance = 40  # Boss使用更大的检测距离
                    dx = x - monster.x
                    dy = y - monster.y
                    dist = (dx**2 + dy**2)**0.5
                    if dist < boss_distance:
                        return monster
        
        # 然后检测普通怪物
        for monster in self.monsters:
            if not monster.is_dead():
                # 跳过已经检查过的Boss
                is_boss = False
                if hasattr(monster, 'name'):
                    if '王' in monster.name or '教主' in monster.name:
                        is_boss = True
                if not is_boss:
                    dx = x - monster.x
                    dy = y - monster.y
                    dist = (dx**2 + dy**2)**0.5
                    if dist < distance:
                        return monster
        
        return None
    
    def check_exit(self, player):
        """检查玩家是否进入了地图出口"""
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        for exit in self.exits:
            exit_rect = pygame.Rect(exit['x'], exit['y'], exit['width'], exit['height'])
            if player_rect.colliderect(exit_rect):
                return exit
        return None