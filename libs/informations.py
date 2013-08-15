# ##### BEGIN CC LICENSE BLOCK #####
#
# This work is licensed under a 
# Creative Commons Attribution 3.0 
# Unported (CC BY 3.0) License : 
#
# More details here : http://creativecommons.org/licenses/by/3.0/deed.en
#
# ##### END CC LICENSE BLOCK #####

# <pep8-80 compliant>
#-*- coding: utf-8 -*-

import bpy, os
from . import environment, keys,  request

#Informations enumerator tuple
def InformationsEnumItems(database_path):
    list = ('num_materials',  'name')
    search_request = request.DatabaseSelect(database_path, list, 'MATERIALS', '', 'all')
    search_tuple = []
    for e in search_request:
        if  e[1] != '':
            name = "%s_(%s)" % (e[1].replace("$T_",  ""),  e[0])
            search_tuple.append(tuple((str(e[0]), name, "")))
    return search_tuple

#Informations for the selected element
def InformationsSelectedItem(database_path,  idx_material):
    list = ('num_materials',  'name',  'description',  'creator',  'category',  'weblink',  'email')
    advanced_request =  'where materials.num_materials=informations.idx_materials and materials.num_materials= %s' % str(idx_material)
    select_request = request.DatabaseSelect(database_path, list,  "'MATERIALS','INFORMATIONS'",  advanced_request, 'one')
    return select_request 
