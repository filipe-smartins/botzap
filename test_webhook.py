import requests

url = 'http://localhost:8000/chatbot/webhook/'
dados = {'msg': 'Testando conexão', 'de': 'Evolution API'}

try:
    response = requests.post(url, json=dados)
    print(f"Status Code: {response.status_code}")
    print(f"Resposta: {response.json()}")
except Exception as e:
    print(f"Erro ao conectar: {e}")
