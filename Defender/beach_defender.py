# Imports
import pygame
import math
import os
from enemy import Enemy
from button import Button
from random import randint

# Initialize game
pygame.init()

# Display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Beach Defender")

# Fonts
font_20 = pygame.font.SysFont('Futura', 20) 
font_30 = pygame.font.SysFont('Futura', 30) 
font_60 = pygame.font.SysFont('Futura', 60) 
# print(pygame.font.get_fonts())

# Game variables
# Level
level = 1
high_score = 0
level_difficulty = 0
target_difficulty = 1000 # Each level difficulty is calculated by enemy hp
DIFFICULTY_MULTIPLIER = 1.07 # Each level is 7% harder
game_over = False
next_level = False
# Enemies
ENEMY_TIMER = 700 # Spawn cooldown
last_enemy = pygame.time.get_ticks()
enemies_alive = 0
# Cannons
CANNON_COST = 3000
MAX_CANNONS = 4
cannon_positions = [
    [287, 482],
    [221, 480],
    [85, 482],
    [137, 412]
]

# Load high score
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())

# Load map images
backround_img = pygame.image.load('Defender/img/graphics/beach_backround.jpg').convert_alpha()
sandcastle_img = pygame.image.load('Defender/img/graphics/sandcastle.png').convert_alpha()
sandcastle_50_img = pygame.image.load('Defender/img/graphics/sandcastle_50.png').convert_alpha()
sandcastle_20_img = pygame.image.load('Defender/img/graphics/sandcastle_20.png').convert_alpha()
cannon_img = pygame.image.load('Defender/img/graphics/cannon.png').convert_alpha()
sand_img = pygame.image.load('Defender/img/graphics/sand.jpg').convert_alpha()
rock_img = pygame.image.load('Defender/img/graphics/rock.png').convert_alpha()
palm1_img = pygame.image.load('Defender/img/graphics/palm1.png').convert_alpha()
palm2_img = pygame.image.load('Defender/img/graphics/palm2.png').convert_alpha()
palm3_img = pygame.image.load('Defender/img/graphics/palm3.png').convert_alpha()
palm4_img = pygame.image.load('Defender/img/graphics/palm4.png').convert_alpha()
sandpile_img = pygame.image.load('Defender/img/graphics/sandpile.png').convert_alpha()
bullet_img = pygame.image.load('Defender/img/graphics/bullets.png').convert_alpha()
repair_img = pygame.image.load('Defender/img/graphics/repair.png').convert_alpha()
armor_img = pygame.image.load('Defender/img/graphics/armor.png').convert_alpha()

# Enemy characteristics (Each index in every list for each enemy)
enemy_types = ['crab','turtle','bird','ant','penguin','duck','crocodile','elephant','saurus']
enemy_health = [80, 120, 40, 60, 60, 200, 100, 280, 80]
enemy_speed = [2, 1, 3, 4, 1, 2, 2, 1, 2]
enemy_hitbox_x = [-20, -30, 30, 20, 0, -10, -70, -150, -40]
enemy_hitbox_y = [50, 0, 80, 70, 40, 10, 0, -100, 20]

# Enemy animations
enemy_animations = []
animation_types = ['walk', 'attack', 'death']

# Add every animation frame in an enemy animation list
for enemy in enemy_types:
    animation_list = []
    for animation in animation_types:
        # Temporary list of images
        temp_list = []
        # Define number of frames
        num_of_frames = 1
        # Load frames
        for i in range(num_of_frames):
            img = pygame.image.load(f'Defender/img/enemies/{enemy}/{animation}/{i}.png').convert_alpha() # Load images/frames from folders based on enemy type
            # Scaling
            enemy_width = img.get_width()
            enemy_height = img.get_height()
            img = pygame.transform.scale(img,(int(enemy_width * 1), int(enemy_height * 1))) # 1 for dedault scale
            # Add animation frames
            temp_list.append(img)
        animation_list.append(temp_list) 
    enemy_animations.append(animation_list) # Animation effect with nested list comperhension

