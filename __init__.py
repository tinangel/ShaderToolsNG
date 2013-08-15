# ##### BEGIN CC LICENSE BLOCK #####
#
# This work is licensed under a 
# Creative Commons Attribution 3.0 
# Unported (CC BY 3.0) License : 
#
# More details here : http://creativecommons.org/licenses/by/3.0/deed.en
#
# ##### END CC LICENSE BLOCK #####

# <pep8-80 compliant>
#-*- coding: utf-8 -*-

bl_info = {
    "name": "ShaderTools Next Gen",
    "author": "GRETETE Karim (Tinangel)",
    "version": (1, 0, 3),
    "blender": (2, 6, 8),
    "api": 58536,
    "location": "User Preferences",
    "description": "Shader tools for blender",
    "warning": "",
    "wiki_url": "http://shadertoolsng.free.fr/help/",
    "tracker_url": "",
    "support": 'COMMUNITY',
    "category": "System",}

import bpy
from bpy.app.handlers import persistent

@persistent
def wait_blender( self ):
    if "bpy" in locals():
        import imp
        imp.reload( gui )
    else:
        from . import gui

def register():
    bpy.app.handlers.load_post.append( wait_blender )

def unregister():
    for c in MyReg :
        bpy.utils.unregister_class(c)
    #end for
#end unregister

if __name__ == "__main__":
    register()
