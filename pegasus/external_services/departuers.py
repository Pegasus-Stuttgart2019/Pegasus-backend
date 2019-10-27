from pegasus.external_services.airport_legacy import Airport
import datetime    
from operator import itemgetter

class Departures(Airport):

    def __init__(self, config, logger):
        super().__init__(config, logger)
        self.time = datetime.datetime.now().timestamp()
        self.departures = self.getDeparturesInSpan(self.time, self.time+2000)

    def getDeparturesById(self, id):
        try:
            for departure in self.departures:
                if departure['AmsId'] == id:
                    return departure
                if departure['Name'] == id or departure['Name'].replace(" ", "") == id:
                    return departure
            return { }
        except Exception:
            return { }

    def getDeparturesInSpan(self, startTime, endTime, pagesize=2000, page=1):
        """Taks to timestamps and returns arriving fligths between them"""
        params = { "from": startTime, "till": endTime, "pagesize" : pagesize, "page" : page }
        

        response = self._send_request('/DepartureFlights/Get', params=params)
        if response.status_code != 200:
            return None
        return response.json()['Items']



    def nextFlightTo(self, destCode ):
        self.departures = self.getDeparturesInSpan(self.time, self.time+20000)
        flights = []
        for dest in self.departures:
            if len(destCode) == 3: 
                if dest['Destination']['Code'].replace(" ", "") == destCode.replace(" ", ""):
                    dest['Plan'] = datetime.datetime.strptime(dest['Plan'], '%Y-%m-%dT%H:%M:%S' ).timestamp()
                    flights.append( dest )
            if dest['Destination']['Name'].replace(" ", "") == destCode.replace(" ", ""):
                dest['Plan'] = datetime.datetime.strptime(dest['Plan'], '%Y-%m-%dT%H:%M:%S' ).timestamp()
                flights.append( dest )
            
        newlist = sorted(flights, key=itemgetter('Plan'))

        return newlist