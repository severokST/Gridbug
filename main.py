#!/usr/bin/python2

import pygame, numpy, random

SX = 800
SY = 600
Res = 20
FrameRate = 30
FrameTime = 1000/FrameRate
spawnchance = 10
buglist = []

class bug(object):
  """This code is full of 'em
  Returns: Bug object
  Functions: spawn, update, crash
  Attributes: X,Y,vector"""

  def __init__(self,X,Y,vector):
    global bugcount
    self.X = X
    self.Y = Y
    self.vector = vector
    bugcount = bugcount + 1
    vchk = 10
    while (vchk>0):
      if (vchk == 1):
        self.vector = vector
        return
      self.vector = random.randint(0,3)
      if not (self.vector == vector):
        if self.vector < 2:
          if grid[self.X/Res + ((self.vector * 2) -1), self.Y/Res] == 1: 
            vchk = 0 
          elif grid[self.X/Res, self.Y/Res + (((self.vector - 2)*2)-1)] == 1:
            vchk = 0
          else:
            vchk = vchk - 1


  def __call__(self,X,Y,vector):
    return

  def update(self):
    if self.vector < 2:
      if self.X==SX - Res: self.vector = 0
      if self.X==Res: self.vector = 1
      self.X = self.X + (self.vector *2) - 1
      self.Y = self.Y - (self.Y % Res)
    else:
      if self.Y==SY - Res: self.vector = 2
      if self.Y==Res: self.vector = 3
      self.Y = self.Y + ((self.vector -2)*2) - 1
      self.X = self.X - (self.X % Res)
    pygame.draw.circle(background,(255,0,0),(self.X,self.Y),4,0)
    if not (self.X%Res) and not (self.Y%Res):
      vchk = 10
      while (vchk>0):
        if (vchk == 1):
          self.vector = 1
          return
        self.vector = random.randint(0,3)
        if self.vector < 2:
          if grid[(self.X/Res + ((self.vector * 2) -1))%(SX/Res), self.Y/Res] == 1: 
            vchk = 0 
        elif grid[self.X/Res, (self.Y/Res + (((self.vector - 2)*2)-1))%(SY/Res)] == 1:
          vchk = 0
        else:
          vchk = vchk - 1

def drawgrid():
  global buglist
  for X in range(1,SX/Res):
    for Y in range(1,SY/Res):
      if grid[X,Y]:
        pygame.draw.line(background,(255,255,255),(X*Res-Res/2,Y*Res),(X*Res+Res/2,Y*Res),1)
	pygame.draw.line(background,(255,255,255),(X*Res,Y*Res-Res/2),(X*Res,Y*Res+Res/2),1)
        pygame.draw.circle(background,(255,255,255),(X*Res,Y*Res),2,0)

bugcount = 0
grid = numpy.ones(shape=(SX/Res,SY/Res))
for a in range(1,SX/Res):
  grid[a,1] = 0
  grid[a,SY/Res-1] = 0
for a in range(1,SY/Res):
  grid[1,a] = 0
  grid[SX/Res-1,a] = 0

pygame.init()
screen = pygame.display.set_mode((SX, SY))
background = pygame.Surface(screen.get_size())
buglist.append(bug(SX/2,SY/2,0))


done = False

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True

  background.fill((0,0,0))
  drawgrid() 
  for cbug in buglist:
    cbug.update()
    for obug in buglist:
      if not (cbug==obug):
        if (cbug.X == obug.X) and (cbug.Y == obug.Y):
          grid[cbug.X/Res,cbug.Y/Res]=0
          buglist.remove(cbug)
          buglist.remove(obug)
          bugcount = bugcount -2

    if not (random.randint(0,spawnchance*bugcount)):
      buglist.append(bug(cbug.X,cbug.Y,cbug.vector))
  screen.blit(background, (0,0))       
  pygame.display.flip()
