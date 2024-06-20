import sys, random
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
random.seed(1) # make the simulation the same each time, easier to debug
import pygame
import pymunk
import pymunk.pygame_util

#initializes the top body (static point on which the pendulum swings)
def initialize(space):
    topbody = pymunk.Body(body_type = pymunk.Body.STATIC)
    topbody.position = (400, 50)
    topBodyShape = pymunk.Circle(topbody, 5)
    space.add(topbody, topBodyShape)

#creates the first ball at position pos and attaches it to the top body by a pin joint
def firstBall(topBody, space, pos):
    circleBody = pymunk.Body(100, 500, body_type=pymunk.Body.DYNAMIC)
    circleBody.position = pos
    circleShape = pymunk.Circle(circleBody, 15)
    joint = pymunk.PinJoint(topBody, circleBody)
    space.add(circleBody, circleShape, joint)

#creates the second ball at position pos and attaches it to the first ball by a pin joint
def secondBall(circle1, space, pos):
    circleBody = pymunk.Body(80, 500, body_type=pymunk.Body.DYNAMIC)
    circleBody.position = pos
    circleShape = pymunk.Circle(circleBody, 15)
    joint = pymunk.PinJoint(circle1, circleBody)
    space.add(circleBody, circleShape, joint)

#draws text at the position pos
def DrawText(text, x : int, y : int, screen):
    font = pygame.font.SysFont("Arial", 24)
    img = font.render(text, True, (10, 10, 10))
    screen.blit(img, (x, y))

#draws all the text on the screen for the sliders and keyboard controls
def DrawAllText(screen, slider1, slider2, slider3, slider4, slider5):
    DrawText(f'Mass of first ball: {slider1.getValue()}', 900, 20, screen)
    DrawText(f'Mass of second ball: {slider2.getValue()}', 880, 100, screen)
    DrawText(f'Momentum of first ball: {slider3.getValue()}', 860, 180, screen)
    DrawText(f'Momentum of second ball: {slider4.getValue()}', 830, 260, screen)
    DrawText(f'Gravity: {slider5.getValue()}', 930, 340, screen)
    DrawText('Press D for default values', 860, 420, screen)

#updates the properties of the balls and gravity
def UpdateProperties(firstMass, firstMomentum, secondMass, secondMomentum, gravity, space):
    space.bodies[1].mass = firstMass
    space.bodies[1].moment = firstMomentum
    space.bodies[2].mass = secondMass
    space.bodies[2].moment = secondMomentum
    space.gravity = (0.0, gravity)

#sets the default values for the sliders 
def SetDefaultValues(slider1, slider2, slider3, slider4, slider5):
    slider1.setValue(100)
    slider2.setValue(80)
    slider3.setValue(500)
    slider4.setValue(500)
    slider5.setValue(500)

def main():
    #initializing pygame screen and pymunk space
    pygame.init()
    screen = pygame.display.set_mode((1100, 500))
    pygame.display.set_caption("Double pendulum")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 500)
    initialize(space)

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    #variables later used for the start of the simulation, where the user places the balls
    pause = True
    circleCount = 0

    #initializing the sliders, used to control the mass, inertia of the balls and gravity
    slider1 = Slider(screen, 880, 70, 200, 10, min=1, max=500, step=10)
    slider2 = Slider(screen, 880, 150, 200, 10, min=1, max=500, step=10)
    slider3 = Slider(screen, 880, 230, 200, 10, min=1, max=1000, step=50)
    slider4 = Slider(screen, 880, 310, 200, 10, min=1, max=1000, step=50)
    slider5 = Slider(screen, 880, 390, 200, 10, min=1, max=1000, step=50)

    SetDefaultValues(slider1, slider2, slider3, slider4, slider5)
    while True:
        #going through events of the simulation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                SetDefaultValues(slider1, slider2, slider3, slider4, slider5)
            #if the R button is pressed the game is reset
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                space = pymunk.Space()
                space.gravity = (0.0, 500)
                initialize(space)
                circleCount = 0
                pause = True  
            #if there is one ball on the screen and the mouse is clicked, the second ball is created at the position of the click             
            elif circleCount == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                secondBall(space.bodies[1], space, mousePos)
                circleCount = -1
                pause = False
            #if there are no balls on the screen and the mouse is clicked, the first ball is created at the position of the click
            elif circleCount == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                firstBall(space.bodies[0], space, mousePos)
                circleCount += 1

        #start of every frame - clearing the screen, updating the simulation, drawing the simulation and updating the sliders
        screen.fill((255,255,255))
        if not pause:
            space.step(1/30)  

        space.debug_draw(draw_options)
        pygame_widgets.update(pygame.event.get())
        DrawAllText(screen, slider1, slider2, slider3, slider4, slider5)
        
        if circleCount == -1:
            UpdateProperties(slider1.getValue(), slider2.getValue(), slider3.getValue(), slider4.getValue(), slider5.getValue(), space)

        clock.tick(50)   
        pygame.display.flip()       

if __name__ == '__main__':
    main()
