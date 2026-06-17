bl_info = {
    "name": "Auto-Fit Lego Face Rig",
    "blender": (4, 32, 0),
    "category": "Rigging",
    "author": "AJ",
    "version": (1, 0),
    "description": "Auto-fits rig and controls to Lego face mesh with expressions",
    "support": "COMMUNITY",
}

import bpy
import mathutils

# Ensure Blender is in the correct context
def check_active_object(context):
    obj = context.object
    if obj is None or obj.type != 'MESH':
        return None
    return obj

class AutoFitLegoFaceRigOperator(bpy.types.Operator):
    bl_idname = "object.auto_fit_lego_face_rig"
    bl_label = "Auto-Fit Lego Face Rig"
    bl_description = "Adds rig and controls to Lego face mesh, scaling it to fit automatically"

    def execute(self, context):
        obj = check_active_object(context)
        if obj is None:
            self.report({'ERROR'}, "No mesh object selected or selected object is not a mesh!")
            return {'CANCELLED'}

        # Ensure the object has shape keys
        if not obj.data.shape_keys:
            obj.shape_key_add(name="Basis")  # Add the default shape key

        # Create expression shape keys
        smile_key = obj.shape_key_add(name="Smile")
        mouth_open_key = obj.shape_key_add(name="Mouth_Open")
        left_eye_blink_key = obj.shape_key_add(name="Eye_Blink_Left")
        right_eye_blink_key = obj.shape_key_add(name="Eye_Blink_Right")

        # Calculate the scaling factor based on the face's bounding box
        bbox = [obj.matrix_world @ v.co for v in obj.data.vertices]
        min_coord = mathutils.Vector((min([v.x for v in bbox]), min([v.y for v in bbox]), min([v.z for v in bbox])))
        max_coord = mathutils.Vector((max([v.x for v in bbox]), max([v.y for v in bbox]), max([v.z for v in bbox])))
        face_width = (max_coord - min_coord).length
        scale_factor = face_width / 2.0  # Scale the rig to fit the face

        # Create control objects (empties)
        bpy.ops.object.empty_add(type='CIRCLE', location=(0, 0, 0))
        mouth_control = bpy.context.object
        mouth_control.name = "Mouth_Control"
        mouth_control.empty_display_size = 0.3 * scale_factor

        bpy.ops.object.empty_add(type='SPHERE', location=(-0.5, 0.5, 0.5))
        left_eye_control = bpy.context.object
        left_eye_control.name = "Left_Eye_Control"
        left_eye_control.empty_display_size = 0.2 * scale_factor

        bpy.ops.object.empty_add(type='SPHERE', location=(0.5, 0.5, 0.5))
        right_eye_control = bpy.context.object
        right_eye_control.name = "Right_Eye_Control"
        right_eye_control.empty_display_size = 0.2 * scale_factor

        # Parent the control objects to the mesh
        mouth_control.parent = obj
        left_eye_control.parent = obj
        right_eye_control.parent = obj

        # Add drivers to control shape keys
        def add_driver_to_shape_key(control_obj, shape_key, expression_name):
            try:
                driver = shape_key.driver_add("value")
                driver.driver.type = 'AVERAGE'
                driver.driver.expression = f"{control_obj.name}.location[0]"
                driver.driver.variables.new().name = "control"
                driver.driver.variables["control"].targets[0].id_type = 'OBJECT'
                driver.driver.variables["control"].targets[0].id = control_obj
                driver.driver.variables["control"].targets[0].data_path = "location[0]"
            except Exception as e:
                self.report({'ERROR'}, f"Failed to add driver for {expression_name}: {str(e)}")

        # Add drivers for shape keys
        add_driver_to_shape_key(mouth_control, smile_key, "Smile")
        add_driver_to_shape_key(mouth_control, mouth_open_key, "Mouth_Open")
        add_driver_to_shape_key(left_eye_control, left_eye_blink_key, "Eye_Blink_Left")
        add_driver_to_shape_key(right_eye_control, right_eye_blink_key, "Eye_Blink_Right")

        self.report({'INFO'}, "Lego Face Rig created and auto-fitted successfully!")
        return {'FINISHED'}

class AutoFitLegoFaceRigPanel(bpy.types.Panel):
    bl_label = "Auto-Fit Lego Face Rig"
    bl_idname = "OBJECT_PT_auto_fit_lego_face_rig"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.auto_fit_lego_face_rig")

def register():
    try:
        bpy.utils.register_class(AutoFitLegoFaceRigOperator)
        bpy.utils.register_class(AutoFitLegoFaceRigPanel)
    except Exception as e:
        print(f"Error registering addon: {str(e)}")

def unregister():
    bpy.utils.unregister_class(AutoFitLegoFaceRigOperator)
    bpy.utils.unregister_class(AutoFitLegoFaceRigPanel)

if __name__ == "__main__":
    register()
