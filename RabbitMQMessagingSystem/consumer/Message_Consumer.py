import pika
import os

EXCHANGE_NAME = 'censored_exchange'
EXCHANGE_TYPE = 'fanout'

def callback(ch, method, properties, body):
    mensagem = body.decode()
    print(f" [CONSUMER] Recebido: {mensagem}")

def main():
    amqp_url = 'amqps://dzrfdabj:XauaSYvj4PxJi96VY6Iowsrlfq2lMA9Y@prawn.rmq.cloudamqp.com/dzrfdabj'

    parameters = pika.URLParameters(amqp_url)
    try:
        connection = pika.BlockingConnection(parameters)
    except pika.exceptions.AMQPConnectionError as e:
        print("Erro ao conectar ao RabbitMQ:", e)
        return

    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE, durable=True)

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

    print(' [CONSUMER]Para sair, pressione CTRL+C')

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(" [CONSUMER] Consumidor interrompido")
        channel.stop_consuming()
    finally:
        connection.close()

if __name__ == "__main__":
    main()
