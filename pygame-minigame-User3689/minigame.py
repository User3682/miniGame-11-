#-----------------------------------------------------------------------------
# Name:        minigame.py
# Purpose:     A minigame with some puzzle elements, smaller games embeded in it (a maze and question game), and a boss level
#
# Author:      Rebecca
#-----------------------------------------------------------------------------
#I think this project deserves a level 4/4+ because ...
#   Elements of randomness/replayability:
#       random questions are generated
#       spikes and extra lives spawn randomly
#       maze makes you go faster if you complete it fast enough
#       pickaxe spawns in random places
#   Extra features/improvements:
#       I modified the character movement strategy discussed in class by making it so that it checks if the keys are down (this allows for much smoother movement)
#       there are smaller stages (the minigames) within a stage (stage 1) and the ability to toggle between them
#       user is able to type text into textbox
#       item that can be collected and used (the pickaxe)
#       increasing difficulty on stage 2
#       lists within lists
#       character animation
#       adjusting character speed
#       platforms (changing groundLevel)
#       multiple random falling objects, collision detection and drawing with classes
#       Sounds and background music
#   Collision detection
#   Character movement with input
#   Start screen, instructions, play button, menu button, instructions button, play again button, end screen, win screen etc.
#   Does not include grossly inefficient or buggy code (there are many times I have shortened/simplified blocks of code by using classes, for loops, lists, tuples, etc.)
#   Polished visually
#-----------------------------------------------------------------------------

import pygame
import random

class wall(): #walls in mini maze
    def __init__(self, posX1, posY1, posX2, posY2):
        self.posX1 = posX1
        self.posY1 = posY1
        self.posX2 = posX2
        self.posY2 = posY2
        #this allows me to access all the positions/dimensions of each individual wall.

class spike(): #spike in stage 2
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY

def stage1SetUp(): #intializes all variables for stage 1; helpful for a play again button
    global charPos, charSpeed, keyDown, jumping, xBoundaries, lives, frameCount, write, complete, pickaxeDisplay, randIndex, randPos, groundList, platformsPos
    charPos = [430,150]
    charSpeed = [4,0]
    keyDown = [False,False,False,False]
    jumping = False
    xBoundaries = [450,-30]
    lives = 3
    frameCount = [0,0,0,0,0,0,0,0,0]
    write = False
    complete = [False,False]
    pickaxeDisplay = "notCollected"
    randIndex = [0,random.randrange(0, 10+2,2)]

    #The data doesn't change for all these lists, they are just used to avoid repetititon. Therefore I made them tuples instead
    randPos = (300,409,30,80,400,169,170,169,30,269,250,90)
    groundList = (310,480,150, 0,115-6,249, 115,120,299, 180,190,149)
    platformsPos = (0,440,480,480,300,200,480,15,100,300,15,330,0,300,100,15,100,350,30,15,170,200,30,15)
    
    buttonColor = [(3,90,102),(3,90,102)]
    imgMemory = charPos[0] #image memory variable allows me to change the images that are used to blit the character onto the screen in order to create animations

def stage2Setup(): #intializes all variables for stage 2
    global charPos,groundList,bossHealth,end,frameCount,spikes,spikeGravity
    charPos = [300,100]
    groundList = (0,100-40+5,309,100+5,250-5,274,250-5,480,339) #I subtracted and added a few pixels in certain places in order to make the hitbox more accurate
    for counter in range (1, len(frameCount),1):
        frameCount[counter] = 0 #Cycles through all indexes of the frame count list and resets it to zero (except the first index because I want that to save for the next level)
    spikes = []
    spikeGravity = []
    bossHealth = 100
    end = 200 #I want the bar for the boss health to be 200 pixels wide, so I set the end condition on the for loop that draws lines on every pixel to 200 (a line is drawn at zero so I dont need to change it to 201). This means that lines will be drawn at each pixel for 200 pixels.
    imgMemory = charPos[0]

