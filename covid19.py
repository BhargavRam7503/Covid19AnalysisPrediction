#!/usr/bin/env python
# coding: utf-8
#importing necessary packages
import pandas as pd
import numpy as np
import datetime
import math
# Visualisation libraries
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import geopandas as gpd
import streamlit as st
from streamlit_folium import folium_static
# Manipulating the default plot size
import json
import webbrowser
import streamlit.components.v1 as components
# importing cases, vaccination visulations
from Cases import cases
from Vaccination import vaccination
#predicting algorithms
from statsmodels.tsa.arima_model import ARIMA
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
# Disable warnings 
import warnings
warnings.filterwarnings('ignore')
#Cases
#Creating Dataframe from cases data
cases_data=pd.read_csv('https://api.covid19india.org/csv/latest/states.csv')
cases_data.drop(['Tested','Other'],inplace = True, axis = 1)
for i in range(len(cases_data['Date'])):
    cases_data['Date'][i]=datetime.datetime.strptime(cases_data['Date'][i], "%Y-%m-%d").date()
cases_data.drop(cases_data[cases_data['State'].apply(lambda x: x.startswith('State Unassigned'))].index,inplace=True)
#Adding Active cases Column
cases_data['Active'] = cases_data['Confirmed']-cases_data['Recovered']-cases_data['Deceased']
d=cases_data.groupby(["State","Date","Confirmed"]).sum()
#Taking Updated Data
cases_date=datetime.date.today()-datetime.timedelta(days = 1)
total_cases=cases_data[:][cases_data['Date']==cases_date]
latest_cases=total_cases[:][total_cases['State']=="India"]
total_cases=total_cases[:][total_cases['State']!="India"]
#Taking indian state coordinates to plot on map
states_coordinates=pd.read_excel('Indian Coordinates.xlsx')
states_coordinates.replace(['Andaman And Nicobar ', 'Andhra Pradesh', 'Arunachal Pradesh ', 'Assam ', 'Bihar ', 'Chandigarh ',
                            'Chhattisgarh ', 'Dadra And Nagar Haveli ', 'Delhi', 'Goa ', 'Haryana', 'Himachal Pradesh ',
                            'Union Territory of Jammu and Kashmir', 'Jharkhand ', 'Karnataka', 'Kerala', 'Lakshadweep ',
                            'Madhya Pradesh ', 'Maharashtra', 'Manipur ', 'Meghalaya ', 'Mizoram ', 'Nagaland ', 'Orissa ',
                            'Puducherry ', 'Punjab', 'Rajasthan','Sikkim ', 'Tripura ', 'West Bengal ', 'Union Territory of Ladakh'],
                           ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
                            'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Haryana', 'Himachal Pradesh',
                            'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra',
                            'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan','Sikkim','Tripura','West Bengal','Ladakh'],inplace=True)
states=list(total_cases['State'].unique())
cases_mapmaker_data = pd.merge(states_coordinates,total_cases,on='State')
#Cases tab
latest_cases.reset_index(inplace=True)
latest_cases.drop(['Date','State','index'],axis='columns',inplace=True)
ctab1=list(latest_cases)
ctab2=latest_cases.values.tolist()[0]
#statewise table
statewise_table_cases_data=total_cases[['State','Recovered','Deceased','Confirmed','Active']]
statewise_table_cases_data.reset_index(drop=True,inplace=True)
statewise_table_cases_data.set_index(['State'],inplace=True)
#seek bar for changing data according to date
datelist=[]
for i in cases_data['Date']:
    if(i not in datelist):
        datelist.append(i)
#Vaccine
#Creating Dataframe from vaccine data
df_vaccine_statewise = pd.read_csv("http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv")
vaccine_date=datetime.date.today()-datetime.timedelta(days = 2)
latest_vaccine_date = (df_vaccine_statewise["Updated On"]==vaccine_date.strftime("%d/%m/%Y"))
latest_vaccine_data = df_vaccine_statewise[latest_vaccine_date]
total_population=[1371360350,417036,53903393,1570458,35607039,124799926,1158473,29436231,615724,18710922,1586250,
                  63872399,28204692,7451955,13606320,38593948,67562686,35699443,289023,73183,85358965,
                  123144223,3091545,3366710,1239244,2249695,46356334,1413542,30141373,81032689,690251,
                  77841267,39362732,4169794,237882725,11250858,99609303]
vaccine_updated_data=list(latest_vaccine_data["Total Individuals Vaccinated"])
vaccine_percent=[]
for i in range(len(vaccine_updated_data)):
    vaccine_percent.append(vaccine_updated_data[i]*100/total_population[i])
