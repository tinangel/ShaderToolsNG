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

import bpy, shutil,  os, binascii, threading
from . import misc, keys, request,  render,  materials,  ramps,  textures
from copy import copy

def InformationsRemove(num_material,  api_functions,  num_informations):
    elements_keys =[]
    elements_val = []
    for e in keys.InformationsKeys():
        elements_keys.append(e)
        if e == "idx_materials": elements_val.append(num_material)
        elif e == "num_informations": elements_val.append(num_informations)
        else: elements_val.append('')
    
    condition = ""
    for k in range(0,  elements_keys.__len__()):
        if elements_val[k] == '': condition = condition + "%s = ''" % elements_keys[k] + ", " 
        else: condition = condition + "%s = %s" % (elements_keys[k], elements_val[k]) + ", " 
    
    condition = condition.strip()
    condition = condition.rstrip(",")
    return condition

def RenderRemove(num_material,  api_functions,  num_render):
    elements_keys =[]
    elements_val = []
    for e in keys.RenderKeys():
        elements_keys.append(e)
        if e == "idx_materials": elements_val.append(num_material)
        elif e == "num_render": elements_val.append(num_render)
        else: elements_val.append('')
    
    condition = ""
    for k in range(0,  elements_keys.__len__()):
        if elements_val[k] == '': condition = condition + "%s = ''" % elements_keys[k] + ", " 
        else: condition = condition + "%s = %s" % (elements_keys[k], elements_val[k]) + ", " 
    
    condition = condition.strip()
    condition = condition.rstrip(",")
    return condition

def MaterialRemove(num_material,  api_functions):
    elements_keys =[]
    elements_val = []
    for e in keys.MaterialsSaveKeys():
        elements_keys.append(e)
        if e == "num_materials": elements_val.append(num_material)
        else: elements_val.append('')
        
    keys_props = (keys.SurfaceWireKeys(),  keys.VolumeKeys(),  keys.HaloKeys())
    for k in keys_props:     
        mat_properties = materials.SurfaceWireVolumeHalo(api_functions, keys.MaterialsPropertiesKeys(api_functions), k)
        for e in mat_properties:
            elements_keys.append(e[0].replace('.',  '_'))
            elements_val.append('')
    
    condition = ""
    for k in range(0,  elements_keys.__len__()):
        if elements_val[k] == '': condition = condition + "%s = ''" % elements_keys[k] + ", " 
        else: condition = condition + "%s = %s" % (elements_keys[k], elements_val[k]) + ", " 
    
    condition = condition.strip()
    condition = condition.rstrip(",")
    return condition

def TexturesRemove(num_material,  api_functions,  default_paths,  num_textures):
    ctx_mat = copy(api_functions['context_material'])
    ctx_texture = copy(api_functions['context_texture'])
    elements_keys =[]
    elements_val = []

    exceptions = ("texture.noise_scale_2",  "texture.environment_map.zoom",  "texture.point_density.vertex_cache_space",  )
    for p in keys.TexturesSaveKeys(): 
        if p not in exceptions: elements_keys.append(p.replace('.',  '_'))
        if p == "num_textures": elements_val.append(num_textures[0])
        elif p =="idx_materials": elements_val.append(num_material)
        elif p in exceptions: None
        else:elements_val.append('')
        
    for p in keys.TexturesPropertiesKeys(api_functions):
        if p not in exceptions: elements_keys.append(p.replace('.',  '_'))
        if p in exceptions: None
        else: elements_val.append('')

    for p in keys.TexturesOtherSaveKeys():
        if p not in exceptions: elements_keys.append(p.replace('.',  '_'))
        if p in exceptions: None
        else: elements_val.append('')
    
    elements_keys.append("influence_color")
    elements_val.append('')
    condition = ""
    for k in range(0,  elements_keys.__len__()):
        if elements_val[k] == '': condition = condition + "%s = ''" % elements_keys[k] + ", " 
        else: condition = condition + "%s = %s" % (elements_keys[k], elements_val[k]) + ", " 
    
    condition = condition.strip()
    condition = condition.rstrip(",")
    return condition

def RampsRemove(num_material,  api_functions,  default_paths,  num_ramps,  type_ramp):
    ctx_mat = copy(api_functions['context_material'])
    ctx_texture = copy(api_functions['context_texture'])
    elements_keys =[]
    elements_val = []

    for p in keys.RampsKeys(type_ramp): 
        elements_keys.append(p.replace('.',  '_'))
        idx_ramps_key = "num_%s_ramps" % type_ramp
        if p == idx_ramps_key: elements_val.append(num_ramps[0])
        elif p =="idx_materials": elements_val.append(num_material)
        else:elements_val.append('')

    condition = ""
    for k in range(0,  elements_keys.__len__()):
        if elements_val[k] == '': condition = condition + "%s = ''" % elements_keys[k] + ", " 
        else: condition = condition + "%s = %s" % (elements_keys[k], elements_val[k]) + ", " 
    
    condition = condition.strip()
    condition = condition.rstrip(",")
    return condition
    
