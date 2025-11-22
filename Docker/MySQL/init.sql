
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

-- 励ましのメッセージテーブルの定義　
CREATE TABLE support_messages(
    support_message_id INT AUTO_INCREMENT PRIMARY KEY,
    hour INT NOT NULL,
    support_message_text VARCHAR(255) NOT NULL
);

INSERT INTO support_messages (hour, support_message_text) VALUES
(0, '静かな夜に学ぶあなた、とても素敵'),
(0, '今日の少しの頑張りが、明日を明るくしてくれる'),
(0, '夜風のようにゆったりと、学びを楽しもう'),

(1, 'この時間までやる気を持てるのはすごいこと'),
(1, '落ち着いた空気の中で、心を整えて進もう'),
(1, '夜の静けさが、集中を優しく包んでくれる'),

(2, '一歩ずつでいいから、自分のペースで進もう'),
(2, '深夜の時間は、思考が深まる特別なひととき'),
(2, '小さな前進でも、確かに力になっていく'),

(3, '空が少し明るくなる頃、あなたの未来も動き出してる'),
(3, 'この時間の努力は、きっと朝の光と一緒に輝く'),
(3, '静かな世界で、自分と向き合う時間を楽しもう'),

(4, '新しい空気を吸って、ゆっくりスイッチを入れよう'),
(4, '朝の静けさが、思考をクリアにしてくれる'),
(4, '小鳥の声を聞きながら、気持ちよくスタートしよう'),

(5, '柔らかな朝日に包まれて、いい一日をつくろう'),
(5, '早起きの時間が、自分を整えるチャンス'),
(5, '静かな朝こそ、学びにぴったりの時間'),

(6, 'おはよう。今日も気持ちのいい朝だね'),
(6, '朝のひとときに、心と頭を動かしてみよう'),
(6, '新しい一日の始まりに、小さな学びをプラスしよう'),

(7, '朝の準備の合間に、少しの学びを積み重ねよう'),
(7, '短い時間でも、自分を育てる大切なひととき'),
(7, '今日を気持ちよく始めるために、学びでウォームアップ'),

(8, '朝の光を感じながら、新しい知識を吸収しよう'),
(8, '今日も穏やかに、自分のペースで進もう'),
(8, '学ぶことで、今日が少し豊かになる'),

(9, '心が落ち着いたら、ゆっくり集中していこう'),
(9, '新しい発見を楽しむ気持ちで始めよう'),
(9, '澄んだ時間が、知識をしっかり育ててくれる'),

(10, '少しずつでも続けられるあなたが素敵'),
(10, '学びが日常に溶け込む時間だね'),
(10, '今日の努力が、未来のあなたを支えてくれる'),

(11, '肩の力を抜いて、できるところから始めよう'),
(11, '気持ちが少し疲れたら、深呼吸してリセット'),
(11, 'リラックスしながら学ぶと、吸収がもっと良くなる'),

(12, 'お昼のひとときに、少しだけ自分を磨こう'),
(12, '気軽に手を伸ばすその一歩が大事'),
(12, 'リラックスしながら学べる時間にしよう'),

(13, '午後の光の中で、心を落ち着けて進もう'),
(13, '眠気がきても大丈夫！少しずつ積み重ねよう'),
(13, '気分を変えて、のんびり取り組もう'),

(14, '無理をせず、ゆるやかに続けよう'),
(14, '一歩だけでも進めたら、それで十分'),
(14, 'お茶を片手に、ゆったり学び時間'),

(15, '少しずつ気持ちを切り替えていこう'),
(15, '今日もここから、もうひとがんばり'),
(15, '優しい気持ちで、今の学びを楽しもう'),

(16, '疲れたときこそ、ゆっくりペースで進もう'),
(16, '無理せず、少しでも手を動かしてみよう'),
(16, '穏やかな気持ちで、今日の学びをつなげよう'),

(17, '今日もおつかれさま。ここからは自分の時間'),
(17, '仕事のモードを切り替えて、心を軽くしよう'),
(17, '夕方の静けさの中で、少しだけ前へ進もう'),

(18, '一日頑張ったね！ここからは自分の成長タイム'),
(18, '疲れてても大丈夫。始めた瞬間に心が動き出す'),
(18, 'ゆるく始めるだけで、今日がいい一日になる'),

(19, '少し落ち着いて、学びの時間を楽しもう'),
(19, '一日の締めくくりに、自分へのごほうび時間'),
(19, '今日の自分を少しだけ育てていこう'),

(20, '夜の空気が落ち着きをくれるね'),
(20, '少しずつでも積み重ねれば大きな力になる'),
(20, '今日の学びが、明日の自信につながる'),

(21, '静かな時間に、自分のペースで進もう'),
(21, '今日の小さな学びを大切に積み重ねよう'),
(21, '夜の穏やかさが、集中をやさしく支えてくれる'),

(22, 'この時間の努力が、明日のあなたを支えてくれる'),
(22, '遅い時間でも、自分を高めようとする姿勢が素敵'),
(22, '眠る前の学びが、心を落ち着けてくれる'),

(23, '一日の終わりに、少しだけ自分を磨こう'),
(23, '今日の一歩が、未来をやさしく照らしてくれる'),
(23, '静かな夜に、心穏やかに学びを楽しもう');