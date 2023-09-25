#Issue: Create images for Figure S1-S4, for actual electrode position
#Author: Filip Niemann & Steffen Riemann
#Date: 21.09.2023

"""
If the mes file is opened with gmesh

to overlap EEG coordinates with brain *geo file must be merged with head

help for parameters https://simnibs.github.io/simnibs/build/html/documentation/sim_struct/electrode.html

Install pandas in simnibs_python before running. "simnibs_python -m pip install pandas==1.2.0"
"simnibs python -m pip install openpyxl"
"""




import os
#import pathmanager
import pandas as pd
from simnibs import sim_struct, run_simnibs, mni2subject_coords
import sys

sys.path.append(r'/media/Data01/Studien/VerFlu/code/Python_Modules/SimNIBS_enhanced')
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

mni_head = '/media/Data01/Studien/VerFlu/code/SimNIBS/MNIhead'
#how to handle outlier

#pathmanager is asking for input and gives variable Exp, similar like
#Exp= input("Welches Experiment, wähle zwischen: VerFlu_HI, VerFlu_TI,VerFlu_HM,VerFlu_TM,VerFlu_Phon Eingabe->")

Experiment=input("Welches Experiment VerFlu_HI; VerFlu_TI, VerFlu_HM, VerFlu_TM ->")

sheet= Experiment +'_' + "Kopf"
stim_data_cor_Kopf = pd.read_excel("/media/Data01/Studien/VerFlu/code/SimNIBS/coordinates_table/Electrode_Coordinates_full_coregistr_sub2mni.xlsx", sheet_name=sheet, engine="openpyxl")
stim_data_cor_Kopf['id']=stim_data_cor_Kopf['id'] + Experiment 
sheet= Experiment +'_' + "Zahl"
stim_data_cor_Zahl = pd.read_excel("/media/Data01/Studien/VerFlu/code/SimNIBS/coordinates_table/Electrode_Coordinates_full_coregistr_sub2mni.xlsx", sheet_name=sheet, engine="openpyxl")
stim_data_cor_Zahl['id']=stim_data_cor_Zahl['id'] + Experiment 

stim_data_cor = pd.concat(stim_data_cor_Kopf,stim_data_cor_Zahl)

stim_data_cor = stim_data_cor.set_index("id")


print(f'show all {stim_data_cor}')



DIMENSION = [25, 25]   #in mm
THICKNESS = [0.1, 0.1]

DIMENSION_SPONGE_ANODE=[50,70]  #in mm
DIMENSION_SPONGE_CATHODE=[100,100]  # in mm (electrode in sponge is only 50, 70 
THICKNESS_SPONGE=[0.1, 0.5, 0.1] #Electrode 2mm thick rubber electrode in the middle of a 8mm thick sponge
DIMENSION_CATHODE=[50,70]
DIMENSION_ANODE=[50,70] 


#r = 10. # 10 mm radius
field_name = 'normE'


dict={}
for vp in stim_data_cor.index:
    sub_coords=[[stim_data_cor["anode_x"].loc[vp],stim_data_cor["anode_y"].loc[vp],stim_data_cor["anode_z"].loc[vp]],[stim_data_cor["cathode_1_x"].loc[vp],stim_data_cor["cathode_1_y"].loc[vp],stim_data_cor["cathode_1_z"].loc[vp]],[stim_data_cor["cathode_2_x"].loc[vp],stim_data_cor["cathode_2_y"].loc[vp],stim_data_cor["cathode_2_z"].loc[vp]],[stim_data_cor["cathode_3_x"].loc[vp],stim_data_cor["cathode_3_y"].loc[vp],stim_data_cor["cathode_3_z"].loc[vp]]] #HD
    
   

# %%                                           mni space


    
if os.path.isfile(os.path.join(mni_head, f"MNI152.msh")): 
    S = sim_struct.SESSION()
    
    #S.fnamehead = 'ernie.msh'  # head mesh
    #S.pathfem = 'tdcs_Nx1' # output directory for the simulation
    S.fnamehead = os.path.join(os.path.join(mni_head, f"MNI152.msh"))  #head mesh
    S.pathfem = os.path.join(os.path.join(mni_head, f'simulations_mni_{Experiment}_actual'))  #output directory for the simulation
    #S.map_to_surf = True # map to subject's middle gray matter surface (optional)
    S.fields = 'eEjJ'    # FN 28-11-2022 
    #S.map_to_fsavg = True
    #S.map_to_MNI = True
    #change to False , by default gmsh is shown
    S.open_in_gmsh = True


 
