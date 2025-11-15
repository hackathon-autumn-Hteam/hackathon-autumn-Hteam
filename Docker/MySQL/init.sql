
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE prefectures (
    prefecture_id INT AUTO_INCREMENT PRIMARY KEY,
    prefecture_name VARCHAR(255) NOT NULL
);

CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    prefecture_id INT NOT NULL,
    FOREIGN KEY (prefecture_id) REFERENCES prefectures(prefecture_id) ON DELETE RESTRICT
);

CREATE TABLE channels (
    channel_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    channel_name VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    channel_id INT NOT NULL,
    message_text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    like_flower_count INT NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id) ON DELETE CASCADE
);

INSERT INTO prefectures (prefecture_name)
VALUES
("北海道"),
("青森県"), ("岩手県"), ("宮城県"), ("秋田県"), ("山形県"), ("福島県"),
("茨城県"), ("栃木県"), ("群馬県"), ("埼玉県"), ("千葉県"), ("東京都"), ("神奈川県"),
("新潟県"), ("富山県"), ("石川県"), ("福井県"), ("山梨県"), ("長野県"),("岐阜県"), ("静岡県"), ("愛知県"),
("三重県"),("滋賀県"), ("京都府"), ("大阪府"), ("兵庫県"), ("奈良県"), ("和歌山県"),
("鳥取県"), ("島根県"), ("岡山県"), ("広島県"), ("山口県"),
("徳島県"), ("香川県"), ("愛媛県"), ("高知県"),
("福岡県"), ("佐賀県"), ("長崎県"), ("熊本県"), ("大分県"), ("宮崎県"), ("鹿児島県"), ("沖縄県");