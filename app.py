from evolution_api import EvolutionAPI
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    body = request.json


    # Dica: Às vezes o Evolution manda eventos de status ou presença. 
    # É bom checar se é uma mensagem nova.
    if body.get('event') != 'messages.upsert':
        return jsonify({'status': 'ignored', 'reason': 'not_upsert'}), 200

    # 2. Acessa o objeto interno 'data'
    msg_data = body.get('data', {})

    wnumber = msg_data.get('key', {}).get('remoteJid', '')
    
    # 4. EXTRAIR A MENSAGEM
    # O WhatsApp muda o campo dependendo se é texto simples ou resposta/link
    message_content = msg_data.get('message', {})
    # Tenta pegar texto simples
    texto = message_content.get('conversation')





    print(f'EVENTO RECEBIDO: {body}')
    
    evo_client = EvolutionAPI()
    
    wnumber = '553185868191@s.whatsapp.net'
    message = f'teste api'
    
    evo_client.send_message(
        number=wnumber,
        text=message,
    )

    evo_client.send_buttons(
        number=wnumber,
    )
    
    evo_client.send_list(
        number=wnumber,
    )

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
