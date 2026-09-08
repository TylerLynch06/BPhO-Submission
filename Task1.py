##Challenge 1 - Defined by parametric motion of t
import math
import numpy as np
import os
import sys
import MiscMath1
from MiscMath1 import *


class BasicParticle:
    def __init__(self, launchAngle, velocity, gravity, launchHeight=0, t=1):
        self.inputAngle = math.radians(launchAngle)
        self.launchHeight = launchHeight
        self.velocity = velocity    
        self.gravity=gravity
        self.interval = t
        self.time = 0
        self.simulationRefresh()
        self.xLabel = "X Displacement (m)"
        self.yLabel = "Y Displacement (m)"
        self.graphLimitX = 100
        self.graphLimitY = 100
        
    #Values that change during runtime set to default values
    def simulationRefresh(self):
        self.xDisplacement = 0
        self.yDisplacement = self.launchHeight
        self.xVel = math.cos(self.inputAngle)*self.velocity
        self.yVel = math.sin(self.inputAngle)*self.velocity
        self.time = 0
        self.frames, self.impactTime = self.calculateFrames()
        ##print(self.frames)
        self.currentFrame=0

    def simulationUpdate(self):
        self.currentFrame+=1
        self.time+=self.interval
        if self.currentFrame==self.frames: time=self.impactTime
        
    def getPoints(self): 
        self.simulationRefresh()
        xpoints=[]
        ypoints=[]
        for i in range(self.frames):
            self.xDisplacement = self.getDisplacementAxis(self.xVel,t=self.time)
            xpoints.append(self.xDisplacement)
            self.yDisplacement = self.getDisplacementAxis(self.yVel, self.time,axisAcceleration=self.gravity, originalDisplacement=self.launchHeight)
            ypoints.append(self.yDisplacement)
            self.simulationUpdate()
        xpoints.append(self.getDisplacementAxis(self.xVel, t=self.impactTime))
        ypoints.append(self.getDisplacementAxis(self.yVel, t=self.impactTime, axisAcceleration=self.gravity, originalDisplacement=self.launchHeight))
        ##(xpoints[-1],ypoints[-1])
        self.graphLimitX = MiscMath1.roundUp(xpoints[-1]+5)
        self.graphLimitY = MiscMath1.roundUp(((self.velocity**2)/(2*-self.gravity))+self.launchHeight+5)
        return [[xpoints,ypoints,"Parametric Projectile","red","o-"]]

    def getDots(self):
        return []

    def calculateFrames(self):
        coeff = [0.5*self.gravity, self.yVel, self.launchHeight]
        roots = np.roots(coeff)
        for root in roots: 
            if root>0: realRoot= root
        ##Total time/interval time, time of impact
        return (1+int(realRoot//self.interval),realRoot)

    def getDisplacementAxis(self, axisVelocity, t, axisAcceleration=0, originalDisplacement=0):
        ##Use suvat equations
        displacement = (0.5*axisAcceleration*(t**2))+(axisVelocity*t)+originalDisplacement
        return displacement
