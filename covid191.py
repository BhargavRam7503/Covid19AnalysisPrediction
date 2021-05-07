#!/usr/bin/env python
# coding: utf-8
#importing necessary packages
import pandas as pd
import datetime
# Visualisation libraries
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import folium 
from folium import plugins
import streamlit as st
import SessionState
# Manipulating the default plot size
import json
import webbrowser
import streamlit.components.v1 as components
# Disable warnings 
import warnings
warnings.filterwarnings('ignore')
#Cases
#Creating Dataframe from cases data
cases_data=pd.read_csv('covid_19_india.csv')
cases_data.rename(columns = {'State/UnionTerritory':'Detected State'}, inplace = True)
#Deleting irrelavant data and correcting
cases_data.drop(['Sno', 'Time','ConfirmedIndianNational', 'ConfirmedForeignNational'],inplace = True, axis = 1)
cases_data.replace(['Telengana'],['Telangana'],inplace=True)
for i in range(len(cases_data['Date'])):
    cases_data['Date'][i]=datetime.datetime.strptime(cases_data['Date'][i], "%Y-%m-%d").date()
#Adding Active cases Column
cases_data['Active'] = cases_data['Confirmed']-cases_data['Cured']-cases_data['Deaths']
#Taking Updated Data
total_cases=cases_data[:][cases_data['Date']==list(cases_data['Date'])[-1]]
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
                            'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim','Tripura',
                            'West Bengal','Ladakh'],inplace=True)
states=['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir',
        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttarakhand', 'Uttar Pradesh', 'West Bengal']
#Cases map
cases_mapmaker_data = pd.merge(states_coordinates,total_cases,on='Detected State')
map = folium.Map(location=[25, 80], zoom_start=4.4,min_zoom=4,tiles="CartoDBdark_matter")
with open('world-countries.json') as handle:
    country_geo = json.loads(handle.read())

for i in country_geo['features']:
    if i['properties']['name'] == 'India':
        country = i
        break
folium.GeoJson(country,
               name='India').add_to(map)
folium.LayerControl().add_to(map)
for lat, lon, value, name in zip(cases_mapmaker_data['Latitude'], cases_mapmaker_data['Longitude'],
                                 cases_mapmaker_data['Confirmed'], cases_mapmaker_data['Detected State']):
    folium.CircleMarker([lat, lon], radius=value*0.00002,
                        popup = ('<strong>State</strong>: ' + str(name).capitalize() + '<br>''<strong>Total Cases</strong>: ' + str(value) + '<br>'),color='red',
                        fill_color="red",fill_opacity=0.1 ).add_to(map)
map.save("VirusSpread.html")
#statewise table
statewise_table_cases_data=total_cases[['Detected State','Cured','Deaths','Confirmed','Active']]
statewise_table_cases_data.reset_index(drop=True,inplace=True)
#seek bar for changing data according to date
datelist=[]
for i in cases_data['Date']:
    if(i not in datelist):
        datelist.append(i)

#Cases Graphs
#Cases Graph - 1
fig1=px.line(cases_data,x='Date',y='Active',title="Covid cases " + str('Date') + ' vs ' + str('Active'),template="plotly_dark")
#Cases Graph - 2
fig2=px.line(cases_data,x='Date',y='Confirmed',title="Covid cases " + str('Date') + ' vs ' + str('Confirmed'),template="plotly_dark")
#Cases Graph - 3
fig3=px.line(cases_data,x='Date',y='Deaths',title="Covid cases " + str('Date') + ' vs ' + str('Deaths'),template="plotly_dark")
#Cases Graph - 4
fig4=px.line(cases_data,x='Date',y='Cured',title="Covid cases " + str('Date') + ' vs ' + str('Cured'),template="plotly_dark")
#Vaccine
#Creating Dataframe from vaccine data
df_vaccine_statewise = pd.read_csv("covid_vaccine_statewise.csv")
latest_vaccine_date = (df_vaccine_statewise["Updated On"]=="21/04/2021")
latest_vaccine_data = df_vaccine_statewise[latest_vaccine_date][1:]
latest_vaccine_data.rename(columns={"State":"Detected State"},inplace=True)
vaccine_mapmaker_data = pd.merge(states_coordinates,latest_vaccine_data,on='Detected State')
map = folium.Map(location=[25, 85], zoom_start=4.4,min_zoom=4)
with open('world-countries.json') as handle:
    country_geo = json.loads(handle.read())
for i in country_geo['features']:
    if i['properties']['name'] == 'India':
        country = i
        break
folium.GeoJson(country,
               name='India').add_to(map)
folium.LayerControl().add_to(map)
for lat, lon, value, name in zip(vaccine_mapmaker_data['Latitude'],vaccine_mapmaker_data['Longitude'], vaccine_mapmaker_data['Total Individuals Vaccinated'], vaccine_mapmaker_data['Detected State']):
    folium.CircleMarker([lat, lon], radius=value*0.000002, popup = ('<strong>State</strong>: ' + str(name).capitalize() + '<br>''<strong>Total Individuals Vaccinated</strong>: ' + str(value) + '<br>'),color='Green',fill_color="Green",fill_opacity=0.3 ).add_to(map)
map.save("VaccinationMap.html")
indian_vaccine_data = (df_vaccine_statewise["State"]=="India")
vaccine_data_x1 = df_vaccine_statewise[indian_vaccine_data]["Updated On"]
#Vaccine Graphs
#Vaccine Graph - 1
vaccine_data_y1 = df_vaccine_statewise[indian_vaccine_data]["Total Individuals Registered"]
fig5 = px.line(x = vaccine_data_x1, y = vaccine_data_y1,color_discrete_sequence=px.colors.qualitative.Dark2,
       title="Total Individuals Registering for vaccines")
fig5.update_xaxes(title_text="Dates")
fig5.update_yaxes(title_text="Number of Persons Registered")
#Vaccine Graph - 2
vaccine_data_y2 = df_vaccine_statewise[indian_vaccine_data]["First Dose Administered"]
vaccine_data_y3 = df_vaccine_statewise[indian_vaccine_data]["Second Dose Administered"]
fig6 = px.line(x = vaccine_data_x1, y = [vaccine_data_y2,vaccine_data_y3],color_discrete_sequence=px.colors.qualitative.Dark2,
       title="First Dose and Second Dose Administered Comparison all over India")
fig6.update_xaxes(title_text="Dates")
fig6.update_yaxes(title_text="No of persons given vaccines")
#Vaccine Graph - 3
vaccine_data_y4 = df_vaccine_statewise[indian_vaccine_data]["Total Covaxin Administered"]
vaccine_data_y5 = df_vaccine_statewise[indian_vaccine_data]["Total CoviShield Administered"]
fig7 = px.line(x = vaccine_data_x1, y = [vaccine_data_y4,vaccine_data_y5],color_discrete_sequence=px.colors.qualitative.Dark2,
       title="Covaxin vs CoviShield")
#Vaccine Graph - 4
vaccine_data_y6 = df_vaccine_statewise[indian_vaccine_data]["Male(Individuals Vaccinated)"]
vaccine_data_y7 = df_vaccine_statewise[indian_vaccine_data]["Female(Individuals Vaccinated)"]
fig8= px.line(x = vaccine_data_x1, y = [vaccine_data_y6,vaccine_data_y7],color_discrete_sequence=px.colors.qualitative.Dark2,
       title="Male vs Female vaccinated in India")
#Title
st.set_page_config(page_title="Covid19 Analysis and Prediction", layout='wide', initial_sidebar_state='collapsed')
st.title("COVID19")
#side bar
choice=st.sidebar.radio("",["Home","About","Resources"])
#creating tabs
option=st.selectbox("",["Cases","Vaccination","Prediction"])
#cases tab
if(option== "Cases"):
        plot_map,updated_table=st.beta_columns(2)
        with plot_map:
            HtmlFile = open("VirusSpread.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            st.subheader("Cases")
            components.html(source_code, width =450, height=420)
        with updated_table:
            table_data=total_cases[['Detected State','Cured','Deaths','Confirmed','Active']]
            table_data.loc['Total']=pd.Series(total_cases[['Detected State','Cured','Deaths','Confirmed','Active']].sum(),
                                     index = ['Detected State','Cured','Deaths','Confirmed','Active'])
            table_data.reset_index(inplace=True)
            del table_data["Detected State"]
            del table_data["index"]
            table_data=table_data.transpose()
            table_data.rename(columns={36:"Total"},inplace=True)
            st.subheader("As on 23/04/2021")
            st.subheader("")
            st.table(table_data["Total"])
        st.subheader("")
        st.table(statewise_table_cases_data)
        option1=st.selectbox("",["Statewise Trends","Datewise Trends"])
        if(option1=="Statewise Trends"):
            selected_state = st.slider('Select Date', 0, 35, 31)
            if(selected_state):
                st.write("State", states[selected_state])
                upto_selected_state=cases_data['Detected State']==states[selected_state]
                #Cases Graph - 1
                fig1=px.line(cases_data[:][upto_selected_state],x='Date',y='Active',title="Covid cases " + str('Date') + ' vs ' + str('Active'),template="plotly_dark")
                #Cases Graph - 2
                fig2=px.line(cases_data[:][upto_selected_state],x='Date',y='Confirmed',title="Covid cases " + str('Date') + ' vs ' + str('Confirmed'),template="plotly_dark")
                #Cases Graph - 3
                fig3=px.line(cases_data[:][upto_selected_state],x='Date',y='Deaths',title="Covid cases " + str('Date') + ' vs ' + str('Deaths'),template="plotly_dark")
                #Cases Graph - 4
                fig4=px.line(cases_data[:][upto_selected_state],x='Date',y='Cured',title="Covid cases " + str('Date') + ' vs ' + str('Cured'),template="plotly_dark")
                cases_graphs=st.beta_columns(2)
                with cases_graphs[0]:
                    st.plotly_chart(fig1)
                    st.plotly_chart(fig2)
                with cases_graphs[1]:
                    st.plotly_chart(fig3)
                    st.plotly_chart(fig4)
        if(option1=="Datewise Trends"):
            selected_date = st.slider('Select Date', datelist[0], datelist[449], datelist[449])
            if(selected_date):
                st.write("Date", selected_date)
                upto_selected_date=cases_data['Date']<=selected_date
                #Cases Graph - 1
                fig1=px.line(cases_data[:][upto_selected_date],x='Date',y='Active',title="Covid cases " + str('Date') + ' vs ' + str('Active'),template="plotly_dark")
                #Cases Graph - 2
                fig2=px.line(cases_data[:][upto_selected_date],x='Date',y='Confirmed',title="Covid cases " + str('Date') + ' vs ' + str('Confirmed'),template="plotly_dark")
                #Cases Graph - 3
                fig3=px.line(cases_data[:][upto_selected_date],x='Date',y='Deaths',title="Covid cases " + str('Date') + ' vs ' + str('Deaths'),template="plotly_dark")
                #Cases Graph - 4
                fig4=px.line(cases_data[:][upto_selected_date],x='Date',y='Cured',title="Covid cases " + str('Date') + ' vs ' + str('Cured'),template="plotly_dark")
                cases_graphs=st.beta_columns(2)
                with cases_graphs[0]:
                    st.plotly_chart(fig1)
                    st.plotly_chart(fig2)
                with cases_graphs[1]:
                    st.plotly_chart(fig3)
                    st.plotly_chart(fig4)
if(option== "Vaccination"):
    map_plot_col=st.beta_columns(3)
    with map_plot_col[1]:
        HtmlFile = open("VaccinationMap.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        st.subheader("Vaccination")
        components.html(source_code, width =450, height=420)
    statewise_table_vaccine_data=latest_vaccine_data.iloc[:,1:].reset_index()
    st.table(statewise_table_vaccine_data.iloc[:,1:])
    vaccine_graphs=st.beta_columns(2)
    with vaccine_graphs[0]:
        st.plotly_chart(fig5)
        st.plotly_chart(fig6)
    with vaccine_graphs[1]:
        st.plotly_chart(fig7)
        st.plotly_chart(fig8)
if(option== "Prediction"):
    prediction=st.button("Prediction")
    if(prediction):
        st.write("pred")

