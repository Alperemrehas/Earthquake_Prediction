import data
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import ssl
ssl._create_default_https_context = ssl._create_unverified_context




def dataReader(method):
    pd.options.display.max_columns = None
    pd.options.display.max_rows = 100
    if(method == "np"):
        earthquakearray = np.genfromtxt("usgsQuery_TR_73-87.csv", delimiter=",",usecols=np.arange(0 ,22))
        np.set_printoptions(linewidth=22)
    else :
        earthquakearray1 = pd.read_csv("usgsQuery_TR_73-87.csv")
        earthquakearray2 = pd.read_csv("usgsQuery_TR_88-93.csv")
        earthquakearray3 = pd.read_csv("usgsQuery_TR_94-99.csv")
        earthquakearray4 = pd.read_csv("usgsQuery_TR_00-05.csv")
        earthquakearray5 = pd.read_csv("usgsQuery_TR_06-21.csv")
        frames = [earthquakearray1, earthquakearray2, earthquakearray3, earthquakearray4, earthquakearray5]
        totalframe = pd.concat(frames)

    return totalframe

def read_data():
    frames = []
    for i in range(1973, 2022):
        frames.append(pd.read_csv("earthquakes/earthquake_" + str(i) + ".csv"))
    
    return pd.concat(frames)

def fetch_earthquakes():
    for i in range(1973, 2021):
        data.APIquery(starttime="1973-01-01", endtime="1987-12-31",
            minlatitude= "35.9025",
            maxlatitude= "42.02683",
            minlongitude= "25.90902",
            maxlongitude= "44.5742",
            filename="earthquakes/earthquake_" + str(i) + ".csv",
            format="csv")
    data.APIquery(starttime="2021-01-01", endtime="2021-06-30",
            minlatitude= "35.9025",
            maxlatitude= "42.02683",
            minlongitude= "25.90902",
            maxlongitude= "44.5742",
            filename="earthquakes/earthquake_2021.csv",
            format="csv")


if __name__ == "__main__":
    # fetch_earthquakes()

    earthquakes = data.preprocesData(read_data())


    print("***************Raw Data***************")
    print(earthquakes)
    processed_data = data.preprocesData(earthquakes)
    print("The DATA After Drop")
    print(processed_data)

    edges = data.extractEdges(processed_data)
    n = 10
    m = 20

    latitudes, longitudes = data.divideIntoGrid(edges, n, m)

    data.addGridCoordinatesAndYear(processed_data, edges, n, m)

    # print(processed_data[(processed_data.time)])

    # print(processed_data)

    for i in range(1973, 2022):
        print(processed_data[(processed_data['year'] == str(i))])

    # print(processed_data.dtypes)

    fig = go.Figure(go.Scattermapbox())

    for latitude in latitudes:
        fig.add_trace(go.Scattermapbox(
            mode = "lines",
            lon = [edges['minLongitude'], edges['maxLongitude']],
            lat = [latitude, latitude],
            marker = {'color': 'red'}))
    
    for longitude in longitudes:
        fig.add_trace(go.Scattermapbox(
            mode = "lines",
            lon = [longitude, longitude],
            lat = [edges['minLatitude'], edges['maxLatitude']],
            marker = {'color': 'red'}))

    for i in range(20):
        fig.add_trace(go.Scattermapbox(
            mode = "markers",
            lon = [processed_data.iloc[i]['longitude']],
            lat = [processed_data.iloc[i]['latitude']],
            marker = {'color': 'blue', 'size': 20}))
    

    fig.update_layout(
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'center': {'lon': (edges["maxLongitude"] + edges["minLongitude"]) / 2, 'lat': (edges["minLatitude"] + edges["maxLatitude"]) / 2},
            'style': "stamen-terrain",
            'zoom': 5})

    fig.show()