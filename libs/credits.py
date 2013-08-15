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

def ShowCredits(credits_key):
    #Imports & external libs:
    try:
        import bpy, os, textwrap
    except:
        print("$hadertools : credits import error")
    #end Imports & external libs:
    credits_list = []
    credits_row = []

    title_row = credits_key['function'].capitalize() + " :"
    title_row = title_row.replace("_", " and ")
    name_row = credits_key['name'].rstrip(",")

    if len(name_row) >= 35:
        wrap_text = textwrap.wrap(name_row,35)
        count = 0
        for v in wrap_text:
            credits_row = []
            if count == 0:
                count = 1
                credits_row.append(title_row)
                credits_row.append(v)
            else:
                credits_row.append('')
                credits_row.append(v)
            
            credits_list.append(credits_row)
    else:
        credits_row.append(title_row)
        credits_row.append(name_row)
        credits_list.append(credits_row)
    
    return credits_list
    
    
    
    
    
