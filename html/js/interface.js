function PAGE_HEADER_HELPME(){
	document.writeln('<div id="header">');		
	document.writeln('<img src="html/img/All/logo.png" id="header_img">');		
	document.writeln('</div>');		
}

function PAGE_HEADER(){
	document.writeln('<div id="header">');		
	document.writeln('<img src="../img/All/logo.png" id="header_img">');		
	document.writeln('</div>');		
}

function PAGE_BOTTOM_EN(){
	document.writeln('<div id="bottom_header">');
	document.writeln('Created by GRETETE Karim (alias Tinangel)<br>');
	document.writeln('<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">');
	document.writeln('<img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-sa/3.0/80x15.png" />');
	document.writeln('</a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">');
	document.writeln('Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License</a>.');
	document.writeln('</div>');
}			
				
function PAGE_BOTTOM_FR(){
	document.writeln('<div id="bottom_header">');
	document.writeln('Créé par GRETETE Karim (alias Tinangel)<br>');
	document.writeln('<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/deed.fr">');
	document.writeln('<img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-sa/3.0/80x15.png" />');
	document.writeln('</a><br />Ce produit est soumis à la licence : <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/deed.fr">');
	document.writeln('Creative Commons Attribution - Pas d\'Utilisation Commerciale - Partage dans les Mêmes Conditions 3.0 non transposé (CC BY-NC-SA 3.0)</a>.');
	document.writeln('</div>');
}			
		
function GLOBAL_MAIN_FR(){
	document.writeln('<div id="main">');
	document.writeln('<!-- Ici je créé la liste du menu -->');
	document.writeln('<ul>');
	document.writeln('<A HREF="index.html"><li> - Accueil </li></A>');
	document.writeln('<A HREF="before.html"><li> - Prérequis </li></A>');
	document.writeln('<A HREF="installation.html"><li> - Installation </li></A>');
	document.writeln('<A HREF="gui.html"><li> - L\'interface	</li></A>');
	document.writeln('<A HREF="alias.html"><li> - Les raccourcis </li></A>');
	document.writeln('<A HREF="open.html"><li> - Le module Ouvrir </li></A>');
	document.writeln('<A HREF="search.html"><li> - Le module Rechercher </li></A>');
	document.writeln('<A HREF="history.html"><li> - Le module Historique </li></A>');
	document.writeln('<A HREF="informations.html"><li> - Le module Informations </li></A>');
	document.writeln('<A HREF="save.html"><li> - Le module Sauvegarder </li></A>');
	document.writeln('<A HREF="export.html"><li> - Le module Exporter </li></A>');
	document.writeln('<A HREF="import.html"><li> - Le module Importer </li></A>');
	document.writeln('<A HREF="utilities.html"><li> - Le module Utilitaires </li></A>');
	document.writeln('<A HREF="configuration.html"><li> - Le module Configuration </li></A>');
	document.writeln('<A HREF="io_database.html"><li> - Exporter ou Importer la base materiau </li></A>');
	document.writeln('<A HREF="open_folder.html"><li> - Ouvrir le dossier de l\'add-on	</li></A>');
	document.writeln('<A HREF="cleanup.html"><li> - Outils de nettoyage	</li></A>');
	document.writeln('<A HREF="new.html"><li> - Le module Créer un nouvelle matière	</li></A>');
	document.writeln('<A HREF="migrate.html"><li> - Le module Migrer une base de données (V1 -> V2) </li></A>');
	document.writeln('<A HREF="autosave.html"><li> - L\'Auto-sauvegarde </li></A>');
	document.writeln('<A HREF="credits_help_logs.html"><li> - Les modules Logs, Aide et Crédits </li></A>');
	document.writeln('</ul>');
	document.writeln('</div>');
}						


function GLOBAL_MAIN_EN(){
	document.writeln('<div id="main">');
	document.writeln('<!-- Ici je créé la liste du menu -->');
	document.writeln('<ul>');
	document.writeln('<A HREF="index.html"><li> - Home </li></A>');
	document.writeln('<A HREF="before.html"><li> - Before you start </li></A>');
	document.writeln('<A HREF="installation.html"><li> - Installation </li></A>');
	document.writeln('<A HREF="gui.html"><li> - User interface	</li></A>');
	document.writeln('<A HREF="alias.html"><li> - Shortcuts </li></A>');
	document.writeln('<A HREF="open.html"><li> - Open </li></A>');
	document.writeln('<A HREF="search.html"><li> - Search </li></A>');
	document.writeln('<A HREF="history.html"><li> - History </li></A>');
	document.writeln('<A HREF="informations.html"><li> - Informations </li></A>');
	document.writeln('<A HREF="save.html"><li> - Save </li></A>');
	document.writeln('<A HREF="export.html"><li> - Export </li></A>');
	document.writeln('<A HREF="import.html"><li> - Import </li></A>');
	document.writeln('<A HREF="utilities.html"><li> - Utilities </li></A>');
	document.writeln('<A HREF="configuration.html"><li> - Settings	</li></A>');
	document.writeln('<A HREF="io_database.html"><li> - Export or Import materials database </li></A>');
	document.writeln('<A HREF="open_folder.html"><li> - Open the path of the add-on 	</li></A>');
	document.writeln('<A HREF="cleanup.html"><li> - Cleaning tools utility	</li></A>');
	document.writeln('<A HREF="new.html"><li> - Create a new material utility	</li></A>');
	document.writeln('<A HREF="migrate.html"><li> - Migrate database (V1 -> V2) utility </li></A>');
	document.writeln('<A HREF="autosave.html"><li> - Auto-backup </li></A>');
	document.writeln('<A HREF="credits_help_logs.html"><li> - Logs, Credits and Help utilities </li></A>');
	document.writeln('</ul>');
	document.writeln('</div>');
}						