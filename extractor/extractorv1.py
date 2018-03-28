import requests
import json
import time
import datetime

# Import MySQl
from mysql.connector import (connection, cursor)
from gevent.libev.corecext import stat


class Extractor:
     
    avg_available_stand = {}
    avg_available_bike = {}
    lat_long = {}
    
    def __init__(self):
        
        
        """
        Aim of this class is to return a dictionary that holds an entry for every station.
        This entry will consist of a bi-dimensional dictionary. The first level of this 
        dictionary will hold entries for each hour of the day (from 0 to 23). Each hour
        entry will correspond to an average value for that period.
        """
        
        #constructor sets up database connection and creates tuple that holds all station names
        
        self.conex = connection.MySQLConnection(user='root', password='Rugby_777', host='0.0.0.0', database='dublinbikes')
        # MySQL object
        self.cursor = self.conex.cursor()
        
        station_names_query = "SELECT distinct(Name) FROM data"
        
        self.cursor.execute(station_names_query)
        
        self.station_names = self.cursor.fetchall()
        
        
    
    def avg_available_stand(self):
        
        #loop through all station names
        
        for j in self.station_names:
            
            
            #for each station name 
            for i in range(0, 24):
                total_tuple = selectHour(i, "Available_Bike_Stands")
                #returns tuple with all values relevant to the selected time period
                total = 0
                for x in total_tuple:
                    total += int(x)
                avg = total / len(total_tuple)
                
                self.avg_available_stand[j][i] = avg
                
            
            
    def avg_available_bike(self):
        
        for j in self.station_names:
        
            for i in range(0, 24):
                
                total_tuple = selectHour(i, "Available_Bikes")
                #returns tuple with all values relevant to the selected time period
                total = 0
                for x in total_tuple:
                    total += int(x)
                avg = total / len(total_tuple)
                
                self.avg_available_stand[j][i] = avg
                
    def selectStation(self, x, h):
        
        query = 'SELECT distinct(%s) FROM dublinbikes.data WHERE name = "%s"' % (x , h)
        
        self.cursor.execute(query)
        
        output = self.cursor.fetchall()
        
        return output
                
    def getLatAndLong(self):
        
        #method queries the latitude and longitude of each station and appends
        #a dictionary containing the lat and long onto a dictionary that holds
        #information for each station (lat&long)
        
        for j in self.station_names:
    
            lat = self.selectStation('position_lat', j[0])
            long = self.selectStation('position_lng', j[0])
            
            self.lat_long[j[0]] = {"latitude":float(lat[0][0]), "longitude":float(long[0][0])}
            
            
    
            
    def selectHour(self, h, x):
        
        #query needs completion
        query = "SELECT %s FROM data WHERE = %s;" % x , h
        
        cursor.execute(query)
        
        output = cursor.fetchall()
        
        return output
    
    
    
    def closeConex(self):
        
        self.conex.close()
        
