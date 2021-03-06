import data
import numpy as np
import pandas as pd


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



if __name__ == "__main__":
    print("USGS APIquery Example")

    #  Magnitude Greater than 0.1 at Turkey area, 1983 through 2021
    # data.APIquery(starttime="2006-01-01", endtime="2021-05-10",
    # data.APIquery(starttime="2000-01-01", endtime="2005-12-31",
    # data.APIquery(starttime="1994-01-01", endtime="1999-12-31",
    # data.APIquery(starttime="1988-01-01", endtime="1993-12-31",
    # data.APIquery(starttime="1973-01-01", endtime="1987-12-31",
    #          minmagnitude="0.1",
    #          latitude="39.925533", longitude="32.866287",
    #          minradiuskm="0", maxradiuskm="1600",
    #          reviewstatus="reviewed",
    #          filename="usgsQuery_TR_73-87.csv",
    #          format="csv")

    earthquakes = dataReader(method="pd")


    print("***************Raw Data***************")
    print(earthquakes)
    processed_data = data.preprocesData(earthquakes)
    print("The DATA After Drop")
    print(processed_data)
