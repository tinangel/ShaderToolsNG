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
    if type_ramp == 'diffuse':
        ramp_properties_final = {}
        ramp_properties = {}
        first = True
        
        for p in range(0, eval(api_functions['diffuse_ramp_elements']).__len__()):
            ramps_prop_temp = copy(ramps_prop)
            ramp_properties_final[str(p)] = {}
            for k in ramps_keys:
                if p == 0:
                    val = ramps_prop_temp[k][0].replace("#1#", str(p))
                    val2 = copy(val)
                    if k.find("elements.color") >= 0:
                        val = misc.RemoveRampsColor(val)
                    ramps_prop_temp[k] = tuple((val, ramps_prop_temp[k][1]))
                    if k.find("elements.color") >= 0:
                        ramp_properties[k] = (val2, str(eval(ramps_prop_temp[k][0])))
                    else:
                        ramp_properties[k] = (val, str(eval(ramps_prop_temp[k][0])))
                    ramp_properties_final[str(p)] = ramp_properties
                else:
                    exception = False
                    if first:
                        ramp_properties = {}
                        first = False
                    
                    for e in keys.ExceptionsRampsKeys():
                        if k.find(e) >= 0:
                            exception = True
                            break
                    if exception == False:
                        val = ramps_prop_temp[k][0].replace("#1#", str(p))
                        val2 = copy(val)
                        if k.find(".elements.color") >= 0:
                            val = misc.RemoveRampsColor(val)
                        
                        if k.find(".elements.position") >= 0:
                            first = True
                        
                        ramps_prop_temp[k] = tuple((val, ramps_prop_temp[k][1]))
                        if k.find("elements.color") >= 0:
                            ramp_properties[k] = (val2, str(eval(ramps_prop_temp[k][0])))
                        else:
                            ramp_properties[k] = (val, str(eval(ramps_prop_temp[k][0])))
                        ramp_properties_final[str(p)] = ramp_properties
        print(ramp_properties_final)
        return ramp_properties_final
