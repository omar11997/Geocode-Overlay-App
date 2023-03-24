import streamlit as st 
import geopandas as gdp
import leafmap.foliumap as leafmap
import folium
import requests



# ////////////title ////////////////
st.title("Geocoding & Overlay & Buffer App")



# /////////////////// isert files ///////////////////
uploaded_file = st.file_uploader("insert file", type = "geojson")
uploaded_file2 = st.file_uploader("insert overlaped file  ", type= "geojson")
uploaded_file3 = st.file_uploader("insert file to create buffer  and set the buffer lenght ", type= "geojson")
# uploaded_file4 = st.file_uploader("insert file4", type= "geojson")


address = st.text_input("search for address : ")



if uploaded_file and uploaded_file2 and uploaded_file3:
    # //////////////// read files data /////////////////////
    filedata1 = gdp.read_file(uploaded_file).to_crs("EPSG:3857")
    filedata2 = gdp.read_file(uploaded_file2).to_crs("EPSG:3857")
    filedata3 = gdp.read_file(uploaded_file3).to_crs("EPSG:3857")
    # filedata4 = gdp.read_file(uploaded_file4).to_crs("EPSG:3857")

    # ////////////// map Creation /////////////
    m = leafmap.Map()
    # ////////////// intersection ///////////////////////////
    try:
        overlay = gdp.overlay(filedata1,filedata2, how = "intersection")
        m.add_gdf(overlay,style_function=lambda feature: {
                    "fillColor": "red",
                    "color": "black",
                    "weight": 1,
                    "fillOpacity": 0.5,
                })
    except:
        pass
    # overlay.plot(color = 'red')
    # join = filedata1.sjoin(filedata4)
    # /////////////// buffer creation//////////////////
    # buffer = filedata3['geometry'].buffer(1000)
    # buffer_gdf = gdp.GeoDataFrame(geometry = buffer)
    # ////////////// map Creation /////////////
    m = leafmap.Map()
    # /////////////////////////////////////////////////
    length = st.text_input("Enter Distance of buffer:")
    st.write("The Defult value of Buffer 3Km")
    bu =st.button("make buffer")
    if bu :
        if not length:
            length = 3000
        length= int(length)
        buffer = filedata3["geometry"].buffer(length)
        map_buffer= gdp.GeoDataFrame(filedata3,geometry =buffer )
        m.add_gdf(map_buffer)
    
    
    
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
    # if overlay:
    #     m.add_gdf(overlay,style_function=lambda feature: {
    #                 "fillColor": "red",
    #                 "color": "black",
    #                 "weight": 1,
    #                 "fillOpacity": 0.5,
    #             })
    # m.add_gdf(buffer_gdf)
    
    m.to_streamlit(height=500)
if address:
    try:
        response = requests.get("https://nominatim.openstreetmap.org/search", params={"q": address, "format": "json"})
        location = response.json()[0]
        lat = location["lat"]
        lon = location["lon"]
        map = leafmap.Map(location=[lat, lon], zoom_start=5)
        map.to_streamlit(height=500)
        folium.Marker([lat, lon],popup=address).add_to(map)
        
    except:
        print("this address is not found ")
    

