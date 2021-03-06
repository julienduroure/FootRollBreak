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
