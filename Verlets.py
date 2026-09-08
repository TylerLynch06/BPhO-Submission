
##T is time, h is time step
class Verlet:
    ##F = acting forces
    ##All motion variables are 2D vectors
    def getParticle(pos,v,a,h,f=[0,0],mass=1):
        deltaSquareT = h*h
        pos1=Verlet.updatePosition(pos,v,a,h,deltaSquareT)
        a1=Verlet.updateAcceleration(a,h,f,mass)
        v1=Verlet.updateVelocity(v,a,a1,h)
        return pos1,v1,a1

    def updatePosition(pos,v,a,h,dt2):
        pos1 = []
        for index in range(len(pos)):
            pos1.append(pos[index]+(v[index]*h)+(0.5*a[index]*h*h))
        return pos1
    
    ##dt2 = Change in time squared
    def updateVelocity(v,a0,a1,h ):
        v1=[]
        for index,pointVelocity in enumerate(v):
            v1.append(pointVelocity+(0.5*(a0[index]+a1[index])*h))
        return v1

    ##Apply resistive and field forces  
    def updateAcceleration(a,h,f,mass):
        return [(a[0]+(f[0]/mass)),(a[1]+(f[0]/mass))]   

class ResistanceVerlet:
    ##F = acting forces
    ##All motion variables are 2D vectors
    def getParticle(pos,v,a,h):
        deltaSquareT = h*h
        pos1=ResistanceVerlet.updatePosition(pos,v,a,h,deltaSquareT)
        v1=ResistanceVerlet.updateVelocity(v,a,h)
        return pos1,v1

    def updatePosition(pos,v,a,h,dt2):
        pos1 = []
        for index in range(len(pos)):
            pos1.append(pos[index]+(v[index]*h)+(0.5*a[index]*h*h))
        return pos1
    
    ##dt2 = Change in time squared
    def updateVelocity(v,a1,h):
        v1=[]
        for index,pointVelocity in enumerate(v):
            v1.append(pointVelocity+a1[index]*h)
        return v1