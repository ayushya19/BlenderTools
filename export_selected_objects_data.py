bl_info = {
    "name": "Export Selected Objects Data",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import json
import os
from mathutils import Vector
from math import degrees

def object_data_to_dict(obj):
    data = {
        "name": obj.name,
        "location": list(obj.location),
        "rotation": list(map(degrees, obj.rotation_euler)),
        "scale": list(obj.scale),
        "parent": obj.parent.name if obj.parent else "No Parent",
        "children_count": len(obj.children)
    }
    return data

def export_selected_objects_data(file_path):
    selected_objects = bpy.context.selected_objects
    objects_data = [object_data_to_dict(obj) for obj in selected_objects]

    with open(file_path, 'w') as json_file:
        json.dump(objects_data, json_file, indent=4)

class OBJECT_OT_export_data(bpy.types.Operator):
    """Export selected objects data to a JSON file"""
    bl_idname = "object.export_data"
    bl_label = "Export Selected Objects Data"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        if not self.filepath:
            self.report({'ERROR'}, "File path is empty")
            return {'CANCELLED'}
        
        export_selected_objects_data(self.filepath)
        self.report({'INFO'}, f"Data exported to {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class VIEW3D_PT_export_data_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Export Selected Objects Data"
    bl_idname = "VIEW3D_PT_export_data"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.export_data")

def register():
    bpy.utils.register_class(OBJECT_OT_export_data)
    bpy.utils.register_class(VIEW3D_PT_export_data_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_export_data)
    bpy.utils.unregister_class(VIEW3D_PT_export_data_panel)

if __name__ == "__main__":
    register()
