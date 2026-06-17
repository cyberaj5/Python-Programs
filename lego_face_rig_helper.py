bl_info = {
    "name": "Lego Face Rig Helper",
    "blender": (4, 32, 0),
    "category": "Rigging",
    "author": "AJ",
    "version": (1, 1),
    "description": "Creates a simple, effective rigging system for Lego faces, with control over expressions and auto-fitting to mesh size.",
    "support": "COMMUNITY",
}

import bpy
import mathutils

# Helper function to ensure object is a mesh
def check_active_object(context):
    obj = context.object
    if obj is None or obj.type != 'MESH':
        return None
    return obj

# Function to auto-fit the rig and control objects to the size of the Lego face
def auto_fit_rig(obj, controls):
    # Get the bounding box of the Lego face mesh
    bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
    min_x = min([corner.x for corner in bbox_corners])
    max_x = max([corner.x for corner in bbox_corners])
    scale_factor = max_x - min_x

    # Apply scaling to the controls and rig to fit the mesh size
    for control in controls:
        control.scale = mathutils.Vector((scale_factor, scale_factor, scale_factor))
        
    return scale_factor

# Operator to set up rigging for Lego face
class LegoFaceRigOperator(bpy.types.Operator):
    bl_idname = "object.lego_face_rig"
    bl_label = "Create Lego Face Rig"
    bl_description = "Set up rigging for Lego face mesh with expression controls."

    def execute(self, context):
        # Step 1: Ensure that the selected object is a mesh
        obj = check_active_object(context)
        if obj is None:
            self.report({'ERROR'}, "Please select a mesh object!")
            return {'CANCELLED'}
        
        # Step 2: Add shape keys if not already present
        if not obj.data.shape_keys:
            obj.shape_key_add(name="Basis")
        else:
            basis = obj.data.shape_keys.key_blocks.get("Basis")
            if not basis:
                obj.shape_key_add(name="Basis")

        # Step 3: Add expression-related shape keys
        smile_key = obj.shape_key_add(name="Smile")
        frown_key = obj.shape_key_add(name="Frown")
        blink_left_key = obj.shape_key_add(name="Blink_Left")
        blink_right_key = obj.shape_key_add(name="Blink_Right")

        # Step 4: Add empty control objects for manipulation
        bpy.ops.object.empty_add(type='CIRCLE', location=(0, 0, 0))
        mouth_control = bpy.context.object
        mouth_control.name = "Mouth_Control"
        mouth_control.empty_display_size = 0.5

        bpy.ops.object.empty_add(type='CIRCLE', location=(-0.5, 0.5, 0.5))
        left_eye_control = bpy.context.object
        left_eye_control.name = "Left_Eye_Control"
        left_eye_control.empty_display_size = 0.3

        bpy.ops.object.empty_add(type='CIRCLE', location=(0.5, 0.5, 0.5))
        right_eye_control = bpy.context.object
        right_eye_control.name = "Right_Eye_Control"
        right_eye_control.empty_display_size = 0.3

        # Step 5: Parent the control objects to the Lego face mesh
        mouth_control.parent = obj
        left_eye_control.parent = obj
        right_eye_control.parent = obj

        # Step 6: Auto-fit the rig based on mesh size
        controls = [mouth_control, left_eye_control, right_eye_control]
        scale_factor = auto_fit_rig(obj, controls)

        # Step 7: Add drivers to shape keys based on control objects
        def add_driver(control_obj, shape_key, expression_name):
            try:
                driver = shape_key.driver_add("value")
                driver.driver.type = 'AVERAGE'
                driver.driver.expression = f"{control_obj.name}.location[0]"
                driver.driver.variables.new().name = "control"
                driver.driver.variables["control"].targets[0].id_type = 'OBJECT'
                driver.driver.variables["control"].targets[0].id = control_obj
                driver.driver.variables["control"].targets[0].data_path = "location[0]"
            except Exception as e:
                self.report({'ERROR'}, f"Driver setup for {expression_name} failed: {str(e)}")

        add_driver(mouth_control, smile_key, "Smile")
        add_driver(mouth_control, frown_key, "Frown")
        add_driver(left_eye_control, blink_left_key, "Blink_Left")
        add_driver(right_eye_control, blink_right_key, "Blink_Right")

        self.report({'INFO'}, f"Lego Face Rig successfully created and auto-fitted with scale factor: {scale_factor}")
        return {'FINISHED'}

# Panel to control the operator in the Blender interface
class LegoFaceRigPanel(bpy.types.Panel):
    bl_label = "Lego Face Rig Helper"
    bl_idname = "OBJECT_PT_lego_face_rig"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lego Rigging'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.lego_face_rig")

def register():
    bpy.utils.register_class(LegoFaceRigOperator)
    bpy.utils.register_class(LegoFaceRigPanel)

def unregister():
    bpy.utils.unregister_class(LegoFaceRigOperator)
    bpy.utils.unregister_class(LegoFaceRigPanel)

if __name__ == "__main__":
    register()
