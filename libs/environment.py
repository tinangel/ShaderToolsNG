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

import bpy, os, sqlite3, sys, platform, copy
from shader_tools_ng.libs import keys, request, misc, configuration, zip

#Convert active configuration to default path 
def ConvertDefaultPaths(default_paths,  active_configuration):
    temp = active_configuration['database_path'].replace('#addon#', default_paths['app'])
    temp = temp.replace('#slash#', os.sep)
    default_paths['database'] = temp
    return default_paths
#end Convert active configuration to default path 
#Materials category dictionnary
def MaterialsCatergories(langage):
    temp =keys.MaterialsKeys()    
    temp_tuple = tuple((v, langage[v], "") for v in temp) 
    return temp_tuple
#end Materials category dictionnary
#Configurations names dictionnary
def ConfigurationsNames(configurations):
    temp_tuple = []
    for v in configurations:
        if configurations[v]['name'] != "":
            temp_tuple.append((str(configurations[v]['num_configuration']), v, ""))
    return temp_tuple
#end Configurations names dictionnary
#Languages names dictionnary
def LanguagesNames(langages):
    temp_tuple = tuple((langages[l]['name_language'], langages[l]['name_language'], "") for l in langages)
    return temp_tuple
#end Languages names dictionnary
#Configurations options dictionnary
def ConfigurationsOptions(langage):
    temp = keys.OptionsKeys()
    temp_tuple = tuple((v, langage[v], "") for v in temp) 
    return temp_tuple
#end Configurations options dictionnary
#Default paths dictionnary
def DefaultPaths():
    app_path = os.path.join(bpy.utils.script_paths()[0], "addons", "shader_tools_ng",  "__init__.py")
    if os.path.exists(app_path): app_path = os.path.join(bpy.utils.script_paths()[0], "addons", "shader_tools_ng")
    else: app_path = os.path.join(bpy.utils.script_paths()[1], "addons", "shader_tools_ng")
    bookmarks_path_user = os.path.join(bpy.utils.resource_path('USER', major=bpy.app.version[0], minor=bpy.app.version[1]), "config", "bookmarks.txt")
    configs_path = os.path.join(app_path, "ShaderToolsConfigs.sqlite")
    #Test : verify if configs database path exists:
    if os.path.exists(configs_path):
        print(misc.ConsoleError("Configs database exists ", 0, True))
        r = request.DatabaseSelect(configs_path, keys.ConfigurationsKeys(), "CONFIGURATION", "where default_config=1", 'one')
        if r:
            print(misc.ConsoleError("Test to open a configuration ", 0, True))
        else:
            os.remove(configs_path)
            configuration.RestoreConfigs(app_path)
            print(misc.ConsoleError("Restore configs database ", 0, True))
    else:
        print(misc.ConsoleError("Configs database exists ", 0, False))
        try:
            configuration.RestoreConfigs(app_path)
            print(misc.ConsoleError("Restore configs database ", 0, True))
        except:
            print(misc.ConsoleError("Restore configs database ", 0, False))
    #end Test : verify if configs database path exists
    req = request.DatabaseSelect(configs_path, keys.ConfigurationsKeys(), "CONFIGURATION", "where default_config=1", 'one')
    if req == None:
        configuration.DefaultConfiguration(configs_path, 'Default')
        req = request.DatabaseSelect(configs_path, keys.ConfigurationsKeys(), "CONFIGURATION", "where default_config=1", 'one')
    
    r = {}
    c = 0
    for k in keys.ConfigurationsKeys():
        r[k] = req[c]
        c = c + 1 
    
    #Test : verify if default database path exists:
    database_path = misc.ConvertMarkOut(r['database_path'], app_path)
    if os.path.exists(database_path):
        print(misc.ConsoleError("Materials database exists ", 0, True))       
    else:
        print(misc.ConsoleError("Materials database exists ", 0, False))
        try:
            configuration.DefaultConfiguration(configs_path, 'Default')
            print(misc.ConsoleError("Restore default configuration ", 1, True))       
        except:
            print(misc.ConsoleError("Restore default configuration ", 1, False))       
    #end Test : verify if default database path exists
    for v in keys.ConfigurationsKeys_2():
        r[v] = misc.ConvertMarkOut(r[v], app_path)
        
    temp = \
        {
            "blend":os.path.dirname(bpy.data.filepath),
            "blend_path":bpy.data.filepath,
            "app":app_path,
            "zip":r['zip_folder'],
            "error":r['error_folder'],
            "configs_database":os.path.join(app_path, "ShaderToolsConfigs.sqlite"),
            "languages_database":os.path.join(app_path, "ShaderToolsLanguages.sqlite"),
            "apis_database":os.path.join(app_path, "ShaderToolsApis.sqlite"),
            "database":r['database_path'],
            "save":r['save_folder'],
            "temp":r['temp_folder'],
            "bin":r['bin_folder'],
            "bookmarks":bookmarks_path_user,
    }
    return temp
