package yourway.api.controller;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Service;
import settings.Email;
import settings.Settings;
import utils.UtilEmail;

import javax.mail.MessagingException;

@Service
public class KafkaController {
    @KafkaListener(topics = Settings.TOPIC_USER, groupId = Settings.GROUP_ID_USER)
    public void listen(@Payload String foo,
                       @Header(KafkaHeaders.RECEIVED_MESSAGE_KEY) String key,
                       @Header(KafkaHeaders.RECEIVED_PARTITION_ID) int partition,
                       @Header(KafkaHeaders.RECEIVED_TOPIC) String topic,
                       @Header(KafkaHeaders.RECEIVED_TIMESTAMP) long ts
    ) throws MessagingException {
        System.out.println(topic);
        System.out.println(foo);
        System.out.println(key);

        UtilEmail.sendAsHtml("tienmetien011111@gmail.com",
                Email.MAIL_WARNING_TITLE,
                Email.MAIL_WARNING_CONTENT + foo
        );
    }
}
