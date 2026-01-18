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
    

    if body.get('event') != 'messages.upsert':
        return jsonify({'status': 'ignored', 'reason': 'not_upsert'}), 200
    
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    body = request.json
    msg_data = body.get('data', {})
    message_content = msg_data.get('message', {})
    texto = message_content.get('conversation')
    wnumber = msg_data.get('key', {}).get('remoteJid', '') 
    nome = msg_data.get('pushName', '')
    
    #CONFIGURAÇÃO DE PAUSA
    global pausar
    if texto.lower().strip() == 'pausar bot':
        pausar = True
    if texto.lower().strip() == 'reiniciar bot':
        pausar = False
    if pausar:
        return jsonify({'status': 'paused'}), 200


    # APENAS PARA DEBUG
    wnumber = '553197166257@s.whatsapp.net'   
    if msg_data.get('key', {}).get('remoteJid', '') != '553197166257@s.whatsapp.net':
        return jsonify({'status': 'ignored', 'reason': 'not_upsert'}), 200
    

    evo_client = EvolutionAPI()
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM contatos WHERE numero=?", (wnumber,))
    contato = cursor.fetchone()
    if not contato:
        
        evo_client.send_message(
            number=wnumber,
            text=boas_vindas,
        )
        
        cursor.execute("INSERT INTO contatos (numero, nome, status, data_ultimo_contato) VALUES (?, ?, ?, ?)", (wnumber, nome, 'primeiro contato', data_atual))
        conn.commit()
    
    elif "day use" in texto.lower().strip() or "dayuse" in texto.lower().strip() or "convite" in texto.lower().strip() or "diária" in texto.lower().strip() or "diaria" in texto.lower().strip():
        
        evo_client.send_message(
            number=wnumber,
            text=cotas_6_meses,
        )
    
    elif contato[2] == 'concluído':
        pass
    
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
        
        cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('concluído', data_atual, wnumber))
     
    else:
        
        evo_client.send_message(
            number=wnumber,
            text=falar_com_atendente,
        )
        
        cursor.execute("UPDATE contatos SET status=?, data_ultimo_contato=? WHERE numero=?", ('concluído', data_atual, wnumber))

    
    conn.commit()
    
    cursor.close()
    conn.close()

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
