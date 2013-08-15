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

import bpy, os, zipfile, platform, shutil
from . import misc

def DeZip(app_path, active_configuration, zip_path, option, active_language):
    #Imports & external libs:
    try:
        import bpy, os, zipfile, platform, shutil
        from . import misc
    except:
        print("#ShaderToolsNG : error import dezip")
    #end Imports & external libs:
    #Copy zip_file & dezip:
    try:
        zip_file = misc.ConvertMarkOut(zip_path, app_path)
        zip_in_zip_folder = os.path.join(misc.ConvertMarkOut(active_configuration['zip_folder'], app_path), zip_file.split(os.path.sep)[-1] + ".zip")
        if os.path.exists(zip_in_zip_folder):
            os.remove(zip_in_zip_folder)
        
        name_folder = ''
        if option == 'folder':
            name_folder = zip_file.split(os.path.sep)[-1]
            name_folder = name_folder.split(".")[0]
            try:
                os.makedirs(os.path.join(misc.ConvertMarkOut(active_configuration['temp_folder'], app_path), name_folder))
            except: 
                misc.Clear()

        shutil.copy2(zip_file, zip_in_zip_folder)

        zfile = zipfile.ZipFile(zip_in_zip_folder, 'r')
        for z in zfile.namelist():
            if os.path.isdir(z):
                try: 
                    os.makedirs(os.path.join(misc.ConvertMarkOut(active_configuration['temp_folder'], app_path), z))
                except: pass
            else:
                try: 
                    os.makedirs(os.path.join(misc.ConvertMarkOut(active_configuration['temp_folder'], app_path), os.path.dirname(z)))
                except: pass
                data = zfile.read(z)
                if option == 'folder': fp = open(os.path.join(misc.ConvertMarkOut(active_configuration['temp_folder'], app_path), name_folder, z), "wb")
                else: fp = open(os.path.join(misc.ConvertMarkOut(active_configuration['temp_folder'], app_path), z), "wb")
                fp.write(data)
                fp.close()
        zfile.close()
        print(active_language['menu_error_error029'])
        misc.LogError(active_language['menu_error_error029'], False)
        if option == 'folder': return os.path.join(misc.ConvertMarkOut(active_configuration['temp_folder'], app_path), name_folder)
        else: return True
    except:
        print(active_language['menu_error_error030'])
        misc.LogError(active_language['menu_error_error030'], False)
        return False
    #end Copy zip_file & dezip:

def Zip(material_dict, api_functions, active_languages):
    #Imports & external libs:
    try:
        import bpy, os, zipfile, platform, shutil
    except:
        print("#ShaderToolsNG : error import zip")
    #Now I zip files :
    material_path = os.path.join(material_dict['zip'], material_dict['material_name'])
    script_path = os.path.join(material_dict['temp'], material_dict['material_name'])
    zip_file_path = "%s_%s.blex" % (material_path, material_dict['creator'])
    zip_file = zipfile.ZipFile(zip_file_path,'w', zipfile.ZIP_DEFLATED)
    
    #I zip files in Zip Folder:
    try:
        files = os.listdir(script_path)
        for f in files:
            if not os.path.isdir(f):
                zip_file_write = os.path.join(script_path , f)
                zip_file.write(zip_file_write, os.path.basename(zip_file_write), zipfile.ZIP_DEFLATED)    
        zip_file.close()
    except:
        try: zip_file.close()
        except: print(active_language['menu_error_error022'] % zip_file_path.split(os.sep)[-1])

    return zip_file_path

def DeZipBlup(default_paths,  blup_path,  blup_directory):
    zfile = zipfile.ZipFile(blup_path, 'r')
    for z in zfile.namelist():
        if os.path.isdir(z):
            try: os.makedirs(blup_directory, z)
            except: 
                try: 
                    data = zfile.read(z)
                    fp = open(os.path.join(blup_directory, z), "wb")
                    fp.write(data)
                    fp.close()
                except: pass
        else:
            try: os.makedirs(os.path.join(blup_directory, os.path.dirname(z)))
            except: pass
            data = zfile.read(z)
            fp = open(os.path.join(blup_directory, z), "wb")
            fp.write(data)
            fp.close()
    zfile.close()
    return 10
    
    
    
    
    
    
    
    
    