#get new radius for anodal coordinate
if Experiment == "VerFlu_HI" or Experiment == "VerFlu_HM":
    ###     SETUP
    ###################


    tdcs_list = S.add_tdcslist()
    tdcs_list.currents = 0.001  # Current flow through center channel (mA)

    # define the center electrode
    center = tdcs_list.add_electrode()
    #center.centre = 'C3'  # Place it over C3
    center.centre = mni_coords_Anode  # Place it over IFG or M1
    center.shape = 'ellipse'  # round shape
    center.dimensions = DIMENSION # 100 mm diameter or 500 mm radius =5 cm radius
    center.thickness = THICKNESS  # 2 mm rubber electrodes on top of 0.5 mm gel layer
    
    # parameters for setting up the surround electrodes
    radius_surround = 45 # distance (centre-to-centre) between the centre and   
                        # surround electrodes (optional; standard: 50 mm)
    #pos_dir_1stsurround = 'C4' # a position indicating the direction in which the 
                            # first surround electrode should be placed 
                            # (optional; standard: None)
    pos_dir_1stsurround = mni_coords_radius_orientation                     
    #N = 4 # number of surround electrodes (optional; standard: 4)
    N = 3 # number of surround electrodes (optional; standard: 4)  FN 28-11-2022 change for 3x1 setup
    multichannel = False # when set to True: Simulation of multichannel stimulator 
                        # with each suround channel receiving 1/N-th of the
                        # center channel (optional; standard: False, i.e. all 
                        # surround electrodes connected to the same channel)

    # set up surround electrodes
    #tdcs_list = expand_to_center_surround(tdcs_list, S.fnamehead, radius_surround, 
    #                                    N, pos_dir_1stsurround, multichannel)

    # set up surround electrodes

    tdcs_list = SE.Simnibs_enhanced.expand_to_center_surround(tdcs_list, S.fnamehead, radius_surround, 
                                        N, pos_dir_1stsurround, multichannel)

       
elif Experiment == "VerFlu_TI" or Experiment == "VerFlu_TM" or Experiment == "VerFlu_Phon":
    #tdcslist = sim_struct.TDCSLIST()
    tdcs_list = S.add_tdcslist()
    #tdcs_list = sim_struct.TDCSLIST()
    tdcs_list.currents = [1e-3, -1e-3]
                  
    anode = tdcs_list.add_electrode()



    anode.centre =  mni_coords_sponge[0]   # trans_coord[0] 
    anode.pos_ydir =mni_coords_ydir_anode            #trans_coord_ydir_anode[0]
        #if not try P7,T7 or C5 or a new direction in mni space            
    anode.shape = 'rect'  #rect or ellipse or custom
    anode.dimensions = DIMENSION_ANODE
    anode.thickness = THICKNESS_SPONGE
    anode.dimensions_sponge = DIMENSION_SPONGE_ANODE
    anode.channelnr = 1
    
    plug_an = anode.add_plug()
    plug_an.shape = 'rect'
    plug_an.dimensions = [5, 20]
    plug_an.centre = [0, 25]

 
    cathode = tdcs_list.add_electrode()
    cathode.centre =  mni_coords_sponge[1]
    cathode.pos_ydir = mni_coords_ydir_cathode  #trans_coord_ydir_cathode[0]
    cathode.shape = 'rect' #rect or ellipse or custom
    cathode.dimensions = DIMENSION_CATHODE
    cathode.thickness = THICKNESS_SPONGE
    cathode.dimensions_sponge = DIMENSION_SPONGE_CATHODE
    cathode.channelnr = 2

    plug_ca = cathode.add_plug()
    plug_ca.shape = 'rect'
    plug_ca.dimensions = [5, 20]
    plug_ca.centre = [0, 25]

 

    ### RUN SIMULATION
    ###################
run_simnibs(S)

    


    #    print(f'simnibs_mni folder already exists for subject {vp}')
    
       



    
#%% Get peak current flow and correlate with meanE in ROI

