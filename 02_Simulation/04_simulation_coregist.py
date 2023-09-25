#Issue: Run simulation for all conventional and actual HD-tDCS experiments
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

from numpy import asarray
import numpy as np
import simnibs
import csv
import fnmatch
from scipy.stats import pearsonr

# if you run the script 
# Note that 3 Windows will pop up and request info. You have to choose: 
#   1. the Experiment (VerFlu_HI, VerFlu_HM, VerFlu_TI, VerFlu_TM) 
#   2. the Session (Kopf, Zahl)
# To get all data processes you habe to run the combination of all of them

# Get all neccessary parameters

Session=input("Which Session? Kopf or Zahl? input ->")
sheet= pathmanager.Exp +'_' + Session

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
DIMENSION_SPONGE_CATHODE=[100,100]  # in mm (electrode in sponge is only 50, 70 
THICKNESS_SPONGE=[4, 2, 4] #Electrode 2mm thick rubber electrode in the middle of a 8mm thick sponge
DIMENSION_CATHODE=[50,70]
DIMENSION_ANODE=[50,70] 

## Run simulation for actual coordinates

for vp in stim_data.index:
    try:
        if not os.path.isfile(os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", "simulations_cor","fields_summary.txt"))):
            if stim_data["tDCS"].loc[vp] == "HD":

                tdcslist = sim_struct.TDCSLIST()
                tdcslist.currents = [1e-3, -0.333e-3, -0.333e-3, -0.334e-3]
            
                anode = tdcslist.add_electrode()          
     
                anode.centre = [stim_data["anode_x"].loc[vp],
                            stim_data["anode_y"].loc[vp],
                            stim_data["anode_z"].loc[vp]]
                anode.shape = 'ellipse'
                anode.dimensions = DIMENSION
                anode.thickness = THICKNESS
                anode.channelnr = 1;            
                e_pos = [
                [stim_data["cathode_1_x"].loc[vp], 
                stim_data["cathode_1_y"].loc[vp],
                stim_data["cathode_1_z"].loc[vp]],
                [stim_data["cathode_2_x"].loc[vp], 
                stim_data["cathode_2_y"].loc[vp],
                stim_data["cathode_2_z"].loc[vp]],
                [stim_data["cathode_3_x"].loc[vp], 
                stim_data["cathode_3_y"].loc[vp],
                stim_data["cathode_3_z"].loc[vp]]
            ]
            
                for ch,pos in enumerate(e_pos, 2):
                    cathode = tdcslist.add_electrode()
                    cathode.centre = pos
                    cathode.shape = 'ellipse'
                    cathode.dimensions = DIMENSION
                    cathode.thickness = THICKNESS
                    cathode.channelnr = ch
            
    
                if os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"{vp}.msh")):
                    s = sim_struct.SESSION()
                    s.map_to_fsavg = True
                    s.map_to_MNI = True
                    s.fields = 'eEjJ'
                    s.fnamehead = os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"{vp}.msh")
                    s.pathfem = os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", "simulations_cor")
                    s.open_in_gmsh = False
                    s.add_poslist(tdcslist)
                    run_simnibs(s)

            #condition konventionel setup 
                             
            elif stim_data["tDCS"].loc[vp] == "konv":
                tdcslist = sim_struct.TDCSLIST()
                tdcslist.currents = [1e-3, -1e-3]
            
                anode = tdcslist.add_electrode()

                anode.centre = [stim_data["anode_x"].loc[vp],
                            stim_data["anode_y"].loc[vp],
                            stim_data["anode_z"].loc[vp]]
                anode.pos_ydir = [stim_data["anode_orientation_x"].loc[vp],
                            stim_data["anode_orientation_y"].loc[vp],
                            stim_data["anode_orientation_z"].loc[vp]]  #if not try P7 T7 or C5

                anode.shape = 'rect'  #rect or ellipse or custom
                anode.dimensions = DIMENSION_ANODE
                anode.thickness = THICKNESS_SPONGE
                anode.dimensions_sponge = DIMENSION_SPONGE_ANODE
                anode.channelnr = 1;                
                plug_an = anode.add_plug()
                plug_an.shape = 'rect'
                plug_an.dimensions = [5, 20]
                plug_an.centre = [0, 25]
                            
                
                cathode = tdcslist.add_electrode()
                cathode.centre = [stim_data["cathode_1_x"].loc[vp], 
                stim_data["cathode_1_y"].loc[vp],
                stim_data["cathode_1_z"].loc[vp]]
                cathode.pos_ydir = [stim_data["cathode_orientation_x"].loc[vp],
                            stim_data["cathode_orientation_y"].loc[vp],
                            stim_data["cathode_orientation_z"].loc[vp]]
                cathode.shape = 'rect' #rect or ellipse or custom
                cathode.dimensions = DIMENSION_CATHODE
                cathode.thickness = THICKNESS_SPONGE
                cathode.dimensions_sponge = DIMENSION_SPONGE_CATHODE
                cathode.channelnr = 2

                plug_ca = cathode.add_plug()
                plug_ca.shape = 'rect'
                plug_ca.dimensions = [5, 20]
                plug_ca.centre = [0, 25]

                if os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"{vp}.msh")):
                    s = sim_struct.SESSION()
                    s.map_to_fsavg = True
                    s.map_to_MNI = True
                    s.fields = 'eEjJ'
                    s.fnamehead = os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"{vp}.msh")
                    s.pathfem = os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", "simulations_cor")
                    s.open_in_gmsh = False
                    s.add_poslist(tdcslist)
                    run_simnibs(s)

                    
    except:
        print(f'check Subject {vp}')

