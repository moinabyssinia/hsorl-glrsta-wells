"""
Created on Wed Aug 25 07:30:00 2021
modified on tue oct 26 17:48:00 2021

this program:
*separates the wells that cut through multiple layers 
saves them separately

@author: Michael Getachew Tadesse

"""
import os 
import pandas as pd
import datetime as dt

dirHome = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
        "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\analysis\\rawFile"
dirOut = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
        "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\analysis\\wellMultipleLayers"


os.chdir(dirHome)


# read raw data
dat = pd.read_csv("ecftx_clipped_v4.txt")
dat.drop(['FID', 'field_1'], axis = 1, inplace = True)

# replace "AVE" with "DEC"
dat['mon'] = dat['mon'].str.replace('AVE', 'DEC')

# concatenate mon and year
removeExt = lambda x: str(x).split('.0')[0]
dat['year'] = pd.DataFrame(list(map(removeExt, dat['year'])))
dat['date'] = pd.DataFrame(pd.to_datetime(dat['year'].astype(str) + dat['mon'].astype(str), 
                                             format = "%Y%b"))
# concatenate row-columns-name
dat['id'] = dat.row.astype(str).str.cat(dat['columns'].astype(str), sep = "_") + "_" + dat['name']


datAll = dat[['id', 'name', 'date', 'mon', 'year', 'x_utm_m', 'y_utm_m', 'layer', 
              'row', 'columns', 'county', 'use_class', 'withdrawal']]
dat = dat[['id',  'date', 'x_utm_m', 'y_utm_m', 'layer', 'county', 'use_class', 'withdrawal']]

# datAll.to_csv('ecftx_clipped_v4_extended.csv')
# dat.to_csv('ecftx_clipped_v4_short.csv')

print(dat)



layers = dat['layer'].unique()
monYear = dat['date'].unique()

print(layers)
print(monYear)

# loop through each monYear
for my in monYear:
    os.chdir(dirHome)
    print(my)
    
    currentDat = dat[dat['date'] == my]

    # fetch wells that traverse layers - all of them not skipping first     
    repWells = currentDat[currentDat['id'].duplicated(keep = False)]
    # print(repWells)

    # drop repWells from original dataframe
    dat.drop(repWells.index, axis = 0, inplace = True)


    # save as csv
    os.chdir(dirOut)
    repWells.to_csv(str(my).split('-01T00:00:00.000000000')[0] + ".csv")

# save truncated dat
os.chdir(dirHome)

# reverse the negative sign for the data where the repWells are removed
dat['withdrawal'] = dat['withdrawal'] * -1
 
dat.to_csv("ecftx_clipped_v4_removedRepWells.csv")
