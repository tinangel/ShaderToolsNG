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
#-*- coding: utf-8 -*-

import bpy, os
from shader_tools_ng.libs import misc,  keys

def Selected(default_paths,  active_configuration, api_functions, active_languages, choices):
    c= 0
    ctx_scene = eval(api_functions['context_scene'])
    ctx_scene.shadertoolsng_utils_bar = c  
    
    for k in keys.CleanupKeys():
        c = c + 1
        ctx_scene.shadertoolsng_utils_bar = misc.CrossProduct(c, keys.CleanupKeys().__len__())

        if choices[k]:
            if k in ('temp',  'zip',  'error'):
                misc.Clear(default_paths[k], 'all', '', active_languages)
                misc.ClearDirectory(default_paths[k],  active_languages)
            elif k == 'materials':
                bookmarks_folder_path = os.path.join(default_paths['app'], active_languages['menu_bookmarks_name'])
                bookmarks_folders = (os.path.join(bookmarks_folder_path, ".tempory"), bookmarks_folder_path)
                for f in bookmarks_folders:
                    misc.Clear(f, 'all', '', active_languages)
                    misc.ClearDirectory(f,  active_languages)
            elif k == 'pycache':
                pycache_folder = (os.path.join(default_paths['app'], "__pycache__"), os.path.join(default_paths['app'], "libs","__pycache__"))
                for f in pycache_folder:
                    misc.Clear(f, 'all', '', active_languages)
                    misc.ClearDirectory(f,  active_languages)
            elif k == 'migrate':
                files = os.listdir(default_paths['save'])
                for f in files:           
                    if not os.path.isdir(f) and 'Migration' in f: misc.Clear(os.path.join(default_paths['save'], f), 'files', 'one', active_languages) 
            elif k in ('autosave',  'completesave'):
                files = os.listdir(default_paths['save'])
                for f in files:
                    if 'AutoSave' in f  and k == 'autosave': 
                        misc.Clear(os.path.join(default_paths['save'],  f), 'all', '', active_languages)
                        misc.ClearDirectory(os.path.join(default_paths['save'], f),  active_languages) 

                    if 'CompleteSave' in f  and k == 'completesave': 
                        misc.Clear(os.path.join(default_paths['save'],  f), 'all', '', active_languages)
                        misc.ClearDirectory(os.path.join(default_paths['save'], f),  active_languages) 
            else:None
    ctx_scene.shadertoolsng_utils_bar = 100
