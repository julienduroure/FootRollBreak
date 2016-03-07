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
			row.prop(context.active_object.pose.bones["###bone###.L"], '["footrollbreak_angle"]', text="Angle")
		
		row = col.row()

		row.prop(context.active_object.pose.bones["###bone###.R"], "footrollbreak", text="FootRoll Break (R)") 
		if context.active_object.pose.bones["###bone###.R"].footrollbreak == True:
			row.prop(context.active_object.pose.bones["###bone###.R"], '["footrollbreak_angle"]', text="Angle")
		
		

def register():
	bpy.utils.register_class(FootRollBreakUI)
	
def unregister():
	bpy.utils.unregister_class(FootRollBreakUI)

	
	
register()
'''