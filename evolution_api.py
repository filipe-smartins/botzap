import os
import requests
from dotenv import load_dotenv


load_dotenv()


EVOLUTION_API_URL = os.getenv('EVOLUTION_API_URL')
EVOLUTION_INSTANCE_NAME = os.getenv('EVOLUTION_INSTANCE_NAME')
EVOLUTION_AUTHENTICATION_API_KEY = os.getenv('AUTHENTICATION_API_KEY')



class EvolutionAPI:

    BASE_URL = EVOLUTION_API_URL
    INSTANCE_NAME = EVOLUTION_INSTANCE_NAME
    def __init__(self):
        self.__api_key = EVOLUTION_AUTHENTICATION_API_KEY
        self.__headers = {
            'apikey': self.__api_key,
            'Content-Type': 'application/json'
        }

    def send_message(self, number, text):
        payload = {
            'number': number,
            'text': text,
        }
        response = requests.post(
            url=f'{self.BASE_URL}/message/sendText/{self.INSTANCE_NAME}',
            headers=self.__headers,
            json=payload,
        )
        return response.json()
