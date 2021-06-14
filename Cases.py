import json
import folium
import plotly
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
class cases:
        def cmap(cases_mapmaker_data):
                map = folium.Map(location=[25, 80], zoom_start=4.4,min_zoom=4,tiles="CartoDBdark_matter")
                with open('world-countries.json') as handle:
                        country_geo = json.loads(handle.read())
                        for i in country_geo['features']:
                                if i['properties']['name'] == 'India':
                                        country = i
                                        break
                folium.GeoJson(country,name='India').add_to(map)
                folium.LayerControl().add_to(map)
                for lat, lon, value, name in zip(cases_mapmaker_data['Latitude'], cases_mapmaker_data['Longitude'],cases_mapmaker_data['Confirmed'], cases_mapmaker_data['State']):
                        folium.CircleMarker([lat, lon], radius=value*0.000018,popup = ('<strong>State</strong>: ' + str(name).capitalize() + '<br><strong>Total Cases</strong>: ' + str(value) + '<br>'),color='red',fill_color="red",fill_opacity=0.1 ).add_to(map)
                return map
        def cfigs(fig_data,X,Y):
            figx=px.line(fig_data,x=X,y=Y,title='<b>'+str(Y)+'</b>',template="plotly_dark")
            figx.update_layout(title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},height=350)
            return figx
