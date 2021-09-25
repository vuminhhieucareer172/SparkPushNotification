CREATE TABLE user_query
(
    `query_id`         INTEGER      NOT NULL AUTO_INCREMENT,
    `user_id`          INTEGER      NOT NULL,
    `name`            varchar(50)  NOT NULL,
    `company_address`  varchar(200) NOT NULL,
    `job_role`         varchar(50)  NOT NULL,
    `age`             INTEGER      NOT NULL,
    `salary`          varchar(20)  NOT NULL,
    `year_experiences` FLOAT        NOT NULL,
    `education_level`  varchar(50)  NOT NULL,
    `job_attribute`    varchar(50)  NOT NULL,
    `contact`         TEXT         NOT NULL,

    PRIMARY KEY (`query_id`),
    UNIQUE KEY UK_queryname (`user_id`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
