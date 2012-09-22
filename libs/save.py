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

import bpy, shutil,  os, binascii, threading
from . import misc, keys, request,  render,  materials,  ramps,  textures
from copy import copy

def InformationsSave(material_dict, api_functions, active_language, active_configuration, test):
    elements_val = []
    for e in keys.InformationsKeys(): elements_val.append(material_dict[e]) 
    if  test: return request.DatabaseInsert(material_dict['paths']['database'], keys.InformationsKeys(), elements_val, "INFORMATIONS",  True)
    else: return request.DatabaseInsert(material_dict['paths']['database'], keys.InformationsKeys(), elements_val, "INFORMATIONS",  False)

def RenderSave(material_dict, api_functions, active_language, active_configuration, test):
    preview_name = render.PreviewRenderInternal(api_functions, active_configuration, material_dict)
    elements_val = [] 
    for e in keys.RenderKeys(): 
        try: elements_val.append(material_dict[e]) 
        except : 
            if e == "render_preview_object":
                preview_path = os.path.join(material_dict['paths']['temp'],  preview_name)
                if os.path.exists(preview_path):
                    byte_preview = open(preview_path, 'rb')
                    elements_val.append(byte_preview .read())
                    misc.Clear(preview_path, 'files', 'one', active_language)
                else: return False
            else: 
                val = eval(api_functions[e])
                if type(val).__name__ == 'bool': val = misc.ConvertBoolStringToNumber(val)
                elements_val.append(val)
                
    if  test: return request.DatabaseInsert(material_dict['paths']['database'], keys.RenderKeys(), elements_val, "RENDER",  True)
    else: return request.DatabaseInsert(material_dict['paths']['database'], keys.RenderKeys(), elements_val, "RENDER",  False)

def MaterialSave(material_dict, api_functions, active_language, active_configuration, test):
    elements_keys =[]
    elements_val = []
    for e in keys.MaterialsSaveKeys():
        elements_keys.append(e)
        elements_val.append(material_dict[e])
        
    keys_props = (keys.SurfaceWireKeys(),  keys.VolumeKeys(),  keys.HaloKeys())
    for k in keys_props:     
        mat_properties = materials.SurfaceWireVolumeHalo(api_functions, keys.MaterialsPropertiesKeys(api_functions), k)
        for e in mat_properties:
            elements_keys.append(e[0].replace('.',  '_'))
            elements_val.append(e[1])
            
    if  test: return request.DatabaseInsert(material_dict['paths']['database'],elements_keys, elements_val, "MATERIALS",  True)
    else: return request.DatabaseInsert(material_dict['paths']['database'], elements_keys, elements_val, "MATERIALS",  False)

