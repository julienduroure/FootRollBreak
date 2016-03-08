import bpy

from .globals import *

class DATA_PT_rigify_patch(bpy.types.Panel):
	bl_label = "Rigify FootRoll Break Patch"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "data"

	@classmethod
	def poll(cls, context):
		if not context.armature:
			return False
		return check_rigify_type(context.active_object) in available

	def draw(self, context):
		if not is_already_patched(context.active_object):
			op = self.layout.operator("pose.patch_rigify", text="Patch FootRoll Break").human_complexity = addonpref().human_complexity
			if addonpref().debug == True:
				self.layout.label("detected type : ", icon="INFO")
				self.layout.label(check_rigify_type(context.active_object))
		else:
			self.layout.label("already patched!", icon="INFO")
			
def register():
	bpy.utils.register_class(DATA_PT_rigify_patch)
	
def unregister():
	bpy.utils.unregister_class(DATA_PT_rigify_patch)
