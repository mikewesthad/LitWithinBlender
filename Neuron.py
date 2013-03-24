import math as m
import random as r
from Vector import Vector

class Neuron:
    def __init__(self, x, y, network):
        self.alive      = True
        self.center     = Vector(x, y, 0.0)
        self.network    = network
        
        self.somaSize           = 0.5
        self.maxRadius          = 10.0
        self.currentRadius      = 0.0
        self.farthestVertex     = [x, y]
        
        self.branches           = 10
        self.dendriteThickness  = 0.1
        self.dendrites          = []
        self.stepDist           = 0.5

        self.clockwiseOrder = False

        self.createSoma()
        self.createDendrites()


    def createSoma(self):
        samples = 30.0
        angle   = 360.0/samples
        verts   = []
        faces   = []

        # Add center vertex
        verts.append(self.center.toList())

        # Add a ring of vertices
        a = 0.0
        while a<360.0:
            x = m.cos(m.radians(a)) * self.somaSize + self.center.x
            y = m.sin(m.radians(a)) * self.somaSize + self.center.y
            verts.append([x,y,0.0])
            a += angle

        # Build the faces (triangles fanning out from the center)
        i = 1
        while i < samples:
            if self.clockwiseOrder: faces.append([i, 0, i+1])
            else: faces.append([i+1, 0, i])
            i += 1
        if self.clockwiseOrder: faces.append([i, 0, 1])
        else: faces.append([1, 0, i])

        self.network.register(verts, faces)


    def createDendrites(self):
        angle           = 360.0/self.branches
        startDist       = 0.95 * self.somaSize
        endDist         = startDist + self.stepDist
        halfThickness   = self.dendriteThickness/2.0

        verts = []
        faces = []
        a = 0.0
        while a<360.0:
            # Define the points that the dendrite would follow if it were a line (i.e. no thickness) 
            p1, p2 = Vector(), Vector()
            p1.x = m.cos(m.radians(a)) * startDist + self.center.x
            p1.y = m.sin(m.radians(a)) * startDist + self.center.y
            p2.x = m.cos(m.radians(a)) * endDist + self.center.x
            p2.y = m.sin(m.radians(a)) * endDist + self.center.y

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

            startVertexNumber = len(verts)
            face = self.createOrderedQuad(v1, v2, v3, v4, startVertexNumber)
            faces.append(face)
            verts = verts + [v1.toList(), v2.toList(), v3.toList(), v4.toList()]
            
            self.dendrites.append([[a,p1,v1,v4], [a,p2,v2,v3]])
            a += angle
            
        self.network.register(verts, faces)

    def growDendrites(self):
        step            = self.stepDist
        halfThickness   = self.dendriteThickness/2.0

        verts = []
        faces = []
        for i in range(len(self.dendrites)):
            dendrite = self.dendrites[i]                

            # Start at the last quad's ending point and vertices
            heading = dendrite[-1][0]
            p1      = dendrite[-1][1]
            v1      = dendrite[-1][2]
            v4      = dendrite[-1][3]

            # Generate a random heading in order to create p2
            heading += r.uniform(-45, 45)
            p2      = Vector()
            p2.x    = p1.x + m.cos(m.radians(heading)) * step
            p2.y    = p1.y + m.sin(m.radians(heading)) * step

            # Calculate the new vertices of the quad (adding thickness)
            t = p2 - p1
            leftPerp    = t.leftXYPerpendicular().normalize()
            rightPerp   = t.rightXYPerpendicular().normalize()
            v2 = leftPerp * halfThickness + p2
            v3 = rightPerp * halfThickness + p2

            startVertexNumber = len(verts)
            face = self.createOrderedQuad(v1, v2, v3, v4, startVertexNumber)
            faces.append(face)
            verts = verts + [v1.toList(), v2.toList(), v3.toList(), v4.toList()]
            
            self.dendrites[i].append([heading,p2,v2,v3])
            
        self.network.register(verts, faces)
        

    def createOrderedQuad(self, v1, v2, v3, v4, startVertexNumber):
        center = (v1+v2+v3+v4)*.25 

        v1 = v1 - center
        v2 = v2 - center
        v3 = v3 - center
        v4 = v4 - center

        a1 = m.atan2(v1.y, v1.x) + m.pi
        a2 = m.atan2(v2.y, v2.x) + m.pi
        a3 = m.atan2(v3.y, v3.x) + m.pi
        a4 = m.atan2(v4.y, v4.x) + m.pi

        lst = [[startVertexNumber+0, a1],
               [startVertexNumber+1, a2],
               [startVertexNumber+2, a3],
               [startVertexNumber+3, a4]]
        
        sortedLst = sorted(lst, key=lambda element: element[1], reverse=self.clockwiseOrder)
        face = [sortedLst[0][0],
                sortedLst[1][0],
                sortedLst[2][0],
                sortedLst[3][0]]
        
        return face
        

    def createVertexListFromVectors(self, v1, v2, v3, v4):
        return [v1.toList(), v2.toList(), v3.toList(), v4.toList()]
