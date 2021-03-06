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

import bpy, os, sqlite3,  binascii
from . import misc,  keys
from copy import copy
        
#end Convert blobs elements
#Insert into database
def DatabaseInsert(database_path, elements, elements_val, table, test,  option):
    ShaderToolsDatabase = sqlite3.connect(database_path) #open database
    DatabaseCursor = ShaderToolsDatabase.cursor() #create cursor
    request = ""
    if not option == 'force':
        request = "insert into '%s' (" % table   
        for e in elements: request = request + "'%s'," % e 
        request = request.rstrip(",") 
        request = request + ") values ("
        for v in elements_val:
            except_list = ("name",  "creator",  "category",  "description", "weblink",  "email")
            if option == 'save' and v in except_list:  v = keys.InputExceptionsKeys(v)
            if type(v).__name__ == 'bytes': request =request + '"%s",' % binascii.hexlify(v)
            else: request = request + "'%s'," % v
        request = request.rstrip(",") + ")"
    else: request = elements
    
    #here my request :
    #print(request)
    try:
        DatabaseCursor.execute(request)
        if not test : ShaderToolsDatabase.commit()
        DatabaseCursor.close() #close cursor
        ShaderToolsDatabase.close() #close database
        if option=='save': return (True,  request)
        return True    
    except:
        DatabaseCursor.close() #close cursor
        ShaderToolsDatabase.close() #close database
        if option=='save': return (False,  request)
        return False
#end Insert into database
#Select in database
def DatabaseSelect(database_path, elements, table, condition, options):
    ShaderToolsDatabase = sqlite3.connect(database_path) #open database
    DatabaseCursor = ShaderToolsDatabase.cursor() #create cursor
    request = "select "
    
    for e in elements:  request = request + e + ","
    if "," in table: request = request.rstrip(",") + " from %s " % table + condition
    else: request = request.rstrip(",") + " from '%s' " % table + condition
    #here my request :
    #print(request)
    try:
        DatabaseCursor.execute(request)
        
        if options == "one": #options 
            result = DatabaseCursor.fetchone()
        else:
            result = DatabaseCursor.fetchall()
        
        DatabaseCursor.close() #close cursor
        ShaderToolsDatabase.close() #close database 
        return result
    
    except:
        DatabaseCursor.close() #close cursor
        ShaderToolsDatabase.close() #close database
        return False
#end Select in database
#Count in database
def DatabaseCount(database_path, element, table, condition, options):
    ShaderToolsDatabase = sqlite3.connect(database_path) #open database
    DatabaseCursor = ShaderToolsDatabase.cursor() #create cursor
    request = "select count('%s')" % element  
    request = request.rstrip(",") + " from '%s' " % table + condition
    
    #here my request :
    try:
        DatabaseCursor.execute(request)
        
        if options == "one": #options
            result = DatabaseCursor.fetchone()
        else:
            result = DatabaseCursor.fetchall()
        
        DatabaseCursor.close() #close cursor
        ShaderToolsDatabase.close() #close database 
        return result
    except:
        DatabaseCursor.close() #close cursor
        ShaderToolsDatabase.close() #close database
        return False
#end Count in database
#Update into database
def DatabaseUpdate(database_path, table, condition):
    ShaderToolsDatabase = sqlite3.connect(database_path) #open database
    DatabaseCursor = ShaderToolsDatabase.cursor() #create cursor
    request = "update '%s' " % table + condition

    #here my request :
    try:
        DatabaseCursor.execute(request)
        ShaderToolsDatabase.commit()
        DatabaseCursor.close() #close cursor
        ShaderToolsDatabase.close() #close database 
        return True
    
    except:
        DatabaseCursor.close() #close cursor
        ShaderToolsDatabase.close() #close database
        print("$haderTools : error update database")
        print(" "*15 + "request : %s"%request)
        return False  
#end Update into database
#Delete in database
def DatabaseDelete(database_path, table, condition):
    ShaderToolsDatabase = sqlite3.connect(database_path) #open database
    DatabaseCursor = ShaderToolsDatabase.cursor() #create cursor
    request = "delete from '%s' " % table + condition
    
    #here my request :
    try:
        DatabaseCursor.execute(request)
        ShaderToolsDatabase.commit()
        DatabaseCursor.close() #close cursor
        ShaderToolsDatabase.close() #close database 
        return True
    
    except:
        DatabaseCursor.close() #close cursor
        ShaderToolsDatabase.close() #close database        
        return False  
#end Delete in database
#Max in database
def DatabaseMax(database_path, element, table, condition, options):
    ShaderToolsDatabase = sqlite3.connect(database_path) #open database
    DatabaseCursor = ShaderToolsDatabase.cursor() #create cursor
    request = "select max(%s)" % element  
    request = request.rstrip(",") + " from '%s' " % table + condition
    #here my request :
    try:
        DatabaseCursor.execute(request)
        
        if options == "one": #options
            result = DatabaseCursor.fetchone()
        else:
            result = DatabaseCursor.fetchall()
        
        DatabaseCursor.close() #close cursor
        ShaderToolsDatabase.close() #close database
        if result[0] == None or result[0] == '': return (0, )        
        else: return result
    except:
        DatabaseCursor.close() #close cursor
        ShaderToolsDatabase.close() #close database
        return False
#end Max in database

def DatabaseDump(default_paths,  path,  name):
    ShaderToolsDatabase = sqlite3.connect(path) #open database
    dump_file = os.path.join(default_paths['temp'],  name)
    if os.path.exists(dump_file): os.remove(dump_file)
    with open(dump_file, 'w') as f:
        for line in ShaderToolsDatabase.iterdump(): f.write('%s\n' % line)
    ShaderToolsDatabase.close() #close database
    return True

def DatabaseDumpImport(default_paths, api_functions,  path,  name):
    ctx_scene = eval(api_functions['context_scene'])
    ctx_scene.shadertoolsng_utils_barm = 0

    ShaderToolsDatabase = sqlite3.connect(path)
    DatabaseCursor = ShaderToolsDatabase.cursor()
    script_file = os.path.join(default_paths['temp'],  name.replace(".sqlite",  ".blump"))
    fscript = open(script_file,'r', encoding = "utf-8")
    line = fscript.read()
    counter = 0
    counter_two = 0
    total_count = line.count("INSERT INTO")
    request_split = line.split(';\n')
    for e in request_split:
        if "CREATE TABLE " not in e: DatabaseCursor.executescript(e)
        if "INSERT INTO" in e:
            counter = counter + 1
            counter_two = counter_two + 1
            if counter_two >= int(total_count/10):
                counter_two = 0
                try:ctx_scene.shadertoolsng_utils_barm = misc.CrossProduct(counter, total_count)
                except:pass
    
    if os.path.exists(script_file): os.remove(script_file)
    counter = total_count    
    ctx_scene.shadertoolsng_utils_barm = 100
    DatabaseCursor.close() #close cursor
    ShaderToolsDatabase.close() #close database
    
