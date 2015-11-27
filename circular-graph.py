# Blender 2.63
import bpy
import bmesh
import random
import math

def rebanada (deg, size, stepSize, name):
    deg = deg * 360
    print('DEGS:', deg)
    bm = bmesh.new()
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name,mesh)
    bm.from_mesh(mesh)
    
    bm.verts.new((0, 0, 0))
    rad = math.radians(deg)
    verts = []
    
    for step in range(int(deg/stepSize) + 1):
        rad = math.radians(stepSize * step)
        bm.verts.new((math.sin(rad), math.cos(rad), 0.0))
        verts.append(rad)
    
    if deg % stepSize:
        rad = math.radians(deg)
        bm.verts.new((math.sin(rad), math.cos(rad), 0.0))
        verts.append(rad)

    if not len(verts) % 2:
        rad = (verts[-1] + verts[-2]) / 2
        bm.verts.new((math.sin(rad), math.cos(rad), 0.0))
        bm.verts.ensure_lookup_table()
        bm.verts[-1].co.xyz, bm.verts[-2].co.xyz = bm.verts[-2].co.xyz, bm.verts[-1].co.xyz
        verts[-1:-1] = [rad]


    for face in range(int(len(verts) / 2)):
        bm.verts.ensure_lookup_table()
        bm.faces.new(bm.verts[1 + 2 * face:4 + 2 * face] + [bm.verts[0]])
        
    bm.to_mesh(mesh)
    bpy.data.scenes[0].objects.link(obj)
    
    obj.select = True
    bpy.data.scenes[0].objects.active = obj
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region()
    bpy.ops.transform.translate(value=(0, 0, 0.5))
    bpy.ops.object.editmode_toggle()
    obj.select = False
    return obj
    
def toRelative(data):
    total = sum(data)
    relativos = []
    for num in data:
        relativos.append(num / total)
    return relativos
    
def grafica(data):
    parts = toRelative(data)
    size = 1
    rot = 0
    step = 5 if min(parts) * 360 >= 5 else min(parts) * 360
        
    for part in range(len(parts)):
        obj = rebanada(parts[part], size, step, 'R' + str(part))
        obj.select = True
        bpy.ops.transform.translate(value=(0, 0, 0.1 * part))
        bpy.ops.transform.rotate(value=rot * math.pi * 2, axis=(0, 0, -1))
        rot += parts[part]
        mat = random.choice(list(bpy.data.materials))
        obj.data.materials.append(mat)
        obj.select = False

def color():
    digits = {'0':0.0, '3':0.2, '6':0.4, '9':0.6, 'C':0.8, 'F':1.0}
    name = ''
    color = []
    for x in range(3):
        digit = random.choice(list(digits))
        name += digit
        color.append(digits[digit])
    return name, color

def materials(amount):
    for n in range(amount):
        name, col = color()
        if bpy.data.materials.find(name) == -1:
            bpy.data.materials.new(name)
            bpy.data.materials[name].diffuse_color = col
    
materials(10)
grafica([16,5,3])
