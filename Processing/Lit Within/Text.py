import bpy
import math as m

verts = []
faces = []

 
# Build a circular soma
radius  = 1.0
samples = 30.0
angle   = 360.0/samples

# Add center vertex
x,y,z = 0.0, 0.0, 0.0
verts.append((x, y, z))

# Add a ring of vertices
a = 0.0
while a<360.0:
    x = m.cos(m.radians(a)) * radius
    y = m.sin(m.radians(a)) * radius
    verts.append((x,y,z))
    a += angle

# Build the faces (triangles fanning out from the center)
i = 1
while i < samples:
    f = (i, 0, i+1)
    faces.append(f)
    i += 1
f = (i, 0, 1)
faces.append(f)



 
me = bpy.data.meshes.new("Neuron")   # create a new mesh  
 
ob = bpy.data.objects.new("Neuron", me)          # create an object with that mesh
ob.location = bpy.context.scene.cursor_location   # position object at 3d-cursor
bpy.context.scene.objects.link(ob)                # Link object to scene
 
# Fill the mesh with verts, edges, faces 
me.from_pydata(verts,[],faces)   # edges or faces should be [], or you ask for problems
me.update(calc_edges=True)    # Update mesh with new data