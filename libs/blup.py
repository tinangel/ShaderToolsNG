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
import bpy, os, platform,  shutil
from . import misc,  request,  keys

def OpenVersion(path):
    version = ""
    path = misc.DoubleSlash(path)
    if os.path.exists(path):
        fversion = open(path, "r", encoding = "utf-8")
        version = fversion.read()
        version = version.split(" = ")[-1]
        version = version.strip()
        fversion.close()
    return version
    
def OpenMigrate(default_paths, path):
    migrate = ""
    path = misc.DoubleSlash(path)
    if os.path.exists(path):
        fmigrate = open(path, "r", encoding = "utf-8")
        migrate = fmigrate.read()
        fmigrate.close()
    
    for e in migrate.split("\n"):
        for k in keys.DumpKeys(default_paths):
            if k in e : return True
    return False
    
def BlupInstall(default_paths,  blup_directory, blup_path,  blup_error,  blup_check, active_languages, api_functions) :
    ctx_scene = eval(api_functions['context_scene'])
    paths = os.path.join(blup_directory,  "paths.blup")
    paths = misc.DoubleSlash(paths)
    tbl_paths = []
    counter = 0
    
    if os.path.exists(paths):
        fpaths = open(paths, "r", encoding = "utf-8")
        for l in fpaths:
            temp_file = l.strip()
            temp_file = temp_file.split(":;:")
            tbl_paths.append(temp_file)
            counter = counter + 1
        fpaths.close()
        ctx_scene.shadertoolsng_utils_bar = misc.CrossProduct(1, counter)

        counter_temp = 1
        complete_hierarchy = misc.DirectoryHierarchy(default_paths["app"],  "",  "")
        
        #Complete save
        default_folder = ""
        try:
            create = "create"
            if complete_hierarchy:
                for e in complete_hierarchy:
                    if create == "create": 
                        default_folder = misc.CompleteSave(complete_hierarchy[0],  default_paths,  create,  default_folder) 
                        create = ""
                    else: misc.CompleteSave(e, default_paths,  create,  default_folder)
        except:
            os.rename(blup_path,  blup_error)
            ctx_scene.shadertoolsng_utils_bar = misc.CrossProduct(counter, counter)
            return 0     
        #End complete save
             
        #Replace files
        try:
            for l in tbl_paths:
                if l[0].strip():
                    temp_path = l[1].lstrip(os.sep)
                    temp_path =  misc.DoubleSlash(temp_path)
                    if l[0].strip() in keys.DumpKeys(default_paths): request.DatabaseDump(default_paths,  os.path.join(default_paths["app"],  temp_path),  l[0].strip().replace("sqlite",  "blump"))
                    misc.Clear(os.path.join(default_paths["app"],  temp_path), "files", "one", active_languages)
                    shutil.copy2(os.path.join(blup_directory, l[0]), os.path.join(default_paths["app"],  temp_path))
                    if l[0].strip() in keys.DumpKeys(default_paths): request.DatabaseDumpImport(default_paths, api_functions,   os.path.join(default_paths["app"],  temp_path),  l[0].strip())
                    ctx_scene.shadertoolsng_utils_bar = misc.CrossProduct(counter_temp, counter)
                    counter_temp = counter_temp + 1
        except: 
            ctx_scene.shadertoolsng_utils_bar = 100
            os.rename(blup_path,  blup_error)
            return 0
        #End replace files

    try:
        ctx_scene.shadertoolsng_utils_bar = 100
        misc.Clear(blup_directory, "all", "", active_languages)
        os.rename(blup_path,  blup_check)
    except: os.rename(blup_path,  blup_error)

def BlupErrorFolder(path):
    blup_error_line = ""
    path = misc.DoubleSlash(path)
    if os.path.exists(path): 
        fblup_error_path = open(path, "r", encoding = "utf-8")
        blup_error_line = fblup_error_path.read()
        fblup_error_path.close()
        blup_error_line = blup_error_line.strip()
    return blup_error_line
