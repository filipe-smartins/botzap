from email import message
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


    # 2. Acessa o objeto interno 'data'
    msg_data = body.get('data', {})
    # 4. EXTRAIR A MENSAGEM
    # O WhatsApp muda o campo dependendo se é texto simples ou resposta/link
    message_content = msg_data.get('message', {})
    # Tenta pegar texto simples
    texto = message_content.get('conversation')

    #print(f'MSG DATA RECEBIDO: {texto}')

    wnumber = msg_data.get('key', {}).get('remoteJid', '')


    #print(f'BODY RECEBIDO: {body}')

    # Dica: Às vezes o Evolution manda eventos de status ou presença. 
    # É bom checar se é uma mensagem nova.
    if body.get('event') != 'messages.upsert' or msg_data.get('key', {}).get('remoteJid', '') != '553185471996@s.whatsapp.net':
        return jsonify({'status': 'ignored', 'reason': 'not_upsert'}), 200

    
    wnumber = '553185471996@s.whatsapp.net'
    
    #print(f'wnumber: {wnumber}')
    
    nome = msg_data.get('pushName', '')
    
    #print(f'nome: {nome}')
    
    evo_client = EvolutionAPI()
    
    cursor.execute("SELECT * FROM contatos WHERE numero=?", (wnumber,))
    contato = cursor.fetchone()
    if not contato:
        
        evo_client.send_message(
            number=wnumber,
            text=boas_vindas,
        )
        sleep(1)
        evo_client.send_message(
            number=wnumber,
            text=sobre_o_valor,
        )
        
        cursor.execute("INSERT INTO contatos (numero, nome, status, data_ultimo_contato) VALUES (?, ?, ?, ?)", (wnumber, nome, 'primeiro contato', data_atual))
        conn.commit()
    
    elif contato[2] == 'primeiro contato':
        
        if texto.lower().strip().isdigit():
        
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
            else:
                evo_client.send_message(
                    number=wnumber,
                    text=cota_1_ano_5_pessoas,
                )
                
                evo_client.send_message(
                    number=wnumber,
                    text=decisao,
                )
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('selecionado número de pessoas na cota', data_atual, wnumber))
        else:
                evo_client.send_message(
                    number=wnumber,
                    text=nao_entendi_numero_pessoas,
                )
            
            
    elif contato[2] == 'selecionado número de pessoas na cota':
        if texto.lower().strip() == 'sim':
            
            evo_client.send_message(
                number=wnumber,
                text=decisao_positiva,
            )
                        
            evo_client.send_message(
                number=wnumber,
                text=final_agradecimento,
            )            
            
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('finalizado com decisão positiva', data_atual, wnumber))
        elif texto.lower().strip() == 'não' or texto.lower().strip() == 'nao':
            
            evo_client.send_message(
                number=wnumber,
                text=decisao_negativa,
            )   
            
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('decisão negativa', data_atual, wnumber))
        else:
            
            evo_client.send_message(
                number=wnumber,
                text=não_entendi_decisao,
            )    
    
    elif contato[2] == 'decisão negativa':        
        if texto.lower().strip() == 'sim':
            
            evo_client.send_message(
                number=wnumber,
                text=cotas_6_meses,
            )
            
            evo_client.send_message(
                number=wnumber,
                text=decisao,
            )
            
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('enviado valores das cotas de 6 meses', data_atual, wnumber))
        elif texto.lower().strip() == 'não' or texto.lower().strip() == 'nao':
            
            evo_client.send_message(
                number=wnumber,
                text=decisao_negativa_final,
            )
            
            evo_client.send_message(
                number=wnumber,
                text=final_agradecimento,
            )

            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('decisão negativa final', data_atual, wnumber))
        else:
            evo_client.send_message(
                number=wnumber,
                text=não_entendi_decisao,
            )

        
    elif contato[2] == 'enviado valores das cotas de 6 meses':
        if texto.lower().strip() == 'sim':
            
            evo_client.send_message(
                number=wnumber,
                text=decisao_positiva,
            )
            evo_client.send_message(
                number=wnumber,
                text=final_agradecimento,
            )
            
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('finalizado com decisão positiva', data_atual, wnumber))
        elif texto.lower().strip() == 'não' or texto.lower().strip() == 'nao':
            evo_client.send_message(
                number=wnumber,
                text=decisao_negativa_final,
            )
            evo_client.send_message(
                number=wnumber,
                text=final_agradecimento,
            )
            cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('decisão negativa final', data_atual, wnumber))
        else:
            
            evo_client.send_message(
                number=wnumber,
                text=não_entendi_decisao,
            )

    elif texto.lower().strip() == 'falar com atendente':
        
        evo_client.send_message(
            number=wnumber,
            text=falar_com_atendente,
        )
        
    else:
        
        evo_client.send_message(
            number=wnumber,
            text=falar_com_atendente,
        )

    
    conn.commit()
    
    cursor.close()
    conn.close()

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
