from pegasus.external_services.airport_legacy import Airport
import random
class Shops(Airport):

    def __init__(self, config, logger):
        super().__init__(config, logger)
        self.data = self._send_request('/Apps/Infostelen/Get').json()

    def get_recomendation(self):
        return self.data[random.randint(0, len(self.data))]
