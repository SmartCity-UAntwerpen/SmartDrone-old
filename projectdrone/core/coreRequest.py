import requests
class coreRequest:
    @staticmethod
    def sendRequest(path):
        try:
            return requests.get(path)
        except requests.exceptions.RequestException as e:
            print (e)
        return None