#function handles main input difference which are Experimenttype, Session and E-field  
#THIS IS WRITTEN FOR SIMNIBS 3.2
#Author Filip Niemann
#Date 13.12.2022
import os
import sys
sys.path.append(os.chdir('../')) #needed function are in parent folder
import pathmanager
import pandas as pd
from simnibs import sim_struct, run_simnibs, mni2subject_coords

import Outlier_list_function as Olf 

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

#Transformation of MNI152 to fsaverage space (MNI305)
M=np.matrix([[1.0022, 0.0071, -0.0177, 0.0528],
            [-0.0146, 0.9990, 0.0027, -1.5519],
            [0.0129, 0.0094, 1.0027, -1.2012]])

#readout_in=['sub_space','fsaverage_mni_space']
Experiment=pathmanager.Exp

def Read_out_Efields(Experiment, Session,region,field_name,subject_space,readout_in,roi_type,r):
    

    sheet= pathmanager.Exp +'_' + Session
    if pathmanager.Exp=='VerFlu_HI' or pathmanager.Exp == 'VerFlu_HM':
        stim_data_cor = pd.read_excel(os.path.join(os.chdir('../Source_Data'),"Electrode_Coordinates_full_coregistr.xlsx"), sheet_name=sheet, engine="openpyxl")
        stim_data_rad = pd.read_excel(os.path.join(os.chdir('../Source_Data'),"HD-tDCS_individ_radius5cm_mni2subj.xlsx"), sheet_name=sheet, engine="openpyxl")

        stim_data_cor=stim_data_cor.set_index('id')
        stim_data_rad=stim_data_rad.set_index('id')

        #drop outlier
        if pathmanager.Exp == 'VerFlu_HI':
            [outlier_List,outlier_List_sub,outlier_List_sub_sex_id,outlier_list_only_measured_subjecst,outlier_list_only_measured_subjecst_SimNIBS,outlier]=Olf.Outlier_function(pathmanager.Exp)
            OUTLIER=outlier_list_only_measured_subjecst_SimNIBS
            stim_data_cor = stim_data_cor.drop(OUTLIER, errors = "ignore")
            stim_data_rad = stim_data_rad.drop(OUTLIER, errors = "ignore")

        elif pathmanager.Exp == 'VerFlu_HM':
            [outlier_List,outlier_List_sub,outlier_List_sub_sex_id,outlier_list_only_measured_subjecst,outlier_list_only_measured_subjecst_SimNIBS,outlier]=Olf.Outlier_function(pathmanager.Exp)
            OUTLIER=outlier_list_only_measured_subjecst_SimNIBS
            stim_data_cor = stim_data_cor.drop(OUTLIER, errors = "ignore")
            stim_data_rad = stim_data_rad.drop(OUTLIER, errors = "ignore")



        

    elif pathmanager.Exp=='VerFlu_TI' or pathmanager.Exp == 'VerFlu_TM' or pathmanager.Exp == 'VerFlu_Phon':
        stim_data_cor = pd.read_excel(os.path.join(os.chdir('../Source_Data'),"Electrode_Coordinates_full_coregistr.xlsx"), sheet_name=sheet, engine="openpyxl")
        stim_data_cor=stim_data_cor.set_index('id')

                #drop outlier
        if pathmanager.Exp == 'VerFlu_TI':
            [outlier_List,outlier_List_sub,outlier_List_sub_sex_id,outlier_list_only_measured_subjecst,outlier_list_only_measured_subjecst_SimNIBS,outlier]=Olf.Outlier_function(pathmanager.Exp)
            OUTLIER=outlier_list_only_measured_subjecst_SimNIBS
            stim_data_cor = stim_data_cor.drop(OUTLIER, errors = "ignore")
       

        elif pathmanager.Exp == 'VerFlu_TM':
            [outlier_List,outlier_List_sub,outlier_List_sub_sex_id,outlier_list_only_measured_subjecst,outlier_list_only_measured_subjecst_SimNIBS,outlier]=Olf.Outlier_function(pathmanager.Exp)
            OUTLIER=outlier_list_only_measured_subjecst_SimNIBS
            stim_data_cor = stim_data_cor.drop(OUTLIER, errors = "ignore")
        
        elif pathmanager.Exp == 'VerFlu_Phon':
            [outlier_List,outlier_List_sub,outlier_List_sub_sex_id,outlier_list_only_measured_subjecst,outlier_list_only_measured_subjecst_SimNIBS,outlier]=Olf.Outlier_function(pathmanager.Exp)
            OUTLIER=outlier_list_only_measured_subjecst_SimNIBS
            stim_data_cor = stim_data_cor.drop(OUTLIER, errors = "ignore")
  


 
    outlier=[]
    fields=[]
    dict_data={}
    for sub in stim_data_cor.index:
        # only read TDCS_1_scalar_center.msh and  TDCS_1_scalar_fsavg.msh containing only nodes and no baricenter elements 

        #conventionel tDCS coordinates from subjects space, read out from original coregistered T1 images 
        if subject_space=='sub' and (stim_data_cor['tDCS'].eq('konv')).any() and readout_in=='sub-space':
            meshfile=os.path.join(pathmanager.BASEDIRECTORY,sub, f"ses-{Session}", "SimNIBS", "simulations_cor",'subject_overlays', f"{sub}_TDCS_1_scalar_central.msh")

        #conventionel tDCS coordinates from optimal montage in mni space to subjects space
        elif subject_space=='mni2sub' and (stim_data_cor['tDCS'].eq('konv')).any() and readout_in=='sub-space':
            meshfile=os.path.join(pathmanager.BASEDIRECTORY,sub, f"ses-{Session}", "SimNIBS", "simulations_mni",'subject_overlays', f"{sub}_TDCS_1_scalar_central.msh")

        #focal tDCS coordinates from subjects space, read out from original coregistered T1 images 

        elif subject_space=='sub' and (stim_data_cor['tDCS'].eq('HD')).any() and readout_in=='sub-space':
            meshfile=os.path.join(pathmanager.BASEDIRECTORY,sub, f"ses-{Session}", "SimNIBS", "simulations_cor",'subject_overlays', f"{sub}_TDCS_1_scalar_central.msh")
            

        #focal tDCS coordinates from optimal montage anod coordinates in mni space transformed into subjects space 
        # read out from original coregistered T1 images 

        elif subject_space=='mni2sub' and (stim_data_cor['tDCS'].eq('HD')).any() and readout_in=='sub-space':
            meshfile=os.path.join(pathmanager.BASEDIRECTORY,sub, f"ses-{Session}", "SimNIBS", "simulations_mni_indiv_radius",'subject_overlays', f"{sub}_TDCS_1_scalar_central.msh")
            

        # only read TDCS_1_scalar_fsavg.msh for mni rois or  for subject space

            #conventionel tDCS coordinates from subjects space, read out from original coregistered T1 images 
        elif subject_space=='sub' and (stim_data_cor['tDCS'].eq('konv')).any() and readout_in=='fsaverage_mni_space':
            meshfile=os.path.join(pathmanager.BASEDIRECTORY,sub, f"ses-{Session}", "SimNIBS", "simulations_cor","fsavg_overlays", f"{sub}_TDCS_1_scalar_fsavg.msh")

        #conventionel tDCS coordinates from optimal montage in mni space to subjects space
        elif subject_space=='mni2sub' and (stim_data_cor['tDCS'].eq('konv')).any() and readout_in=='fsaverage_mni_space':
            meshfile=os.path.join(pathmanager.BASEDIRECTORY,sub, f"ses-{Session}", "SimNIBS", "simulations_mni","fsavg_overlays", f"{sub}_TDCS_1_scalar_fsavg.msh")

        #focal tDCS coordinates from subjects space, read out from original coregistered T1 images 

        elif subject_space=='sub' and (stim_data_cor['tDCS'].eq('HD')).any() and readout_in=='fsaverage_mni_space':
            meshfile=os.path.join(pathmanager.BASEDIRECTORY,sub, f"ses-{Session}", "SimNIBS", "simulations_cor","fsavg_overlays", f"{sub}_TDCS_1_scalar_fsavg.msh")
            

        #focal tDCS coordinates from optimal montage anod coordinates in mni space transformed into subjects space 
        # read out from original coregistered T1 images 

        elif subject_space=='mni2sub' and (stim_data_cor['tDCS'].eq('HD')).any() and readout_in=='fsaverage_mni_space':
            meshfile=os.path.join(pathmanager.BASEDIRECTORY,sub, f"ses-{Session}", "SimNIBS", "simulations_mni_indiv_radius","fsavg_overlays", f"{sub}_TDCS_1_scalar_fsavg.msh")
            

        else:
            meshfile='Nope'
            print('something is wrong in if statements check for typo')


        if not os.path.isfile(meshfile):
            print(F'{sub} mesh is not available')
            outlier.append(sub)
        elif os.path.isfile(meshfile):
            print(meshfile)
            
            ##  differentiat if mean e field is taken from subject space or from mni / fsaverage space
            if region=="IFG" and readout_in=='fsaverage_mni_space':
                coords=[-57,24,12,1]
                print('MNI coord:',coords)
                coords=M.dot(coords)  #transform MNI152 coordinates into MNI305 coordinates
                print('fsaverage coord:',coords)

            elif region=="IFG" and readout_in=='sub-space':
                mni_coords=[-57,24,12]
                #transform into subject space
                coords = simnibs.mni2subject_coords(mni_coords,os.path.join(pathmanager.BASEDIRECTORY, sub, f"ses-{Session}", "SimNIBS",f"m2m_{sub}"))
            
            elif region=="M1" and readout_in=='fsaverage_mni_space':
                coords=[-52.2,-16.4,57.8,1]
                print('MNI coord:',coords)
                coords=M.dot(coords)  #transform MNI152 coordinates into MNI305 coordinates
                print('fsaverage coord:',coords)
 
            elif region=="M1" and readout_in=='sub-space':
                coords=[-52.2,-16.4,57.8]
                coords = simnibs.mni2subject_coords(mni_coords,os.path.join(pathmanager.BASEDIRECTORY, sub, f"ses-{Session}", "SimNIBS",f"m2m_{sub}"))
                
            atlas = simnibs.get_atlas('HCP_MMP1') 
            #https://www.nature.com/articles/nature18933
            #ther download supplementary
            if region =='IFG' and roi_type =='mask':
                region_names = ['lh.44','lh.45', 'lh.47l','lh.p47r','lh.FOP4','lh.FOP5','lh.IFSa','lh.IFSp','lh.IFJa']
                roi = [atlas[region_name] for region_name in region_names]
                roi=np.array(roi).sum(axis=0)   #sum all rois into one big mask

            elif region=='IFG' and roi_type=='sphere':
                
                #r=1.25,2.5,3.75
                radius=str(r)
            elif region=='M1' and roi_type=='mask':
                region_names = ['lh.4','lh.3a','lh.6mp','lh.FEF','lh.55b','lh.6v','lh.6d'] #5m shows no activity at all, so zero values
                roi = [atlas[region_name] for region_name in region_names]
                roi=np.array(roi).sum(axis=0)   #sum all rois into one big mask

            elif region=='M1' and roi_type=='sphere':    
                #r=1.25,2.5,3.75
                radius=str(r)

        #read mesh
        #two kinds of msh exist 
        # 1) volumen meshes like sub-01_TDCS_1_scalar.msh. There you can use crop_mesh(2) to get grey matter
        # 2) overlay meshes like sub-01_TDCS_1_scalar_central.msh or sub-01_TDCS_1_scalar_fsaverage.msh. typical in overlay folders use crop_mesh(1002)

        # read mesh with results transformed to fsaverage space

        #head mesh is already croped with value of 1002
            results_fsavg = simnibs.read_msh(meshfile)
            if roi_type=='sphere':
            #roi = np.linalg.norm(elm_centers - coords_sub, axis=1) < r
                roi = np.linalg.norm(results_fsavg.nodes.node_coord - coords, axis=1) < r

            elif roi_type=='mask':
                #node_areas = results_fsavg.nodes_areas()
                #field_roi = np.average(field[roi], weights=node_areas[roi])
                print('mask is used')
            field = results_fsavg.field[field_name][:]

            fields.append(results_fsavg.field[field_name][:])

        if field_name=='E_norm' and os.path.isfile(meshfile):
            # Calculate the mean
            node_areas = results_fsavg.nodes_areas()
            if roi_type=='mask':
                #get all values in roi as array and build mean
                field_mean=np.mean(results_fsavg.field[field_name].value[roi>0])
                field_std=np.std(results_fsavg.field[field_name].value[roi>0])
                size=len(results_fsavg.field[field_name].value[roi>0])
            elif roi_type=='sphere':
            
            
                field_mean=np.mean(results_fsavg.field[field_name][roi][results_fsavg.field[field_name][roi]>0])
                field_std=np.std(results_fsavg.field[field_name][roi][results_fsavg.field[field_name][roi]>0])
                size=len(results_fsavg.field[field_name][roi][results_fsavg.field[field_name][roi]>0])
                #write data in dict
            dict_data[sub]=[field_mean,field_std,size]
            columns_field=[f'mean magnitude E_{Session}',f'std magnitude E_{Session}',f'size_magnitude E_{Session}']
            print(field_mean,size)

        elif field_name=='E_normal' and os.path.isfile(meshfile):
            #results_fsavg.add_node_field(roi, region)
            node_areas = results_fsavg.nodes_areas()
            if roi_type=='mask':
                #get all value in mask an check if value in that mask is bigger or smaller then zero
                pos=results_fsavg.field[field_name].value[roi>0][results_fsavg.field[field_name].value[roi>0]>0]
                neg=results_fsavg.field[field_name].value[roi>0][results_fsavg.field[field_name].value[roi>0]<0]

                pos_field_mean=np.mean(pos)
                neg_field_mean=np.mean(neg)
                pos_field_std=np.std(pos)
                neg_field_std=np.std(neg)

                size_pos_field=len(pos)
                size_neg_field=len(neg)



            elif roi_type=='sphere':
                pos=results_fsavg.field[field_name][roi][results_fsavg.field[field_name][roi]>0]
                neg=results_fsavg.field[field_name][roi][results_fsavg.field[field_name][roi]<0]
                
                pos_field_mean=np.mean(pos)
                neg_field_mean=np.mean(neg)
                pos_field_std=np.std(pos)
                neg_field_std=np.std(neg)

                size_pos_field=len(pos)
                size_neg_field=len(neg)
            #write data in dict
            
            
            columns_field=[f'mean_E_normal_pos_{Session}',f'mean_E_normal_neg_{Session}',f'std_E_normal_pos_{Session}',f'std_E_normal_neg_{Session}',f'size_E_normal_pos_{Session}',f'size_E_normal_neg_{Session}']
            dict_data[sub]=[pos_field_mean,neg_field_mean,pos_field_std,neg_field_std,size_pos_field,size_neg_field]
            print(pos_field_mean,neg_field_mean)
        else:
            print('meshfile non existent for combination of variable, this could hapen in the loop')
    
    if dict_data:
        if roi_type=='mask':
            meanE_path_mni = os.path.join(os.chdir('../Source_Data'),pathmanager.Exp, f'{pathmanager.Exp}_{Session}_{region}_{roi_type}_{field_name}_{subject_space}_{readout_in}.tsv')
         
        elif roi_type=='sphere':    
            meanE_path_mni = os.path.join(os.chdir('../Source_Data'),pathmanager.Exp, f'{pathmanager.Exp}_{Session}_{region}_{roi_type}_{field_name}_{subject_space}_{readout_in}_{radius}.tsv')
        df=pd.DataFrame.from_dict(dict_data,orient='index',columns=columns_field)       
        df.to_csv(meanE_path_mni,sep="\t")
    
    

    ### show avg fiels
            
        print('outlier=',outlier)

        ## Calculate and plot averages
        # Calculate
        #beware all the input array dimensions for the concatenation axis must match exactly, but along dimension 1, the array at index 0 has size 294268 and the array at index 1 has size 273372
        
        # Plot field_name=['normE','E_normal']
        if field_name=='E_normal' and not readout_in=='sub-space' and fields:  #is readout_in== 'sub_space' roise have different sizes due to individual haedsize
   
            fields = np.vstack(fields)
            avg_field = np.mean(fields, axis=0)
            std_field = np.std(fields, axis=0)

            results_fsavg.nodedata = [] # cleanup fields
            results_fsavg.add_node_field(avg_field, 'E_normal_avg') # add average field to simnibs.msh class
            results_fsavg.add_node_field(std_field, 'E_normal_std') # add std field

            node_areas = results_fsavg.nodes_areas()

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
            neg_avg_field_rois.append(np.average(neg_avg_f, weights=neg_weight))
            neg_std_field_rois.append(np.average(neg_std_f, weights=neg_weight))

            #show roi
            results_fsavg.add_node_field(roi, region)
            #results_fsavg.view(visible_fields='roi').show()

            # Plot if elementdata not nodedata

        elif field_name=='E_norm' and not readout_in=='sub-space' and fields:   #is readout_in== 'sub_space' roise have different sizes due to individual haedsize

            fields = np.vstack(fields)
            avg_field = np.mean(fields, axis=0)
            std_field = np.std(fields, axis=0)


            # Plot
            results_fsavg.nodedata = [] # cleanup fields
            results_fsavg.add_node_field(avg_field, 'mean magnitude E avg') # add average field
            results_fsavg.add_node_field(std_field, 'mean magnitude E std') # add std field

            region_name = region

            # calculate mean field using a weighted mean
            node_areas = results_fsavg.nodes_areas()

            if roi_type=='sphere':
                avg_field_roi = np.average(avg_field[roi], weights=node_areas[roi])
            elif roi_type=='mask':
                avg_field_roi = np.average(avg_field[roi], weights=node_areas.value[roi])

            print(f'Average {field_name} in {region_name}: ', avg_field_roi)
            
            #show rois
            results_fsavg.add_node_field(roi, region_name)  
            #results_fsavg.view(visible_fields='roi').show()



    else:
        print('no meshfile')

        
    




   































