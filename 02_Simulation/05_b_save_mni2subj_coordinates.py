#Issue: Transform mni coordinates into subject coordinates and creates excel file 
#Author: Filip Niemann & Steffen Riemann
#Date: 21.09.2023

"""
Install pandas in simnibs_python before running. "simnibs_python -m pip install pandas==1.2.0"
"simnibs python -m pip install openpyxl"

https://simnibs.github.io/simnibs/build/html/documentation/command_line/mni2subject_coords.html#mni2subject-coords-docs

When transforming electrode positions, the results are always projected to the skin after the transformation.
"""
# Beware that mni2sub coordinates with given coordinates from mni space for HD-tDCS or focal tDCS wrongly estimate fields 
# because radius of cathodes



import os
import pathmanager
import pandas as pd
from simnibs import sim_struct, run_simnibs, mni2subject_coords

from numpy import asarray
import numpy as np
import simnibs
import csv
import fnmatch
from scipy.stats import pearsonr


Session=input("Which Session? Kopf or Zahl? input ->")
sheet= pathmanager.Exp +'_' + Session

# Read in all subjects 
stim_data_cor = pd.read_excel("./Source_Data/Electrode_Coordinates_full_coregistr.xlsx", sheet_name=sheet, engine="openpyxl")
stim_data_cor = stim_data_cor.set_index("id")


dict={}
for vp in stim_data_cor.index:
    if stim_data_cor["site"].loc[vp] == "IFG":
        if stim_data_cor["tDCS"].loc[vp] == "HD":
            mni_coords=[[-69, 35, 17],[-72,  32 ,  -28],[-75,  -1,  41],[-40, 66, 33 ]]   #3x1 setup  #HD
            columns=['anode_x','anode_y','anode_z','cathode_1_x','cathode_1_y','cathode_1_z','cathode_2_x','cathode_2_y','cathode_2_z','cathode_3_x','cathode_3_y','cathode_3_z']


        elif stim_data_cor["tDCS"].loc[vp] == "konv":
            mni_coords=[[-69, 35, 17],[36.47,75.46,21.04],[-80.1, -5.69, 21.16],[31,54,56]]      #1x1 setup Anode IFG, Cathode AF4 sponge
            columns=['anode_x','anode_y','anode_z','cathode_1_x','cathode_1_y','cathode_1_z','anode_orientation_x','anode_orientation_y','anode_orientation_z','cathode_orientation_x','cathode_orientation_y','cathode_orientation_z']  

            
    
    elif stim_data_cor["site"].loc[vp] == "M1":
        if stim_data_cor["tDCS"].loc[vp] == "HD":
            mni_coords=[[-67.99, -13.10, 61.52],[-32.44, -11.21,  89.93],[-71.1, 19.58, 32.68],[-74.89, -54.38, 45.60]] #HD
            columns=['anode_x','anode_y','anode_z','cathode_1_x','cathode_1_y','cathode_1_z','cathode_2_x','cathode_2_y','cathode_2_z','cathode_3_x','cathode_3_y','cathode_3_z']
        
        elif stim_data_cor["tDCS"].loc[vp] == "konv":         
            mni_coords=[[-67.99, -13.10, 61.52],[36.47,75.46,21.04],[-58.92,21.42,54.49],[31,54,56]] #'C3'   #sponge
            columns=['anode_x','anode_y','anode_z','cathode_1_x','cathode_1_y','cathode_1_z','anode_orientation_x','anode_orientation_y','anode_orientation_z','cathode_orientation_x','cathode_orientation_y','cathode_orientation_z']  

    
    if pathmanager.Exp == 'VerFlu_HI' or pathmanager.Exp == 'VerFlu_HM':
         if os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", "simulations_mni_indiv_radius", f"{vp}_TDCS_1_scalar.msh")): 
                
            head_mesh = simnibs.read_msh(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", "simulations_mni_indiv_radius", f"{vp}_TDCS_1_scalar.msh"))    
            gray_matter = head_mesh.crop_mesh(2) # only grey matter
            
            # arg1: MNI coords, arg2: m2m path
            
            
            #transform mni coordinates to subjects coordinates
            sub_coords_mni = simnibs.mni2subject_coords(mni_coords,os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS",f"m2m_{vp}"))
            sub_coords_mni = [element for sublist in sub_coords_mni for element in sublist]
            
            dict[vp]=sub_coords_mni
            #print(dict)


    elif pathmanager.Exp == 'VerFlu_TI' or pathmanager.Exp == 'VerFlu_TM' or pathmanager.Exp == 'VerFlu_Phon':
        if os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", "simulations_mni", f"{vp}_TDCS_1_scalar.msh")): 
                
            head_mesh = simnibs.read_msh(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", "simulations_mni", f"{vp}_TDCS_1_scalar.msh"))    
            gray_matter = head_mesh.crop_mesh(2) # only gm
            
            # arg1: MNI coords, arg2: m2m path
                      
            #nur für MNIcoordinaten notwendig
            sub_coords_mni = simnibs.mni2subject_coords(mni_coords,os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS",f"m2m_{vp}"))
            sub_coords_mni = [element for sublist in sub_coords_mni for element in sublist]
            
            dict[vp]=sub_coords_mni
            #print(dict)
df=pd.DataFrame.from_dict(dict,orient='index',columns=columns)
print(df)

if not os.path.isfile('./Source_Data/Electrode_Coordinates_full_coregistr_mni2sub.xlsx'):
    writer= pd.ExcelWriter('./Source_Data/Electrode_Coordinates_full_coregistr_mni2sub.xlsx')  
    df.to_excel(writer, sheet_name=sheet)
    # save also to tsv if something goes wrong with excel file
    writer.save()
    df.to_csv(os.path.join(pathmanager.CODEDIRECTORY,f'coordinates_table/{pathmanager.Exp}_{Session}_mni2sub_coordinates.tsv'),sep='\t')

else: 
    with pd.ExcelWriter('./Source_Data/Electrode_Coordinates_full_coregistr_mni2sub.xlsx', mode='a',if_sheet_exists='overlay') as writer:  
        df.to_excel(writer, sheet_name=sheet)
    df.to_csv(os.path.join(pathmanager.CODEDIRECTORY,f'coordinates_table/{pathmanager.Exp}_{Session}_mni2sub_coordinates.tsv'),sep='\t')








#%% Get simulation results at ROI
#https://simnibs.github.io/simnibs/build/html/tutorial/analysis.html

