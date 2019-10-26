from pegasus.external_services.airport_legacy import Airport
import time

class Departures(Airport):

    def getDeparturesInSpan(self, startTime, endTime, pagesize=2000, page=1):
        """Taks to timestamps and returns arriving fligths between them"""
        params = { "from": startTime, "till": endTime, "pagesize" : pagesize, "page" : page }
        

        response = self._send_request('/DepartureFlights/Get', params=params)
        if response.status_code != 200:
            return None
        return response.json()

        
        