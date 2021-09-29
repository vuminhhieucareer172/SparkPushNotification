package com.yourway.alert.streaming.settings;

import io.github.cdimascio.dotenv.Dotenv;

public class Email {
    public static final Dotenv dotenv = Dotenv.configure()
            .directory(".")
            .ignoreIfMalformed()
            .ignoreIfMissing()
            .load();

    public static final String MAIL_MAILER = dotenv.get("MAIL_MAILER", "smtp");
    public static final String MAIL_HOST = dotenv.get("MAIL_HOST", "smtp.gmail.com");
    public static final String MAIL_PORT = dotenv.get("MAIL_PORT", "465");
    public static final String MAIL_USERNAME = dotenv.get("MAIL_USERNAME");
    public static final String MAIL_PASSWORD = dotenv.get("MAIL_PASSWORD");
    public static final String MAIL_FROM_ADDRESS = dotenv.get("MAIL_FROM_ADDRESS");
    public static final String MAIL_ENCRYPTION = dotenv.get("MAIL_ENCRYPTION");
    public static final String MAIL_WARNING_TITLE = "Yourway - Đề xuất công việc mới";
    public static final String MAIL_WARNING_CONTENT = "<h2>BẠN CÓ CÔNG VIỆC ĐỀ XUẤT MỚI</h2>" +
            "<p>hi there!</p>";
}
