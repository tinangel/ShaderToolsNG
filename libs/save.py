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
from . import misc, keys, request,  render,  materials,  ramps
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
