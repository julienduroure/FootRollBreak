bl_info = {
	"name": "Add Roll Break to Rigify",
	"author": "Julien Duroure",
	"version": (0, 0, 1),
	"blender": (2,77, 0),
	"description": "Add Roll Break to Rigify",
	"category": "Rigging",   
}

#TODO implement patch_pitchipoy
#TODO replace slider by checkbox
#TODO RollBreak, rollbreak, rollBreak, Roll Break, etc... : choose how to write it, and change label, class names, etc...

import bpy
from mathutils import Vector
import math

available = ['Human','Pitchipoy']


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

def new_bone(obj, bone_name):
	new_ = obj.data.edit_bones.new(bone_name)
	new_name = new_.name
	new_.head = (0,0,0)
	new_.tail = (0,1,0)
	new_.roll = 0
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.mode_set(mode='EDIT')
	return new_name
			
def copy_layer(obj, source_name, target_name):
	obj.data.edit_bones[target_name].layers = obj.data.edit_bones[source_name].layers

def copy_custom_shape(obj, source_name, target_name):
	bpy.ops.object.mode_set(mode='OBJECT')
	obj.pose.bones[target_name].custom_shape = obj.pose.bones[source_name].custom_shape
	bpy.ops.object.mode_set(mode='EDIT')
			
def copy_rotation_mode(obj, source_name, target_name):
	bpy.ops.object.mode_set(mode='POSE')
	obj.pose.bones[target_name].rotation_mode = obj.pose.bones[source_name].rotation_mode
	bpy.ops.object.mode_set(mode='EDIT')

def def_geo(obj, bone_name, head, tail, roll):
	obj.data.edit_bones[bone_name].head = head
	obj.data.edit_bones[bone_name].tail = tail
	obj.data.edit_bones[bone_name].roll = roll

class DATA_PT_rigify_patch(bpy.types.Panel):
	bl_label = "Rigify RollBreak Patch"
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
			self.layout.operator("pose.patch_rigify", text="Patch RollBreak")
			self.layout.label("detected type : ", icon="INFO")
			self.layout.label(check_rigify_type(context.active_object))
		else:
			self.layout.label("already patched!", icon="INFO")
					
			

