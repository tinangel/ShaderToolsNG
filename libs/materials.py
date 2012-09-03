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
 
def MaterialMigrateV1V2(path, api_functions, active_language, active_configuration, default_paths):
    print("test")
