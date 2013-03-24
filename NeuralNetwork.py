try: import bpy
except: print("Import failed - not running within blender")

import math as m
import random as r


class Network:
    def __init__(self, width, height, depth, numberCells):
        self.cells = []
        self.verts = []
        self.faces = []

        self.buildMeshCube(width, height, depth)        
        
        for i in range(numberCells):
            self.cells.append(Neuron(r.uniform(-width/2.0,width/2.0),
                                     r.uniform(-height/2.0,height/2.0),
                                     self))
            
    def update(self):
        for c in self.cells: c.growDendrites()

    def buildNetwork(self):
        self.buildMesh("Network", self.verts, self.faces)

    # newVerts and newFaces must be lists of lists
    def register(self, newVerts, newFaces):
        offset = len(self.verts)
        for f in range(len(newFaces)):
            for i in range(len(newFaces[f])): 
                newFaces[f][i] += offset
            self.faces.append(newFaces[f][:])
        self.verts = self.verts + newVerts

        
    # I don't know how exactly the normals are generated
    # I had to copy this order of verts/faces from http://blenderscripting.blogspot.com/2011/07/making-cube-using-frompydata.html
    def buildMeshCube(self, width, height, depth):  
        verts, faces = [], []
        halfw, halfh, halfd = width/2.0, height/2.0, depth/2.0
        
        verts.append([+halfw, +halfh, -halfd]) # 0  Right   Top     Back
        verts.append([+halfw, -halfh, -halfd]) # 1  Right   Bottom  Back
        verts.append([-halfw, -halfh, -halfd]) # 2  Left    Botom   Back
        verts.append([-halfw, +halfh, -halfd]) # 3  Left    Top     Back
        verts.append([+halfw, +halfh, +halfd]) # 4  Right   Top     Front
        verts.append([+halfw, -halfh, +halfd]) # 5  Right   Bottom  Front
        verts.append([-halfw, -halfh, +halfd]) # 6  Left    Bottom  Front
        verts.append([-halfw, +halfh, +halfd]) # 7  Left    Top     Front

        faces = [[0, 1, 2, 3],     # Front
                 [4, 7, 6, 5],     # Back
                 [0, 4, 5, 1],     # Left
                 [1, 5, 6, 2],     # Right
                 [2, 6, 7, 3],     # Top
                 [4, 0, 3, 7]]     # Bottom

        self.buildMesh("Light Box", verts, faces)
        
        

    def buildMesh(self, name, verts, faces):
        
        try:
            # Create empty mesh data
            mesh = bpy.data.meshes.new(name)

            # Create an object that contains that mesh
            obj = bpy.data.objects.new(name, mesh)

            # Place the object at Blender's 3D cursor location
            obj.location = bpy.context.scene.cursor_location

            # Link the object to the scene
            bpy.context.scene.objects.link(obj)
             
            # Fill the mesh with verts, edges, faces 
            mesh.from_pydata(verts,[],faces)

            # Update the mesh with the new data
            mesh.update(calc_edges=True)
            
        except: print("Mesh creation failed - not running within blender")
                            
                

    
        

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
        
##        print(v1)
##        print(v2)
##        print(v3)
##        print(v4)
##
##        # Find the angle from v1 to the points it connects to (v2 or v4) 
##        v2 = v2 - v1                        # Create vector from v1 to v2
##        v4 = v4 - v1       
##        a2 = m.atan2(v2.y, v2.x)            # atan2 goes from -pi to pi (+ is clockwise)
##        a4 = m.atan2(v4.y, v4.x)
##
##        print(m.degrees(a2))
##        print(m.degrees(a4))
##
##        # Create a counter-clockwise ordering
##        if (a2 > a4):
##            face = [startVertexNumber, startVertexNumber+1, startVertexNumber+2, startVertexNumber+3]
##        else:
##            face = [startVertexNumber, startVertexNumber+3, startVertexNumber+2, startVertexNumber+1]
##        
##        # Reverse order if needed
##        if self.clockwiseOrder: face.reverse()
##
##        
##        print(face)
##        print("")
##        
##        return face
        

    def createVertexListFromVectors(self, v1, v2, v3, v4):
        return [v1.toList(), v2.toList(), v3.toList(), v4.toList()]


class Vector:

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    """
    Vector functions:
         normalize()
         length()
         leftXYPerpendicular()
         rightXYPerpendicular()
         toList()
    """
    def normalize(v):
        return v.__div__(v.length())
        
    def length(v):
        return (v.x**2 + v.y**2 + v.z**2)**0.5

    def leftXYPerpendicular(v1):
        v2 = Vector()
        v2.x = -v1.y
        v2.y = v1.x
        return v2
        
    def rightXYPerpendicular(v1):
        v2 = Vector()
        v2.x = v1.y
        v2.y = -v1.x
        return v2

    def toList(v):
        return [v.x, v.y, v.z]
            

    """
    Vector operations:
        +, - (add/sub elementwise or by scaler
        * (cross product or multiplication by scaler)
        - (negative)
        / (division by a scaler)
    """
    def __add__(v1, v2):
        if not(isinstance(v2, Vector)):
            v2 = Vector(v2, v2, v2)
        v3 = Vector()
        v3.x = v1.x + v2.x
        v3.y = v1.y + v2.y
        v3.z = v1.z + v2.z
        return v3

    def __sub__(v1, v2):
        if not(isinstance(v2, Vector)):
            v2 = Vector(v2, v2, v2)
        v3 = Vector()
        v3.x = v1.x - v2.x
        v3.y = v1.y - v2.y
        v3.z = v1.z - v2.z
        return v3
    
    def __mul__(v1, v2):
        if not(isinstance(v2, Vector)):
            v2 = Vector(v2, v2, v2)
        v3 = Vector()
        v3.x = v1.x * v2.x
        v3.y = v1.y * v2.y
        v3.z = v1.z * v2.z
        return v3

    def __mul__(v1, v2):
        if not(isinstance(v2, Vector)):
            v2 = Vector(v2, v2, v2)
        v3 = Vector()
        v3.x = v1.x * v2.x
        v3.y = v1.y * v2.y
        v3.z = v1.z * v2.z
        return v3

    def __div__(v1, scaler):
        v2 = Vector()
        v2.x = v1.x / scaler
        v2.y = v1.y / scaler
        v2.z = v1.z / scaler
        return v2

    def __neg__(v1):
        v2 = Vector()
        v2.x = -v1.x
        v2.y = -v1.y
        v2.z = -v1.z
        return v2

    
    """
    Conversion to string
    """
    def __str__(self):
        return "<%.4f, %.4f, %.4f>" % (self.x, self.y, self.z)



