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

def OpenLog(app_path, active_configuration, api_function):
    #Imports & external libs:
    try:
        import bpy, os, platform
        from . import misc
    except:
        print("#ShaderToolsNG : error import logs")
    #end Imports & external libs:
    path_files = os.path.join(misc.ConvertMarkOut(active_configuration['error_folder'], app_path), "log.txt")
    #Open log file:
    if platform.system() == 'Windows':
        logs = os.popen('"%s"' % path_files)

    if platform.system() == 'Darwin':
        logs = os.popen("open '%s' " % path_files)

    if platform.system() == 'Linux':
        logs = os.popen("gedit '%s'" % path_files)    
    #end Open log file:
