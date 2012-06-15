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

def MakeCheckup(database_path, configs_database_path,bookmark_path, bookmark_folder_path, bookmark_folder_name, active_configuration, app_path, languages_config):
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
        result = request.DatabaseInsert(database_path, keys.TestKeys(), elements_val, 'TEST')
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
    condition_update = "set text='Hello world', float='1234.56789', bool='0', blob='4+4e4û4ÿ55M5á5¬5˝676', date='22/12/2012', time='00:30:58' where num_test='0'"
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
             active_configuration['pack_folder'], active_configuration['html_folder'],
             active_configuration['error_folder'], active_configuration['bin_folder'],
            )

        for v in folder_list:
            v = v.replace("#addon#", app_path)
            if not os.path.exists(v):
                os.makedirs(v)
        print(misc.ConsoleError("check folders ", 1, True))        
    except:
        print(misc.ConsoleError("check folders ", 1, False))
    #end Test : folders verification:
    #Test : html sub folder verification:
    print(" "*11 + "check help subfolder : ")        
    for h in languages_config:
        help_file = os.path.join(app_path, "html", h + ".html")
        if os.path.exists(help_file):
            print(misc.ConsoleError(str(h), 3, True))
        else:
            print(misc.ConsoleError(str(h), 3, False))
    #end Test : html sub folder verification:
    #Test : zip files verification:
    zip_file_list = \
        (
         active_configuration['workbase_file_path'].replace("#addon#", app_path),
         active_configuration['help_file_path'].replace("#addon#", app_path),
         active_configuration['img_file_path'].replace("#addon#", app_path),
        )
    print(" "*11 + "compress file : ")        
    for v in zip_file_list:
        name_file = str(v.split(os.path.sep)[-1])
        if os.path.exists(v):
            print(misc.ConsoleError(name_file, 2, True))
        else:
            print(misc.ConsoleError(name_file, 2, False))
    #end Test : zip files verification:
    #Test : bookmark verification:
    return(bookmark.VerifyBookmark(bookmark_path, bookmark_folder_path, bookmark_folder_name))
    #end Test : bookmark verification:















