package com.guilda.producer;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManagerFactory;
import java.io.FileInputStream;
import java.security.KeyStore;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Scanner;

public class MessageProducer {

    private static final Logger logger = LoggerFactory.getLogger(MessageProducer.class);
    private static final String EXCHANGE_NAME = "guilda_exchange";
    private static final String EXCHANGE_TYPE = "fanout"; // Usando fanout para broadcast

    public static void main(String[] args) {
        // Parâmetros configuráveis via linha de comando
        Scanner scanner = new Scanner(System.in);
        System.out.print("Digite o nome do produtor: ");
        String producerName = scanner.nextLine();

        System.out.print("Digite a mensagem: ");
        String messageBody = scanner.nextLine();

        try {
            // Configurações da conexão com RabbitMQ
            ConnectionFactory factory = new ConnectionFactory();
            factory.setUri("amqps://dzrfdabj:XauaSYvj4PxJi96VY6Iowsrlfq2lMA9Y@prawn.rmq.cloudamqp.com/dzrfdabj");

            // Configurar SSL com TrustStore
            KeyStore trustStore = KeyStore.getInstance(KeyStore.getDefaultType());
            FileInputStream trustStoreStream = new FileInputStream("path/to/cloudamqp_keystore.jks");
            trustStore.load(trustStoreStream, "keystore_password".toCharArray());

            TrustManagerFactory trustManagerFactory = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
            trustManagerFactory.init(trustStore);

            SSLContext sslContext = SSLContext.getInstance("TLS");
            sslContext.init(null, trustManagerFactory.getTrustManagers(), null);

            factory.useSslProtocol(sslContext);

            Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();

            // Declara o exchange
            channel.exchangeDeclare(EXCHANGE_NAME, EXCHANGE_TYPE, true);

            // Formata a mensagem
            String timestamp = new SimpleDateFormat("dd/MM/yyyy - HH:mm").format(new Date());
            String message = String.format("[%s] %s : %s", timestamp, producerName, messageBody);

            // Publica a mensagem no exchange
            channel.basicPublish(EXCHANGE_NAME, "", null, message.getBytes("UTF-8"));
            logger.info("Mensagem enviada: " + message);

            // Fecha a conexão
            channel.close();
            connection.close();

        } catch (Exception e) {
            logger.error("Erro ao enviar mensagem", e);
        }
    }
}
