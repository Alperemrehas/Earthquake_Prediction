import urllib.request, urllib.parse, time
import pandas as pd
import math
import datetime



class APIquery(object):
    """USGS Earthquake API Python3 Wrapper

    KEYWORD ARGUMENTS
        params** -- any USGS earthquake query parameter, for a list and
                    description of parameters, visit:
                        http://comcat.cr.usgs.gov/fdsnws/event/1/
                    for the USGS API web interface, go to:
                        http://earthquake.usgs.gov/earthquakes/search/

    DEFAULT BEHAVIOR
        If query format is indicated as csv or text, a text file is
        written to disk, otherwise the result is returned with the
        call to usgs.APIquery()
    USAGE
        # obtain earthquake events surrounding San Francisco (within 
        # 200 km) since 2013, minimum magnitude of 2.5, in geojson format
        usgs.APIquery(starttime = "2013-01-01", endtime = "",
                      minmagnitude = "2.5",
                      latitude = "37.77", longitude = "-122.44",
                      minradiuskm = "0", maxradiuskm = "200",
                      format = "geojson")
    """

    parameters = {"starttime": "",
                  "endtime": "",
                  "updateafter": "",
                  # rectangular box
                  "minlatitude": "",
                  "maxlatitude": "",
                  "minlongitude": "",
                  "maxlongitude": "",
                  # circle
                  "latitude": "",
                  "longitude": "",
                  "minradius": "",
                  "minradiuskm": "",
                  "maxradius": "",
                  "maxradiuskm": "",
                  # other
                  "mindepth": "",
                  "maxdepth": "",
                  "minmagnitude": "",
                  "maxmagnitude": "",
                  "includeallorigins": "",
                  "includeallmagnitudes": "",
                  "includearrivals": "",
                  "includedelete": "",
                  "eventid": "",
                  "limit": "",
                  "offset": "",
                  "orderby": "",  # time, time-asc, magnitude, magnitude-asc
                  "catalog": "",
                  "contributor": "",
                  # extensions
                  "format": "",  # quakeml, csv, geojson, kml, xml, text
                  "eventtype": "",  # earthquake will limit non-earthquake events
                  "reviewstatus": "",
                  "minmmi": "",
                  "maxmmi": "",
                  "mincdi": "",
                  "maxcdi": "",
                  "minfelt": "",
                  "alertlevel": "",
                  "mingap": "",
                  "maxgap": "",
                  "maxsig": "",
                  "producttype": ""}

    def __init__(self, filename="", **params):

        self.filename = filename
        for param in params.keys():
            if param in self.parameters.keys():
                self.parameters[param] = params[param]
            else:
                raise KeyError("{} is not a USGS api parameter".format(param))
        self.result = self.query()
        if self.parameters["format"] == "csv" or self.parameters["format"] == "text":
            self.writeResult()
        else:
            self.returnResult()

    def query(self):
        """query USGS API at: http://comcat.cr.usgs.gov/fdsnws/event/1/query?"""

        url = "https://earthquake.usgs.gov/fdsnws/event/1/query?{}&".format(
            urllib.parse.urlencode(self.parameters, safe="+:"))
        print("Querying USGS with: {}".format(url))
        with urllib.request.urlopen(url) as usgs:
            response = usgs.read()
        return response

    def returnResult(self):
        """return result from usgs.APIquery() call"""

        print("Returned in {} format, string of length {}".format(self.parameters["format"], len(self.result)))
        return self.result

    def writeResult(self):
        """write result from usgs.APIquery() call to text file"""

        if self.filename:
            filename = self.filename
        else:
            filename = "usgsQuery_{}.{}".format(
                time.strftime("%Y-%m-%d_%H%M", time.localtime()), self.parameters["format"])
        print("Writing results to: {}".format(filename))
        with open(filename, "wb") as btxt:
            btxt.write(self.result)

def preprocesData(plaindata):
    #Only specific columns selected
    processed_data = plaindata.filter(['time','latitude','longitude','mag','place'],axis=1)
    #Checking for any NaN values in dataframe
    check_for_nan = processed_data.isnull().values.any()
    print("There is Nan Values in Dataframe: " , check_for_nan)
    #Cleaning The DF From Earthquakes Which Are Not Occured in Turkey
    earthquakes_tr = processed_data[processed_data.place.str.contains("Turkey")== True]
    #Reseting The Index
    earthquakes_tr = earthquakes_tr.reset_index(drop=True)

    return earthquakes_tr

def extractEdges(df): 
    minRows = df.min()
    maxRows = df.max()

    minLatitude = minRows['latitude']
    minLongitude = minRows['longitude']
    maxLatitude = maxRows['latitude']
    maxLongitude = maxRows['longitude']

    return {
        "minLatitude": minLatitude,
        "minLongitude": minLongitude,
        "maxLatitude": maxLatitude,
        "maxLongitude": maxLongitude
    }


def divideIntoGrid(edges, n, m):
    deltaLatitude = (edges['maxLatitude'] - edges['minLatitude']) / n
    deltaLongitude = (edges['maxLongitude'] - edges['minLongitude']) / m

    latitudes = [edges['minLatitude']]
    longitudes = [edges['minLongitude']]

    for i in range(1, n):
        latitudes.append(edges['minLatitude'] + i * deltaLatitude)
    
    for i in range(1, m):
        longitudes.append(edges['minLongitude'] + i * deltaLongitude)

    latitudes.append(edges['maxLatitude'])
    longitudes.append(edges['maxLongitude'])

    return latitudes, longitudes

def addGridCoordinatesAndYear(df, edges, n, m):
    deltaLatitude = (edges['maxLatitude'] - edges['minLatitude']) / n
    deltaLongitude = (edges['maxLongitude'] - edges['minLongitude']) / m

    ns = []
    ms = []
    years = []

    for row in df.iterrows():
        latitude = row[1]['latitude']
        longitude = row[1]['longitude']

        years.append(row[1]['time'].split('-')[0])
        # print(type(str(row[1]['time'].split('-')[0])))
        
        y = math.ceil((latitude - edges['minLatitude']) / deltaLatitude)
        x = math.ceil((longitude - edges['minLongitude']) / deltaLongitude)

        ns.append(x)
        ms.append(y)
    
    df['x'] = ns
    df['y'] = ms
    df['year'] = years



    