## Run simulation for plannend coordinates

r = 10. # 10 mm radius
field_name = 'normE'

if region=="IFG":
    mni_coords_anode=[-68.917, 34.5,16.97]  # MNI IFG position
    mni_coords_radius_orientation=[-70.712, 33.62, -9.95]#parallel point thoru FT7 adn FT9 as first orientation
    mni_coords_sponge=[[-68.917, 34.5,16.97],[36.47,75.46,21.04]]   #1x1 setup Anode IFG, Cathode AF4
    mni_coords_ydir_anode=[-80.1, -5.69, 21.16]   #or parallel through T7
    mni_coords_ydir_cathode=[31,54,56]   #F6
elif region=="M1":
    mni_coords_anode=[-67.99, -13.10, 61.52]   # MNI M1 position C3
    mni_coords_radius_orientation=[-38.29,-10.91,86.93] #C1 as orientation
    mni_coords_sponge=[[-67.99, -13.10, 61.52],[36.47,75.46,21.04]] #'C3'
    mni_coords_ydir_anode=[-58.92,21.42,54.49]   #FC3 dire
    mni_coords_ydir_cathode=[31,54,56] #F6


for vp in stim_data.index:
    try:
        if not os.path.isdir(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", "simulations_mni")):
            if stim_data["tDCS"].loc[vp] == "HD":

                tdcslist = sim_struct.TDCSLIST()
                tdcslist.currents = [1e-3, -0.333e-3, -0.333e-3, -0.334e-3]
            
                anode = tdcslist.add_electrode()

                trans_coord=mni2subject_coords(mni_coords, os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"m2m_{vp}"))


                anode.centre = trans_coord[0]
                anode.shape = 'ellipse'
                anode.dimensions = DIMENSION
                anode.thickness = THICKNESS
                anode.channelnr = 1;
            
                e_pos = trans_coord[1:]
            
                for ch,pos in enumerate(e_pos, 2):
                    cathode = tdcslist.add_electrode()
                    cathode.centre = pos
                    cathode.shape = 'ellipse'
                    cathode.dimensions = DIMENSION
                    cathode.thickness = THICKNESS
                    cathode.channelnr = ch
            

                if os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"{vp}.msh")):
                    s = sim_struct.SESSION()
                    s.map_to_fsavg = True
                    s.map_to_MNI = True
                    s.fields = 'eEjJ'
                    s.fnamehead = os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"{vp}.msh")
                    s.pathfem = os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", "simulations_mni")
                    s.open_in_gmsh = False
                    s.add_poslist(tdcslist)
                    run_simnibs(s)
                else:
                    print(f'no correct {vp}.msh file' )


              #condition konventionel setup 
            
                    
            elif stim_data["tDCS"].loc[vp] == "konv":
                tdcslist = sim_struct.TDCSLIST()
                tdcslist.currents = [1e-3, -1e-3]
            
                anode = tdcslist.add_electrode()
                print(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"m2m_{vp}"))
                trans_coord=mni2subject_coords(mni_coords_sponge, os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"m2m_{vp}"))
            
            
                trans_coord_ydir_anode=mni2subject_coords(mni_coords_ydir_anode, os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"m2m_{vp}"))
                print(trans_coord_ydir_anode)

                anode.centre =  trans_coord[0]   # trans_coord[0] 
                anode.pos_ydir =trans_coord_ydir_anode             #trans_coord_ydir_anode[0]
       
                anode.shape = 'rect'  #rect or ellipse or custom
                anode.dimensions = DIMENSION_ANODE
                anode.thickness = THICKNESS_SPONGE
                anode.dimensions_sponge = DIMENSION_SPONGE_ANODE
                anode.channelnr = 1;
                
                plug_an = anode.add_plug()
                plug_an.shape = 'rect'
                plug_an.dimensions = [5, 20]
                plug_an.centre = [0, 25]
            
                trans_coord_ydir_cathode=mni2subject_coords(mni_coords_ydir_cathode, os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"m2m_{vp}"))     
                
                cathode = tdcslist.add_electrode()
                cathode.centre =  trans_coord[1]
                cathode.pos_ydir = trans_coord_ydir_cathode  #trans_coord_ydir_cathode[0]
                cathode.shape = 'rect' #rect or ellipse or custom
                cathode.dimensions = DIMENSION_CATHODE
                cathode.thickness = THICKNESS_SPONGE
                cathode.dimensions_sponge = DIMENSION_SPONGE_CATHODE
                cathode.channelnr = 2

                plug_ca = cathode.add_plug()
                plug_ca.shape = 'rect'
                plug_ca.dimensions = [5, 20]
                plug_ca.centre = [0, 25]

                if os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"{vp}.msh")):
                    s = sim_struct.SESSION()
                    s.map_to_fsavg = True
                    s.map_to_MNI = True
                    s.fields = 'eEjJ'
                    s.fnamehead = os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", f"{vp}.msh")
                    s.pathfem = os.path.join(pathmanager.BASEDIRECTORY, vp, f"ses-{Session}", "SimNIBS", "simulations_mni")
                    s.open_in_gmsh = False
                    s.add_poslist(tdcslist)
                    run_simnibs(s)
                else:
                    print(f'no correct {vp}.msh file' )
            else: 
                print(f'simnibs_mni folder already exists for subject {vp}')
    except:
        print(f' something could be wrong {vp}')
    
       



 