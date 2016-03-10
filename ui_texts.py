ui_text = '''
import bpy

rig_id = ###rig_id###

class FootRollBreakUI(bpy.types.Panel):

	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "FootRoll Break"
	bl_idname = rig_id + "_PT_FootRollBreak_ui"


	@classmethod
	def poll(self, context):
		if context.mode != 'POSE':
			return False

		try:
			return (context.active_object.data.get("rig_id") == rig_id)
		except (AttributeError, KeyError, TypeError):
			return False
		

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		row = col.row()
		row.prop(context.active_object.pose.bones["###bone###.L"], "footrollbreak", text="FootRoll Break (L)") 

		if context.active_object.pose.bones["###bone###.L"].footrollbreak == True:
			if context.active_object.pose.bones["###bone_roll###.L"]["complexity"] == "FULL":
				row = col.row()
				row.prop(context.active_object.pose.bones["###bone###.L"], '["footrollbreak_angle"]', text="Angle")
				row.prop(context.active_object.pose.bones["###bone###.L"], '["footrollbreak_angle_max"]', text="Angle Max")
			else:
				row.prop(context.active_object.pose.bones["###bone###.L"], '["footrollbreak_angle"]', text="Angle")
		
		row = col.row()

		row.prop(context.active_object.pose.bones["###bone###.R"], "footrollbreak", text="FootRoll Break (R)") 
		if context.active_object.pose.bones["###bone###.R"].footrollbreak == True:
			if context.active_object.pose.bones["###bone_roll###.R"]["complexity"] == "FULL":
				row = col.row()
				row.prop(context.active_object.pose.bones["###bone###.R"], '["footrollbreak_angle"]', text="Angle")
				row.prop(context.active_object.pose.bones["###bone###.R"], '["footrollbreak_angle_max"]', text="Angle Max")
			else:
				row.prop(context.active_object.pose.bones["###bone###.R"], '["footrollbreak_angle"]', text="Angle")
		
		

def register():
	bpy.utils.register_class(FootRollBreakUI)
	
def unregister():
	bpy.utils.unregister_class(FootRollBreakUI)

	
	
register()
'''

text_drivers = '''
import bpy
import math
import mathutils

def get_length_coeff(obj, side, toe_def, foot_def, toe_top):
	return (obj.bones[toe_def + side].matrix_local.to_translation() - obj.bones[toe_top + side ].matrix_local.to_translation()).length / (obj.bones[foot_def + side].matrix_local.to_translation() - obj.bones[toe_def + side].matrix_local.to_translation()).length

def driver_rollbreak(current_angle, angle, angle_max):
    if current_angle <= angle:
        return angle*2* math.pi/360
    elif current_angle >= angle and current_angle < angle_max:
        return (- angle / ( angle_max - angle ) * ( current_angle - angle_max) * 2 * math.pi / 360)
    else:
        return 0.0

def driver_rollbreak_return(side, angle, corrective):
    obj = bpy.data.armatures["###armature###"]
    a = ###a###
    b = ###b###
    c = ###c###
    d = ###d###
    coeff_length =   get_length_coeff(obj, side, "###toe_def###", "###foot_def###", "###toe_top###")
    slop         = a + b*coeff_length + c*coeff_length*coeff_length + d*coeff_length*coeff_length*coeff_length
    return (angle + corrective) * slop * 2 *math.pi / 360

bpy.app.driver_namespace["driver_rollbreak"] = driver_rollbreak
bpy.app.driver_namespace["driver_rollbreak_return"] = driver_rollbreak_return

'''
