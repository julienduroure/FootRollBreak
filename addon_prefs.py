import bpy

from .globals import *

class RigifyPatchPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__
	
	debug = bpy.props.BoolProperty(default= False)
	
	human_complexity = bpy.props.EnumProperty(items=human_complexity_items, default=default_complexity)
	
	def draw(self, context):
		layout = self.layout
		row_global    = layout.row()
		
		col = row_global.column()
		row = col.row()
		row.prop(self, "debug", text="Debug mode")
		row    = layout.row()
		row.prop(self, "human_complexity", text="Human complexity")
		
def register():
	bpy.utils.register_class(RigifyPatchPreferences)
	
def unregister():
	bpy.utils.unregister_class(RigifyPatchPreferences)