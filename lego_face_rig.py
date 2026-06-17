bl_info = {
    "name": "LEGO Face Rig (MecaFace Style)",
    "description": "Customizable LEGO-style face rig for animators.",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "View3D > Sidebar > LEGO Face Rig",
    "category": "Animation",
}

import bpy
from bpy.props import FloatProperty, PointerProperty
from bpy.types import Panel, Operator, PropertyGroup

class LEGOFaceProperties(PropertyGroup):
    eye_left_x: FloatProperty(
        name="Left Eye X",
        description="Move the left eye horizontally",
        default=0.0,
        min=-1.0,
        max=1.0
    )
    eye_left_y: FloatProperty(
        name="Left Eye Y",
        description="Move the left eye vertically",
        default=0.0,
        min=-1.0,
        max=1.0
    )
    eye_right_x: FloatProperty(
        name="Right Eye X",
        description="Move the right eye horizontally",
        default=0.0,
        min=-1.0,
        max=1.0
    )
    eye_right_y: FloatProperty(
        name="Right Eye Y",
        description="Move the right eye vertically",
        default=0.0,
        min=-1.0,
        max=1.0
    )
    mouth_open: FloatProperty(
        name="Mouth Open",
        description="Open or close the mouth",
        default=0.0,
        min=0.0,
        max=1.0
    )
    mouth_smile: FloatProperty(
        name="Mouth Smile",
        description="Control the smile curve",
        default=0.0,
        min=-1.0,
        max=1.0
    )

class OBJECT_OT_CreateLEGOFace(Operator):
    bl_idname = "object.create_lego_face"
    bl_label = "Create LEGO Face"
    bl_description = "Generate a LEGO-style face rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Create LEGO head
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
        lego_head = context.active_object
        lego_head.name = "LEGO_Head"

        # Create eye objects
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(-0.2, 0.9, 0))
        eye_left = context.active_object
        eye_left.name = "LEGO_Eye_Left"

        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0.2, 0.9, 0))
        eye_right = context.active_object
        eye_right.name = "LEGO_Eye_Right"

        # Create mouth object
        bpy.ops.mesh.primitive_plane_add(size=0.4, location=(0, 0.85, -0.1))
        mouth = context.active_object
        mouth.name = "LEGO_Mouth"

        # Parent eyes and mouth to the head
        eye_left.parent = lego_head
        eye_right.parent = lego_head
        mouth.parent = lego_head

        return {'FINISHED'}

class VIEW3D_PT_LEGOFaceRigPanel(Panel):
    bl_label = "LEGO Face Rig"
    bl_idname = "VIEW3D_PT_LEGOFaceRigPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LEGO Rig'

    def draw(self, context):
        layout = self.layout
        props = context.scene.lego_face_properties

        layout.prop(props, "eye_left_x")
        layout.prop(props, "eye_left_y")
        layout.prop(props, "eye_right_x")
        layout.prop(props, "eye_right_y")
        layout.prop(props, "mouth_open")
        layout.prop(props, "mouth_smile")
        layout.operator("object.create_lego_face")

# Update function for drivers
def update_eye_left(self, context):
    obj = bpy.data.objects.get("LEGO_Eye_Left")
    if obj:
        obj.location.x = self.eye_left_x
        obj.location.z = self.eye_left_y

def update_eye_right(self, context):
    obj = bpy.data.objects.get("LEGO_Eye_Right")
    if obj:
        obj.location.x = self.eye_right_x
        obj.location.z = self.eye_right_y

def update_mouth(self, context):
    obj = bpy.data.objects.get("LEGO_Mouth")
    if obj:
        obj.scale.y = 1 + self.mouth_open
        obj.location.y = 0.85 + (self.mouth_smile * 0.1)

# Register properties and handlers
LEGOFaceProperties.eye_left_x.update = update_eye_left
LEGOFaceProperties.eye_left_y.update = update_eye_left
LEGOFaceProperties.eye_right_x.update = update_eye_right
LEGOFaceProperties.eye_right_y.update = update_eye_right
LEGOFaceProperties.mouth_open.update = update_mouth
LEGOFaceProperties.mouth_smile.update = update_mouth

classes = [
    LEGOFaceProperties,
    OBJECT_OT_CreateLEGOFace,
    VIEW3D_PT_LEGOFaceRigPanel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.lego_face_properties = PointerProperty(type=LEGOFaceProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.lego_face_properties

if __name__ == "__main__":
    register()
