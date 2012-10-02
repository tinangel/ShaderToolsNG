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
            v = keys.InputExceptionsKeys(v)
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
