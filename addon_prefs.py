import bpy

class RigifyPatchPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__
	
	debug = bpy.props.BoolProperty(default= False)
	
	def draw(self, context):
		layout = self.layout
		row    = layout.row()
		row.prop(self, "debug", text="Debug mode")
		
def register():
	bpy.utils.register_class(RigifyPatchPreferences)
	
def unregister():
	bpy.utils.unregister_class(RigifyPatchPreferences)