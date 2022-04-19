import pygame
import random
import math

from pygame import mixer

"""Background was designed by images from Freepik.com
https://www.freepik.com/free-vector/space-background-with-planet-landscape_13643566.htm#query=space%20game&position=0&from_view=keyword

Alien Icon Designed by I Wayan Wika
https://www.flaticon.com/authors/i-wayan-wika

"Arcade-Game" icon for player designed by Freepik
https://www.flaticon.com/authors/freepik

"""

# Start game !!! Important
pygame.init()

# Create window
screen = pygame.display.set_mode((800, 600))

# Background to the window
background = pygame.image.load("spacebg.jpg")

# Title and icon
pygame.display.set_caption("Alien Invasion")
icon = pygame.image.load('alien.png')
# makes sure icon has been added
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('arcade-game.png')
# Position
playerX = 370
playerY = 480
# change in position
playerX_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    # Setting to random
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    # Enemy position
    enemyX_change.append(1)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
# Bullet position change
bulletX_change = 0
bulletY_change = 3
# Bullet state
bullet_state = "ready"  # Can't see the bullet on the screen

# Score
score_value = 0
font = pygame.font.Font('Chicken Hunter.ttf', 44)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 72)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True

while running:
    # Background
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    # Quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check if right or left
        if event.type == pygame.KEYDOWN:
            print("A keystroke is pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # Coordinate of ship and fires.
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    playerX += playerX_change

    # Player boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # Enemy boundary
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("collision.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
