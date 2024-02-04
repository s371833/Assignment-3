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


## pip install pygame
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT - 50)
        self.speed = 5
        self.jump_height = -15
        self.gravity = 1
        self.vel_y = 0
        self.health = 100
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.rect.bottom >= HEIGHT:
            self.vel_y = self.jump_height

        # Apply gravity
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

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
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 100, HEIGHT - 50)
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.y = HEIGHT - 50

# Game initialization
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scrolling Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

all_sprites.add(player)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Shoot projectile when space key is pressed
            projectile = Projectile(player.rect.right, player.rect.centery)
            all_sprites.add(projectile)
            projectiles.add(projectile)

    # Update
    all_sprites.update()
    enemies.update()
    projectiles.update()

    # Collision detection
    hits = pygame.sprite.groupcollide(enemies, projectiles, True, True)
    for hit in hits:
        # Increase score or handle other actions
        pass

    # Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    enemies.draw(screen)
    projectiles.draw(screen)

    # Display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()


# In[ ]:




