import json
import folium
import plotly
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
class vaccination:
        def vmap(vaccine_mapmaker_data):
                map = folium.Map(location=[25, 80], zoom_start=4.4,min_zoom=4)
                with open('world-countries.json') as handle:
                        country_geo = json.loads(handle.read())
                        for i in country_geo['features']:
                                if i['properties']['name'] == 'India':
                                        country = i
                                        break
                folium.GeoJson(country,name='India').add_to(map)
                folium.LayerControl().add_to(map)
                for lat, lon, value, name in zip(vaccine_mapmaker_data['Latitude'],vaccine_mapmaker_data['Longitude'], vaccine_mapmaker_data['Total Individuals Vaccinated'], vaccine_mapmaker_data['State']):
                        folium.CircleMarker([lat, lon], radius=value*0.000002, popup = ('<strong>State</strong>: ' + str(name).capitalize() + '<br>''<strong>Total Individuals Vaccinated</strong>: ' + str(value) + '<br>'),color='Green',fill_color="Green",fill_opacity=0.3 ).add_to(map)
                return map
        def vfigs(df,X,Y,title):
                figx=px.bar(df,x=X,y=Y,color_discrete_sequence=px.colors.qualitative.Dark2,title='<b>'+title+'</b>')
                figx.update_layout(title={
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'}}
                return figx
