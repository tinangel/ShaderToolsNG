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

def Clear(path, type, option):
    #Imports & external libs:
    try:
        import bpy, os
    except:
        print("#ShaderToolsNG : error import misc")
    #end Imports & external libs:
    #Clear files & folder:
    if type == 'files' and option == 'one':
        if os.path.exists(path) :
            return os.remove(path)
    
    if type == 'files' and option == 'all':
        if os.path.exists(path) :
            files = os.listdir(path)
            for f in files:           
                if not os.path.isdir(f):
                    return os.remove(os.path.join(path, f))
    #end Clear files & folder:

def ConsoleError(msg, sub_error, type):
    e = ""
    if sub_error:
        msg = " "*10*sub_error + " %s" % msg

    if type:
        e = "%s" % msg + "."*(76-len(msg)) + "ok"
    else:
        e = "%s" % msg + "."*(73-len(msg)) + "error"

    return e

def EnumPropertyItemsIdx(string_enum):
    idx = string_enum.split("_")[-1]
    idx = idx.replace("(", "")
    idx = idx.replace(")", "")
    return idx

def EnumPropertyItemsInverseIdx(string_enum, configurations_config):
    config_val = "_(%s)" % string_enum
    for c in configurations_config:
        if config_val in c:
            config_val = c
            break
    return config_val

def ConvertBoolStringToNumber(val):
    if val == True or val == 'True': val = 1
    if val == False or val == 'False': val = 0
    return val

def ConvertBoolNumberToString(val):
    if val == 1 or val == '1': val = True
    if val == 0 or val == '0': val = False
    return val

def RemoveInvalidValues(val):
    InvalidValues = \
        (
         '<bpy',
        )
    for v in InvalidValues:
        if v == val or v in str(val): val = 0
    if val == '': val = "''"
    return val

def ConvertStringProperties(prop, keys_list):
    val = False
    for p in keys_list:
        if p == prop:
            val = True
            break
    return val

def RemoveExceptions(prop, val):
    if prop == "use_light_group_exclusive":
        if val == None or val == 'None':
            val = 0
    return val

def RemoveColor(value):
    if "Color(" in value:
        value = value.replace("))", ")")
        value = value.replace("Color(", "")
    return value

def RemoveVector(value):
    if "Vector(" in value:
        value = value.replace("))", ")")
        value = value.replace("Vector(", "")
    return value


def RemoveRadius(value):
    one = str(eval(value)[0])
    two = str(eval(value)[1])
    three = str(eval(value)[2])
    value = "(%s, %s, %s)" % (one, two, three)
    return value

def RemoveRampsColor(value):
    red = str(eval(value)[0])
    green = str(eval(value)[1])
    blue = str(eval(value)[2])
    alpha = str(eval(value)[3])
    value = "(%s, %s, %s, %s)" % (red, green, blue, alpha)
    return value
