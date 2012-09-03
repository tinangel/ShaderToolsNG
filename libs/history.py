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

import bpy, shutil,  os, binascii, threading
from . import misc, keys, request
from copy import copy

def CurrentHistory(default_paths,  active_configuration, api_functions, active_languages):
    history_list = request.DatabaseSelect(default_paths['database'], keys.HistoryKeys(), "HISTORY", "", 'one')
    history_tuple =[]
    if history_list:
        for v in history_list:  history_tuple.append(tuple((v,  v,  "")))
    else:
        for v in range(1,  21): 
            history_tuple.append(tuple((v,  "No history %s" % str(v),  "")))
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
