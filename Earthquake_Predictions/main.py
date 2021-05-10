import data
import numpy as np
import pandas as pd


def dataReader(method):
    if(method == "np"):
        earthquakearray = np.genfromtxt("usgsQuery_TR_83-21.csv", delimiter=",",usecols=np.arange(0 ,22))
        np.set_printoptions(linewidth=22)
    else :
        earthquakearray = pd.read_csv("usgsQuery_TR_83-21.csv")
        pd.options.display.max_columns = None
        pd.options.display.max_rows =100
    return earthquakearray



if __name__ == "__main__":
    print("USGS APIquery Example")

    #  Magnitude Greater than 0.1 at Turkey area, 1983 through 2021

    # data.APIquery(starttime="1983-01-01", endtime="2021-05-10",
    #          minmagnitude="0.1",
    #          latitude="39.925533", longitude="32.866287",
    #          minradiuskm="0", maxradiuskm="650",
    #          reviewstatus="reviewed",
    #          filename="usgsQuery_TR_83-21.csv",
    #          format="csv")

    earthquakes = dataReader(method="pd")


    print("***************Raw Data***************")
    print(earthquakes)
    processed_data = data.preprocesData(earthquakes)
    print("The DATA After Drop")
    print(processed_data)
