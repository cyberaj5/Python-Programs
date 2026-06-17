bl_info = {
    "name": "LEGO Face Rig (MecaFace Style)",
    "blender": (4, 32, 0),
    "category": "Object",
    "author": "Your Name",
    "description": "Customizable LEGO-style face with procedural controls for animators.",
    "version": (1, 0, 0),
    "support": "COMMUNITY",
}

import bpy
import bmesh

# Function to create a base LEGO face
def create_lego_face():
    # Create a base LEGO head
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
    head = bpy.context.object
    head.name = "LEGO_Head"
    
    # Smooth shading
    bpy.ops.object.shade_smooth()
    
    # Add materials for face customization
    mat = bpy.data.materials.new(name="LEGO_Head_Material")
    mat.use_nodes = True
    head.data.materials.append(mat)

    # Customize material for procedural face
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)

    # Add a new Principled BSDF
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    output_node.location = (400, 0)

    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)

    # Color inputs for face elements
    face_color = nodes.new(type="ShaderNodeRGB")
    face_color.location = (-400, 0)
    face_color.outputs[0].default_value = (1, 1, 0, 1)  # Default LEGO yellow
    
    # Link the color to the shader
    links.new(face_color.outputs[0], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs[0], output_node.inputs[0])

    return head

# Add a UI panel for face controls
class LEGOFaceRigPanel(bpy.types.Panel):
    bl_label = "LEGO Face Rig Controls"
    bl_idname = "VIEW3D_PT_lego_face_rig"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Face customization sliders
        layou
