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

import bpy, shutil,  os, binascii,  time, threading,  platform
from . import misc, keys, request,  textures
from copy import copy

def AddonFolder(default_paths,  active_configuration, api_functions, active_languages,  path):
    browser =''
    if 'None' in str(active_configuration['file_browser']):browser = 'nautilus'
    else: browser =  active_configuration['file_browser']
    navi = { "Windows":'explorer',  "Darwin":'open',  "Linux":browser}
    try: 
        if not path : folder = os.popen('%s "%s"' % (navi[platform.system()],  default_paths['app']))
        else: folder = os.popen('%s "%s"' % (navi[platform.system()],  path))
    except: 
        error = active_languages['menu_error_error052']
        misc.LogAndPrintError((error , error))

def CreateImage(default_paths,  active_configuration, api_functions, active_languages,  image_uv_blob,  idx):
    extension_file = ""
    image_path = ""
    tmp = ""
    if '\\' in image_uv_blob[1]: tmp =  image_uv_blob[1].split('\\')[-1]
    else: tmp =  image_uv_blob[1].split('/')[-1]
    if tmp == '' or not '.' in tmp: extension_file = 'png'
    else: extension_file = tmp.split('.')[-1]
    
    for c in range(1,  100):
        name = "$T_Img_"
        times = time.strftime('%d%m%y%H%M%S',time.localtime()) + str(time.clock())
        times = times.replace('.', '')
        name = "%s%02d" % (name, c) 
        image_path = os.path.join(default_paths['app'], default_paths['temp'],  "%s_%s.%s" % (name, times ,extension_file))     
        image_path = misc.DoubleSlash(image_path)
        if os.path.exists(image_path) == False:break
    try:misc.Clear(image_path , 'files', 'one', active_languages)
    except:pass
    try:
        image_bytes = binascii.unhexlify(eval(image_uv_blob[0]))
        image_file = open(image_path,'wb')
        image_file.write(image_bytes)
        image_file.close()
        img=api_functions['texture_image_load'].replace("#1#", "'%s'" % str(image_path))
        exec("%s = %s" % (api_functions['texture_image'].replace("#1#", str(idx)), str(img)))
        exec("%s" % api_functions['texture_image_pack'].replace("#1#", str(idx)))
        try:misc.Clear(image_path , 'files', 'one', active_languages)
        except: pass
        return True
    except: 
        return False
        pass
        
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
            if req_names[0] != '':
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
    req_type = request.DatabaseSelect(database_path,  ('type', 'name'),"MATERIALS", "where num_materials =%s" % IdxMaterial(name_object), 'one')
    materials_keys_elements = []

    eval(api_functions['material_slot_add'])
    slots = api_functions['material_slots']
    slots = slots.replace("#1#", str(api_functions['material_slots'].replace("[#1#].material", "")) + ".__len__() - 1")
    new_mat = api_functions['materials_new'].replace("#1#", "'%s'" % req_type[1])
    mat_slots = eval(api_functions['material_slots'].replace("[#1#].material", ".__len__()" ))
    exec("%s = %s" % (slots,  new_mat))
    exec("%s = %s" %(api_functions['material_index'],  mat_slots-1))
    exec("%s = '%s'" %(api_functions['type'],  req_type[0]))
    
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
    ImportMaterialRampsInApp(default_paths,  active_configuration, api_functions, active_languages,  name_object,  step_number,   IdxMaterial(name_object))
    ImportTexturesInApp(default_paths,  active_configuration, api_functions, active_languages,  name_object,  step_number,   IdxMaterial(name_object))
   
