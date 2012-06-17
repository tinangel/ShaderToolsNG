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

        for p in range(0, eval(api_functions['diffuse_ramp_elements']).__len__()):
            ramps_prop_temp = copy(ramps_prop)
            ramp_properties_final[str(p)] = {}
            for k in ramps_keys:
                if p == 0:
                    print("P = 0")
                    val = ramps_prop_temp[k][0].replace("#1#", str(p))
                    if k.find("elements.color") > 0:
                        val = misc.RemoveRampsColor(val)
                    ramps_prop_temp[k] = tuple((val, ramps_prop_temp[k][1]))
                    ramp_properties[k] = str(eval(ramps_prop_temp[k][0]))
                else:
                    test = True
                    for e in keys.ExceptionsRampsKeys():
                        if k.find(e) == -1:
                            test = False

                    if test == False:
                        print(k)
                        val = ramps_prop_temp[k][0].replace("#1#", str(p))
                        if k.find("elements.color") > 0:
                            val = misc.RemoveRampsColor(val)
                        ramps_prop_temp[k] = tuple((val, ramps_prop_temp[k][1]))
                        ramp_properties[k] = str(eval(ramps_prop_temp[k][0]))


            print(ramp_properties_final)
            ramp_properties_final[str(p)] = ramp_properties
            
        return ramp_properties_final
