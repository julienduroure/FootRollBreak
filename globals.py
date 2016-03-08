import bpy

available = ['Human','Pitchipoy']

human_complexity_items = [
		("DRIVER", "Driver", "", 1),
		("CONSTRAINT", "Constraint", "", 2),
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

name_intermediate_roll = "ORG-foot_roll.ik"
name_toe_top           = "toe-top"

name_footrollbreak_angle = 	"footrollbreak_angle"

default_footrollbreak_angle = 50.0
default_footrollbreak       = False
default_human_complexity = "DRIVER"
default_pitchipoy_complexity = "CONSTRAINT"

def addonpref():
	user_preferences = bpy.context.user_preferences
	return user_preferences.addons[__package__].preferences
