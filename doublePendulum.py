import sys, random
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
random.seed(1) # make the simulation the same each time, easier to debug
import pygame
import pymunk
import pymunk.pygame_util

def initialize(space, screen):
    topbody = pymunk.Body(body_type = pymunk.Body.STATIC)
    topbody.position = (400, 50)
    topBodyShape = pymunk.Circle(topbody, 5)
    DrawText("Mass of first ball", 100, 100, screen)
    space.add(topbody, topBodyShape)

def firstBall(topBody, space, pos):
    circleBody = pymunk.Body(100, 500, body_type=pymunk.Body.DYNAMIC)
    circleBody.position = pos
    circleShape = pymunk.Circle(circleBody, 15)
    joint = pymunk.PinJoint(topBody, circleBody)
    space.add(circleBody, circleShape, joint)

def secondBall(circle1, space, pos):
    circleBody = pymunk.Body(80, 500, body_type=pymunk.Body.DYNAMIC)
    circleBody.position = pos
    circleShape = pymunk.Circle(circleBody, 15)
    joint = pymunk.PinJoint(circle1, circleBody)
    space.add(circleBody, circleShape, joint)

def DrawText(text, x, y, screen):
    font = pygame.font.SysFont("Arial", 24)
    img = font.render(text, True, (10, 10, 10))
    screen.blit(img, (x, y))

def TextAndSliders(screen):
    DrawText("Mass of first ball", 650, 20, screen)
    slider = Slider(screen, 500, 50, 100, 20, min=0, max=100, step=1)
    slider.draw()


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Double pendulum")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 500)

    initialize(space, screen)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    pause = True
    circleCount = 0

    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                space = pymunk.Space()
                space.gravity = (0.0, 500)
                initialize(space)
                circleCount = 0
                pause = True               
            elif circleCount == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                secondBall(space.bodies[1], space, mousePos)
                circleCount = -1
                pause = False
            elif circleCount == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                firstBall(space.bodies[0], space, mousePos)
                circleCount += 1

        screen.fill((255,255,255))
        if not pause:
            space.step(1/30)  
        TextAndSliders(screen)
        space.debug_draw(draw_options)
        clock.tick(50)   
        pygame.display.flip()       

if __name__ == '__main__':
    main()