# Text format
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Display game info
def show_info():
    draw_text(f'Money: {sandcastle.money}' , font_30, 'grey15', 90, 15)
    draw_text(f'Kills: {sandcastle.kills}' , font_30, 'red', 398, 15)
    draw_text(f'Level: {level}' , font_30, 'yellow', 733, 15)
    draw_text('MAX HP' , font_20, 'brown', sandcastle.max_hp_x_pos, 32)
    draw_text('1000', font_30, 'brown', 22, 340)
    draw_text('800', font_30, 'brown', 98, 341)
    draw_text('3000', font_30, 'brown', 25, 480)
    draw_text(f'HP: {sandcastle.hp}/{sandcastle.max_hp}', font_30, 'darkred', 170, 315)
    draw_text(f'High score: {high_score}', font_30, 'gold', 100, 220)

# Sandcastle
class SandCastle():
    def __init__(self, image100, image50, image20, x, y, scale):      
        self.hp = 1000
        self.max_hp = self.hp
        self.fired = False
        self.money = 10000
        self.kills = 0
        width = image100.get_width()
        height = image100.get_height()
        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
        self.image20 = pygame.transform.scale(image20, (int(width * scale), int(height * scale)))
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp_green = 300
        self.hp_black = 300
        self.max_hp_x_pos = 276

    def draw_image(self):

        # Change sandcastle image based on hp
        if self.hp <= 200:
          self.image = self.image20
        elif self.hp <= 500:
            self.image = self.image50
        else:
            self.image = self.image100
        screen.blit(self.image, self.rect)

    def shoot(self):

        # Get the mouse position and calculate the angle
        pos = pygame.mouse.get_pos() # x[0] y[1]
        x_dist = pos[0] - self.rect.center[0]
        y_dist = -(pos[1] - self.rect.center[1])
        self.angle = math.degrees(math.atan2(y_dist,x_dist)) # math.atan2 - arctangen (angle measurment in radians)

        # Get mouseclick
        if pygame.mouse.get_pressed()[0] and self.fired == False and pos[0] > 200: # Check if left mouseclick and mouse x_pos is in the clicking range
            self.fired = True
            bullet = Bullet(bullet_img, self.rect.center[0] + 30, self.rect.center[1] - 105, self.angle) # Create bullet - (image, x, y, angle)
            bullet_group.add(bullet)

        # Reset mouseclick
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False

    def repair(self):
        # Changes in hp/money when repaired
        if self.money >= 1000 and self.hp < self.max_hp:
            self.money -= 1000
            self.hp += 500
            sandcastle.hp_green += 150
            # Limit repair to no more than max hp 
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            if sandcastle.hp_green >= 1200:
                sandcastle.hp_green = 1200
            if sandcastle.hp_green >= self.hp_black:
                sandcastle.hp_green = self.hp_black
            
    def armor(self):
        # Changes in money/max hp/healthbar repaired
        if self.money >= 800:
            self.money -= 800
            self.max_hp += 200
            self.hp_black += 60
            self.max_hp_x_pos += 60
            # Limit max armor
            if self.max_hp > 4000:
                self.max_hp = 4000
            if self.hp_black >= 1197:
                self.hp_black = 1197
            if self.max_hp_x_pos >= 1176:
                self.max_hp_x_pos = 1176

