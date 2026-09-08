import math
import numpy as np
import os
import sys
import MiscMath1
from MiscMath1 import *

class Challenge6Particles:
    def __init__(self, velocity, launchAngle, gravity,point,launchHeight=0,numberOfPoints=10,GUI=None):
        self.launchHeight = launchHeight
        self.inputAngle = math.radians(launchAngle)
        self.pointX = point[0]
        self.pointY = point[1]
        self.velocity = velocity
        self.gravity = gravity
        self.pointCount = numberOfPoints
        self.displayMessages = []
        self.graphLimitX = 105
        self.graphLimitY = 105   
        self.xLabel = "Displacement X: x (m)"
        self.yLabel = "Displacement Y: y (m)"
        self.realPoint = False
        self.previousRealPoint = False
        self.pointToggle = True
        self.GUI = GUI
            ##Index Relation
        """
        1 - Input Parabola
        2 - Point Particle Parabola High 
        3 - Point Particle Parabola Low
        4 - Max Range Parabola
        5 - Bounding Parabola
        """
            ##2 and 3 Combined as they are both points particles

        self.inputParabola = ParticleData(name = "Input",v = velocity, angle = self.inputAngle, color = (1,0,0),enabled=True)
        self.highPointParabola = ParticleData(name="Max Angle", color = (0,1,0))
        self.lowPointParabola = ParticleData(name="Min Angle",color = (0,0,1))
        self.minimumVelocityParabola = ParticleData(name="Min U",color= "grey")
        self.maxRangeParabola = ParticleData(name="Max Range",color = (1,0,1))
        self.boundingParabola = ParticleData(name="Bounding Parabola", color = (0,0,0))

            ##Bounding parabola is fundamentally different, so not included
        self.parabolas = [self.inputParabola, self.highPointParabola, self.lowPointParabola, self.minimumVelocityParabola, self.maxRangeParabola]

    ##--SIMULATION RUNNING-------------------------------------------
    def simulationRefresh(self):
        for parabola in self.parabolas:
            parabola.velocity = self.velocity
        self.minimumVelocityParabola.velocity=self.minimumVelocity(self.pointX,self.pointY,-self.gravity)
        ##print(self.minimumVelocityParabola.velocity)
        self.minimumVelocityParabola.angle=self.minimumAngle(self.pointX,self.pointY,self.minimumVelocityParabola.velocity,-self.gravity)
        self.inputParabola.angle = self.inputAngle
        self.maxDisplacementX = self.getMaxDisplacementX(self.velocity,self.gravity)

        angles = self.intersectionAngles(self.pointX,self.pointY,self.velocity,self.gravity)
        self.highPointParabola.angle = angles[0]
        self.lowPointParabola.angle = angles[1]
        (f"Angles: {angles[0]},{angles[1]}")

        self.realPoint = self.pointEligible(self.pointX,self.pointY,self.velocity,self.gravity)
        if self.realPoint!=self.previousRealPoint:
            if self.realPoint:
                self.GUI.realPoint()
            else: self.GUI.nonRealPoint()
        if self.realPoint==False:
            self.highPointParabola.enabled = False
            self.lowPointParabola.enabled = False
        self.previousRealPoint=self.realPoint

        self.maxRangeParabola.angle = self.intersectionAngles(self.maxDisplacementX, 0,self.velocity,self.gravity)[0]

        ##if self.velocity<self.minVelocity: self.displayMessages.append(("\nNo real values possible for given V"))

        ##Stretch Canvas to fit whole graph
        self.graphLimitX = MiscMath1.roundUp(self.maxDisplacementX)+10
        self.graphLimitY = MiscMath1.roundUp(self.getMaxDisplacementY(self.velocity,self.gravity))+10


    ##--PLOTTING DATA--------------------------------------------------------

        ##Get points holds all of the graph data, inclduing colour, points, name and display messages
    def getPoints(self):
        graphPointList = []
        yPoints = []
        self.simulationRefresh()
        self.enabledParabolas = []
        for parabola in self.parabolas:
            parabola.apogee=self.findApogee(parabola.velocity,parabola.angle,self.launchHeight)
            if parabola.enabled: self.enabledParabolas.append(parabola)
        graphPointList = self.getPlots(self.enabledParabolas)
        if self.boundingParabola.enabled:
            boundingParabolaParameters=self.boundingParabolaPoints(self.velocity)+["Bounding Parabola",(0,0,0),"--"]
            graphPointList.append(boundingParabolaParameters)
        self.setParticleText()
        return graphPointList

        ##Get plots feeds into get points
    def getPlots(self, particles):
        self.setParticleText()
        plots=[]
        for particle in particles:
            yPoints = []
            xPoints = self.xPointSpacing(particle.velocity,particle.angle)
            for point in xPoints:
                yPoints.append(self.yFromX(point,particle.velocity,particle.angle))
            particle.xPoints = xPoints
            particle.yPoints = yPoints
            particle.xIntersect = self.getMaxPlotDisplacementX(particle.velocity,particle.angle)
            particle.distanceTravelled = self.distanceTravelled(particle.velocity, -self.gravity, particle.angle, particle.xIntersect)

            #(f"Integral: {self.distanceTravelled(particle.velocity, -self.gravity, particle.angle, particle.xIntersect)}")
            #(f"Summation: {self.distanceTravelledSummation(particle.velocity, self.gravity, particle.angle, particle.xPoints)}")

            plots.append((xPoints,yPoints,particle.name,particle.color,"o-"))
        return plots

    def getDots(self):
        dots = []
        if self.pointToggle:
            dots.append([self.pointX,self.pointY,"black"])
        for parabola in self.enabledParabolas:
            apogee = self.findApogee(parabola.velocity,parabola.angle,self.launchHeight)
            dots.append(apogee+["red"])
            
        return dots

    def boundingParabolaPoints(self,velocity):
        xPoints=[0,0]
        max = self.getMaxDisplacementX(velocity,self.gravity)
        for point in range(self.pointCount-2):
             xPoints.append((max/self.pointCount)*point)
        xPoints.append(max)
        yPoints = []
        for point in xPoints:
            yPoints.append(self.boundingParabolaYFromX(velocity,point))
        return [xPoints,yPoints]

    ##--LABELS--------------------------------------------
    def setParticleText(self):
        ##Write all text as a tuple, each value corresponding to a parabola attribute
        self.inputParabola.text = (f"Input Velocity (ms⁻¹): {MiscMath1.sf(self.velocity)}",
                                f"Input θ (°): {MiscMath1.sf(math.degrees(self.inputAngle))}",
                                f"Distance Travelled (m) : {MiscMath1.sf(self.inputParabola.distanceTravelled)}",
                                f"Apogee: ({MiscMath1.sf(self.inputParabola.apogee[0])},{MiscMath1.sf(self.inputParabola.apogee[1])})")

        self.highPointParabola.text = (f"θ (°): {MiscMath1.sf(math.degrees(self.highPointParabola.angle))}",
                                       f"Distance Travelled (m): {MiscMath1.sf(self.highPointParabola.distanceTravelled)}",
                                       f"Apogee: ({MiscMath1.sf(self.highPointParabola.apogee[0])},{MiscMath1.sf(self.highPointParabola.apogee[1])})")
                                        

        self.lowPointParabola.text = (f"θ (°): {MiscMath1.sf(math.degrees(self.lowPointParabola.angle))}°",
                                      f"Distance Travelled (m): {MiscMath1.sf(self.lowPointParabola.distanceTravelled)}",
                                      f"Apogee: ({MiscMath1.sf(self.lowPointParabola.apogee[0])},{MiscMath1.sf(self.lowPointParabola.apogee[1])})")
        
        self.minimumVelocityParabola.text = (f"Velocity (ms⁻¹): {MiscMath1.sf(self.minimumVelocityParabola.velocity)}",
                                            f"Angle (°): {MiscMath1.sf(math.degrees(self.minimumVelocityParabola.angle))}",
                                            f"Distance Travelled (m): {MiscMath1.sf(self.minimumVelocityParabola.distanceTravelled)}",
                                            f"Apogee: ({MiscMath1.sf(self.minimumVelocityParabola.apogee[0])},{MiscMath1.sf(self.minimumVelocityParabola.apogee[1])})")

        self.maxRangeParabola.text = (f"Max Displacement X (m): {MiscMath1.sf(self.maxDisplacementX)}",
                                ##f"Max Displacement Y: {MiscMath1.sf(self.getMaxDisplacementY(self.velocity,self.gravity))}m",
                                f"Max θ (°): {MiscMath1.sf(math.degrees(self.maxRangeParabola.angle))}",
                                f"Distance Travelled (m): {MiscMath1.sf(self.maxRangeParabola.distanceTravelled)}",
                                f"Apogee: ({MiscMath1.sf(self.maxRangeParabola.apogee[0])},{MiscMath1.sf(self.maxRangeParabola.apogee[1])})")

        self.boundingParabola.text = (f"X Intersection (m): {MiscMath1.sf(self.maxDisplacementX)}",
                                      f"Y Intersection (m): {MiscMath1.sf(self.getMaxDisplacementY(self.velocity,self.gravity))}")

    #--GET MIN AND MAXIMUM VALUES-----------------------------------
    def minimumAngle(self, x ,y, minU,g):
        a = (-g*(x**2))/(2*(minU**2))
        b = x
        c = a-y
        coeffs = [a,b,c]
        roots = np.roots(coeffs)
        ##Due to rounding error, we get two values which are diffeerent but incredibly close. Since they are so close, we just take the first one
        return math.atan(roots[0])
        
        ##Minimum velocity
    def minimumVelocity(self, x,y,g):
        #(f"Theta: {theta}")
        Y=y-self.launchHeight
        u=(g**0.5)*((Y+((x**2+Y**2)**0.5))**0.5)
        return u

    def findApogee(self,v,angle,h=0):
        x=(((v)**2)/(-self.gravity))*(math.sin(angle)*math.cos(angle))
        y=h+((((v)**2)/(2*-self.gravity))*(math.sin(angle))**2)
        return [x,y]

        ##For indiviudal plots
    def getMaxPlotDisplacementX(self,velocity,angle):
        a = (self.gravity*(1+(math.tan(angle)**2)))/(2*(velocity**2))
        b = math.tan(angle)
        c = self.launchHeight
        coeff = [a,b,c]
        roots = np.roots(coeff)
        for root in roots:
            if root>0: return root

        ##For total model given v
    def getMaxDisplacementX(self,velocity,g):
        a = (velocity**2)/(-g)
        if  velocity>0: b = (2*-g*self.launchHeight)/(velocity**2)
        else: b=0
        c = (1+b)**0.5
        return a*c

    def getMaxDisplacementY(self,velocity,g): return (velocity**2)/(2*-g)+self.launchHeight
        
    ##--POINT SPACING---------------------------------------

        ##Used for Y displacement X displacement
    def xPointSpacing(self,velocity,angle):
        xPoints=[0]
        maxValue = self.getMaxPlotDisplacementX(velocity,angle)
        ##print(maxValue)
        for point in range(self.pointCount+1):
            try:
                xPoints.append((maxValue/self.pointCount)*point)
            except: pass
        xPoints.append(maxValue)
        return xPoints

    ##--FUNCTIONS FOR FINDING Y POINTS-------------------------------------
        ##y(x) for displacement
    def yFromX(self, x, v, angle):
        g = self.gravity
        xVel = v*math.cos(angle)
        xtan = math.tan(angle)*x
        gX = g*(x**2)
        xV = 2*(xVel**2)
        return xtan+((gX)/(xV))+self.launchHeight

    def boundingParabolaYFromX(self,velocity,x):
        a = (velocity**2)/(2*-self.gravity)
        b = ((-self.gravity*(x**2))/(2*(velocity**2)))
        return a-b+self.launchHeight

    ##--GENERAL PARTICLE FUNCTIONS--------------------------
    def distanceTravelled(self,velocity, gravity, angle, xPoint):
        #("Xpoint: ",xPoint)
        coeffPartA = (velocity**2)/(2*gravity)
        coeffPartB = (1+(math.tan(angle)**2))
        coeff = coeffPartA/coeffPartB
        #("Coeff: ", coeff)
        upperBound = math.tan(angle)
        lowerBoundA = (gravity*xPoint)/(velocity**2)
        lowerBoundB = (1+(math.tan(angle)**2))
        lowerBound = math.tan(angle)-(lowerBoundA*lowerBoundB)
        #(f"Upper: {upperBound}\nLower: {lowerBound}")
        bounds = [upperBound,lowerBound]
        integrals=[]
        ##CB = Current Bound
        for CB in bounds:
            part1a = ((CB**2)+1)**0.5
            part1b = MiscMath1.ln(abs(part1a+(CB)))
            part2 = CB*(part1a)
            integrals.append(part1b+part2)
        #(f"Integral One: {integrals[0]}\nIntergral Two: {integrals[1]}")
        distanceTravelled = (integrals[0]-integrals[1])*coeff
        return distanceTravelled

        ##Rudimentary method of finding distance travelled, evolves to integral method
    def distanceTravelledSummation(self, velocity, gravity, angle, xPoints):
        totalDistance=0
        for i in range(len(xPoints)-1):
            currentX = xPoints[i]
            subsequentX = xPoints[i+1]
            deltaX = (currentX-subsequentX)
            currentY=self.yFromX(currentX,velocity,angle)
            subsequentY=self.yFromX(subsequentX,velocity,angle)
            deltaY = (currentY-subsequentY)
            modXY = MiscMath1.pythag(deltaX,deltaY)
            totalDistance+=modXY
        return totalDistance

        ##Given velocity, return angles, if any, that may pass through (x,y)
    def intersectionAngles(self, x, y, velocity, g):
        a = (-g*(x**2))/(2*(velocity**2))
        b = -x
        c = y - self.launchHeight+ ((-g*(x**2))/(2*(velocity**2)))

        coeff = [a,b,c]
        roots = np.roots(coeff)
        #(f"roots {roots}")
        processedRoots = []
        if roots[0]==roots[1]: roots = [roots[0]]
        for root in roots:
            currentRoot = math.atan(root)
            while currentRoot<-math.pi/2: currentRoot+=math.pi/2
            while currentRoot>(math.pi/2): currentRoot-=math.pi/2
            processedRoots.append(currentRoot)
        return processedRoots

        ##Can high and low ball reach the target (is the target within the bounding parabola)
        ##If, with a given velocity, there is no angle that can reach the point, it is ineligible
        ##Use discriminant of intersection angles function
    def pointEligible(self,x,y,v,g):
        a = (-g*(x**2))/(2*(v**2))
        bSq = x**2
        c = y-self.launchHeight+(-g*(x**2))/(2*(v**2))
        ##print(bSq-(4*a*c))
        return bSq-(4*a*c)>=0

class ParticleData:
    #Give colour as RGB Tuple
    def __init__(self,name, color, v=0,angle=0,text="", enabled=False):
        self.velocity=v
        self.angle = 0
        self.text=text
        self.name = name
        self.enabled = enabled
        self.color = color
        self.distanceTravelled = 0
        self.xPoints=None
        self.yPoints=None
        self.xIntersect=None

def sliderHandler(value, particleAttribute):
    particleAttribute=value
