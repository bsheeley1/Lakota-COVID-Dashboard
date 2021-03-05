# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 14:34:47 2021

@author: bbshe
"""
import pandas as pd
import numpy as np
import os 

data = pd.read_csv('OLC_covid_data.csv')
d = {'Date': [0], 'Confirmed Cases': [1], 'Deaths': [2]}
dataf = pd.DataFrame(data=d)
column_names = ['Date', "Confirmed Cases", 'Deaths']
df = pd.read_csv('OLC_covid_data.csv', names = column_names)
df.reset_index(drop=True)
df.dropna()
newdf = df.dropna()
newdf.to_string()


print(df)
with open("OLC_covid_data.csv", "r") as file:
    
    text = file.readlines()
    line = text[0].split()
    #dates = collum.split(',')[:] #acquire dates
    for x in text:
        if 'Oglala Lakota County' in x.split(','): #search only in Oglala Lakota County
            confirmed_cases = x.split()
            confirmed_cases = confirmed_cases[2].split(',')
            confirmed_cases = confirmed_cases[3:] #Grab the number of confirmed cases