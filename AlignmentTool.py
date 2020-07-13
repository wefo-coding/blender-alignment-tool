# # # # # # # # # # # # # # # # # #
#         Alignment Tool          #
#        for Blender 2.80         #
#        by Florian Otten         #
# # # # # # # # # # # # # # # # # #

bl_info = {
    "name": "Alignment Tool",
    "description": "Tool for aligning objects and profiles in Blender.",
    "author": "Florian Otten",
    "version": (0, 5),
    "blender": (2, 82, 0),
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
import bmesh
import math
from mathutils import *
from math import *

# # # # # # # # # # # # # # # # # #
#            Functions            #
# # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # #
#           Properties            #
# # # # # # # # # # # # # # # # # #

class AlignProps(bpy.types.PropertyGroup):
    # Profile (Mesh)
    mesh_profile: bpy.props.PointerProperty(
        type = bpy.types.Mesh,
        name = "Mesh",
        description = "The profile to be used for the angles"
    )
    # Profile (Curve)
    curve_profile: bpy.props.PointerProperty(
        type = bpy.types.Curve,
        name = "Curve",
        description = "The profile to be used for the angles"
    )


# # # # # # # # # # # # # # # # # #
#            Operators            #
# # # # # # # # # # # # # # # # # #

class SetOrientationToObjectOperator(bpy.types.Operator):
    """Align the transformation axes to the active object"""
    bl_idname = "align.set_orientation_to_object"
    bl_label = "to active object"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    
    # Methods
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        obj_src = context.active_object
        
        bpy.ops.transform.create_orientation(name = "Align", use = True, overwrite = True)
        return {'FINISHED'}

#ToDo: Copied from align_to_vertices. Create a function to avoid duplicated code
class SetOrientationToVerticesOperator(bpy.types.Operator):
    """Align the transformation axes to the selected vertices"""
    bl_idname = "align.set_orientation_to_vertices"
    bl_label = "to vertices"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    inverse: bpy.props.BoolProperty(
        name = "Inverse",
        default = False,
        description = "Inverse the alignment of the Z-axis"
    )
    
    # Properties
    select: bpy.props.BoolProperty(
        name = "Select Orientation",
        default = True,
        description = "Set transformation orientation to 'Align'"
    )
    
    # Methods
    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None and
            context.active_object.type == 'MESH'
        )
    
    def execute(self, context):
        
        error_msg = ""
        
        # Store and set modes
        obj = context.active_object
        mode = obj.mode
        bpy.ops.object.mode_set(mode='EDIT')
        selection_mode = context.tool_settings.mesh_select_mode
        bpy.ops.mesh.select_mode(type='VERT', action='ENABLE')
        selected = obj.select_get()
        orientation = context.scene.transform_orientation_slots[0].type
        
        # Get orientation matrix
        bm = bmesh.from_edit_mesh(obj.data)
        
        if(len(bm.select_history) != 3):
            error_msg = "Please make sure that you have selected exactly three vertices from the active object (manually vertex by vertex)."
        else:
            # Get Vertices
            if(self.inverse):
                coord_start = bm.select_history[2].co
                coord_center = bm.select_history[1].co
                coord_end = bm.select_history[0].co
            else:
                coord_start = bm.select_history[0].co
                coord_center = bm.select_history[1].co
                coord_end = bm.select_history[2].co
            
            # Get global coordinates
            coord_start = obj.matrix_world @ coord_start
            coord_center = obj.matrix_world @ coord_center
            coord_end = obj.matrix_world @ coord_end
            
            # Get coordinates of a vertex on Z-Axis
            # coord_center to coord_end is Z-Axis so coord_end is a vertex on the Z-Axis
            coord_z = coord_end
            
            # Get coordinates of a vertex on Y-Axis
            coord_y = (coord_start - coord_center).cross(coord_z - coord_center) + coord_center
            
            # Get coordinates of a vertex on X-Axis
            coord_x = (coord_y - coord_center).cross(coord_z - coord_center) + coord_center
            
            # Get vectors
            vector_x = coord_x - coord_center
            vector_y = coord_y - coord_center
            vector_z = coord_z - coord_center
            
            vector_x.normalize()
            vector_y.normalize()
            vector_z.normalize()
            
            # Build matrix
            matrix = Matrix([
                [vector_x[0], vector_y[0], vector_z[0]],
                [vector_x[1], vector_y[1], vector_z[1]],
                [vector_x[2], vector_y[2], vector_z[2]]
            ]) 
            
            # Set Orientation
            bpy.ops.transform.select_orientation(orientation="Align")
            context.scene.transform_orientation_slots[0].custom_orientation.matrix = matrix
        
        # Reset modes
        if(not self.select):
            bpy.ops.transform.select_orientation(orientation=orientation)
        use_extend = False
        for i in range(3):
            if(i == 0):
                type = 'VERT'
            elif(i == 1):
                type = 'EDGE'
            else:
                type = 'FACE'
            if(selection_mode[i]):
                bpy.ops.mesh.select_mode(use_extend=use_extend, type=type, action='ENABLE')
                use_extend=True
        bpy.ops.object.mode_set(mode=mode)
        
        if(error_msg == ""):
            return {'FINISHED'}
        
        self.report({'ERROR'}, error_msg)
        return {'CANCELLED'}

