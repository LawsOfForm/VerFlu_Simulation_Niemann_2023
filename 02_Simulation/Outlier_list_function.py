#global Exp
#FN 22.12.2023
#import easygui
#Exp=input('Wähle dein Lieblingsexperiment oder Lieblingspokemon: VerFlu_HI, VerFlu_HM, VerFlu_TI, VerFlu_TM,VerFlu_Phon: Eingabe ->')
#Exp=easygui.buttonbox('Choose your Experiment', 'Experiment', ('VerFlu_HI', 'VerFlu_TI', 'VerFlu_HM','VerFlu_TM','VerFlu_Phon'))
def Outlier_function(Exp):
	if Exp=='VerFlu_TI':
		#sub-01 outlier simnibs kopf...haedreco mit cat12 gibt Fehler aus :  Warning:cat_io_report:CATgui: Incomplete report creation in cat_io_report because of incomplete CAT parameters.
		# Zahl allerdings funktioniert, daher könnte man die Elektroden
		#sub06 schlechte mrt daten aber weiblich  
		#sub-09 zu gute behavioral performance und zu schlechte mrt daten weiblich
		#sub 11 und 12 recht lateralisiert aktivität
		#16 left handed männlich
		#19 schlechte mr qualitäte männchen
		#22 left handed weiblich
		#26 schlechte mr qualitäte weiblich 
		#39 schlechte mr qualitäte weiblich 
		# sub 14 extreme value in coordinates space
		#Outlier for Coordinates
		#33 Elektrode verutscht Zahl 
		#44 schelchte mr qualität weiblich   elektrode verrutscht in Kopf
		
		
		outlier_List=['14','16','23','26','32','34','35','37','38','40','41','42','43','44']
		
		outlier=[14,16,23,26,32,34,35,37,38,40,41,42,43,44]
		#TI subjects go to list sub-44, this list contains subjects which are excluded and which are not measured 
		#exampele sub-06 is measures but excluded, sub-43 ist not measured but some lists generate list from max value, in this case 44
		outlier_List_sub=['sub-14','sub-16','sub-23','sub-26','sub-32','sub-34','sub-35','sub-37','sub-38','sub-40','sub-41','sub-42','sub-43','sub-44']
		outlier_List_sub_sex_id=['sub-14','sub-16','sub-23','sub-26','sub-34','sub-44']
		outlier_list_only_measured_subjecst=['sub-14','sub-16','sub-23','sub-26','sub-34','sub-44']
		outlier_list_only_measured_subjecst_SimNIBS=['sub-14','sub-33','sub-34','sub-44']  # sub 34, sub 44 not in simnibs simulations
		#outlier_list_only_measured_subjecst_SimNIBS=['sub-14','sub-33','sub-44','sub-19'] # to match age
		
	elif Exp=='VerFlu_HI':

		
		#left hande  3, 19, 20,24,25
		#11 ADHS 
		#10 Draht in Maske
		#14 data nicht übertrage und von radiologie nach 2 Tagen gelöscht
		#21 Logdatei überschrieben
		#35 ???
		#36 coordinates bad
		#39 zu Oft in Pause gesprochen und zu viele Fehler gemacht
		#42 zu gut, performed, fast 100%
		
		#47 eventuell outlier - baumkategorie Ast, Blat etc.
		

		outlier_List=['02','03','10','11','12','14','19','20','21','24','25','27','32','33','36','39','42'] #see group effect '45','46','47'	
		outlier_List_sub=['sub-02','sub-03','sub-10','sub-11','sub-12','sub-14','sub-19','sub-20','sub-21','sub-24','sub-25','sub-27','sub-32','sub-33','sub-36','sub-39','sub-42'] #why 27?
			
		outlier_List_sub_sex_id=['sub-02','sub-03','sub-12','sub-14','sub-19','sub-20','sub-24','sub-25','sub-27','sub-32','sub-33','sub-36','sub-42'] #sub-21, sub-39 not a folder #sub 42 was to good, sub-10 leere datei in func data -speicher probleme, sub-11 mit maske gemessen , sub-21 -verlorene log daten
	

		outlier_list_only_measured_subjecst=['sub-02','sub-03','sub-12','sub-19','sub-20','sub-24','sub-25','sub-27','sub-32','sub-33','sub-36','sub-42']
		outlier_list_only_measured_subjecst_SimNIBS=['sub-02' ,'sub-03'         ,'sub-05'        ,'sub-12','sub-19','sub-20','sub-24','sub-25','sub-27','sub-32','sub-33','sub-36','sub-42'] #sub 42 sub 03 not in simnibs simulation but coordinates measured
		#outlier_list_only_measured_subjecst_SimNIBS=['sub-02','sub-03','sub-05','sub-10','sub-12','sub-19','sub-20','sub-24','sub-25','sub-27','sub-32','sub-33','sub-36'] #to match age
		outlier=[2,3,10,11,12,14,19,20,21,24,25,27,32,33,36,39,42]  #	
		
		
		#Outlier for unbalanced vs balance group test
		# group 1 is 19 times in session 1 and 12 times session2; group 2 is 12 times in session 1 and 19 times in session 2 ... bacause of session learn effect group 2 is supposed to be higher than group 1 
		#running analysis without 45,46,47,36,37 made no difference so group effect seems to be not correlated to session effect	
		"""
		outlier_List=['02','03','10','11','12','14','19','20','21','24','25','27','32','33','36','37','39','42','45','46','47']
		outlier_List_sub=['sub-02','sub-03','sub-10','sub-11','sub-12','sub-14','sub-19','sub-20','sub-21','sub-24','sub-25','sub-27','sub-32','sub-33','sub-36','sub-37','sub-39','sub-42','sub-44','sub-45','sub-46','sub-47'] 
		
		
		outlier=[2,3,10,11,12,14,19,20,21,24,25,27,32,33,36,37,39,42,45,46,47]
		
		outlier_List_sub_sex_id=['sub-02','sub-03','sub-12','sub-14','sub-19','sub-20','sub-24','sub-25','sub-27','sub-32','sub-33','sub-36','sub-37','sub-42','sub-45','sub-46','sub-47'] #sub 10,11 21,39 doesn't exist as folder, 
		"""
		
	elif Exp=='VerFlu_HM':
		#sub-05 nur einmal vermessen
		#sub-08 in Pause gesprochen, Baum [Ast, Blatt, Birke,Eich, Pappel, WUrzel]
		#schlechte Performance verhaltensdaten
		#28 Spielzeug alles weiter gesagt       tag2 dafür fast alles vollständig, treibt den Verhaltenseffekt
		
		#25 Kopf T1 electrodes merkwürdige Ringe - Bilder kontrollieren  # Ausschluss, zu viele Bewegungsartefakte
		
		
		outlier_List=['sub-05','sub-25','sub-28','sub-30','sub-32']
		outlier_List_sub=['sub-05','sub-28','sub-25','sub-30','sub-32']
		outlier_List_sub_sex_id=['sub-05','sub-28', 'sub-25']
		outlier_list_only_measured_subjecst=['sub-28', 'sub-25']
		outlier_list_only_measured_subjecst_SimNIBS=['sub-25']
		outlier=[5,25,28,30,32]
		
	elif Exp=='VerFlu_TM':
		#08 Baum: [Blatt Ast, Linde, Pappel, Eiche, Wurzel]
		#18 Gemüseart Probleme geahbt ---nur auch Schot, Hülse, Knolle gekommen zieht den Schnitt somit für Tag2 nach unten 
		#27 ses 1 func data 0bytes in one of 84 
		
		#!!!!34 Zahl Elektrode sehr weit nach hinten gerutscht  -44 -42 71     statt üblicherweise -60 -38 63 ---WENN SHAM = ZAHL DANN KANN ER VERWENDE WERDEN ,'sub-34'
		#verzerrt ANOVA daher lieber rausnehmen

		#46 starkes Rauschen durch Kabel in ses2 gesamte linke Gehirnhälfte
		#47 vieatnamesische und deutsche Mutter sprache ---reinnehmen da sub 34 rausgenommen wegen verrutschter Elektroden # für simnibs drin lassen
		
		outlier_List=['sub-18','sub-27','sub-26','sub-28','sub-29','sub-30','sub-31','sub-32','sub-33','sub-34','sub-35','sub-37','sub-39','sub-40','sub-41','sub-42','sub-44','sub-46'] #Audio Onset
		outlier_List_sub=['sub-18','sub-27','sub-46','sub-26','sub-28','sub-29','sub-30','sub-31','sub-32','sub-33','sub-34','sub-35','sub-37','sub-39','sub-40','sub-41','sub-42','sub-44']
		outlier_List_sub_sex_id=['sub-18','sub-27','sub-34','sub-46']
		outlier_list_only_measured_subjecst=['sub-18','sub-34','sub-46']
		outlier_list_only_measured_subjecst_SimNIBS=['sub-27','sub-34','sub-46','sub-19']
		outlier=[18,27,26,28,29,30,31,32,33,34,35,37,39,40,41,42,44,46] #must be equal outlier_List_sub
		
	elif Exp=='VerFlu_Phon':
		#14 or 17 IFG nicht gut getroffen
		
		outlier_List=['sub-02','sub-05','sub-13']
		outlier_List_sub=['sub-02','sub-05','sub-13']
		outlier_List_sub_sex_id=['sub-02','sub-13']
		outlier_list_only_measured_subjecst=['sub-02','sub-13'] #sub-01 treibt effect in left vIFG
		outlier_list_only_measured_subjecst_SimNIBS=['sub-02','sub-13']
		outlier=[2,5,13]
	return(outlier_List,outlier_List_sub,outlier_List_sub_sex_id,outlier_list_only_measured_subjecst,outlier_list_only_measured_subjecst_SimNIBS,outlier)
