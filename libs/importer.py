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

import bpy, os, shutil, platform
from . import environment, misc, keys, zip
from copy import copy

#Create import blex file folder
def BlexImportFolder(path,  name,  api_functions, active_language, active_configuration, default_paths):
    blend_all_path = eval(api_functions['blend_filepath'])
    blend_name = blend_all_path.split("/")[-1]
    blend_path = blend_all_path.replace(blend_name,  "") + "/ShaderToolsNGImport/" + name
    if not os.path.exists(blend_path): os.makedirs(blend_path)
    return blend_path

#Import blex file
def BlexImport(path, api_functions, active_language, active_configuration, default_paths):
    misc.Clear(default_paths['zip'], 'all', '', active_language)
    misc.Clear(default_paths['temp'], 'all', '', active_language)
    script_path = zip.DeZip(default_paths['app'], active_configuration, path, 'folder', active_language)
    if platform.system() == 'Windows':
        script_path = misc.DoubleSlash(script_path)

    new_script_file = []
    if type(script_path).__name__ == 'str':
        script_path_2 = os.path.join(copy(script_path), "script.py")
        file = open(script_path_2,'r', encoding = "utf-8")
        file_lines = file.readlines()
        
        for l in file_lines:
            if l.find('# Material name : ') >= 0:
                name_folder = l.replace('# Material name : ', '')
                name_folder = name_folder.replace("\n",  "")
                blend_folder = BlexImportFolder(path,  name_folder,api_functions, active_language, active_configuration, default_paths)
            if l == '!*-environment_path-*!\n': l = "environment_path = '%s'\n" % script_path
            if l == '!*-blend_folder-*!\n': l = "blend_folder = '%s'\n" % blend_folder
            new_script_file.append(l)
        file.close()
    
        script_path_2 = script_path_2.replace(".py", "_out.py")
        file = open(script_path_2,'a', encoding = "utf-8")
        for l in new_script_file:
            file.write(l)
        file.close()
        
        misc.CopyAllFiles(script_path,  blend_folder)
        eval(api_functions['ops_script_python_file_run'].replace("#1#", "'%s'" % script_path_2))
        
    misc.Clear(default_paths['zip'], 'all', '', active_language)
    misc.Clear(default_paths['temp'], 'all', '', active_language)
#end Import blex file
