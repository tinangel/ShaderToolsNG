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

import bpy, shutil,  os
from . import misc, keys, request, misc
from copy import copy

def MoveAllInsideFolder(active_configuration, api_functions, active_languages,  database_folder,  tempory_folder):
    files = os.listdir(database_folder)
    for f in files:
        if not os.path.isdir(f) and f.endswith(".jpg"):
            shutil.copy2(os.path.join(database_folder, f), os.path.join(tempory_folder, f))
    misc.Clear(database_folder, 'files', 'all', active_languages)
    return True

def FilterHistory(default_paths,  active_configuration, api_functions, active_languages,  material_name):
    database_folder = os.path.join(default_paths['app'],  active_languages['menu_bookmarks_name'])
    tempory_folder = os.path.join(database_folder,  ".tempory")
    if MoveAllInsideFolder(active_configuration, api_functions, active_languages, database_folder,  tempory_folder):
        shutil.copy2(os.path.join(tempory_folder, material_name),  os.path.join(database_folder, material_name))
    exec(api_functions['ops_file_refresh'])
    return True

def FilterSearch(default_paths,  active_configuration, api_functions, active_languages,  advanced_search_properties):
    keywords = advanced_search_properties['keywords']
    database_folder = os.path.join(default_paths['app'],  active_languages['menu_bookmarks_name'])
    tempory_folder = os.path.join(database_folder,  ".tempory")
    materials_listing = []
    for e in ( "," ,  " ", "-",  "_",  ";",  ":"):keywords = keywords.replace(e,  "$")
    keywords = keywords.split("$")
    for v in range(0,  keywords.__len__()):
        try:keywords.remove('')
        except: pass 
    
    if MoveAllInsideFolder(active_configuration, api_functions, active_languages, database_folder,  tempory_folder):
        result_search_final = []
        #Here just the default search :
        keys_list = ['num_materials', 'name']
        search_list = ['name','description', 'creator', 'category',  'weblink',  'email']
        for k in keywords:
            final_keyword = "%" + k + "%"
            advanced_request =  "where "
            c = 0
            for e in search_list : 
                if c == 0:
                    if advanced_search_properties[e]: 
                        advanced_request = advanced_request + "%s LIKE '%s' "%(e, final_keyword)
                        c = 1
                else: 
                    if advanced_search_properties[e]: advanced_request = advanced_request + "or %s LIKE '%s' "%(e, final_keyword)
            advanced_request = advanced_request + " and materials.num_materials=informations.idx_materials group by num_materials"
            result_search = request.DatabaseSelect(default_paths['database'], keys_list, "'MATERIALS', 'INFORMATIONS'", advanced_request, "all")
            for v in result_search: result_search_final.append("%s_(%s).jpg" % (v[1].replace("$T_",  ""),  str(v[0])))
        for i in result_search_final:shutil.copy2(os.path.join(tempory_folder, i),  os.path.join(database_folder, i))
    exec(api_functions['ops_file_refresh'])
    return True
