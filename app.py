from evolution_api import EvolutionAPI
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json

    print(f'EVENTO RECEBIDO: {data}')
    
    evo_client = EvolutionAPI()
    
    wnumber = '553185868191@s.whatsapp.net'
    message = f'teste api'
    
    evo_client.send_message(
        number=wnumber,
        text=message,
    )

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
