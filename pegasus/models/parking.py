
import csv
import pathlib
import inspect

class ParkingData():

    def __init__(self):
        """csv fomat: time,carparkid,capacity,currently_used"""
        self.path =  pathlib.Path(inspect.getfile(self.__class__)).parent.joinpath('parkingdata.csv')
        self.data = csv.DictReader(open(self.path))
        self.keys = self.data.fieldnames[0:4]

    def get_all_car_parks(self):
        car_parks = []
        for row in self.data:
            if row['carparkid'] not in car_parks:
                 print(row)
        


        

