bl_info = {
	"name": "Add Roll Break to Rigify",
	"author": "Julien Duroure",
	"version": (0, 0, 1),
	"blender": (2,77, 0),
	"description": "Add Roll Break to Rigify",
	"category": "Rigging",   
}

import bpy
from mathutils import Vector
import math

available = ['Human','Pitchipoy']

complexity_items = [
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
		row.prop(context.active_object.pose.bones["###bone###.L"], "footbreak", text="Roll break (L)") 

		if context.active_object.pose.bones["###bone###.L"].footbreak == True:
			row.prop(context.active_object.pose.bones["###bone###.L"], '["footbreak_angle"]', text="Angle")
		
		row = col.row()

		row.prop(context.active_object.pose.bones["###bone###.R"], "footbreak", text="Roll break (R)") 
		if context.active_object.pose.bones["###bone###.R"].footbreak == True:
			row.prop(context.active_object.pose.bones["###bone###.R"], '["footbreak_angle"]', text="Angle")
		
		

def register():
	bpy.utils.register_class(FootBreakUI)
	
def unregister():
	bpy.utils.unregister_class(FootBreakUI)

	
	
register()
'''

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
			if check_rigify_type(context.active_object) == "Human":
                        	self.layout.prop(context.scene, "complexity")
			op = self.layout.operator("pose.patch_rigify", text="Patch RollBreak").complexity = bpy.context.scene.complexity
			self.layout.label("detected type : ", icon="INFO")
			self.layout.label(check_rigify_type(context.active_object))
		else:
			self.layout.label("already patched!", icon="INFO")
					
			

class PatchRigify(bpy.types.Operator):
	bl_idname = "pose.patch_rigify"
	bl_label  = "Patch Rigify to add Roll Break"
	bl_options = {'REGISTER'}	

	complexity = bpy.props.EnumProperty(items=complexity_items,default="DRIVER")
	
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
		global ui_text
		# Force to be in edit mode
		start_mode = bpy.context.mode
		if bpy.context.mode != "EDIT_ARMATURE":
			bpy.ops.object.mode_set(mode='EDIT')

		obj = bpy.context.active_object
		toe_name  = "ORG-toe"
		foot_name = "foot_ik"
		roll_name = "foot_heel_ik"
		internal_roll = "ORG-foot"
		constraint_01 = "MCH-heel.02_roll"
		constraint_02_01 = "MCH-heel.02_roll"
		constraint_02_02 = ".001"
		constraint_03 = "MCH-heel.02_roll"
		constraint_04_01 = "MCH-heel.02_rock"
		constraint_04_02 = ".001"
		constraint_add_name = "MCH-thigh_ik_target"
		shoulder_wgt        = "shoulder.L"

		for side in [".L", ".R"]:
			# Top toe bone
			top = new_bone(obj, "toe-top" + side)
			def_geo(obj, top, obj.data.edit_bones[toe_name+side].tail,
							  Vector((obj.data.edit_bones[toe_name+side].tail[0],obj.data.edit_bones[toe_name+side].tail[1],obj.data.edit_bones[roll_name+side].tail[2])),
							  0)
			copy_layer(obj, roll_name + side, top)
			copy_custom_shape(obj, shoulder_wgt, top)
			obj.data.edit_bones[top].use_deform = False
		
			
			# new intermediate roll bone
			new_roll_name = new_bone(obj, "ORG-foot_roll.ik"+side)
			def_geo(obj, new_roll_name, obj.data.edit_bones[roll_name+side].head, obj.data.edit_bones[roll_name+side].tail, obj.data.edit_bones[roll_name+side].roll)
			copy_layer(obj, constraint_01 + side, new_roll_name)
			copy_rotation_mode(obj, roll_name + side, new_roll_name)

			#change rotation mode of top 
			bpy.ops.object.mode_set(mode='POSE')
			obj.pose.bones[new_roll_name].rotation_mode = 'XYZ'
			bpy.ops.object.mode_set(mode='EDIT')

			#change parenting
			obj.data.edit_bones[top].parent = obj.data.edit_bones[foot_name + side]
			obj.data.edit_bones[new_roll_name].parent = obj.data.edit_bones[top]
			obj.data.edit_bones[constraint_04_01 + side + constraint_04_02].parent = obj.data.edit_bones[top]

			#create custom properties
			bpy.context.active_object.pose.bones[foot_name+side]["_RNA_UI"] = {}
			bpy.context.active_object.pose.bones[foot_name+side]["_RNA_UI"]['footbreak_angle'] = {"min":0.0, "max":180.0}
			bpy.context.active_object.pose.bones[foot_name+side]["footbreak_angle"] = 50.0
			bpy.context.active_object.pose.bones[foot_name+side].footbreak = False

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
			limit.use_limit_y = True
			limit.use_limit_z = True
			limit.max_x 	  = math.pi
			limit.owner_space = 'LOCAL'
			
			#create constraint on new roll bone
			bpy.ops.pose.select_all(action='DESELECT')
			obj.data.bones[new_roll_name].select = True
			obj.data.bones.active = obj.data.bones[new_roll_name]
			copy_rot = obj.pose.bones[new_roll_name].constraints.new(type='COPY_ROTATION')
			copy_rot.target = obj
			copy_rot.subtarget = roll_name + side
			copy_rot.target_space = 'LOCAL'
			copy_rot.owner_space = 'LOCAL'

			limit_rot = obj.pose.bones[new_roll_name].constraints.new(type='LIMIT_ROTATION')
			limit_rot.use_limit_x = True
			limit_rot.min_x = - 2 * math.pi
			limit_rot.owner_space = 'LOCAL'

			#change existing constraints
			obj.pose.bones[constraint_01 + side].constraints[0].subtarget = new_roll_name 
			obj.pose.bones[constraint_02_01 + side + constraint_02_02].constraints[0].subtarget = new_roll_name
			obj.pose.bones[constraint_03 + side].constraints[0].subtarget = new_roll_name 
			obj.pose.bones[constraint_04_01 + side + constraint_04_02].constraints[0].subtarget = new_roll_name 



			# create new drivers
			fcurve = obj.pose.bones[new_roll_name].constraints[1].driver_add('max_x')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "var*2*pi/360"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"footbreak_angle\"]"
			
			fcurve = obj.pose.bones[new_roll_name].constraints[1].driver_add('influence')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "var"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"].footbreak"
			
				
			fcurve = obj.pose.bones[top].constraints[0].driver_add('from_min_x_rot')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "var*2*pi/360"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"footbreak_angle\"]"

			fcurve = obj.pose.bones[top].constraints[0].driver_add('to_max_x_rot')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "(180-var)*2*pi/360"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"footbreak_angle\"]"

			fcurve = obj.pose.bones[top].constraints[0].driver_add('influence')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "var"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"].footbreak"
			

			bpy.ops.object.mode_set(mode='EDIT')

		bpy.ops.object.mode_set(mode=start_mode)

		# add UI
		ui_text_ = ui_text.replace("###rig_id###", "\"" + obj.data["rig_id"] + "\"")
		ui_text_ = ui_text_.replace("###bone###", foot_name)

		if obj.data["rig_id"] + "_rollbreakUI.py" in bpy.data.texts.keys():
			bpy.data.texts.remove(bpy.data.texts[obj.data["rig_id"] + "_rollbreakUI.py"])
		text = bpy.data.texts.new(name=obj.data["rig_id"] + "_rollbreakUI.py")
		text.use_module = True
		text.write(ui_text_)
		exec(text.as_string(), {})
		return {'FINISHED'}
		
	def patch_human(self, context):
		global ui_text
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
			obj.data.edit_bones[top].use_deform = False
			
			
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
			bpy.context.active_object.pose.bones[foot_name+side]["_RNA_UI"]['footbreak_angle'] = {"min":0.0, "max":180.0}
			bpy.context.active_object.pose.bones[foot_name+side]["footbreak_angle"] = 50.0
			bpy.context.active_object.pose.bones[foot_name+side].footbreak = False

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
			
			#create constraint on new roll bone
			bpy.ops.pose.select_all(action='DESELECT')
			obj.data.bones[new_roll_name].select = True
			obj.data.bones.active = obj.data.bones[new_roll_name]
			copy_rot = obj.pose.bones[new_roll_name].constraints.new(type='COPY_ROTATION')
			copy_rot.target = obj
			copy_rot.subtarget = roll_name + side
			if self.complexity == "DRIVER":
				copy_rot.use_x = False
			copy_rot.target_space = 'LOCAL'
			copy_rot.owner_space = 'LOCAL'
			
			if self.complexity == "DRIVER":
				#change existing drivers
				for driv in obj.animation_data.drivers:
					if driv.data_path == "pose.bones[\"" + driver_01_01 + side + driver_01_02 + "\"].rotation_euler" and driv.array_index == 0:
						driv.driver.variables[0].targets[0].data_path = "pose.bones[\"" + new_roll_name + "\"].rotation_euler[0]"
					elif driv.data_path == "pose.bones[\"" + driver_02_01 + side + driver_02_02 + "\"].rotation_euler" and driv.array_index == 0:
						driv.driver.variables[0].targets[0].data_path = "pose.bones[\"" + new_roll_name + "\"].rotation_euler[0]"
			elif self.complexity == "CONSTRAINT":
				#delete drivers
				obj.pose.bones[driver_01_01 + side + driver_01_02].driver_remove("rotation_euler", 0)
				obj.pose.bones[driver_02_01 + side + driver_02_02].driver_remove("rotation_euler", 0)	

				#add new constraints
				copy_rot = obj.pose.bones[driver_01_01 + side + driver_01_02].constraints.new(type='COPY_ROTATION')
				copy_rot.target = obj
				copy_rot.subtarget = new_roll_name
				copy_rot.owner_space = 'LOCAL'
				copy_rot.target_space = 'LOCAL'
				limit_rot = obj.pose.bones[driver_01_01 + side + driver_01_02].constraints.new(type='LIMIT_ROTATION')
				limit_rot.use_limit_x = True
				limit_rot.min_x = - math.pi
				limit_rot.owner_space = 'LOCAL'

				copy_rot = obj.pose.bones[driver_02_01 + side + driver_02_02].constraints.new(type='COPY_ROTATION')
				copy_rot.target = obj
				copy_rot.subtarget = new_roll_name
				copy_rot.owner_space = 'LOCAL'
				copy_rot.target_space = 'LOCAL'
				limit_rot = obj.pose.bones[driver_02_01 + side + driver_02_02].constraints.new(type='LIMIT_ROTATION')
				limit_rot.use_limit_x = True
				limit_rot.max_x = math.pi
				limit_rot.owner_space = 'LOCAL'
				
			if self.complexity == "DRIVER":		
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
				targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"footbreak_angle\"]"
				var = drv.variables.new()
				var.name = 'var_onoff'
				var.type = 'SINGLE_PROP'
				targ = var.targets[0]
				targ.id = obj
				targ.data_path = "pose.bones[\"" + foot_name + side + "\"].footbreak"

			elif self.complexity == "CONSTRAINT":
				#add constraint
				limit_rot = obj.pose.bones[new_roll_name].constraints.new(type="LIMIT_ROTATION")
				limit_rot.use_limit_x = True
				limit_rot.min_x = - math.pi
				limit_rot.max_x = 0 #will be set be driver
				limit_rot.owner_space = 'LOCAL'

				#add driver
				fcurve = obj.pose.bones[new_roll_name].constraints[1].driver_add('max_x')
				drv = fcurve.driver
				drv.type = 'SCRIPTED'
				drv.expression = "var*2*pi/360"
				var = drv.variables.new()
				var.name = 'var'
				var.type = 'SINGLE_PROP'
				targ = var.targets[0]
				targ.id = obj
				targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"footbreak_angle\"]"
			
			
				
			fcurve = obj.pose.bones[top].constraints[0].driver_add('from_min_x_rot')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "var*2*pi/360"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"footbreak_angle\"]"

			fcurve = obj.pose.bones[top].constraints[0].driver_add('to_max_x_rot')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "(180-var)*2*pi/360"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"footbreak_angle\"]"

			fcurve = obj.pose.bones[top].constraints[0].driver_add('influence')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "var"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"].footbreak"


					
			bpy.ops.object.mode_set(mode='EDIT')
			
		bpy.ops.object.mode_set(mode=start_mode)

		# add UI
		ui_text_ = ui_text.replace("###rig_id###", "\"" + obj.data["rig_id"] + "\"")
		ui_text_ = ui_text_.replace("###bone###", foot_name)

		if obj.data["rig_id"] + "_rollbreakUI.py" in bpy.data.texts.keys():
			bpy.data.texts.remove(bpy.data.texts[obj.data["rig_id"] + "_rollbreakUI.py"])
		text = bpy.data.texts.new(name=obj.data["rig_id"] + "_rollbreakUI.py")
		text.use_module = True
		text.write(ui_text_)
		exec(text.as_string(), {})
		return {'FINISHED'}
		
	
def register():
	bpy.types.PoseBone.footbreak = bpy.props.BoolProperty()
	bpy.types.Scene.complexity   = bpy.props.EnumProperty(items=complexity_items)
	bpy.utils.register_class(PatchRigify)
	bpy.utils.register_class(DATA_PT_rigify_patch)
	
def unregister():
	del bpy.types.PoseBone.footbreak
	bpy.utils.unregister_class(PatchRigify)
	bpy.utils.unregister_class(DATA_PT_rigify_patch)
		
if __name__ == "__main__":
	register()
