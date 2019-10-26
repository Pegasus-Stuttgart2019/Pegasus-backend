from pegasus.external_services.airport_legacy import Airport


class Airlines(Airport):

    def __init__(self, config, logger):
        super().__init__(config, logger)
        self.airlines = self.getAirlines()

    def getAirlines(self):
        return self._send_request('/Airlines/Get').json()
        
        