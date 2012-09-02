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
#-*- coding: utf-8 -*-

bl_info = {
    "name": "ShaderTools Next Gen",
    "author": "GRETETE Karim (Tinangel)",
    "version": (0, 8, 0),
    "blender": (2, 6, 0),
    "api": 41098,
    "location": "User Preferences",
    "description": "Shader tools for blender",
    "warning": "Alpha version",
    "wiki_url": "http://noadress",
    "tracker_url": "",
    "support": 'COMMUNITY',
    "category": "System",}

print("*"*78)
print("*" + " "*22 + "Shader Tools Next Gen - Console" + " "*23 + "*")
print("*"*78)

#Imports & external libs:
try:
    import bpy, sqlite3, os, platform, locale, shutil, sys, time, shader_tools_ng.libs, threading,  webbrowser
    from shader_tools_ng.libs import *
    from bpy.types import Header
    print(misc.ConsoleError("Import external module ", 0, True))
except: print(misc.ConsoleError("Import external module ", 0, False))

try:
    misc.LogError("", True)
    misc.LogError("*"*78, True)
    misc.LogError("*" + " "*22 + "Shader Tools Next Gen - Console" + " "*23 + "*", False)
    misc.LogError("*"*78, False)
    blender_version = str(bpy.app.version[0]) + "." + str(bpy.app.version[1]) + str(bpy.app.version[2])
    default_paths = environment.DefaultPaths()
    api_functions = environment.ApiDatas(default_paths['apis_database'], blender_version)
    configurations_config = environment.ConfigurationsDatas(default_paths['configs_database'], False)
    languages_config = environment.LanguagesDatas(default_paths['languages_database'])
    active_configuration = environment.ActiveConfigurations(configurations_config)
    active_languages = environment.ActiveLanguage(languages_config, active_configuration['language'])
    about_config = environment.AboutDatas(default_paths['database'])
    active_categories = environment.MaterialsCatergories(active_languages)
    names_config = environment.ConfigurationsNames(configurations_config)
    options_actions = environment.ConfigurationsOptions(active_languages)
    names_languages = environment.LanguagesNames(languages_config)
    space_access_name = active_languages['space_access_name'] + " "
    active_history = history.CurrentHistory(default_paths,  active_configuration, api_functions, active_languages)
    default_paths = environment.ConvertDefaultPaths(default_paths,  active_configuration)
    print(misc.ConsoleError("Globals ", 0, True))
except: print(misc.ConsoleError("Globals ", 0, False))

#Functions
conf_current_name = ""
conf_current_idx = 1
database_stuff = False
inf_current_weblink = False
#Tests & verifications
bookmarks_folder_path = os.path.join(default_paths['app'], active_languages['menu_bookmarks_name'])
update = checkup.MakeCheckup(default_paths['database'], default_paths['configs_database'], default_paths['bookmarks'], 
                             bookmarks_folder_path, active_languages['menu_bookmarks_name'], active_configuration, default_paths['app'], 
                             languages_config,  default_paths)
lauch_progress_bar = threading.Thread(None, open.CreateThumbnails, "Create_thumbnails", (default_paths,  active_configuration, api_functions, active_languages, False, ), {})
lauch_progress_bar.start()
#Panel and buttons 
def ctx_active_object():
    global api_functions
    ctx_active_object = False
    try:
        eval(api_functions['type'])
        ctx_active_object = True
    except:
        ctx_active_object = False
    return ctx_active_object 

def OpenUpdateHistory(self,  context): search.FilterHistory(default_paths,  active_configuration, api_functions, active_languages,  self.history_EP)
def OpenSearch(self,  context): 
    advanced_search_properties = \
        {
            'name': self.name_BP, 
            'keywords': self.search_SP, 
            'description': self.description_BP, 
            'creator': self.creator_BP, 
            'category': self.category_BP, 
            'weblink': self.weblink_BP, 
            'email': self.email_BP, 
        }
    try:
        search.FilterSearch(default_paths,  active_configuration, api_functions, active_languages,  advanced_search_properties)
    except:
        error = active_languages['menu_error_error050'] % self.search_SP
        misc.LogAndPrintError((error,  error))
        
def UpdateProgressBar(self,  context): return None
def LoadingMigrateProgressBar(path):
    global database_stuff
    database_stuff = True
    ctx_scene = eval(api_functions['context_scene'])
    number_max = request.DatabaseCount(path, "Mat_Index", "MATERIALS", "", 'one')
    version_values = request.DatabaseSelect(path, keys.OldVersionKeys(), "VERSION", "", 'one')
    errors_list = ("*"*78,  "*" + " "*22 + "Shader Tools Next Gen - Migrate" + " "*23 + "*", "Database version : %s" %version_values[2], )
    error_val = (0,  1,  0,  2)
    for v in error_val: misc.LogAndPrintError((errors_list[v], errors_list[v]))
    misc.SaveDatabase(default_paths['database'],  default_paths['save'],  default_paths['bin'])
 
    for v in range(2, number_max[0]+1):
        ctx_scene.shadertoolsng_utils_bar = misc.CrossProduct(v+1, number_max[0]+1)
        err = active_languages['menu_error_error037'] % str(v)
        print("\n%s" % err)
        misc.LogError("*"*3, 0)
        misc.LogError(err, 0)
        migrate.MigrateV1V2(path, api_functions, active_languages, active_configuration, default_paths, v)
        open.CreateThumbnails(default_paths,  active_configuration, api_functions, active_languages, False)
        misc.LogError("*"*3 +"\n", 0)
    database_stuff = False

