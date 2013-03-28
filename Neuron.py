import math as m
import random as r
import imp

import Vector
imp.reload(Vector)
from Vector import Vector

import DendriteTip
imp.reload(DendriteTip)
from DendriteTip import DendriteTip

class Neuron:
    def __init__(self, position, micronsPerUnit):
        self.growing    = True
        self.center     = position
        self.vertices   = []
        self.faces      = []

        self.micronsPerUnit     = micronsPerUnit
        self.somaSize           = 10.0/micronsPerUnit
        self.maxRadius          = 500.0/micronsPerUnit
        self.currentRadius      = 0.0
        self.farthestVertex     = self.center

        self.dendrites  = []
        self.branchSplitProbability = 0.0
        self.branches               = 10
        self.dendriteThickness      = 5.0/micronsPerUnit
        self.minDendriteThickness   = 0.5/micronsPerUnit
        self.stepSize               = 50.0/micronsPerUnit
        self.headingRange           = 45
        
        self.clockwiseOrder = False
        
        self.createSoma()
        self.createDendrites()


    def createSoma(self):
        samples = 30.0
        angle   = 360.0/samples
        # Add center vertex
        self.vertices.append(self.center.toList())

        # Add a ring of vertices
        a = 0.0
        while a<360.0:
            x = m.cos(m.radians(a)) * self.somaSize + self.center.x
            y = m.sin(m.radians(a)) * self.somaSize + self.center.y
            self.vertices.append([x,y,0.0])
            a += angle

        # Build the faces (triangles fanning out from the center)
        i = 1
        while i < samples:
            if self.clockwiseOrder:     self.faces.append([i, 0, i+1])
            else:                       self.faces.append([i+1, 0, i])
            i += 1
        if self.clockwiseOrder: self.faces.append([i, 0, 1])
        else:                   self.faces.append([1, 0, i])


    def createDendrites(self):
        angle           = 360.0/self.branches
        startDist       = 0.95 * self.somaSize
        
        heading = 0.0
        while heading<360.0:
            
            resources = self.maxRadius
            maxResources = self.maxRadius
            
            pos     = Vector()
            pos.x   = m.cos(m.radians(heading)) * startDist + self.center.x
            pos.y   = m.sin(m.radians(heading)) * startDist + self.center.y

            dendrite = DendriteTip(heading, self.headingRange, self.stepSize,
                                   resources, maxResources, self.dendriteThickness,
                                   self.minDendriteThickness, pos, self.center, self)

            self.dendrites.append(dendrite)

            heading += angle 



    def branchDendrites(self):
        dendriteIndex   = 0
        numberDendrites = len(self.dendrites)
        
        while dendriteIndex < numberDendrites:
            dendrite = self.dendrites[dendriteIndex]
            rand = r.uniform(0.0, 1.0)
            if (dendrite.isGrowing()) and (rand < self.branchSplitProbability):
                newChildren = dendrite.split()
                self.dendrites = self.dendrites + newChildren
            dendriteIndex += 1


    def growDendrites(self):
        finishedGrowing = True
        for dendrite in self.dendrites:
            dendrite.grow()
            if dendrite.isGrowing(): finishedGrowing = False

        if finishedGrowing: self.growing = False

    def buildNeuronMesh(self):
        for dendrite in self.dendrites:
            existingVertices    = len(self.vertices)
            
            # Each quad is built from 4 vertices sequential vertices
            # Quads made in sequence from [v1, v2, v3, v4, v5, v6, ...]:
            #   v1, v2, v3, v4
            #   v3, v4, v5, v6
            # ...
            numberDendriteVertices = len(dendrite.vertices)
            v1 = dendrite.vertices[0]
            v4 = dendrite.vertices[1]
            self.vertices = self.vertices + [v1.toList()] + [v4.toList()]
            
            for i in range(0, numberDendriteVertices-3, 2):
                v1          = dendrite.vertices[i]
                v1_index    = existingVertices+i
                
                v4          = dendrite.vertices[i+1]
                v4_index    = existingVertices+i+1
                
                v2          = dendrite.vertices[i+2]
                v2_index    = existingVertices+i+2
                
                v3          = dendrite.vertices[i+3]
                v3_index    = existingVertices+i+3

                self.vertices = self.vertices + [v2.toList()] + [v3.toList()]
                face = self.createOrderedQuad(v1, v2, v3, v4, v1_index, v2_index, v3_index, v4_index)

                self.faces.append(face)

        
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
