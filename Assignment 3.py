#!/usr/bin/env python
# coding: utf-8

# #### Question 1

# In[1]:


import tkinter as tk

class Video:
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration

    def play(self):
        pass

class YouTubeVideo(Video):
    def __init__(self, title, duration, video_id):
        super().__init__(title, duration)
        self.video_id = video_id

    # Method overriding
    def play(self):
        print(f"Playing YouTube video: {self.title} (ID: {self.video_id})")

class LocalVideo(Video):
    def __init__(self, title, duration, file_path):
        super().__init__(title, duration)
        self.file_path = file_path

    # Method overriding
    def play(self):
        print(f"Playing local video: {self.title} (File: {self.file_path})")

class VideoPlayer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Video Player")
        self.geometry("400x300")

        # Encapsulation: Creating private variables
        self._current_video = None

        # Polymorphism: Using a generic play button
        self.play_button = tk.Button(self, text="Play Video", command=self.play_video)
        self.play_button.pack(pady=10)

    # Method overriding
    def play_video(self):
        if isinstance(self._current_video, Video):
            self._current_video.play()
        else:
            print("No video selected.")

if __name__ == "__main__":
    # Usage of multiple inheritance not demonstrated in this example

    app = VideoPlayer()
    
    # Polymorphism: Different types of videos can be assigned
    youtube_video = YouTubeVideo("Python Basics", "10:00", "xyz123")
    local_video = LocalVideo("Intro to Tkinter", "05:30", "intro_tkinter.mp4")

    # Encapsulation: Assigning a video to the VideoPlayer instance
    app._current_video = youtube_video

    app.mainloop()


# #### Question 2

# In[2]:

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GROUND_HEIGHT = 50
GRAVITY = 1

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT - GROUND_HEIGHT - 25)
        self.speed = 5
        self.jump_height = -15
        self.vel_y = 0
        self.health = 100
        self.lives = 3

    def update(self):
        self.handle_input()
        self.apply_gravity()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            self.vel_y = self.jump_height

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        if self.rect.bottom > HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 100, HEIGHT - GROUND_HEIGHT - 25)
        self.speed = 3

    def update(self):
        self.move_left_wrap()

    def move_left_wrap(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.y = HEIGHT - GROUND_HEIGHT - 25

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Initialize game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scrolling Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            projectile = Projectile(player.rect.right, player.rect.centery)
            all_sprites.add(projectile)
            projectiles.add(projectile)

    # Add enemies randomly
    if random.randint(1, 100) < 2:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Add collectibles randomly
    if random.randint(1, 100) < 1:
        collectible = Collectible(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - GROUND_HEIGHT - 50))
        all_sprites.add(collectible)
        collectibles.add(collectible)

    # Update
    all_sprites.update()
    enemies.update()
    projectiles.update()

    # Collision detection
    hits_projectile_enemy = pygame.sprite.groupcollide(enemies, projectiles, True, True)
    for hit in hits_projectile_enemy:
        # Increase score or handle other actions
        pass

    hits_player_collectible = pygame.sprite.spritecollide(player, collectibles, True)
    for hit in hits_player_collectible:
        # Increase score or handle other actions (e.g., health boost)
        pass

    # Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # Display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()


# In[ ]:




