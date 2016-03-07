available = ['Human','Pitchipoy']

human_complexity_items = [
		("DRIVER", "Driver", "", 1),
		("CONSTRAINT", "Constraint", "", 2),
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