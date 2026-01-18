# Chatbot IA para WhatsApp com EvolutionAPI

Clonar repo e subir containers:

```bash
cd ~
git clone git@github.com:filipe-smartins/botzap.git
cd botzap
sudo docker compose up -d
```

Configurar o webhook na instância > Events > Webhook para o link abaixo.

http://host.docker.internal:8000/chatbot/webhook/

marcar CHATS_UPSERT e MESSAGES_UPSERT

Para parar o bot:

pausar bot

Para reinificar o bot:

reinificar bot
