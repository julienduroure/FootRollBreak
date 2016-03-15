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

available = ['Human','Pitchipoy']

human_complexity_items = [
		("DRIVER", "Driver", "", 1),
		("CONSTRAINT", "Constraint", "", 2),
		("FULL", "Full", "", 3),
		]
		
pitchipoy_complexity_items = [
		("CONSTRAINT", "Constraint", "", 1),
		("FULL", "Full", "", 2),
		]
		
		
def check_rigify_type(obj):
	human = "MCH-foot.L.roll.01"
	pitchipoy = "MCH-heel.02_roll.L.001"
	if human in obj.data.bones:
		return 'Human'
	elif pitchipoy in obj.data.bones:
		return 'Pitchipoy'
	else:
		return 'UNKNOWN'

def is_already_patched(obj):
	bone = "ORG-foot_roll.ik.L" #This is a bone addon will add. If already here --> Rig is already patched
	return bone in obj.data.bones

#any modification on this function must be duplicate on ui_texts
#Here, this function is only used by debug system to display length coeff
#Real use of this function is on ui_texts, that is unsed into driver function
def get_length_coeff(obj, side, toe_def, foot_def, toe_top):
	return  (obj.bones[toe_def + side].matrix_local.to_translation() - obj.bones[toe_top + side ].matrix_local.to_translation()).length / (obj.bones[foot_def + side].matrix_local.to_translation() - obj.bones[toe_def + side].matrix_local.to_translation()).length
    
#Some names of created bones & properties
name_intermediate_roll = "ORG-foot_roll.ik"
name_toe_top           = "toe-top"

name_footrollbreak_angle = 	"footrollbreak_angle"
name_footrollbreak_angle_max = 	"footrollbreak_angle_max"
name_corrective_return_angle = "footrollbreak_corrective_angle"

name_rig_ui_text = "rig_ui.py"

#Some default values
default_footrollbreak_angle = 50.0
default_footrollbreak_angle_max = 90.0
default_corrective_return_angle = 0.0
default_footrollbreak       = False
default_footrollbreak_return = True
default_human_complexity = "FULL"
default_pitchipoy_complexity = "FULL"

#Coeff used by compensate rotation during return (full method)
a = 1.00366
b = -0.68879
c = 0.21013
d = -0.0265

#shortcut to prefs
def addonpref():
	user_preferences = bpy.context.user_preferences
	return user_preferences.addons[__package__].preferences
	
#Error message display
error_message = "Unknown Rigify MetaRig"
