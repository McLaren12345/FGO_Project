# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 18:59:06 2019

@author: McLaren
"""

import pandas as pd
import sys
sys.path.append(r'F:\FGO_Project')
import FGO_func

df = pd.read_csv('F:/FGO_Project/Config/Config.csv')

df1 = df[df['Turn']==1]
df2 = df[df['Turn']==2].reset_index(drop=True)
df3 = df[df['Turn']==3].reset_index(drop=True)

def Config2Command(df):
    for i in range(df['Turn'].count()):
        if df.loc[i,'Command']=='Character_skill':
            if df['Para3'].isna()[i]:
                FGO_func.character_skill(df.loc[i,'Para1'],df.loc[i,'Para2'])
            else:
                FGO_func.character_skill(df.loc[i,'Para1'],df.loc[i,'Para2'],df.loc[i,'Para3'])
                
        if df.loc[i,'Command']=='Master_skill':
            if df['Para2'].isna()[i]:
                Para2 = 3
            else:
                Para2 = df.loc[i,'Para2']
            if df['Para3'].isna()[i]:
                Para3 = 2
            else:
                Para3 = df.loc[i,'Para3']
            FGO_func.Master_skill(df.loc[i,'Para1'],Para2,Para3)
            
        if df.loc[i,'Command']=='Card':
            FGO_func.card(df.loc[i,'Para1'])


