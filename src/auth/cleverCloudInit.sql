CREATE TABLE user(
 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 email VARCHAR(255) NOT NULL,
 password VARCHAR(255) NOT NULL
);

INSERT INTO user (email,password) VALUE ('galantini@email.com', 'Admin123');

ALTER TABLE user ADD UNIQUE (email);

