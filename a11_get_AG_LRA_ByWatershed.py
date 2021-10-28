"""  
Created on thu oct 28 17:39:00 2021

this script gets only AG and LRA use class wells 
to use them for irrigation module on MIKE-SHE as 
external sources

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
                        "concat_refinedWells\\wells_ag_lra_ByWatrshd"

os.chdir(dirHome)

dat = pd.read_csv("allWells_with_watershed_v2.csv")

dat.drop(['Unnamed: 0'], axis = 1, inplace = True)

print(dat)

print(dat['use_class'].unique())


for ws in dat['watershed'].unique():
    print(ws)
    currentWells = dat[(dat['watershed'] == ws) & 
                       (dat['use_class'].isin(['AG', 'LRA']))]
    
    os.chdir(dirOut)
    currentWells.to_csv(ws+".csv")