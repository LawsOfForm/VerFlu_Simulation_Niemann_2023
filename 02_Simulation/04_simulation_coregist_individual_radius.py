#Issue: Run simulation of planend electrode position for HD-tDCS experiments
#Author: Filip Niemann & Steffen Riemann
#Date: 21.09.2023

"""
help for parameters https://simnibs.github.io/simnibs/build/html/documentation/sim_struct/electrode.html

Install pandas in simnibs_python before running. "simnibs_python -m pip install pandas==1.2.0"
"simnibs python -m pip install openpyxl"
"""

import os
import pathmanager
import pandas as pd
from simnibs import sim_struct, run_simnibs, mni2subject_coords
import sys

sys.path.append(r'./SimNIBS_enhanced')
import Simnibs_enhanced as SE
#import Simnibs_enhanced 
from importlib import reload
reload(SE)

from numpy import asarray
import numpy as np
import simnibs
import csv
import fnmatch
from scipy.stats import pearsonr


#how to handle outlier

#pathmanager is asking for input and gives variable Exp, similar like
#Exp= input("Welches Experiment, wähle zwischen: VerFlu_HI, VerFlu_TI,VerFlu_HM,VerFlu_TM,VerFlu_Phon Eingabe->")

Session=input("Which session? Kopf or Zahl? input ->")
sheet= pathmanager.Exp +'_' + Session

os.chdir('/Source_Data')
stim_data = pd.read_excel(os.path.join(os.chdir('./Source_Data'),"Electrode_Coordinates_full_coregistr.xlsx"), 
                          sheet_name=sheet, engine="openpyxl")

if pathmanager.Exp == "VerFlu_HI" or pathmanager.Exp == "VerFlu_TI":
    region = 'IFG'
elif pathmanager.Exp == "VerFlu_HM" or pathmanager.Exp == "VerFlu_TM": 
    region = 'M1'



stim_data = stim_data.set_index("id")

print(f'show all {stim_data}')



DIMENSION = [25, 25]   #in mm
THICKNESS = [1, 2]

DIMENSION_SPONGE_ANODE=[50,70]  #in mm
DIMENSION_SPONGE_CATHODE=[100,100]  # in mm
THICKNESS_SPONGE=[4, 2, 4] #Electrode 2mm thick rubber electrode in the middle of a 8mm thick sponge

field_name = 'normE'
#field_name = 'normalE'
   

# %%                                           mni space

if region=="IFG":
    mni_coords_Anode=[-68.917, 34.5,16.97]  # MNI IFG position
    mni_coords_radius_orientation=[-70.712, 33.62, -9.95] #parallel point thoru FT7 adn FT9 as first orientation
    mni_coords_sponge=[[-68.917, 34.5,16.97],[36.47,75.46,21.04]]   #1x1 setup Anode IFG, Cathode AF4
    mni_coords_ydir_anode=[-80.1, -5.69, 21.16]   #or parallel through T7
    mni_coords_ydir_cathode=[31,54,56]   #F6
elif region=="M1":
    mni_coords_Anode=[-67.99, -13.10, 61.52]   # MNI M1 position C3
    mni_coords_radius_orientation=[-38.29,-10.91,86.93] #C1 as orientation
    mni_coords_sponge=[[-67.99, -13.10, 61.52],[36.47,75.46,21.04]] #'C3'
    mni_coords_ydir_anode=[-58.92,21.42,54.49]   #FC3 dire
    mni_coords_ydir_cathode=[31,54,56] #F6



for vp in stim_data.index:
    #try:
    if not os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", "simulations_mni_indiv_radius","fields_summary.txt")):
        if stim_data["tDCS"].loc[vp] == "HD":

#get new radius for anodal coordinate
            if os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"{vp}.msh")):
                ###     SETUP
                ###################
                S = sim_struct.SESSION()
                # transform mni to subject coordinates
                mni_coords_Anode_mni2sub=mni2subject_coords(mni_coords_Anode, os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"m2m_{vp}"))     
                mni_coords_radius_orientation_mni2sub=mni2subject_coords(mni_coords_radius_orientation, os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"m2m_{vp}"))
                #S.fnamehead = 'ernie.msh'  # head mesh
                #S.pathfem = 'tdcs_Nx1' # output directory for the simulation
                S.fnamehead = os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"{vp}.msh")  #head mesh
                S.pathfem = os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", "simulations_mni_indiv_radius")  #output directory for the simulation
                #S.map_to_surf = True # map to subject's middle gray matter surface (optional)
                S.fields = 'eEjJ'    # FN 28-11-2022 
                S.map_to_fsavg = True
                S.map_to_MNI = True
                #change to False , by default gmsh is shown
                S.open_in_gmsh = False

                tdcs_list = S.add_tdcslist()
                tdcs_list.currents = 0.001  # Current flow through center channel (mA)

                # define the center electrode
                center = tdcs_list.add_electrode()
                #center.centre = 'C3'  # Place it over C3
                center.centre = mni_coords_Anode_mni2sub  # Place it over IFG or M1
                center.shape = 'ellipse'  # round shape
                center.dimensions = DIMENSION # 100 mm diameter or 500 mm radius =5 cm radius
                center.thickness = THICKNESS  # 2 mm rubber electrodes on top of 0.5 mm gel layer
                
                # parameters for setting up the surround electrodes
                radius_surround = 45 # distance (centre-to-centre) between the centre and   
                                    # surround electrodes (optional; standard: 50 mm)
                #pos_dir_1stsurround = 'C4' # a position indicating the direction in which the 
                                        # first surround electrode should be placed 
                                        # (optional; standard: None)
                pos_dir_1stsurround = mni_coords_radius_orientation_mni2sub                       
                #N = 4 # number of surround electrodes (optional; standard: 4)
                N = 3 # number of surround electrodes (optional; standard: 4)  FN 28-11-2022 change for 3x1 setup
                multichannel = True # when set to True: Simulation of multichannel stimulator 
                                    # with each suround channel receiving 1/N-th of the
                                    # center channel (optional; standard: False, i.e. all 
                                    # surround electrodes connected to the same channel)

                # set up surround electrodes
                #tdcs_list = expand_to_center_surround(tdcs_list, S.fnamehead, radius_surround, 
                #                                    N, pos_dir_1stsurround, multichannel)

                # set up surround electrodes

                tdcs_list = SE.Simnibs_enhanced.expand_to_center_surround(tdcs_list, S.fnamehead, radius_surround, 
                                                    N, pos_dir_1stsurround, multichannel)
                    


                ### RUN SIMULATION
                ###################
                
                run_simnibs(S)
                

            else:
                print(f'{vp} has no msh data')
            #condition konventionel setup 

        else: 
            print(f'simnibs_mni folder already exists for subject {vp}')
    #except:
    #    print(f'simnibs_mni folder already exists for subject {vp}')
    
       




