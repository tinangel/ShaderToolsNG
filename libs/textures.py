# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>
import bpy, os, shutil, platform
from . import misc, keys 
from copy import copy

def TexturesGeneratedImageTypeExport(api_functions, texture_structure, t, active_language, material_dict):
    source_image = eval(api_functions['texture_image_source'].replace("#1#", str(t)))
    if source_image == 'FILE' or source_image == 'GENERATED':
        name_image = eval(api_functions['texture_image_filepath'].replace("#1#", str(t)))
        name_image_2 = copy(name_image)
        name_image = name_image.upper()
        type_image = 'GENERATED' 
        for k in keys.ImageFileFormatKeys(''):
            keys_temp = keys.ImageFileFormatKeys('') 
            if name_image.find(keys_temp[k].upper()) >= 0:
                type_image = 'FILE'
        
        if type_image == 'GENERATED':
            infos_texture = TexturesGeneratedImagesExport(api_functions, material_dict, t, active_language)
            if infos_texture != False:
                image_path_in_script = "os.path.join(blend_folder, %s)" % str("'" + infos_texture[1] + "'" )
                image_path_in_script = "img = %s \n" % api_functions['texture_image_load'].replace("#1#", image_path_in_script)
                texture_structure.append(image_path_in_script)
                texture_structure.append("slot.texture.image = img\n")
                texture_structure = TexturesPropertiesExport(api_functions, texture_structure, keys.ImageExportKeys(), t, active_language)
        else:
            infos_texture = TexturesFileImagesExport(api_functions, material_dict, t, active_language)
            if infos_texture != False:
                image_path = infos_texture[1].split(os.sep)[-1]
                image_path_in_script = "os.path.join(environment_path, %s)" % str("'" + image_path + "'" )
                image_path_in_script = "img = %s \n" % api_functions['texture_image_load'].replace("#1#", image_path_in_script)
                texture_structure.append(image_path_in_script)
                texture_structure.append("slot.texture.image = img\n")
                texture_structure = TexturesPropertiesExport(api_functions, texture_structure, keys.ImageExportKeys(), t, active_language)
        texture_structure.append("try:%s\n" % api_functions['texture_image_pack'].replace("#1#", str(t)))
        texture_structure.append("except:pass\n")
        name_image_2 = name_image_2.split(os.sep)[-1]
        if name_image_2.find(".") < 0:
            name_image_2 = name_image_2 + ".png"
        name_image_2 = name_image_2.split(os.sep)[-1]
        name_image_2 = name_image_2.split("/")[-1]
        exec_path = "//ShaderToolsImportNG/%s/%s" % (eval(api_functions['material_name']), name_image_2)
        texture_structure.append("try:%s = '%s'\n" % (api_functions['texture_image_filepath'].replace("#1#", str(t)), exec_path))
        texture_structure.append("except:pass\n\n")
    else:
        print(active_language['menu_error_error015'])
        misc.LogError(active_language['menu_error_error015'], False)
    return texture_structure            

def TexturesIgnoreLayersExport(api_functions, texture_structure, texture_keys, idx, active_language):
    layers = eval(api_functions['texture_environment_map_layers_ignore'].replace("#1#", str(idx)))
    for l in range(0, layers.__len__()):
        if layers[l]:
            texture_structure.append("slot.%s[%s] = %s\n" % (keys.IgnoreLayersExportKeys()[0], str(l), str(layers[l])))
    return texture_structure

def TexturesPropertiesExport(api_functions, texture_structure, texture_keys, idx, active_language):
    for k in texture_keys:
        slot = "%s[%s].%s" % (api_functions['texture_slots'], idx, k)
        val = ""
        try: 
            val = copy(eval(slot))
            if val == 'GENERATED': val = 'FILE'
        except: val = None
        if val != None and val != '':
            if type(val).__name__ == 'str': texture_structure.append("slot.%s = '%s'\n" % (k,val))
            elif type(val).__name__ == 'Color':
                val = misc.RemoveColor(str(val))
                texture_structure.append("slot.%s = %s\n" % (k,val))
            elif type(val).__name__ == 'Vector':
                val = misc.RemoveVector(str(val))
                texture_structure.append("slot.%s = %s\n" % (k,val))                        
            else: texture_structure.append("slot.%s = %s\n" % (k,val))

        if k.find("voxel_data.resolution") >= 0:
            for v in range(0, 3):
                texture_structure.append("slot.%s[%s] = %s\n" % (k, str(v), eval(slot)[v]))
    return texture_structure

def TexturesFileImagesExport(api_functions, material_dict, idx, active_language):
    if eval(api_functions['texture_image_source'].replace("#1#", str(idx))) == 'GENERATED':
        exec("%s = 'FILE'" % api_functions['texture_image_source'].replace("#1#", str(idx)))
    
    try:
        material_folder = ""
        name_image = misc.ImageAbsolutePath(os.path.relpath(api_functions['texture_image_filepath'].replace("#1#", str(idx))))
        material_folder = os.path.join(material_dict['temp'], material_dict['material_name'], name_image.split(os.sep)[-1])
        material_folder = misc.DoubleSlash(material_folder)
        export_image = api_functions['texture_image_save_render'].replace("#1#", str(idx))
        export_image = export_image.replace("#2#", "'%s'" % material_folder)
        eval(export_image)
        list = (True, name_image, material_folder, export_image)
        return list
    except: 
        try:
            unpack = api_functions['texture_image_unpack'].replace("#1#", str(idx))
            eval(unpack.replace("#2#", "'USE_ORIGINAL'"))
            material_folder = ""
            name_image = misc.ImageAbsolutePath(os.path.relpath(api_functions['texture_image_filepath'].replace("#1#", str(idx))))
            material_folder = os.path.join(material_dict['temp'], material_dict['material_name'], name_image.split(os.sep)[-1])
            material_folder = misc.DoubleSlash(material_folder)
            shutil.copy2(name_image, material_folder)            
            pack = eval(api_functions['texture_image_pack'].replace("#1#", str(idx)))
            print(active_language['menu_error_error018'])
            misc.LogError(active_language['menu_error_error018'], False)
            list = (True, name_image, material_folder)
            return list
        except: 
            print(active_language['menu_error_error019'])
            misc.LogError(active_language['menu_error_error019'], False)
            return False

def TexturesGeneratedImagesExport(api_functions, material_dict, idx, active_language):
        name_image = eval(api_functions['texture_image_filepath'].replace("#1#", str(idx)))
        name_image_2 = eval(api_functions['texture_image_filepath'].replace("#1#", str(idx)))
        name_image = name_image + ".png"
        material_folder = os.path.join(material_dict['temp'], material_dict['material_name'], name_image)
        material_folder = misc.DoubleSlash(material_folder)
        export_generated = api_functions['texture_image_save_render'].replace("#1#", str(idx))
        export_generated = export_generated.replace("#2#", "'%s'" % material_folder)
        try: 
            eval(export_generated)
            list = (True, name_image, name_image_2, material_folder, export_generated)
            return list
        except:
            try:
                exec("%s = 'GENERATED'" % api_functions['texture_image_source'].replace("#1#", str(idx)))
                eval(export_generated)
                list = (True, name_image, name_image_2, material_folder, export_generated)
                return list
            except:
                print(active_language['menu_error_error020'])
                misc.LogError(active_language['menu_error_error020'], False)
                return False
