import pika
import os
import re

EXCHANGE_NAME = 'guilda_exchange'
EXCHANGE_TYPE = 'fanout'

# Lista de palavras proibidas
PROHIBITED_WORDS = ['raid', 'massacre', 'steal']  # Substitua pelas palavras reais

def censurar_mensagem(mensagem):
    for palavra in PROHIBITED_WORDS:
        mensagem = re.sub(palavra, '*' * len(palavra), mensagem, flags=re.IGNORECASE)
    return mensagem

def callback(ch, method, properties, body):
    mensagem = body.decode()
    censurada = censurar_mensagem(mensagem)
    print(f" [AUDITORIA] {censurada}")

def main():
    # AMQP URI do CloudAMQP
    amqp_url = 'amqps://dzrfdabj:XauaSYvj4PxJi96VY6Iowsrlfq2lMA9Y@prawn.rmq.cloudamqp.com/dzrfdabj'

    # Alternativamente, use variáveis de ambiente
    # amqp_url = os.getenv('CLOUDAMQP_URL')

    parameters = pika.URLParameters(amqp_url)
    try:
        connection = pika.BlockingConnection(parameters)
    except pika.exceptions.AMQPConnectionError as e:
        print("Erro ao conectar ao RabbitMQ:", e)
        return

    channel = connection.channel()

    # Declara o exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE, durable=True)

    # Cria uma fila exclusiva para este consumidor
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Liga a fila ao exchange
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

    print(' [AUDITORIA] Aguardando mensagens para auditoria. Para sair, pressione CTRL+C')

    # Consumidor
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(" [AUDITORIA] Consumidor interrompido")
        channel.stop_consuming()
    finally:
        connection.close()

if __name__ == "__main__":
    main()
