"""  
Created on Thu Sep 23 16:13:00 2021
modified on Wed Oct 06 18:03:00 2021

prepare dfs0 withdrawal files with the 
units, types and datatypes included - but for pumping rate

@author: Michael Getachew Tadesse

"""

import os
from datetime import datetime
from mikecore.DfsFile import DataValueType
from mikeio import Dfs0, Dataset
from mikeio.eum import ItemInfo, EUMType, EUMUnit
import pandas as pd 
from mikeio import Dfs0

dirHome = "C:\\Users\\mtadesse\\Hazen and Sawyer\\"\
    "MIKE_Modeling_Group - Documents\\ECFTX\\"\
            "extractedWellData\\07-staticFile\\wellsByWS4Dfs0"

dirOut = "C:\\Users\\mtadesse\\Hazen and Sawyer\\"\
    "MIKE_Modeling_Group - Documents\\ECFTX\\"\
            "extractedWellData\\07-staticFile\\wellsByWS4Dfs0_pumpingRate"


os.chdir(dirHome)


# loop through watersheds
wsList = os.listdir()

for ws in wsList:
    os.chdir(dirHome)

    print(ws)

    dat = pd.read_csv(ws)
    dat.drop('Unnamed: 0', axis = 1, inplace = True)
    
    print(dat)

    # organize the columns by changing them to arrays
    # but based on columns 
    # for the withdrawals - for now use "water volume"

    df = []
    items = []
    for ii in range(1,dat.shape[1]):
        df.append(dat.iloc[:,ii].to_numpy())
        
        ###########################################################
        # make final decision here for EUMUnit *** 
        ###########################################################

        items.append(ItemInfo(dat.columns[ii], EUMType.Pumping_Rate, 
                                EUMUnit.feet_pow_3_per_day, 
                                    data_value_type= DataValueType.MeanStepBackward))

    # generate monthly time from 12/2003 to 12/2014
    datTime = pd.date_range(start='12/1/2003', end='12/31/2014', freq='MS')    

    '''  
    # writing dataframe to dfs0
    # use pumping rate for withdrawal
    # use meanstepBackward for mean step accumulated

    '''
    ds = Dataset(data = df, time = datTime, items = items)
    print(ds)


    # write the dfs0 file
    
    os.chdir(dirOut)
    
    dfs = Dfs0()

    dfs.write(filename= ws.split(".csv")[0] + ".dfs0", 
            data=ds,
            title="monthly_withdrawal_volume_mg")