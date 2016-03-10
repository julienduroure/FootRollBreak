bl_info = {
	"name": "Add FootRoll Break to Rigify",
	"author": "Julien Duroure",
	"version": (0, 0, 3),
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
	del bpy.types.PoseBone.footrollbreak
	del bpy.types.PoseBone.footrollbreak_return
	addon_prefs.unregister()
	ops.unregister()
	ui.unregister()
		
if __name__ == "__main__":
	register()
