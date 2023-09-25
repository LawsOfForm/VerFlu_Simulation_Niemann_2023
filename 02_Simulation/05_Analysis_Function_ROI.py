#Issue: Create tsv document for all needed E-field analysis 
#Author: Filip Niemann & Steffen Riemann
#Date: 21.09.2023

import os
import pathmanager
import pandas as pd
from simnibs import sim_struct, run_simnibs, mni2subject_coords
import sys
import traceback

sys.path.append(r'./SimNIBS_enhanced')
import Readout_E_fields_roi_and_mask as SE

from importlib import reload
reload(SE)

from numpy import asarray
import numpy as np
import simnibs
import csv
import fnmatch
from scipy.stats import pearsonr



#Simnibs seperates it"s mesh values in nodes of the tetraedic structure which gets optimise to get mesh and element structure, which is at the baricenter of 3 nodes.
#The normal TDCS_1_scalar.msh has the possibility to get rois for the elements at grey matter by gropping all mesh structures labels as 2
#These element files only contain normE fields but no normal component of the field, therefor a surface with orientation is needed
#The fsaverage space however is such a surface made of nodes and only grey matter, only head_mesh.crop_mesh(1002) is working, but also not needed
#The fsaverage space contains all fields in the superficial grey matter (insula etc, but noch amygdala etc.)

#Get subject coordinates
#subject coordinates are use to caculate simulations. In the overlay foder the fields are saved in MNI space
#so USE MNI COORDINATES for readouts of fsaverage mesh files _TDCS_1_scalar_fsaverage.msh"


#readout_in=['sub_space','fsaverage_mni_space'] #chooses the overlay meshfile in the subject or fsaverage overlay folder, 
# E fields will be read out in this space

#mask error in subject space because different sizes of rois

if pathmanager.Exp=='VerFlu_HI' or pathmanager.Exp == 'VerFlu_TI' or pathmanager.Exp == 'VerFlu_Phon':
    for Session in ['Kopf','Zahl']:
        sheet= pathmanager.Exp +'_' + Session
        for region in ['IFG','M1']:
            for roi_type in ['mask','sphere']: # Use IFG or M1 mask and spheres read out 
                for field_name in ['E_normal','E_norm']:  # choose normal component E-field and magnitude E-field (norm E)
                    for subject_space in ['mni2sub','sub']: # planned coordinates in mni space, actual in sub space
                        if roi_type== 'mask': #mask error in subject space because different sizes of rois
                            r=[]
                            readout_in = 'fsaverage_mni_space'                     
                            SE.Read_out_Efields(pathmanager.Exp, Session,region,field_name,subject_space,readout_in,roi_type,r)
                        else: 

                            readout_in in 'fsaverage_mni_space'          
                            for radius in [12.5,25,37.5]: #radius in mm for 3 different radii
                                r=radius
                                try:
                                    SE.Read_out_Efields(pathmanager.Exp, Session,region,field_name,subject_space,readout_in,roi_type,r)
                                except Exception:
                                    traceback.print_exc()    

elif pathmanager.Exp=='VerFlu_HM' or pathmanager.Exp == 'VerFlu_TM':
    for Session in ['Kopf','Zahl']:
        sheet= pathmanager.Exp +'_' + Session
        for region in ['M1','IFG']:
            for roi_type in ['mask','sphere']:
                for field_name in ['E_normal','E_norm']:
                    for subject_space in ['mni2sub','sub']:
                        if roi_type== 'mask': #mask error in subject space because different sizes of rois
                            r=[]
                            readout_in = 'fsaverage_mni_space' # E fields will be read out in this space
                            SE.Read_out_Efields(pathmanager.Exp, Session,region,field_name,subject_space,readout_in,roi_type,r)
                        else: 
                            #for readout_in in ['sub-space','fsaverage_mni_space']:
                            readout_in in 'fsaverage_mni_space' # E fields will be read out in this space         
                            for radius in [12.5,25,37.5]: #radii in mm   
                                r=radius
                                try:
                                    SE.Read_out_Efields(pathmanager.Exp, Session,region,field_name,subject_space,readout_in,roi_type,r)
                                except Exception:
                                    traceback.print_exc()


#to show how M1 montage effects IFG area uncomment and analyse this part
"""
if pathmanager.Exp=='VerFlu_HM' or pathmanager.Exp == 'VerFlu_TM':
    region='IFG'
    for Session in ['Kopf','Zahl']:
        sheet= pathmanager.Exp +'_' + Session
        for roi_type in ['mask','sphere']:
            for field_name in ['E_normal','E_norm']:
                for subject_space in ['mni2sub','sub']:
                    if roi_type== 'mask': #mask error in subject space because different sizes of rois
                        readout_in = 'fsaverage_mni_space'
                        r=[]
                        RE.Read_out_Efields(Experiment, Session,region,field_name,subject_space,readout_in,roi_type,r)
                    else: 
                        #for readout_in in ['sub-space','fsaverage_mni_space']:
                        readout_in in 'fsaverage_mni_space'          
                        for radius in [12.5,25,32.5]: #radius in mm
                            r=radius
                            try:
                                RE.Read_out_Efields(Experiment, Session,region,field_name,subject_space,readout_in,roi_type,r)
                            except Exception:
                                traceback.print_exc()

if pathmanager.Exp=='VerFlu_HI' or pathmanager.Exp == 'VerFlu_TI':
    region='M1'
    for Session in ['Kopf','Zahl']:
        sheet= pathmanager.Exp +'_' + Session
        for roi_type in ['mask','sphere']:
            for field_name in ['E_normal','E_norm']:
                for subject_space in ['mni2sub','sub']:
                    if roi_type== 'mask': #mask error in subject space because different sizes of rois
                        readout_in = 'fsaverage_mni_space'
                        r=[]
                        RE.Read_out_Efields(Experiment, Session,region,field_name,subject_space,readout_in,roi_type,r)
                    else: 
                        #for readout_in in ['sub-space','fsaverage_mni_space']:
                        readout_in in 'fsaverage_mni_space'          
                        for radius in [12.5,25,32.5]: #radius in mm
                            r=radius
                            try:
                                RE.Read_out_Efields(Experiment, Session,region,field_name,subject_space,readout_in,roi_type,r)
                            except Exception:
                                traceback.print_exc()
"""
