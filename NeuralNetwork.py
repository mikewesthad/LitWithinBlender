import bpy
from Neuron import Neuron
from Vector import Vector
from LightBox import LightBox
import random as r

class Network:
    def __init__(self, width, height, depth, numberCells):        
        self.cells = []
        self.verts = []
        self.faces = []

        # Set the position to the 3D cursor 
        pos             = bpy.context.scene.cursor_location
        self.position   = Vector(pos[0], pos[1], pos[2])
            
        # Create a light box
        self.lightBox = LightBox(self.position, width, height, depth)  

        # Create a set of cells
        for i in range(numberCells):
            self.cells.append(Neuron(r.uniform(-width/2.0,width/2.0),
                                     r.uniform(-height/2.0,height/2.0),
                                     self))
            
    def update(self):
        for c in self.cells: c.growDendrites()

    def buildNetwork(self):
        self.buildMesh("Network", self.position.toList(), self.verts, self.faces)
        
    def register(self, newVerts, newFaces):
        offset = len(self.verts)
        for f in range(len(newFaces)):
            for i in range(len(newFaces[f])): 
                newFaces[f][i] += offset
            self.faces.append(newFaces[f][:])
        self.verts = self.verts + newVerts
        
    def buildMesh(self, name, position, verts, faces):
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        obj.location = position
        bpy.context.scene.objects.link(obj)
        mesh.from_pydata(verts,[],faces)
        mesh.update(calc_edges=True)
                            
                

    



