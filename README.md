# Chat de guilda
Nosso chat de Guilda de WoW Classic é um sistema de comunicação desenvolvido para facilitar a troca de mensagens dentro de um ambiente de guilda (criado com o WoW Classic em mente), utilizando RabbitMQ como broker de mensagens. O sistema é composto por um produtor Java, um backend auditor em Python e múltiplos consumidores Python, cada um associado a diferentes roles dentro da guilda.

## requirements.txt
pip install pika

## Características:
Fila de Mensagens: Gerenciamento eficiente da entrega de mensagens entre produtores e consumidores.
Escalabilidade: Suporta múltiplos produtores e consumidores, adequado para sistemas distribuídos.
Comunicação Assíncrona: Desacopla serviços, melhorando o desempenho e a confiabilidade.
Mensagens baseadas em role: Envie mensagens para roles específicos (tank, healer, dps) ou realize broadcasts para todos os roles.
Backend Auditing: Censura palavras proibidas antes de encaminhar as mensagens para os consumidores.

#Instalação

1. Clone o Repositório
   
```git clone git@github.com:theomilll/Guild_FCCPD.git```

2. Navegue até os diretórios audit_backend e consumer, rode o venv e instale a biblioteca pika

```source /venv/bin/activate```

```pip install pika```

Instalação feita, após isso, basta rodar o MessageProducer.java, Message_Consumer.py e backend_aditoria.py.

Integrantes:

Adaury Neto
Guilherme Alcoforado
Pedro Xavier
Théo Moura
