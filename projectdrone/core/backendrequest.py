import requests


class BackendRequest:
    # send a get request to a specific address
    @staticmethod
    def sendRequest(path):
        try:
            return requests.get(path)
        except requests.exceptions.RequestException as e:
            print (e)
        return None
