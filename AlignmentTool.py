# # # # # # # # # # # # # # # # # #
#         Alignment Tool          #
#        for Blender 2.80         #
#        by Florian Otten         #
# # # # # # # # # # # # # # # # # #

bl_info = {
    "name": "Alignment Tool",
    "description": "Tool for aligning objects and profiles in Blender.",
    "author": "Florian Otten",
    "version": (0, 3),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "https://github.com/wefo-coding/blender-alignment-tool",
    "tracker_url": "https://github.com/wefo-coding/blender-alignment-tool/issues/new",
    "category": "Object"
}


# # # # # # # # # # # # # # # # # #
#             Imports             #
# # # # # # # # # # # # # # # # # #

import bpy

# # # # # # # # # # # # # # # # # #
#            Functions            #
# # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # #
#           Properties            #
# # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # #
#            Operators            #
# # # # # # # # # # # # # # # # # #

class SetOrientationToObjectOperator(bpy.types.Operator):
    bl_idname = "align.set_orientation_to_object"
    bl_label = "to object"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    
    # Execute
    def execute(self, context):
        
        obj_src = context.active_object
        
        print("Bye")
        return {'FINISHED'}

class SetOrientationToVerticesOperator(bpy.types.Operator):
    bl_idname = "align.set_orientation_to_vertices"
    bl_label = "to vertices"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    inverse: bpy.props.BoolProperty(
        name = "Inverse",
        default = False,
        description = "TODO"
    )
    
    # Execute
    def execute(self, context):
        
        obj_src = context.active_object
        
        if(self.inverse):
            print("Bye")
        else:
            print("Hello World")
        return {'FINISHED'}

# # # # # # # # # # # # # # # # # #
#             Panels              #
# # # # # # # # # # # # # # # # # #

class OrientationPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_orientation"
    bl_label = "Orientation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Align"
    
    def draw(self, context):
        layout = self.layout
        layout.operator(SetOrientationToObjectOperator.bl_idname)
        layout.operator(SetOrientationToVerticesOperator.bl_idname)


# # # # # # # # # # # # # # # # # #
#          Registration           #
# # # # # # # # # # # # # # # # # #

classes = (
    # Properties
    
    # Operators
    SetOrientationToObjectOperator,
    SetOrientationToVerticesOperator,
    
    # Panels
    OrientationPanel,
    
)

def register():
    
    # Register classes
    for c in classes:
        bpy.utils.register_class(c)
    
    # Set Properties

def unregisert():
    
    # Delete Properties
    
    # Unregister classes
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()