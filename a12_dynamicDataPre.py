"""
Created on Wed Aug 25 18:29:00 2021
modified on thu oct 28 18:28:00 2021

this program:
*filters the withdrawal time series for each rowColPermit and
 prepares it on a format that is needed for dfs0

@author: Michael Getachew Tadesse

"""
import os
import pandas as pd

# change directory here to 'wellsByWatrshd' or 'wells_ag_lra_ByWatrshd'

dirHome = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
        "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\analysis\\"\
                        "concat_refinedWells\\wells_ag_lra_ByWatrshd"
dirOut = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
        "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\analysis\\"\
                        "concat_refinedWells\\ag_lra_UseClassWells4Dfs0"


os.chdir(dirHome)

wsList = os.listdir()

for ws in wsList:
    os.chdir(dirHome)

    print(ws)

    dat = pd.read_csv(ws)
    dat.drop('Unnamed: 0', axis = 1, inplace = True)
    
    # modify month and year format
    dat['date'] = pd.to_datetime(dat['date'])

    print(dat[['date', 'id', 'withdrawal']])
    
    #################################################
    # convert cubic feet/day to gallon/day
    # withdrawal is in cfd; 1 cf = 7.48052 gallon
    dat['withdrawal_gal'] = dat['withdrawal']*7.48052
    #################################################

    rcpUnique = dat['id'].unique()
    # print(rcpUnique)


    dfs0File = pd.DataFrame(dat['date'].unique())
    dfs0File.columns = ['date']

    for rcp in rcpUnique:
        df = dat[dat['id'] == rcp]
        newDf = df[['date', 'withdrawal_gal']] # take the gallon/day data
        newDf.columns = ['date', rcp]
        # print(newDf)

        # merge to rcpUnique
        dfs0File = pd.merge(dfs0File, newDf, on="date", how="left")

    print(dfs0File)

    # save county dfs0 ready csv
    os.chdir(dirOut)
    dfs0File.to_csv(ws)