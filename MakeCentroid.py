import bpy
import mathutils

def get_all_mesh_vertices(obj, vertices_list):
    if obj.type == 'MESH':
        mesh = obj.data
        vertices_world = [obj.matrix_world @ vert.co for vert in mesh.vertices]
        vertices_list.extend(vertices_world)
    
    for child in obj.children:
        get_all_mesh_vertices(child, vertices_list)

def calculate_centroid(vertices):
    if not vertices:
        return None
    
    centroid = mathutils.Vector((0, 0, 0))
    for vert in vertices:
        centroid += vert
    centroid /= len(vertices)
    
    return centroid

class OBJECT_OT_calculate_center(bpy.types.Operator):
    """Calculate the center of an object considering all its mesh children"""
    bl_idname = "object.calculate_center"
    bl_label = "Calculate Object Center"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj:
            self.report({'ERROR'}, "No active object selected")
            return {'CANCELLED'}
        
        vertices_list = []
        get_all_mesh_vertices(obj, vertices_list)
        
        if not vertices_list:
            self.report({'ERROR'}, "No mesh data found in the object and its children")
            return {'CANCELLED'}
        
        centroid = calculate_centroid(vertices_list)
        
        self.report({'INFO'}, f"Calculated Center: {centroid}")
        
        # Optionally, set the cursor to the calculated center
        context.scene.cursor.location = centroid

        return {'FINISHED'}

class VIEW3D_PT_calculate_center_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Calculate Object Center"
    bl_idname = "VIEW3D_PT_calculate_center"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.calculate_center")

def register():
    bpy.utils.register_class(OBJECT_OT_calculate_center)
    bpy.utils.register_class(VIEW3D_PT_calculate_center_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_calculate_center)
    bpy.utils.unregister_class(VIEW3D_PT_calculate_center_panel)

if __name__ == "__main__":
    register()
