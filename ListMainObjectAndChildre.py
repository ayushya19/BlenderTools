bl_info = {
    "name": "Scene Hierarchy Tool",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

def list_children(obj, children_list):
    for child in obj.children:
        children_list.append(child.name)
        list_children(child, children_list)

def find_parent_and_list_children(scene):
    hierarchy_info = {}
    for obj in scene.objects:
        if obj.parent:
            parent_name = obj.parent.name
        else:
            parent_name = "No Parent"
        
        children_names = []
        list_children(obj, children_names)

        hierarchy_info[obj.name] = {
            "parent": parent_name,
            "children": children_names
        }
    return hierarchy_info

class OBJECT_OT_scene_hierarchy_info(bpy.types.Operator):
    """Find the parent and list all children of each object in the scene"""
    bl_idname = "object.scene_hierarchy_info"
    bl_label = "Get Scene Hierarchy Info"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        hierarchy_info = find_parent_and_list_children(scene)
        
        for obj_name, info in hierarchy_info.items():
            self.report({'INFO'}, f"Object: {obj_name}")
            self.report({'INFO'}, f"  Parent: {info['parent']}")
            if info['children']:
                self.report({'INFO'}, f"  Children: {', '.join(info['children'])}")
            else:
                self.report({'INFO'}, "  Children: No Children")

        return {'FINISHED'}

class VIEW3D_PT_scene_hierarchy_info_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Scene Hierarchy Tool"
    bl_idname = "VIEW3D_PT_scene_hierarchy_info"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.scene_hierarchy_info")

def register():
    bpy.utils.register_class(OBJECT_OT_scene_hierarchy_info)
    bpy.utils.register_class(VIEW3D_PT_scene_hierarchy_info_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_scene_hierarchy_info)
    bpy.utils.unregister_class(VIEW3D_PT_scene_hierarchy_info_panel)

if __name__ == "__main__":
    register()
