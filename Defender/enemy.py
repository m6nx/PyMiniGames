# Imports
import pygame
from random import randint

# Enemies
class Enemy(pygame.sprite.Sprite):

    def __init__(self, name, hp, animation_list, x, y, speed, rect):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.name = name
        self.hp = hp
        self.last_attack = pygame.time.get_ticks() # Time in milliseconds
        self.cooldown = 1000 # Attack cooldown
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0 # 0- move 1- attack 2- death
        self.update_time = pygame.time.get_ticks()

        # Select starting image
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = rect
        self.rect.center = (x, y)

        # Bomb
        self.bomb_image = pygame.image.load('Defender/img/graphics/bomb.png').convert_alpha()
        self.bomb_rect = self.bomb_image.get_rect()
        self.bomb_rect.center = (randint(180,260), 80) # Bomb position
        self.bomb_active = False

    
    def update(self, surface, target, bullet_group):
        if self.alive:

            # Check collision
            if pygame.sprite.spritecollide(self, bullet_group, True): # True - delete bullet if hit
                # Deal damage to enemy
                self.hp -= 20
                # Knockback
                self.rect.x += 5

            # If attack mode and enemy gets knocked back, start walking again
            if self.action == 1 and self.rect.left > target.rect.right - 170:
                self.update_action(0)

            # If enemy is reached the castle (Attack position)
            if self.rect.left < target.rect.right - 170:
                self.update_action(1) # attack action

                # If enemy is bird, keep moving when reached the castle
                if self.name == 'bird':
                    self.update_action(0) # moving action
                    # If bird is on top of the castle, trigger bomb
                    if self.rect.left < target.rect.right - 270 and self.rect.right > 0:
                        self.bomb_active = True

            # Penguin attack position
            if self.name == 'penguin' and self.rect.left < target.rect.right + 250:
                self.update_action(1) # attack action
            
            # Elephant attack position
            if self.name == 'elephant' and self.rect.left < target.rect.right - 100:
                self.update_action(1) # attack action

            # Saurus attack position
            if self.name == 'saurus' and self.rect.left < target.rect.right:
                self.update_action(1) # attack action

            # Bomb trigger
            if self.bomb_active:
                self.bomb_rect.y += 3
                surface.blit(self.bomb_image, self.bomb_rect)
                # If bird gets out of the screen, deal damage and kill it
                if self.rect.right < -5 and self.action == 0:
                    target.hp -= 100
                    target.hp_green -= 30  
                    self.alive = False
                    self.bomb_active = False
                    # Stop hp from going negative
                    if target.hp <= 0:
                        target.hp = 0
                
            # Enemy walk action
            if self.action == 0:
                self.rect.x -= self.speed

            # Enemy attack action
            if self.action == 1:
                # Attack cooldown (1 second)
                if pygame.time.get_ticks() - self.last_attack > self.cooldown:
                    # Deal damage based on enemy type
                    if self.name == 'crab':
                        target.hp -= 20
                        target.hp_green -= 6
                    if self.name == 'turtle':
                        target.hp -= 35
                        target.hp_green -= 10.5
                    if self.name == 'ant':
                        target.hp -= 15
                        target.hp_green -= 4.5
                    if self.name == 'penguin':
                        target.hp -= 20
                        target.hp_green -= 6
                    if self.name == 'duck':
                        target.hp -= 15
                        target.hp_green -= 4.5
                    if self.name == 'crocodile':
                        target.hp -= 30
                        target.hp_green -= 9
                    if self.name == 'elephant':
                        target.hp -= 40
                        target.hp_green -= 12
                    if self.name == 'saurus':
                        target.hp -= 25
                        target.hp_green -= 7.5
                        
                    # Stop hp from going negative 
                    if target.hp < 0:
                        target.hp = 0
                    
                    # Attack timer
                    self.last_attack = pygame.time.get_ticks()

            # Enemy death
            if self.hp <= 0:
                target.kills += 1
                self.update_action(2) # death action
                self.alive = False
                # Sandcastle money based on which enemy is killed
                if self.name == 'crab':
                    target.money += 20
                if self.name == 'turtle':
                    target.money += 25
                if self.name == 'bird':
                    target.money += 10
                if self.name == 'ant':
                    target.money += 15
                if self.name == 'penguin':
                    target.money += 30
                if self.name == 'duck':
                    target.money += 25
                if self.name == 'crocodile':
                    target.money += 30
                if self.name == 'elephant':
                    target.money += 40
                if self.name == 'saurus':
                    target.money += 30

        # Update animation frames
        self.update_animation()

        # Draw enemy on screen
        # pygame.draw.rect(surface, "red", self.rect, 1) # Hitbox
        surface.blit(self.image, (self.rect.x - 12, self.rect.y - 17))

    # Update enemy animations
    def update_animation(self):   
        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]
          
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
          self.update_time = pygame.time.get_ticks()
          self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # If new action is different than last one
        if new_action != self.action:
            # Start new action
            self.action = new_action
            # Reset animation frames to start
            self.frame_index = 0
            self.update_date = pygame.time.get_ticks()
