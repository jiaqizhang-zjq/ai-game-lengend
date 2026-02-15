import pygame
import sys
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('字体测试')
clock = pygame.time.Clock()

print('当前工作目录:', os.getcwd())
print('字体文件路径:', 'assets/fonts/NotoSansCJKsc-Regular.otf')
print('字体文件是否存在:', os.path.exists('assets/fonts/NotoSansCJKsc-Regular.otf'))

try:
    font = pygame.font.Font('assets/fonts/NotoSansCJKsc-Regular.otf', 48)
    print('字体加载成功！')
    
    text = font.render('传奇游戏 - 中文测试', True, (255, 215, 0))
    print('文字渲染成功！')
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((50, 50, 50))
        screen.blit(text, (200, 200))
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()
except Exception as e:
    print('错误:', e)
    import traceback
    traceback.print_exc()
    pygame.quit()
    sys.exit(1)
