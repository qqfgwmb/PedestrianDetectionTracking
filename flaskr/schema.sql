DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE op_log
(
    log_id  INTEGER PRIMARY KEY NOT NULL,
    usr_id  INTEGER             NOT NULL,
    op      varchar(25)         NOT NULL,
    op_date DATE                NOT NULL
);

CREATE TABLE user
(
    usr_id   INTEGER PRIMARY KEY NOT NULL,
    name     VARCHAR(25)         NOT NULL UNIQUE,
    password VARCHAR(25)         NOT NULL,
    create_date    DATE          NOT NULL
);

CREATE TABLE video
(
    video_id    INTEGER PRIMARY KEY NOT NULL,
    name        VARCHAR(25)         NOT NULL,
    url         TEXT                NOT NULL,
    create_user INTEGER             NOT NULL,
    create_date    DATE             NOT NULL,
    FOREIGN KEY (create_user) REFERENCES user (usr_id)
);


CREATE TRIGGER insert_log
    AFTER INSERT
    ON video
BEGIN
    INSERT INTO op_log(usr_id, op, op_date) VALUES (new.create_user, 'insert', new.create_date);
END;



CREATE TRIGGER delete_log
    AFTER DELETE
    ON video
BEGIN
    INSERT INTO op_log(usr_id, op, op_date) VALUES (old.create_user, 'delete video', date ('now'));
END;

