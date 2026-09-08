import sys 
import os
##sys.path.append(os.path.abspath("C:\\...\\Task1"))
# sys.path.append(os.path.abspath("C:\\...\\Task2to6"))
# sys.path.append(os.path.abspath("C:\\...\\Task7"))
# sys.path.append(os.path.abspath("C:\\...\\Task8"))
# sys.path.append(os.path.abspath("C:\\...\\Task9"))
# sys.path.append(os.path.abspath("C:\\...\\ExTask1"))
# sys.path.append(os.path.abspath("C:\\...\\GUI"))
# sys.path.append(os.path.abspath("C:\\...\\Globals"))
import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation 
import math
import time
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation

from Task1 import *
from Task2to6 import *
from Task7 import *
from Task8 import *
from Task9 import *
from ExTask1 import *
from GUI import *

class matPlotter:
    def __init__(self,fig,ax):
        print("Program Started")
        self.fig = fig
        self.ax = ax
        self.xpoints = []
        self.ypoints = []
        ##LArge interval means that sliders are smooth, but graph is late to update
        ##Small interval means sliders arent smooth, graph is also slow to update
        self.anim = animation.FuncAnimation(self.fig,self.update,interval=100,cache_frame_data=False)
        self.renderer = self.fig.canvas.get_renderer()
        self.GUI = None

    def load(self,velocity,launchAngle, point,launchHeight):
        self.models = [Challenge6Particles(velocity,launchAngle,-9.81, point,numberOfPoints= 500, launchHeight = launchHeight,GUI=self.GUI),
                Challenge7Particles(velocity,launchAngle,-9.81,numberOfPoints= 500, launchHeight = launchHeight),
                Challenge8Particles(velocity,launchAngle,-9.81,numberOfPoints=500,launchHeight=launchHeight,GUI=self.GUI),
                ExChallenge1Particles(velocity,launchAngle,-9.81,numberOfPoints=500,launchHeight=launchHeight),
                BasicParticle(velocity,launchAngle,-9.81,launchHeight=launchHeight,t=1)]
        self.particle = self.models[0]
        self.modelID=0
        ##self.particle = Challenge6Particles(velocity,launchAngle,-9.81, point,numberOfPoints= 20, launchHeight = launchHeight)
        ##self.particle = HorizontalParticles(velocity,launchAngle,-9.81,numberOfPoints= 50, launchHeight = launchHeight)
        ##self.particle = IntersectionParticles(velocity,-9.81, point,numberOfPoints= 50)
        ##self.particles = [AnalyticParticle(launchAngle, velocity, -9.81,launchHeight = 0,numberOfPoints=20),BasicParticle(launchAngle, velocity, -9.81,launchHeight = 0,t=0.05)]
                          
        self.airResistance = False
        self.airResistanceParticle = None
        
        self.paused=False

        self.animating=False
        self.frame = 0
        ##self.textAlert is additional text added to the boxPlot
        self.alertText=""
        self.animationInProcess=False
        self.animationComplete=False
        self.displayXPoints=[[],[],[],[],[]]
        self.displayYPoints=[[],[],[],[],[]]
        self.animationPointsTravelled=0
        ##self.PPF: Points per frame. for every frame, how many X points are travelled
        self.PPF=70
        self.idleFrames=0


    def update(self, frame):
        ##self.GUI.updateText()
        #print("Update")
        if self.idleFrames<=0:   
            if self.GUI.inputVariableProcessing():
                self.particle.velocity=float(self.GUI.velocityInput.get())
                self.particle.inputAngle=math.radians(float(self.GUI.angleInput.get()))
                ##print(self.particle.inputAngle)
                self.particle.launchHeight=float(self.GUI.heightInput.get())
            try:
                if self.GUI.pointXEntry.get()=="" or self.GUI.pointYEntry.get()=="":
                    self.particle.pointX=50
                    self.particle.pointY=30
                else:
                    if self.GUI.pointXEntry.get()==0 or self.GUI.pointYEntry.get()==0:
                        self.particle.pointX=0.0000001
                        self.particle.pointY=0.0000001
                        self.GUI.pointZero()
                    else:
                        self.particle.pointX=float(self.GUI.pointXEntry.get())
                        self.particle.pointY=float(self.GUI.pointYEntry.get())
                    
                        
            except: pass
            try: self.PPF=int(self.GUI.PPFInput.get())
            except: pass

            p = self.particle
            if self.airResistance: self.airResistanceParticle = Challenge9Particles(p.velocity,
                                                                                    math.degrees(p.inputAngle),
                                                                                    -9.81,
                                                                                    launchHeight=p.launchHeight)
            if not self.animating:
                self.drawGraph()
            if self.animating:
                ##load animation once
                if not self.animationInProcess:
                    self.loadAnimation()
                    self.animationInProcess=True
                ##Update animation until complete
                self.animateGraph()
        else: self.idleFrames-=1

    def drawGraph(self):
        self.setOfPlots = self.setPoints()
        self.ax.clear()
        ##Y 0 displacement line
        self.ax.axhline(y=0.0, color='r', linestyle='-')
        for plot in self.setOfPlots:
            self.xpoints = plot[0]
            self.ypoints = plot[1]
            self.ax.plot(self.xpoints,self.ypoints,plot[4],ms=1,label=plot[2],color=(plot[3]))
        self.plotDots()

        plt.xlim(0, 500)#self.particle.graphLimitX)
        plt.ylim(0, 4000)#self.particle.graphLimitY)
        self.commonGraph()

    def loadAnimation(self):
        self.frame=0
        self.animationPointsTravelled=0
        self.displayXPoints=[[],[],[],[],[],[]]
        self.displayYPoints=[[],[],[],[],[],[]]
        self.setOfPlots = self.setPoints()
        self.completedAnimations = [0 for x in range(len(self.setOfPlots))]

    def animateGraph(self): 
        self.ax.clear()
        if not self.animationComplete:
            self.alertText=f"Points Per Frame (PPF): {self.PPF}\nZ: Increase PPF\nX: Decrease PPF\n\nPoints Travelled: {self.animationPointsTravelled}"
            for i in range(self.PPF):
                for index,plot in enumerate(self.setOfPlots):
                    try:
                        self.displayXPoints[index].append(plot[0][self.frame])
                        self.displayYPoints[index].append(plot[1][self.frame]) 
                    except IndexError:
                        self.completedAnimations[index]=1
                    pass
                self.frame+=1
            ##print(f"{sum(self.completedAnimations)}/{len(self.setOfPlots)}")
            if sum(self.completedAnimations) >= len(self.setOfPlots):
                self.animationComplete=True         
            ##Plot front of animation
            self.plotBall()
        else: self.animationCompleteAlert()
        for index,plot in enumerate(self.setOfPlots):
            self.ax.plot(self.displayXPoints[index],self.displayYPoints[index],"o-",ms=1,label=plot[2],color=(plot[3]))

        ##self.plotBox()
        self.plotDots()

        ##Y 0 displacement line
        self.ax.axhline(y=0.0, color='r', linestyle='-')

        self.commonGraph()

    ##Lines used in both animate and draw graph
    def commonGraph(self):
        plt.legend(loc='upper right')
        plt.rcParams["figure.autolayout"] = True
        plt.grid(True)
        plt.xlabel(self.particle.xLabel)
        plt.ylabel(self.particle.yLabel)
        ##self.toolbar.setStyleSheet("background-color:Gray;")
        self.fig.set_facecolor("white")
        self.ax.set_facecolor("whitesmoke")
        self.animationPointsTravelled+=self.PPF
        self.fig.canvas.draw()

    def setPoints(self):
        allPoints = self.particle.getPoints()
        if self.airResistance:
            allPoints.append(self.airResistanceParticle.getPoints())
            self.setOfPlots.append(self.airResistanceParticle)
        return allPoints

    def set3DPoints(self):
        allPoints = self.particle.getPoints()
        return allPoints

    ##Plot distinct thick dots that would otherwise not be well represented by a graph, such as the apogee, or maxima and minima
    def plotDots(self):
        dots = self.particle.getDots()
        if self.animating==False:
            for dot in dots:
                if dot!=None:
                    self.ax.plot(dot[0],dot[1],"ro",alpha=0.6,markersize=5,color=dot[2])

    ##Plot ball only used for challenge 8 animation
    def plotBall(self):
        for i,plot in enumerate(self.setOfPlots):
            self.ax.plot(self.displayXPoints[i][-1],self.displayYPoints[i][-1],'ro',alpha=0.4,markersize=7)

    def beginAnimation(self):
        self.animating=True

    def resetAnimation(self):
        self.loadAnimation()
        self.animationComplete=False
        self.animationInProcess=False

    def loadNewModel(self,modelIndex):
        if self.animating==True: 
            self.exitAnimation()
        self.particle=self.models[modelIndex]
        self.setOfPlots = self.setPoints()
        self.modelID=modelIndex

    def exitAnimation(self):
        self.animating=False
        self.animationComplete=False
        self.animationInProcess=False

    def retreivekeyInputs(self, event):
        ##self.particle.keyInputs(event)
        if event.key=="escape": window.destroy()
        if event.key=="p": self.togglePause()
        if event.key=="o": 
            writervideo = animation.FFMpegWriter(fps=60) 
            self.anim.save(r"C:\\Users\\Tyler\\OneDrive - Lincoln Minster School\\Senior school\\Bpho Computational Challenge\\Graph Results\\Animations\\graph.mp4", writer=writervideo) 

    def togglePause(self):
        self.paused= not self.paused
        if self.paused: self.anim.pause()
        else: self.anim.resume()

    def animationCompleteAlert(self):
        self.alertText=(f"Points Per Frame (PPF): {self.PPF}\nZ: Increase PPF\nX: Decrease PPF\n\nAnimation Complete\nPress I to restart Animation\nPress O to view graph\nPress P to save video")

    ##Often called to avoid intense canvas flickering
    def idle(self,frames=10):
        self.idleFrames=frames