latest_vaccine_data["Total Estimated Population"]=total_population
latest_vaccine_data["Vaccine Percent"]=vaccine_percent
statewise_table_vaccine_data=latest_vaccine_data.iloc[1:,1:]
statewise_table_vaccine_data.set_index(["State"],inplace=True)
#Vaccine Tab
vtab=latest_vaccine_data.iloc[0,2:]
vtab1=list(dict(vtab).keys())
vtab2=list(vtab)
#Vaccine Map
shp_gdf = gpd.read_file("Indian_states.shp")
shp_gdf.rename(columns = {'st_nm':'State'}, inplace = True)
shp_gdf["State"].replace(['Andaman & Nicobar Island', 'Andhra Pradesh', 'Arunanchal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadara & Nagar Havelli', 
                          'NCT of Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Lakshadweep', 
                          'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 
                          'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'],
                ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu',
                 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra',
                 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                 'Uttarakhand', 'West Bengal'],inplace=True)
vaccine_mapmaker_data = pd.merge(shp_gdf,latest_vaccine_data,on='State')
#Vaccine Graphs
indian_vaccine_data = (df_vaccine_statewise["State"]=="India")
#Vaccine Graph - 1
fig5 = vaccination.vfigs(df_vaccine_statewise[indian_vaccine_data],"Updated On","Total Individuals Vaccinated","Total Individuals Vaccinated")
fig5.update_xaxes(title_text="Dates")
fig5.update_yaxes(title_text="Number of Persons Vaccinated")
#Vaccine Graph - 2
fig6 = vaccination.vfigs(df_vaccine_statewise[indian_vaccine_data],"Updated On",["First Dose Administered","Second Dose Administered"],"First Dose and Second Dose Administered Comparison all over India")
fig6.update_xaxes(title_text="Dates")
fig6.update_yaxes(title_text="No of persons given vaccines")
#Vaccine Graph - 3
fig7 = vaccination.vfigs(df_vaccine_statewise[indian_vaccine_data],"Updated On",["Total Covaxin Administered","Total CoviShield Administered"],"Covaxin vs CoviShield")
#Vaccine Graph - 4
fig8= vaccination.vfigs(df_vaccine_statewise[indian_vaccine_data],"Updated On",["Male(Individuals Vaccinated)","Female(Individuals Vaccinated)"],"Male vs Female vaccinated in India")
#Prediction
pred_data=cases_data[:][cases_data["State"]=="India"]
pred_data["Days Since"]=range(0,len(pred_data))
india_confirmed=list(pred_data["Active"])
change_diff = []
for i in range(1,len(india_confirmed)):
    change_diff.append(india_confirmed[i] / (india_confirmed[i-1]+1))
change_factor = sum(change_diff)/len(change_diff)
prediction_dates = []
start_date = datelist[len(datelist) - 1]
type(datelist[1])
for i in range(15):
    date = start_date + datetime.timedelta(days=1)
    prediction_dates.append(date)
    start_date = date
previous_day_cases = india_confirmed[len(india_confirmed) - 1]
predicted_cases = []
for i in range(15):
    predicted_value = math.ceil(previous_day_cases /  change_factor)
    predicted_cases.append(predicted_value)
    previous_day_cases = predicted_value

fig = go.Figure()
pred_fig1=fig.add_trace(go.Scatter(y=predicted_cases,x=prediction_dates,mode='lines+markers',name='Predicted'))

data = pd.DataFrame(columns = ['ds','y'])
data['ds'] = datelist
data['y'] = india_confirmed

arima = ARIMA(data['y'], order=(5, 1, 0))
arima = arima.fit(trend='c', full_output=True, disp=True)
forecast = arima.forecast(steps= 30)
pred = list(forecast[0])

start_date = data['ds'].max()
prediction_dates = []
for i in range(30):
    date = start_date + datetime.timedelta(days=1)
    prediction_dates.append(date)
    start_date = date

fig=go.Figure()
fig.add_trace(go.Scatter(y=pred,x=prediction_dates,mode='lines+markers',name = 'Predicted'))
pred_fig2=fig.add_trace(go.Scatter(y=data['y'],x=data['ds'],mode='lines+markers',name = 'Actual'))



train_ml=pred_data.iloc[:int(pred_data.shape[0]*0.95)]
valid_ml=pred_data.iloc[int(pred_data.shape[0]*0.95):]
#Polynomial
poly = PolynomialFeatures(degree = 10)
linreg=LinearRegression(normalize=True)
train_poly=poly.fit_transform(np.array(train_ml["Days Since"]).reshape(-1,1))
valid_poly=poly.fit_transform(np.array(valid_ml["Days Since"]).reshape(-1,1))
y=train_ml["Active"]
linreg.fit(train_poly,y)
prediction_poly=linreg.predict(valid_poly)

Prediction_Polynomial_Regression = prediction_poly.tolist()
comp_data=poly.fit_transform(np.array(pred_data["Days Since"]).reshape(-1,1))
plt.figure(figsize=(11,6))
predictions_poly=linreg.predict(comp_data)
fig_poly=go.Figure()
fig_poly.add_trace(go.Scatter(x=pred_data['Date'], y=pred_data["Active"],
                    mode='lines+markers',name="Train Data for Active Cases"))
fig_poly.add_trace(go.Scatter(x=pred_data['Date'], y=predictions_poly,
                    mode='lines',name="Polynomial Regression Best Fit",
                   line=dict(color='black', dash='dot' )))
