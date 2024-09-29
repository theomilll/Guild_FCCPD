import subprocess
import sys

def print_menu():
    print("=== Sistema de Mensagens da Guilda ===")
    print("1. Iniciar Produtor de Mensagens")
    print("2. Iniciar Consumidor de Mensagens")
    print("3. Iniciar Backend de Auditoria")
    print("4. Sair")

def start_producer():
    try:
        subprocess.Popen(['java', '-cp', 'amqp-client-5.15.0.jar:./src/main/java', 'com.guilda.producer.MessageProducer'])
    except Exception as e:
        print(f"Erro ao iniciar o produtor: {e}")

def start_consumer():
    try:
        subprocess.Popen([sys.executable, '../consumer/message_consumer.py'])
    except Exception as e:
        print(f"Erro ao iniciar o consumidor: {e}")

def start_auditoria():
    try:
        subprocess.Popen([sys.executable, '../audit_backend/backend_auditoria.py'])
    except Exception as e:
        print(f"Erro ao iniciar o backend de auditoria: {e}")

def main():
    while True:
        print_menu()
        choice = input("Escolha uma opção: ")
        if choice == '1':
            start_producer()
        elif choice == '2':
            start_consumer()
        elif choice == '3':
            start_auditoria()
        elif choice == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
