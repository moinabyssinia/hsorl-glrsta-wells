"""  
Created on Wed Sep 30 17:46:00 2021
modified on fri oct 29 17:09:00 2021

prepare the withdrawal csvs to get total monthly withdrwal volume
summed up per watershed

@author: Michael Getachew Tadesse

"""

import os 
import pandas as pd 

dirHome = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
                "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\"\
                                "analysis\\concat_refinedWells\\"\
                                                "watervolume-ag_lra_useclass"

dirOut = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
                "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\"\
                                "analysis\\concat_refinedWells\\"\
                                                "external_ag_lra_useclass"

os.chdir(dirHome)

for wellDat in os.listdir():
    
    os.chdir(dirHome)

    print(wellDat)
    
    dat = pd.read_csv(wellDat)
            
    dat['monthly_WS_Withdrawal_volume_mg'] = dat.iloc[:,2:].sum(axis = 1)
    
    os.chdir(dirOut)
    
    dat[['date', 'monthly_WS_Withdrawal_volume_mg']].to_csv(wellDat)



