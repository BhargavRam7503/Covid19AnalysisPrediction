import json
import folium
import plotly
import geopandas as gpd
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
                map_child = folium.features.GeoJson(vaccine_mapmaker_data, tooltip=folium.features.GeoJsonTooltip(
                        fields=['State','Total Individuals Vaccinated','Total Estimated Population','Vaccine Percent'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") ) )
                map.add_child(map_child)
                map.keep_in_front(map_child)
                folium.LayerControl().add_to(map)
                return map
        def vfigs(df,X,Y,title):
                return px.bar(df,x=X,y=Y,color_discrete_sequence=px.colors.qualitative.Dark2,title='<b>'+title+'</b>')