# Cannon
class Cannon(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.got_target = False
        self.angle = 0
        self.last_shot = pygame.time.get_ticks()
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, enemy_group):
        self.got_target = False
        for e in enemy_group:
            # If enemy is alive, target it
            if e.alive:
                target_x, target_y = e.rect.midright
                self.got_target = True
                break
        # If enemy is targeted, shoot it
        if self.got_target:
            x_dist = target_x - self.rect.midtop[0]
            y_dist = -(target_y - self.rect.midtop[1])
            self.angle = math.degrees(math.atan2(y_dist,x_dist))
            shot_cooldown = 1000

            # Cannon fire
            if pygame.time.get_ticks() - self.last_shot > shot_cooldown:
                self.last_shot = pygame.time.get_ticks()
                bullet = Bullet(bullet_img, self.rect.midtop[0] - 20, self.rect.midtop[1], self.angle) # Create bullet - (image, x, y, angle)
                bullet_group.add(bullet)

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle) # Angle converted to radians
        self.speed = 10

        # Changing aim angle to make aiming harder
        # Calculating the horizontal and vertical speeds based on the angle
        self.delta_x = math.cos(self.angle) * self.speed # Change in x based of an angle
        self.delta_y = -(math.sin(self.angle) * self.speed) # Change in y based of an angle

    def update(self):
        # If bullet is out of the screen, delete it
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # Move the bullet
        self.rect.x += self.delta_x # x = x + change in x based on the angle
        self.rect.y += self.delta_y # y = y + change in y based on the angle

# Crosshair
class Crosshair():
    def __init__(self, scale):
        image = pygame.image.load('Defender/img/graphics/crosshair.png').convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()

        # Hide mouse
        pygame.mouse.set_visible(False)

    def draw_crosshair(self):
       
        # Get mouse center position and draw it 
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.center = (mouse_x, mouse_y)
        screen.blit(self.image, self.rect)

# Objects
sandcastle = SandCastle(sandcastle_img, sandcastle_50_img, sandcastle_20_img, -80, 290, 1) # Sandcastle instance- image, 50hp image, 20hp image, x, y, scale
crosshair = Crosshair(0.1)

# Buttons
repair = Button(10, 365, repair_img, 1) # x pos, y pos, img, scale
armor = Button(80, 363, armor_img, 1)
cannon_btn = Button(5, 500, cannon_img, 1.2)

