import requests

while True:

    msg = input("MENSAGEM: ")

    url = 'http://localhost:8000/chatbot/webhook/'
    dados = {
        'event': 'messages.upsert', 'instance': 'teste', 'data': {
            'key': {
                'remoteJid': '553185868191@s.whatsapp.net', 'remoteJidAlt': '553185868191@s.whatsapp.net', 'fromMe': True, 
                'id': 'AC34A891FBA79BD8BA8DA34AA33EFE6E', 'participant': '', 'addressingMode': 'lid'
                }, 'pushName': 'Filipe', 'status': 'SERVER_ACK', 'message': {'conversation': msg}, 'messageType': 'conversation', 'messageTimestamp': 1768698788, 'instanceId': 'a5086095-4a41-4217-89f1-1163592e027a', 'source': 'android'}, 'destination': 'http://host.docker.internal:8000/chatbot/webhook/', 'date_time': '2026-01-17T22:13:08.829Z', 'sender': '553185868191@s.whatsapp.net', 'server_url': 'http://localhost:8080', 'apikey': 'EEF311489210-4102-BFBF-430B388449D3'}

    try:
        response = requests.post(url, json=dados)
        print(f"Status Code: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except Exception as e:
        print(f"Erro ao conectar: {e}")
