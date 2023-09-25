#Issue: Get mean E-field images and images for Figure 3 and Figure S5 for actual electrodes
#Author: Filip Niemann & Steffen Riemann
#Date: 21.09.2023

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

from Outlier_list_function import Outlier_function

"""
Install pandas in simnibs_python before running. "simnibs_python -m pip install pandas==1.2.0"
"simnibs python -m pip install openpyxl"
"""

#ROI vs mask
#mask has add.element feature. an element ist the vektor of 3 rectangular vectors combined in 1
#roi has *.nodedata or add_node_field. Nodes are the Nodes of the rectangular and not the combined vector
#so if you switch code between ROIS and MASKS beware of the difference if the vector is given als element or node 
 
#only mesh data in subject_overlays folder have E_normal component field "subject_overlays", f'{sub}_TDCS_1_scalar_central.msh 
#test by field['E_normal']
#field_name = 'E_normal' #simnibs 3.2
#field_name = 'normE'

field_name = input("Which field E_norm (magnidute E) or E_normal (normale component of E-field) ->")



 # we will use a sphere of radius 10 mm
r=12.5 # 50 mm=5cm 25 mm like # all raddi 12.5 radii 25 mm 32.5
fields = []
outlier=[]
#for sub in stim_data_cor.index[0:6]:

region=input("Welche Region, IFG oder M1? Eingabe ->")

if region=="IFG":
    coords=[-56,24,12]   #outer area of ifg to match th 1.25 radius of the HD-tDCS electrode, only aesthetic reasons no analysis
    
elif region=="M1":

    coords=[-52,-16,58] #C3



for Session in ['Kopf','Zahl']:
    sheet= pathmanager.Exp +'_' + Session

    stim_data_cor = pd.read_excel("./Source_Data/Electrode_Coordinates_full_coregistr.xlsx", sheet_name=sheet, engine="openpyxl")
    
        
        
    #    coords=[3,-54,29] #sub_01 HI Zahl

    [outlier_List,outlier_List_sub,outlier_List_sub_sex_id,outlier_list_only_measured_subjecst,outlier_list_only_measured_subjecst_SimNIBS,outlier]=Outlier_function(pathmanager.Exp)

    outlier_list=outlier_list_only_measured_subjecst_SimNIBS

    stim_data_cor=(stim_data_cor
                .set_index('id')
                .drop(outlier_list)
                )

    for sub in stim_data_cor.index:
    #only use subjects with 
        if not os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, sub, f"ses-{Session}", "SimNIBS", "simulations_cor","fsavg_overlays", f'{sub}_TDCS_1_scalar_fsavg.msh')):
            #get outlier
            print(f'{sub} mesh is not available')
            outlier.append(sub)
        else:
            #read mesh
            #two kinds of msh exist 
            # 1) volumen meshes like sub-01_TDCS_1_scalar.msh. There you can use crop_mesh(2) to get grey matter
            # 2) overlay meshes like sub-01_TDCS_1_scalar_central.msh or sub-01_TDCS_1_scalar_fsaverage.msh. typical in overlay folders use crop_mesh(1002)

            # read mesh with results transformed to fsaverage space

            #head mesh is already croped with value of 1002

            results_fsavg = simnibs.read_msh(os.path.join(pathmanager.BASEDIRECTORY, sub, f"ses-{Session}", "SimNIBS", "simulations_cor","fsavg_overlays", f"{sub}_TDCS_1_scalar_fsavg.msh"))


            #coords_sub = simnibs.mni2subject_coords(coords, os.path.join(pathmanager.BASEDIRECTORY, sub, f"ses-{Session}", "SimNIBS",f'm2m_{sub}'))
            #fsavereage space is nearly mni space
            #coords_sub = simnibs.mni2subject_coords(coords, os.path.join(pathmanager.BASEDIRECTORY, sub, f"ses-{Session}", "SimNIBS",f'm2m_{sub}'))
            
            coords_sub=coords

            roi = np.linalg.norm(results_fsavg.nodes.node_coord - coords_sub, axis=1) < r


            field = results_fsavg.field[field_name][:]

            fields.append(results_fsavg.field[field_name][:])



print('combined',len(fields))

        
print('outlier=',outlier)


# Calculate field mean for 
fields = np.vstack(fields) #concatenates vectors


avg_field = np.mean(fields, axis=0)
std_field = np.std(fields, axis=0)



#results_fsavg.view(visible_fields='E_normal_avg').show()

