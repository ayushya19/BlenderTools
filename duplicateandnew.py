bl_info = {
    "name": "Duplicate Grid Tool",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import random

def create_material(name, color, texture_image_path):
    # Create a new material
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color

        if texture_image_path:
            # Add a texture image to the material
            tex_image = material.node_tree.nodes.new('ShaderNodeTexImage')
            tex_image.image = bpy.data.images.load(texture_image_path)
            material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

    return material

def duplicate_object(context, grid_size=4, spacing=2.0):
    obj = context.object
    
    mesh_objects = []
    
    # Check if the selected object has mesh data
    if obj.type == 'MESH':
        mesh_objects.append(obj)
    
    # Check if the selected object has children with mesh data
    for child in obj.children:
        if child.type == 'MESH':
            mesh_objects.append(child)

    if not mesh_objects:
        print("Selected object or its children do not have any mesh data.")
        return

    for mesh_obj in mesh_objects:
        original_location = mesh_obj.location
        materials = []
        texture_paths = [None] * 16  # Replace with your texture paths if you have any

        for i in range(grid_size):
            for j in range(grid_size):
                # Duplicate the object
                new_obj = mesh_obj.copy()
                new_obj.data = mesh_obj.data.copy()
                bpy.context.collection.objects.link(new_obj)

                # Calculate new location
                new_obj.location = (original_location.x + i * spacing, original_location.y + j * spacing, original_location.z)

                # Create a unique material for each object
                color = (random.random(), random.random(), random.random(), 1.0)
                material_name = f"Material_{i}_{j}"
                texture_path = texture_paths[i * grid_size + j]  # Get texture path if exists
                new_material = create_material(material_name, color, texture_path)
                materials.append(new_material)

                # Assign the new material to the object
                if new_obj.data.materials:
                    new_obj.data.materials[0] = new_material
                else:
                    new_obj.data.materials.append(new_material)

class OBJECT_OT_duplicate_grid(bpy.types.Operator):
    """Duplicate selected object in a 4x4 grid with unique materials"""
    bl_idname = "object.duplicate_grid"
    bl_label = "Duplicate Grid"
    bl_options = {'REGISTER', 'UNDO'}

    grid_size: bpy.props.IntProperty(name="Grid Size", default=4, min=1, max=10)
    spacing: bpy.props.FloatProperty(name="Spacing", default=2.0, min=0.1, max=10.0)

    def execute(self, context):
        duplicate_object(context, self.grid_size, self.spacing)
        return {'FINISHED'}

class VIEW3D_PT_duplicate_grid_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Duplicate Grid Tool"
    bl_idname = "VIEW3D_PT_duplicate_grid"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj is None:
            layout.label(text="No object selected")
        else:
            layout.label(text="Selected object: " + obj.name)
            layout.operator("object.duplicate_grid")

def register():
    bpy.utils.register_class(OBJECT_OT_duplicate_grid)
    bpy.utils.register_class(VIEW3D_PT_duplicate_grid_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_duplicate_grid)
    bpy.utils.unregister_class(VIEW3D_PT_duplicate_grid_panel)

if __name__ == "__main__":
    register()
