from pegasus.external_services.airport_legacy import Airport
import datetime

class Departures(Airport):

    def __init__(self, config, logger):
        super().__init__(config, logger)
        self.time = datetime.datetime.now().timestamp()
        self.departures = self.getDeparturesInSpan(self.time-1000, self.time+2000)

    def getDeparturesById(self, id):
        for departure in self.departures:
            if departure['AmsId'] == id:
                return departure
            if departure['Name'] == id or departure['Name'].replace(" ", "") == id:
                return departure
        return "False"

    def getDeparturesInSpan(self, startTime, endTime, pagesize=2000, page=1):
        """Taks to timestamps and returns arriving fligths between them"""
        params = { "from": startTime, "till": endTime, "pagesize" : pagesize, "page" : page }
        

        response = self._send_request('/DepartureFlights/Get', params=params)
        if response.status_code != 200:
            return None
        return response.json()['Items']

        
        