#end Default paths dictionnary
#Active configuration dictionnary
def ActiveConfigurations(dict_config):
    for k in dict_config:
        if dict_config[k]['default_config']:
            return dict_config[k] 
#end Active configuration dictionnary
#Active language dictionnary
def ActiveLanguage(dict_language, active_config_lang):
    for k in dict_language:
        if active_config_lang in k:
            return dict_language[k] 
#end language configuration dictionnary
#ApiDatas dictionnary
def ApiDatas(database_path, version):
    ApiFunctions = {}
    temp_datas = keys.ApiKeys()
    
    def DatabaseRequest(database_path, request, list):
        ShaderToolsDatabase = sqlite3.connect(database_path) #open database
        DatabaseCursor = ShaderToolsDatabase.cursor() #create cursor        
        #here my request :
        try:
            DatabaseCursor.execute(request)
            result = DatabaseCursor.fetchone()
            DatabaseCursor.close() #close cursor
            ShaderToolsDatabase.close() #close database        
            
            #now the dictionnary :
            count = 0
            for k in list:
                ApiFunctions[k] = result[count]
                count = count + 1     
            
            return ApiFunctions   
        
        except:
            DatabaseCursor.close() #close cursor
            ShaderToolsDatabase.close() #close database        
            print('Api Functions : error database access')                  
    #end DatabaseRequest
    #Api functions dictionnary :
    api_functions_request = "select "
    
    for v in temp_datas :
        api_functions_request  = api_functions_request + v + ","     
    
    api_functions_request = api_functions_request.rstrip(",") + " from 'API_FUNCTIONS' where " + version  + " between 'API_FUNCTIONS'.'blender_version_min' and 'API_FUNCTIONS'.'blender_version_max'"
    return DatabaseRequest(database_path, api_functions_request, temp_datas)    
#end Api functions dictionnary
#Languages datas dictionnary
def LanguagesDatas(database_path):
    temp_lang_datas = {}
    temp_lang_datas_new_keys = {}
    temp_datas = keys.LangagesKeys()
    
    def DatabaseRequest(database_path, request, list):
        ShaderToolsDatabase = sqlite3.connect(database_path) #open database
        DatabaseCursor = ShaderToolsDatabase.cursor() #create cursor
        
        try:
            #here my request :
            DatabaseCursor.execute(request)
            result = DatabaseCursor.fetchall()
            
            #i create temp_datas_lang keys dictionnary:
            for v in result:
                count = 0
                temp_lang_datas = {}
                for w in v:
                    temp_lang_datas[temp_datas[count]] = w
                    count = count+1
                #end for
                temp_lang_datas_new_keys[v[2]] = temp_lang_datas
            #end for
            DatabaseCursor.close() #close cursor
            ShaderToolsDatabase.close() #close database        
            return temp_lang_datas_new_keys
        
        except:
            DatabaseCursor.close() #close cursor
            ShaderToolsDatabase.close() #close database        
            print('Lang Datas : error database access')
    #end DatabaseRequest
    #Languages datas dictionnary :
    languages_datas_request = "select "
    
    for v in temp_datas :
        languages_datas_request = languages_datas_request + v + ","     
    
    languages_datas_request = languages_datas_request.rstrip(",") + " from 'LANGUAGES'"
    return DatabaseRequest(database_path, languages_datas_request, temp_datas)    
