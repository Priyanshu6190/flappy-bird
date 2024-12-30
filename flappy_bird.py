import random
import sys 
import pygame
from pygame.locals import * 
FPS = 32
screenwidth = 289
screenheight = 511
screen = pygame.display.set_mode((screenwidth, screenheight))
groundy = screenheight*0.8
game_sprites = {}
game_sounds = {}
player = 'resources/SPRITES/bird.png'
background = 'resources/SPRITES/bg.jpeg'
pipe = 'resources/SPRITES/pipe.png '

def welcomescreen(): 
    
    playerx = int(screenwidth/5)
    playery = int(screenheight - game_sprites['player'].get_height())/2
    messagex = int(screenwidth - game_sprites['message'].get_width())/2
    messagey = int(screenheight * 0.13)
    basex = 0
    
    playbutton = pygame.Rect(108,222,68,65)

    while True:
        for event in pygame.event.get():
            
            if event.type== QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if pygame.mouse.get_pos()[0] > playbutton[0]  and pygame.mouse.get_pos()[0] < playbutton[0] + playbutton[2]:
                if pygame.mouse.get_pos()[1] > playbutton[1]  and pygame.mouse.get_pos()[1] < playbutton[1] + playbutton[3]:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if playbutton.collidepoint(pygame.mouse.get_pos()): 
            
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    mainGame()

            else :
                screen.blit(game_sprites['background'],(0,0))
                screen.blit(game_sprites['player'],(playerx,playery))
                screen.blit(game_sprites['message'],(messagex,messagey))
                screen.blit(game_sprites['base'],(basex,groundy))
            
                pygame.mixer.music.load('resources/AUDIO/INTROMUSIC.mp3')
                pygame.mixer.music.play()
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    
    
    pygame.mixer.music.stop()
    pygame.mixer.music.load('resources/AUDIO/BGMUSIC.mp3')
    pygame.mixer.music.play()
    score = 0
    playerx = int(screenwidth/5)
    playery = int (screenheight/2)
    basex = 0

    
    newpipe1 = getRandompipe()
    newpipe2 = getRandompipe()

    
    upperpipes = [
        {'x':screenwidth + 200, 'y': newpipe1[0]['y']},
        {'x':screenwidth + 200 + (screenwidth/2), 'y': newpipe2[0]['y']}
    ]

   
    lowerpipes = [
        {'x':screenwidth + 200, 'y': newpipe1[1]['y']},
        {'x':screenwidth + 200 + (screenwidth/2), 'y': newpipe2[1]['y']}
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10  
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 
    playerFlapped = False 

    while True:

        for event in pygame.event.get():
           
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    game_sounds['wing'].play()

        crashTest = isCollide(playerx, playery, upperpipes, lowerpipes) 
        if crashTest:
            return     

        
        playerMidPos = playerx + game_sprites['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidPos = pipe['x'] + game_sprites['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                game_sounds['point'].play()

        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = game_sprites['player'].get_height()
        playery = playery + min(playerVelY, groundy - playery - playerHeight)

        
        for upperpipe , lowerpipe in zip(upperpipes, lowerpipes):
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX

        
        if 0<upperpipes[0]['x']<5:
            newpipe = getRandompipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        
        if upperpipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        
        screen.blit(game_sprites['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            screen.blit(game_sprites['pipe'][0], (upperpipe['x'], upperpipe['y']))
            screen.blit(game_sprites['pipe'][1], (lowerpipe['x'], lowerpipe['y']))

        screen.blit(game_sprites['base'], (basex, groundy))
        screen.blit(game_sprites['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_sprites['numbers'][digit].get_width()
        Xoffset = (screenwidth - width)/2

        for digit in myDigits:
            screen.blit(game_sprites['numbers'][digit], (Xoffset, screenheight*0.12))
            Xoffset += game_sprites['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperpipes, lowerpipes):
    if playery> groundy - 25  or playery<0:
        game_sounds['hit'].play()
        pygame.mixer.music.stop()
        gameOver()

    for pipe in upperpipes:
        pipeHeight = game_sprites['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < game_sprites['pipe'][0].get_width()-20):
            game_sounds['hit'].play()
            print(playerx, pipe['x'],)
            pygame.mixer.music.stop()
            gameOver()
            

    for pipe in lowerpipes:
        if (playery + game_sprites['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < game_sprites['pipe'][0].get_width()-20:
            game_sounds['hit'].play()
            pygame.mixer.music.stop()
            gameOver()

    return False


def getRandompipe():
            
    pipeHeight = game_sprites['pipe'][0].get_height()
    offset = screenheight/3.7
    y2 = offset + random.randrange(0, int(screenheight - game_sprites['base'].get_height() - 1.2 *offset))
    pipeX = screenwidth + 10
    y1 = pipeHeight - y2 + offset
    pipe = [ 
        {'x': pipeX, 'y': -y1}, 
        {'x': pipeX, 'y': y2}   
    ]
    return pipe 

def gameOver():
    
    screen = pygame.display.set_mode((screenwidth, screenheight))
    pygame.display.set_caption('Flappy Bird')
    game_sprites['OVER'] = pygame.image.load('resources/SPRITES/gameover.png').convert_alpha()
    game_sprites['RETRY'] = pygame.image.load('resources/SPRITES/retry.png').convert_alpha()
    game_sprites['HOME'] = pygame.image.load('resources/SPRITES/Home.png').convert_alpha()
    screen.blit(game_sprites['background'],(0,0))
    screen.blit(game_sprites['base'],(0,groundy))
    screen.blit(game_sprites['OVER'], (0,0))
    screen.blit(game_sprites['RETRY'], (30, 220))
    screen.blit(game_sprites['HOME'], (30, 280))
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
 
            if event.type == KEYDOWN and event.key == K_SPACE:
                mainGame()
  
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if pygame.mouse.get_pos()[0]>30 and pygame.mouse.get_pos()[0]< 30+game_sprites['RETRY'].get_width():
                if pygame.mouse.get_pos()[1]>220 and pygame.mouse.get_pos()[1]< 220+game_sprites['RETRY'].get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        
                        mainGame()
                      
            
            if pygame.mouse.get_pos()[0]>30 and pygame.mouse.get_pos()[0]< 30+game_sprites['HOME'].get_width():
                if pygame.mouse.get_pos()[1]>280 and pygame.mouse.get_pos()[1]< 280+game_sprites['HOME'].get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        welcomescreen()
            



if __name__ == "__main__":

    pygame.init()  
    FPSCLOCK = pygame.time.Clock() 
    pygame.display.set_caption('Flappy Bird') 

    

    game_sprites['numbers'] = (
        pygame.image.load('resources/SPRITES/0.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/1.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/2.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/3.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/4.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/5.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/6.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/7.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/8.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/9.png').convert_alpha(),
    ) 
    
    game_sprites['background'] = pygame.image.load(background).convert_alpha()
    game_sprites['player'] = pygame.image.load(player).convert_alpha()
    game_sprites['message'] = pygame.image.load('resources/SPRITES/message.png').convert_alpha()
    game_sprites['base'] = pygame.image.load('resources/SPRITES/base.png').convert_alpha()
    game_sprites['pipe'] = (
    pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
    pygame.image.load(pipe).convert_alpha()   
    )

    
    game_sounds['die'] = pygame.mixer.Sound('resources/AUDIO/die.wav')
    game_sounds['hit'] = pygame.mixer.Sound('resources/AUDIO/hit.wav')
    game_sounds['point'] = pygame.mixer.Sound('resources/AUDIO/point.wav')
    game_sounds['swoosh'] = pygame.mixer.Sound('resources/AUDIO/swoosh.wav')
    game_sounds['wing'] = pygame.mixer.Sound('resources/AUDIO/wing.wav')
    while True:
        welcomescreen() 
        mainGame() 