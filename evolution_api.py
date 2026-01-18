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

    def send_message(self, number, text, delay=5000):   
        payload = {
            "number": number,
            "text": text,
            "delay": delay # O delay fica na raiz do JSON (em milissegundos)
            #"linkPreview": True # Opcional: Adiciona prévia se houver link
        }
        response = requests.post(
            url=f'{self.BASE_URL}/message/sendText/{self.INSTANCE_NAME}',
            headers=self.__headers,
            json=payload,
        )
        return response.json()
    
    def get_contact(self, number):
        response = requests.get(
            url=f'{self.BASE_URL}/contact/get/{self.INSTANCE_NAME}/{number}',
            headers=self.__headers,
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
        # DEFINIÇÃO DAS SEÇÕES (Isso não muda)
        sections = [
            {
                "title": "Serviços Principais",
                "rows": [
                    {"title": "Consultar preços", "description": "Veja tabela", "rowId": "id_precos"},
                    {"title": "Receber fotos", "description": "Imagens", "rowId": "id_fotos"},
                    {"title": "Agendar visita", "description": "Presencial", "rowId": "id_agendar"}
                ]
            },
            {
                "title": "Outras Opções",
                "rows": [
                    {"title": "Falar com atendente", "description": "Humano", "rowId": "id_humano"},
                    {"title": "Encerrar", "rowId": "id_sair"}
                ]
            }
        ]

        # PAYLOAD CORRIGIDO (COM ENVELOPE listMessage)
        payload = {
            'number': number,
            # NÃO coloque "options" aqui
            # NÃO coloque "title", "sections" soltos na raiz aqui.
            
            # AQUI ESTÁ A CORREÇÃO MÁGICA:
            "listMessage": {
                "title": "Menu de Atendimento",
                "description": "Selecione o que você deseja fazer hoje:",
                "buttonText": "Abrir Opções",
                "footerText": "Credat Auto",
                "sections": sections,
                "listType": 1 # 1 = SINGLE_SELECT (Padrão)
            }
        }

        response = requests.post(
            url=f'{self.BASE_URL}/message/sendList/{self.INSTANCE_NAME}',
            headers=self.__headers,
            json=payload,
        )
        return response.json()