class PatchRigify(bpy.types.Operator):
	bl_idname = "pose.patch_rigify"
	bl_label  = "Patch Rigify to add Roll Break"	
	
	@classmethod
	def poll(cls, context):
		return context.active_object.type == 'ARMATURE' 	
		
	def execute(self, context):
		obj = context.active_object
		rigify_type = check_rigify_type(obj)
		if rigify_type == 'Human':
			return self.patch_human(context)
		elif rigify_type == 'Pitchipoy':
			return self.patch_pitchipoy(context)
		else: 
			pass #TODO message unknown

	def patch_pitchipoy(self, context):
		# Force to be in edit mode
		start_mode = bpy.context.mode
		if bpy.context.mode != "EDIT_ARMATURE":
			bpy.ops.object.mode_set(mode='EDIT')

		obj = bpy.context.active_object

		bpy.ops.object.mode_set(mode=start_mode)

		return {'FINISHED'}
		
	def patch_human(self, context):
		# Force to be in edit mode
		start_mode = bpy.context.mode
		if bpy.context.mode != "EDIT_ARMATURE":
			bpy.ops.object.mode_set(mode='EDIT')
		   
		obj = bpy.context.active_object   
		toe_name  = "ORG-toe"
		foot_name = "foot.ik"
		roll_name = "foot_roll.ik"
		internal_roll_01 = "MCH-foot"
		internal_roll_02 = ".rocker.01"
		driver_01_01 = "MCH-foot"
		driver_01_02 = ".roll.01"
		driver_02_01 = "MCH-foot"
		driver_02_02 = ".roll.02"
			
			   
		for side in [".L", ".R"]:
			# Top toe bone
			top = new_bone(obj, "toe-top" + side)
			def_geo(obj, top, obj.data.edit_bones[toe_name+side].tail,
							  Vector((obj.data.edit_bones[toe_name+side].tail[0],obj.data.edit_bones[toe_name+side].tail[1],obj.data.edit_bones[foot_name+side].tail[2])),
							  0)
			copy_layer(obj, roll_name + side, top)
			copy_custom_shape(obj, roll_name + side, top)
			
			
			# new intermediate roll bone
			new_roll_name = new_bone(obj, "ORG-foot_roll.ik"+side)
			def_geo(obj, new_roll_name, obj.data.edit_bones[roll_name+side].head, obj.data.edit_bones[roll_name+side].tail, obj.data.edit_bones[roll_name+side].roll)
			copy_layer(obj, internal_roll_01 + side + internal_roll_02, new_roll_name)
			copy_rotation_mode(obj, roll_name + side, new_roll_name)
			
			#change rotation mode of top
			copy_rotation_mode(obj, new_roll_name, top)
			
			#change parenting
			obj.data.edit_bones[top].parent = obj.data.edit_bones[foot_name + side]
			obj.data.edit_bones[new_roll_name].parent = obj.data.edit_bones[top]
			obj.data.edit_bones[internal_roll_01 + side + internal_roll_02].parent = obj.data.edit_bones[top]

			#create custom properties
			bpy.context.active_object.pose.bones[foot_name+side]["_RNA_UI"]['footbreak'] = {"min":0.0, "max":180.0}
			bpy.context.active_object.pose.bones[foot_name+side]["footbreak"] = 50.0
			bpy.context.active_object.pose.bones[foot_name+side]["_RNA_UI"]['footbreak_onoff'] = {"min":0, "max":1}
			bpy.context.active_object.pose.bones[foot_name+side]["footbreak_onoff"] = True

			#add constraint to top
			bpy.ops.object.mode_set(mode='POSE')
			bpy.ops.pose.select_all(action='DESELECT')
			obj.data.bones[top].select = True
			obj.data.bones.active = obj.data.bones[top]
			transform = obj.pose.bones[top].constraints.new(type='TRANSFORM')
			transform.target = obj
			transform.subtarget = roll_name + side
			transform.map_from = 'ROTATION'
			transform.from_max_x_rot = math.pi
			transform.map_to = 'ROTATION'
			transform.target_space = 'LOCAL'
			transform.owner_space = 'LOCAL'
			
			limit = obj.pose.bones[top].constraints.new(type='LIMIT_ROTATION')
			limit.use_limit_x = True
			limit.max_x 	  = math.pi / 2
			limit.owner_space = 'LOCAL'
			
			bpy.ops.pose.select_all(action='DESELECT')
			obj.data.bones[new_roll_name].select = True
			obj.data.bones.active = obj.data.bones[new_roll_name]
			copy_rot = obj.pose.bones[new_roll_name].constraints.new(type='COPY_ROTATION')
			copy_rot.target = obj
			copy_rot.subtarget = roll_name + side
			copy_rot.use_x = False
			copy_rot.target_space = 'LOCAL'
			copy_rot.owner_space = 'LOCAL'
			
			#change existing drivers
			for driv in obj.animation_data.drivers:
				if driv.data_path == "pose.bones[\"" + driver_01_01 + side + driver_01_02 + "\"].rotation_euler" and driv.array_index == 0:
					driv.driver.variables[0].targets[0].data_path = "pose.bones[\"" + new_roll_name + "\"].rotation_euler[0]"
				elif driv.data_path == "pose.bones[\"" + driver_02_01 + side + driver_02_02 + "\"].rotation_euler" and driv.array_index == 0:
					driv.driver.variables[0].targets[0].data_path = "pose.bones[\"" + new_roll_name + "\"].rotation_euler[0]"
					
			# create new drivers
			fcurve = obj.pose.bones[new_roll_name].driver_add('rotation_euler' ,0)
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "min(var_break*2*pi/360,var) if var_onoff == True else var"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + roll_name + side + "\"].rotation_euler[0]"
			var = drv.variables.new()
			var.name = 'var_break'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"footbreak\"]"
			var = drv.variables.new()
			var.name = 'var_onoff'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"footbreak_onoff\"]"
			
			
				
			fcurve = obj.pose.bones[top].constraints[0].driver_add('from_min_x_rot')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "var*2*pi/360"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"footbreak\"]"

			fcurve = obj.pose.bones[top].constraints[0].driver_add('to_max_x_rot')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "(180-var)*2*pi/360"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"footbreak\"]"

			fcurve = obj.pose.bones[top].constraints[0].driver_add('influence')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "var"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"footbreak_onoff\"]"


					
			bpy.ops.object.mode_set(mode='EDIT')
			
		bpy.ops.object.mode_set(mode=start_mode)

		# add UI
		ui_text = '''
import bpy

rig_id = ###rig_id###

class FootBreakUI(bpy.types.Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "Foot Break"
	bl_idname = rig_id + "_PT_footbreak_ui"

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
		row.prop(context.active_object.pose.bones["foot.ik.L"], '["footbreak_onoff"]', text="Roll break (L)") 
		if context.active_object.pose.bones["foot.ik.L"]["footbreak_onoff"] == True:
			row.prop(context.active_object.pose.bones["foot.ik.L"], '["footbreak"]', text="Angle")
		
		row = col.row()
		row.prop(context.active_object.pose.bones["foot.ik.R"], '["footbreak_onoff"]', text="Roll break (R)") 
		if context.active_object.pose.bones["foot.ik.R"]["footbreak_onoff"] == True:
			row.prop(context.active_object.pose.bones["foot.ik.R"], '["footbreak"]', text="Angle")
		
		
def register():
	bpy.utils.register_class(FootBreakUI)
	
def unregister():
	bpy.utils.unregister_class(FootBreakUI)
	
	
register()
'''

		ui_text = ui_text.replace("###rig_id###", "\"" + obj.data["rig_id"] + "\"")

		text = bpy.data.texts.new(name="rollbreakUI.py")
		text.use_module = True
		text.write(ui_text)
		exec(text.as_string(), {})
		return {'FINISHED'}
		
		
def register():
	bpy.utils.register_class(PatchRigify)
	bpy.utils.register_class(DATA_PT_rigify_patch)
	
def unregister():
	bpy.utils.unregister_class(PatchRigify)
	bpy.utils.unregister_class(DATA_PT_rigify_patch)
		
if __name__ == "__main__":
	register()
