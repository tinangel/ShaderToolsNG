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

def MappingInfluenceColorsExport(api_functions, texture_structure, texture_keys, idx):
    for k in texture_keys:
        slot = "%s[%s].%s" % (api_functions['texture_slots'], idx, k)
        val = ""
        try: val = copy(eval(slot))
        except: val = None
        if val != None and val != '':
            if type(val).__name__ == 'str': texture_structure.append("slot.%s = '%s'\n" % (k,val))
            elif type(val).__name__ == 'Color':
                val = misc.RemoveColor(str(val))
                texture_structure.append("slot.%s = %s\n" % (k,val))
            elif type(val).__name__ == 'Vector':
                val = misc.RemoveVector(str(val))
                texture_structure.append("slot.%s = %s\n" % (k,val))
            else: texture_structure.append("slot.%s = %s\n" % (k,val))
    return texture_structure
