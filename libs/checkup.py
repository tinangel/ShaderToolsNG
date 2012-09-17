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

def MakeCheckup(database_path, configs_database_path,bookmark_path, bookmark_folder_path, bookmark_folder_name, active_configuration, app_path, languages_config, default_paths):
    #Imports & external libs:
    print("Checkup : ")
    try:
        import bpy, sqlite3, os, zipfile
        from . import bookmark, environment, request, misc, keys, configuration
        print(misc.ConsoleError("import ", 1, True))
    except:
        print(misc.ConsoleError("import ", 1, False))
    #end Imports & external libs:
    #Test : verify if database path exists:
    try:
        if os.path.exists(database_path):
            print(misc.ConsoleError("database exists ", 1, True))       
        else:
            print(misc.ConsoleError("database exists ", 1, False))
            
            print(misc.ConsoleError("path : %s" % database_path, 2, False))
    
    except:
        print(misc.ConsoleError("database exists ", 1, False))
        print(misc.ConsoleError("path : %s" % database_path, 2, False))
    #end Test : verify if database path exists
    #Test : insert in database:
    elements_val = \
        (
         "0", "hello", "10.9999", "1", "3F33∏3Ò4", "01/01/1970", "00:01:54", 
        )
    
    try:
        result = request.DatabaseInsert(database_path, keys.TestKeys(), elements_val, 'TEST',  False)
        if result:
            print(misc.ConsoleError("insert into database ", 1, True))
        else:
            print(misc.ConsoleError("insert into database ", 1, False))

    except:
        print(misc.ConsoleError("insert into database ", 1, False))
    #end Test : insert in database:
    #Test : select in database:
    try:
        result = request.DatabaseSelect(database_path, keys.TestKeys(), 'TEST', "", "one")
        if result == False:
            print(misc.ConsoleError("select in database ", 1, False))
        else:
            print(misc.ConsoleError("select in database ", 1, True))

    except:
        print(misc.ConsoleError("select in database ", 1, False))
    #end Test : select in database:
    #Test : update in database:
    condition_update = "set text='Hello world', float='1234.56789', bool='0', blob='ffd8ffe000104a46', date='22/12/2012', time='00:30:58' where num_test='0'"
    try:
        result = request.DatabaseUpdate(database_path, 'TEST', condition_update)
        if result:
            print(misc.ConsoleError("update into database ", 1, True))
        else:
            print(misc.ConsoleError("update into database ", 1, False))
    except:
        print(misc.ConsoleError("update into database ", 1, False))
    #end Test : update into database:
    #Test : delete in database:
    condition_delete = "where num_test='0'"
    try:
        result = request.DatabaseDelete(database_path, 'TEST', condition_delete)
        if result:
            print(misc.ConsoleError("delete in database ", 1, True))
        else:
            print(misc.ConsoleError("delete in database ", 1, False))
    except:
        print(misc.ConsoleError("delete in database ", 1, False))
    #end Test : delete in database:
    #Verify : default configuration:
    try:
        result = request.DatabaseCount(configs_database_path, 'default_config', "CONFIGURATION", "where default_config=1", 'all')
        if result[0][0] > 1:
            request.DatabaseUpdate(database_path, "CONFIGURATION", "set default_config=0 where default_config=1")
            request.DatabaseUpdate(database_path, "CONFIGURATION", "set default_config=1 where name='Default'")
        print(misc.ConsoleError("default configuration verification ", 1, True))
    except:
        print(misc.ConsoleError("default configuration verification ", 1, False))
    #end Verify : default configuration
    #Test : folders verification:
    try:
        folder_list = \
            (
             active_configuration['zip_folder'],active_configuration['temp_folder'],
             active_configuration['save_folder'], active_configuration['html_folder'],
             active_configuration['error_folder'], active_configuration['bin_folder'],
            )

        for v in folder_list:
            v = misc.ConvertMarkOut(v, app_path)
            
            if not os.path.exists(v):
                os.makedirs(v)
        print(misc.ConsoleError("check folders ", 1, True))        
    except:
        print(misc.ConsoleError("check folders ", 1, False))
    #end Test : folders verification:
    #Test : html sub folder verification:
    print(" "*11 + "check help subfolder : ")        
    for h in languages_config:
        help_file = os.path.join(app_path, "html", h)
        if os.path.exists(help_file):
            print(misc.ConsoleError(str(h), 3, True))
        else:
            print(misc.ConsoleError(str(h), 3, False))
    #end Test : html sub folder verification:
    #Test : zip files verification:
    zip_file_list = \
        (
         misc.ConvertMarkOut(active_configuration['workbase_file_path'], app_path),
         misc.ConvertMarkOut(active_configuration['help_file_path'], app_path),         
         misc.ConvertMarkOut(active_configuration['img_file_path'], app_path),
        )

    print(" "*11 + "compress file : ")        
    for v in zip_file_list:
        name_file = str(v.split(os.path.sep)[-1])
        if os.path.exists(v):
            print(misc.ConsoleError(name_file, 2, True))
        else:
            print(misc.ConsoleError(name_file, 2, False))
    #end Test : zip files verification:
    #Auto save verification:
    req = request.DatabaseSelect(default_paths['configs_database'], keys.AutoSaveKeys(), "CONFIGURATION", "where default_config=1", 'one')
    if not req == None:
        if req[1] >= req[0]:
            auto_save_list = \
            (
            default_paths['database'],  default_paths['configs_database'],  
            default_paths['languages_database'],  default_paths['apis_database'], 
            )
            for s in auto_save_list: misc.AutoSaveDatabase(s,  default_paths['save'])
            auto_save_update = "set %s = '%s' where default_config=1" % (keys.AutoSaveKeys()[1] ,  "0")
            result = request.DatabaseUpdate(default_paths['configs_database'], 'CONFIGURATION', auto_save_update)  
        else:
            auto_save_update = "set %s = '%s' where default_config=1" % (keys.AutoSaveKeys()[1] ,  str(req[1] + 1))
            result = request.DatabaseUpdate(default_paths['configs_database'], 'CONFIGURATION', auto_save_update)  
    #end Auto save verification
    #Test : bookmark verification:
    return(bookmark.VerifyBookmark(bookmark_path, bookmark_folder_path, bookmark_folder_name))
    #end Test : bookmark verification:















