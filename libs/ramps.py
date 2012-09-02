# ##### BEGIN GPL LICENSE BLOCK #####
#
# This work is licensed under a Creative 
# Commons Attribution-NonCommercial-ShareAlike 
# 3.0 Unported License : 
#
# More details here : http://creativecommons.org/licenses/by-nc-sa/3.0/deed.fr
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>
import bpy
from . import misc, keys
from copy import copy

def Ramps(api_functions, ramps_prop, ramps_keys, type_ramp, idx_texture):
    ramp_properties_final = {}
    ramp_properties = {}
    first = True
    range_elements = '' 
    if type_ramp == 'color' or type_ramp == 'point_density_color':
        type_ramp = 'texture_' + type_ramp
        range_elements = eval(api_functions['%s_ramp_elements' % type_ramp].replace("#1#", str(idx_texture))).__len__()
    else:
        range_elements = eval(api_functions['%s_ramp_elements' % type_ramp]).__len__()

    for p in range(0, range_elements):
        ramps_prop_temp = copy(ramps_prop)
        ramp_properties_final[str(p)] = {}
        for k in ramps_keys:
            if type_ramp == 'texture_color' or type_ramp == 'texture_point_density_color':
                val = copy(ramps_prop_temp[k][0].replace("#1#", str(idx_texture)))
                val = val.replace("#2#", str(p))
            else: val = copy(ramps_prop_temp[k][0].replace("#1#", str(p)))
            val2 = copy(val)
            if k.find("elements.color") >= 0:
                val = misc.RemoveRampsColor(val)
            ramps_prop_temp[k] = tuple((val, ramps_prop_temp[k][1]))
            if k.find("elements.color") >= 0:
               ramp_properties[k] = (copy(val2), copy(str(eval(ramps_prop_temp[k][0]))))
            else:
               ramp_properties[k] = (copy(val), copy(str(eval(ramps_prop_temp[k][0]))))
        ramp_properties_final[str(p)] = copy(ramp_properties)
    return ramp_properties_final

def RemoveElements(exception, list):
    c = 0
    n = 0
    val = ""
    for e in list:
        if e.find(exception) >= 0:
            n = n + 1
            val = copy(e)
    list.reverse()
    for p in range(0, n-1):
        try:
            list.remove(val)
        except:
            print("Error : %s" % val)
            pass
    return list.reverse()

def RampsPositions(api_functions, type_ramp, idx_texture):
    ramp_positions = []
    ramps_numbers = ''
    if type_ramp == 'color' or type_ramp == 'point_density_color':
        type_ramp = 'texture_' + type_ramp
        ramps_numbers = eval(api_functions['%s_ramp_elements' % type_ramp].replace("#1#", str(idx_texture))).__len__()
    else : ramps_numbers = eval(api_functions['%s_ramp_elements' % type_ramp]).__len__()
    for p in range(1, ramps_numbers-1):
        ramp_positions.append("%s.new(position=%s)\n" % (api_functions['%s_ramp_elements' % type_ramp].replace("#1#", str(idx_texture)), eval(api_functions['%s_ramp_elements' % type_ramp].replace("#1#", str(idx_texture)))[p].position))

    return ramp_positions