## this part is only for later tables an values, not neccesary for ploting
if field_name == 'E_normal':
# Plot

    results_fsavg.nodedata = [] # cleanup fields
    results_fsavg.add_node_field(avg_field, 'E_normal_avg') # add average field to simnibs.msh class
    results_fsavg.add_node_field(std_field, 'E_normal_std') # add std field

    node_areas = results_fsavg.nodes_areas()

    results_fsavg.add_node_field(roi, region)
    
    results_fsavg.view(visible_fields='roi').show()
    #results_fsavg.view().show()

        # Calculate the mean
    mean_magnNormE = np.average(field[roi], weights=node_areas[roi])  # because areas are different for each node, weighted areas correct for them
    std_magnNormE = np.std(field[roi])
    mean_magnNormE_All = np.average(field, weights=node_areas[:])  # ist the weight correct?
    std_magnNormE_All = np.std(field)

    print('mean ROI ', field_name, f' in {region} ROI: ', mean_magnNormE)
    print('std ROI', field_name, f' in {region} ROI: ', std_magnNormE)
    print('mean All ', field_name, f' whole brain: ', mean_magnNormE_All)
    print('std All', field_name, f' whole brain: ', std_magnNormE_All)


    avg_field_rois = []
    neg_avg_field_rois = []
    std_field_rois = []
    neg_std_field_rois = []


    weight = node_areas
    #print(roi,weight[0:2:100])
    #print(weight[0:2:100]==0)
    avg_f = avg_field
    std_f= std_field

    pos_weight = weight[avg_f > 0]
    pos_avg_f = avg_f[avg_f > 0]
    pos_std_f= std_f[avg_f > 0]

    neg_weight = weight[avg_f < 0]
    neg_avg_f = avg_f[avg_f < 0]
    neg_std_f= std_f[avg_f < 0]

    #[avg_field_rois.append(np.average(pos_avg_f, weights=pos_weight)) if np.average(pos_avg_f, weights=pos_weight) is not 0 else print('positive average field does not exist')]
    avg_field_rois.append(np.average(pos_avg_f, weights=pos_weight))
    std_field_rois.append(np.average(pos_std_f, weights=pos_weight))
    print("mean:", avg_field_rois)
    print("std:", std_field_rois)
    
    neg_avg_field_rois.append(np.average(neg_avg_f, weights=neg_weight))
    neg_std_field_rois.append(np.average(neg_std_f, weights=neg_weight))

    # Plot if elementdata not nodedata
    #results_fsavg.elementdata = [] # cleanup fields
    #results_fsavg.add_elemnt_field(avg_field, 'E_normal_avg') # add average field
    #results_fsavg.add_element_field(std_field, 'E_normal_std') # add std field

    df=pd.DataFrame([avg_field_rois,neg_avg_field_rois,std_field_rois,neg_std_field_rois],columns=[region],index=['pos norm meanE','neg norm meanE','pos norm stdE','neg norm stdE'])
    #df.to_excel( f'/Exp_norm_meanE/{pathmanager.Exp}/norm_meanE.xlsx')
    df=df.T

    #with pd.ExcelWriter('/media/Data01/Studien/VerFlu/code/SimNIBS/Exp_norm_meanE/normal_meanE_roi.xlsx', mode='a',if_sheet_exists='overlay') as writer:  
    #   df.to_excel(writer, sheet_name=f'{pathmanager.Exp}_{Session}')

    ## Plot the ROI
    #results_fsavg.add_element_field(roi, 'roi')
    results_fsavg.add_node_field(roi, region)
    #results_fsavg.view(visible_fields='roi').show()

    # Calculate the mean

    #print('mean ROI ', field_name, f' in {region} ROI: ', mean_magnE)
    #print('std ROI', field_name, f' in {region} ROI: ', std_magnE)

elif field_name == 'E_norm':
    print("wrong")

# Plot

    results_fsavg.nodedata = [] # cleanup fields
    results_fsavg.add_node_field(avg_field, 'mean magnitude E ') # add average field to simnibs.msh class
    results_fsavg.add_node_field(std_field, 'std magnitude E') # add std field
    node_areas = results_fsavg.nodes_areas()

    results_fsavg.add_node_field(roi, region)
    
    results_fsavg.view(visible_fields='roi').show()

        # Calculate the mean
    mean_magnE = np.average(field[roi], weights=node_areas[roi])  # because areas are different for each node, weighted areas correct for them
    std_magnE = np.std(field[roi])
    
    mean_magnE_All = np.average(pos_avg_f, weights=pos_weigh)  # ist the weight correct?
       
    std_magnE_All = np.std(pos_std_f,weights=pos_weigh)
    
    #mean_magnE_All = np.average(field, weights=node_areas[:])  # ist the weight correct?
    #std_magnE_All = np.std(field)

    print('mean ROI ', field_name, f' in {region} ROI: ', mean_magnE)
    print('std ROI', field_name, f' in {region} ROI: ', std_magnE)
    print('mean All ', field_name, f' in {region} ROI: ', mean_magnE_All)
    print('std All', field_name, f' in {region} ROI: ', std_magnE_All)





