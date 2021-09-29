package com.yourway.alert.utils;

import com.yourway.alert.streaming.settings.Email;

import javax.mail.*;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import java.util.Objects;
import java.util.Properties;

public class UtilEmail {
    public static void sendAsHtml(String to, String title, String html) throws MessagingException {
        System.out.println("Sending email to " + to);

        Session session = createSession();

        //create message using session
        MimeMessage message = new MimeMessage(session);
        prepareEmailMessage(message, to, title, html);

        //sending message
        Transport.send(message);
        System.out.println("Completed!");
    }

    private static void prepareEmailMessage(MimeMessage message, String to, String title, String html)
            throws MessagingException {
        message.setContent(html, "text/html; charset=utf-8");
        assert Email.MAIL_FROM_ADDRESS != null;
        message.setFrom(new InternetAddress(Email.MAIL_FROM_ADDRESS));
        message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(to));
        message.setSubject(title);
    }

    private static Session createSession() {
        Properties props = new Properties();
        props.put("mail.smtp.auth", "true");
        if (Objects.equals(Email.MAIL_ENCRYPTION, "ssl")) {
            props.put("mail.smtp.ssl.enable", "true");
        } else {
            props.put("mail.smtp.starttls.enable", "true");
        }
        props.put("mail.smtp.host", Email.MAIL_HOST);
        props.put("mail.smtp.port", Email.MAIL_PORT);
        props.put("mail.smtp.user", Email.MAIL_USERNAME);

        return Session.getInstance(props, new Authenticator() {
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(Email.MAIL_FROM_ADDRESS, Email.MAIL_PASSWORD);
            }
        });
    }

    public static void main(String[] args) throws MessagingException {
        UtilEmail.sendAsHtml("tienmetien011111@gmail.com",
                Email.MAIL_WARNING_TITLE,
                Email.MAIL_WARNING_CONTENT
        );
    }
}
