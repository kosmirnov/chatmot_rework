import requests

# class Access_Token():
#     def __init__(self,):

def retry(max_attempts):
    def decorator(func):
        def wrapper(*args,**kwargs):
            for i in range(max_attempts):
                try:
                    output = func(*args,**kwargs)
                    return output
                except requests.Timeout:
                    if i == max_attempts-1:
                        raise
        return wrapper
    return decorator


@retry
class DVSA_API_Client():
    def __init__(self,timeout:int, api_key:str, access_token:str):
        self.base_url = 'https://history.mot.api.gov.uk/v1/trade/vehicles/registration/'
        self.timeout = timeout
        self.api_key = api_key
        self.access_token = access_token
    def get_mot_history(self,registration):
        path = self.base_url + registration
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "x-api-key": self.api_key,
            "Accept": "application/json",
        }
        response = requests.get(path, timeout=self.timeout, headers=headers)
        response.raise_for_status()
        return response.json()
