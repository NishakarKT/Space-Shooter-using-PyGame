import pygame
import random

pygame.init()

# Game Variables
# Screen
width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
fps = 32

# PLayer
player_width = 50
player_length = 76
player_x = (width-player_width)/2
player_y = height - player_length
vel_x = 20
vel_y = 5
player_nav = "player"
shake = 1

# Bullet
shoot = [player_x, player_y + player_length/4]
shoot_vel = 50

# Asteorids
asteroid_pos = [[0, 0]]
asteroid_count = 1
asteroid_vel = 15

# Background
bg_y_1 = 0
bg_y_2 = -height

# Image dictionaries
player_images = {
    "player": pygame.image.load("images\\player.png").convert(),
    "player_left": pygame.image.load("images\\player_left.png").convert(),
    "player_right": pygame.image.load("images\\player_right.png").convert()
}

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # background motion
    bg_y_1 += vel_y
    bg_y_2 += vel_y
    if bg_y_1 >= height:
        bg_y_1 = -height
    if bg_y_2 >= height:
        bg_y_2 = -height

    # horizontal limit
    if player_x >= (width - player_width):
        player_x = width - player_width
    elif player_x <= 0:
        player_x = 0

    # Held key events
    keys = pygame.key.get_pressed()
    # Horizontal navigation
    if keys[pygame.K_LEFT]:
        player_x -= vel_x
        player_nav = "player_left"
    elif keys[pygame.K_RIGHT]:
        player_x += vel_x
        player_nav = "player_right"

    # Crash tests
    # player and asteroid
    for i in range(asteroid_count):
        if abs(player_x - asteroid_pos[i][0] - player_width) < 55 and abs(player_y - asteroid_pos[i][1]) <130:
            screen.blit(pygame.image.load("images\\bang.png").convert(), ((player_x + asteroid_pos[i][0])/2 - player_width, player_y - 100))  
            pygame.display.update()
            if(player_x > asteroid_pos[i][0] + player_width):
                player_x += 50
            elif(player_x < asteroid_pos[i][0] + player_width):
                player_x -= 50
    # asteroid and bullet
    for i in range(asteroid_count):
        if abs((shoot[0]+player_width/2) - (asteroid_pos[i][0]+75)) < 75 and abs(shoot[1] - asteroid_pos[i][1]) <50:
            asteroid_pos.append([random.randint(100, 400), - 550])
            asteroid_pos.pop(i)
            screen.blit(pygame.image.load("images\\bang.png").convert(), (asteroid_pos[i][0] - 100, shoot[1] - 50))  
            pygame.display.update()
            break

    # Display
    screen.blit(pygame.image.load(
        "images\\background.png").convert(), (0, bg_y_1))
    screen.blit(pygame.image.load(
        "images\\background.png").convert(), (0, bg_y_2))

    # Bullets display
    shoot[1] -= shoot_vel
    pygame.draw.rect(screen, (255, 255, 255), [shoot[0], shoot[1], 5, 30])
    pygame.draw.rect(screen, (255, 255, 255), [shoot[0] + player_width - 10, shoot[1], 5, 30])
    if shoot[1] <= -10:
        shoot[0] = player_x
        shoot[1] = player_y + player_length/4

    # ateroids
    for i in range(asteroid_count):
        asteroid_pos[i][1] += asteroid_vel
        screen.blit(pygame.image.load("images\\asteroid.png").convert_alpha(), (asteroid_pos[i][0], asteroid_pos[i][1])) 
        # pygame.display.update()
        if(asteroid_pos[i][1] == height):
            asteroid_pos.append([random.randint(0, 400), -100])
            asteroid_pos.pop(i)
        
    # Player display
    if shake % 2 == 0:
        screen.blit(player_images[player_nav], (player_x, player_y))
    else:
        screen.blit(player_images[player_nav], (player_x + 2, player_y))

    # Update
    pygame.display.update()
    clock.tick(fps)

    # Resets
    player_nav = "player"
    shake += 1
