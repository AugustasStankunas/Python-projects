import sys, random
import numpy as np
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
random.seed(1) # make the simulation the same each time, easier to debug
import pygame
import pymunk
import pymunk.pygame_util

#initializes the top body (static point on which the pendulum swings)
def initialize(space, firstBallPos = (400, 200), secondBallPos = (400, 350)):
    topBody = pymunk.Body(body_type = pymunk.Body.STATIC)
    topBody.position = (400, 50)
    topBodyShape = pymunk.Circle(topBody, 5)
    space.add(topBody, topBodyShape)

    circleBody = pymunk.Body(40, 50, body_type=pymunk.Body.DYNAMIC)
    circleBody.position = firstBallPos
    circleShape = pymunk.Circle(circleBody, 25)
    joint = pymunk.PinJoint(topBody, circleBody)
    space.add(circleBody, circleShape, joint)

    circle2Body = pymunk.Body(70, 50, body_type=pymunk.Body.DYNAMIC)
    circle2Body.position = secondBallPos
    circle2Shape = pymunk.Circle(circle2Body, 25)
    joint2 = pymunk.PinJoint(circleBody, circle2Body)
    space.add(circle2Body, circle2Shape, joint2)

#draws text at the position pos
def DrawText(text, x : int, y : int, screen):
    font = pygame.font.SysFont("Arial", 24)
    img = font.render(text, True, (10, 10, 10))
    screen.blit(img, (x, y))

#draws all the text on the screen for the sliders and keyboard controls
def DrawAllText(screen, slider1, slider2, slider3, slider4, space):
    DrawText(f'Mass of first ball: {slider1.getValue():.2f}', 900, 20, screen)
    DrawText(f'Mass of second ball: {slider2.getValue():.2f}', 880, 100, screen)
    DrawText(f'Gravity: {slider3.getValue():.2f}', 930, 180, screen)
    DrawText(f'Time step: {slider4.getValue():.2f}', 930, 260, screen)   
    DrawText('Press D for default values', 860, 340, screen)

#updates the properties of the balls and gravity
def UpdateProperties(firstMass, secondMass, gravity, space):
    space.bodies[1].mass = 40 * firstMass
    space.bodies[2].mass = 70 * secondMass
    space.gravity = (0.0, 300 * gravity)

#sets the default values for the sliders 
def SetDefaultValues(slider1, slider2, slider3, slider4):
    slider1.setValue(1)
    slider2.setValue(1)
    slider3.setValue(1)
    slider4.setValue(1)

def SetFirstBallPosition(mousePos : 'tuple[int, int]', space):
    previousX = space.bodies[1].position[0] 
    previousY = space.bodies[1].position[1]
    previousDistance = np.sqrt(previousX**2 + previousY**2)
    space.bodies[1].position = mousePos

def MouseInBall(mousePos : 'tuple[int, int]', ballPos : 'tuple[int, int]', ballSize : int):
    distance = np.sqrt((mousePos[0] - ballPos[0])**2 + (mousePos[1] - ballPos[1])**2)
    return distance <= ballSize


def main():
    #initializing pygame screen and pymunk space
    pygame.init()
    screen = pygame.display.set_mode((1300, 500))
    pygame.display.set_caption("Double pendulum")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 500)
    initialize(space)

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    #variables later used for the start of the simulation, where the user places the balls
    dragFirst = False
    dragSecond = False

    #initializing the sliders, used to control the mass, inertia of the balls and gravity
    slider1 = Slider(screen, 880, 70, 200, 10, min=0.01, max=3, step=0.05, initial = 1)
    slider2 = Slider(screen, 880, 150, 200, 10, min=0.01, max=3, step=0.05, initial = 1)
    slider3 = Slider(screen, 880, 230, 200, 10, min=0, max=3, step=0.05, initial = 1)
    slider4 = Slider(screen, 880, 310, 200, 10, min=0, max=3, step=0.05, initial = 1)

    SetDefaultValues(slider1, slider2, slider3, slider4)

    step = 1/20

    while True:
        #going through events of the simulation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                SetDefaultValues(slider1, slider2, slider3, slider4)

            #if the R button is pressed the game is reset
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                #print(space.bodies)
                #print(space.shapes)
                space = pymunk.Space()
                space.gravity = (0.0, 300)
                initialize(space)
                
            elif event.type == pygame.MOUSEBUTTONDOWN and MouseInBall(pygame.mouse.get_pos(), space.bodies[1].position, 25):
                dragFirst = True
                space.bodies[1].position = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONDOWN and MouseInBall(pygame.mouse.get_pos(), space.bodies[2].position, 25):
                dragSecond = True

            elif event.type == pygame.MOUSEBUTTONUP:
                dragFirst = False
                dragSecond = False

            elif event.type == pygame.MOUSEMOTION and dragFirst:
                secondBallPos = space.bodies[2].position
                space = pymunk.Space()
                space.gravity = (0.0, 300)
                initialize(space, pygame.mouse.get_pos(), secondBallPos)

            elif event.type == pygame.MOUSEMOTION and dragSecond:
                firstBallPos = space.bodies[1].position
                space = pymunk.Space()
                space.gravity = (0.0, 300)
                initialize(space, firstBallPos, pygame.mouse.get_pos())

                

        #start of every frame - clearing the screen, updating the simulation, drawing the simulation and updating the sliders
        screen.fill((255,255,255))
        if not dragFirst and not dragSecond:
            space.step(step)  

        space.debug_draw(draw_options)
        pygame_widgets.update(pygame.event.get())
        DrawAllText(screen, slider1, slider2, slider3, slider4, space)
        
        UpdateProperties(slider1.getValue(), slider2.getValue(), slider3.getValue(), space)
        step = 1/20 * slider4.getValue()

        clock.tick(60)   
        pygame.display.flip()       

if __name__ == '__main__':
    main()