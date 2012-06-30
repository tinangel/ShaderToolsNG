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

def CreateNew(app_path, active_configuration, api_function, active_language):
    #Imports & external libs:
    try:
        import bpy, os, platform
        from . import zip, misc
    except:
        print("#ShaderToolsNG : error import createnew")
    #end Imports & external libs:
    #Dezip file:
    path_files = \
        (
         os.path.join(active_configuration['zip_folder'].replace("#addon#", app_path), active_configuration['workbase_file_path'].split(os.sep)[-1] + ".zip"),
         os.path.join(active_configuration['temp_folder'].replace("#addon#", app_path), active_configuration['workbase_file_path'].split(os.sep)[-1] + ".blend"),
        )
    for v in path_files:
        misc.Clear(v, 'files', 'one', active_language)
    zip.DeZip(app_path, active_configuration, active_configuration['workbase_file_path'])        
    #end Dezip file: 
    #Open workbase blend file:
    bin_path = eval(api_function['app_binary_path'])
    if platform.system() == 'Windows':
        workbase = os.popen('"%s"' % path_files[1])

    if platform.system() == 'Darwin':
        workbase = os.popen("open -n -a '%s' '%s'" % (bin_path.rstrip("/Contents/MacOS/blender"), path_files[1]))

    if platform.system() == 'Linux':
        workbase = os.popen(bin_path + " '%s'" % path_files[1])
    
    print("$hader Tools : create a new material.")
    #end Open workbase zip file: