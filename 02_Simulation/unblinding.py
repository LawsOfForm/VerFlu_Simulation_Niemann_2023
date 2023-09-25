#global Exp


#Exp=['VerFlu_HI', 'VerFlu_HM', 'VerFlu_TI', 'VerFlu_TM','VerFlu_Phon']
def unblinding(Exp):
	dict_unbl={}
	if Exp=='VerFlu_HI':
		dict_unbl['Stim'] = 'Kopf' 
		dict_unbl['Sham'] = 'Zahl'
		dict_unbl['Kopf'] = 'Stim'
		dict_unbl['Zahl'] = 'Sham'
		dict_unbl['K'] = 'Stim'
		dict_unbl['Z'] = 'Sham'

	elif Exp=='VerFlu_HM': 
		dict_unbl['Stim'] = 'Zahl' 
		dict_unbl['Sham'] = 'Kopf'
		dict_unbl['Zahl'] = 'Stim'
		dict_unbl['Kopf'] = 'Sham'
		dict_unbl['K'] = 'Sham'
		dict_unbl['Z'] = 'Stim'

	elif Exp=='VerFlu_TM': 
		dict_unbl['Stim'] = 'Kopf' 
		dict_unbl['Sham'] = 'Zahl'
		dict_unbl['Kopf'] = 'Stim'
		dict_unbl['Zahl'] = 'Sham'
		dict_unbl['K'] = 'Stim'
		dict_unbl['Z'] = 'Sham'
	elif Exp=='VerFlu_TI': 
		dict_unbl['Stim'] = 'Zahl' 
		dict_unbl['Sham'] = 'Kopf'
		dict_unbl['Kopf'] = 'Sham'
		dict_unbl['Zahl'] = 'Stim'
		dict_unbl['K'] = 'Sham'
		dict_unbl['Z'] = 'Stim'
	elif Exp=='VerFlu_Phon': 
		#Not correct order, juste dummy filled in 15.03.2023
		dict_unbl['Stim'] = 'Zahl' 
		dict_unbl['Sham'] = 'Kopf'
		dict_unbl['Kopf'] = 'Sham'
		dict_unbl['Zahl'] = 'Stim'
		dict_unbl['K'] = 'Sham'
		dict_unbl['Z'] = 'Stim'
		

	return dict_unbl



