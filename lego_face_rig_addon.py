bl_info = {
    "name": "Lego Face Rig (MecaFace-like)",
    "blender": (4, 32, 0),
    "category": "Rigging",
    "author": "Your Name",
    "version": (1, 0),
    "description": "Automatic Lego Face Rigging similar to MecaFace",
    "support": "COMMUNITY",
}

import bpy

class AutoLegoFaceRigOperator(bpy.types.Operator):
    bl_idname = "object.auto_lego_face_rig"
    bl_label = "Create Lego Face Rig"

    def execute(self, context):
        # Ensure we are in object mode
        if bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Select the active object (Lego head mesh)
        lego_head = bpy.context.object
        if not lego_head:
            self.report({'ERROR'}, "No active object found!")
            return {'CANCELLED'}

        # Create the armature for the face rig
        bpy.ops.object.armature_add(enter_editmode=True)
        armature = bpy.context.object
        armature.name = "LegoFaceRig"
        
        # Add bones for key facial features (mouth and eyes)
        bones = [
            {'name': 'Mouth', 'head': (0, 0, 0), 'tail': (0, 0.5, 0)},
            {'name': 'Eye_Left', 'head': (0.2, 0.5, 0), 'tail': (0.2, 0.6, 0)},
            {'name': 'Eye_Right', 'head': (-0.2, 0.5, 0), 'tail': (-0.2, 0.6, 0)},
        ]

        for bone in bones:
            bpy.ops.armature.bone_primitive_add(name=bone['name'])
            bpy.context.object.data.edit_bones[bone['name']].head = bone['head']
            bpy.context.object.data.edit_bones[bone['name']].tail = bone['tail']
        
        bpy.ops.object.mode_set(mode='OBJECT')

        # Link armature to mesh (character)
        modifier = lego_head.modifiers.new(name="FaceRig", type='ARMATURE')
        modifier.object = armature
        
        # Create shape keys for facial expressions (smile, frown)
        if "Shape Keys" not in lego_head.data.keys():
            lego_head.shape_key_add(name="Basis")

        shape_key_smile = lego_head.shape_key_add(name="Smile")
        shape_key_frown = lego_head.shape_key_add(name="Frown")
        
        # Set up basic expression modifications (this part would be expanded later)
        shape_key_smile.value = 0.2  # Smile expression default
        shape_key_frown.value = 0.2  # Frown expression default

        self.report({'INFO'}, "Lego Face Rig Created Successfully!")
        return {'FINISHED'}

class LegoFaceRigPanel(bpy.types.Panel):
    bl_label = "Lego Face Rig"
    bl_idname = "OBJECT_PT_lego_face_rig"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.auto_lego_face_rig")

def menu_func(self, context):
    self.layout.operator(AutoLegoFaceRigOperator.bl_idname)

def register():
    bpy.utils.register_class(AutoLegoFaceRigOperator)
    bpy.utils.register_class(LegoFaceRigPanel)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(AutoLegoFaceRigOperator)
    bpy.utils.unregister_class(LegoFaceRigPanel)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
