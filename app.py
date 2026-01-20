from email import message
from evolution_api import EvolutionAPI
from flask import Flask, request, jsonify
from time import sleep
import sqlite3
from datetime import datetime
from respostas import *

app = Flask(__name__)

pausar = False

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    
    body = request.json

    if body.get('event') != 'messages.upsert':
        return jsonify({'status': 'ignored', 'reason': 'not_upsert'}), 200
    
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    

    msg_data = body.get('data', {})
    message_content = msg_data.get('message', {})
    texto = message_content.get('conversation')
    wnumber = msg_data.get('key', {}).get('remoteJid', '') 
    nome = msg_data.get('pushName', '')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
        
    cursor.execute("INSERT INTO contatos (numero, nome, status, data_ultimo_contato) VALUES (?, ?, ?, ?)", (wnumber, nome, 'primeiro contato', data_atual))
    conn.commit()
    
    #CONFIGURAÇÃO DE PAUSA
    global pausar
    if texto and texto.lower().strip() == 'pausar bot':
        pausar = True
    if texto and texto.lower().strip() == 'reiniciar bot':
        pausar = False
    if pausar:
        return jsonify({'status': 'paused'}), 200


    # APENAS PARA DEBUG
    #wnumber = '553185868191@s.whatsapp.net'   
    #if msg_data.get('key', {}).get('remoteJid', '') != '553185868191@s.whatsapp.net':
    #    return jsonify({'status': 'ignored', 'reason': 'not_upsert'}), 200
    

    evo_client = EvolutionAPI()
        
    
    if "day use" in texto.lower().strip() or "dayuse" in texto.lower().strip() or "convite" in texto.lower().strip() or "diária" in texto.lower().strip() or "diaria" in texto.lower().strip():
        
        evo_client.send_message(
            number=wnumber,
            text=cotas_6_meses,
        )
        
    elif texto.lower().strip().isdigit():
    
        if int(texto.strip()) == 1:
            
            evo_client.send_message(
                number=wnumber,
                text=cota_1_ano_1_pessoa,
            )
            
            evo_client.send_message(
                number=wnumber,
                text=decisao,
            )
            
        elif int(texto.strip()) == 2:
            evo_client.send_message(
                number=wnumber,
                text=cota_1_ano_2_pessoas,
            )
            
            evo_client.send_message(
                number=wnumber,
                text=decisao,
            )
        elif int(texto.strip()) == 3:
            
            evo_client.send_message(
                number=wnumber,
                text=cota_1_ano_3_pessoas,
            )
            
            evo_client.send_message(
                number=wnumber,
                text=decisao,
            )
            
        elif int(texto.strip()) == 4:
            
            evo_client.send_message(
                number=wnumber,
                text=cota_1_ano_4_pessoas,
            )
            
            evo_client.send_message(
                number=wnumber,
                text=decisao,
            )
        elif int(texto.strip()) > 4 and int(texto.strip()) <= 10:
            evo_client.send_message(
                number=wnumber,
                text=cota_1_ano_5_pessoas,
            )
            
            evo_client.send_message(
                number=wnumber,
                text=decisao,
            )

    
    cursor.close()
    conn.close()

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
