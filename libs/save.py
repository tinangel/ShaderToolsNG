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

import bpy, shutil,  os, binascii, threading, platform
from . import misc, keys, request,  render,  materials,  ramps,  textures
from copy import copy

def InformationsSave(material_dict, api_functions, active_language, active_configuration, test):
    elements_val = []
    for e in keys.InformationsKeys(): elements_val.append(material_dict[e]) 
    if  test: return request.DatabaseInsert(material_dict['paths']['database'], keys.InformationsKeys(), elements_val, "INFORMATIONS",  True,  'save')
    else: return request.DatabaseInsert(material_dict['paths']['database'], keys.InformationsKeys(), elements_val, "INFORMATIONS",  False,  'save')

def RenderSave(material_dict, api_functions, active_language, active_configuration, test, default_paths):
    preview_name = render.PreviewRenderInternal(default_paths, api_functions, active_configuration, active_language, material_dict,  'save')
    elements_val = []
    new_keys = []
    for e in keys.RenderKeys():
        #filter keys 
        exception = False
        if( bpy.app.version[0] == 2 and bpy.app.version[1] >= 65 ):
            if( e == "render_color_management" ):   exception = True
        
        if( exception ): continue
        
        new_keys.append( e )
        try: elements_val.append(material_dict[e]) 
        except : 
            if e == "render_preview_object":
                print( preview_name )
                if os.path.exists(preview_name):
                    byte_preview = open(preview_name, 'rb')
                    elements_val.append(byte_preview.read())
                    byte_preview.close()
                    misc.Clear(preview_name, 'files', 'one', active_language)
                else: return False
            else:
                val = eval(api_functions[e])
                if type(val).__name__ == 'bool': val = misc.ConvertBoolStringToNumber(val)
                elements_val.append(val)
                
    if  test: return request.DatabaseInsert(material_dict['paths']['database'], new_keys, elements_val, "RENDER",  True, 'save')
    else: return request.DatabaseInsert(material_dict['paths']['database'], new_keys, elements_val, "RENDER",  False, 'save')

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
            
    if  test: return request.DatabaseInsert(material_dict['paths']['database'],elements_keys, elements_val, "MATERIALS",  True, 'save')
    else: return request.DatabaseInsert(material_dict['paths']['database'], elements_keys, elements_val, "MATERIALS",  False, 'save')

def TexturesSave(material_dict, api_functions, active_language, active_configuration, test):
    ctx_mat = copy(api_functions['context_material'])
    ctx_texture = copy(api_functions['context_texture'])
    current_texture = eval(api_functions['texture_slots_values'])
    return_request = []
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
                elif e == "idx_point_density_color_ramp":  elements_val.append(material_dict[e])
                elif e == "use_textures":  elements_val.append(material_dict[e])
                elif e == "name":  elements_val.append(copy(texture_name))
                elif e == "texture_use_preview_alpha":  elements_val.append(copy(preview_alpha))
                elif e == "num_textures": 
                    try: 
                        material_dict[e] = request.DatabaseMax(material_dict['paths']['database'], "num_textures", "TEXTURES", "", 'one')[0] + 1 + t
                        elements_val.append(material_dict[e])
                    except: return False
                elif e in ("color",  "scale"):
                    texture_structure = []
                    texture_structure = textures.TexturesPropertiesExport(api_functions, texture_structure, (e, ), t, active_language)
                    tmp = texture_structure[0].split("=")
                    val = tmp[-1].strip()
                    elements_val.append(val)
                else:
                    try:
                        val = ''
                        if e == "image_uv_blob" and texture_type == 'IMAGE':
                            source = eval(api_functions["texture_image_source"].replace("#1#", str(t)))
                            if source == 'FILE':
                                img_filepath = eval(api_functions["texture_image_filepath"].replace("#1#", str(t)))
                                if platform.system() == 'Windows': img_filepath = misc.DoubleSlash(img_filepath)
                                img_filepath_2 = copy(img_filepath) 
                                img_filepath = bpy.path.abspath(img_filepath, start=None, library=None)
                                if '\\' in img_filepath: new_img_path = os.path.join(material_dict['paths']['temp'],  img_filepath.split('\\')[-1])
                                else: new_img_path = os.path.join(material_dict['paths']['temp'],  img_filepath.split('/')[-1])
                                if platform.system() == 'Windows': new_img_path = misc.DoubleSlash(new_img_path)
                                try:
                                    exec("%s = '%s'" % (api_functions["texture_image_filepath"].replace("#1#", str(t)), new_img_path))
                                    unpack = api_functions['texture_image_unpack'].replace("#1#", str(t))
                                    exec("%s" % unpack.replace("#2#", "'WRITE_ORIGINAL'"))
                                    pack = eval(api_functions['texture_image_pack'].replace("#1#", str(t)))
                                    exec("%s = '%s'" % (api_functions["texture_image_filepath"].replace("#1#", str(t)), img_filepath_2))                                    
                                except:pass                                
                                if os.path.exists(img_filepath) or os.path.exists(new_img_path):
                                    try:shutil.copy2(img_filepath,  new_img_path)
                                    except:pass
                                    byte_preview = open(new_img_path, 'rb')
                                    val = byte_preview.read()
                                    byte_preview.close()
                                    misc.Clear(new_img_path, 'files', 'one', active_language)
                            elif source == 'GENERATED':
                                list = textures.TexturesGeneratedImagesExport(api_functions, material_dict, t, active_language)
                                if os.path.exists(list[3]):
                                    byte_preview = open(list[3], 'rb')
                                    val = byte_preview.read()
                                    byte_preview.close()
                                    misc.Clear(list[3], 'files', 'one', active_language)
                        elif e == "texture_image_filepath" or e == "texture_image_filepath_raw":
                            source = eval(api_functions["texture_image_source"].replace("#1#", str(t)))
                            img_filepath = eval(api_functions["texture_image_filepath"].replace("#1#", str(t)))
                            if '\\' in img_filepath: val = os.path.join(material_dict['paths']['temp'],  img_filepath.split('\\')[-1])
                            else: val = os.path.join(material_dict['paths']['temp'],  img_filepath.split('/')[-1])
                        else: val = eval(api_functions[e].replace("#1#", str(t)))
                        elements_val.append( misc. ConvertBoolStringToNumber(val))
                    except: elements_val.append('')
            color_ramps = True
            point_ramps = True
            try:
                if eval(api_functions['texture_use_color_ramp'].replace("#1#", str(t))):
                    return_request.append(RampsSave(material_dict, api_functions, active_language, active_configuration, 'color',  True,  t))
                ramp_point =  copy(api_functions['texture_point_density_color_source'].replace("#1#", str(t)))
                
                if eval(ramp_point) == 'PARTICLE_SPEED' or eval(ramp_point) == 'PARTICLE_AGE':
                    return_request.append(RampsSave(material_dict, api_functions, active_language, active_configuration, 'point_density_color',  True,  t))
            except: pass
            
            if  test: 
                try:
                        return_request.append(request.DatabaseInsert(material_dict['paths']['database'],elements_keys, elements_val, "TEXTURES",  True, 'save'))
                except: return False
            else: 
                request.DatabaseInsert(material_dict['paths']['database'], elements_keys, elements_val, "TEXTURES",  False, 'save')
                try:
                    if eval(api_functions['texture_use_color_ramp'].replace("#1#", str(t))):
                        RampsSave(material_dict, api_functions, active_language, active_configuration, 'color',  False,  t)
                    
                    ramp_point =  copy(api_functions['texture_point_density_color_source'].replace("#1#", str(t)))
                    if eval(ramp_point) == 'PARTICLE_SPEED' or eval(ramp_point) == 'PARTICLE_AGE':
                        point_ramps = RampsSave(material_dict, api_functions, active_language, active_configuration, 'point_density_color',  False,  t)
                except: pass
    return (True,  return_request)