class RestoreFilters(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_restore"
    bl_label = ''

    def execute(self, context):
        database_folder = os.path.join(default_paths['app'],  active_languages['menu_bookmarks_name'])
        tempory_folder = os.path.join(database_folder,  ".tempory")
        search.MoveAllInsideFolder(active_configuration, api_functions, active_languages, tempory_folder,  database_folder)
        exec(api_functions['ops_file_refresh'])
        return {'FINISHED'}

class Errors(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_errors"
    bl_label = space_access_name + active_languages['bl_id_name_logs']

    def execute(self, context):
        global default_paths, active_configuration, api_functions
        log.OpenLog(default_paths['app'], active_configuration, api_functions)
        return {'FINISHED'}

class UpdateWarning(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_warning"
    bl_label = " "

    def execute(self, context):
        return {'FINISHED'}

class BeforeOpen(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_before"
    bl_label = ''    

    def execute(self, context):
        global database_stuff,  active_history
        if not database_stuff:
            ops_object = eval(api_functions['ops_object'])
            Open.history_EP[1]['items'] = active_history
            eval(api_functions['utils_unregister_class'].replace("#1#", "Open"))
            eval(api_functions['utils_register_class'].replace("#1#", "Open"))
            database_folder = os.path.join(default_paths['app'],  active_languages['menu_bookmarks_name'])
            tempory_folder = os.path.join(database_folder,  ".tempory")
            search.MoveAllInsideFolder(active_configuration, api_functions, active_languages, tempory_folder,  database_folder)
            ops_object.shadertoolsng_open('INVOKE_DEFAULT')
        return {'FINISHED'}

class InformationsWeblink(eval(api_functions['types_operator'])): 
    bl_idname = "object.shadertoolsng_weblink"
    bl_label = ''    
    
    def execute(self, context):
        global  inf_current_weblink
        try:
            if  inf_current_weblink:
                webbrowser.open_new( inf_current_weblink)
                inf_current_weblink = False
        except:pass
        return {'FINISHED'}   

class BeforeInformations(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_before_inf"
    bl_label = space_access_name + active_languages['bl_id_name_search_infos']      

    ctx = eval(api_functions['props'])
    type = ctx.EnumProperty(name='info',  items=informations.InformationsEnumItems(default_paths['database']))

    def invoke(self, context, event):
        wm = eval(api_functions['invoke_search_popup'].replace("#1#", "self"))
        return {'PASS_THROUGH'}

    def execute(self, context):
        global inf_current_weblink
        ops_object = eval(api_functions['ops_object'])
        eval(api_functions['utils_unregister_class'].replace("#1#", "Informations"))
        eval(api_functions['utils_register_class'].replace("#1#", "Informations"))
        infos = informations.InformationsSelectedItem(default_paths['database'],  self.type)
        if infos == None: 
            ops_object.shadertoolsng_infos('INVOKE_DEFAULT',  inf_name_SP='No informations',  inf_creator_SP='No informations',  inf_description_SP='No informations', 
                                                                inf_category_SP='No informations',  inf_weblink_SP='No informations',  inf_email_SP='No informations')      
        else:
            inf_current_weblink = infos[5]
            ops_object.shadertoolsng_infos('INVOKE_DEFAULT',  inf_name_SP=infos[1].replace("$T_",  ""),  inf_creator_SP=infos[3],  inf_description_SP=infos[2], 
                                                                inf_category_SP=infos[4],  inf_weblink_SP=infos[5],  inf_email_SP=infos[6])      
        return {'PASS_THROUGH'}

class Informations(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_infos"
    bl_label = ''
    
    ctx = eval(api_functions['props'])
    #Informations properties
    inf_name_SP = ctx.StringProperty()
    inf_description_SP = ctx.StringProperty(name=active_languages['menu_information_description'])
    inf_creator_SP = ctx.StringProperty()
    inf_category_SP = ctx.StringProperty(name=active_languages['menu_information_category'])
    inf_weblink_SP = ctx.StringProperty()
    inf_email_SP = ctx.StringProperty(name=active_languages['menu_information_email'])

    def draw(self, context):
        global inf_current_self,  inf_current_context
        inf_current_self = self
        inf_current_context = context
        ctx_scene = eval(api_functions['context_scene'])
        layout = self.layout
        row = layout.row(align=True)
        row.label(active_languages['menu_information_label01'])
        row = layout.row(align=True)
        row.label(active_languages['menu_information_label02'] + " :")                        
        row.label(self.inf_name_SP)                        
        row = layout.row(align=True)
        row.label(active_languages['menu_information_creator'] + " :") 
        row.label(self.inf_creator_SP)            
        row = layout.row(align=True)
        row.label(active_languages['menu_information_category'] + " :") 
        row.label(self.inf_category_SP)
        row = layout.row(align=True)
        row.label(active_languages['menu_information_email'] + " :") 
        row.label(self.inf_email_SP)
        row = layout.row(align=True)
        row.prop(self, "inf_description_SP")
        row = layout.row(align=True)
        row.operator("object.shadertoolsng_weblink",  text=active_languages['menu_information_weblink'])            
        row = layout.row(align=True)
         
    def invoke(self, context, event):
        wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=400"))
        return {'RUNNING_MODAL'}
        
    def execute(self, context): 
        return {'FINISHED'}   

class Open(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_open"
    bl_label = space_access_name + active_languages['bl_id_name_open']  
    
    global  database_stuff
    ctx = eval(api_functions['props'])
    types_scene = eval(api_functions['types_scene'])
    msg = "%s %s" % (active_languages['menu_search_label02'] ,  active_languages['menu_search_label03'])

    filename_ext = ".jpg"
    filename = ctx.StringProperty(subtype="FILENAME")
    #Search properties
    name_BP = ctx.BoolProperty(name=active_languages['menu_search_name'], default=1)
    history_EP = ctx.EnumProperty(name=active_languages['menu_history_label01'],items=(active_history),  update=OpenUpdateHistory)
    search_SP = ctx.StringProperty(name=active_languages['menu_search_label01'],  update=OpenSearch,  description=msg)
    description_BP = ctx.BoolProperty(name=active_languages['menu_search_description'], default=0)
    creator_BP = ctx.BoolProperty(name=active_languages['menu_search_creator'], default=0)
    category_BP = ctx.BoolProperty(name=active_languages['menu_search_category'], default=0)
    weblink_BP = ctx.BoolProperty(name=active_languages['menu_search_weblink'], default=0)
    email_BP = ctx.BoolProperty(name=active_languages['menu_search_email'], default=0)
    
    def draw(self, context):
        ctx_scene = eval(api_functions['context_scene'])
        layout = self.layout
        row = layout.row(align=True)
        if database_stuff: 
            row.label(active_languages['menu_error_error040'], icon='RADIO')
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error041'])
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error042'])
        else:
            row.label(active_languages['menu_search_title'])
            row = layout.row(align=True)
            row.prop(self, "search_SP") 
            row = layout.row(align=True)
            row.label(active_languages['menu_search_label04'])
            row = layout.row(align=True)
            row.prop(self, "name_BP")            
            row.prop(self, "description_BP")            
            row = layout.row(align=True)
            row.prop(self, "creator_BP")
            row.prop(self, "category_BP")                        
            row = layout.row(align=True)
            row.prop(self, "weblink_BP")            
            row.prop(self, "email_BP")            
            row = layout.row(align=True)
            row.label(" ")
            row = layout.row(align=True)
            row.label(active_languages['menu_history_title'])
            row = layout.row(align=True)
            row.prop(self, "history_EP")            
            row = layout.row(align=True)
            row.label(" ")
            row = layout.row(align=True)
            row.operator("object.shadertoolsng_restore", text=active_languages['menu_open_restore'], icon='FILE_REFRESH')
            row = layout.row(align=True)
            row.operator("object.shadertoolsng_before_inf", text=active_languages['menu_information_label01'], icon='INFO')
            row = layout.row(align=True)
            row.label(" ")
            
    def invoke(self, context, event):
        eval(api_functions['utils_unregister_class'].replace("#1#", "BeforeInformations"))
        eval(api_functions['utils_register_class'].replace("#1#", "BeforeInformations"))
        if not database_stuff : wm = eval(api_functions['fileselect_add'].replace("#1#", "self"))
        else: wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=500"))
        return {'RUNNING_MODAL'}
        
    def execute(self, context):
        global database_stuff,  active_history
        if not database_stuff :
            ctx_scene = eval(api_functions['context_scene'])
            ops_object = eval(api_functions['ops_object'])
            ctx = eval(api_functions['props'])
            ctx_scene.shadertoolsng_utils_bar = 0
            step_number = 4
            open.ImportMaterialInApp(default_paths,  active_configuration, api_functions, active_languages, self.filename,  step_number)
            history.UpdateHistory(default_paths,  active_configuration, api_functions, active_languages,  self.filename,  active_history)
            active_history = history.CurrentHistory(default_paths,  active_configuration, api_functions, active_languages)
        return {'FINISHED'}
        
class Save(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_save"
    bl_label = space_access_name + active_languages['bl_id_name_save']    

    global  database_stuff
    
    def draw(self, context):
        if database_stuff: 
            layout = self.layout
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error040'], icon='RADIO')
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error041'])
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error042'])
        else: 
            layout = self.layout
            row = layout.row(align=True)
            row.label("En cours de developpement", icon='RADIO')
 
    def invoke(self, context, event):
        if not database_stuff: wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self"))
        else: wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self"))
        return {'RUNNING_MODAL'} 
    
    def execute(self, context):
        global database_stuff
        if not database_stuff:
           print("Database has not stuff") 
        return {'FINISHED'}   

class Export(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_export"
    bl_label = space_access_name + active_languages['bl_id_name_export']    

    global default_paths
    ctx = eval(api_functions['props'])
    filename_ext = ".blex"
    filter_glob = ctx.StringProperty(default="*.blex;*.BLEX", options={'HIDDEN'})
    filename = ctx.StringProperty(subtype="FILENAME")
    filepath = ctx.StringProperty(subtype="FILE_PATH")    

    creator_SP = ctx.StringProperty(name=active_languages['menu_configuration_creator_name'], default=active_configuration['author'])
    take_preview_BP = ctx.BoolProperty(name=active_languages['take_preview'], default=int(active_configuration['take_preview']))
    weblink_SP = ctx.StringProperty(name=active_languages['menu_configuration_web_link'], default=active_configuration['web_link'])
    email_SP = ctx.StringProperty(name=active_languages['menu_configuration_email'], default=active_configuration['email_creator'])
    key_words_SP = ctx.StringProperty(name=active_languages['menu_configuration_key_words'], default=active_configuration['key_words'])
    description_SP = ctx.StringProperty(name=active_languages['menu_configuration_description'], default=active_configuration['description'])

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        if ctx_active_object():
            row.label(active_languages['menu_configuration_material_name'] + ":")
            row.label(eval(api_functions['material_name']))
            row = layout.row(align=True)
            row.prop(self, "take_preview_BP")    
            row = layout.row(align=True)
            row.prop(self, "creator_SP")    
            row = layout.row(align=True)
            row.prop(self, "weblink_SP")    
            row = layout.row(align=True)
            row.prop(self, "email_SP")    
            row = layout.row(align=True)
            row.prop(self, "description_SP")    
            row = layout.row(align=True)
            row.prop(self, "key_words_SP")    
        else:
            row.label(active_languages['menu_error_error002'], icon='RADIO')

    def invoke(self, context, event):
        if ctx_active_object(): wm = eval(api_functions['fileselect_add'].replace("#1#", "self"))
        else: wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=500"))
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if ctx_active_object():
            global default_paths, active_configuration, api_functions
            material_dict = \
                    {
                     "filepath":self.filepath.replace(".",  "_"), "filename":self.filename.replace(".",  "_"), "app_path":default_paths['app'],
                     "material_name":eval(api_functions['material_name']), "creator":self.creator_SP,
                     "weblink":self.weblink_SP,"email":self.email_SP,"description":self.description_SP,
                     "key_words":self.key_words_SP, "take_preview":self.take_preview_BP,
                     "temp":default_paths['temp'],  "zip":default_paths['zip'],
                    }
            misc.Clear(os.path.join(material_dict['temp'], material_dict['material_name']), 'files', 'all', active_languages)
            exporter.MaterialExport(material_dict, api_functions, active_languages)
            exporter.MaterialRampsExport(material_dict, api_functions, 'diffuse', active_languages)
            exporter.MaterialRampsExport(material_dict, api_functions, 'specular', active_languages)
            exporter.TextureExport(material_dict, api_functions, active_languages)
            try:
                zip_file_path = zip.Zip(material_dict, api_functions, active_languages)
                if material_dict['filepath'].find(".blex") < 0:
                    material_dict['filepath'] = material_dict['filepath'] + ".blex"
                shutil.copy2(zip_file_path, material_dict['filepath'])
                print(active_languages['menu_error_error027'])
                misc.LogError(active_languages['menu_error_error027'], False)
            except:
                print(active_languages['menu_error_error028'])
                misc.LogError(active_languages['menu_error_error028'], False)
            try:
                misc.Clear(default_paths['zip'], 'all', '', active_language)
                misc.Clear(default_paths['temp'], 'all', '', active_language)
            except: pass
            if self.take_preview_BP:
                try: 
                    render.PreviewRenderInternal(api_functions, active_configuration, material_dict)
                    print(active_languages['menu_error_error023'])
                    misc.LogError(active_languages['menu_error_error023'], False)
                except:
                    print(active_languages['menu_error_error024'])
                    misc.LogError(active_languages['menu_error_error024'], False)
        else:
            eval(api_functions['utils_unregister_class'].replace("#1#", "Export"))
            eval(api_functions['utils_register_class'].replace("#1#", "Export"))
        return {'FINISHED'}   

class Import(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_import"
    bl_label = space_access_name + active_languages['bl_id_name_import']    

    global default_paths
    ctx = eval(api_functions['props'])
    filename_ext = ".blex"
    filter_glob = ctx.StringProperty(default="*.blex;*.BLEX", options={'HIDDEN'})
    filename = ctx.StringProperty(subtype="FILENAME")
    filepath = ctx.StringProperty(subtype="FILE_PATH")    

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        if not eval(api_functions['blend_save']):
            row.label(active_languages['menu_error_error050'], icon="RADIO")
        else:
            row.label(active_languages['menu_import_label001'], icon="HELP")
            row = layout.row(align=True)
            row.label(eval(active_languages['menu_import_label002']))

    def invoke(self, context, event):
        if not eval(api_functions['blend_save']): wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self"))
        else: wm = eval(api_functions['fileselect_add'].replace("#1#", "self"))
        return {'RUNNING_MODAL'}

    def execute(self, context):
        importer.BlexImport(self.filepath, api_functions, active_languages, active_configuration,default_paths)
        return {'FINISHED'}   

class New(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_new"
    bl_label = space_access_name + active_languages['bl_id_name_create']    

    def execute(self, context):
        new.CreateNew(default_paths['app'], active_configuration, api_functions, active_languages)
        return {'PASS_THROUGH'}   

def ConfigurationUpdateDefaultConfig(self,  context):
    global default_paths,  active_configuration,  configurations_config,  conf_current_idx
    try:
        request.DatabaseUpdate(default_paths['configs_database'], 'CONFIGURATION', 'set default_config=0 where default_config=1')
        request.DatabaseUpdate(default_paths['configs_database'], 'CONFIGURATION', 'set default_config=1 where num_configuration=%s' % str(conf_current_idx))
        configurations_config = environment.ConfigurationsDatas(default_paths['configs_database'], False)
        active_configuration = environment.ActiveConfigurations(configurations_config)
        default_paths = environment.ConvertDefaultPaths(default_paths,  active_configuration)
        lauch_progress_bar = threading.Thread(None, open.CreateThumbnails, "Create_thumbnails", (default_paths,  active_configuration, api_functions, active_languages, False, ), {})
        lauch_progress_bar.start()
    except:
        error = active_languages['menu_error_error051']
        misc.LogAndPrintError((error,  error))
        pass
    return None
    
class Configuration(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_configuration"
    bl_label = space_access_name + active_languages['bl_id_name_config']    

    ctx = eval(api_functions['props'])
    conf_choice_EP = ctx.EnumProperty(name=active_languages['menu_configuration_select_title'],items=(names_config))
    conf_language_EP = ctx.EnumProperty(name=active_languages['menu_configuration_langage_choice'],items=(names_languages),default=active_configuration['language'])
    conf_options_EP = ctx.EnumProperty(name=active_languages['menu_configuration_options'],items=(options_actions),default=active_configuration['option'],)
    category_EP = ctx.EnumProperty(name=active_languages['menu_configuration_category'],items=(active_categories),default=active_configuration['category'])
    conf_name_SP = ctx.StringProperty(name=active_languages['menu_configuration_name'], default=active_configuration['name'])
    conf_current_name = active_configuration['name']
    conf_default_BP = ctx.BoolProperty(name="", default=active_configuration['default_config'],  update=ConfigurationUpdateDefaultConfig)
    mat_name_SP = ctx.StringProperty(name=active_languages['menu_configuration_material_name'], default=active_configuration['material_name'])
    key_words_SP = ctx.StringProperty(name=active_languages['menu_configuration_key_words'], default=active_configuration['key_words'])
    description_SP = ctx.StringProperty(name=active_languages['menu_configuration_description'], default=active_configuration['description'])
    creator_SP = ctx.StringProperty(name=active_languages['menu_configuration_creator_name'], default=active_configuration['author'])
    weblink_SP = ctx.StringProperty(name=active_languages['menu_configuration_web_link'], default=active_configuration['web_link'])
    email_SP = ctx.StringProperty(name=active_languages['menu_configuration_email'], default=active_configuration['email_creator'])
    conf_res_x_IP = ctx.IntProperty(name=active_languages['menu_configuration_resolution_x'], min=active_configuration['resolution_min'], \
                                    max=active_configuration['resolution_max'], default=active_configuration['resolution_default_x'])
    conf_res_y_IP = ctx.IntProperty(name=active_languages['menu_configuration_resolution_y'], min=active_configuration['resolution_min'], \
                                    max=active_configuration['resolution_max'], default=active_configuration['resolution_default_y'])
    take_preview_BP = ctx.BoolProperty(name="", default=int(active_configuration['take_preview']))
    database_SP = ctx.StringProperty(name=active_languages['menu_configuration_base_path'], default=misc.ConvertMarkOut(active_configuration['database_path'], default_paths['app']))
    auto_save_IP = ctx.IntProperty(name="", min=1, max=50, default=active_configuration['auto_save'])
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_current_index'] + ":")
        row.label(conf_current_idx)
        row.label(" ")
        row = layout.row(align=True)
        row.prop(self, "conf_name_SP")
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_default_config'] + ":")
        row.prop(self, "conf_default_BP")
        row.label(" ")
        row.label(" ")
        row = layout.row(align=True)
        row.prop(self, "conf_language_EP")
        row = layout.row(align=True)
        row.prop(self, "conf_options_EP")
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_informations'])
        row = layout.row(align=True)
        row.prop(self, "mat_name_SP")
        row = layout.row(align=True)
        row.prop(self, "description_SP")
        row = layout.row(align=True)
        row.prop(self, "creator_SP")
        row = layout.row(align=True)
        row.prop(self, "weblink_SP")
        row = layout.row(align=True)
        row.prop(self, "email_SP")
        row = layout.row(align=True)
        row.prop(self, "category_EP")
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_preview_parameters'])
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_resolution_x'] + ":")
        row.prop(self, "conf_res_x_IP")
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_resolution_y'] + ":")
        row.prop(self, "conf_res_y_IP")
        row = layout.row(align=True)
        row.label(active_languages['take_preview'] + ":")
        row.prop(self, "take_preview_BP")
        row.label(" ")
        row.label(" ")
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_base_parameters'])
        row = layout.row(align=True)
        row.prop(self, "database_SP")
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_auto_save_1'] )
        row.prop(self, "auto_save_IP")
        row.label(active_languages['menu_configuration_auto_save_2'] )

    def invoke(self, context, event):
        wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=520"))
        return {'RUNNING_MODAL'}

    def execute(self, context):
        global default_paths, languages_config, active_configuration, active_languages, active_categories, names_config, options_actions,\
               names_languages, space_access_name, ConfigurationSearch, conf_current_idx 
        configurations_config = environment.ConfigurationsDatas(default_paths['configs_database'], False)
        c = self.conf_options_EP.split("_")[-1]
        if c == "delete":
            my_new_config = \
                {"num_configuration": conf_current_idx, "default_config":misc.ConvertBoolStringToNumber(self.conf_default_BP), 
                 "name":'', "database_path":'', "author":'', "description":'',
                 "web_link":'', "material_name":'', "key_words":'', "category":'', "email_creator":'', "resolution_min":0, 
                 "resolution_default_x":0, "resolution_default_y":0, "resolution_max":0, "language":'', "error_folder":'',
                "html_folder":'', "save_folder":'', "temp_folder":'', "zip_folder":'', "workbase_file_path":'', "bin_folder":'', 
                "help_file_path":'', "img_file_path":'', "option":'', "take_preview":0,"auto_save":0, "load_number":0, }
            configuration.DeleteConfiguration(default_paths['configs_database'], my_new_config, names_config, active_languages)
        else:
            my_new_config = \
                {"num_configuration": conf_current_idx, "default_config":misc.ConvertBoolStringToNumber(self.conf_default_BP), "name":self.conf_name_SP, 
                 "database_path":self.database_SP, "author":self.creator_SP, "description":self.description_SP,
                 "web_link":self.weblink_SP, "material_name":self.mat_name_SP, "key_words":self.key_words_SP,
                 "category":self.category_EP, "email_creator":self.email_SP,
                 "resolution_min":active_configuration['resolution_min'], "resolution_default_x":self.conf_res_x_IP,
                 "resolution_default_y":self.conf_res_y_IP, "resolution_max":active_configuration['resolution_max'],
                 "language":self.conf_language_EP, "error_folder":active_configuration['error_folder'],
                 "html_folder":active_configuration['html_folder'], "save_folder":active_configuration['save_folder'],
                 "temp_folder":active_configuration['temp_folder'], "zip_folder":active_configuration['zip_folder'],
                 "workbase_file_path":active_configuration['workbase_file_path'], 
                 "bin_folder":active_configuration['bin_folder'], "help_file_path":active_configuration['help_file_path'],
                 "img_file_path":active_configuration['img_file_path'], "option":'menu_configuration_option_save', "name2":self.conf_name_SP,
                 "take_preview":misc.ConvertBoolStringToNumber(self.take_preview_BP), "auto_save":self.auto_save_IP,  "load_number":0}
            configuration.SaveConfiguration(default_paths['configs_database'], my_new_config, active_languages)

        configurations_config = environment.ConfigurationsDatas(default_paths['configs_database'], False)
        active_configuration = environment.ActiveConfigurations(configurations_config)
        names_config = environment.ConfigurationsNames(configurations_config)
        options_actions = environment.ConfigurationsOptions(active_languages)
        ConfigurationSearch.type[1]['items'] = names_config
        Configuration.conf_choice_EP[1]['items'] = names_config

        class_reg = ("ConfigurationSearch", "Export",)
        for c in class_reg:        
                eval(api_functions['utils_unregister_class'].replace("#1#", c))
                eval(api_functions['utils_register_class'].replace("#1#", c))
        default_paths = environment.ConvertDefaultPaths(default_paths,  active_configuration)
        lauch_progress_bar = threading.Thread(None, open.CreateThumbnails, "Create_thumbnails", (default_paths,  active_configuration, api_functions, active_languages, False, ), {})
        lauch_progress_bar.start()
        return {'FINISHED'}

class ConfigurationSearch(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_configuration_search"
    bl_label = ''
    
    global  database_stuff
    ctx = eval(api_functions['props'])
    type = ctx.EnumProperty(name=active_languages['menu_configuration_select_title'],items=(names_config),)
        
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(active_languages['menu_error_error040'], icon='RADIO')
        row = layout.row(align=True)
        row.label(active_languages['menu_error_error041'])
        row = layout.row(align=True)
        row.label(active_languages['menu_error_error042'])
        
    def invoke(self, context, event):
        if not database_stuff: 
            wm = eval(api_functions['invoke_search_popup'].replace("#1#", "self"))
        else: 
             wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self"))
        return {'PASS_THROUGH'}

    def execute(self, context):
        global default_paths, conf_current_name, conf_current_idx,  database_stuff
        if not database_stuff: 
            conf_current_idx = str(self.type)
            ops_object = eval(api_functions['ops_object'])
            configurations_config = environment.ConfigurationsDatas(default_paths['configs_database'], False)
            selected_configuration = configurations_config[misc.EnumPropertyItemsInverseIdx(conf_current_idx, configurations_config)]
            conf_current_name = selected_configuration['name']
            eval(api_functions['utils_unregister_class'].replace("#1#", "Configuration"))
            eval(api_functions['utils_register_class'].replace("#1#", "Configuration"))
            ops_object.shadertoolsng_configuration('INVOKE_DEFAULT', conf_choice_EP=conf_current_idx , conf_language_EP=selected_configuration['language'],  
                                 conf_options_EP=selected_configuration['option'], category_EP=selected_configuration['category'],
                                 conf_name_SP=selected_configuration['name'], conf_default_BP=selected_configuration['default_config'],
                                 mat_name_SP=selected_configuration['material_name'], key_words_SP=selected_configuration['key_words'],
                                 description_SP=selected_configuration['description'], creator_SP=selected_configuration['author'],
                                 weblink_SP=selected_configuration['web_link'], email_SP=selected_configuration['email_creator'],
                                 conf_res_x_IP=selected_configuration['resolution_default_x'], conf_res_y_IP=selected_configuration['resolution_default_y'],
                                 database_SP=misc.ConvertMarkOut(selected_configuration['database_path'], default_paths['app']),
                                 take_preview_BP=int(selected_configuration['take_preview']),  auto_save_IP=selected_configuration['auto_save'])
        return {'PASS_THROUGH'}   

class Help(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_help"
    bl_label = space_access_name + active_languages['bl_id_name_help']    

    def execute(self, context):
        help.help_me(default_paths['app'], active_languages['name_language'])
        return {'FINISHED'}   

class Credits(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_credits"
    bl_label = space_access_name + active_languages['bl_id_name_credits']    

    def draw(self, context):
        credits_keys = keys.CreditsKeys()
        layout = self.layout
        row = layout.row(align=True)
        row.label("Credits :", icon='QUESTION')
        for k in credits_keys:
            row = layout.row(align=True)
            r = credits.ShowCredits(about_config[k])
            for v in r:
                row.label(v[0])
                row.label(v[1])
                row = layout.row(align=True)

    def invoke(self, context, event):
        return eval(api_functions['invoke_popup'].replace("#1#", "self, width = 380"))

    def execute(self, context):
        return {'FINISHED'}   

class UtilsMigrate(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_utils_migrate"
    bl_label = space_access_name + active_languages['bl_id_name_utils_migrate']    

    global database_stuff
    
    ctx = eval(api_functions['props'])
    filename_ext = ".sqlite"
    filter_glob = ctx.StringProperty(default="*.sqlite;*.SQLITE", options={'HIDDEN'})
    filename = ctx.StringProperty(subtype="FILENAME")
    filepath = ctx.StringProperty(subtype="FILE_PATH")   

    def draw(self, context):
        if not database_stuff:
            layout = self.layout
            row = layout.row(align=True)
            row.label(active_languages['menu_utils_migrate_help01'], icon="HELP")
            row = layout.row(align=True)
        else:
            layout = self.layout
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error040'], icon='RADIO')
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error041'])
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error042'])

    def invoke(self, context, event):
        if not database_stuff: 
           wm = eval(api_functions['fileselect_add'].replace("#1#", "self"))
        else: 
             wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self"))
        return {'RUNNING_MODAL'} 

    def execute(self, context):
        global database_stuff
        if not database_stuff: 
            lauch_progress_bar = threading.Thread(None, LoadingMigrateProgressBar, None, (self.filepath,), {})
            lauch_progress_bar.start()
        return {'FINISHED'}   

def OpenSaveSwitch(self, context):
    ops_object = eval(api_functions['ops_object'])
    if self.shadertoolsng_open_save == 'buttons_open':ops_object.shadertoolsng_before('INVOKE_DEFAULT')
    else:ops_object.shadertoolsng_save('INVOKE_DEFAULT')

def ExportImportSwitch(self, context):
    ops_object = eval(api_functions['ops_object'])
    if self.shadertoolsng_export_import == 'buttons_export':ops_object.shadertoolsng_export('INVOKE_DEFAULT')
    else:ops_object.shadertoolsng_import('INVOKE_DEFAULT')

def UtilsSwitch(self, context):
    ops_object = eval(api_functions['ops_object'])
    if self.shadertoolsng_utils_enum == 'buttons_config':ops_object.shadertoolsng_configuration_search('INVOKE_DEFAULT')
    elif self.shadertoolsng_utils_enum == 'buttons_log':ops_object.shadertoolsng_errors('INVOKE_DEFAULT')
    elif self.shadertoolsng_utils_enum == 'buttons_help':ops_object.shadertoolsng_help('INVOKE_DEFAULT')
    elif self.shadertoolsng_utils_enum == 'buttons_create':ops_object.shadertoolsng_new('INVOKE_DEFAULT')
    elif self.shadertoolsng_utils_enum == 'menu_utils_migrate':ops_object.shadertoolsng_utils_migrate('INVOKE_DEFAULT')
    else:ops_object.shadertoolsng_credits('INVOKE_DEFAULT')

def SwitchButtonsList(list):
    temp = []
    for p in list: temp.append(tuple((p, active_languages[p], "")))
    return temp

class ShadersToolsNGPanel(eval(api_functions['types_panel'])):
    bl_label = active_languages['panel_name']
    bl_idname = "OBJECT_PT_shaderstoolsng"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    ctx_props = eval(api_functions['props'])
    types_scene = eval(api_functions['types_scene'])

    #Open and save buttons in panel
    OpenSaveItems = SwitchButtonsList(("buttons_open", "buttons_save"))
    OpenSave = ctx_props.EnumProperty( name = "OpenSave", items = OpenSaveItems, update=OpenSaveSwitch)
    types_scene.shadertoolsng_open_save = OpenSave
    #Export and import buttons in panel
    ExportImportItems = SwitchButtonsList(("buttons_export", "buttons_import"))
    ExportImport = ctx_props.EnumProperty( name = "ExportImport", items = ExportImportItems, update=ExportImportSwitch)
    types_scene.shadertoolsng_export_import = ExportImport
    #Utils button in panel
    UtilsItems = SwitchButtonsList(("buttons_config", "buttons_create", "buttons_log", "buttons_help", "buttons_credits", "menu_utils_migrate",))
    UtilsEnum = ctx_props.EnumProperty( name = "", items = UtilsItems, update=UtilsSwitch)
    UtilsProgressBar = ctx_props.IntProperty( name = "",  subtype='PERCENTAGE',  options={'ANIMATABLE'},  min=0,  max=100,  default=0,  update=UpdateProgressBar)
    types_scene.shadertoolsng_utils_bar = UtilsProgressBar
    types_scene.shadertoolsng_utils_enum = UtilsEnum

    def draw(self, context):
        ctx_scene = eval(api_functions['context_scene'])
        layout = self.layout
        row = layout.row()
    
        workbase_path = os.path.join(default_paths['temp'],  'workbase.blend')
        workbase_path_exists =  os.path.exists(workbase_path)
        if workbase_path_exists and  bpy.data.filepath == workbase_path:  
            #new.NewPreviewRenderTypeHandler(eval(api_functions['preview_render_type']), api_functions, active_languages)
            row.template_preview(context.material,  show_buttons=False)
            row = layout.row()
            row.prop(context.scene, "layers",  text="")
            row = layout.row()
    
        if update: row.operator("object.shadertoolsng_warning", text=active_languages['menu_error_error001'], icon="RADIO")
        else:
            row.label("%s : " % active_languages['panel_database_label'], icon="SCENE_DATA")
            row.prop(ctx_scene, "shadertoolsng_open_save", expand=True)
            row = layout.row()
            row.label("%s : " % active_languages['panel_archive_label'], icon="NEW")
            row.prop(ctx_scene, "shadertoolsng_export_import", expand=True)
            row = layout.row()
            row.label("%s : " % active_languages['panel_utils_label'], icon="PREFERENCES")
            row.prop(ctx_scene, "shadertoolsng_utils_enum")
            row = layout.row()
            row.prop(ctx_scene, "shadertoolsng_utils_bar")
            
MyReg = \
    (
     ShadersToolsNGPanel, Open, Save, Export, Import,New, Configuration, Help, Credits, UpdateWarning,
     ConfigurationSearch, Errors, UtilsMigrate, BeforeOpen, RestoreFilters, Informations, BeforeInformations,
     InformationsWeblink,
    )

def register():
    try:
        for c in MyReg :
            bpy.utils.register_class(c)
        #end 
        print(misc.ConsoleError("Panel ", 0, True))
        print("*"*78)
        misc.LogError("*"*78, False)
    except:
        print(misc.ConsoleError("Panel ", 0, False))
#end register
def unregister():
    for c in MyReg :
        bpy.utils.unregister_class(c)
    #end for
#end unregister
if __name__ == "__main__":
    register()
    
    
