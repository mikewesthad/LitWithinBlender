"""
LightBox is a cube object of width, height and depth located at (x, y, z) that
contains a point source lamp object at its center

It's class variables include:
    width
    height
    depth
    center (Vector class instance)
    verts (list of list)
    faces (list of list)
    mesh
    meshObj
    lamp
    lampObj    
"""

import bpy

class LightBox:
    def __init__(self, position, width, height, depth):
        
        self.width  = width
        self.height = height
        self.depth  = depth
        self.center = position
        
        verts, faces = [], []
        halfw, halfh, halfd = width/2.0, height/2.0, depth/2.0
        
        verts.append([+halfw, +halfh, -halfd]) 
        verts.append([+halfw, -halfh, -halfd]) 
        verts.append([-halfw, -halfh, -halfd]) 
        verts.append([-halfw, +halfh, -halfd]) 
        verts.append([+halfw, +halfh, +halfd]) 
        verts.append([+halfw, -halfh, +halfd]) 
        verts.append([-halfw, -halfh, +halfd]) 
        verts.append([-halfw, +halfh, +halfd])
        
        # Winding order taken from:
        #   http://blenderscripting.blogspot.com/2011/07/making-cube-using-frompydata.html
        faces = [[0, 1, 2, 3], 
                 [4, 7, 6, 5],
                 [0, 4, 5, 1],    
                 [1, 5, 6, 2],  
                 [2, 6, 7, 3],
                 [4, 0, 3, 7]]
        
        mesh                = bpy.data.meshes.new("Box")
        meshObj             = bpy.data.objects.new("Light Box", mesh)
        meshObj.location    = self.center.toList()
        bpy.context.scene.objects.link(meshObj)
        mesh.from_pydata(verts,[],faces)
        mesh.update(calc_edges=True)

        lamp                = bpy.data.lamps.new("Lamp", "POINT")
        lampObj             = bpy.data.objects.new("Inner Light", lamp)
        lampObj.location    = self.center.toList()
        lampObj.parent      = meshObj
        bpy.context.scene.objects.link(lampObj)

        self.mesh       = mesh
        self.meshObj    = meshObj
        self.lamp       = lamp
        self.lampObj    = lampObj
        self.faces      = faces
        self.verts      = verts
