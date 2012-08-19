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
import bpy, os
from . import environment, keys,  request

#Informations enumerator tuple
def InformationsEnumItems(database_path):
    list = ('num_materials',  'name')
    search_request = request.DatabaseSelect(database_path, list, 'MATERIALS', '', 'all')
    search_tuple = []
    for e in search_request: 
        name = "%s_(%s)" % (e[1].replace("$T_",  ""),  e[0])
        search_tuple.append(tuple((str(e[0]), name, "")))
    return search_tuple

#Informations for the selected element
def InformationsSelectedItem(database_path,  idx_material):
    list = ('num_materials',  'name',  'description',  'creator',  'category',  'weblink',  'email')
    advanced_request =  'where materials.num_materials=informations.idx_materials and materials.num_materials= %s' % str(idx_material)
    select_request = request.DatabaseSelect(database_path, list,  "'MATERIALS','INFORMATIONS'",  advanced_request, 'one')
    return select_request 
