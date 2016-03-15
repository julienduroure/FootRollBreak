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

class RigifyPatchPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__
	
	debug = bpy.props.BoolProperty(default= False)
	
	human_complexity = bpy.props.EnumProperty(items=human_complexity_items, default=default_human_complexity)
	pitchipoy_complexity = bpy.props.EnumProperty(items=pitchipoy_complexity_items, default=default_pitchipoy_complexity)
	
	def draw(self, context):
		layout = self.layout
		row_global    = layout.row()
		
		col = row_global.column()
		row = col.row()
		row.prop(self, "debug", text="Debug mode")
		col = row_global.column()
		if self.debug == True:
			row    = col.row()
			row.prop(self, "human_complexity", text="Human complexity")
			row    = col.row()
			row.prop(self, "pitchipoy_complexity", text="Pitchipoy complexity")
		
		
		
		
def register():
	bpy.utils.register_class(RigifyPatchPreferences)
	
def unregister():
	bpy.utils.unregister_class(RigifyPatchPreferences)