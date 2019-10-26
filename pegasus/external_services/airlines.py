from pegasus.external_services.airport_legacy import Airport


class Airlines(Airport):


    def getAirlines(self):
        airlines = self._send_request('/Airlines/Get').json()
        
        