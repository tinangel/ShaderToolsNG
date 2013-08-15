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

import bpy
from . import misc, keys

def SurfaceWireVolumeHalo(api_functions, mat_properties_keys, surface_wire_keys):
    mat_properties = []
    for k in surface_wire_keys:
        if k == "subsurface_scattering.radius": #radius subsurface is an exception
            prop = misc.RemoveRadius(mat_properties_keys[k][0])

        if k != "subsurface_scattering.radius": #radius subsurface is an exception
            prop = misc.RemoveColor(str(eval(mat_properties_keys[k][0])))
        
        prop = misc.RemoveInvalidValues(prop) #remove invalid values
        prop = misc.ConvertBoolStringToNumber(prop) #convert True/False to 0/1
        prop = misc.RemoveExceptions(k, prop)
        c  = misc.ConvertStringProperties(k, keys.StringPropertiesKeys())
        mat_properties.append((k,prop, c))
    return mat_properties
