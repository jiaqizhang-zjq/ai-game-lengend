import pygame
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game import Game


def main():
    """主函数"""
    # 初始化游戏
    game = Game()
    
    # 游戏主循环
    while game.running:
        game.handle_events()
        game.update()
        game.render()
    
    # 退出游戏
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()