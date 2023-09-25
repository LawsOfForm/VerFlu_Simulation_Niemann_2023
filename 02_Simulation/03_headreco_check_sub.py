#Issue: Run head reconstruction check  
#Author: Filip Niemann & Steffen Riemann
#Date: 21.09.2023

import os
import subprocess
import pathmanager
from simnibs.msh import headreco

vps = os.listdir(pathmanager.BASEDIRECTORY)
vps = [vp for vp in vps if vp != "code"]

vps.sort()

for vp in vps:
    print(vp)
    try:
    
        if not os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.KOPF,f"m2m_{vp}", "head_contr.fsmesh")):
            raw=os.path.join(pathmanager.BASEDIRECTORY, vp, pathmanager.KOPF)
            os.chdir(raw)   #change directory to
            #subprocess.run(["headreco", "check", f"{vp}"]) #headreco check simnibs
            headreco.headmodel(['headreco','check',f'{vp}'])
            #subprocess.call('ls', shell=True, cwd='path/to/wanted/dir/')
            #subprocess.call('headreco check ', shell=True, cwd=raw)
            print(f"{vp} headreco check done Kopf")
    except:
        print("Fehler")
        
    try:
        if not os.path.isfile(os.path.join(pathmanager.BASEDIRECTORY, vp ,pathmanager.ZAHL,f"m2m_{vp}", "head_contr.fsmesh")):
            raw=os.path.join(pathmanager.BASEDIRECTORY, vp, pathmanager.ZAHL)
            os.chdir(raw)  #change directory to
            #subprocess.run(["headreco", "check", f"{vp}"]) #headreco check simnibs
            headreco.headmodel(['headreco','check',f'{vp}'])
            print(f"{vp} headreco check done Zahl")
    except:
        print("Fehler")
        
    
   
