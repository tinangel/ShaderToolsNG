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
import bpy
from . import misc, keys
from copy import copy

def Ramps(api_functions, ramps_prop, ramps_keys, type_ramp):
    ramp_properties_final = {}
    ramp_properties = {}
    first = True
    for p in range(0, eval(api_functions['%s_ramp_elements' % type_ramp]).__len__()):
        ramps_prop_temp = copy(ramps_prop)
        ramp_properties_final[str(p)] = {}
        for k in ramps_keys:
            val = copy(ramps_prop_temp[k][0].replace("#1#", str(p)))
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
        except: pass
    return list.reverse()

def RampsPositions(api_functions, type_ramp):
    ramp_positions = []
    ramps_numbers = eval(api_functions['%s_ramp_elements' % type_ramp]).__len__()
    for p in range(1, ramps_numbers-1):
        ramp_positions.append("%s.new(position=%s)\n" % (api_functions['%s_ramp_elements' % type_ramp], eval(api_functions['%s_ramp_elements' % type_ramp])[p].position))

    return ramp_positions