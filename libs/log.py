# ##### BEGIN CC LICENSE BLOCK #####
#
# This work is licensed under a Creative 
# Commons Attribution-NonCommercial-ShareAlike 
# 3.0 Unported License : 
#
# More details here : http://creativecommons.org/licenses/by-nc-sa/3.0/deed.fr
#
# ##### BEGIN CC LICENSE BLOCK #####

# <pep8-80 compliant>

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