def RampsSave(material_dict, api_functions, active_language, active_configuration, type_ramp,  test,  idx_texture):
    elements_keys = []
    elements_val = []
    return_request = []
    ramp_properties = ''
    ramp_properties = ramps.Ramps(api_functions, keys.RampsPropertiesKeys(api_functions), keys.RampsKeys(type_ramp), type_ramp, idx_texture)
    for v in range(0,  ramp_properties.__len__()):
        elements_keys = []
        elements_val = []
        if type_ramp == 'point_density_color': type_ramp = 'point_density'
        elements_keys .append('num_%s_ramps' % type_ramp)
        elements_keys .append('idx_materials')
        if type_ramp == 'color': 
            elements_keys .append('idx_textures')
            elements_val .append(material_dict['idx_%s_ramp' % type_ramp] + v)
            elements_val .append(material_dict['idx_materials'] )
            elements_val .append(request.DatabaseMax(material_dict['paths']['database'], "num_textures", "TEXTURES", "", 'one')[0]+1 + idx_texture)
        elif type_ramp == 'point_density': 
            elements_keys .append('idx_textures')
            elements_val .append(material_dict['idx_point_density_color_ramp'] + v)
            elements_val .append(material_dict['idx_materials'] )
            elements_val .append(request.DatabaseMax(material_dict['paths']['database'], "num_textures", "TEXTURES", "", 'one')[0]+1 +  idx_texture)
        else: 
            elements_val .append(material_dict['idx_%s_ramp' % type_ramp] + v)
            elements_val .append(material_dict['idx_materials'] )

        for e in ramp_properties[str(v)]: 
            if type_ramp == 'point_density': 
                tmp = e.replace('_color',  '')
                elements_keys.append(tmp.replace('.',  '_'))
            else: elements_keys.append(e.replace('.',  '_'))
            elements_val.append(ramp_properties[str(v)][e][1])

        if  test:            
            if type_ramp == 'point_density': return_request.append(request.DatabaseInsert(material_dict['paths']['database'],elements_keys, elements_val, "POINTDENSITY_RAMPS",  True, 'save'))
            else: return_request.append(request.DatabaseInsert(material_dict['paths']['database'],elements_keys, elements_val, "%s_RAMPS" % type_ramp.capitalize(),  True, 'save'))
            if v == ramp_properties.__len__()-1: return (True, return_request)
        else:
            if type_ramp == 'point_density': request.DatabaseInsert(material_dict['paths']['database'],elements_keys, elements_val, "POINTDENSITY_RAMPS",  False, 'save') 
            else: request.DatabaseInsert(material_dict['paths']['database'], elements_keys, elements_val, "%s_RAMPS" % type_ramp.capitalize(),  False, 'save')
