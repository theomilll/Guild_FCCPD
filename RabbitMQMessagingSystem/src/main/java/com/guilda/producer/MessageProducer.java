package com.guilda.producer;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Scanner;

public class MessageProducer {

    private static final Logger logger = LoggerFactory.getLogger(MessageProducer.class);
    private static final String EXCHANGE_NAME = "guilda_direct_exchange";
    private static final String EXCHANGE_TYPE = "direct"; // Tipo 'direct'

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Digite o nome do produtor: ");
        String producerName = scanner.nextLine();

        ConnectionFactory factory = new ConnectionFactory();
        try {
            // Configurações da conexão com RabbitMQ
            factory.setUri("amqps://dzrfdabj:XauaSYvj4PxJi96VY6Iowsrlfq2lMA9Y@prawn.rmq.cloudamqp.com/dzrfdabj"); // Atualize com novas credenciais

            // Estabelece a conexão e o canal uma única vez
            Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();

            // Declara a exchange 'guilda_direct_exchange' do tipo 'direct'
            channel.exchangeDeclare(EXCHANGE_NAME, EXCHANGE_TYPE, true);

            // Adiciona um shutdown hook para fechar a conexão de forma graciosa
            final Connection finalConnection = connection;
            final Channel finalChannel = channel;
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                try {
                    if (finalChannel != null && finalChannel.isOpen()) {
                        finalChannel.close();
                        logger.info("Canal fechado.");
                    }
                    if (finalConnection != null && finalConnection.isOpen()) {
                        finalConnection.close();
                        logger.info("Conexão fechada.");
                    }
                } catch (Exception e) {
                    logger.error("Erro ao fechar a conexão ou o canal.", e);
                }
            }));

            logger.info("Produtor iniciado. Você pode começar a enviar mensagens. Para encerrar, pressione CTRL+C ou digite 'exit'.");

            // Loop para enviar mensagens continuamente
            while (true) {
                System.out.print("Digite a mensagem (ou 'exit' para encerrar): ");
                String messageBody = scanner.nextLine();

                // Permitir que o usuário encerre o programa digitando 'exit'
                if (messageBody.equalsIgnoreCase("exit")) {
                    logger.info("Encerrando o produtor conforme solicitado.");
                    break;
                }

                // Solicita o role para a mensagem via opções numéricas
                String role;
                while (true) {
                    System.out.println("Escolha o role para a mensagem:");
                    System.out.println("1 - Tank");
                    System.out.println("2 - Healer");
                    System.out.println("3 - DPS");
                    System.out.println("4 - Null (broadcast)");
                    System.out.print("Digite a opção (1-4): ");
                    String opcao = scanner.nextLine();
                    switch (opcao) {
                        case "1":
                            role = "tank";
                            break;
                        case "2":
                            role = "healer";
                            break;
                        case "3":
                            role = "dps";
                            break;
                        case "4":
                            role = "broadcast"; // Define 'broadcast' para enviar para todos
                            break;
                        default:
                            System.out.println("Opção inválida. Por favor, digite de 1 a 4.");
                            continue;
                    }
                    break;
                }

                // Formata a mensagem
                String timestamp = new SimpleDateFormat("dd/MM/yyyy - HH:mm").format(new Date());
                String message = String.format("[%s] %s : %s", timestamp, producerName, messageBody);

                try {
                    if (role.equals("broadcast")) {
                        // Envia a mensagem para todos os roles (tank, healer, dps)
                        String[] roles = {"tank", "healer", "dps"};
                        for (String r : roles) {
                            channel.basicPublish(EXCHANGE_NAME, r, null, message.getBytes("UTF-8"));
                            logger.info("Mensagem enviada para role '" + r + "': " + message);
                        }
                    } else {
                        // Publica a mensagem no exchange com a routing key correspondente ao role
                        channel.basicPublish(EXCHANGE_NAME, role, null, message.getBytes("UTF-8"));
                        logger.info("Mensagem enviada: " + message + " [Role: " + role + "]");
                    }
                } catch (Exception e) {
                    logger.error("Erro ao enviar mensagem", e);
                }
            }

            // Fecha o canal e a conexão após o loop
            if (channel != null && channel.isOpen()) {
                channel.close();
                logger.info("Canal fechado.");
            }
            if (connection != null && connection.isOpen()) {
                connection.close();
                logger.info("Conexão fechada.");
            }

        } catch (Exception e) {
            logger.error("Erro ao configurar o produtor.", e);
        }
    }
}