class AlignToOrientationOperator(bpy.types.Operator):
    """Align selected objects"""
    bl_idname = "align.align_to_orientation"
    bl_label = "to orientation"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    
    # Methods
    def execute(self, context):
        
        bpy.ops.transform.transform(mode='ALIGN')
        
        return {'FINISHED'}

class AlignToObjectOperator(bpy.types.Operator):
    """Align selected objects to active object"""
    bl_idname = "align.align_to_object"
    bl_label = "to active object"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    
    move: bpy.props.BoolProperty(
        name = "Move",
        default = True,
        description = "Move the object to active object"
    )
    
    # Methods
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and (
            len(context.selected_objects) > 1 or (
                len(context.selected_objects) == 1 and
                not context.active_object.select_get()
            )
        )
    
    def execute(self, context):
        
        # Store and set modes
        obj = context.active_object
        mode = obj.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        selected = obj.select_get()
        
        # Set orientation to active object
        bpy.ops.align.set_orientation_to_object()
        
        # Align selected objects
        obj.select_set(False)
        bpy.ops.transform.transform(mode='ALIGN')
        
        # Move selected objects
        if(self.move):
            for selected_obj in context.selected_objects:
                selected_obj.location = obj.location
                
        # Reset modes
        obj.select_set(selected)
        bpy.ops.object.mode_set(mode=mode)
        
        return {'FINISHED'}

class AlignToVerticesOperator(bpy.types.Operator):
    """Align selected objects to selected vertices of the active object"""
    bl_idname = "align.align_to_vertices"
    bl_label = "to vertices"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    inverse: bpy.props.BoolProperty(
        name = "Inverse",
        default = False,
        description = "Inverse the alignment of the Z-axis"
    )
    
    move: bpy.props.BoolProperty(
        name = "Move",
        default = True,
        description = "Move the object to selected vertices"
    )
    
    # Methods
    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None and
            context.active_object.type == 'MESH' and
            len(context.selected_objects) > 1
        )
        
    def execute(self, context):
        
        error_msg = ""
        
        # Store and set modes
        obj = context.active_object
        mode = obj.mode
        bpy.ops.object.mode_set(mode='EDIT')
        selection_mode = context.tool_settings.mesh_select_mode
        bpy.ops.mesh.select_mode(type='VERT', action='ENABLE')
        selected = obj.select_get()
        
        # Get orientation matrix
        bm = bmesh.from_edit_mesh(obj.data)
        
        if(len(bm.select_history) != 3):
            error_msg = "Please make sure that you have selected exactly three vertices from the active object (manually vertex by vertex)."
        else:
            # Get Vertices
            if(self.inverse):
                coord_start = bm.select_history[2].co
                coord_center = bm.select_history[1].co
                coord_end = bm.select_history[0].co
            else:
                coord_start = bm.select_history[0].co
                coord_center = bm.select_history[1].co
                coord_end = bm.select_history[2].co
            
            # Get global coordinates
            coord_start = obj.matrix_world @ coord_start
            coord_center = obj.matrix_world @ coord_center
            coord_end = obj.matrix_world @ coord_end
            
            # Get coordinates of a vertex on Z-Axis
            # coord_center to coord_end is Z-Axis so coord_end is a vertex on the Z-Axis
            coord_z = coord_end
            
            # Get coordinates of a vertex on Y-Axis
            coord_y = (coord_start - coord_center).cross(coord_z - coord_center) + coord_center
            
            # Get coordinates of a vertex on X-Axis
            coord_x = (coord_y - coord_center).cross(coord_z - coord_center) + coord_center
            
            # Get vectors
            vector_x = coord_x - coord_center
            vector_y = coord_y - coord_center
            vector_z = coord_z - coord_center
            
            vector_x.normalize()
            vector_y.normalize()
            vector_z.normalize()
            
            # Build matrix
            matrix = Matrix([
                [vector_x[0], vector_y[0], vector_z[0]],
                [vector_x[1], vector_y[1], vector_z[1]],
                [vector_x[2], vector_y[2], vector_z[2]]
            ]) 
        
        # Reset selection mode
        use_extend = False
        for i in range(3):
            if(i == 0):
                type = 'VERT'
            elif(i == 1):
                type = 'EDGE'
            else:
                type = 'FACE'
            if(selection_mode[i]):
                bpy.ops.mesh.select_mode(use_extend=use_extend, type=type, action='ENABLE')
                use_extend=True
        
        # Align objects
        if(error_msg == ""):
            bpy.ops.object.mode_set(mode='OBJECT')
            obj.select_set(False)
            bpy.ops.transform.transform(mode='ALIGN', orient_matrix=matrix)
            if(self.move):
                for selected_obj in context.selected_objects:
                    #TODO does not work for child-objects
                    selected_obj.location = coord_center
            obj.select_set(selected)
        
        # Reset mode
        bpy.ops.object.mode_set(mode=mode)
        
        if(error_msg == ""):
            return {'FINISHED'}
        
        self.report({'ERROR'}, error_msg)
        return {'CANCELLED'}

