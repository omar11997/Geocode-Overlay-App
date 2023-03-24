import streamlit as st 
import geopandas as gdp
import leafmap.foliumap as leafmap
from geopy.geocoders import Nominatim
import folium
import requests


# /////////////////// isert files ///////////////////
uploaded_file = st.file_uploader("insert file", type = "geojson")
uploaded_file2 = st.file_uploader("insert file 2 ", type= "geojson")
uploaded_file3 = st.file_uploader("insert file 3 (to buffer) ", type= "geojson")
# uploaded_file4 = st.file_uploader("insert file4", type= "geojson")


address = st.text_input("Enter an address :")

st.title("Geocoding & Overlay App")

if uploaded_file and uploaded_file2 and uploaded_file3:
    # //////////////// read files data /////////////////////
    filedata1 = gdp.read_file(uploaded_file).to_crs("EPSG:3857")
    filedata2 = gdp.read_file(uploaded_file2).to_crs("EPSG:3857")
    filedata3 = gdp.read_file(uploaded_file3).to_crs("EPSG:3857")
    # filedata4 = gdp.read_file(uploaded_file4).to_crs("EPSG:3857")

    # ////////////// intersection ///////////////////////////
    overlay = gdp.overlay(filedata1,filedata2, how = "intersection")
    # overlay.plot(color = 'red')
    # join = filedata1.sjoin(filedata4)
    # /////////////// buffer creation//////////////////
    # buffer = filedata3['geometry'].buffer(1000)
    # buffer_gdf = gdp.GeoDataFrame(geometry = buffer)
    # /////////////////////////////////////////////////
    buffer = filedata3["geometry"].buffer(2000)
    map_buffer= gdp.GeoDataFrame(filedata3,geometry =buffer )
    # ///////////////coloring ////////////////////
    # fig, ax = plt.subplots()
    # overlay.plot(ax=ax , color = "blue", edgecolor ="black")
    # area = filedata1["geometry"].area
    # map_area= gdp.GeoDataFrame(filedata1,geometry =area )

    
    # ////////////// map Creation /////////////
    m = leafmap.Map()

    # ////////// Adding data to Map //////////////
    m.add_gdf(filedata1,style_function=lambda feature: {
                  "fillColor": "green",
                  "color": "black",
                  "weight": 1,
                  "fillOpacity": 0.5,
              })
    m.add_gdf(filedata2,style_function=lambda feature: {
                  "fillColor": "yellow",
                  "color": "black",
                  "weight": 1,
                  "fillOpacity": 0.5,
              })
    m.add_gdf(overlay,style_function=lambda feature: {
                  "fillColor": "red",
                  "color": "black",
                  "weight": 1,
                  "fillOpacity": 0.5,
              })
    # m.add_gdf(buffer_gdf)
    m.add_gdf(map_buffer)
    m.to_streamlit(height=500)
    # m.add_gdf(join,style_function=lambda feature: {
    #               "fillColor": "yellow",
    #               "color": "black",
    #               "weight": 1,
    #               "fillOpacity": 0.5,
    #           })
   

if address:
    try:
        response = requests.get("https://nominatim.openstreetmap.org/search", params={"q": address, "format": "json"})
        location = response.json()[0]
        lat = location["lat"]
        lon = location["lon"]
        map = leafmap.Map(location=[lat, lon], zoom_start=5)
        map.to_streamlit(height=500)
        # folium.Marker([lat, lon],popup=address,size = 20).add_to(map)
        folium.Marker([lat, lon]).add_to(map)
    except:
        print("this address is not found ")
    

