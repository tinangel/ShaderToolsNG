# ##### BEGIN GPL LICENSE BLOCK #####
#
# This work is licensed under a Creative 
# Commons Attribution-NonCommercial-ShareAlike 
# 3.0 Unported License : 
#
# More details here : http://creativecommons.org/licenses/by-nc-sa/3.0/deed.fr
#
# ##### END GPL LICENSE BLOCK #####


# <pep8-80 compliant>
import bpy, sqlite3, shutil, os
from shader_tools_ng.libs import request, keys, misc, zip

def RestoreConfigs(app_path):
    config_save_path = os.path.join(app_path, "bin", "configs")
    config_restore_path = os.path.join(app_path, "ShaderToolsConfigs.sqlite")
    shutil.copy2(config_save_path, config_restore_path)

def DefaultConfiguration(database_path, name):
    update_configuration = request.DatabaseUpdate(database_path, "CONFIGURATION", "set default_config=0 where default_config=1")
    update_configuration = request.DatabaseUpdate(database_path, "CONFIGURATION", "set default_config=1 where name='%s'" % name)

def DeleteConfiguration(database_path, new_config, names_config, active_language):
    condition = "set "
    for v in new_config:
        condition = condition + "%s='%s',"%(v, new_config[v])
    condition = condition.rstrip(",") + " where num_configuration=%s"%new_config['num_configuration']
    try:
        if len(names_config) > 1:
            r = request.DatabaseUpdate(database_path, "CONFIGURATION", condition)
            if new_config['default_config']:
                for v in names_config:
                    if v[0] != new_config['num_configuration']:
                        DefaultConfiguration(database_path, v[1])
                        break
            print(active_language['menu_error_error003'])
            misc.LogError(active_language['menu_error_error003'], False)
        else:
            print(active_language['menu_error_error004'])
            print(eval(active_language['menu_error_error005']))
            misc.LogError(active_language['menu_error_error004'], False)
            misc.LogError(eval(active_language['menu_error_error005']), False)
    except:
        print(active_language['menu_error_error006'])
        misc.LogError(active_language['menu_error_error006'], False)

def SaveConfiguration(database_path, new_config, active_language):
    idx = new_config['name2'].split("_")[-1]
    new_config['name2'] = new_config['name2'].replace("_%s" % idx, "")
    r = request.DatabaseCount(database_path, 'name', "CONFIGURATION", "", 'all')
    
    if r:
        elements = keys.ConfigurationsKeys()
        elements_val = []
        new_config['num_configuration'] = r[0][0] + 1
        new_config['name'] = new_config['name2'] + "_(%s)" % (r[0][0] + 1)
        for v in elements:
            if new_config[v] == True: new_config[v] = 1
            if new_config[v] == False: new_config[v] = 0
            elements_val.append(new_config[v]) 
        
        try:
            request.DatabaseInsert(database_path, elements, elements_val, "CONFIGURATION")
            if new_config['default_config']:
                DefaultConfiguration(database_path, new_config['name'])
            print(active_language['menu_error_error007'])
            misc.LogError(active_language['menu_error_error007'], False)
        except:
            print(active_language['menu_error_error008'])
            misc.LogError(active_language['menu_error_error008'], False)

    return new_config['name']

