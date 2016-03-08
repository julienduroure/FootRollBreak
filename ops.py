import bpy

from .globals import *
from .patch_human import *
from .patch_pitchipoy import *

class PatchRigify(bpy.types.Operator):
	bl_idname = "pose.patch_rigify"
	bl_label  = "Patch Rigify to add FootRoll Break"
	bl_options = {'REGISTER'}	

	@classmethod
	def poll(cls, context):
		return context.active_object.type == 'ARMATURE' 	
		
	def execute(self, context):
		obj = context.active_object
		rigify_type = check_rigify_type(obj)
		if rigify_type == 'Human':
			return exec_patch_human(addonpref().human_complexity)
		elif rigify_type == 'Pitchipoy':
			return exec_patch_pitchipoy(addonpref().pitchipoy_complexity)
		else: 
			pass #TODO message unknown

def register():
	bpy.utils.register_class(PatchRigify)
	
def unregister():
	bpy.utils.unregister_class(PatchRigify)
