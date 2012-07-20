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
import bpy, os, sqlite3,  binascii
from copy import copy
        
#end Convert blobs elements
#Insert into database
def DatabaseInsert(database_path, elements, elements_val, table):
    ShaderToolsDatabase = sqlite3.connect(database_path) #open database
    DatabaseCursor = ShaderToolsDatabase.cursor() #create cursor
    request = "insert into '%s' (" % table   
    for e in elements: request = request + "'%s'," % e 
    request = request.rstrip(",") 
    request = request + ") values ("
    for v in elements_val: 
        if type(v).__name__ == 'bytes': request =request + '"%s",' % binascii.hexlify(v)
        else: request = request + "'%s'," % v
    request = request.rstrip(",") + ")"
    #here my request :
    #print(request)
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
#end Insert into database
#Select in database
def DatabaseSelect(database_path, elements, table, condition, options):
    ShaderToolsDatabase = sqlite3.connect(database_path) #open database
    DatabaseCursor = ShaderToolsDatabase.cursor() #create cursor
    request = "select "
    
    for e in elements:  request = request + e + ","
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