# Groups (Manage updates and render multiple objects simultaneously)
cannon_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# Game loop
running = True
while running:
    if game_over == False:

        # Draw map
        screen.blit(backround_img,(0,-330))
        screen.blit(sand_img,(0,360))
        sandcastle.draw_image()
        screen.blit(cannon_img,(200,382))
        screen.blit(rock_img, (680,455))
        screen.blit(rock_img, (470,670))
        screen.blit(rock_img, (710,600))
        screen.blit(rock_img, (50,270))
        screen.blit(rock_img, (15,575))
        screen.blit(rock_img, (430,630))
        screen.blit(palm3_img, (320,120))
        screen.blit(palm4_img, (1020,60))
        screen.blit(rock_img, (380,300))
        screen.blit(palm3_img, (620,130))
        screen.blit(rock_img, (700,320))
        screen.blit(sandpile_img, (300,350))
        screen.blit(sandpile_img, (500,600))
        screen.blit(sandpile_img, (1000,290))
        screen.blit(rock_img, (280,390))
        screen.blit(sandpile_img, (500,300))
        screen.blit(sandpile_img, (1150,600))
        screen.blit(sandpile_img, (300,600))
        screen.blit(palm3_img, (-140,70))

        # Draw cannons
        cannon_group.draw(screen)
        cannon_group.update(enemy_group)

        # Draw healthbar
        pygame.draw.rect(screen, "red", (0, 0, 1200, 10)) # x pos, y pos, x len, y len
        pygame.draw.rect(screen, "green", (0, 0, sandcastle.hp_green, 10))
        pygame.draw.rect(screen, "black", (0, 0, 1200, 10), 3) # x pos, y pos, x len, y, len, border
        pygame.draw.rect(screen, "black", (sandcastle.hp_black, 0, 3, 30))

        # Draw buttons
        if repair.draw(screen):
            sandcastle.repair() 
        if armor.draw(screen):
            sandcastle.armor()
        if cannon_btn.draw(screen):
            # If player has money and max cannons are not reached, draw cannon
            if sandcastle.money >= CANNON_COST and len(cannon_group) < MAX_CANNONS:
                cannon = Cannon(cannon_img, cannon_positions[len(cannon_group)][0], cannon_positions[len(cannon_group)][1], 1)
                cannon_group.add(cannon)
                sandcastle.money -= CANNON_COST
            
        # Draw bullets
        bullet_group.update()
        sandcastle.shoot()
        bullet_group.draw(screen)

        # Draw enemies
        enemy_group.update(screen, sandcastle, bullet_group)

        # More map
        screen.blit(palm1_img, (710,400))
        screen.blit(palm2_img, (400,490))
        screen.blit(palm2_img, (50,550))
        screen.blit(rock_img, (1030,660))

        # Draw crosshair
        crosshair.draw_crosshair()

        # Draw info
        show_info()

        # Generate enemies (until difficulty is greater than max difficulty based on total enemy hp)
        if level_difficulty <= target_difficulty:
            if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:
                # Enemy generator
                enemy_index = randint(0, len(enemy_types) - 1) # Random enemy index generator

                enemy_y = [randint(320,680), # Enemy y pos based on the enemy type
                            randint(270,630),
                            randint(40,210),
                                randint(320,690),
                                randint(340,640),
                                    randint(280,630),
                                    randint(270,635),
                                        randint(300,600),
                                        randint(70,160)]
                
                enemy = Enemy(enemy_types[enemy_index], # Enemy type
                            enemy_health[enemy_index], # Enemy hp
                                enemy_animations[enemy_index], # Enemy animation
                                    1600, # Enemy x spawn position
                                        enemy_y[enemy_index], # Enemy y spawn position (randomized, but different for each enemy)
                                        enemy_speed[enemy_index], # Enemy speed
                                            pygame.Rect(0, 0, 50 - enemy_hitbox_x[enemy_index], # Enemy hitbox x
                                            120 - enemy_hitbox_y[enemy_index])) # Enemy hitbox y
                
                # Generate
                enemy_group.add(enemy)
                # Reset enemy timer
                last_enemy = pygame.time.get_ticks()
                # Generate level difficulty
                level_difficulty += enemy_health[enemy_index]

        # If all enemies have spawned
        if level_difficulty >= target_difficulty:
            # Check how many enemies are alive
            enemies_alive = 0
            for e in enemy_group:
                if e.alive == True:
                    enemies_alive += 1
    
            # Check if all enemies are dead
            if enemies_alive == 0 and next_level == False:
                next_level = True
                level_reset_time = pygame.time.get_ticks()
                
        # Move to the next level
        if next_level == True:
            draw_text('LEVEL COMPLETE!', font_60, 'yellow', 440, 100) # Text, font, color, x, y
            # Update high score
            if sandcastle.kills > high_score:
                high_score = sandcastle.kills
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            # Changes in next level
            if pygame.time.get_ticks() - level_reset_time > 2000: # Level restart delay to 2 seconds
                next_level = False # Set false to run level change once
                level += 1
                last_enemy = 0
                last_enemy = pygame.time.get_ticks()
                target_difficulty *= DIFFICULTY_MULTIPLIER # Set each level 7% harder
                level_difficulty = 0
                enemy_group.empty() # Delete dead enemies

        # Check if game is over
        if sandcastle.hp <= 0:
            sandcastle.hp_green = 0
            game_over = True

    # Game over
    else:
        draw_text(f'GAME OVER!' , font_30, 'black', 915, 100)
        draw_text(f'Press space to play again' , font_30, 'black', 860, 150)
        pygame.mouse.set_visible(True)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # Reset variables
            game_over = False
            level = 1
            target_difficulty = 1000
            level_difficulty = 0
            last_enemy = pygame.time.get_ticks()
            enemy_group.empty()
            cannon_group.empty()
            sandcastle.kills = 0
            sandcastle.hp = 1000
            sandcastle.max_hp = sandcastle.hp
            sandcastle.money = 0
            sandcastle.hp_green = 300
            sandcastle.hp_black = 300
            sandcastle.max_hp_x_pos = 276
            pygame.mouse.set_visible(False)

    # If exit is clicked, quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update frames every loop
    pygame.display.flip()
    CLOCK.tick(60)

# Quit
pygame.quit()