class AlignToCurveOperator(bpy.types.Operator):
    """Coming soon: Align selected objects to the curve"""
    bl_idname = "align.align_to_curve"
    bl_label = "to curve"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    move: bpy.props.FloatProperty(
        name = "Move",
        default = 0,
        description = "Move the object along the curve"
    )
    
    # Methods
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'CURVE' and False
    
    def execute(self, context):
        
        return {'FINISHED'}
    
class AngleFromMeshOperator(bpy.types.Operator):
    """Coming soon: Create an angle from a mesh."""
    bl_idname = "align.angle_from_mesh"
    bl_label = "from mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    
    # Methods
    @classmethod
    def poll(cls, context):
        return False
    
    def execute(self, context):
        return {'FINISHED'}
    
class AngleFromCurveOperator(bpy.types.Operator):
    """Coming soon: Create an angle from a curve."""
    bl_idname = "align.angle_from_curve"
    bl_label = "from curve"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    
    # Methods
    @classmethod
    def poll(cls, context):
        return False
    
    def execute(self, context):
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
        layout.label(text="Orientation:")
        layout.operator(SetOrientationToObjectOperator.bl_idname)
        layout.operator(SetOrientationToVerticesOperator.bl_idname)
        layout.label(text="Align:")
        layout.operator(AlignToOrientationOperator.bl_idname)
        layout.operator(AlignToObjectOperator.bl_idname)
        layout.operator(AlignToVerticesOperator.bl_idname)
        layout.operator(AlignToCurveOperator.bl_idname)

class AnglePanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_angle"
    bl_label = "Angle"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Align"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Create angle")
        box = layout.box()
        box.prop(context.scene.align, "mesh_profile", text="Profile")
        box.operator(AngleFromMeshOperator.bl_idname)
        box = layout.box()
        box.prop(context.scene.align, "curve_profile", text="Profile")
        box.operator(AngleFromCurveOperator.bl_idname)


# # # # # # # # # # # # # # # # # #
#          Registration           #
# # # # # # # # # # # # # # # # # #

classes = (
    # Properties
    AlignProps,
    
    # Operators
    SetOrientationToObjectOperator,
    SetOrientationToVerticesOperator,
    AlignToOrientationOperator,
    AlignToObjectOperator,
    AlignToVerticesOperator,
    AlignToCurveOperator,
    AngleFromMeshOperator,
    AngleFromCurveOperator,
    
    # Panels
    OrientationPanel,
    AnglePanel
    
)

def register():
    
    # Register classes
    for c in classes:
        bpy.utils.register_class(c)
    
    # Set Properties
    bpy.types.Scene.align = bpy.props.PointerProperty(type = AlignProps)

def unregisert():
    
    # Delete Properties
    del bpy.types.Scene.align
    
    # Unregister classes
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()