#end Languages Datas dictionnary
#Configuration datas dictionnary
def VerifyDefaultConfiguration(database_path, option):
    #Verify : default configuration:
    try:
        result = request.DatabaseCount(database_path, 'default_config', "CONFIGURATION", "where default_config=1", 'all')
        if result[0][0] == 0:
            elements_val = \
                (
                 "1", "1", "Default_(1)", "#addon##slash#ShaderToolsDatabaseNG.sqlite", "You", "My material description",
                 "http://", "MyMaterial", "menu_category_personal", "my_email@company.com",
                 "256", "768", "Francais", "#addon##slash#error", "#addon##slash#html", "#addon##slash#save", "#addon##slash#temp",
                 "#addon##slash#zip", "#addon##slash#bin#slash#workbase", "#addon##slash#bin#slash#help","#addon##slash#bin#slash#img", "#addon##slash#bin", 
                 "green, mat, red lines ...", "menu_configuration_option_save", "256", "256",
                 )
            request.DatabaseInsert(database_path, keys.ConfigurationsKeys(), elements_val, "CONFIGURATION",  False,  '')
        if option:
            print(misc.ConsoleError("default configuration verification ", 1, True))
    except:
        if option:
            print(misc.ConsoleError("default configuration verification ", 1, False))
#end Verify : default configuration

def ConfigurationsDatas(database_path, option):
    VerifyDefaultConfiguration(database_path, option)
    temp_config_datas = {}
    temp_config_datas_new_keys = {}
    temp_datas = keys.ConfigurationsKeys()    
    def DatabaseRequest(database_path, request, list):
        ShaderToolsDatabase = sqlite3.connect(database_path) #open database
        DatabaseCursor = ShaderToolsDatabase.cursor() #create cursor
        
        try:
            #here my request :
            DatabaseCursor.execute(request)
            result = DatabaseCursor.fetchall()
            
            #i create temp_datas_lang keys dictionnary:
            for v in result:
                count = 0
                temp_config_datas = {}
                for w in v:
                    temp_config_datas[temp_datas[count]] = w
                    count = count+1
                #end for
                temp_config_datas_new_keys[v[2]] = temp_config_datas
            #end for
            DatabaseCursor.close() #close cursor
            ShaderToolsDatabase.close() #close database        
            return temp_config_datas_new_keys
        
        except:
            DatabaseCursor.close() #close cursor
            ShaderToolsDatabase.close() #close database        
            print('Configurations Datas : error database access')
    #end DatabaseRequest
    #Configurations datas dictionnary :
    configurations_datas_request = "select "
    
    for v in temp_datas :
        configurations_datas_request = configurations_datas_request + v + ","     
    
    configurations_datas_request = configurations_datas_request.rstrip(",") + " from 'CONFIGURATION'"
    return DatabaseRequest(database_path, configurations_datas_request, temp_datas)    
#end Configuration Datas dictionnary
#About datas dictionnary
def AboutDatas(database_path):
    temp_about_datas = {}
    temp_about_datas_new_keys = {}
    temp_datas = keys.AboutKeys()    
    def DatabaseRequest(database_path, request, list):
        ShaderToolsDatabase = sqlite3.connect(database_path) #open database
        DatabaseCursor = ShaderToolsDatabase.cursor() #create cursor
        
        try:
            #here my request :
            DatabaseCursor.execute(request)
            result = DatabaseCursor.fetchall()
            
            #i create temp_datas_lang keys dictionnary:
            for v in result:
                count = 0
                temp_about_datas = {}
                for w in v:
                    temp_about_datas[temp_datas[count]] = w
                    count = count+1
                #end for
                temp_about_datas_new_keys[v[2]] = temp_about_datas
            #end for
            DatabaseCursor.close() #close cursor
            ShaderToolsDatabase.close() #close database        
            return temp_about_datas_new_keys
        
        except:
            DatabaseCursor.close() #close cursor
            ShaderToolsDatabase.close() #close database        
            print('About Datas : error database access')
    #end DatabaseRequest
    #About datas dictionnary :
    about_datas_request = "select "
    
    for v in temp_datas :
        about_datas_request = about_datas_request + v + ","     
    
    about_datas_request = about_datas_request.rstrip(",") + " from 'ABOUT'"
    return DatabaseRequest(database_path, about_datas_request, temp_datas)    
#end About Datas dictionnary







