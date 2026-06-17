bl_info = {
    "name": "Lego Face Generator",
    "blender": (3, 0, 0),
    "category": "Object",
    "version": (1, 0, 0),
    "author": "AJ",
    "description": "Generate a pre-rigged Lego face with shape keys and support for assets."
}

import bpy

def create_lego_head(context):
    # Add a cylinder for the head
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1.5, location=(0, 0, 0))
    head = bpy.context.object
    head.name = "Lego_Head"

    # Add a UV Sphere for the top stud
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(0, 0, 1.2))
    stud = bpy.context.object
    stud.name = "Head_Stud"

    # Join the stud and the head
    bpy.ops.object.select_all(action='DESELECT')
    head.select_set(True)
    stud.select_set(True)
    bpy.context.view_layer.objects.active = head
    bpy.ops.object.join()

    # Add Shape Keys
    if head.data.shape_keys is None:
        head.shape_key_add(name="Basis")  # Basis shape key

    head.shape_key_add(name="Smile")
    head.shape_key_add(name="Blink")

    # Set smile key (example: deform bottom of the face slightly)
    smile_key = head.data.shape_keys.key_blocks["Smile"]
    bpy.context.object.active_shape_key = smile_key
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.translate(value=(0, 0, -0.1))  # Example deformation
    bpy.ops.object.mode_set(mode='OBJECT')

    # Set blink key (example: move top vertices to simulate a blink)
    blink_key = head.data.shape_keys.key_blocks["Blink"]
    bpy.context.object.active_shape_key = blink_key
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    return head

class OBJECT_OT_CreateLegoFace(bpy.types.Operator):
    """Operator to create a Lego face"""
    bl_idname = "object.create_lego_face"
    bl_label = "Create Lego Face"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        create_lego_head(context)
        return {'FINISHED'}

class VIEW3D_PT_LegoFacePanel(bpy.types.Panel):
    """UI Panel for the Lego Face Generator"""
    bl_label = "Lego Face Generator"
    bl_idname = "VIEW3D_PT_legoface_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lego Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.create_lego_face", text="Generate Lego Face")

classes = [
    OBJECT_OT_CreateLegoFace,
    VIEW3D_PT_LegoFacePanel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
