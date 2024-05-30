bl_info = {
    "name": "Basic Lighting Setup Tool",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

def create_light(light_type, name, location, energy=1000, **kwargs):
    # Create a new light datablock
    light_data = bpy.data.lights.new(name=name, type=light_type)
    light_data.energy = energy

    # Set additional properties for specific light types
    if light_type == 'SPOT':
        light_data.spot_size = kwargs.get('spot_size', 1.0)
        light_data.spot_blend = kwargs.get('spot_blend', 0.15)
    elif light_type == 'AREA':
        light_data.size = kwargs.get('size', 1.0)
    
    # Create a new light object with this data
    light_object = bpy.data.objects.new(name, light_data)
    
    # Set the location of the light object
    light_object.location = location

    # Link the light object to the current collection
    bpy.context.collection.objects.link(light_object)

    return light_object

def setup_basic_lighting():
    # Clear existing lights
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()

    # Create point light
    point_light = create_light(
        light_type='POINT',
        name='Point Light',
        location=(5, 5, 5),
        energy=800
    )

    # Create spotlight
    spotlight = create_light(
        light_type='SPOT',
        name='Spotlight',
        location=(-5, -5, 10),
        energy=1200,
        spot_size=0.785,  # 45 degrees in radians
        spot_blend=0.3
    )
    spotlight.rotation_euler = (1.1, 0, 0.8)  # Rotate spotlight to point towards the center of the scene

    # Create area light
    area_light = create_light(
        light_type='AREA',
        name='Area Light',
        location=(0, -10, 10),
        energy=600,
        size=5
    )
    area_light.rotation_euler = (1.2, 0, 0)  # Rotate area light to point towards the center of the scene

    # Create sunlight
    sun_light = create_light(
        light_type='SUN',
        name='Sun Light',
        location=(0, 0, 20),
        energy=2
    )
    sun_light.rotation_euler = (1.2, -0.3, -0.8)  # Rotate sunlight to simulate natural sunlight

class OBJECT_OT_setup_lighting(bpy.types.Operator):
    """Set up basic lighting for the scene"""
    bl_idname = "object.setup_lighting"
    bl_label = "Setup Basic Lighting"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        setup_basic_lighting()
        return {'FINISHED'}

class VIEW3D_PT_lighting_setup_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Lighting Setup Tool"
    bl_idname = "VIEW3D_PT_lighting_setup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.setup_lighting")

def register():
    bpy.utils.register_class(OBJECT_OT_setup_lighting)
    bpy.utils.register_class(VIEW3D_PT_lighting_setup_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_setup_lighting)
    bpy.utils.unregister_class(VIEW3D_PT_lighting_setup_panel)

if __name__ == "__main__":
    register()
