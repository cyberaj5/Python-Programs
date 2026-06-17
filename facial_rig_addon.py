import bpy

def create_facial_rig():
    # Ensure we are in object mode
    if bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Select the active object (assumed to be the character mesh)
    character = bpy.context.object
    if not character:
        print("No active object found!")
        return

    # Create a new armature for the facial rig
    bpy.ops.object.armature_add(enter_editmode=True)
    armature = bpy.context.object
    armature.name = "FacialRig"
    
    # Create bones for key facial features (e.g., eyes, mouth, brows)
    bones = [
        {'name': 'Eye_Left', 'head': (0, 0, 0), 'tail': (0, 0.2, 0)},
        {'name': 'Eye_Right', 'head': (0, 0, 0), 'tail': (0, -0.2, 0)},
        {'name': 'Mouth_Left', 'head': (0, 0, 0), 'tail': (0.2, 0, 0)},
        {'name': 'Mouth_Right', 'head': (0, 0, 0), 'tail': (-0.2, 0, 0)},
        {'name': 'Eyebrow_Left', 'head': (0, 0.2, 0), 'tail': (0, 0.3, 0)},
        {'name': 'Eyebrow_Right', 'head': (0, -0.2, 0), 'tail': (0, -0.3, 0)}
    ]
    
    # Adding bones to armature
    for bone in bones:
        bpy.ops.armature.bone_primitive_add(name=bone['name'])
        bpy.context.object.data.edit_bones[bone['name']].head = bone['head']
        bpy.context.object.data.edit_bones[bone['name']].tail = bone['tail']
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Add a basic mesh constraint to allow bone movement for facial expressions
    character.modifiers.new(name="FacialRig", type='ARMATURE')
    character.modifiers["FacialRig"].object = armature
    
    print("Facial Rig Created Successfully!")

# Run the facial rig creation function
create_facial_rig()

