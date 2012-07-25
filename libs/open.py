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

import bpy, shutil,  os, binascii,  time, threading
from . import misc, keys, request
from copy import copy

def IdxMaterial(name_object):
    idx_material = name_object.split("(")[-1]
    idx_material = idx_material.split(")")[0]
    return idx_material 
    
def CreateThumbnails(default_paths,  active_configuration, api_functions, active_languages,  option_bar):
    ctx_scene = eval(api_functions['context_scene'])
    thumbnails_folder_path = os.path.join(default_paths['app'], active_languages['menu_bookmarks_name'])
    database_path = misc.ConvertMarkOut(active_configuration['database_path'], default_paths['app'])
    req = request.DatabaseSelect(database_path, keys.ThumbnailsRenderKeys(),"RENDER", "", 'all')
    try: misc.Clear(thumbnails_folder_path, 'files', 'all', active_languages)
    except: pass
    try:
        current_element = 1
        max_elements = req.__len__()
        for e in req:
            if  option_bar: ctx_scene.shadertoolsng_utils_bar = misc.CrossProduct(current_element, max_elements)
            req_names = request.DatabaseSelect(database_path, keys.ThumbnailsMaterialsKeys(),"MATERIALS", "where num_materials =%s" %e[0], 'one')
            thumbnail_name = req_names[0].replace("$T_",  "") + "_(%s).jpg" %e[0]
            thumbnail_bytes = binascii.unhexlify(eval(e[1]))
            thumbnails_file_path = os.path.join(thumbnails_folder_path,   thumbnail_name)
            if os.path.exists(thumbnails_file_path) : os.remove(thumbnails_file_path)
            create_thumbnail = open(thumbnails_file_path,'wb')
            create_thumbnail.write(thumbnail_bytes)
            create_thumbnail.close()
            current_element = current_element + 1
    except:
        err = ('menu_error_error043', thumbnails_folder_path, 'menu_error_error044', 'menu_error_error045', 'menu_error_error046')
        for e in err: 
            try: misc.LogAndPrintError((active_languages[e] , active_languages[e]))
            except: misc.LogAndPrintError((e, e))
            
def ImportMaterialInApp(default_paths,  active_configuration, api_functions, active_languages,  name_object,  step_number):
    ctx_scene = eval(api_functions['context_scene'])
    database_path = misc.ConvertMarkOut(active_configuration['database_path'], default_paths['app'])
    database_keys_elements = []
    keys_elements = []
    req_type = request.DatabaseSelect(database_path,  ('type', ),"MATERIALS", "where num_materials =%s" % IdxMaterial(name_object), 'one')
    materials_keys_elements = []
    if req_type[0] == 'SURFACE' or req_type[0] == 'WIRE':
        for k in keys.SurfaceWireKeys(): materials_keys_elements.append(k)
    elif req_type[0] == 'VOLUME':  
        for k in keys.VolumeKeys(): materials_keys_elements.append(k)
    else: 
         for k in keys.HaloKeys(): materials_keys_elements.append(k)
 
    for e in materials_keys_elements:
        keys_elements.append(e)
        database_keys_elements.append(e.replace(".",  "_"))
    req = request.DatabaseSelect(database_path,  database_keys_elements,"MATERIALS", "where num_materials =%s" % IdxMaterial(name_object), 'one')
    if not req == []:
        c = 0
        for p in keys_elements:
            type_value = type(req[c]).__name__
            val = ""
            if type_value == 'NoneType': val = '0'
            elif type_value == 'str': val = copy(req[c])
            elif req[c] == None or req[c] == 'None': val = '0'
            else: val = str(req[c])
            api_propertie = keys.MaterialsPropertiesKeys(api_functions)[p][0]
            if keys.MaterialsPropertiesKeys(api_functions)[p][1] == 'yes': val = "'%s'" % val
            try:exec("%s = %s"% (api_propertie,  val, ))
            except: pass
            c = c + 1
    ctx_scene.shadertoolsng_utils_bar = (100/step_number) * 1
    ImportTexturesInApp(default_paths,  active_configuration, api_functions, active_languages,  name_object,  step_number,   IdxMaterial(name_object))
   
def ImportTexturesInApp(default_paths,  active_configuration, api_functions, active_languages,  name_object,  step_number,  idx_materials):
    ctx_scene = eval(api_functions['context_scene'])
    database_path = misc.ConvertMarkOut(active_configuration['database_path'], default_paths['app'])
    req_type = request.DatabaseSelect(database_path,  ('type', ),"TEXTURES", "where idx_materials =%s" % IdxMaterial(name_object), 'all')

    textures_keys_elements = []
    database_keys_elements = []
    for e in keys.InfluenceExportKeys(): textures_keys_elements.append(e)
    for e in keys.MappingExportKeys(): textures_keys_elements.append(e)
    for e in keys.ColorsExportKeys(): textures_keys_elements.append(e)

    if req_type[0] == 'BLEND':
        for e in keys.BlendExportKeys(): textures_keys_elements.append(e)
    elif req_type[0] == 'CLOUDS':
        for e in keys.BlendExportKeys(): textures_keys_elements.append(e)
    elif req_type[0] == 'DISTORTED_NOISE':
        for e in keys.DistortedExportKeys(): textures_keys_elements.append(e)
    elif req_type[0] == 'MAGIC':
        for e in keys.MagicExportKeys(): textures_keys_elements.append(e)    
    elif req_type[0] == 'MARBLE':
        for e in keys.MarbleExportKeys(): textures_keys_elements.append(e)
    elif req_type[0] == 'MUSGRAVE':
        for e in keys.MusgraveExportKeys(): textures_keys_elements.append(e)
    elif req_type[0] == 'STUCCI':
        for e in keys.StucciExportKeys(): textures_keys_elements.append(e)
    elif req_type[0] == 'VORONOI':
        for e in keys.VoronoiExportKeys(): textures_keys_elements.append(e)
    elif req_type[0] == 'WOOD':
        for e in keys.WoodExportKeys(): textures_keys_elements.append(e)
    elif req_type[0] == 'POINT_DENSITY':
        for e in keys.PointExportKeys(): textures_keys_elements.append(e)
    elif req_type[0] == 'IMAGE':
        for e in keys.ImageExportKeys(): textures_keys_elements.append(e)
    elif req_type[0] == 'ENVIRONMENT_MAP':
        for e in keys.EnvironmentExportKeys(): textures_keys_elements.append(e)
    else: 
        for e in keys.VoxelExportKeys(): textures_keys_elements.append(e)

    for e in  textures_keys_elements:
        database_keys_elements.append(e.replace(".",  "_")) 
        
    req = request.DatabaseSelect(database_path, database_keys_elements,"TEXTURES", "where idx_materials =%s" % IdxMaterial(name_object), 'all')
    print(req)
    
    
    
    
    
    
    
    
    ctx_scene.shadertoolsng_utils_bar = (100/step_number) * 2
    
    
