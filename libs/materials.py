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

def RemoveColor(value):
    if "Color(" in value:
        value = value.replace("))", ")")
        value = value.replace("Color(", "")
    return value

def RemoveRadius(value):
    one = str(eval(value)[0])
    two = str(eval(value)[1])
    three = str(eval(value)[2])
    value = "(%s, %s, %s)" % (one, two, three)
    return value

def SurfaceWireVolumeHalo(api_functions, mat_properties_keys, surface_wire_keys):
    mat_properties = []
    for k in surface_wire_keys:
        if k == "subsurface_scattering.radius": #radius subsurface is an exception
            prop = RemoveRadius(mat_properties_keys[k][0])

        if k != "subsurface_scattering.radius": #radius subsurface is an exception
            prop = RemoveColor(str(eval(mat_properties_keys[k][0])))
        
        prop = misc.RemoveInvalidValues(prop) #remove invalid values
        prop = misc.ConvertBoolStringToNumber(prop) #convert True/False to 0/1
        prop = misc.RemoveExceptions(k, prop)
        c  = misc.ConvertStringProperties(k, keys.StringPropertiesKeys())
        mat_properties.append((k,prop, c))
    return mat_properties
 