def main():
    #-----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = 480   # Desired physical surface size, in pixels.
    clock = pygame.time.Clock()  #Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    #-----------------------------Program Variable Initialization----------------------------#
    gameState = "start"
    walls = (wall(90,60,5,50),wall(90,160,5,220), wall(145,60,245,5),wall(385,60,5,320),wall(90,375,300,5),wall(90,105,150,5),wall(135,105,5,50),wall(235,105,5,50),wall(235,155,50,5),wall(280,155,5,50),wall(280,200,50,5),wall(300,110,50,5),wall(300,60,5,50),wall(340,155,50,5),wall(325,200,5,130),wall(280,200,5,130),wall(235,330,50,5),wall(90,210,50,5),wall(135,210,5,50),wall(185,260,5,120),wall(140,330,50,5),wall(185,260,50,5),wall(185,260,50,5),wall(230,215,5,50),wall(185,210,50,5), wall(185,160,5,50)) #creates each wall object as a different index in the tuple so that I can use this later to greatly reduce the amount of lines I have to use for collision detection and everything else
    buttonColor = [(3,90,102),(3,90,102)]

    #render font
    fonts = (pygame.font.Font('freesansbold.ttf', 22), pygame.font.Font('freesansbold.ttf', 12),pygame.font.Font("vertopal.com_8514oem.ttf", 15),pygame.font.Font("vertopal.com_CHILLER.ttf",200),pygame.font.Font("vertopal.com_CHILLER.ttf",100),pygame.font.Font("vertopal.com_8514oem.ttf", 25),pygame.font.Font("vertopal.com_CHILLER.ttf",30))
    
    text3 = fonts[2].render('PLAY', True, (255,255,255))
    text3Rect = text3.get_rect()
    text3Rect.topleft = (130+2,220+2)

    text4 = fonts[3].render('JUMP', True, (0,0,0))
    text4Rect = text4.get_rect()
    text4Rect.topleft = (70,10)

    text5 = fonts[4].render('YOU DIED', True, (163, 12, 2))

    text6 = fonts[5].render('PLAY AGAIN', True, (255,255,255))
    text6Rect = text6.get_rect()
    text6Rect.topleft = (70+2,110+2)

    text7 = fonts[5].render('BACK TO MENU', True, (255,255,255))
    text7Rect = text7.get_rect()
    text7Rect.topleft = (70+2,170+2)

    text8 = fonts[4].render('YOU WIN', True, (9, 105, 70))

    text9 = fonts[2].render('INSTRUCTIONS', True, (255,255,255))
    text9Rect = text9.get_rect()
    text9Rect.topleft = (130+2,260+2)

    text10 = fonts[2].render('BACK TO MENU',True, (255,255,255))
    text10Rect = text10.get_rect()
    text10Rect.topleft = (0+5,455+5)

    #Load an image
    charImg = [pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (1).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (2).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (3).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (4).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (5).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (6).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (7).png")]
    sign = pygame.image.load("Sign-removebg-preview.png")
    pressE = pygame.image.load("pressE.png")
    pickaxe = pygame.image.load("pickaxe-removebg-preview.png")
    brick = pygame.image.load("brickwall.png")
    door = pygame.image.load("door - Copy.png")
    open = pygame.image.load("open.png")
    lock = pygame.image.load("lock-removebg-preview (6).png")
    boss = pygame.image.load("boss-removebg-preview (3).png")
    spikeImg = pygame.image.load("spike-removebg-preview.png")
    life = pygame.image.load("life-removebg-preview.png")
    instructions = pygame.image.load("instructions.png")

    #Load sounds
    pygame.mixer.music.load("sonatina_letsadventure_9MechanicalDancer.wav")
    pygame.mixer.music.play(-1)
    button_Sound = pygame.mixer.Sound("MI_SFX 45 (1).mp3")
    hit_Sound = pygame.mixer.Sound("Hit_3.wav")
    death_Sound = pygame.mixer.Sound("Monster_Scream.wav")
    win_Sound = pygame.mixer.Sound("Powerup.wav")
    jump_Sound = pygame.mixer.Sound("SFX_Jump_01.wav")
    life_Sound = pygame.mixer.Sound("Fruit collect 1.wav")
    door_Sound = pygame.mixer.Sound("door-1-open.mp3")
    pickaxe_Sound = pygame.mixer.Sound("Big Egg collect 1.wav")
    break_Sound = pygame.mixer.Sound("Block Break 1.wav")

    def playerJump(): #Allows player to jump
        global jumping, bossHealth, end
        if keyDown[2] == True and jumping == False: #can only jump if the up key is down and the character isnt already jumping
            pygame.mixer.Sound.play(jump_Sound)
            if gameState == "stage2":
                bossHealth -= 1
                end -= 2 #200/100 is 2, therefore each time the boss looses one life it is equivalent to 2 of the lines drawn to represent the boss health. By making the end condition 2 lower, 2 less lines will be drawn
            charSpeed[1] = -15 #it will add -15 to the y position of hte character, which will therefore make it go higher
            jumping = True #jumping needs to be true to indicate that the character is jumping
        charPos[1] += charSpeed[1] #charSpeed for y needs to be applied to y position of the character
        if charPos[1] >= groundLevel: #if the y position of the character is below or on the current ground level
            charPos[1] = groundLevel
            charSpeed[1] = 0
            jumping = False
        else:
            charSpeed[1] += 1
    
    def playerMove(): #allows player to move and establishes boundaries for movement
        global imgMemory
        #Character movement
        if keyDown[0] == True:
            if frameCount[8] == 5:
                imgMemory = charImg[6]
            if frameCount[8] == 10:
                imgMemory = charImg[5]
            if frameCount[8] == 15:
                imgMemory = charImg[4]
                frameCount[8] = 0
            frameCount[8] += 1
            charPos[0] += charSpeed[0]
        elif keyDown[1] == True:
            if frameCount[8] == 5:
                imgMemory = charImg[1]
            if frameCount[8] == 10:
                imgMemory = charImg[2]
            if frameCount[8] == 15:
                imgMemory = charImg[3]
                frameCount[8] = 0
            frameCount[8] += 1
            charPos[0] -= charSpeed[0]
        else:
            imgMemory = charImg[0]
            frameCount[8] = 0 #should reset because movement has stoped

        #x boundaries
        if charPos[0] > xBoundaries[0]:
            charPos[0] -= charSpeed[0]
        if charPos[0] < xBoundaries[1]:
            charPos[0] += charSpeed[0]
    
    def charKeyDownInput(): #checks if certain keys are down and assigns True to the corresponding index of the keyDown list
        if ev.key == pygame.K_UP:
            if charPos[1] == groundLevel or gameState == "miniMaze":
                keyDown[2] = True
        elif ev.key == pygame.K_DOWN:
            keyDown[3] = True
        if ev.key == pygame.K_RIGHT:
            keyDown[0] = True
        elif ev.key == pygame.K_LEFT:
            keyDown[1] = True

    def charKeyUpInput(): #checks if certain keys are up (not being pressed) and assigns False to the corresponding index of the keyDown list
        if ev.key == pygame.K_UP:
            keyDown[2] = False
        elif ev.key == pygame.K_DOWN:
            keyDown[3] = False
        if ev.key == pygame.K_RIGHT:
            keyDown[0] = False
        elif ev.key == pygame.K_LEFT:
            keyDown[1] = False
    
    def livesDisplay(): #prints lives text
        text9 = fonts[6].render(f'LIVES: {lives}', True, (255,255,255))
        text9Rect = text9.get_rect()
        text9Rect.topleft = (380,445)
        mainSurface.blit(text9, text9Rect)

    def buttonFill(xPos, width, yPos, height, buttonColorIndex): #changes the color of the button depending on whether or not the mouse cursor is over it
        if pygame.mouse.get_pos()[0] > xPos and pygame.mouse.get_pos()[0] < xPos + width and pygame.mouse.get_pos()[1] > yPos and pygame.mouse.get_pos()[1] < yPos + height:
            buttonColor[buttonColorIndex] = (54, 141, 153)
        else:
            buttonColor[buttonColorIndex] = (3,90,102)

    #-----------------------------Main Program Loop---------------------------------------------#
    while True:
        if gameState == "start":
            #-----------------------------Event Handling-----------------------------------------#
            ev = pygame.event.poll()    # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break
            if pygame.mouse.get_pressed()[0] == True: 
                if pygame.mouse.get_pos()[0] > 130 and pygame.mouse.get_pos()[0] < 130 + 200 and pygame.mouse.get_pos()[1] > 220 and pygame.mouse.get_pos()[1] < 220 + 22:
                    pygame.mixer.Sound.play(button_Sound)
                    stage1SetUp()
                    global charPos, charSpeed, keyDown, jumping, xBoundaries, lives, frameCount, write, complete, pickaxeDisplay, randIndex, randPos, groundList, platformsPos
                    gameState = "stage1"
                if pygame.mouse.get_pos()[0] > 130 and pygame.mouse.get_pos()[0] < 130 + 200 and pygame.mouse.get_pos()[1] > 260 and pygame.mouse.get_pos()[1] < 260 + 22:
                    pygame.mixer.Sound.play(button_Sound)
                    gameState = "instructions"
            #-----------------------------Program Logic---------------------------------------------#
            buttonFill(130,200,260,22,1)
            buttonFill(130,200,220,22,0)
            #-----------------------------Drawing Everything-------------------------------------#
            mainSurface.fill((255, 255, 255))
            pygame.draw.rect(mainSurface, (buttonColor[0]), (130,220,200,22))
            pygame.draw.rect(mainSurface, (buttonColor[1]), (130,260,200,22))
            mainSurface.blit(text3, text3Rect)
            mainSurface.blit(text4, text4Rect)
            mainSurface.blit(text9, text9Rect)
        elif gameState == "instructions":
            #-----------------------------Event Handling-----------------------------------------#
            ev = pygame.event.poll()    # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break
            if pygame.mouse.get_pressed()[0] == True: 
                if pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[0] < 0 + 160 and pygame.mouse.get_pos()[1] > 455 and pygame.mouse.get_pos()[1] < 455 + 25:
                    pygame.mixer.Sound.play(button_Sound)
                    gameState = "start"
            #-----------------------------Program Logic---------------------------------------------#
            buttonFill(0, 160, 455, 25, 0)
            #-----------------------------Drawing Everything-------------------------------------#
            mainSurface.fill((255, 255, 255))
            mainSurface.blit(instructions, (0, 0))
            pygame.draw.rect(mainSurface, (buttonColor[0]), (0,455,160,25))
            mainSurface.blit(text10, text10Rect)
        elif gameState == "stage2":
            #-----------------------------Event Handling-----------------------------------------#
            ev = pygame.event.poll()    # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break
            elif ev.type == pygame.KEYDOWN:
                charKeyDownInput()
            elif ev.type == pygame.KEYUP:
                charKeyUpInput()

            #-----------------------------Program Logic---------------------------------------------#
            #increase/decrease frame rates
            for counter in range(2,6,1):
                frameCount[counter] += 1
            for counter in range(6,8,1):
                if frameCount[counter] > 0:
                    frameCount[counter] -= 1

            #if statements with frame rates
            if frameCount[5] == 400:
                frameCount[5] = 0
            if frameCount[4] == 2000:
                frameCount[4] = 0
            if frameCount[4] == 1: #create and store new random coordinates for the heart image to spawn at
                randNum[4] = random.randint(0,460)
                randNum[5] =  random.randint(150,280)
            for counter in range(15,45+1,15): #cycles through intervals of 15 frames, adding spikes to the screen each time
                if frameCount[2] == counter:
                   spikes.append(spike(random.randint(0,480),random.randint(15,30))) #add a new spike object to the spikes list
                   spikeGravity.append(0) #add a new index for spikeGravity list to correspond to the new spike
                   if counter == 45:
                       frameCount[2] = 0 #frameCount needs to be reset or else the spikes will stop spawning after 45 frames
            
            #establish ground level
            for counter in range (0,9,3):
                if charPos[0]+40 > groundList[counter] and charPos[0] < groundList[counter+1] and charPos[1] <= groundList[counter+2]:
                    groundLevel = groundList[counter+2]
                    break
            pygame.draw.rect(mainSurface, (0,0,0), (0,360,100,480))
            pygame.draw.rect(mainSurface, (0,0,0), (100,325,150,480))
            pygame.draw.rect(mainSurface, (0,0,0), (250,390,230,480))
            #prevent character from moving past the sides of the platforms
            if groundLevel == 309 and charPos[1]+51 > 325 and (charPos[0]+40) >= 100 and keyDown[0] == True: #if statement only runs if the right key is down because that is the direction that the side of the platform is (otherwise the character wouldn't be able to move at all)
                charSpeed[0] = 0
                charPos[0] = 60
            elif groundLevel == 339 and charPos[1]+51 > 325 and charPos[0] <= 250 and keyDown[1] == True:
                charSpeed[0] = 0
                charPos[0] = 250
            else:
                if frameCount[0] <= 600 and complete[0] == True:
                    charSpeed[0] = 6
                else:
                    charSpeed[0] = 4
            
            counter = 0
            while counter < len(spikes) and frameCount[3] > 40: #cycles through the spikes list. frameCount[3] starts at 0 and increases by 1 each frame until it reaches 40 and then this while loop is able to run. This allows for there to be a 40 frame delay after stage 2 starts
                #adjust speed of spikes based on boss health
                if bossHealth > 80:
                    spikeGravity[counter] += 0.1
                elif bossHealth > 60:
                    spikeGravity[counter] += 0.2
                else:
                    spikeGravity[counter] += 0.3
                spikes[counter].posY += spikeGravity[counter] #increase y of the spike objects by the gravity variable to cause them to fall
                if spikes[counter].posY >= 480: #if they are past the screen, remove the items from their respective lists to avoid having extremely long lists
                    spikes.pop(counter)
                    spikeGravity.pop(counter)
                if frameCount[6] == 0 and charPos[0] + 40 > spikes[counter].posX and charPos[0] < spikes[counter].posX + 20 and charPos[1] + 51 > spikes[counter].posY and charPos[1] < spikes[counter].posY + 20: #even though the height of the spike image is 30, the hitbox is more accurate with a height of 20
                    pygame.mixer.Sound.play(hit_Sound)
                    lives -= 1
                    frameCount[6] = 30 #30 frames must pass before the character is able to lose another life
                counter += 1
            
            playerJump()
            playerMove()
            if lives <= 0:
                pygame.mixer.Sound.play(death_Sound)
                gameState = "endScreen"
            if bossHealth <= 0:
                pygame.mixer.Sound.play(win_Sound)
                gameState = "winScreen"
            #-----------------------------Drawing Everything-------------------------------------#
            mainSurface.fill((255, 255, 255))

            #draw platforms
            pygame.draw.rect(mainSurface, (0,0,0), (0,360,100,480))
            pygame.draw.rect(mainSurface, (0,0,0), (100,325,150,480))
            pygame.draw.rect(mainSurface, (0,0,0), (250,390,230,480))
            
            if frameCount[4] >= 35 and frameCount[4] < 500: #the heart only appears in this frame interval
                mainSurface.blit(life, (randNum[4],randNum[5]))
                if charPos[0] + 40 > randNum[4] and charPos[0] < randNum[4] + 20 and charPos[1] + 51 > randNum[5] and charPos[1] < randNum[5] + 20:
                    pygame.mixer.Sound.play(life_Sound)
                    lives += 1
                    frameCount[4] = 500 #skip to 500 so that this if statement doesnt run again and therefore the character can only collect the life once each time it spawns in
            for counter in range(0,int(end),1): #lines are drawn at every pixel and therefore form a solid bar
                pygame.draw.line(mainSurface, (255,0,0), (150+counter, 100), (150+counter, 120), 1)
            if frameCount[5] >= 300: #300 frames must pass before the laser is drawn
                pygame.draw.line(mainSurface, (255,0,0), (0,250), (480,250), 5)
                if frameCount[7] == 0 and charPos[1] < 250:
                    pygame.mixer.Sound.play(hit_Sound)
                    lives -= 1
                    frameCount[7] = 50 #ensures that they must be a 50 frame interval between each time the character loses a life to the laser
            pygame.draw.rect(mainSurface, (0,0,0), (149,100,201,22),1)
            mainSurface.blit(imgMemory, (charPos[0],charPos[1]))
            mainSurface.blit(boss, (150,0))
            for counter in range (0,len(spikes),1): #draws all the spikes to the screen
                mainSurface.blit(spikeImg, (spikes[counter].posX,spikes[counter].posY))
            livesDisplay()
        elif gameState == "endScreen":
            #-----------------------------Event Handling-----------------------------------------#
            ev = pygame.event.poll()    # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break
            if pygame.mouse.get_pressed()[0] == True: 
                if pygame.mouse.get_pos()[0] > 70 and pygame.mouse.get_pos()[0] < 70 + 330 and pygame.mouse.get_pos()[1] > 110 and pygame.mouse.get_pos()[1] < 110 + 40:
                    pygame.mixer.Sound.play(button_Sound)
                    stage1SetUp()
                    gameState = "stage1"
                elif pygame.mouse.get_pos()[0] > 70 and pygame.mouse.get_pos()[0] < 70 + 330 and pygame.mouse.get_pos()[1] > 170 and pygame.mouse.get_pos()[1] < 170 + 40:
                    pygame.mixer.Sound.play(button_Sound)
                    gameState = "start"
            #-----------------------------Program Logic---------------------------------------------#
            buttonFill(70, 330, 110, 40, 0)
            buttonFill(70, 330, 170, 40, 1)
            #-----------------------------Drawing Everything-------------------------------------#
            #by not filling the screen, whatever the screen was last will stay
            pygame.draw.rect(mainSurface, (buttonColor[0]), (70,110,330,40))
            pygame.draw.rect(mainSurface, (buttonColor[1]), (70,170,330,40))
            mainSurface.blit(text5, text4Rect)
            mainSurface.blit(text6, text6Rect)
            mainSurface.blit(text7, text7Rect)
        elif gameState == "winScreen":
            #-----------------------------Event Handling-----------------------------------------#
            ev = pygame.event.poll()    # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break
            if pygame.mouse.get_pressed()[0] == True: 
                if pygame.mouse.get_pos()[0] > 70 and pygame.mouse.get_pos()[0] < 70 + 330 and pygame.mouse.get_pos()[1] > 110 and pygame.mouse.get_pos()[1] < 110 + 40:
                    pygame.mixer.Sound.play(button_Sound)
                    gameState = "start"
            #-----------------------------Program Logic---------------------------------------------#
            buttonFill(70, 330, 110, 40, 0)
            #-----------------------------Drawing Everything-------------------------------------#
            #by not filling the screen, whatever the screen was last will stay
            pygame.draw.rect(mainSurface, (buttonColor[0]), (70,110,330,40))
            mainSurface.blit(text8, text4Rect)
            mainSurface.blit(text7, text6Rect)
        else:
            #-----------------------------Event Handling-----------------------------------------#
            if pygame.mouse.get_pressed()[0] == True: 
                if gameState == "question" and pygame.mouse.get_pos()[0] >= 60 and pygame.mouse.get_pos()[0] <= 60+360 and pygame.mouse.get_pos()[1] >= 70 and pygame.mouse.get_pos()[1] <= 70+20: #checks if the player clicked on the textbox during the question minigame
                    write = True
                else:
                    write = False
                if pickaxeDisplay == "used" and pygame.mouse.get_pos()[0] >= 0 and pygame.mouse.get_pos()[0] <= 0+80 and pygame.mouse.get_pos()[1] >= 460 and pygame.mouse.get_pos()[1] <= 460+20:
                    pygame.mixer.Sound.play(door_Sound)
                    stage2Setup()
                    gameState = "stage2"
            ev = pygame.event.poll()    # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break                   #   ... leave game loop
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN and write == True:
                    for counter in range (0,len(answerList[randIndex[0]]),1): #the randIndex indicates which answer corresponds with the question being asked so that this can be checked agaisnt the userText. Since there are multiple possible answers for many of the questions, I included lists within the answer list. Therefore, this for loop cycles through all the indexes of the lists within the answerlist.
                        if userText.lower() == answerList[randIndex[0]][counter]:
                            complete[1] = True
                            pygame.mixer.Sound.play(win_Sound)
                    if complete[1] == False:
                        pygame.mixer.Sound.play(hit_Sound)
                        lives -= 1
                    gameState = "stage1"
                elif ev.key == pygame.K_BACKSPACE and gameState == "question":
                    userText = userText[0:len(userText)-1] # "deletes" text by cutting off the last term
                elif gameState == "question" and write == True and text2Rect.width <= 350: #need to make sure that the width of the user text does not surpass the boundary of the text box. If it does, than you can't type anything
                        userText += ev.unicode #adds the code of the keys to the userText variables to print out the text
                if ev.key == pygame.K_e:
                    if groundLevel == 150 and charPos[0] + 40 > 330 and charPos[0] < 370 and complete[0] == False and gameState == "stage1": #if the character is within the range of the sign and gametate is stage1 and the groundLevel is 150
                        pygame.mixer.Sound.play(button_Sound)
                        keyDown = [False,False,False,False] #need to reset these
                        xBoundaries = [90+300-20,90]

                        #Here I appended the old x and y position of the character to the charPos list so that I can access them later to make sure that the player will return back to their original place when the gamestate switches back to stage1
                        charPos.append(charPos[0])
                        charPos.append(charPos[1])

                        charSpeed = [4,4]
                        charPos[0] = 120
                        charPos[1] = 65
                        gameState = "miniMaze"
                    elif groundLevel == 389 and charPos[0]+40 > 200 and charPos[0] < 370 and charPos[1] > 350 and gameState == "stage1" and complete[1] == False:
                        pygame.mixer.Sound.play(button_Sound)
                        gameState = "question"
                        randNum = [random.randint(0,100), random.randint(0,30), random.randint(0,10),random.randint(0,10),0,0]
                        #Each index of the question list corresponds with the indexes in the answer list
                        questionList = (f"What is {randNum[0]}+{randNum[1]}?","How many contenants are there?",f"What's {randNum[2]}*{randNum[3]}?","What is a group of crows called?", "Whats the 3rd largest human organ?", "Which element does 'Pt' represent?")
                        answerList = ([f'{randNum[0]+randNum[1]}'],["seven","7"],[f'{randNum[2]*randNum[3]}'],["murder","a murder"],["the lungs", "lung","lungs"],["platinum"])
                        randIndex[0] = random.randint(0,len(questionList)-1) #chooses random index of the lists in order to get a random question
                        userText = "" #reset it to nothing
                        keyDown = [False, False, False, False]
                        frameCount[1] = 0
                if gameState == "stage1" or gameState == "miniMaze" or gameState == "stage2":
                    charKeyDownInput()
            elif ev.type == pygame.KEYUP:
                if gameState == "stage1" or gameState == "miniMaze" or gameState == "stage2":
                    charKeyUpInput()

            #-----------------------------Program Logic----------------------------------------------
            if gameState == "stage1":
                if complete == [True,True] and charPos[0] + 40 > 465 and charPos[0] < 465 + 15 and charPos[1] + 51 > 315 and charPos[1] < 315 + 125 and pickaxeDisplay == "Collected":
                    pygame.mixer.Sound.play(break_Sound)
                    charPos = [0,389]
                    pickaxeDisplay = "used"

                #set up platforms
                groundLevel = 389 #will default to 389 if the character isn't on any other platforms
                for counter in range (0,12,3): #Every three terms of groundList correspond to eachother, which is why the counter increases by 3 each time and I used counter+1 and counter+2 in order to access the other two indexes. 
                    if charPos[0]+40 >= groundList[counter] and charPos[0] <= groundList[counter+1] and charPos[1] <= groundList[counter+2]:
                        groundLevel = groundList[counter+2]
                        break #I cant use elif statemnts in for loops so I just need to make sure nothing else implements by ending the loop
                
                #makes sure character cant move through the sides of platforms
                if (groundLevel == 389 and charPos[1] < 215 and (charPos[0]+40) >= 310 and keyDown[0] == True):
                    charSpeed[0] = 0
                elif ((groundLevel == 389 or groundLevel == 299) and charPos[0] <= 115 and charPos[0] > 100 and charPos[1]+51 >= 300 and keyDown[1] == True):
                    charSpeed[0] = 0
                    charPos[0] = 115
                elif (pickaxeDisplay == "used" and charPos[0]+40 >= 100 and keyDown[0] == True and groundLevel == 389):
                    charSpeed[0] = 0
                    charPos[0] = 60
                else:
                    if frameCount[0] <= 600 and complete[0] == True: #frameCount[0] counts the amount of frames it took the player to complete the maze. Therefore, this means that if the player takes less than (or equal to) 600 frames, they will be able to move quicker
                        charSpeed[0] = 6
                    else:
                        charSpeed[0] = 4

                if charPos[1] > 300 and charPos[1] < 315 and charPos[0] <= 100 and groundLevel == 389: #y boundaries to prevent the player from jumping past the bottom of the platform
                    charSpeed[1] = 0 #speed is set to 0. This makes it so that, when it is subtracted by 1 later, it will be negative and make the character go down (away from the bottom of the platform)
                    charPos[1] = 315 #y position is set exactly to the bottom of the platform to make sure the character does not go above it

                playerJump()

            elif gameState == "miniMaze":
                frameCount[0] += 1
                for counter in range(0, len(walls), 1):
                    if charPos[0] + 20 > walls[counter].posX1 and charPos[0] < walls[counter].posX1 + walls[counter].posX2 and charPos[1] + 20 > walls[counter].posY1 and charPos[1] < walls[counter].posY1 + walls[counter].posY2:
                        charPos[0] = 120
                        charPos[1] = 65
                        pygame.mixer.Sound.play(hit_Sound)
                        lives -= 1
                if charPos[0] < 95 and charPos[1] > 110 and charPos[1] < 160 and lives > 0:
                    pygame.mixer.Sound.play(win_Sound)
                    complete[0] = True
                    gameState = "stage1"
                    keyDown = [False,False,False,False]
                    charPos[0] = charPos[2]
                    charPos[1] = charPos[3]
                    xBoundaries = [450,-30]

                #allows player to move up
                if keyDown[2] == True:
                    charPos[1] -= charSpeed[1]
                if keyDown[3] == True:
                    charPos[1] += charSpeed[1]

                #y boundaries
                if charPos[1]+20 > 380:
                    charPos[1] -= charSpeed[1]
                if charPos[1] < 60:
                    charPos[1] += charSpeed[1]
            elif gameState == "question":
                text = fonts[0].render(f'{questionList[randIndex[0]]}', True, (3, 90, 102))
                textRect = text.get_rect()
                textRect.center = (240, 30)

                text2 = fonts[1].render(f'{userText}', True, (3, 90, 102))
                text2Rect = text2.get_rect()
                text2Rect.topleft = (60+2.5, 70+2.5)
                
                frameCount[1] += 1
                if frameCount[1] == 600:
                    pygame.mixer.Sound.play(hit_Sound)
                    lives -= 1
                    gameState = "stage1"

            if lives <= 0:
                pygame.mixer.Sound.play(death_Sound)
                gameState = "endScreen"
            
            playerMove()
            #-----------------------------Drawing Everything-------------------------------------#
            # We draw everything from scratch on each frame.
            # So first fill everything with the background color
            mainSurface.fill((255, 255, 255))

            for counter in range (0,24,4):
                pygame.draw.rect(mainSurface, (0,0,0), (platformsPos[counter],platformsPos[counter+1],platformsPos[counter+2], platformsPos[counter+3]))

            mainSurface.blit(sign, (330,155))
            mainSurface.blit(sign, (200,400))
            mainSurface.blit(door, (30,340))
            if pickaxeDisplay == "notCollected":
                mainSurface.blit(pickaxe, (randPos[randIndex[1]], randPos[randIndex[1]+1])) #I cant just make the x and y position random numbers because then the pickaxe would spawn in nonsensical places. Therefore I made a list of random x and y positions and generated a random index of that list to cycle through it randomly.
            if complete == [True,True]:
                if pickaxeDisplay == "notCollected" and charPos[0] + 40 > randPos[randIndex[1]] and charPos[0] < randPos[randIndex[1]] + 30 and charPos[1] + 51 > randPos[randIndex[1]+1] and charPos[1] < randPos[randIndex[1]+1] + 31:
                    pygame.mixer.Sound.play(pickaxe_Sound)
                    pickaxeDisplay = "Collected"
                if pickaxeDisplay == "Collected":
                    mainSurface.blit(pickaxe, (charPos[0]+31, charPos[1]))
            else:
                mainSurface.blit(lock, (randPos[randIndex[1]], randPos[randIndex[1]+1]+5))
            if pickaxeDisplay != "used": #when it equals "used" the brick walls will dissapeer
                mainSurface.blit(brick, (0,315))
                mainSurface.blit(brick, (465,315))
            if complete == [False,False]:
                mainSurface.blit(lock, ((randPos[randIndex[1]])+15, randPos[randIndex[1]+1]+5))

            # Draw character on the screen
            if gameState == "stage1":
                mainSurface.blit(imgMemory, (charPos[0],charPos[1]))
                if ((groundLevel == 150 and charPos[0] + 40 > 330 and charPos[0] < 370 and charPos[1] > 105 and complete[0] == False) or (groundLevel == 389 and charPos[0]+40 > 200 and charPos[0] < 270 and charPos[1] > 350 and complete[1] == False)):
                    mainSurface.blit(pressE, (0,460))
                if pickaxeDisplay == "used":
                    mainSurface.blit(open, (0,460))
            elif gameState == "miniMaze":
                pygame.draw.rect(mainSurface, (104, 178, 212), (90,60,300,320))
                pygame.draw.rect(mainSurface, (0,0,0), (charPos[0],charPos[1],20,20))
                for counter in range(0, len(walls), 1):
                    pygame.draw.rect(mainSurface,(3, 90, 102),(walls[counter].posX1, walls[counter].posY1,walls[counter].posX2,walls[counter].posY2))
            elif gameState == "question":
                pygame.draw.rect(mainSurface, (104, 178, 212), (60,70,360,20))
                mainSurface.blit(imgMemory, (charPos[0],charPos[1]))
                mainSurface.blit(text2, text2Rect)
                mainSurface.blit(text, textRect)
            livesDisplay()
        
        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower


    pygame.quit()     # Once we leave the loop, close the window.

main()
