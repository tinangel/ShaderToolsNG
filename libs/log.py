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

def OpenLog(app_path, active_configuration, api_function):
    #Imports & external libs:
    try:
        import bpy, os, platform
        from . import misc
    except:
        print("#ShaderToolsNG : error import logs")
    #end Imports & external libs:
    path_files = os.path.join(misc.ConvertMarkOut(active_configuration['error_folder'], app_path), "log.txt")
    #Open log file:
    if platform.system() == 'Windows':
        logs = os.popen('"%s"' % path_files)

    if platform.system() == 'Darwin':
        logs = os.popen("open '%s' " % path_files)

    if platform.system() == 'Linux':
        logs = os.popen("gedit '%s'" % path_files)    
    #end Open log file: