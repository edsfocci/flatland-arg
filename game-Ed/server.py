# Images imported
p_arrow = "800px-Arrow_east.svg.png"
p_spring = "resources0001.png"
p_uZone = "Mario-Mushroom1UP.png"
p_dZone = "120px-PoisonMushroom.png"

#Pygame initialization
import pygame, random
from pygame.locals import *
from math import *
pygame.init()

# Display settings
screen_width, screen_height = 1212, 746
screen = pygame.display.set_mode((screen_width, screen_height))

# Center coordinates and facing direction of player
p_x, p_y, theta = 100., 400., 0.
ds, dtheta = 0, 0.  # This only needed for keyboard control
u_size = 25     # Size of player icon

# Make arrow image usable & rescale
arrow = pygame.image.load(p_arrow).convert_alpha()
arrow = pygame.transform.scale(arrow, (20, 20))

circle = False

spring = pygame.image.load(p_spring).convert_alpha()
spring = pygame.transform.scale(spring, (100, 100))
s_x, s_y, s_countdown = 0, 0, 0

u_zone = pygame.image.load(p_uZone).convert_alpha()
u_zone = pygame.transform.scale(u_zone, (50, 50))
u_x, u_y = screen_width - 100, 100

d_zone = pygame.image.load(p_dZone).convert_alpha()
d_zone = pygame.transform.scale(d_zone, (50, 50))
d_x, d_y = screen_width - 100, screen_height - 100

# TODO: Need to implement for various reasons
clock = pygame.time.Clock()
time = 0

running = True

while running:
    screen.fill((34, 139, 34)) # Color the playing field forest green
#    clock.tick(30)  # Keep game at 30 frames per second maximum
#    time += clock.tick()

#    if time >= 5000:    # Debug: get frames per second
#        time = 0
#        print clock.get_fps()
    
    for event in pygame.event.get():
        if event.type == QUIT:      # Detect close program
            running = False
        if event.type == KEYDOWN:   # Detect key-press
            if event.key == K_UP:
                ds = +2
            elif event.key == K_DOWN:
                ds = -2
            elif event.key == K_LEFT:
                dtheta = -.04
            elif event.key == K_RIGHT:
                dtheta = +.04
            elif event.key == K_SPACE:
                circle = True
        if event.type == KEYUP:     # Detect key-unpress
            if event.key == K_UP:
                ds = 0
            elif event.key == K_DOWN:
                ds = 0
            elif event.key == K_LEFT:
                dtheta = 0.
            elif event.key == K_RIGHT:
                dtheta = 0.
            elif event.key == K_SPACE:
                circle = False

    # Change player origin and facing direction
    theta += dtheta
    p_x += ds * cos(theta)
    p_y += ds * sin(theta)

    # Make sure player doesn't get out of bounds
    if p_x < 0:
        p_x = 0
    elif p_x > screen_width:
        p_x = screen_width
    if p_y < 0:
        p_y = 0
    elif p_y > screen_height:
        p_y = screen_height

    # Calculations to properly rotate & move player icon
    pointsTriangle = [(int(round(p_x+u_size*cos(theta))),int(round(p_y+u_size*sin(theta)))),
                      (int(round(p_x+u_size*cos(theta+2./3*pi))),int(round(p_y+u_size*sin(theta+2./3*pi)))),
                      (int(round(p_x+u_size*cos(theta+4./3*pi))),int(round(p_y+u_size*sin(theta+4./3*pi))))]

    pygame.draw.polygon(screen, (255, 0, 0), pointsTriangle)
    n_arrow = pygame.transform.rotate(arrow, -theta*180./pi)
    screen.blit(n_arrow, (p_x-n_arrow.get_width()/2, p_y-n_arrow.get_height()/2))

    # Spring with random location, and moves at random times
    s_countdown -= clock.tick()
    if s_countdown <=0:
        s_countdown = int(5000.*random.random()) + 5000
        s_x = random.randint(5, screen_width - 5)
        s_y = random.randint(5, screen_height - 5)
    screen.blit(spring, (s_x-spring.get_width()/2, s_y-spring.get_height()/2))

    screen.blit(u_zone, (u_x-u_zone.get_width()/2, u_y-u_zone.get_height()/2))
    screen.blit(d_zone, (d_x-d_zone.get_width()/2, d_y-d_zone.get_height()/2))

    if circle == True:
        pygame.draw.circle(screen, (0, 255, 255), (int(p_x), int(p_y)), 50, 1)
        pygame.draw.circle(screen, (218, 112, 214), (s_x, s_y), 75, 1)

    pygame.draw.circle(screen, (0, 255, 0), (u_x, u_y), 50, 1)
    pygame.draw.circle(screen, (218, 112, 214), (d_x, d_y), 50, 1)

    pygame.display.flip()   # Updates the screen

pygame.quit()   # When running == False, ends program