def ImportTexturesInApp(default_paths,  active_configuration, api_functions, active_languages,  name_object,  step_number,  idx_materials):
    ctx_scene = eval(api_functions['context_scene'])
    database_path = misc.ConvertMarkOut(active_configuration['database_path'], default_paths['app'])
    req_type = request.DatabaseSelect(database_path,  ('type', 'name',  'num_textures',  'texture_use_alpha'),"TEXTURES", "where idx_materials =%s" % IdxMaterial(name_object), 'all')
    # Create textures slots : 
    idx = 0
    for t in req_type:
        new_texture = api_functions['texture_slots_new'].replace("#1#", "'%s'" % t[1]) 
        new_texture = eval(new_texture.replace("#2#", "'%s'" % t[0]))
        slot = eval(api_functions['texture_slots_add'])
        slot.texture = new_texture
        texture_type = api_functions['texture_slots_texture_type'].replace("#1#", "%s" % idx)
        texture_use_alpha = api_functions['texture_use_preview_alpha'].replace("#1#", "%s" % idx)
        #Create textures keys:
        textures_keys_elements = []
        keys_elements = []
        database_keys_elements = []

        for e in keys.InfluenceExportKeys(): textures_keys_elements.append(e)
        for e in keys.MappingExportKeys(): textures_keys_elements.append(e)
        for e in keys.ColorsExportKeys(): textures_keys_elements.append(e)
        exec("%s = '%s'" % (texture_type, t[0]))
        try:exec("%s = %s" % (texture_use_alpha, t[3]))        
        except:pass
        if not t[0] == 'NONE':
            if t[0] == 'BLEND':
                for e in keys.BlendExportKeys(): textures_keys_elements.append(e)
            elif t[0] == 'NOISE': None
            elif t[0] == 'CLOUDS':
                for e in keys.CloudsExportKeys(): textures_keys_elements.append(e)
            elif t[0] == 'DISTORTED_NOISE':
                for e in keys.DistortedExportKeys(): textures_keys_elements.append(e)
            elif t[0] == 'MAGIC':
                for e in keys.MagicExportKeys(): textures_keys_elements.append(e)    
            elif t[0] == 'MARBLE':
                for e in keys.MarbleExportKeys(): textures_keys_elements.append(e)
            elif t[0] == 'MUSGRAVE':
                for e in keys.MusgraveExportKeys(): textures_keys_elements.append(e)
            elif t[0] == 'STUCCI':
                for e in keys.StucciExportKeys(): textures_keys_elements.append(e)
            elif t[0] == 'VORONOI': 
                for e in keys.VoronoiExportKeys(): textures_keys_elements.append(e)
            elif t[0] == 'WOOD':
                for e in keys.WoodExportKeys(): textures_keys_elements.append(e)
            elif t[0] == 'POINT_DENSITY':
                for e in keys.PointExportKeys(): textures_keys_elements.append(e)
            elif t[0] == 'IMAGE':
                req_image_uv_blob = request.DatabaseSelect(database_path,  ('image_uv_blob', 'texture_image_filepath', 'name', ),"TEXTURES", "where idx_materials =%s and num_textures=%s" % (IdxMaterial(name_object),  t[2]), 'one')
                if req_image_uv_blob : CreateImage(default_paths,  active_configuration, api_functions, active_languages,  req_image_uv_blob,  idx)
                for e in keys.ImageExportKeys(): textures_keys_elements.append(e)
                textures_keys_elements.remove("texture.image.source")
            elif t[0] == 'ENVIRONMENT_MAP':
                for e in keys.EnvironmentExportKeys(): textures_keys_elements.append(e)
            else: 
                for e in keys.VoxelExportKeys(): textures_keys_elements.append(e)
            for e in  textures_keys_elements: 
                keys_elements.append(e)
                database_keys_elements.append(e.replace(".",  "_")) 
            req = request.DatabaseSelect(database_path, database_keys_elements,"TEXTURES", "where num_textures = %s" % t[2], 'one')
            if not req == [] and not req == False:
                c = 0
                for v in req:
                    propertie = keys.TexturesPropertiesKeys(api_functions)[keys_elements[c]][0].replace("#1#", str(idx))
                    propertie = propertie.replace("[#2#]", "")
                    if type(v).__name__ == 'str' : 
                        if not "(" in v: v = "'%s'" %v
                    try: exec("%s = %s" % (propertie, v))
                    except: pass
                    c = c + 1
                ImportTextureRampsInApp(default_paths,  active_configuration, api_functions, active_languages,  step_number, idx,  t[2])
                idx = idx + 1
    ctx_scene.shadertoolsng_utils_bar = (100/step_number) * 5
    
