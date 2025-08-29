# Monitorador CAP-UFRJ - WhatsApp Alerts

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-green)](https://twilio.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

Um sistema automatizado que monitora o site do CAP-UFRJ em busca de novidades sobre processos seletivos com horário programado e envia um alerta instantâneo via WhatsApp caso encontre ou não os termos buscados.

## Funcionalidades

- ✅ **Monitoramento Automático** - Verifica diariamente o site do CAP-UFRJ
- ✅ **Busca Inteligente** - Procura por termos específicos como "Edital 2026", "Admissão de Estudantes 2026"
- ✅ **Alertas WhatsApp** - Notificações instantâneas no seu celular
- ✅ **Logs Detalhados** - Registro completo de todas as execuções
- ✅ **Configuração Segura** - Variáveis de ambiente protegidas
- ✅ **Agendamento Flexível** - Execução automática personalizável

## Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **BeautifulSoup4** - Web scraping e parsing HTML
- **Twilio API** - Integração com WhatsApp
- **Requests** - Requisições HTTP
- **python-dotenv** - Gerenciamento de variáveis de ambiente


## Pré-requisitos

Antes de começar, você precisará:

1. **Conta no [Twilio](https://twilio.com)** - Para API do WhatsApp
2. **Conta no [GitHub](https://github.com)** - Para hospedagem do código
3. **Python 3.8+** instalado
4. **Acesso SSH** configurado no GitHub
5. **WhatsApp** no celular para receber alertas

## Configuração Rápida

### 1. Clone o repositório
```bash
git clone git@github.com:anacvieiraa/monitorador-cap-ufrj.git
cd monitorador-cap-ufrj
```

### 2. Configure o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
nano .env  # ou use seu editor favorito
```

Preencha o arquivo `.env` com suas credenciais:
```env
# Twilio Configuration
TWILIO_SID=seu_account_sid_twilio_aqui
TWILIO_TOKEN=seu_auth_token_twilio_aqui
TWILIO_FROM=whatsapp:+14155238886
TWILIO_TO=whatsapp:+5511999999999

# Application Settings
SITE_URL=https://www.cap.ufrj.br/index.php/ingresso-no-cap
PALAVRAS_CHAVE=Edital 2026,Admissão de Estudantes 2026
```

### 5. Teste a configuração
```bash
python src/monitoramento.py
```

## Configuração do Twilio

### 1. Crie uma conta no [Twilio](https://twilio.com)
### 2. Acesse o Console → WhatsApp → Sandbox
### 3. Vincule seu número ao Sandbox:
1. Adicione `+14155238886` como contato no WhatsApp
2. Envie a mensagem: `join exemplo-12` (use o código do seu Sandbox)
3. Aguarde a confirmação do Twilio

### 4. Obtenha suas credenciais:
- **Account SID**: Encontrado no Dashboard
- **Auth Token**: Disponível nas configurações da conta

## Deploy na AWS EC2

### 1. Crie uma instância EC2
- AMI: Ubuntu 22.04 LTS
- Tipo: t3.micro (Gratuito)
- Configure regras de segurança: SSH (22), HTTP (80), HTTPS (443)

### 2. Conecte via SSH
```bash
ssh -i sua-chave.pem ubuntu@ip-da-instancia
```

### 3. Configure o ambiente
```bash
sudo apt update
sudo apt install python3-pip python3-venv git -y
git clone git@github.com:anacvieiraa/monitorador-cap-ufrj.git
cd monitorador-cap-ufrj
```

### 4. Siga os passos de configuração anteriores

### 5. Configure agendamento automático
```bash
crontab -e
```

Adicione a linha (executa diariamente às 12:00 horário de Brasília):
```bash
0 15 * * * cd /home/ubuntu/monitorador-cap-ufrj && /home/ubuntu/monitorador-cap-ufrj/venv/bin/python /home/ubuntu/monitorador-cap-ufrj/src/monitoramento.py >> /home/ubuntu/cron.log 2>&1
```

## Estrutura do Projeto

```
monitorador-cap-ufrj/
├── .gitignore
├── .env.example
├── requirements.txt
├── README.md
├── src/
│   └── monitoramento.py
├── config/
│   └── settings.py
└── scripts/
    └── setup.sh
```

## Personalização

### Alterar palavras-chave
Edite `PALAVRAS_CHAVE` no arquivo `.env`:
```env
PALAVRAS_CHAVE=Admissão de Estudantes 2026,Edital 2026
```

### Modificar frequência de verificação
Ajuste o agendamento no crontab:
```bash
# Verificar a cada hora
0 * * * * 

# Verificar diariamente às 09:00
0 9 * * * 

# Verificar a cada 6 horas
0 */6 * * * 
```

## Solução de Problemas

### Erro de autenticação Twilio
```bash
# Verifique se as variáveis de ambiente estão corretas
echo $TWILIO_SID
echo $TWILIO_TOKEN
```

### Erro de conexão
```bash
# Teste a conectividade
python -c "import requests; print(requests.get('https://www.cap.ufrj.br').status_code)"
```

### Erro de agendamento
```bash
# Verifique os logs do cron
tail -f /home/ubuntu/cron.log
```

## Monitoramento

### Verificar logs de execução
```bash
# Logs da aplicação
cat /home/ubuntu/monitorador-cap-ufrj/monitoramento.log

# Logs do agendador
cat /home/ubuntu/cron.log
```

### Testar manualmente
```bash
cd /home/ubuntu/monitorador-cap-ufrj
source venv/bin/activate
python src/monitoramento.py
```

## Contribuindo

Contribuições são bem-vindas! Siga estos passos:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Conceitos Utilizados na prática

- `Python`: Web Scraping, Manipulação de Strings, Requisições HTTP, Manipulação de Datas, Tratamento de Exceções, Ambientes Virtuais (venv) e gerenciamento de dependências, Variáveis de Ambiente e configuração segura e Parsing de HTML.

- `Automação`: Agendamento de Tarefas com Cron (Linux), Monitoramento Contínuo de fontes de dados, Execução Automática sem intervenção humana, Notificações Proativas baseadas em eventos, Scripting para automação de processos.

- `Conceitos de Integração`: APIs RESTful (Twilio WhatsApp API), Autenticação com tokens e chaves API, Comunicação entre Sistemas (Python ↔ Twilio ↔ WhatsApp) e Webhooks (conceito por trás do Twilio).

- `Conceitos de Cloud/DevOps`: Deploy em Cloud (AWS EC2), Configuração de Servidores Linux, SSH e conexão remota segura, Gestão de Instâncias na nuvem e Variáveis de Ambiente para configuração.

- `Conceitos de Segurança`: Proteção de Credenciais com variáveis de ambiente, GitHub Secrets Protection, Chaves SSH para autenticação segura, Gitignore para evitar commit de dados sensíveis e Tokens de Acesso em vez de senhas.

- `Conceitos de Monitoramento`: Logging estruturado e persistente, Rastreamento de Execuções, Alertas em Tempo Real e Status Reporting.

- `Conceitos de Desenvolvimento`: Versionamento com Git, Documentação técnica (README), Estrutura de Projeto organizada e configuração fácil de se reproduzir.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## Agradecimentos

- Twilio pela excelente API de WhatsApp
- Comunidade Python pelas incríveis bibliotecas
- Curso de Python da Hashtag Treinamentos

## Suporte

Se encontrar problemas ou tiver dúvidas:

1. Verifique a [documentação do Twilio](https://www.twilio.com/docs/whatsapp)
2. Consulte as [issues do GitHub](https://github.com/anacvieiraa/monitorador-cap-ufrj/issues)
3. Entre em contato através do GitHub

---

⭐ **Se este projeto foi útil, deixe uma star no GitHub!**
