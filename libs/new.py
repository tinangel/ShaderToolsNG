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

import bpy,  shutil
from shader_tools_ng.libs import keys
    
def CreateNew(app_path, active_configuration, api_function, active_language):
    #Imports & external libs:
    try:
        import bpy, os, platform
        from . import zip, misc
    except:
        print("#ShaderToolsNG : error import createnew")
    #end Imports & external libs:
    #Copy file:
    wbfp = misc.ConvertMarkOut(active_configuration['workbase_file_path'], app_path)
    wbdf = misc.ConvertMarkOut(active_configuration['temp_folder'], app_path)
    temp_val = os.path.join(wbdf, wbfp.split(os.sep)[-1] + ".blend")
    shutil.copy2(wbfp, temp_val)
    #end Copy file: 
    #Open workbase blend file:
    try:
        bin_path = eval(api_function['app_binary_path'])
        if platform.system() == 'Darwin': workbase = os.popen("open -n -a '%s' '%s'" % (bin_path.rstrip("/Contents/MacOS/blender"), temp_val),  'w')
        else: workbase = os.popen('"%s" "%s"' % (bin_path,  temp_val),  'w')
        print(active_language['menu_error_error025'])
        misc.LogError(active_language['menu_error_error025'], False)
    except:
        print(active_language['menu_error_error026'])
        misc.LogError(active_language['menu_error_error026'], False)
    #end Open workbase zip file:
