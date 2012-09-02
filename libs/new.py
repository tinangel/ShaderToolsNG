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
from shader_tools_ng.libs import keys

def NewActiveLayers(function_string, element_one, element_two,  activated):
    try: 
        if element_one and element_two: exec(function_string % (element_one, element_two,  activated))
        else: exec(function_string % (element_one,  activated))
    except:pass

def NewPreviewRenderTypeHandler(type, api_function, active_language):
    for v in range(0,  eval(api_function['scene_layers']).__len__()): 
        try:NewActiveLayers("%s[%s] = %s", api_function['scene_layers'], v,  'False')
        except:pass
        
    try: NewActiveLayers("%s[0] = %s", api_function['scene_layers'], False,  'True')
    except:pass

    if type == 'SPHERE':
        try: 
            for e in ('0',  '1') : 
                NewActiveLayers("%s[#1#] = %s".replace('#1#', e), api_function['scene_layers'], False,  'True')
        except:pass
    elif type == 'CUBE':
        try: 
            for e in ('0',  '2') : 
                NewActiveLayers("%s[#1#] = %s".replace('#1#', e), api_function['scene_layers'], False,  'True')
        except:pass
    elif type == 'MONKEY':
        try: 
            for e in ('0',  '3') : 
                NewActiveLayers("%s[#1#] = %s".replace('#1#', e), api_function['scene_layers'], False,  'True')
        except:pass
    elif type == 'FLAT':
        try: 
            for e in ('0',  '4') : 
                NewActiveLayers("%s[#1#] = %s".replace('#1#', e), api_function['scene_layers'], False,  'True')
        except:pass
    else:
        try: 
            for e in ('0',  '3') :
                NewActiveLayers("%s[#1#] = %s".replace('#1#', e), api_function['scene_layers'], False,  'True')
        except:pass
    
def CreateNew(app_path, active_configuration, api_function, active_language):
    #Imports & external libs:
    try:
        import bpy, os, platform
        from . import zip, misc
    except:
        print("#ShaderToolsNG : error import createnew")
    #end Imports & external libs:
    #Dezip file:
    wbfp = misc.ConvertMarkOut(active_configuration['workbase_file_path'], app_path)
    zf = misc.ConvertMarkOut(active_configuration['zip_folder'], app_path)
    zip_val = os.path.join(zf, wbfp.split(os.sep)[-1] + ".zip")
    tf = misc.ConvertMarkOut(active_configuration['temp_folder'], app_path)
    temp_val = os.path.join(tf, wbfp.split(os.sep)[-1] + ".blend")
    path_files = [zip_val, temp_val]

    for v in path_files:
        misc.Clear(v, 'files', 'one', active_language)
    zip.DeZip(app_path, active_configuration, wbfp, '', active_language)        
    #end Dezip file: 
    #Open workbase blend file:
    try:
        bin_path = eval(api_function['app_binary_path'])
        if platform.system() == 'Windows':
            workbase = os.popen('"%s"' % path_files[1])

        if platform.system() == 'Darwin':
            workbase = os.popen("open -n -a '%s' '%s'" % (bin_path.rstrip("/Contents/MacOS/blender"), path_files[1]))

        if platform.system() == 'Linux':
            workbase = os.popen("'%s' '%s'" % (bin_path,  path_files[1]))

        print(active_language['menu_error_error025'])
        misc.LogError(active_language['menu_error_error025'], False)
    except:
        print(active_language['menu_error_error026'])
        misc.LogError(active_language['menu_error_error026'], False)
    #end Open workbase zip file:
