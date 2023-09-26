# Title: Oulier list function
# Author: Filip Niemann
# Date: 22.12.2023

#List is needed for outlier, because some experiment failed participant canceld, data were missing etc.
# Therefore the table /03_Analysis_Electrode_Difference/Source_Data/Treatment_Subjects.xlsx is modified to get 30 balanced MRI data at the end
# in this data set all failed experiments are deleted


def Outlier_function(Exp):
	if Exp=='VerFlu_TI':
			
		outlier_List=[]
		
		outlier=[]

		outlier_List_sub=[]
		outlier_List_sub_sex_id=[]
		outlier_list_only_measured_subjecst=[]
		outlier_list_only_measured_subjecst_SimNIBS=[]  
		
	elif Exp=='VerFlu_HI':



		outlier_List=[] 	
		outlier_List_sub=[] 
			
		outlier_List_sub_sex_id=[] 

		outlier_list_only_measured_subjecst=[]
		outlier_list_only_measured_subjecst_SimNIBS=[] 
		outlier=[]  #	
		
		
		
	elif Exp=='VerFlu_HM':

		
		outlier_List=[]
		outlier_List_sub=[]
		outlier_List_sub_sex_id=[]
		outlier_list_only_measured_subjecst=[]
		outlier_list_only_measured_subjecst_SimNIBS=[]
		outlier=[]
		
	elif Exp=='VerFlu_TM':

		outlier_List=[] 
		outlier_List_sub=[]
		outlier_List_sub_sex_id=[]
		outlier_list_only_measured_subjecst=[]
		outlier_list_only_measured_subjecst_SimNIBS=[]		
		
	elif Exp=='VerFlu_Phon':

		outlier_List=[]
		outlier_List_sub=[]
		outlier_List_sub_sex_id=[]
		outlier_list_only_measured_subjecst=[] 
		outlier_list_only_measured_subjecst_SimNIBS=[]
		outlier=[2,5,13]
	return(outlier_List,outlier_List_sub,outlier_List_sub_sex_id,outlier_list_only_measured_subjecst,outlier_list_only_measured_subjecst_SimNIBS,outlier)
