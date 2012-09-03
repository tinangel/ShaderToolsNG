# ##### BEGIN CC LICENSE BLOCK #####
#
# This work is licensed under a Creative 
# Commons Attribution-NonCommercial-ShareAlike 
# 3.0 Unported License : 
#
# More details here : http://creativecommons.org/licenses/by-nc-sa/3.0/deed.fr
#
# ##### BEGIN CC LICENSE BLOCK #####

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
