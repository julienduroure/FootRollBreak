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

bl_info = {
	"name": "Add FootRoll Break to Rigify",
	"author": "Julien Duroure",
	"version": (1, 0, 0),
	"blender": (2,77, 0),
	"description": "Add FootRoll Break to Rigify",
	"location": "Armature Properties, View 3D Properties",
	"wiki_url": "http://julienduroure.com/footrollbreak/",
	"tracker_url": "https://github.com/julienduroure/rigify_rollbreak_patch",
	"category": "Rigging",   
}

if "bpy" in locals():
	import imp
	imp.reload(addon_prefs)
	imp.reload(ui_texts)
	imp.reload(globals)
	imp.reload(utils)
	imp.reload(ui)
	imp.reload(patch_human)
	imp.reload(patch_pitchipoy)
	imp.reload(ops)
else:
	from .addon_prefs import *
	from .ui_texts import *
	from .globals import *
	from .utils import *
	from . import ui
	from .patch_human import *
	from .patch_pitchipoy import *
	from . import ops

import bpy

def register():
	bpy.types.PoseBone.footrollbreak = bpy.props.BoolProperty()
	bpy.types.PoseBone.footrollbreak_return = bpy.props.BoolProperty()
	addon_prefs.register()
	ops.register()
	ui.register()
	
def unregister():
	#Do not del BoolProperty : needed for footbreakroll still working after removing addon
	addon_prefs.unregister()
	ops.unregister()
	ui.unregister()
		
if __name__ == "__main__":
	register()
