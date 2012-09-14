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

import bpy, os, webbrowser

def help_me(app_path, active_language_name):
    #I open help file:
    if '(French)' in active_language_name: active_language_name = 'French'
    elif '(English)' in active_language_name: active_language_name = 'English'
        
    url = "file://" + os.path.join(app_path, "html", active_language_name, "index.html")
    webbrowser.open_new(url)       
