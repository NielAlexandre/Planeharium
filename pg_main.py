#!/usr/bin/python3
# -*- coding: utf-8 -*-

from math import *
from itertools import cycle

import pygame as pg
import pygame.locals as pgl

pg.init()

class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY1 = (50, 50, 50)

class Sphere:
    def __init__(self, x, y, z, r):
        self.set_pos(x, y, z)
        self.r = r

    def set_pos(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def xy_projection(self, surf):
        x, y = surf.get_rect().center
        x += self.x
        y -= self.y
        maxz = 20
        z = 0.5 + (maxz+self.z)/(maxz*2)
        pg.draw.circle(surf, Colors.WHITE, (x, y), z*self.r)

def going_round(nb_pts, center, radius, offset=0, clockwise=True, xj=0, yj=0):
    """ Generator of points equaly distributed in a circle
    Radius can be send a each iteration
    nb_pts : integer number of points which will be yielded
    center : tuple of 2 integers center of the circle
    radius : distance between the points and the center
    inclination : of the orbital plane to the referencial
    offset : angle offset of the first point
        0 : first point east
        pi/2 : first point north
        pi : first point west
        3*pi/2 : first point south
    """
    for i in range(nb_pts):
        i *= [-1, 1][clockwise]
        i *= 2*pi/nb_pts+offset
        r = (int(radius * cos(i) * cos(xj) + center[0]),
                int(radius * sin(i) * cos(yj) + center[1]),
                int(radius * sin(i) * sin(yj) + center[2])
             )
        nradius = (yield r)
        radius = radius if nradius is None else nradius

def reset_surf(surf):
    surf.fill((25, 10, 35))
    #Drawing guidlines
    rect = surf.get_rect()
    pg.draw.circle(surf, Colors.GREY1, rect.center, 5)
    pg.draw.line(surf, Colors.GREY1,
                 (0, rect.height/2), (rect.width, rect.height/2))
    pg.draw.line(surf, Colors.GREY1,
                 (rect.width/2, 0), (rect.width/2, rect.height))

def main():

    display = pg.display.set_mode((800, 500))
    clock = pg.time.Clock()


    sphere = Sphere(100, 100, 100, 15)

    itgr = cycle(going_round(360, (0, 0, 0), 150, xj=45, yj=25))

    loop = True
    while loop:
        for e in pg.event.get():
            if e.type == pgl.QUIT:
                loop = False

        sphere.set_pos(*next(itgr))

        if sphere.z > 0:
            reset_surf(display)
            sphere.xy_projection(display)
        else:
            sphere.xy_projection(display)
            reset_surf(display)
        pg.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
