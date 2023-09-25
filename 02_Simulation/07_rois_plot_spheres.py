import os
import pathmanager
import pandas as pd
from simnibs import sim_struct, run_simnibs, mni2subject_coords
import sys
from numpy import asarray
import numpy as np
import simnibs
import csv
import fnmatch
from scipy.stats import pearsonr

sys.path.append(r'/media/Data01/Studien/VerFlu/code/Outlier_list')
from Outlier_list_function import Outlier_function

"""
Install pandas in simnibs_python before running. "simnibs_python -m pip install pandas==1.2.0"
"simnibs python -m pip install openpyxl"
"""

#ROI vs mask
#mask has add.element feature. an element ist the vektor of 3 rectangular vectors combined in 1
#roi has *.nodedata or add_node_field. Nodes are the Nodes of the rectangular and not the combined vector
#so if you switch code between ROIS and MASKS beware of the difference if the vector is given als element or node 
 


field_name = input("Which field E_norm (magnidute E) or E_normal (normale component of E-field) ->")


#only mesh data in subject_overlays folder have E_normal component field "subject_overlays", f'{sub}_TDCS_1_scalar_central.msh 
#test by field['E_normal']

#field_name = 'E_normal' #simnibs 3.2
#field_name = 'normE'
 # we will use a sphere of radius 10 mm
#r=12.5 # 50 mm=5cm 25 mm like # all raddi 12.5 radii 25 mm 32.5
fields = []
outlier=[]
#for sub in stim_data_cor.index[0:6]:

results_fsavg = simnibs.read_msh(os.path.join(pathmanager.BASEDIRECTORY, 'sub-01', f"ses-Kopf", "SimNIBS", "simulations_cor","fsavg_overlays", f"sub-01_TDCS_1_scalar_fsavg.msh"))
results_fsavg.nodedata = []

for region in ['IFG', 'M1']:
    if region=="IFG":
        coords=[-57,24,12]   #outer area of ifg
        
        
    elif region=="M1":
        #coords=[-67.99,-13.10,61.52]   #C3 simnibs GUI  outer area of C3 for optimal readout nudged 1 mm into brain changing x axis an 1 mm y axis
        #coords=[-37.59,-13.10,61.52] #file:///home/niemannf/Downloads/jcm-09-00975-s001.pdf mean of all lefM1 MNI x coordinates
        coords=[-52.2,-16.4,57.8] #Okamoto et al 2004 htt
    for r in [12.5, 25, 32.5]:            

            #read mesh
            coords_sub=coords

            #roi = np.linalg.norm(elm_centers - coords_sub, axis=1) < r
            roi = np.linalg.norm(results_fsavg.nodes.node_coord - coords_sub, axis=1) < r
            if r ==12.5:

                roi_125 = np.linalg.norm(results_fsavg.nodes.node_coord - coords_sub, axis=1) < r
                results_fsavg.add_node_field(roi_125, region)
            elif r == 25:

                roi_25 = np.linalg.norm(results_fsavg.nodes.node_coord - coords_sub, axis=1) < r
                results_fsavg.add_node_field(roi_25, region)
            elif r ==32.5:

                roi_325 = np.linalg.norm(results_fsavg.nodes.node_coord - coords_sub, axis=1) < r
                results_fsavg.add_node_field(roi_325, region)      

            #field = results_fsavg.field[field_name][:]

            #fields.append(results_fsavg.field[field_name][:])

                #print('single', len(fields))
#results_fsavg.nodedata = []
results_fsavg.view(visible_fields='roi_125').show()
#results_fsavg.view(visible_fields='roi_25').show()
#results_fsavg.view(visible_fields='roi_325').show()

