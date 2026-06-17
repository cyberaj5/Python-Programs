bl_info = {
    "name": "Lego Face Rig Generator",
    "blender": (4, 32, 0),
    "category": "Rigging",
    "author": "AJ",
    "version": (1, 1),
    "description": "Generate a simple face rig with expressions like smiling, frowning, and more for Lego faces.",
    "support": "COMMUNITY",
}

import bpy
import mathutils

# Safe error handling for mesh creation and rigging
def create_face_rig(obj):
    try:
        # Create materials for different expressions
        mat_smile = bpy.data.materials.new(name="Smile")
        mat_smile.use_nodes = True

        mat_frown = bpy.data.materials.new(name="Frown")
        mat_frown.use_nodes = True

        mat_blink_left = bpy.data.materials.new(name="Blink_Left")
        mat_blink_left.use_nodes = True

        mat_blink_right = bpy.data.materials.new(name="Blink_Right")
        mat_blink_right.use_nodes = True

        # Ensure the object is a mesh before continuing
        if obj.type != 'MESH':
            raise TypeError("Selected object is not a mesh. Please select a Lego mesh.")

        # Create a simple face mesh (plane) and place it in front of the Lego model
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0.1))
        face_obj = bpy.context.object
        face_obj.name = "Lego_Face"
        
        # Create face rig (mesh, not bones, but a placeholder rig)
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0.2))
        face_rig = bpy.context.object
        face_rig.name = "Face_Rig"
        face_rig.empty_display_size = 0.2

        # Parent face rig to Lego model to keep it in place
        face_rig.parent = obj
        
        # Assign materials for different expressions
        face_obj.data.materials.append(mat_smile)
        face_obj.data.materials.append(mat_frown)
        face_obj.data.materials.append(mat_blink_left)
        face_obj.data.materials.append(mat_blink_right)

        # Adding shape keys (expressions) to the face mesh
        if not face_obj.data.shape_keys:
            face_obj.shape_key_add(name="Basis")
        smile_key = face_obj.shape_key_add(name="Smile")
        frown_key = face_obj.shape_key_add(name="Frown")
        blink_left_key = face_obj.shape_key_add(name="Blink_Left")
        blink_right_key = face_obj.shape_key_add(name="Blink_Right")

        return face_obj, face_rig
    except Exception as e:
        print(f"Error in create_face_rig: {e}")
        raise e

# Operator to add the face rig to Lego face
class LegoFaceRigOperator(bpy.types.Operator):
    bl_idname = "object.lego_face_rig"
    bl_label = "Generate Lego Face Rig"
    bl_description = "Generate a simple rigged Lego face with expressions."

    def execute(self, context):
        try:
            # Step 1: Ensure that the selected object is a mesh (Lego face mesh)
            obj = context.object
            if obj is None or obj.type != 'MESH':
                self.report({'ERROR'}, "Please select a Lego mesh object!")
                return {'CANCELLED'}

            # Step 2: Create face rig with expressions
            face_obj, face_rig = create_face_rig(obj)

            # Step 3: Add basic shape key (e.g., smile) to face for facial expression control
            if not face_obj.data.shape_keys:
                face_obj.shape_key_add(name="Basis")
            smile_key = face_obj.shape_key_add(name="Smile")
            frown_key = face_obj.shape_key_add(name="Frown")
            blink_left_key = face_obj.shape_key_add(name="Blink_Left")
            blink_right_key = face_obj.shape_key_add(name="Blink_Right")

            # Report success
            self.report({'INFO'}, "Lego Face Rig generated successfully with expressions.")
            return {'FINISHED'}

        except Exception as e:
            print(f"Error in LegoFaceRigOperator: {e}")
            self.report({'ERROR'}, f"Failed to generate Lego face rig: {str(e)}")
            return {'CANCELLED'}

# Panel to control the operator in the Blender interface
class LegoFaceRigPanel(bpy.types.Panel):
    bl_label = "Lego Face Rig Generator"
    bl_idname = "OBJECT_PT_lego_face_rig"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lego Rigging'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.lego_face_rig")

def register():
    try:
        bpy.utils.register_class(LegoFaceRigOperator)
        bpy.utils.register_class(LegoFaceRigPanel)
        print("Lego Face Rig Generator registered successfully.")
    except Exception as e:
        print(f"Error in registering classes: {e}")

def unregister():
    try:
        bpy.utils.unregister_class(LegoFaceRigOperator)
        bpy.utils.unregister_class(LegoFaceRigPanel)
        print("Lego Face Rig Generator unregistered successfully.")
    except Exception as e:
        print(f"Error in unregistering classes: {e}")

if __name__ == "__main__":
    register()
