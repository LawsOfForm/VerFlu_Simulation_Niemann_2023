#Issue: Run SimNIBS head reconstruction for subjects of given experiment   
#Author: Filip Niemann & Steffen Riemann
#Date: 21.09.2023


from simnibs.msh import headreco
import os
import pathmanager

#if script is not running start /reorient2std.py script first
#beware that the script runs for specific subjects

#define function for headreconstruction
def reco (subject, T1, T2, cwd):
    os.chdir (os.path.join(cwd))
    T1_true = os.path.isfile(T1)
    T2_true = os.path.isfile(T2)
    try:   
        if (T1_true and T2_true):   #try to run simulation with T1 and T2
            headreco.headmodel(['headreco','all','--cat',subject,T1,T2]) #use cat for segmentation
        elif T1_true:    # use only T1 if T2 not available
            headreco.headmodel(['headreco','all','--cat',subject,T1])
    except RuntimeError:
        old = f'm2m_{subject}'
        new = f'm2m_{subject}_failed'
        count = 1
        new2 = new
        while os.path.exists(new2):
            new2 = f'{new}_{count}'
            count+=1
        os.rename(old, new2)
        if (T1_true and T2_true):
            headreco.headmodel(['headreco','all','--cat','-v=1',subject,T1,T2])
        elif T1_true:
           headreco.headmodel(['headreco','all','--cat','-v=1',subject,T1])

# write all subject path in list        
vps = os.listdir(pathmanager.BASEDIRECTORY)
vps = [vp for vp in vps if vp != "code"]  # ignore "code" folder but noth subject folders

vps.sort()

#loop through all subjects processing headreconstruction
for vp in vps[0:len(vps)]:
    #For Session Kopf (Sham or Stimulation)
    if not os.path.isdir(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.KOPF, f"m2m_{vp}")) and os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.KOPF,f'r{vp}_ses-Kopf_T1w.nii.gz')):

        cwd = os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.KOPF)
        
        T1 = f"r{vp}_ses-Kopf_T1w.nii.gz"
        T2 = f"r{vp}_ses-Kopf_T2w.nii.gz"

        reco (vp,T1,T2,cwd)

    elif os.path.isdir(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.KOPF,f'm2m_{vp}')):
        print(f'{vp} ready for simulations' )
    else:
        print(f'something wrong for {vp} Kopf')
        print(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.KOPF,f'm2m_{vp}'))

for vp in vps[0:len(vps)]:
    #For Session Zahl (Sham or Stimulation)
    if not os.path.isdir(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.ZAHL, f"m2m_{vp}")) and os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.ZAHL,f'r{vp}_ses-Zahl_T1w.nii.gz')):
        
        cwd = os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.ZAHL)
        T1 = f"r{vp}_ses-Zahl_T1w.nii.gz" #
        T2 = f"r{vp}_ses-Zahl_T2w.nii.gz" #

        reco (vp,T1,T2,cwd)


    elif os.path.isdir(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.ZAHL,f'm2m_{vp}')):
        print(f'{vp} ready for simulations' )
    else:
        print(f'something wrong for {vp} Zahl')
        print(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.ZAHL,f'm2m_{vp}'))
        print(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.ZAHL,f'r{vp}_ses-Zahl_T1w.nii.gz'))


