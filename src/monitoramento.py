#!/usr/bin/env python3
"""
Monitorador de Site CAP-UFRJ com Alerta WhatsApp
Automação para monitorar o site de ingresso do CAP-UFRJ buscando a divulgação do Edital 2026 para ingresso de novos alunos em 2026 e enviar alertas via WhatsApp
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from twilio.rest import Client
import logging
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
SITE_URL = os.getenv('SITE_URL', 'https://www.cap.ufrj.br/index.php/ingresso-no-cap')
PALAVRAS_CHAVE = os.getenv('PALAVRAS_CHAVE', 'Edital 2026,Admissão de Estudantes 2026').split(',')

# Configurações Twilio
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_FROM = os.getenv('TWILIO_FROM', 'whatsapp:+14155238886')
TWILIO_TO = os.getenv('TWILIO_TO')

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def monitorar_site():
    """Monitora o site e envia alertas via WhatsApp"""
    try:
        # Verificar credenciais
        if not all([TWILIO_SID, TWILIO_TOKEN, TWILIO_TO]):
            raise ValueError("Variáveis Twilio não configuradas. Verifique o arquivo .env")
        
        logging.info("Iniciando monitoramento do site CAP-UFRJ...")
        
        # Headers para simular navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Acessar o site
        response = requests.get(SITE_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Analisar conteúdo
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar conteúdo - múltiplos seletores
        seletores = [
            {'name': 'div', 'attrs': {'itemprop': 'articleBody'}},
            {'name': 'article'},
            {'name': 'div', 'class': 'content'},
            {'name': 'main'},
            {'name': 'body'}
        ]
        
        texto_para_buscar = ""
        for seletor in seletores:
            elementos = soup.find_all(**seletor)
            if elementos:
                texto_para_buscar = " ".join([elem.get_text().lower() for elem in elementos])
                logging.info(f" Conteúdo encontrado com seletor: {seletor}")
                break
        
        if not texto_para_buscar:
            texto_para_buscar = soup.get_text().lower()
            logging.warning("  Usando texto completo da página")
        
        # Buscar palavras-chave
        encontrou = False
        termos_encontrados = []
        
        for termo in PALAVRAS_CHAVE:
            if termo.lower() in texto_para_buscar:
                encontrou = True
                termos_encontrados.append(termo)
                logging.info(f" Termo encontrado: '{termo}'")
        
        # Preparar mensagem
        data_hora = datetime.now().strftime("%d/%m/%Y às %H:%M")
        mensagem = f"📋 Monitoramento CAP-UFRJ - {data_hora}\n\n"
        
        if encontrou:
            mensagem += f"🚨 **ALERTA!** Foram encontrados os termos:\n"
            mensagem += f"📌 {', '.join(termos_encontrados)}\n\n"
            mensagem += f"🔗 Acesse: {SITE_URL}"
        else:
            mensagem += "✅ Nenhuma novidade encontrada.\n"
            mensagem += "Não foram localizados os termos monitorados."
        
        # Enviar via WhatsApp
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages.create(
            body=mensagem,
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )
        
        logging.info(f" Mensagem enviada com SID: {message.sid}")
        return True
        
    except Exception as e:
        logging.error(f"❌ Erro no monitoramento: {str(e)}")
        return False

if __name__ == "__main__":
    monitorar_site()
