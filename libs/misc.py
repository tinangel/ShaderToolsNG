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
import bpy, os, time, shutil, platform,  threading

def AutoSaveDatabase(path,  destination):
    auto_save_folder =  os.path.join(destination , time.strftime('AutoSave %d-%m-%y %H:%M:%S',time.localtime()))
    if not os.path.exists(auto_save_folder): os.makedirs(auto_save_folder)
    destination_path = os.path.join(destination , auto_save_folder,  path.split(os.sep)[-1])
    try: os.remove(destination_path)
    except:pass
    shutil.copy2(path, destination_path)

def SaveDatabase(path,  destination,  bin_folder):
    destination_path = os.path.join(destination ,   time.strftime('Migration %d-%m-%y %H:%M:%S',time.localtime()) + path.split(os.sep)[-1])
    try: os.remove(destination_path)
    except:pass
    shutil.copy2(path, destination_path)
    os.rename(path,  path+"_old")
    shutil.copy2(os.path.join(bin_folder,  "database"), path)
    os.remove(path+"_old")

def Clear(path, type, option, active_language):
    #Imports & external libs:
    try:
        import bpy, os
    except:
        print("$haderTools : error import misc")
    #end Imports & external libs:
    #Clear files & folder:
    exception = os.path.join(path,  '.tempory')
    if type == 'files' and option == 'one':
        if os.path.exists(path) :
            return os.remove(path)
    
    if type == 'files' and option == 'all':
        if os.path.exists(path) :
            files = os.listdir(path)
            for f in files:           
                if not os.path.isdir(f):
                    try: os.remove(os.path.join(path, f))
                    except: 
                        if not os.path.exists(exception): print(active_language['menu_error_error021'] % f)
                            
    if type == 'all':
        try:
            shutil.rmtree(path)
            os.makedirs(path)
        except:
            if not os.path.exists(exception): print(active_language['menu_error_error021'] % path)
    #end Clear files & folder:

def LogAndPrintError(list_error):
    print(list_error[0])
    LogError(list_error[1], 0)

def LogTimeError():
    return time.strftime('[%H:%M:%S]',time.localtime())

def LogError(msg, clear):
    app_path = os.path.join(bpy.utils.script_paths()[0], "addons", "shader_tools_ng")
    error_folder = os.path.join(app_path, "error") 
    path = os.path.join(app_path, "error" ,"log.txt")

    #Verify error folder:
    try:os.makedirs(error_folder)
    except:pass
    if clear:
        if os.path.exists(path) :
            os.remove(path)
    #Test log file exists:
    try:
        # create log file:
        log_file = open(path, 'a',  encoding = "utf-8")
        log_file.write("%s -> %s\n" % (LogTimeError(), msg))
        log_file.close()
    except:
        print(active_language['menu_error_error020']) 

def ConsoleError(msg, sub_error, type):
    e = ""
    if sub_error:
        msg = " "*10*sub_error + " %s" % msg

    if type:
        e = "%s" % msg + "."*(76-len(msg)) + "ok"
    else:
        e = "%s" % msg + "."*(73-len(msg)) + "error"
    
    LogError(e, False)
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

def ImageAbsolutePath(path):
    idx = 0
    for p in bpy.utils.blend_paths(absolute=False):
        if p.find(eval(path)) >= 0: break
        else: idx = idx + 1
    return bpy.utils.blend_paths(absolute=True)[idx]

def ConvertMarkOut(path, app_path):
    temp = path.replace("#addon#", app_path)
    temp = temp.replace("#slash#", os.sep)
    return temp

def DoubleSlash(path):
    if platform.system() == 'Windows': return path.replace(os.sep, "%s%s" % (os.sep, os.sep))
    else: return path

def CrossProduct(current_value, max_value):
    total = (current_value*100)/max_value
    return int(total)

def CurrentThreads():
    while threading.active_count() > 1:return None
        
