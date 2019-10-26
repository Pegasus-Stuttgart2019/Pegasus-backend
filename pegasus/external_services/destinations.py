from pegasus.external_services.airport_legacy import Airport


class Destionations(Airport):

    def __init__(self, config, logger):
        super().__init__(config, logger)
        self.destinations = self._send_request('/Flightplan/GetAirports').json()

    def getDestinationCode(self, dcode):
        print("code")
        for dest in self.destinations:
            if dest['Code'] == dcode:
                return dest
        return { }

    def getDestinationName(self, name):
        print("name")
        for dest in self.destinations:
            if dest['Name'].replace(" ", "") == name.replace(" ", ""):
                return dest
        return { }
          