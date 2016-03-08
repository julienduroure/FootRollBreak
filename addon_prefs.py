import bpy

from .globals import *

class RigifyPatchPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__
	
	debug = bpy.props.BoolProperty(default= False)
	
	human_complexity = bpy.props.EnumProperty(items=human_complexity_items, default=default_human_complexity)
	pitchipoy_complexity = bpy.props.EnumProperty(items=pitchipoy_complexity_items, default=default_pitchipoy_complexity)
	
	def draw(self, context):
		layout = self.layout
		row_global    = layout.row()
		
		col = row_global.column()
		row    = col.row()
		row.prop(self, "human_complexity", text="Human complexity")
		row    = col.row()
		row.prop(self, "pitchipoy_complexity", text="Pitchipoy complexity")
		col = row_global.column()
		row = col.row()
		row.prop(self, "debug", text="Debug mode")
		
		
		
def register():
	bpy.utils.register_class(RigifyPatchPreferences)
	
def unregister():
	bpy.utils.unregister_class(RigifyPatchPreferences)