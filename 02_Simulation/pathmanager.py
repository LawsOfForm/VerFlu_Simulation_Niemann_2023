#Author: Filip Niemann
#Date: 21.09.2023

# simulations will be done for 4 Verbal Fluency (VerFlu) Experiments differ in Montage(HD-tDCS, conventional tDCS) and Area (IFG, M1), namely
# 1. VerFlu_HI : Verbal Fluency HD-tDCS IFG
# 2. VerFlu_HM : Verbal Fluency HD-tDCS M1
# 3. VerFlu_TI : Verbal Fluency conventional-tDCS IFG
# 4. VerFlu_TM : Verbal Fluency conventional-tDCS IFG

Exp=input('Choose Experiment: VerFlu_HI, VerFlu_HM, VerFlu_TI, VerFlu_TM: Eingabe ->')

# Change BASEDIRECTOR to the given Experimental folder
# BASEDIRECTORY = f"YOUR_FOLDER_PATH/{Exp}/derivatives/spm-preproc"

BASEDIRECTORY = f"YOUR_FOLDER_PATH/{Exp}/ADDITIONAL_FOLDERS"

#Change codedirectory

CODEDIRECTORY=''

# Kopf and Zahl can also be coded as Stimulation or Sham, in our case analysis was done blinded so folder structure was named as blinding code.
KOPF = "ses-Kopf/SimNIBS/"
ZAHL = "ses-Zahl/SimNIBS/"

