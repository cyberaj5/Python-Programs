bl_info = {
    "name": "MECA Face Rig",
    "author": "AJ",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Tool Shelf",
    "description": "Automates Lego-style face rigging",
    "category": "Animation",
}

import bpy

class OBJECT_OT_MecaFaceRig(bpy.types.Operator):
    """Create a MECA Face Rig"""
    bl_idname = "object.meca_face_rig"
    bl_label = "Create MECA Face Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Add your rigging logic here
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_MecaFaceRig.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_MecaFaceRig)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_MecaFaceRig)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
