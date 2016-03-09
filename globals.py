import bpy

available = ['Human','Pitchipoy']

human_complexity_items = [
		("DRIVER", "Driver", "", 1),
		("CONSTRAINT", "Constraint", "", 2),
		("FULL", "Full", "", 3),
		]
		
pitchipoy_complexity_items = [
		("CONSTRAINT", "Constraint", "", 1),
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
	bone = "ORG-foot_roll.ik.L"
	return bone in obj.data.bones

#any modification on this function must be duplicate on ui_texts
def get_length_coeff(obj, side, toe_def, foot_def, toe_top):
	return  (obj.bones[toe_def + side].matrix_local.to_translation() - obj.bones[toe_top + side ].matrix_local.to_translation()).length / (obj.bones[foot_def + side].matrix_local.to_translation() - obj.bones[toe_def + side].matrix_local.to_translation()).length
    
name_intermediate_roll = "ORG-foot_roll.ik"
name_toe_top           = "toe-top"

name_footrollbreak_angle = 	"footrollbreak_angle"
name_footrollbreak_angle_max = 	"footrollbreak_angle_max"

default_footrollbreak_angle = 50.0
default_footrollbreak_angle_max = 90.0
default_footrollbreak       = False
default_human_complexity = "DRIVER"
default_pitchipoy_complexity = "CONSTRAINT"


a = 1.00366
b = -0.68879
c = 0.21013
d = -0.0265

def addonpref():
	user_preferences = bpy.context.user_preferences
	return user_preferences.addons[__package__].preferences
