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
    private static final String EXCHANGE_NAME = "guilda_exchange";
    private static final String EXCHANGE_TYPE = "fanout";

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Digite o nome do produtor: ");
        String producerName = scanner.nextLine();

        ConnectionFactory factory = new ConnectionFactory();
        try {
            factory.setUri("amqps://dzrfdabj:XauaSYvj4PxJi96VY6Iowsrlfq2lMA9Y@prawn.rmq.cloudamqp.com/dzrfdabj");

            Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();

            channel.exchangeDeclare(EXCHANGE_NAME, EXCHANGE_TYPE, true);

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

            while (true) {
                System.out.print("Digite a mensagem (ou 'exit' para encerrar): ");
                String messageBody = scanner.nextLine();

                if (messageBody.equalsIgnoreCase("exit")) {
                    logger.info("Encerrando o produtor conforme solicitado.");
                    break;
                }

                String timestamp = new SimpleDateFormat("dd/MM/yyyy - HH:mm").format(new Date());
                String message = String.format("[%s] %s : %s", timestamp, producerName, messageBody);

                try {
                    channel.basicPublish(EXCHANGE_NAME, "", null, message.getBytes("UTF-8"));
                    logger.info("Mensagem enviada: " + message);
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
