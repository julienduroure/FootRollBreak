import bpy
from .ui_texts import *
from .globals import *
from .utils import *

from mathutils import Vector
import math

def exec_patch_pitchipoy(complexity):

	# Force to be in edit mode
	start_mode = bpy.context.mode
	if bpy.context.mode != "EDIT_ARMATURE":
		bpy.ops.object.mode_set(mode='EDIT')
	
	obj = bpy.context.active_object

	toe_name  = "ORG-toe"
	foot_name = "foot_ik"
	foot_def  = "DEF-foot"
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
	parenting_name      = "MCH-thigh_ik_target"
	
	#Create text for drivers
	if complexity == "FULL":
		driver_text_ = text_drivers.replace("###armature###", obj.name)
		driver_text_ = driver_text_.replace("###a###", str(a)) 
		driver_text_ = driver_text_.replace("###b###", str(b)) 
		driver_text_ = driver_text_.replace("###c###", str(c)) 
		driver_text_ = driver_text_.replace("###d###", str(d))
		driver_text_ = driver_text_.replace("###toe_def###", toe_name)
		driver_text_ = driver_text_.replace("###toe_top###", name_toe_top)
		driver_text_ = driver_text_.replace("###foot_def###", foot_def)
		
		if obj.data["rig_id"] + "_footrollbreakDriver.py" in bpy.data.texts.keys():
			bpy.data.texts.remove(bpy.data.texts[obj.data["rig_id"] + "_footrollbreakDriver.py"])
		text = bpy.data.texts.new(name=obj.data["rig_id"] + "_footrollbreakDriver.py")
		text.use_module = True
		text.write(driver_text_)
		exec(text.as_string(), {})

	for side in [".L", ".R"]:
		# Top toe bone
		top = new_bone(obj, name_toe_top + side)
		def_geo(obj, top, obj.data.edit_bones[toe_name+side].tail,
						  Vector((obj.data.edit_bones[toe_name+side].tail[0],obj.data.edit_bones[toe_name+side].tail[1],obj.data.edit_bones[roll_name+side].tail[2])),
						  0)
		copy_layer(obj, roll_name + side, top)
		copy_custom_shape(obj, shoulder_wgt, top)
		obj.data.edit_bones[top].use_deform = False
	
		
		# new intermediate roll bone
		new_roll_name = new_bone(obj, name_intermediate_roll +side)
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
		obj.data.edit_bones[parenting_name + side].parent = obj.data.edit_bones[name_intermediate_roll + side]

		#create custom properties
		bpy.context.active_object.pose.bones[new_roll_name]["complexity"] = complexity
		bpy.context.active_object.pose.bones[foot_name+side]["_RNA_UI"] = {}
		bpy.context.active_object.pose.bones[foot_name+side]["_RNA_UI"]['footrollbreak_angle'] = {"min":0.0, "max":180.0}
		bpy.context.active_object.pose.bones[foot_name+side]["footrollbreak_angle"] = default_footrollbreak_angle
		bpy.context.active_object.pose.bones[foot_name+side].footrollbreak = default_footrollbreak
		if complexity == "FULL":
			bpy.context.active_object.pose.bones[foot_name+side].footrollbreak_return = default_footrollbreak_return
			bpy.context.active_object.pose.bones[foot_name+side]["_RNA_UI"][name_corrective_return_angle] = {"min":-180.0, "max":180.0}
			bpy.context.active_object.pose.bones[foot_name+side][name_corrective_return_angle] = default_corrective_return_angle
			bpy.context.active_object.pose.bones[foot_name+side]["_RNA_UI"][name_footrollbreak_angle_max] = {"min":0.0, "max":180.0}
			bpy.context.active_object.pose.bones[foot_name+side][name_footrollbreak_angle_max] = default_footrollbreak_angle_max			

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
		
		if complexity == "FULL":
			#Return system
			transform = obj.pose.bones[top].constraints.new(type='TRANSFORM')
			transform.target = obj
			transform.subtarget = roll_name + side
			transform.map_from = 'ROTATION'
			#min & max will be set by drivers
			transform.map_to = 'ROTATION'
			#max will be set be driver
			transform.target_space = 'LOCAL'
			transform.owner_space = 'LOCAL'
			
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
		if complexity == "CONSTRAINT":
			fcurve = obj.pose.bones[new_roll_name].constraints[1].driver_add('max_x')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "var*2*pi/360"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"" + name_footrollbreak_angle + "\"]"
		elif complexity == "FULL":
			#Return system
			fcurve = obj.pose.bones[new_roll_name].constraints[1].driver_add('max_x')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "driver_rollbreak(return_enable, current_angle/(2*pi)*360, angle, angle_max)"
			var = drv.variables.new()
			var.name = 'angle'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"" + name_footrollbreak_angle + "\"]"
			var = drv.variables.new()
			var.name = 'return_enable'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"].footrollbreak_return"
			var = drv.variables.new()
			var.name = 'angle_max'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"" + name_footrollbreak_angle_max + "\"]"
			var = drv.variables.new()
			var.name = 'current_angle'
			var.type = 'TRANSFORMS'
			targ = var.targets[0]
			targ.transform_type = 'ROT_X'
			targ.id = obj
			targ.bone_target = roll_name + side
			targ.transform_space = 'LOCAL_SPACE'
			
		#on / off
		fcurve = obj.pose.bones[new_roll_name].constraints[1].driver_add('influence')
		drv = fcurve.driver
		drv.type = 'SCRIPTED'
		drv.expression = "var"
		var = drv.variables.new()
		var.name = 'var'
		var.type = 'SINGLE_PROP'
		targ = var.targets[0]
		targ.id = obj
		targ.data_path = "pose.bones[\"" + foot_name + side + "\"].footrollbreak"
		
			
		fcurve = obj.pose.bones[top].constraints[0].driver_add('from_min_x_rot')
		drv = fcurve.driver
		drv.type = 'SCRIPTED'
		drv.expression = "var*2*pi/360"
		var = drv.variables.new()
		var.name = 'var'
		var.type = 'SINGLE_PROP'
		targ = var.targets[0]
		targ.id = obj
		targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"" + name_footrollbreak_angle + "\"]"

		fcurve = obj.pose.bones[top].constraints[0].driver_add('to_max_x_rot')
		drv = fcurve.driver
		drv.type = 'SCRIPTED'
		drv.expression = "(180-var)*2*pi/360"
		var = drv.variables.new()
		var.name = 'var'
		var.type = 'SINGLE_PROP'
		targ = var.targets[0]
		targ.id = obj
		targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"" + name_footrollbreak_angle + "\"]"

		#On / Off
		fcurve = obj.pose.bones[top].constraints[0].driver_add('influence')
		drv = fcurve.driver
		drv.type = 'SCRIPTED'
		drv.expression = "var"
		var = drv.variables.new()
		var.name = 'var'
		var.type = 'SINGLE_PROP'
		targ = var.targets[0]
		targ.id = obj
		targ.data_path = "pose.bones[\"" + foot_name + side + "\"].footrollbreak"
		
		if complexity == "FULL":
			#Return System
			fcurve = obj.pose.bones[top].constraints[2].driver_add('from_min_x_rot')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "var*2*pi/360"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"" + name_footrollbreak_angle + "\"]"

			fcurve = obj.pose.bones[top].constraints[2].driver_add('from_max_x_rot')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "var*2*pi/360"
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"" + name_footrollbreak_angle_max + "\"]"

			fcurve = obj.pose.bones[top].constraints[2].driver_add('to_max_x_rot')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "driver_rollbreak_return('" + side + "', angle, corrective)"
			var = drv.variables.new()
			var.name = 'angle'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"" + name_footrollbreak_angle + "\"]"
			var = drv.variables.new()
			var.name = 'corrective'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"][\"" + name_corrective_return_angle + "\"]"

			fcurve = obj.pose.bones[top].constraints[2].driver_add('influence')
			drv = fcurve.driver
			drv.type = 'SCRIPTED'
			drv.expression = "rollbreak"
			drv.expression = "rollbreak * return_enable"
			var = drv.variables.new()
			var.name = 'rollbreak'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"].footrollbreak"
			var = drv.variables.new()
			var.name = 'return_enable'
			var.type = 'SINGLE_PROP'
			targ = var.targets[0]
			targ.id = obj
			targ.data_path = "pose.bones[\"" + foot_name + side + "\"].footrollbreak_return" 
			

		bpy.ops.object.mode_set(mode='EDIT')

	bpy.ops.object.mode_set(mode=start_mode)

	# add UI
	ui_text_ = ui_text.replace("###rig_id###", "\"" + obj.data["rig_id"] + "\"")
	ui_text_ = ui_text_.replace("###bone###", foot_name)
	ui_text_ = ui_text_.replace("###bone_roll###", name_intermediate_roll)

	if obj.data["rig_id"] + "_footrollbreakUI.py" in bpy.data.texts.keys():
		bpy.data.texts.remove(bpy.data.texts[obj.data["rig_id"] + "_footrollbreakUI.py"])
	text = bpy.data.texts.new(name=obj.data["rig_id"] + "_footrollbreakUI.py")
	text.use_module = True
	text.write(ui_text_)
	exec(text.as_string(), {})
	return {'FINISHED'}