def TexturesSave(material_dict, api_functions, active_language, active_configuration, test):
    ctx_mat = copy(api_functions['context_material'])
    ctx_texture = copy(api_functions['context_texture'])
    current_texture = eval(api_functions['texture_slots_values'])
    for t in range(0, current_texture.__len__()):
        texture_type = 'NONE'
        try :texture_type = copy(eval(api_functions['texture_slots_texture_type'].replace("#1#", str(t))))
        except:pass
        if texture_type != 'NONE' and eval(api_functions['use_textures'].replace('#1#', str(t))):
            texture_name = copy(eval(api_functions['texture_slots_texture_name'].replace("#1#", str(t))))
            preview_alpha = eval(api_functions['texture_use_preview_alpha'].replace("#1#", str(t))) 
            elements_keys =[]
            elements_val = []
            all_keys = []
            for p in keys.TexturesSaveKeys(): all_keys.append(p)
            for p in keys.TexturesPropertiesKeys(api_functions): all_keys.append(p)
            for p in keys.TexturesOtherSaveKeys(): all_keys.append(p)
            for exceptions in ("texture_use_alpha",  "texture.noise_scale_2",  "texture.environment_map.zoom",  "texture.point_density.vertex_cache_space"):
                all_keys.remove(exceptions)
            
            for k in all_keys: elements_keys .append(k.replace(".",  '_'))
            for e in elements_keys:
                if e == "type": elements_val.append(copy(texture_type))
                elif e == "idx_materials":  elements_val.append(material_dict[e])
                elif e == "idx_color_ramp":  elements_val.append(material_dict[e])
                elif e == "idx_point_density_ramp":  elements_val.append(material_dict[e])
                elif e == "use_textures":  elements_val.append(material_dict[e])
                elif e == "name":  elements_val.append(copy(texture_name))
                elif e == "texture_use_alpha":  elements_val.append(copy(preview_alpha))
                elif e == "num_textures": 
                    try: 
                        material_dict[e] = request.DatabaseMax(material_dict['paths']['database'], "num_textures", "TEXTURES", "", 'one')[0] + 1
                        elements_val.append(material_dict[e])
                    except: return False
                else: 
                    try:
                        val = ''
                        if e == "image_uv_blob" and texture_type == 'IMAGE':
                            source = eval(api_functions["texture_image_source"].replace("#1#", str(t)))
                            if source == 'FILE':
                                img_filepath = eval(api_functions["texture_image_filepath"].replace("#1#", str(t)))                            
                                img_filepath = bpy.path.abspath(img_filepath, start=None, library=None)
                                if os.path.exists(img_filepath):
                                    new_img_path = os.path.join(material_dict['paths']['temp'],  img_filepath.split(os.sep)[-1])
                                    shutil.copy2(img_filepath,  new_img_path)
                                    byte_preview = open(new_img_path, 'rb')
                                    val = byte_preview .read()
                                    misc.Clear(new_img_path, 'files', 'one', active_language)
                            elif source == 'GENERATED':
                                list = textures.TexturesGeneratedImagesExport(api_functions, material_dict, t, active_language)
                                if os.path.exists(list[3]):
                                    byte_preview = open(list[3], 'rb')
                                    val = byte_preview .read()
                                    misc.Clear(list[3], 'files', 'one', active_language)
                        else: val = eval(api_functions[e].replace("#1#", str(t)))
                        elements_val.append( misc. ConvertBoolStringToNumber(val))
                    except: elements_val.append('')

            if  test: 
                try: 
                    request.DatabaseInsert(material_dict['paths']['database'],elements_keys, elements_val, "TEXTURES",  True)
                except: return False
            else: request.DatabaseInsert(material_dict['paths']['database'], elements_keys, elements_val, "TEXTURES",  False)
    
    return True




def RampsSave(material_dict, api_functions, active_language, active_configuration, type_ramp,  test):
    elements_keys = []
    elements_val = []
    ramp_properties = ramps.Ramps(api_functions, keys.RampsPropertiesKeys(api_functions), keys.RampsKeys(type_ramp), type_ramp, '')
    for v in range(0,  ramp_properties.__len__()):
        elements_keys = []
        elements_val = []
        if type_ramp == 'diffuse' or type_ramp == 'specular': 
            elements_keys .append('num_%s_ramps' % type_ramp)
            elements_keys .append('idx_materials')
            elements_val .append(material_dict['idx_%s_ramp' % type_ramp] + v)
            elements_val .append(material_dict['idx_materials'] )

        for e in ramp_properties[str(v)]: 
            elements_keys.append(e.replace('.',  '_'))
            elements_val.append(ramp_properties[str(v)][e][1])

        if  test:
            if type_ramp == 'diffuse' or type_ramp == 'specular': 
                request.DatabaseInsert(material_dict['paths']['database'],elements_keys, elements_val, "%s_RAMPS" % type_ramp.capitalize(),  True)
            if v == ramp_properties.__len__()-1: return True
        else: 
            if type_ramp == 'diffuse' or type_ramp == 'specular': 
                request.DatabaseInsert(material_dict['paths']['database'], elements_keys, elements_val, "%s_RAMPS" % type_ramp.capitalize(),  False)
