import pygame

class wall():
    def __init__(self, posX1, posX2, posY1, posY2):
        self.posX1 = posX1
        self.posX2 = posX2
        self.posY1 = posY1
        self.posY2 = posY2
    
 #   def draw(self,surface):
#        self.surface = surface
#        pygame.draw.rect(self.surface, (0,0,0), (self.posX1,self.posY1,self.posX2,self.posY2))

def main():
    #-----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = 480   # Desired physical surface size, in pixels.
    rectangles = []
    rectangles.append(wall(0,3,5,6))
    rectangles.append(wall(20,49,69,49))
    rectangles.append(wall(100,49,58,6))
    rectangles.append(wall(2,50,2,5))
    
    clock = pygame.time.Clock()  #Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))
    
    #-----------------------------Program Variable Initialization----------------------------#
    # Set up some data to describe a small circle and its color

    #-----------------------------Main Program Loop---------------------------------------------#
    while True:       
        #-----------------------------Event Handling-----------------------------------------#
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop
        
        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here...
        for counter in range(0, len(rectangles), 1):
            if (rectangles[counter].posX1 == 2):
                print(True)
        break
            

        #-----------------------------Drawing Everything-------------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        mainSurface.fill((255, 255, 255))
        for counter in range(0, len(rectangles), 1):
           pygame.draw.rect(mainSurface,(0,0,0),(rectangles[counter].posX1, rectangles[counter].posY1,rectangles[counter].posX2,rectangles[counter].posY2))

               
        # Draw a circle on the surface
        
        # Draw character on the screen
        
        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower

    pygame.quit()     # Once we leave the loop, close the window.

main()