# VerFlu_Simulation_Niemann_2023

# Help Preprocessing script

## Preprocessing

1. Change the path of the script [start_conn_script.sh](01_Preprocessing/start_conn_script.sh)
2. If MRI data are available (only after request, due to data privacy reasons) and not preprocessed, copy the "start_conn_script.sh" in every subjects ses-Kopf and ses-Zahl folder, if not already done
3. Run the preprocessing script via bash

```{bash}
./start_conn_script.sh
```

## Coregistration

- In the anat folder of the data 2 T1 images are given
  
  1. sub-01_ses-Kopf_electrodes_T1w.nii (data example, T1 with electrodes on head)
  2. sub-01_ses-Kopf_T1w.nii (data example, T1 without electrodes)
- Coregister the second image to the first one (use spm or other tools to do that; [help coregistration](https://andysbrainbook.readthedocs.io/en/stable/SPM/SPM_Short_Course/SPM_04_Preprocessing/03_SPM_Coregistration.html))  

- Use only coregistrated images for Simnibs simulation [Next step 02_Simulation](../02_Simulation/README.md)