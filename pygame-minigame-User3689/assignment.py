import pygame

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
    charPos = [100,389]
    charSpeed = [4,4]
    keyDown = [False,False]
    frameCount = 0

    #Load an image
    charImg = [pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (1).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (2).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (3).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (4).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (5).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (6).png"),pygame.image.load("dcbwv3h-47b1c55e-0154-46ec-afec-64fda9477530 (7).png")]


    #-----------------------------Main Program Loop---------------------------------------------#
    while True:       
        #-----------------------------Event Handling-----------------------------------------#
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RIGHT:
                keyDown[0] = True
            elif ev.key == pygame.K_LEFT:
                keyDown[1] = True
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_RIGHT:
                keyDown[0] = False
            elif ev.key == pygame.K_LEFT:
                keyDown[1] = False

        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here...
        if keyDown[0] == True:
            if frameCount == 5:
                imgMemory = charImg[6]
            if frameCount == 10:
                imgMemory = charImg[5]
            if frameCount == 15:
                imgMemory = charImg[4]
                frameCount = 0
            charPos[0] += charSpeed[0]
            frameCount += 1
        if keyDown[1] == True:
            if frameCount == 5:
                imgMemory = charImg[1]
            if frameCount == 10:
                imgMemory = charImg[2]
            if frameCount == 15:
                imgMemory = charImg[3]
                frameCount = 0
            charPos[0] -= charSpeed[0]
            frameCount += 1
        if keyDown[0] == True and keyDown[1] == True:
            imgMemory = charImg[0]
        if charPos[0] > 450:
            charPos[0] -= charSpeed[0]
        if charPos[0] < -30:
            charPos[0] += charSpeed[0]

        #-----------------------------Drawing Everything-------------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        mainSurface.fill((255, 255, 255))

               
        # Draw a circle on the surface
        pygame.draw.rect(mainSurface, (0,0,0), (0,440,480, 480))
        
        # Draw character on the screen
        if keyDown[0] == False and keyDown[1] == False:
            frameCount = 0
            imgMemory = charImg[0]
        mainSurface.blit(imgMemory, (charPos[0],charPos[1]))

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower


    pygame.quit()     # Once we leave the loop, close the window.

main()