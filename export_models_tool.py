bl_info = {
    "name": "Export Models Tool",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

class OBJECT_OT_export_models(bpy.types.Operator):
    """Export selected models to a specified format"""
    bl_idname = "object.export_models"
    bl_label = "Export Models"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    file_format: bpy.props.EnumProperty(
        name="File Format",
        description="Choose the file format for export",
        items=[
            ('OBJ', "OBJ", "Export as .obj file"),
            ('FBX', "FBX", "Export as .fbx file"),
            ('STL', "STL", "Export as .stl file"),
            ('GLB', "GLB", "Export as .glb file")
        ],
        default='OBJ'
    )
    
    def execute(self, context):
        if not self.filepath:
            self.report({'ERROR'}, "File path is empty")
            return {'CANCELLED'}

        export_funcs = {
            'OBJ': self.export_as_obj,
            'FBX': self.export_as_fbx,
            'STL': self.export_as_stl,
            'GLB': self.export_as_glb,
        }
        
        export_func = export_funcs.get(self.file_format)
        if export_func:
            export_func(context)
        else:
            self.report({'ERROR'}, "Unsupported file format")
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"Models exported to {self.filepath}")
        return {'FINISHED'}

    def export_as_obj(self, context):
        bpy.ops.export_scene.obj(
            filepath=self.filepath,
            use_selection=True,
            axis_forward='-Z',
            axis_up='Y'
        )

    def export_as_fbx(self, context):
        bpy.ops.export_scene.fbx(
            filepath=self.filepath,
            use_selection=True,
            axis_forward='-Z',
            axis_up='Y'
        )

    def export_as_stl(self, context):
        bpy.ops.export_mesh.stl(
            filepath=self.filepath,
            use_selection=True
        )

    def export_as_glb(self, context):
        bpy.ops.export_scene.gltf(
            filepath=self.filepath,
            use_selection=True
        )
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class VIEW3D_PT_export_models_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Export Models Tool"
    bl_idname = "VIEW3D_PT_export_models"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.export_models")

def register():
    bpy.utils.register_class(OBJECT_OT_export_models)
    bpy.utils.register_class(VIEW3D_PT_export_models_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_export_models)
    bpy.utils.unregister_class(VIEW3D_PT_export_models_panel)

if __name__ == "__main__":
    register()
