# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 15:29:21 2020

@author: Jharp
"""

#Modules and Libraries

#Dash Modules for Dashboard in Browser
import dash
import dash_core_components as dcc
import dash_html_components as html

#Matplotlib for plotting graphs and charts
#Numpy for mathematical operations
#Datetime for date formatting
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

#Format of dates given as month-year for x axis
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%m-%y') #how the date will appear on the x axis

#Declaration of dictionaries regarding each death and each case corresponding to the dates
death_dict = dict()
cases_dict = dict()


#Open the first file holding death amount per day
with open("covid_deaths_usafacts.csv", "r") as file:
    text = file.readlines()
    line = text[0].split()
    dates = line[1].split(',')[3:] #acquire the dates
    for x in text:
        if 'Oglala Lakota County' in x.split(','): #search only in Oglala Lakota County
            death_toll = x.split()
            death_toll = death_toll[2].split(',')
            death_toll = death_toll[3:] #Grab all the number of deaths

#reformat death number from string to integer
death_toll = [int(i) for i in death_toll]

#format dates to add year number
dates = [d + '20' for d in dates]

#obtain the change in death number and populate dictionary of dates:deaths
placeholder = 0 #number of deaths starts in 0
for x in range(len(death_toll)):
    #If we reach a date where death toll changes, update the threshold amount
    if placeholder != death_toll[x]: 
        placeholder = death_toll[x]
        death_dict[dates[x]] = death_toll[x]

#Format dates to be changed to datetime data type
dates1 = [datetime.datetime.strptime(d,"%m/%d/%Y").date() for d in dates]

#Create 4 plots in a [2,2] matrix format
#First plot will contain Cumulative death count in Oglala Lakota County
fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2) #Create plots
plt.subplots_adjust(bottom=3, right=3, top=3.5) #adjust distance between each
ax1.plot(dates1,death_toll) #plot 1
ax1.xaxis.set_tick_params(which='both', labelbottom=True) #x axis ticks appear

#Format x axis ticks so that we show only certain x axis data
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)
ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

#Show data from first date month to the last date month plus 1 month
datemin = np.datetime64(dates1[0], 'M')
datemax = np.datetime64(dates1[-1], 'M') + np.timedelta64(1, 'M')
ax1.set_xlim(datemin, datemax)

#format plot and title
ax1.format_xdata = mdates.DateFormatter('%Y-%m-%d')
ax1.grid(True)
ax1.set_title('Cumulative Death Count in Oglala Lakota County')


#Open the second file holding confirmed cases amount per day
with open("covid_confirmed_usafacts.csv", "r") as file:
    text = file.readlines()
    line = text[0].split()
    dates = line[1].split(',')[3:] #acquire dates
    for x in text:
        if 'Oglala Lakota County' in x.split(','): #search only in Oglala Lakota County
            confirmed_cases = x.split()
            confirmed_cases = confirmed_cases[2].split(',')
            confirmed_cases = confirmed_cases[3:] #Grab the number of confirmed cases

#reformat confirmed cases number from string to integer
confirmed_cases = [int(i) for i in confirmed_cases]

#obtain the change in death number and populate dictionary of dates:deaths
placeholder = 0 #number of confirmed cases starts in 0
for x in range(len(confirmed_cases)):
    #If we reach a date where confirmed caes toll changes, update the threshold amount
    if placeholder != confirmed_cases[x]:
        placeholder = confirmed_cases[x]
        cases_dict[dates[x]] = confirmed_cases[x]

#format dates to add year number
dates = [d + '20' for d in dates]
#Format dates to be changed to datetime data type
dates = [datetime.datetime.strptime(d,"%m/%d/%Y").date() for d in dates]

#Second plot will contain Cumulative confirmed cases in Oglala Lakota County
ax2.plot(dates,confirmed_cases)

#Format x axis ticks so that we show only certain x axis data
ax2.xaxis.set_major_formatter(years_fmt)
ax2.xaxis.set_minor_locator(months)
ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

#Show data from first date month to the last date month plus 1 month
datemin = np.datetime64(dates[0], 'M')
datemax = np.datetime64(dates[-1], 'M') + np.timedelta64(1, 'M')
ax2.set_xlim(datemin, datemax)

#format plot and title
ax2.format_xdata = mdates.DateFormatter('%Y-%m-%d')
ax2.grid(True)
ax2.set_title('Cumulative Confirmed Cases in Oglala Lakota County')
fig.autofmt_xdate()

#Open the third file holding population amount
with open("covid_county_population_usafacts.csv", "r") as file:
    text = file.readlines()
    for x in text:
        if 'Oglala Lakota County' in x.split(','): #search only in Oglala Lakota County
            population = int(x.split(',')[-1]) #Grab the number of population of county

#Plot percentage of death in total population
death_percentage = [(x / population) * 100 for x in death_toll]
ax3.plot(dates,death_percentage)
ax3.grid(True)
ax3.set_title('Death % By Total Population')

#Plot percentage of confirmed cases in total population
confirmed_percentage = [(x / population) * 100 for x in confirmed_cases]
ax4.plot(dates,confirmed_percentage)
ax4.grid(True)
ax4.set_title('Confirmed Cases % by Total Population')


#Create 2 plots in a side by side
#Plot 5 will contain  death amount per day in Oglala Lakota County
fig , (ax5,ax6) = plt.subplots(2) #Create plots
plt.subplots_adjust(bottom=3.5, right=1, top=5.5) #format space

#create lists with date of deaths for x axis, and amount of deaths for y axis
x_dates_deaths = []
y_amount_deaths = []

#Run through death_dict to obtain the number of deaths occured in that day
placeholder = 0 #number of deaths start at 0
for key,definition in death_dict.items():#run through each key and definition in dictionary
    if definition > placeholder: #whenever death amount changes, update placeholder
        death_count = definition - placeholder
        placeholder = definition
        x_dates_deaths.append(key) #populate dates
        y_amount_deaths.append(death_count) #populate death amount

#plot scatter plot
ax5.scatter(x_dates_deaths,y_amount_deaths)
ax5.set_title('New Known Deaths Per Day')
ax5.grid(True)


#Second plot will contain new known cases per day

#Declare 2 lists, one with the dates and one with the amount of cases in that day
x_dates_confirmed = []
y_amount_confirmed = []

#Run through cases_dict to obtain the number of cases occured in that day
placeholder = 0 #number of deaths start at 0
for key,definition in cases_dict.items(): #run through each key and definition in dictionary
    if definition > placeholder: #whenever case amount changes, update placeholder
        confirmed_count = definition - placeholder
        placeholder = definition
        x_dates_confirmed.append(key) #populate dates
        y_amount_confirmed.append(confirmed_count) #populate confirmed death amount

#format dates to add year number
x_dates_confirmed = [d + '20' for d in x_dates_confirmed]
#Format dates to be changed to datetime data type
x_dates_confirmed = [datetime.datetime.strptime(d,"%m/%d/%Y").date() for d in x_dates_confirmed]

#Plot number 6 contains new known cases per day
ax6.plot(x_dates_confirmed,y_amount_confirmed)

#Format x axis ticks so that we show only certain x axis data
ax6.xaxis.set_major_formatter(years_fmt)
ax6.xaxis.set_minor_locator(months)
ax6.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

#Show data from first date month to the last date month plus 1 month
datemin = np.datetime64(x_dates_confirmed[0], 'M')
datemax = np.datetime64(x_dates_confirmed[-1], 'M') + np.timedelta64(1, 'M')
ax6.set_xlim(datemin, datemax)

#format plot and title
ax6.format_xdata = mdates.DateFormatter('%Y-%m-%d')
ax6.set_title('New Known Cases per Day')
ax6.grid(True)
plt.show()

#Declare the dashboard app
app = dash.Dash()



colors = {
    'backstage': 'rgb(150,15,35)',
    'background': 'rgb(203,213,222)',
    # 'text': '#999999',
    'text': 'rgb(0,0,0)',
    # 'text': 'rgb(0,0,255)',
    # 'text': '#d62728'
}



#------------------------------------------------------------------------------

# df6 = pd.DataFrame({
#         "Dates_confimed": x_dates_confirmed,
#         "Cases": y_amount_confirmed,
# })
fig6 = px.line(x=x_dates_confirmed, y=y_amount_confirmed, title = "New Known Cases per day")
# fig6 = {
#             'data': [
#                 {'x': x_dates_confirmed, 'y': y_amount_confirmed, 'type': 'line', 'name': 'Known cases per Day'},
#             ],
        
#             'layout': {
#                 'title': 'New Known Cases per Day'
#                 }
#             }
fig6.update_layout(
     plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

df5 = pd.DataFrame({
        "Dates_deaths": x_dates_deaths,
        "Amount_deaths": y_amount_deaths,
})
fig5 = px.line(df5, x="Dates_deaths", y="Amount_deaths", title = "New Known Deaths per day")
# fig5 = {
#             'data': [
#                 {'x': x_dates_deaths, 'y': y_amount_deaths, 'type': 'line', 'name': 'Known cases per Day'},
#             ],
        
#             'layout': {
#                 'title': 'New Known Deaths Per Day'
#                 }
#             }
fig5.update_layout(
     plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )
# df4 = pd.DataFrame({
#         "Dates": dates,
#         "Confirmed_Percentage": confirmed_percentage,
# })
fig4 = px.line(x=dates, y=confirmed_percentage, title = "Confirmed Cases % by Total Population")
# fig4 = {
#             'data': [
#                 {'x': dates, 'y': confirmed_percentage, 'type': 'line', 'name': 'Known cases per Day'},
#             ],
        
#             'layout': {
#                 'title': 'Confirmed Cases % by Total Population'
#                 }
#             }
fig4.update_layout(
     plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )
df3 = pd.DataFrame({
        "Dates": dates,
        "Death_Percentage": death_percentage,
})
fig3 = px.line(df3, x="Dates", y="Death_Percentage", title = "Death % by Total Population")
# fig3 = {
#             'data': [
#                 {'x': dates, 'y': death_percentage, 'type': 'line', 'name': 'Known cases per Day'},
#             ],
        
#             'layout': {
#                 'title': 'Death % by Total Population'
#                 }
#             }
fig3.update_layout(
     plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )
df2 = pd.DataFrame({
        "Dates": dates,
        "Confirmed_Cases": confirmed_cases,
})
fig2 = px.line(df2, x="Dates", y="Confirmed_Cases", title = "Cumulative Confirmed Cases in Oglala Lakota County")
# fig2 = {
#             'data': [
#                 {'x': dates, 'y': confirmed_cases, 'type': 'line', 'name': 'Known cases per Day'},
#             ],
        
#             'layout': {
#                 'title': 'Cumulative Confirmed Cases in Oglala Lakota County'
#                 }
#             }
fig2.update_layout(
     plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )
df1 = pd.DataFrame({
        "Dates": dates,
        "Death_Toll": death_toll,
})
fig1 = px.line(df1, x="Dates", y="Death_Toll", title = "Cumulative Death Count in Oglala Lakota County")
# fig1 = {
#             'data': [
#                 {'x': dates, 'y': death_toll, 'type': 'line', 'name': 'Known cases per Day'},
#             ],
        
#             'layout': {
#                 'title': 'Cumulative Death Count in Oglala Lakota County'
#                 }
#             }
fig1.update_layout(
     plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )





#------------------------------------------------------------------------------



tab_style = {
    'borderBottom': '1px dashed rgb(255,255,255)',
    'backgroundColor': 'rgb(0,0,0)',
    'padding': '6px',
    'fontWeight': 'bold',
    'color': 'white',
}

tab_selected_style = {
    'borderTop': '3px solid rgb(255,255,255)',
    # 'borderBottom': '2px dash rgb(255,255,255)',
    'backgroundColor': 'rgb(200,200,200)',
    'color': 'black',
    'padding': '6px'
}

#------------------------------------------------------------------------------



#Create the layout, declare how many tabs will be used
#One tab per each plot, with its identifying name
app.layout = html.Div(style={'backgroundColor': colors['backstage']}, children = [
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
       dcc.Tab(label='Cumulative Death Count in Oglala Lakota County', value='tab-1',style=tab_style, selected_style = tab_selected_style),
       dcc.Tab(label='Cumulative Confirmed Cases in Oglala Lakota County', value='tab-2',style=tab_style, selected_style = tab_selected_style),
       dcc.Tab(label='Death % per Population', value='tab-3',style=tab_style, selected_style = tab_selected_style),
       dcc.Tab(label='Confirmed Cases % per Population', value='tab-4',style=tab_style, selected_style = tab_selected_style),
       dcc.Tab(label='New Known Deaths per Day', value='tab-5',style=tab_style, selected_style = tab_selected_style),
       dcc.Tab(label='New Known Cases per Day', value='tab-6',style=tab_style, selected_style = tab_selected_style)
       
    ]),
    html.Div(id='tabs-example-content')
])

#App callback is used to alternate between tabs and populate each one with a plot
@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def TabsFunction(tab):
    if tab == 'tab-6': #tab 6 layout
        return html.Details([
        html.Div([
            html.H1(children='COVID Dashboard'), #tab 1 header string
    dcc.Graph(
        id='example',
        figure = fig6
        )
    ])
    ])
    elif tab == 'tab-5': #tab 5 layout
        return html.Div([
            html.H1(children='COVID Dashboard'), #tab 1 header string
    dcc.Graph(
        id='example',
        figure = fig5
        )
        ])
    elif tab == 'tab-4': #tab 4 layout
        return html.Div([
            html.H1(children='COVID Dashboard'), #tab 1 header string
    dcc.Graph(
        id='example',
        figure = fig4
        )
        ])
    elif tab == 'tab-3': #tab 3 layout
        return html.Div([
            html.H1(children='COVID Dashboard'), #tab 1 header string
    dcc.Graph(
        id='example',
        figure = fig3
        )
        ])
    elif tab == 'tab-2': #tab 2 layout
        return html.Div([
            html.H1(children='COVID Dashboard'), #tab 1 header string
    dcc.Graph(
        id='example',
        figure = fig2
        )
        ])
    elif tab == 'tab-1': #tab 1 layout
        return html.Div([
            html.H1(children='COVID Dashboard'), #tab 1 header string
    dcc.Graph(
        id='example',
        figure = fig1
        )
        ])
    
#Main function, here we call the dashboard app to run on server
#Please check the console for the printout of the server location
if __name__ == '__main__':
    app.run_server(debug=False)

        

            
