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
        layout.label(text="Alignment tool test")


# # # # # # # # # # # # # # # # # #
#          Registration           #
# # # # # # # # # # # # # # # # # #

classes = (
    # Properties
    
    # Operators
    
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
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    
    # Unregister classes

if __name__ == "__main__":
    register()