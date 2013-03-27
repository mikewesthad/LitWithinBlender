import bpy
import random as r
import imp

import LightBox
imp.reload(LightBox)
from LightBox import LightBox

import Neuron
imp.reload(Neuron)
from Neuron import Neuron

import Vector
imp.reload(Vector)
from Vector import Vector



class Network:
    def __init__(self, lightboxDimensions, micronsPerBlenderUnit, numberCells):        
        self.cells = []
        self.verts = []
        self.faces = []

        # Set the position to the 3D cursor 
        pos             = bpy.context.scene.cursor_location
        self.position   = Vector(pos[0], pos[1], pos[2])
            
        # Create a light box
        self.lightBox = LightBox(self.position, lightboxDimensions, micronsPerBlenderUnit)  

        # Create a set of cells
        for i in range(numberCells):
            pos = Vector()
            self.cells.append(Neuron(pos,micronsPerBlenderUnit))
            

    def buildNetwork(self):

        cellsDoneGrowing = False
        while not(cellsDoneGrowing):
            cellsDoneGrowing = True
            for c in self.cells:
                if c.growing:
                    c.growDendrites()
                    cellsDoneGrowing = False
        for i in range(len(self.cells)):
            cell = self.cells[i]
            name = "Neuron "+str(i)
            verts = cell.verts
            faces = cell.faces
            self.buildMesh(name, verts, faces)
        
    def buildMesh(self, name, verts, faces):
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        obj.location = self.position.toList()
        bpy.context.scene.objects.link(obj)
        mesh.from_pydata(verts,[],faces)
        mesh.update(calc_edges=True)
                            
                

    



