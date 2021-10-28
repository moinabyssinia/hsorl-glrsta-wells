"""
Created on Wed Aug 25 15:31:00 2021

this program:
*concatenates the individual refinedWells 

@author: Michael Getachew Tadesse

"""

import os
import numpy as np
import pandas as pd

dirHome = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
        "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\analysis\\"\
                "refinedWellMultipleLayers"
dirOut = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
        "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\analysis\\"\
                "concat_refinedWells"
dirConcat = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
        "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\analysis\\"\
                "rawFile"
        
os.chdir(dirHome)

wellList = os.listdir()

# create empty dataframe
df = pd.DataFrame(columns = ['Unnamed: 0', 'id', 'date', 'x_utm_m', 'y_utm_m', 'layer', 
                                 'county', 'use_class', 'withdrawal'])

for well in wellList:
    print(well)
    newDf = pd.read_csv(well)
    # print(newDf)

    df = pd.concat([df, newDf], axis = 0)

df.reset_index(inplace = True)
df.drop(['Unnamed: 0', 'index'], axis = 1, inplace = True)

# print(df.columns)

# save concatenated well data
os.chdir(dirOut)
df.to_csv("refinedWellsConcat.csv")


# open "ecftx_clipped_v4_removedRepWells.csv" and add it
os.chdir(dirConcat)
newDat = pd.read_csv("ecftx_clipped_v4_removedRepWells.csv") 
newDat.reset_index(inplace = True)
newDat.drop(['Unnamed: 0', 'index'], axis = 1, inplace = True)

print(newDat)

# add the refined wells
allWells = pd.concat([newDat, df], axis = 0)

print(allWells)

allWells.to_csv("ecftx_clipped_v4_removedRepWells_with_traversingWells.csv")
