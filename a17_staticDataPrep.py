"""
Created on Wed Aug 26 07:40:00 2021
modified on mon nov 01 15:36:00 2021

this program:
*prepares the static file for the wells

@author: Michael Getachew Tadesse

"""
import os
import pandas as pd

dirHome = "C:\\Users\\mtadesse\\Hazen and Sawyer\\"\
        "MIKE_Modeling_Group - Documents\\ECFTX\\extractedWellData\\"\
                "011-allECFTXPermits-county-useclass\\analysis\\concat_refinedWells"
dirDfs0 = "C:\\Users\\mtadesse\\Hazen and Sawyer\\MIKE_Modeling_Group - Documents\\"\
        "ECFTX\\extractedWellData\\011-allECFTXPermits-county-useclass\\analysis\\"\
                "concat_refinedWells\\allUseClassWells4Dfs0"
dirOut = "C:\\Users\\mtadesse\\Hazen and Sawyer\\"\
        "MIKE_Modeling_Group - Documents\\ECFTX\\extractedWellData\\"\
                "011-allECFTXPermits-county-useclass\\analysis\\"\
                        "concat_refinedWells\\staticFile"

os.chdir(dirHome)

# all wells data
datWells = pd.read_csv("allWells_with_watershed_v2.csv")
datWells.drop('Unnamed: 0', axis = 1, inplace = True)

# changing layer column to string (to account for wells traversing many layers)
datWells['layer'] = datWells['layer'].astype(str)

print(datWells)
print(datWells.columns)

print(datWells['layer'].unique())

# all layers top/bottom data - Rama Rani provided this file
datInfo = pd.read_csv("ECFTX_allRC_layersTopBot.csv")


# get unique wells/rcps
rcpUnique = datWells['id'].unique()

# create empty dataframe
df = pd.DataFrame(columns = ['wellID', 'x', 'y', 'level', 'depth', 
     'wellField', 'top', 'bottom',  'fraction', 'dfs0File', 'dfs0Item'])

# defining top and bottom of layers
layerDict = {
    '1' : ['L01_top_ft', 'L02_top_ft'],
    '3' : ['L03_top_ft', 'L04_top_ft'],
    '4' : ['L04_top_ft', 'L05_top_ft'],
    '5' : ['L05_top_ft', 'L06_top_ft'],
    '7' : ['L07_top_ft', 'L08_top_ft'],
    '9' : ['L09_top_ft', 'L10_top_ft'],
    '3_4' : ['L03_top_ft', 'L05_top_ft'],
    '3_4_5' : ['L03_top_ft', 'L06_top_ft'],
    '4_5' : ['L04_top_ft', 'L06_top_ft'],
    '7_8_9' : ['L07_top_ft', 'L10_top_ft'],
    '3_4_5_7_8_9' : ['L03_top_ft', 'L10_top_ft'],
}


for rcp in rcpUnique:
    print(rcp)

    rowcol = '_'.join([rcp.split("_")[0], rcp.split("_")[1]])
    
    wellID = rcp
    
    x = datWells[datWells['id'] == rcp]['x_utm_m'].unique()[0]
    y = datWells[datWells['id'] == rcp]['y_utm_m'].unique()[0]
    
    # using the L01 top elevation as level
    level = datInfo[datInfo['ROWCOL'] == rowcol]['L01_top_ft'].unique()[0]
    wellField = rcp
    
    # figure out top and bottom
    rcpLayer = datWells[datWells['id'] == rcp]['layer'].unique()[0]

    t, b = layerDict[str(rcpLayer)]
    
    # print(t, "-", b)
    
    top = datInfo[datInfo['ROWCOL'] == rowcol][t].values[0]
    bottom = datInfo[datInfo['ROWCOL'] == rowcol][b].values[0]
    depth = level - bottom
    
    fraction = 1.0
   
    dfs0File = ''.join(datWells[datWells['id'] \
                    == rcp]['watershed'].unique()[0])
    
    
    # get the dfs0 item number corresponding to each watershed - from alluseclass
    os.chdir(dirDfs0)
    datDfs0 = pd.read_csv(dfs0File+".csv")
    
    datDfs0.drop('Unnamed: 0', axis = 1, inplace = True)
    
    dfs0Item = list(datDfs0.columns).index(rcp)


    newDf = pd.DataFrame([wellID, x, y, level, depth, wellField, top, 
        bottom,  fraction, dfs0File, dfs0Item]).T 
    newDf.columns = ['wellID', 'x', 'y', 'level', 'depth', 
     'wellField', 'top', 'bottom', 'fraction', 'dfs0File', 'dfs0Item']

    # add to empty dataframe
    df = pd.concat([df, newDf], axis = 0)

# save as csv
os.chdir(dirOut)
df.to_csv('staticWellFileByWS_4WellEditor.csv', 
            sep='\t', index = False,  header=False)

