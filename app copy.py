from evolution_api import EvolutionAPI
from flask import Flask, request, jsonify
from time import sleep
import sqlite3
from datetime import datetime
from respostas import *

app = Flask(__name__)


@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    body = request.json


    #print(f'BODY RECEBIDO: {body}')

    # Dica: Às vezes o Evolution manda eventos de status ou presença. 
    # É bom checar se é uma mensagem nova.
    if body.get('event') != 'messages.upsert' and msg_data.get('key', {}).get('remoteJid', '') != '553185868191@s.whatsapp.net':
        return jsonify({'status': 'ignored', 'reason': 'not_upsert'}), 200

    # 2. Acessa o objeto interno 'data'
    msg_data = body.get('data', {})
    # 4. EXTRAIR A MENSAGEM
    # O WhatsApp muda o campo dependendo se é texto simples ou resposta/link
    message_content = msg_data.get('message', {})
    # Tenta pegar texto simples
    texto = message_content.get('conversation')

    #print(f'MSG DATA RECEBIDO: {texto}')

    wnumber = msg_data.get('key', {}).get('remoteJid', '')
    
    #print(f'wnumber: {wnumber}')
    
    nome = msg_data.get('pushName', '')
    
    #print(f'nome: {nome}')
    
    cursor.execute("SELECT * FROM contatos WHERE numero=?", (wnumber,))
    contato = cursor.fetchone()
    if not contato:
        
        print(boas_vindas)
        print(sobre_o_valor)
        
        cursor.execute("INSERT INTO contatos (numero, nome, status, data_ultimo_contato) VALUES (?, ?, ?, ?)", (wnumber, nome, 'primeiro contato', data_atual))
        conn.commit()
    
    elif contato[2] == 'primeiro contato':
        
        if texto.lower().strip().isdigit():
        
            if int(texto.strip()) == 1:
                print(cota_1_ano_1_pessoa)
                print(decisao)
            elif int(texto.strip()) == 2:
                print(cota_1_ano_2_pessoas)
                print(decisao)
            elif int(texto.strip()) == 3:
                print(cota_1_ano_3_pessoas)
                print(decisao)
            elif int(texto.strip()) == 4:
                print(cota_1_ano_4_pessoas)
                print(decisao)
            else:
                print(cota_1_ano_5_pessoas)
                print(decisao)
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('selecionado número de pessoas na cota', data_atual, wnumber))
        else:
            print(nao_entendi_numero_pessoas)
    elif contato[2] == 'selecionado número de pessoas na cota':
        if texto.lower().strip() == 'sim':
            print(decisao_positiva)
            print(final_agradecimento)
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('finalizado com decisão positiva', data_atual, wnumber))
        elif texto.lower().strip() == 'não' or texto.lower().strip() == 'nao':
            print(decisao_negativa)
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('decisão negativa', data_atual, wnumber))
        else:
            print(não_entendi_decisao)
    
    
    elif contato[2] == 'decisão negativa':        
        if texto.lower().strip() == 'sim':
            print(cotas_6_meses)
            print(decisao)
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('enviado valores das cotas de 6 meses', data_atual, wnumber))
        elif texto.lower().strip() == 'não' or texto.lower().strip() == 'nao':
            print(decisao_negativa_final)
            print(final_agradecimento)
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('decisão negativa final', data_atual, wnumber))
        else:
            print(não_entendi_decisao)
        
    elif contato[2] == 'enviado valores das cotas de 6 meses':
        if texto.lower().strip() == 'sim':
            print(decisao_positiva)
            print(final_agradecimento)
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('finalizado com decisão positiva', data_atual, wnumber))
        elif texto.lower().strip() == 'não' or texto.lower().strip() == 'nao':
            print(decisao_negativa_final)
            print(final_agradecimento)
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('decisão negativa final', data_atual, wnumber))
        else:
            print(não_entendi_decisao)


    elif texto.lower().strip() == 'falar com atendente':
        print(falar_com_atendente)


    else:
        print(falar_com_atendente)


    """

    print(f'EVENTO RECEBIDO: {body}')
    
    
    
    wnumber = '553185868191@s.whatsapp.net'
    message = f'teste api'
    
    evo_client.send_message(
        number=wnumber,
        text=message,
    )
    """
    
    conn.commit()
    
    cursor.close()
    conn.close()

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
