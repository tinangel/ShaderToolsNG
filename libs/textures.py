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
import bpy, os, shutil
from . import misc, keys 
from copy import copy

def TexturesPropertiesExport(api_functions, texture_structure, texture_keys, idx, active_language):
    for k in texture_keys:
        slot = "%s[%s].%s" % (api_functions['texture_slots'], idx, k)
        val = ""
        try: val = copy(eval(slot))
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
    return texture_structure

def TexturesFileImagesExport(api_functions, material_dict, idx, active_language):
    if eval(api_functions['texture_image_source'].replace("#1#", str(idx))) == 'GENERATED':
        exec("%s = 'FILE'" % api_functions['texture_image_source'].replace("#1#", str(idx)))
    
    try:
        material_folder = ""
        name_image = misc.ImageAbsolutePath(os.path.relpath(api_functions['texture_image_filepath'].replace("#1#", str(idx))))
        material_folder = os.path.join(material_dict['temp'], material_dict['material_name'], name_image[0].split(os.path.sep)[-1])
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
            material_folder = os.path.join(material_dict['temp'], material_dict['material_name'], name_image[0].split(os.path.sep)[-1])
            shutil.copy2(name_image[0], material_folder)            
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
        name_image = name_image + ".tga"
        material_folder = os.path.join(material_dict['temp'], material_dict['material_name'], name_image)
        export_generated = api_functions['texture_image_save_as'].replace("#1#", "'%s'" % name_image_2)
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