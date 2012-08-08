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

import bpy, shutil,  os, binascii, threading
from . import misc, keys, request
from copy import copy

def CurrentHistory(default_paths,  active_configuration, api_functions, active_languages):
    history_list = request.DatabaseSelect(default_paths['database'], keys.HistoryKeys(), "HISTORY", "", 'one')
    history_tuple =[]
    c = 1
    if history_list:
        for v in history_list: 
            history_tuple.append(tuple((str(c),  v,  "")))
            c = c+1
    else:
        for v in range(1,  21): 
            history_tuple.append(tuple((str(c),  "No history %s" % str(v),  "")))
            c = c+1
    return history_tuple

def UpdateHistory(default_paths,  active_configuration, api_functions, active_languages,  material_name,  active_history):
    history_list_new =[]
    condition = []
    condition_final = "set "
    history_list_new.append(material_name)
    if active_history:
        for v in range(0, 20): history_list_new.append(active_history[v][1])
    
    c = 0
    for e in keys.HistoryKeys():
        condition.append("%s = '%s'," % (e, history_list_new[c]))
        c = c+1
    
    for v in condition: condition_final = condition_final + v
    condition_final = condition_final.rstrip(",")
    condition_final = condition_final + " where num_history = '1'"
    return request.DatabaseUpdate(default_paths['database'], "HISTORY", condition_final)
    