pred_fig3=fig_poly.update_layout(title="Active Cases Polynomial Regression Prediction",
                 xaxis_title="Date",yaxis_title="Active Cases",
                 legend=dict(x=0,y=1,traceorder="normal"))
#Title
st.set_page_config(page_title="Covid19 Analysis and Prediction", layout='wide', initial_sidebar_state='collapsed')
st.markdown("<h1 style='text-align: center;'>Covid 19 India</h1>", unsafe_allow_html=True)
st.subheader("")
#side bar
choice=st.sidebar.radio("",["Home","About","Resources"])
#creating tabs
option=st.selectbox("",["Cases","Vaccination","Prediction"])
#cases tab
if(option== "Cases"):
        plot_map,cases_tab=st.beta_columns([2,1])
        with plot_map:
            st.subheader("")
            folium_static(cases.cmap(cases_mapmaker_data),600,500)
        with cases_tab:
            st.subheader("As on "+cases_date.strftime("%d %b %Y"))
            st.subheader("")
            chtml="<table style='width:100%'>"
            for i in range(len(ctab1)):
                chtml+="<tr><td><b>"+str(ctab1[i])+"</b></td><td>"+str(ctab2[i])+"</td></tr>"
            st.markdown(chtml+"</table>",unsafe_allow_html=True)
        st.subheader("")
        ctable=st.beta_columns(2)
        with ctable[0]:
            selected_state=st.selectbox("",states,30)
            if(selected_state):
                st.markdown("<h3 style='text-align: center;'>"+str(selected_state)+"</h3>", unsafe_allow_html=True)
                upto_selected_state=cases_data['State']==selected_state
                #Cases Graph - 1
                fig1=cases.cfigs(cases_data[:][upto_selected_state],"Date","Active")
                #Cases Graph - 2
                fig2=cases.cfigs(cases_data[:][upto_selected_state],"Date","Confirmed")
                #Cases Graph - 3
                fig3=cases.cfigs(cases_data[:][upto_selected_state],"Date","Deceased")
                #Cases Graph - 4
                fig4=cases.cfigs(cases_data[:][upto_selected_state],"Date","Recovered")
                st.plotly_chart(fig1)
                st.plotly_chart(fig2)
                st.plotly_chart(fig3)
                st.plotly_chart(fig4)
        with ctable[1]:
            st.table(statewise_table_cases_data)
        st.markdown("<h2 style='text-align: center;'>"+"Datewise Trends"+"</h2>", unsafe_allow_html=True)
        selected_date = st.slider('Select Date', datelist[0], datelist[-1], datelist[-1])
        if(selected_date):
                st.markdown("<h3 style='text-align: center;'>"+selected_date.strftime("%d %b %Y")+"</h3>", unsafe_allow_html=True)
                upto_selected_date=cases_data['Date']<=selected_date
                #Cases Graph - 1
                fig1=cases.cfigs(cases_data[:][upto_selected_date],"Date","Active")
                #Cases Graph - 2
                fig2=cases.cfigs(cases_data[:][upto_selected_date],"Date","Confirmed")
                #Cases Graph - 3
                fig3=cases.cfigs(cases_data[:][upto_selected_date],"Date","Deceased")
                #Cases Graph - 4
                fig4=cases.cfigs(cases_data[:][upto_selected_date],"Date","Recovered")
                cases_graphs=st.beta_columns(2)
                with cases_graphs[0]:
                    st.plotly_chart(fig1)
                    st.plotly_chart(fig2)
                with cases_graphs[1]:
                    st.plotly_chart(fig3)
                    st.plotly_chart(fig4)
if(option== "Vaccination"):
    map_plot_col,vaccine_tab=st.beta_columns([2,1])
    with map_plot_col:
        st.subheader("")
        st.subheader("")
        st.subheader("")
        folium_static(vaccination.vmap(vaccine_mapmaker_data),600,700)
    with vaccine_tab:
        st.subheader("As on "+vaccine_date.strftime("%d %b %Y"))
        st.subheader("")
        vhtml="<table style='width:100%'>"
        for i in range(len(vtab)):
            vhtml+="<tr><td>"+str(vtab1[i])+"</td><td>"+str(vtab2[i])+"</td></tr>"
        st.markdown(vhtml+"</table>",unsafe_allow_html=True)
    st.subheader("")
    st.table(statewise_table_vaccine_data)
    vaccine_graphs=st.beta_columns(2)
    with vaccine_graphs[0]:
        st.plotly_chart(fig5)
        st.plotly_chart(fig6)
    with vaccine_graphs[1]:
        st.plotly_chart(fig7)
        st.plotly_chart(fig8)
if(option== "Prediction"):
    predcols=st.beta_columns(2)
    with predcols[0]:
        st.subheader("Using Reduction Factor")
        st.plotly_chart(pred_fig1)
        st.subheader("Polynomial regression")
        st.plotly_chart(pred_fig3)
    with predcols[1]:
        st.subheader("Arima model")
        st.plotly_chart(pred_fig2)
