import math as m
import random as r
import imp

import Vector
imp.reload(Vector)
from Vector import Vector

class Neuron:
    def __init__(self, position, micronsPerUnit):
        self.growing    = True
        self.center     = position
        self.verts      = []
        self.faces      = []

        self.micronsPerUnit     = micronsPerUnit
        self.somaSize           = 10.0/micronsPerUnit
        self.maxRadius          = 600.0/micronsPerUnit
        self.currentRadius      = 0.0
        self.farthestVertex     = self.center

        self.branchSplitProbability = 0.0
        self.branches               = 30
        self.dendriteThickness      = 30.0/micronsPerUnit
        self.minDendriteThickness   = 10.0/micronsPerUnit
        self.dendrites              = []
        self.stepDist               = 10.0/micronsPerUnit
        self.headingRange           = 15

        self.lineSegments = []
        
        self.clockwiseOrder = False
        
        self.createSoma()
        self.createDendrites()


    def createSoma(self):
        samples = 30.0
        angle   = 360.0/samples
        # Add center vertex
        self.verts.append(self.center.toList())

        # Add a ring of vertices
        a = 0.0
        while a<360.0:
            x = m.cos(m.radians(a)) * self.somaSize + self.center.x
            y = m.sin(m.radians(a)) * self.somaSize + self.center.y
            self.verts.append([x,y,0.0])
            a += angle

        # Build the faces (triangles fanning out from the center)
        i = 1
        while i < samples:
            if self.clockwiseOrder:
                self.faces.append([i, 0, i+1])
            else:
                self.faces.append([i+1, 0, i])
            i += 1
        if self.clockwiseOrder:
            self.faces.append([i, 0, 1])
        else:
            self.faces.append([1, 0, i])



    def createDendrites(self):
        angle           = 360.0/self.branches
        startDist       = 0.95 * self.somaSize
        endDist         = startDist + self.stepDist
        halfThickness   = self.dendriteThickness/2.0
        
        a = 0.0
        while a<360.0:
            
            # Define the points that the dendrite would follow if it were a line (i.e. no thickness)
            initialResources = self.maxRadius 
            p1, p2 = Vector(), Vector()
            p1.x = m.cos(m.radians(a)) * startDist + self.center.x
            p1.y = m.sin(m.radians(a)) * startDist + self.center.y
            p2.x = m.cos(m.radians(a)) * endDist + self.center.x
            p2.y = m.sin(m.radians(a)) * endDist + self.center.y
            remainingResources = initialResources - p1.distance(p2)

            # Find the first and last vertex of the quad (moving perpendicular from p1 to create thickness)
            t = p1 - self.center
            leftPerp    = t.leftXYPerpendicular().normalize()
            rightPerp   = t.rightXYPerpendicular().normalize()
            v1 = leftPerp * halfThickness + p1
            v4 = rightPerp * halfThickness + p1

            # Find the second and third vertex of the quad (moving perpendicular from p2 to create thickness)
            t = p2 - p1
            leftPerp    = t.leftXYPerpendicular().normalize()
            rightPerp   = t.rightXYPerpendicular().normalize()
            v2 = leftPerp * halfThickness + p2
            v3 = rightPerp * halfThickness + p2

            # Find the vertex index of the newly added vertices
            startVertexNumber = len(self.verts)
            v1Number = startVertexNumber
            v2Number = startVertexNumber + 1
            v3Number = startVertexNumber + 2
            v4Number = startVertexNumber + 3

            # Add the vertices
            self.verts = self.verts + [v1.toList(), v2.toList(), v3.toList(), v4.toList()]

            # Add a properly ordered face
            face = self.createOrderedQuad(v1, v2, v3, v4, v1Number, v2Number, v3Number, v4Number)
            self.faces.append(face)

            # Store some information about the current dendrite branch
            self.dendrites.append([[a,initialResources,p1,[v1,v1Number],[v4,v4Number]],
                                   [a,remainingResources,p2,[v2,v2Number],[v3,v3Number]]])
            self.lineSegments.append([p1, (p1+p2)/2.0, p2])
            self.updateRadius(v1, v2, v3, v4)
            a += angle


    def branchDendrites(self):
        i = 0
        numDendrites = len(self.dendrites)
        while i < numDendrites:
            if r.uniform(0.0, 1.0) < self.branchSplitProbability:
                dendrite        = self.dendrites[i]
                heading         = dendrite[-1][0]
                resources       = dendrite[-1][1]
                p1              = dendrite[-1][2]
                v1, v1Number    = dendrite[-1][3]
                v4, v4Number    = dendrite[-1][4]

                if resources > 4*self.stepDist:

                    del(self.dendrites[i])
                    i-=1
                    numDendrites-=1

                    self.dendrites.append([[heading+self.headingRange,resources/2.0,p1,[v1,v1Number],[v4,v4Number]]])
                    self.dendrites.append([[heading-self.headingRange,resources/2.0,p1,[v1,v1Number],[v4,v4Number]]])
                
            i+=1
                                
            
        

    def growDendrites(self):
        finishedGrowing = True
        for i in range(len(self.dendrites)):
            dendrite = self.dendrites[i]
            resources = dendrite[-1][1]
            if resources > 0:
                self.growDendrite(i)
                finishedGrowing = False
        if finishedGrowing: self.growing = False

        self.branchDendrites()


    def growDendrite(self, i):
        dendrite        = self.dendrites[i]
        step            = self.stepDist
        halfThickness   = self.dendriteThickness/2.0

        # Load this dendrite's information
        heading         = dendrite[-1][0]
        resources       = dendrite[-1][1]
        p1              = dendrite[-1][2]
        v1, v1Number    = dendrite[-1][3]
        v4, v4Number    = dendrite[-1][4]

        thickness = resources/self.maxRadius * (self.dendriteThickness - self.minDendriteThickness) + self.minDendriteThickness
        halfThickness = thickness / 2.0

        # Generate a random heading in order to create p2
        heading += r.uniform(-self.headingRange, self.headingRange)
        p2      = Vector()
        p2.x    = p1.x + m.cos(m.radians(heading)) * step
        p2.y    = p1.y + m.sin(m.radians(heading)) * step
        resources = resources - p1.distance(p2)

        # Calculate the new vertices of the quad (adding thickness)
        t = p2 - p1
        leftPerp    = t.leftXYPerpendicular().normalize()
        rightPerp   = t.rightXYPerpendicular().normalize()
        v2 = leftPerp * halfThickness + p2
        v3 = rightPerp * halfThickness + p2
        
        # Find the vertex index of the newly added vertices
        startVertexNumber = len(self.verts)
        v2Number = startVertexNumber
        v3Number = startVertexNumber + 1
        
        # Add the vertices
        self.verts = self.verts + [v2.toList(), v3.toList()]
        
        # Add a properly ordered face
        face = self.createOrderedQuad(v1, v2, v3, v4, v1Number, v2Number, v3Number, v4Number)
        self.faces.append(face)

        # Store some information about the current dendrite branch
        self.dendrites[i].append([heading, resources, p2, [v2,v2Number], [v3,v3Number]])
        self.lineSegments.append([p1, (p1+p2)/2.0, p2])
        self.updateRadius(v1, v2, v3, v4)

        
    def generateRandomHeading(position, heading, visualRange, headingRange):

        for line in self.lineSegments:
            p1, midp, p2 = line

            t = midp - position
            m.atan2(t.y, t.x) + m.pi
        
        

            
    def createOrderedQuad(self, v1, v2, v3, v4, v1Number, v2Number, v3Number, v4Number):
        center = (v1+v2+v3+v4)*.25 

        v1 = v1 - center
        v2 = v2 - center
        v3 = v3 - center
        v4 = v4 - center

        a1 = m.atan2(v1.y, v1.x) + m.pi
        a2 = m.atan2(v2.y, v2.x) + m.pi
        a3 = m.atan2(v3.y, v3.x) + m.pi
        a4 = m.atan2(v4.y, v4.x) + m.pi

        lst = [[v1Number, a1], [v2Number, a2], [v3Number, a3], [v4Number, a4]]
        
        sortedLst = sorted(lst, key=lambda element: element[1], reverse=self.clockwiseOrder)
        
        face = [sortedLst[0][0], sortedLst[1][0], sortedLst[2][0], sortedLst[3][0]]
        
        return face

    def updateRadius(self, v1, v2, v3, v4):
        for v in [v1, v2, v3, v4]:
            d = self.center.distance(v)
            if d>self.currentRadius:
                self.currentRadius = d
                self.farthestVertex = v
    
    def createVertexListFromVectors(self, v1, v2, v3, v4):
        return [v1.toList(), v2.toList(), v3.toList(), v4.toList()]
