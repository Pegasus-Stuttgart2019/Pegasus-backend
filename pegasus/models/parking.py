
import csv
import pathlib
import inspect
import time 
class ParkingData():

    def __init__(self):
        """csv fomat: time,carparkid,capacity,currently_used"""
        self.path =  pathlib.Path(inspect.getfile(self.__class__)).parent.joinpath('parkingdata.csv')
        self.data = csv.DictReader(open(self.path))
        self.keys = self.data.fieldnames[0:4]
        # tupe(Termial 1, Terminal 2, Termina 3 ) walking time in min
        self.waking_time = {
            'P00': ( 10, 12, 14 ),
            'P02': ( 13, 13, 15 ),
            'P03': ( 5, 6, 7 ),
            'P04': ( 7, 10, 15 ),
            'P05': ( 7, 8, 9 ),
            'P06': ( 7, 5, 5 ),
            'P08': ( 60, 60, 60 ),
            'P09': ( 60, 60, 60 ),
            'P11': ( 60, 60, 60 ),
            'P21': ( 60, 60, 60 ),
            'P22': ( 60, 60, 60 ),
            'P23': ( 60, 60, 60 ),
            'P24': ( 60, 60, 60 ),
            'P25': ( 60, 60, 60 ),
            'P07': ( 6, 3, 5 ),
            'P12': ( 10, 7, 6 ),
            'P14': ( 8, 6, 4 ),
            'P15': ( 16, 18, 18 ),
            'P20': ( 25, 26, 25 ),
        }

    def get_all_car_parks(self):
        car_parks = []
        for row in self.data:
            if row['carparkid'] not in car_parks:
                car_parks.append(row['carparkid'])
        return tuple(car_parks)

    def find_best_parkingspace(self, arrivaleTime, Terminal ):
        """ arrivaleTime: datatime Terminal: 1,2,3"""
        h, m = self._roundTime((10,25))
        best_parkspace = "P07"
        best_value = 1000
        alternativs = []

        for row in self.data:
            if row['time'] == f"{h}:{m}":
                value = self.waking_time[row['carparkid']][Terminal-1]
                if best_value > value:
                    alternativs.append(( best_parkspace, best_value ))
                    best_value = value
                    best_parkspace = row['carparkid']
        return ( (best_parkspace, best_value ) , tuple(alternativs))


    def _roundTime(self, arravleTime):
        """tupe(hh,mm) always returns 10:30"""
        return (10, 30)

        



        