def ImportTextureRampsInApp(default_paths,  active_configuration, api_functions, active_languages, step_number, new_idx,  idx_textures):
    ctx_scene = eval(api_functions['context_scene'])
    database_path = misc.ConvertMarkOut(active_configuration['database_path'], default_paths['app'])
    
    ramp_list = []
    for p in keys.RampsKeys("color"):ramp_list.append(p.replace(".",  "_"))
    req_color_ramps = request.DatabaseSelect(database_path,  ramp_list,"COLOR_RAMPS", "where idx_textures =%s" % idx_textures, 'all')

    ramp_list = []
    for p in keys.RampsKeys("point_density_color"):ramp_list.append(p.replace(".",  "_"))
    req_pointdensity_ramps = request.DatabaseSelect(database_path, ramp_list,"POINTDENSITY_RAMPS", "where idx_textures =%s" %  idx_textures, 'all')
    requests_ramps = \
        {
         "texture_use_color_ramp":req_color_ramps, "texture_point_density_color_source":req_pointdensity_ramps,  
        }
    #Active ramps:
    for r in requests_ramps:
        if requests_ramps[r] != False and requests_ramps[r] != []:
            try: exec("%s = True" % api_functions[r].replace("#1#", str(new_idx)))
            except: pass
            #Import ramps new positions:
            c = 0
            if requests_ramps[r].__len__() > 2:
                for e in requests_ramps[r]:
                    if c > 1:   
                        type_ramp = r.replace("texture_use_",  "")
                        exec(api_functions['ramps_new_2'] % (str(new_idx),  type_ramp,  str(e[0])))
                    c = c + 1
            #Import ramps elements:
            c = 0
            for e in requests_ramps[r]:
                type_ramp = r.replace("_use_",  "_")
                type_ramp_2 = r.split("_",  2)[-1]
                my_temp_list = \
                    (
                     (api_functions['%s_elements_position' % type_ramp].replace("#1#", str(new_idx)).replace("#2#", str(c)), str(e[0]), False), 
                     (api_functions['%s_elements_color' % type_ramp].replace("#1#", str(new_idx)).replace("#2#", str(c)), str(e[1]), False),                    
                     (api_functions['%s_interpolation' % type_ramp].replace("#1#", str(new_idx)).replace("#2#", str(c)), str(e[2]), True),
                    )
                    
                for k in my_temp_list:
                    if k[2]: exec("%s = '%s'" % (k[0],  k[1]))
                    else: exec("%s = %s" % (k[0],  k[1]))
                c = c + 1
    ctx_scene.shadertoolsng_utils_bar = (100/step_number) * 3
    
def ImportMaterialRampsInApp(default_paths,  active_configuration, api_functions, active_languages,  name_object,  step_number,  idx_materials):
    ctx_scene = eval(api_functions['context_scene'])
    database_path = misc.ConvertMarkOut(active_configuration['database_path'], default_paths['app'])
    req_textures = request.DatabaseSelect(database_path,  ('num_textures', ), "TEXTURES", "where idx_materials =%s" % IdxMaterial(name_object), 'all')
    
    ramp_list = []
    for p in keys.RampsKeys("diffuse"):ramp_list.append(p.replace(".",  "_"))
    req_diffuse_ramps = request.DatabaseSelect(database_path,  ramp_list,"DIFFUSE_RAMPS", "where idx_materials =%s" % IdxMaterial(name_object), 'all')

    ramp_list = []
    for p in keys.RampsKeys("specular"):ramp_list.append(p.replace(".",  "_"))
    req_specular_ramps = request.DatabaseSelect(database_path, ramp_list,"SPECULAR_RAMPS", "where idx_materials =%s" % IdxMaterial(name_object), 'all')
    requests_ramps = \
        {
         "use_diffuse_ramp":req_diffuse_ramps,  "use_specular_ramp":req_specular_ramps, 
        }
    #Active ramps:
    for r in requests_ramps:
        if requests_ramps[r] and not requests_ramps[r] == []:
            try: exec("%s = True" % api_functions[r])
            except: pass
            #Import ramps new positions:
            c = 0
            if requests_ramps[r].__len__() > 2:
                for e in requests_ramps[r]:
                    if c > 1:   
                        type_ramp = r.split("_",  1)[-1]                
                        exec(api_functions['ramps_new'] % (type_ramp,  str(e[0])))
                    c = c + 1
            #Import ramps elements:
            c = 0
            for e in requests_ramps[r]:
                type_ramp = r.split("_",  1)[-1]
                my_temp_list = \
                    (
                     (api_functions['%s_elements_position' % type_ramp].replace("#1#", str(c)), str(e[0]), False), 
                     (api_functions['%s_elements_color' % type_ramp].replace("#1#", str(c)), str(e[1]), False),                    
                     (api_functions['%s_blend' % type_ramp].replace("#1#", str(c)), str(e[2]), True),
                     (api_functions['%s_input' % type_ramp].replace("#1#", str(c)), str(e[3]), True),
                     (api_functions['%s_factor' % type_ramp].replace("#1#", str(c)), str(e[4]), False),
                     (api_functions['%s_interpolation' % type_ramp].replace("#1#", str(c)), str(e[5]), True),
                    )
                for k in my_temp_list:
                    if k[2]: exec("%s = '%s'" % (k[0],  k[1]))
                    else: exec("%s = %s" % (k[0],  k[1]))
                c = c + 1
    ctx_scene.shadertoolsng_utils_bar = (100/step_number) * 2
