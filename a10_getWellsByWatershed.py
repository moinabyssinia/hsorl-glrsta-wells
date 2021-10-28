"""  
Created on tue Sep 28 17:04:00 2021
modified on thu oct 28 17:39:00 2021

this script gets the wells based on the watersheds
to later prepare them for dfs0 files 

using the latest 'allWells_with_watershed_v2.csv' file

@author: Michael Getachew Tadesse

"""

import os 
import pandas as pd

dirHome = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
        "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\analysis\\"\
                        "concat_refinedWells"
dirOut = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
        "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\analysis\\"\
                        "concat_refinedWells\\wellsByWatrshd"

os.chdir(dirHome)

dat = pd.read_csv("allWells_with_watershed_v2.csv")

dat.drop(['Unnamed: 0'], axis = 1, inplace = True)

print(dat)


for ws in dat['watershed'].unique():
    print(ws)
    currentWells = dat[dat['watershed'] == ws]
    
    os.chdir(dirOut)
    currentWells.to_csv(ws+".csv")