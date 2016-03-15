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
			op = self.layout.operator("pose.patch_rigify", text="Patch FootRoll Break")
			if addonpref().debug == True:
				row = self.layout.row()
				row.label("detected type : ")
				row.label(check_rigify_type(context.active_object))
				
				row = self.layout.row()
				if check_rigify_type(context.active_object) == "Human":
					row.label("complexity mode : ")
					row.label(addonpref().human_complexity)
				elif check_rigify_type(context.active_object) == "Pitchipoy":
					row.label("complexity mode : ")
					row.label(addonpref().pitchipoy_complexity)					
		else:
			self.layout.label("already patched!", icon="INFO")
			if addonpref().debug == True:
				row = self.layout.row()
				row.label("length factor L:")
				row = self.layout.row()
				row.label(str(get_length_coeff(bpy.context.active_object.data, ".L", "ORG-toe", "DEF-foot", name_toe_top)))
				row = self.layout.row()
				row.label("length factor R:")
				row = self.layout.row()
				row.label(str(get_length_coeff(bpy.context.active_object.data, ".R", "ORG-toe", "DEF-foot", name_toe_top)))
			
def register():
	bpy.utils.register_class(DATA_PT_rigify_patch)
	
def unregister():
	bpy.utils.unregister_class(DATA_PT_rigify_patch)
