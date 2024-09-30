import pika
import os

EXCHANGE_NAME = 'censored_direct_exchange'
EXCHANGE_TYPE = 'direct'

def callback(ch, method, properties, body):
    mensagem = body.decode()
    print(f" [CONSUMER] Recebido: {mensagem}")

def main():
    # AMQP URI do CloudAMQP
    amqp_url = 'amqps://dzrfdabj:XauaSYvj4PxJi96VY6Iowsrlfq2lMA9Y@prawn.rmq.cloudamqp.com/dzrfdabj'
    parameters = pika.URLParameters(amqp_url)
    try:
        connection = pika.BlockingConnection(parameters)
    except pika.exceptions.AMQPConnectionError as e:
        print("Erro ao conectar ao RabbitMQ:", e)
        return

    channel = connection.channel()

    # Declara a exchange censurada 'censored_direct_exchange'
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE, durable=True)

    # Solicita o role do consumidor com opções numéricas
    role = ''
    while True:
        print("Selecione seu role:")
        print("1 - Tank")
        print("2 - Healer")
        print("3 - DPS")
        print("4 - Null (receber todas as mensagens)")
        opcao = input("Digite a opção (1-4): ")

        if opcao == "1":
            role = "tank"
            break
        elif opcao == "2":
            role = "healer"
            break
        elif opcao == "3":
            role = "dps"
            break
        elif opcao == "4":
            role = "all"  # Define 'all' para receber todas as mensagens
            break
        else:
            print("Opção inválida. Por favor, digite de 1 a 4.")

    # Cria uma fila exclusiva para este consumidor
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Vincula a fila à exchange censurada com a routing key correspondente
    if role != "all":
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=role)
        print(f' [CONSUMER] Aguardando mensagens para o role "{role}". Para sair, pressione CTRL+C')
    else:
        # Vincula a fila a todas as routing keys (tank, healer, dps, broadcast)
        for rk in ['tank', 'healer', 'dps', 'broadcast']:
            channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=rk)
        print(' [CONSUMER] Aguardando todas as mensagens. Para sair, pressione CTRL+C')

    # Consumidor
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
