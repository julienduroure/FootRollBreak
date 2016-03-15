##########################################################################################
#	GPL LICENSE:
#-------------------------
# This file is part of FootRollBreak.
#
#    FootRollBreak is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    FootRollBreak is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with FootRollBreak.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################################
#
#	Copyright 2015 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################

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
			#should'nt happen because of poll of UI panel, but just in case ... error message
			self.report({'ERROR'}, error_message)
			return {'CANCELLED'}

def register():
	bpy.utils.register_class(PatchRigify)
	
def unregister():
	bpy.utils.unregister_class(PatchRigify)
