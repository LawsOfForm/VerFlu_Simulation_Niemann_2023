# VerFlu_Simulation_Niemann_2023
Git repository for the paper; Electrode positioning errors reduce current dose in target brain regions for focal but not conventional tDCS: Evidence from individualized electric field mapping.

## Electrode positioning errors reduce current dose in target brain regions for focal but not conventional tDCS: Evidence from individualized electric field mapping
Author List:
Filip Niemann, Steffen Riemann, Ann-Kathrin Hubert, Daria Antonenko, Axel Thielscher, Andrew K. Martin, Nina Unger, Agnes Flöel, Marcus Meinzer

### Data and Code Availability

 The data are not publicly available due to potential identifying information that could compromise participant privacy. Source data are provided for each script located in the 00_Source_Data folder and can be viewed using the appropriate script (in R the View(df) option)

All analyses were performed using the available toolboxes: [Anaconda 3.2.31](https://anaconda.org/), [Python 3.7.13](https://www.python.org/), [R version 4.3.1](https://www.r-project.org/), [MATLAB R2021b](https://www.mathworks.com), [SPM12](https://www.fil.ion.ucl.ac.uk/spm/software/spm12/), [CONN 20.b](https://web.conn-toolbox.org), [Cat](https://neuro-jena.github.io/cat/), [BrainNetViewer 1.7](https://www.nitrc.org/projects/bnv/), [SimNIBS 3.2.6](https://simnibs.github.io/simnibs/build/html/index.html), [FreeSurfer Version 7.4.1](https://surfer.nmr.mgh.harvard.edu), [FSL 6.0.0](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/) and [gmsh](https://gmsh.info/) Costumized codes are available within the respository.

### Statistical Analyses and Source Data

For transparency and in order to reconstruct/ replicate our results, we uploaded all R scripts and needed source data for all major analyses.

1. Coordinates differences between planned and actual coordinates reproducible with the LMM_Coordinates.Rmd script, in the "03_Analysis_Electrode_Difference" folder.
2. Comparison of magnitude E-field values for all Areas (IFG, M1), Montages (conventional, focal), ROI radius (1.25 mm, 2.5 mm), and electrode position (planned, actual), reproducible with the LMM_magnitude_E-field.Rmd script; in the "04_Analysis_Analysis_Simulated_E-fields/01_magnitude_E-field" folder.
3. Comparison of the positive normal component of the E-field values for all Areas (IFG, M1), Montages (conventional, focal), ROI radius (1.25 mm, 2.5 mm), and electrode position (planned, actual), reproducible with the LMM_nE-field.Rmd script; in the "04_Analysis_Analysis_Simulated_E-fields/02_normal_component_E-field" folder.

All scripts automatically access the associated source data when the repository is cloned and if the downloaded folder structure is not changed.
For further details see descriptions in the scripts.

To run the R markdown script, you need to:

- install [R](https://www.r-project.org)
- install the required packages to run the analysis (can be found in the first lines of the R script)
- download the data and run the script

To run the Python and Jupyter Notebook scripts, you need to:

- install [python](https://anaconda.org/)
- [create and activate a virtual environment with YAML](https://saturncloud.io/blog/how-to-create-a-conda-environment-based-on-a-yaml-file-a-guide-for-data-scientists/)
- download the data and run the script

### MRI Analyses and E-filed simulations

1. - No non-standard hardware is required.
2. - Installation instructions are available on the respective homepages:
[Anaconda](https://docs.anaconda.com/free/anaconda/install/index.html)
[Python install via conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-python.html)
[Matlab](https://de.mathworks.com/help/install/install-products.html)
[SPM](https://en.wikibooks.org/wiki/SPM/Installation_on_Windows#Installation)
[Cat](https://andysbrainbook.readthedocs.io/en/latest/CAT12/CAT12_01_DownloadInstall.html)
[BrainNetViewer 1.7](https://www.nitrc.org/docman/view.php/504/1280/BrainNet)
[FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation)
[Freesurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/ReleaseNotes)
[CONN](https://web.conn-toolbox.org)
[SimNIBS 3.2.6](https://github.com/simnibs/simnibs/releases)
[SimNIBS 3.2.6 install via conda](https://simnibs.github.io/simnibs/build/html/installation/conda.html)
[gmsh](https://gmsh.info/#Download)

1. - We provide the Python codes and a short introduction for  

- Preprocessing of the MRI data, [find details here](01_Preprocessing/README.md)
- Simulation of the E-fields with SimNIBS, [find details here](02_Simulation/README.md)
- Note: for [conda environments](https://saturncloud.io/blog/how-to-create-a-conda-environment-based-on-a-yaml-file-a-guide-for-data-scientists/) YAML files (*.yml) are provided containing all neccessary packages for [02_Simulation](02_Simulation/simnibs_env.yml) and Python scripts in th folder for coordinate differences [03_ANalysis_Electrode_Difference](03_Analysis_Electrode_Difference/Get_Figures_S1-S4.yml)

## Focality Analysis

- Focality analysis script and data are provided in "05_Focality_Analysis"
- data from

##  Comparison neuronavigate and non neuronavigated electrode placement

- Focality analysis script and data are provided in "06_Comparison_Electrode_Placement_Error"



## 3D printed templates
- template ideas from Filip Niemann (university medicine greifswald) and Robert Malinowski (university medicine greifswald)
- in folder "07_3D_print_templates" 3D templates for the spacer an the fillaid are stored
  - "07_3D_print_templates/Fillaid" contains the printable "Fillaid.stl" and the modifiable "Fillaid.3mf" and "Fillaid.f3d" files.
  - "07_3D_print_templates/Spacer" contains the printable "Spacer.stl" and the modifiable "Spacer.3mf" and "Spacer.f3d" files.
