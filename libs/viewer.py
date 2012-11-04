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
import bpy, os, platform

def OpenViewer(program_parameters):
    if platform.system() == 'Darwin': os.popen("open -n -a '%s' --args '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s'" %  program_parameters)
    else: os.popen('"%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' %  program_parameters)

