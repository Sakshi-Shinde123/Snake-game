#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Admin
#
# Created:     17-10-2022
# Copyright:   (c) Admin 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import math
import random
import pygame
import random
import tkinter as tk
from tkinter import messagebox

width = 500
height = 500

cols = 25
rows = 20 #make sure it divides 500 evenly, if set to 10 it will be harder and there won't be much room for the snake to move around and the snake will be faster


class cube():
    rows = 20
    w = 500
    def __init__(self, start, dirnx=0, dirny=0, color=(255,165,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)


    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2)) #this is to still see the grid when we draw rectangle
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,71,171), circleMiddle, radius)
            pygame.draw.circle(surface, (0,71,171), circleMiddle2, radius)



class snake():
    body = []
    turns = {}

    def __init__(self, color, pos): #this is the given pos which is the starting pos of our snake
        #pos is given as coordinates on the grid ex (1,5)
        self.color = color
        self.head = cube(pos) # head of the snake is the cube at the given pos
        self.body.append(self.head)
        self.dirnx = 0 #we have a direction for x (-1/1/0)
        self.dirny = 1 #we have direction for y (-1/1/0) these both will keep track of what direction we are moving in

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny] #it stores the turn and guides tail in the direction of the head
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny] #it stores the turn and guides tail in the direction of the head
                elif keys[pygame.K_UP]:
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny] #it stores the turn and guides tail in the direction of the head
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny] #it stores the turn and guides tail in the direction of the head [:]-this make copy of the snake pos

        for i, c in enumerate(self.body): # i - gives index and c - gives cube object in self.body
            p = c.pos[:]
            if p in self.turns: #if position p is in the turns then we will move or turn
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx,c.dirny) #we are checking if we have reached the edge of the screen


    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1]))) #direction we are moving in
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True) #true draws eyes
            else:
                c.draw(surface)



def redrawWindow():
    global win
    win.fill((0,71,171))
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()
    pass



def drawGrid(w, rows, surface): # we want to fig out how big each sq in the grid is going to be(Gap between the lines)
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y +sizeBtwn

        pygame.draw.line(surface, (28,37,116), (x, 0),(x,w)) #vertical line
        pygame.draw.line(surface, (28,37,116), (0, y),(w,y)) #horizontal line



def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1,rows-1)
        y = random.randrange(1,rows-1)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
               continue #to make sure we dont put a snack on the top of a snake
        else:
               break

    return (x,y)


def main():
    global s, snack, win
    win = pygame.display.set_mode((width,height))
    s = snake((255,165,0), (10,10))
    s.addCube()
    snack = cube(randomSnack(rows,s), color=(255,255,0))
    flag = True
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(100) # we will delay the game by 100 milli sec so that the game doesn't run too fast
        clock.tick(8) #to make sure the snake does not run 8 blocks per sec, if its less then the game would run slower
        s.move()
        headPos = s.head.pos
        if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
            print("Score:", len(s.body))
            s.reset((10, 10))

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows,s), color=(255,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print("Score:", len(s.body))
                s.reset((10,10))
                break

        redrawWindow()

main()