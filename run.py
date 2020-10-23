import bpy
filepath = bpy.path.abspath("//main.py")
exec(compile(open(filepath).read(), filepath, 'exec'))