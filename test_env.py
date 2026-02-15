#!/usr/bin/env python3
import pygame
import os
import sys

print("Testing environment...")
print(f"Python version: {sys.version}")
print(f"Pygame version: {pygame.version.ver}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")

# Try to initialize pygame
print("Initializing pygame...")
pygame.init()
print("Pygame initialized")

# Try to create a window
print("Creating window...")
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Test Window")
print("Window created")

# Fill the window with a color
screen.fill((255, 0, 0))
pygame.display.flip()
print("Window filled with red")

# Wait for 2 seconds
import time
time.sleep(2)

# Quit pygame
pygame.quit()
print("Pygame quit")
print("Test completed successfully!")