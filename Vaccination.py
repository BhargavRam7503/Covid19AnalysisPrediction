import json
import folium
import plotly
import geopandas as gpd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import branca.colormap as cmp
class vaccination:
        def vmap(vaccine_mapmaker_data):
                map = folium.Map(location=[25, 80], zoom_start=4.4,min_zoom=4)
                folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(map)
                linear = cmp.LinearColormap(
                    ['#7CFC00','#7CFC00','#32CD32','#00FF00','#228B22','#008000','#006400'],
                    vmin=1, vmax=100,
                    caption='% of Vaccinated People')
                style_function = lambda x: {"weight":0.5, 
                                            'color':'black',
                                            'fillColor':linear(x['properties']['Vaccine Percent']), 
                                            'fillOpacity':0.75}
                highlight_function = lambda x: {'fillColor': '#ADD8E6', 
                                                'color':'#ADD8E6', 
                                                'fillOpacity': 0.50, 
                                                'weight': 0.1}
                map_child=folium.features.GeoJson(
                        vaccine_mapmaker_data,
                        style_function=style_function,
                        control=False,
                        highlight_function=highlight_function,
                        tooltip=folium.features.GeoJsonTooltip(fields=['State','Vaccine Percent'],
                            aliases=['State','Total Individuals Vaccinated','Total Estimated Population','Vaccine Percent'],
                            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                            sticky=True
                        )
                    ).add_to(map)
                map.add_child(map_child)
                map.keep_in_front(map_child)
                return map
        def vfigs(df,X,Y,title):
                return px.bar(df,x=X,y=Y,color_discrete_sequence=px.colors.qualitative.Dark2,title='<b>'+title+'</b>')
