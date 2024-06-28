import pygame

class wall():
    def __init__(self, posX1, posX2, posY1, posY2):
        self.posX1 = posX1
        self.posX2 = posX2
        self.posY1 = posY1
        self.posY2 = posY2

def main():
    #-----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = 480   # Desired physical surface size, in pixels.
    
    clock = pygame.time.Clock()  #Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    #-----------------------------Program Variable Initialization----------------------------#
    # Set up some data to describe a small circle and its color
    charPos = [430,150]
    #(100, 389) for the ground
    charSpeed = [4,0]
    keyDown = [False,False,False,False]
    jumping = False
    gameState = "stage1"
    xBoundaries = [450,-30]

    #Load an image
    charImg = [pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (1).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (2).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (3).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (4).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (5).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (6).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (7).png")]
    sign = pygame.image.load("Sign-removebg-preview.png")
    pressE = pygame.image.load("pressE.png")

    #-----------------------------Main Program Loop---------------------------------------------#
    while True:       
        #-----------------------------Event Handling-----------------------------------------#
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_e:
                if groundLevel == 150 and charPos[0] + 40 > 330 and charPos[0] < 370:
                    keyDown = [False,False,False,False]
                    xBoundaries = [375,105]
                    charPos.append(charPos[0])
                    charPos.append(charPos[1])
                    charPos[0] = 225
                    charPos[1] = 75
                    gameState = "miniMaze"
                    #when i have to switch back to stage1, I can do this to make sure that the character is in its original spot
                    #charPos[0] = charPos[2]
                    #charPos[1] = charPos[3]
                    #gameState = "stage1"
                elif groundLevel == 389 and charPos[0]+40 > 200 and charPos[0] < 370 and charPos[1] >350:
                    gameState = "question"
            if ev.key == pygame.K_UP:
                keyDown[2] = True
            elif ev.key == pygame.K_DOWN:
                keyDown[3] = True
            if ev.key == pygame.K_RIGHT:
                keyDown[0] = True
            elif ev.key == pygame.K_LEFT:
                keyDown[1] = True
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_UP:
                keyDown[2] = False
            elif ev.key == pygame.K_DOWN:
                keyDown[3] = False
            if ev.key == pygame.K_RIGHT:
                keyDown[0] = False
            elif ev.key == pygame.K_LEFT:
                keyDown[1] = False
        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here...
        if gameState == "stage1":
            if keyDown[2] == True and jumping == False:
                charSpeed[1] = -15
                jumping = True

        #set up platforms
            if (charPos[0]+31) >= 300 and charPos[1] <= 150:
                groundLevel = 150
            elif charPos[0] <= 115 and charPos[1] <= 249:
                groundLevel = 249
            else:
                groundLevel = 389
            if groundLevel == 389 and charPos[1] < 215 and (charPos[0]+31) > 300:
                charSpeed[0] = 0
            else:
                charSpeed[0] = 4

        #y position
            charPos[1] += charSpeed[1]
            if charPos[1] >= groundLevel:
                charPos[1] = groundLevel
                charSpeed[1] = 0
                jumping = False
            else:
                charSpeed[1] += 1

        elif gameState == "miniMaze":
            charSpeed = [4,4]
            if keyDown[2] == True:
                charPos[1] -= charSpeed[1]
            if keyDown[3] == True:
                charPos[1] += charSpeed[1]

            #y boundaries
            if charPos[1] > 365:
                charPos[1] -= charSpeed[1]
            if charPos[1] < 75:
                charPos[1] += charSpeed[1]

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
        #-----------------------------Drawing Everything-------------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        mainSurface.fill((255, 255, 255))
        
               
        pygame.draw.rect(mainSurface, (0,0,0), (0,440,480, 480))
        pygame.draw.rect(mainSurface, (0,0,0), (300,200,480,15))
        pygame.draw.rect(mainSurface, (0,0,0), (100,300,15,330))
        pygame.draw.rect(mainSurface, (0,0,0), (0,300,100,15))
        pygame.draw.rect(mainSurface, (0,0,0), (100,350,30,15))
        mainSurface.blit(sign, (330,155))
        mainSurface.blit(sign, (200,400))
        
        # Draw character on the screen
        if gameState == "stage1":
            mainSurface.blit(charImg[0], (charPos[0],charPos[1]))
            if (groundLevel == 150 and charPos[0] + 40 > 330 and charPos[0] < 370 and charPos[1] > 105) or (groundLevel == 389 and charPos[0]+40 > 200 and charPos[0] < 370 and charPos[1] >350):
                mainSurface.blit(pressE, (0,460))
        elif gameState == "miniMaze":
            pygame.draw.rect(mainSurface, (104, 178, 212), (90,60,300,320))
            pygame.draw.circle(mainSurface, (0,0,0), (charPos[0],charPos[1]), 15)

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower


    pygame.quit()     # Once we leave the loop, close the window.

main()
