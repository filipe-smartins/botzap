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
            "options": {
                "delay": 3000,
                "presence": "composing"
            },
            'text': text,
        }
        response = requests.post(
            url=f'{self.BASE_URL}/message/sendText/{self.INSTANCE_NAME}',
            headers=self.__headers,
            json=payload,
        )
        return response.json()
    
    
    def send_buttons(self, number):
        payload = {
            'number': number,
            "buttonMessage": {
            "title": "Olá! Como podemos te ajudar hoje?",
            "description": "Escolha uma das opções abaixo para agilizar seu atendimento:",
            "footerText": "Bot de Atendimento",
            "buttons": [
            {
                "type": "reply",
                "id": "btn_precos",
                "displayText": "Consultar preços"
            },
            {
                "type": "reply",
                "id": "btn_fotos",
                "displayText": "Receber fotos"
            },
            {
                "type": "reply",
                "id": "btn_agendar",
                "displayText": "Agendar visita"
            }
            ]
            }
        }

        response = requests.post(
            url=f'{self.BASE_URL}/message/sendButtons/{self.INSTANCE_NAME}',
            headers=self.__headers,
            json=payload,
        )
        return response.json()
    
    
    def send_list(self, number):
        payload = {
            'number': number,
            "title": "Menu de Atendimento",
            "description": "Selecione o que você deseja fazer hoje:",
            "buttonText": "Abrir Opções",
            "footerText": "Credat Auto",
            "sections": [
                {
                "title": "Serviços Principais",
                "rows": [
                    {
                    "title": "Consultar preços",
                    "description": "Veja nossa tabela atualizada",
                    "rowId": "id_precos"
                    },
                    {
                    "title": "Receber fotos",
                    "description": "Imagens do veículo/produto",
                    "rowId": "id_fotos"
                    },
                    {
                    "title": "Agendar visita",
                    "description": "Marque um horário presencial",
                    "rowId": "id_agendar"
                    }
                ]
                },
                {
                "title": "Outras Opções",
                "rows": [
                    {
                    "title": "Falar com atendente",
                    "description": "Atendimento humano",
                    "rowId": "id_humano"
                    },
                    {
                    "title": "Encerrar",
                    "rowId": "id_sair"
                    }
                ]
                }
            ]
        }

        response = requests.post(
            url=f'{self.BASE_URL}/message/sendList/{self.INSTANCE_NAME}',
            headers=self.__headers,
            json=payload,
        )
        return response.json()
