bl_info = {
    "name": "Auto Facial Rig (MecaFace Replica)",
    "blender": (4, 32, 0),
    "category": "Rigging",
    "author": "Your Name",
    "version": (1, 0),
    "description": "Automatic Facial Rigging similar to MecaFace",
    "support": "COMMUNITY",
}

import bpy

class AutoFacialRigOperator(bpy.types.Operator):
    bl_idname = "object.auto_facial_rig"
    bl_label = "Create Auto Facial Rig"

    def execute(self, context):
        # Ensure the active object is selected (should be a mesh)
        character = bpy.context.object
        if not character or character.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object!")
            return {'CANCELLED'}

        # Create armature for facial rig
        bpy.ops.object.armature_add(enter_editmode=True)
        armature = bpy.context.object
        armature.name = "FacialRig"

        # Add bones for key facial features
        bones = [
            {'name': 'Eye_Left', 'head': (0.2, 0.5, 0), 'tail': (0.2, 0.6, 0)},
            {'name': 'Eye_Right', 'head': (-0.2, 0.5, 0), 'tail': (-0.2, 0.6, 0)},
            {'name': 'Mouth_Left', 'head': (0.2, -0.3, 0), 'tail': (0.3, -0.3, 0)},
            {'name': 'Mouth_Right', 'head': (-0.2, -0.3, 0), 'tail': (-0.3, -0.3, 0)},
            {'name': 'Eyebrow_Left', 'head': (0.2, 0.6, 0), 'tail': (0.2, 0.7, 0)},
            {'name': 'Eyebrow_Right', 'head': (-0.2, 0.6, 0), 'tail': (-0.2, 0.7, 0)},
        ]

        for bone in bones:
            bpy.ops.armature.bone_primitive_add(name=bone['name'])
            bpy.context.object.data.edit_bones[bone['name']].head = bone['head']
            bpy.context.object.data.edit_bones[bone['name']].tail = bone['tail']

        bpy.ops.object.mode_set(mode='OBJECT')

        # Link armature to mesh (character)
        modifier = character.modifiers.new(name="FacialRig", type='ARMATURE')
        modifier.object = armature

        self.report({'INFO'}, "Facial Rig Created Successfully!")
        return {'FINISHED'}

class FacialRigPanel(bpy.types.Panel):
    bl_label = "Auto Facial Rig"
    bl_idname = "OBJECT_PT_auto_facial_rig"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.auto_facial_rig")

def menu_func(self, context):
    self.layout.operator(AutoFacialRigOperator.bl_idname)

def register():
    bpy.utils.register_class(AutoFacialRigOperator)
    bpy.utils.register_class(FacialRigPanel)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(AutoFacialRigOperator)
    bpy.utils.unregister_class(FacialRigPanel)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
