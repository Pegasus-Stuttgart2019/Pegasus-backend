import requests


class Airport:
    """config: logger"""
    def __init__(self, config, logger):

        self.base_url = config["LEGACYURL"]
        self.apikey = config["APIKEY"]
        self._session = requests.Session()
        self._logger = logger

    def _send_request(self, url_extension, method="get", params=None):
        headers = {
            # Request headers
            "Ocp-Apim-Subscription-Key": self.apikey
        }

        if method == "get":
            response = self._session.get(
                self.base_url + url_extension, params=params, headers=headers
            )


        if response.status_code != 200:
            self._logger.error(
                f"Couln't fetch data from {self.base_url}{url_extension} with status code {response.status_code}"
            )

        return response