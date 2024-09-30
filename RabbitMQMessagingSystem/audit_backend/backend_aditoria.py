import pika
import os
import re

EXCHANGE_NAME = 'guilda_direct_exchange'
EXCHANGE_TYPE = 'direct'

CENSORED_EXCHANGE = 'censored_direct_exchange'
CENSORED_EXCHANGE_TYPE = 'direct'

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

    # Publicar censurada no censored_direct_exchange com a mesma routing key (role)
    try:
        ch.basic_publish(
            exchange=CENSORED_EXCHANGE,
            routing_key=method.routing_key,  # Mantém a mesma routing key
            body=censurada.encode('utf-8'),
            properties=pika.BasicProperties(
                delivery_mode=2,  # tornar a mensagem persistente
            )
        )
        print(f" [AUDITORIA] Mensagem censurada publicada: {censurada} [Role: {method.routing_key}]")
    except Exception as e:
        print(f" [AUDITORIA] Erro ao publicar mensagem censurada: {e}")

def main():
    # AMQP URI do CloudAMQP
    amqp_url = 'amqps://dzrfdabj:XauaSYvj4PxJi96VY6Iowsrlfq2lMA9Y@prawn.rmq.cloudamqp.com/dzrfdabj'  # Atualize com novas credenciais

    parameters = pika.URLParameters(amqp_url)
    try:
        connection = pika.BlockingConnection(parameters)
    except pika.exceptions.AMQPConnectionError as e:
        print("Erro ao conectar ao RabbitMQ:", e)
        return

    channel = connection.channel()

    # Declara a exchange original 'guilda_direct_exchange'
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE, durable=True)

    # Declara a exchange censurada 'censored_direct_exchange'
    channel.exchange_declare(exchange=CENSORED_EXCHANGE, exchange_type=CENSORED_EXCHANGE_TYPE, durable=True)

    # Cria uma fila exclusiva para este consumidor
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Liga a fila ao exchange original com todas as routing keys possíveis (tank, healer, dps)
    for role in ['tank', 'healer', 'dps']:
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=role)

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
