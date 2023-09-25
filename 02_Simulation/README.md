# VerFlu_simulation_Niemann_2023

## Help simulation scripts

0. All scripts only will work if there are data in [00_MRI_Data](../00_MRI_Data)
   - [Request data here](mailto:filip.niemann@med.uni-greifswald.de)
   - Note: You don't need MRI data to inspect main outcomes, you will find analysis scripts
     - [Analysis of electrode differences](../03_Analysis_Electrode_Difference/README.md)
     - [Analysis of simulated E-filed](../04_Analysis_Simulated_E-fields/README.md)
1. First open and change the commented directories [in this script](00_pathmanager.py)
2. Run the [01_reorient2std.py] script, to reorient the T1 into standardspace [fslreorient2std](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Orientation%20Explained)

   1. If you have simnibs 3.2.6 installed as conda environment "simnibs_env" [recommended](https://simnibs.github.io/simnibs/build/html/installation/conda.html), activate your conda environment
      - Note: YAML file [simnibs_env.yml](simnibs_env.yml) is provided for install help

    ```{bash}
    (base)$conda activate simnibs_env
    ```  

   2. If SimNIBS is not installed as virtual environment only run code below

- Run script via

```{bash}
(simnibs_env)$python3 01_reorient2std.py
```

- Run all further scripts in this way

3. For headreconstruction run script [02_run_headreco_chpath.py](02_run_headreco_chpath.py)
4. Check if haedreconstruction was successfully run [03_headreco_check_sub.py](03_headreco_check_sub.py)
5. Start SimNIBS simulation
   1. Run [04_simulation_coregist.py](04_simulation_coregist.py)
   - Note, script was modified from [SimNIBS tutorial](https://simnibs.github.io/simnibs/build/html/tutorial/scripting.html) 
   - Note that 2 windows will pop up and request info. You have to choose: 
     1. The Experiment (VerFlu_HI, VerFlu_HM, VerFlu_TI, VerFlu_TM) 
     2. The Session (Kopf, Zahl)
     - Run all sessions for all experiments to get full data
     - In the scripts you will find all parameters, coordinates etc. you need
   1. Because planned HD-tDCS electrodes needed to be transformed into subject space and created automatically, a [SimNIBS function was customized](SimNIBS_enhanced/Readout_E_fields_roi_and_mask.py)
   - Run script [04_simulation_coregist_individual_radius.py](04_simulation_coregist_individual_radius.py)
  
6. To get all needed E-field values run the script [05_Analysis_Function_ROI.py](05_Analysis_Function_ROI.py)
    - Data will be written in the "Source_Data" folder 
7. To get all mni coordinates to subject coordinates, run [05_b_save_mni2subj_coordinates.py](05_b_save_mni2subj_coordinates.py)

8. To get mean values and images for Figure 3 and Figure S5 run script
   1.  For actual electrode position script  [06_rois_analysis_fsaverage.py](06_rois_analysis_fsaverage.py)
   2.  For planned electrode position [06_rois_analysis_fsaverage_optimal.py](06_rois_analysis_fsaverage_optimal.py)
   
9.  To get montage images for Figure S1-S4 and Figure 3
    1.  For actual electrode position run  [07_rois_plot_actual_coordinate_montage.py](07_rois_plot_actual_coordinate_montage.py)
    2.  For optimal electrode position run [07_rois_plot_optimal_coordinate_montage.py](07_rois_plot_optimal_coordinate_montage.py)
    3.  For Region of interest in Figure 3 [07_rois_plot_spheres.py](07_rois_plot_spheres.py)

## [Next step, analysis of electrode differences](../03_Analysis_Electrode_Difference/README.md)
