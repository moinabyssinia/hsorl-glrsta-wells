"""
Created on Wed Aug 25 08:12:00 2021
modified on wed oct 27 15:42:00 2021 

this program:
*organizes the multiple wells in such a way that
 the withdrawal is summed up and sign reveresed and 
 layers cut through are marked 

@author: Michael Getachew Tadesse

"""

import os
import numpy as np
import pandas as pd

dirHome = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
        "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\analysis\\"\
                "wellMultipleLayers"
dirOut = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
        "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\analysis\\"\
                "refinedWellMultipleLayers"

os.chdir(dirHome)
monYear = os.listdir()

for my in monYear:
    os.chdir(dirHome)

    print(my)
    dat = pd.read_csv(my)
    
    dat.drop('Unnamed: 0', axis = 1, inplace = True)
    
    # get unique rowcolPermit
    rowColPermit = dat['id'].unique()

    # create empty dataframe - for trend computation 
    df = pd.DataFrame(columns = ['id', 'date', 'x_utm_m', 'y_utm_m', 'layer', 
                                 'county', 'use_class', 'withdrawal'])

    # loop through unique rowcols
    for rcp in rowColPermit:
        currentDat = dat[dat['id'] == rcp]
        
        layer = currentDat['layer'].unique()
        layerStr = [str(i) for i in layer]
        layerStrJoin = "_".join(layerStr)

        # sum up withdrawal - reverse sign
        withdrawalSum = -1 * np.sum(currentDat['withdrawal'].tolist())

        newDf = pd.DataFrame([
            
                currentDat['id'].unique()[0], currentDat['date'].unique()[0],
                currentDat['x_utm_m'].unique()[0], currentDat['y_utm_m'].unique()[0],
                layerStrJoin, currentDat['county'].unique()[0],
                currentDat['use_class'].unique()[0], withdrawalSum
                
            ]).T

        newDf.columns = ['id', 'date', 'x_utm_m', 'y_utm_m', 'layer', 
                                 'county', 'use_class', 'withdrawal']
        df = pd.concat([df, newDf], axis = 0)


    # save as csv
    os.chdir(dirOut)
    df.to_csv(my)
    