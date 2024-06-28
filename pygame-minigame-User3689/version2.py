import pygame
import random

class wall():
    def __init__(self, posX1, posY1, posX2, posY2):
        self.posX1 = posX1
        self.posY1 = posY1
        self.posX2 = posX2
        self.posY2 = posY2

def main():
    #-----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = 480   # Desired physical surface size, in pixels.
    walls = [wall(90,60,5,50),wall(90,160,5,220), wall(145,60,245,5),wall(385,60,5,320),wall(90,375,300,5),wall(90,105,150,5),wall(135,105,5,50),wall(235,105,5,50),wall(235,155,50,5),wall(280,155,5,50),wall(280,200,50,5),wall(300,110,50,5),wall(300,60,5,50),wall(340,155,50,5),wall(325,200,5,130),wall(280,200,5,130),wall(235,330,50,5),wall(90,210,50,5),wall(135,210,5,50),wall(185,260,5,120),wall(140,330,50,5),wall(185,260,50,5),wall(185,260,50,5),wall(230,215,5,50),wall(185,210,50,5), wall(185,160,5,50)]
    clock = pygame.time.Clock()  #Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    #-----------------------------Program Variable Initialization----------------------------#
    # Set up some data to describe a small circle and its color
    charPos = [430,150]
    charSpeed = [4,0]
    keyDown = [False,False,False,False]
    jumping = False
    gameState = "stage1"
    xBoundaries = [450,-30]
    lives = 3
    frameCount = [0,0]
    write = False
    complete = [False,False]
    pickaxeDisplay = "notCollected"
    randIndex = [0,random.randrange(0, 10+2,2)]
    randPos = [300,409,30,80,400,169,170,169,30,269,250,90]
    groundList = [310,480,150, 0,115-6,249, 115,120,299, 180,190,149]
    platformsPos = [0,440,480,480,300,200,480,15,100,300,15,330,0,300,100,15,100,350,30,15,170,200,30,15]
    global end #need to declare as a global variable so that I can use it in the charKeyDownInput function
    global bossHealth

    #render font
    font = [pygame.font.Font('freesansbold.ttf', 22), pygame.font.Font('freesansbold.ttf', 12)]

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

    def playerJump():
        global jumping
        global bossHealth
        global end
        if keyDown[2] == True and jumping == False:
            if gameState == "stage2":
                bossHealth -= 1
                end -= 2 #200/100 is 2, therefore each time the boss looses one life it is equivalent to 1.5 of the lines 
            charSpeed[1] = -15
            jumping = True
        charPos[1] += charSpeed[1]
        if charPos[1] >= groundLevel:
            charPos[1] = groundLevel
            charSpeed[1] = 0
            jumping = False
        else:
            charSpeed[1] += 1
    
    def playerMove():
        #Character movement
        if keyDown[0] == True:
            charPos[0] += charSpeed[0]
        if keyDown[1] == True:
            charPos[0] -= charSpeed[0]
    
        #x boundaries
        if charPos[0] > xBoundaries[0]:
            charPos[0] -= charSpeed[0]
        if charPos[0] < xBoundaries[1]:
            charPos[0] += charSpeed[0]
    
    def charKeyDownInput():
        if ev.key == pygame.K_UP:
            if charPos[1] == groundLevel or gameState == "miniMaze":
                keyDown[2] = True
        elif ev.key == pygame.K_DOWN:
            keyDown[3] = True
        if ev.key == pygame.K_RIGHT:
            keyDown[0] = True
        elif ev.key == pygame.K_LEFT:
            keyDown[1] = True

    def charKeyUpInput():
        if ev.key == pygame.K_UP:
            keyDown[2] = False
        elif ev.key == pygame.K_DOWN:
            keyDown[3] = False
        if ev.key == pygame.K_RIGHT:
            keyDown[0] = False
        elif ev.key == pygame.K_LEFT:
            keyDown[1] = False

    def gameOver():
        if lives <= 0:
            gameState = "endScreen"

    #-----------------------------Main Program Loop---------------------------------------------#
    while True:
        if gameState == "start":
            #-----------------------------Event Handling-----------------------------------------#
    
            #-----------------------------Program Logic---------------------------------------------#
    
            #-----------------------------Drawing Everything-------------------------------------#
            pass
        elif gameState == "instructions":
            #-----------------------------Event Handling-----------------------------------------#
    
            #-----------------------------Program Logic---------------------------------------------#
        
            #-----------------------------Drawing Everything-------------------------------------#   
            pass
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
            for counter in range (0,9,3):
                if charPos[0]+40 > groundList[counter] and charPos[0] < groundList[counter+1] and charPos[1] <= groundList[counter+2]:
                    groundLevel = groundList[counter+2]
                    break

            if (groundLevel == 309 and charPos[1]+51 > 325 and (charPos[0]+40) >= 100 and keyDown[0] == True):
                charSpeed[0] = 0
                charPos[0] = 60
            elif groundLevel == 339 and charPos[1]+51 > 274 and charPos[0] <= 250 and keyDown[1] == True:
                charSpeed[0] = 0
                charPos[0] = 250
            else:
                if frameCount[0] <= 600 and complete[0] == True:
                    charSpeed[0] = 6
                else:
                    charSpeed[0] = 4
            playerJump()
            playerMove()
            gameOver()
            if bossHealth <= 0:
                gameState = "winScreen"
            #-----------------------------Drawing Everything-------------------------------------#
            mainSurface.fill((255, 255, 255))
            pygame.draw.rect(mainSurface, (0,0,0), (0,360,100,480))
            pygame.draw.rect(mainSurface, (0,0,0), (100,325,150,480))
            pygame.draw.rect(mainSurface, (0,0,0), (250,390,230,480))
            for counter in range(0,int(end),1):
                pygame.draw.line(mainSurface, (255,0,0), (150+counter, 100), (150+counter, 120), 1)
            pygame.draw.rect(mainSurface, (0,0,0), (149,100,201,22),1)
            mainSurface.blit(charImg[0], (charPos[0],charPos[1]))
            mainSurface.blit(boss, (150,0))
        elif gameState == "endScreen":
            #-----------------------------Event Handling-----------------------------------------#
            ev = pygame.event.poll()    # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break     
            #-----------------------------Program Logic---------------------------------------------#
            
            #-----------------------------Drawing Everything-------------------------------------#
        elif gameState == "winScreen":
            #-----------------------------Event Handling-----------------------------------------#
            ev = pygame.event.poll()    # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break     
            #-----------------------------Program Logic---------------------------------------------#
            
            #-----------------------------Drawing Everything-------------------------------------#
        else:
            #-----------------------------Event Handling-----------------------------------------#
            if pygame.mouse.get_pressed()[0] == True: 
                if gameState == "question" and pygame.mouse.get_pos()[0] >= 60 and pygame.mouse.get_pos()[0] <= 60+360 and pygame.mouse.get_pos()[1] >= 70 and pygame.mouse.get_pos()[1] <= 70+20:
                    write = True
                else:
                    write = False
                if pickaxeDisplay == "used" and pygame.mouse.get_pos()[0] >= 0 and pygame.mouse.get_pos()[0] <= 0+80 and pygame.mouse.get_pos()[1] >= 460 and pygame.mouse.get_pos()[1] <= 460+20:
                    charPos = [300,100]
                    groundList = [0,100-40+5,309,100+5,250-5,274,250-5,480,339] #I subtracted and added a few pixels in certain places in order to make the hitbox more accurate
                    gameState = "stage2"
                    bossHealth = 100
                    end = 200
            ev = pygame.event.poll()    # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break                   #   ... leave game loop
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN and write == True:
                    for counter in range (0,len(answerList[randIndex[0]]),1):
                        if userText.lower() == answerList[randIndex[0]][counter]:
                            complete[1] = True
                    if complete[1] == False:
                        lives -= 1
                    gameState = "stage1"
                elif ev.key == pygame.K_BACKSPACE and gameState == "question":
                    userText = userText[0:len(userText)-1]
                elif gameState == "question" and write == True and text2Rect.width <= 350:
                        userText += ev.unicode
                if ev.key == pygame.K_e:
                    if groundLevel == 150 and charPos[0] + 40 > 330 and charPos[0] < 370 and complete[0] == False and gameState == "stage1":
                        keyDown = [False,False,False,False]
                        xBoundaries = [90+300-20,90]
                        charPos.append(charPos[0])
                        charPos.append(charPos[1])
                        charSpeed = [4,4]
                        charPos[0] = 120
                        charPos[1] = 65
                        gameState = "miniMaze"
                    elif groundLevel == 389 and charPos[0]+40 > 200 and charPos[0] < 370 and charPos[1] > 350 and gameState == "stage1" and complete[1] == False:
                        gameState = "question"
                        randNum = [random.randint(0,100), random.randint(0,30), random.randint(0,10),random.randint(0,10)]
                        questionList = [f"What is {randNum[0]}+{randNum[1]}?","How many contenants are there?",f"What's {randNum[2]}*{randNum[3]}?","What is a group of crows called?", "Whats the 3rd largest human organ?", "Which element does 'Pt' represent?"]
                        answerList = [[f'{randNum[0]+randNum[1]}'],["seven","7"],[f'{randNum[2]*randNum[3]}'],["murder","a murder"],["the lungs", "lung","lungs"],["platinum"]]
                        randIndex[0] = random.randint(0,len(questionList)-1)
                        charSpeed[0] = 0
                        userText = ""
                        keyDown = [False, False, False, False]
                        frameCount[1] = 0
                if gameState == "stage1" or gameState == "miniMaze" or gameState == "stage2":
                    charKeyDownInput()
            elif ev.type == pygame.KEYUP:
                if gameState == "stage1" or gameState == "miniMaze" or gameState == "stage2":
                    charKeyUpInput()

            #-----------------------------Program Logic---------------------------------------------#
            gameOver()

            if gameState == "stage1":
                if complete == [True,True] and charPos[0] + 40 > 465 and charPos[0] < 465 + 15 and charPos[1] + 51 > 315 and charPos[1] < 315 + 125 and pickaxeDisplay == "Collected":
                    charPos = [0,389]
                    pickaxeDisplay = "used"

                #set up platforms
                groundLevel = 389 #will default to 389 if the character isn't on any other platforms
                for counter in range (0,12,3):
                    if charPos[0]+40 >= groundList[counter] and charPos[0] <= groundList[counter+1] and charPos[1] <= groundList[counter+2]:
                        groundLevel = groundList[counter+2]
                        break #I cant use elif statemnts in for loops so I just need to make sure nothing else implements by ending the loop
                
                if (groundLevel == 389 and charPos[1] < 215 and (charPos[0]+40) >= 310 and keyDown[0] == True):
                    charSpeed[0] = 0
                elif ((groundLevel == 389 or groundLevel == 299) and charPos[0] <= 115 and charPos[0] > 100 and charPos[1]+51 >= 300 and keyDown[1] == True):
                    charSpeed[0] = 0
                    charPos[0] = 115
                elif (pickaxeDisplay == "used" and charPos[0]+40 >= 100 and keyDown[0] == True and groundLevel == 389):
                    charSpeed[0] = 0
                    charPos[0] = 60
                else:
                    if frameCount[0] <= 600 and complete[0] == True:
                        charSpeed[0] = 6
                    else:
                        charSpeed[0] = 4

                if charPos[1] > 300 and charPos[1] < 315 and charPos[0] <= 100 and groundLevel == 389:
                    charSpeed[1] = 0
                    charPos[1] = 315

                playerJump()

            elif gameState == "miniMaze":
                frameCount[0] += 1
                for counter in range(0, len(walls), 1):
                    if charPos[0] + 20 > walls[counter].posX1 and charPos[0] < walls[counter].posX1 + walls[counter].posX2 and charPos[1] + 20 > walls[counter].posY1 and charPos[1] < walls[counter].posY1 + walls[counter].posY2:
                        charPos[0] = 120
                        charPos[1] = 65
                        lives -= 1
                if charPos[0] < 95 and charPos[1] > 110 and charPos[1] < 160 and lives > 0:
                    complete[0] = True
                    gameState = "stage1"
                    keyDown = [False,False,False,False]
                    charPos[0] = charPos[2]
                    charPos[1] = charPos[3]
                    xBoundaries = [450,-30]
                if frameCount[1] == 300:
                    lives -= 1
                    gameState = "stage1"

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
                question = questionList[randIndex[0]]

                text = font[0].render(f'{question}', True, (3, 90, 102))
                textRect = text.get_rect()
                textRect.center = (240, 30)

                text2 = font[1].render(f'{userText}', True, (3, 90, 102))
                text2Rect = text2.get_rect()
                text2Rect.topleft = (60+2.5, 70+2.5)
                
                frameCount[1] += 1

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
                mainSurface.blit(pickaxe, (randPos[randIndex[1]], randPos[randIndex[1]+1]))
            if complete == [True,True]:
                if charPos[0] + 40 > randPos[randIndex[1]] and charPos[0] < randPos[randIndex[1]] + 30 and charPos[1] + 51 > randPos[randIndex[1]+1] and charPos[1] < randPos[randIndex[1]+1] + 31:
                    pickaxeDisplay = "Collected"
                if pickaxeDisplay == "Collected":
                    mainSurface.blit(pickaxe, (charPos[0]+31, charPos[1]))
            else:
                mainSurface.blit(lock, (randPos[randIndex[1]], randPos[randIndex[1]+1]+5))
            if pickaxeDisplay != "used":
                mainSurface.blit(brick, (0,315))
                mainSurface.blit(brick, (465,315))
            if complete == [False,False]:
                mainSurface.blit(lock, ((randPos[randIndex[1]])+15, randPos[randIndex[1]+1]+5))

            # Draw character on the screen
            if gameState == "stage1":
                mainSurface.blit(charImg[0], (charPos[0],charPos[1]))
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
                mainSurface.blit(charImg[0], (charPos[0],charPos[1]))
                mainSurface.blit(text2, text2Rect)
                mainSurface.blit(text, textRect)

            # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower


    pygame.quit()     # Once we leave the loop, close the window.

main()
