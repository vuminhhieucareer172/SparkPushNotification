package com.yourway.alert.web.rest;

import com.yourway.alert.streaming.settings.Email;
import com.yourway.alert.streaming.settings.Settings;
import com.yourway.alert.utils.UtilEmail;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Service;

import javax.mail.MessagingException;
import java.sql.Timestamp;
import java.util.Date;
import java.util.Objects;

@Service
public class KafkaResource {
    @KafkaListener(topics = Settings.TOPIC_USER, groupId = Settings.GROUP_ID_USER)
    public void listen(@Payload String message,
                       @Header(KafkaHeaders.RECEIVED_MESSAGE_KEY) String key,
                       @Header(KafkaHeaders.RECEIVED_TIMESTAMP) long ts
    ) throws MessagingException {
        System.out.println("---------------------------------");
        System.out.println(message);
        System.out.println(key);

        Timestamp timestamp = new Timestamp(ts);
        Date date= new Date(timestamp.getTime());
        System.out.println(date);

        if (!Objects.equals(message, "")) {
            UtilEmail.sendAsHtml("tienmetien011111@gmail.com",
                    Email.MAIL_ALERT_TITLE,
                    Email.MAIL_ALERT_CONTENT + message
            );
        }
    }
}
