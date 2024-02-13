import pygame
from sys import exit
from random import randint

def displayScore():
    currentTime = int(pygame.time.get_ticks() / 1000) - startTime
    textSuface = testFont.render(f'Score: {currentTime}', False, (64, 64, 64))
    textRect = textSuface.get_rect(center = (400, 50))
    screen.blit(textSuface, textRect)
    return currentTime

speed = 12

def obsMovement(obsList):
    if obsList:
        for obsRect in obsList:
            obsRect.x -= speed

            if obsRect.bottom == 300:
                screen.blit(enemy1, obsRect)
            else:
                screen.blit(enemy2, obsRect)
        
        obsList = [obs for obs in obsList if obs.x > -100]

        return obsList
    else:
        return []

def collisions(player, obs):
    if obs:
        for obsRect in obs:
            if player.colliderect(obsRect):
                return False
    return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('First Game')
clock = pygame.time.Clock()
testFont = pygame.font.Font(None, 50)
gameActive = False
startTime = 0
score = 0
skySurface = pygame.Surface((800, 350))
skySurface.fill('Dark Blue')
skyRect = skySurface.get_rect(topleft = (0, 0))
groundSurface = pygame.Surface((800, 150))
groundSurface.fill('Dark Green')
groundRect = groundSurface.get_rect(topleft = (0, 300))
textSurface = testFont.render('Speed Cube', False, (64, 64, 64))
textRect = textSurface.get_rect(midbottom = (400, 75))
instSurface = testFont.render('To Start Press Space', False, (64, 64, 64))
instRect = instSurface.get_rect(midbottom = (400, 375))

enemy1 = pygame.Surface((50, 30))
enemy1.fill('Dark Red')

enemy2 = pygame.Surface((40, 20))
enemy2.fill('Black')

obsRectList = []

playerSurface = pygame.Surface((60, 60))
playerSurface.fill('Yellow')
playerRect = playerSurface.get_rect(midbottom = (80, 300))
playerGrav = 0

obsTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obsTimer, 600)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if gameActive:
            speed += 0.05
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playerRect.bottom >= 300:
                    if playerRect.collidepoint(event.pos):
                        playerGrav = -15
                    if groundRect.collidepoint(event.pos):
                        playerGrav = -15
                    if skyRect.collidepoint(event.pos):
                        playerGrav = -15
            if event.type == pygame.KEYDOWN:
                if playerRect.bottom >= 300:
                    if event.key == pygame.K_SPACE:
                        playerGrav = -15
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if gameActive == False:
                    gameActive = True
                    startTime = int(pygame.time.get_ticks() / 1000)
        if event.type == obsTimer and gameActive:
            if randint(0, 2):
                obsRectList.append(enemy1.get_rect(bottomright = (randint(800, 950), 300)))
            else:
                obsRectList.append(enemy2.get_rect(bottomright = (randint(800, 950), 210)))

    if gameActive:
        screen.blit(skySurface, skyRect)
        screen.blit(groundSurface, groundRect)
        # pygame.draw.rect(screen, '#c0e8ec', textRect)
        # pygame.draw.rect(screen, '#c0e8ec', textRect, 10, 20)
        # screen.blit(textSurface,textRect)
        score = displayScore()

        # enemy1Rect.x -= 9
        # if enemy1Rect.right <= 0:
        #     enemy1Rect.left = 800
        # screen.blit(enemy1, enemy1Rect)
        
        playerGrav += 1
        playerRect.y += playerGrav
        if playerRect.bottom >= 300:
            playerRect.bottom = 300
        screen.blit(playerSurface, playerRect)

        obsRectList = obsMovement(obsRectList)

        gameActive = collisions(playerRect, obsRectList)

    else:
        speed = 12
        screen.fill((94, 129, 162))
        screen.blit(textSurface, textRect)
        obsRectList.clear()
        playerRect.midbottom = (80, 300)
        playerGrav = 0

        scoreMess = testFont.render(f'Your Score: {score}', False, (64, 64, 64))
        scoreMessRect = scoreMess.get_rect(center = (400, 200))
        
        if score == 0:
            screen.blit(instSurface, instRect)
        else:
            screen.blit(instSurface, instRect)
            screen.blit(scoreMess, scoreMessRect)

    pygame.display.update()
    clock.tick(60)
