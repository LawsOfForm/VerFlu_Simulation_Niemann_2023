import os
import subprocess
import pathmanager

vps = os.listdir(pathmanager.BASEDIRECTORY)
vps = [vp for vp in vps if vp != "code"]

vps.sort()
#fslreorient2std is a tool for reorienting the image to match theapproximate orientation of the standard template images (MNI152)

for vp in vps[:]:
    print(vp)
    if not os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.KOPF, f"r{vp}_ses-Kopf_T1w.nii.gz")):
        raw = os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.KOPF, f"{vp}_ses-Kopf_T1w.nii")
        reoriented = os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.KOPF, f"r{vp}_ses-Kopf_T1w.nii")
        subprocess.run(["fslreorient2std", raw, reoriented]) #fslreorient2std $dir/$subjects/T1w.nii $dir/$subjects/rT1w.nii
        print("Kopf T1 reorientiert.")
    if not os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.KOPF, f"r{vp}_ses-Kopf_T2w.nii.gz")):
        raw = os.path.join(pathmanager.BASEDIRECTORY, vp, pathmanager.KOPF, f"{vp}_ses-Kopf_T2w.nii")
        reoriented = os.path.join(pathmanager.BASEDIRECTORY, vp, pathmanager.KOPF, f"r{vp}_ses-Kopf_T2w.nii")
        subprocess.run(["fslreorient2std", raw, reoriented]) #fslreorient2std $dir/$subjects/T1w.nii $dir/$subjects/rT1w.nii
        print("Kopf T2 reorientiert.")
    if not os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.ZAHL, f"r{vp}_ses-Zahl_T1w.nii.gz")):
        raw = os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.ZAHL, f"{vp}_ses-Zahl_T1w.nii")
        reoriented = os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.ZAHL, f"r{vp}_ses-Zahl_T1w.nii")
        subprocess.run(["fslreorient2std", raw, reoriented]) #fslreorient2std $dir/$subjects/T1w.nii $dir/$subjects/rT1w.nii
        print("Zahl T1 reoirentiert.")
    if not os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.ZAHL, f"r{vp}_ses-Zahl_T2w.nii.gz")):
        raw = os.path.join(pathmanager.BASEDIRECTORY, vp, pathmanager.ZAHL, f"{vp}_ses-Zahl_T2w.nii")
        reoriented = os.path.join(pathmanager.BASEDIRECTORY, vp, pathmanager.ZAHL, f"r{vp}_ses-Zahl_T2w.nii")
        subprocess.run(["fslreorient2std", raw, reoriented]) #fslreorient2std $dir/$subjects/T1w.nii $dir/$subjects/rT1w.nii
        print("Zahl T2 reorientiert")
