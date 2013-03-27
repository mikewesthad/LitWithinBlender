import bpy

name = "test"

# Create two planes
# The top plane has a clockwise ordering (and a downward facing normal)
# The bottom plane has a counter-clockwise ordering (and an upward facing normal)

verts = [[-1.0,-1.0,+0.0],  
         [-1.0,+1.0,+0.0],
         [+1.0,+1.0,+0.0],
         [+1.0,-1.0,+0.0],
         [-1.0,-1.0,-5.0],  
         [-1.0,+1.0,-5.0],
         [+1.0,+1.0,-5.0],
         [+1.0,-1.0,-5.0]]
         
faces = [[0, 1, 2, 3],
         [7, 6, 5, 4]]

mesh = bpy.data.meshes.new(name)
obj = bpy.data.objects.new(name, mesh)
obj.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(obj)
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)