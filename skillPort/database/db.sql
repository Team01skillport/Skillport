-- ユーザー情報テーブル作成
CREATE TABLE user_tbl(
id INT AUTO_INCREMENT PRIMARY KEY,
user_name CHAR(16),
first_name CHAR(8),
last_name CHAR(8),
first_name_katakana CHAR(8),
last_name_katakana CHAR(8),
tel_no CHAR(12),
zip_code CHAR(7),
prefecture VARCHAR(20),
address1 VARCHAR(20),
address2 VARCHAR(20),
address3 VARCHAR(20),
birthday DATE,
gender CHAR(6),
mail VARCHAR(32),
password CHAR(32),
introduction VARCHAR(100) NULL,
user_tags VARCHAR(48) NULL,
profile_icon VARCHAR(255) NULL,
user_rating INT(1) DEFAULT 0,
report_flag TINYINT(1) DEFAULT 0,
PRIMARY KEY(id, user_name)
);


CREATE TABLE user_follow_tbl(
    id INT AUTO_INCREMENT PRIMARY KEY,
    follower_id INT,
    followed_id INT,
    follow_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (follower_id) REFERENCES user_tbl(id),
    FOREIGN KEY (followed_id) REFERENCES user_tbl(id),
    UNIQUE (follower_id, followed_id) 
);

INSERT INTO user_follow_tbl (follower_id, followed_id) VALUES
('usr0001', 'usr0002'),  -- user1 follows user2
('usr0002', 'usr0003'),  -- user2 follows user3
('usr0003', 'usr0001'); 
-------------------------------------------------------------------

-- 支払い情報テーブル作成
CREATE TABLE payment_tbl(
    user_id INT,
    card_num CHAR(16),
    card_name CHAR(16),
    card_expiration CHAR(4),
    card_block TINYINT(1),
    bank_name VARCHAR(30),
    bank_account_num CHAR(16),
    branch_name CHAR(7),
    branch_num CHAR(3),
    acc_holder_name CHAR(16),
    monthly_sales INT(16),
    total_sales INT(16),
    withdrawal INT(16),
    account_type CHAR(10),
    PRIMARY KEY (user_id, card_num)
);



INSERT INTO payment_tbl (
    user_id, card_num, card_name, card_expiration, card_block, 
    bank_name, bank_account_num, branch_name, branch_num, acc_holder_name, 
    monthly_sales, total_sales, withdrawal, account_type
) VALUES
(1, '4980123456789012', 'タナカ カズヤ', '1028', 0, NULL, NULL, NULL, NULL, NULL, 55000, 1200000, 800000, 'クレジット'),
(2, '0000000000000000', NULL, NULL, 0, '三菱ＵＦＪ銀行', '1234567890123456', '本店', '001', 'サトウ ユイ', 120000, 3500000, 2000000, '普通'),
(3, '5100000012345678', 'ヤマダ ハヤト', '0526', 0, NULL, NULL, NULL, NULL, NULL, 15000, 350000, 150000, 'クレジット'),
(4, '0000000000000000', NULL, NULL, 0, '三井住友銀行', '9876543210123456', '渋谷支店', '101', 'コイケ エミ', 80000, 1500000, 1000000, '当座'),
(5, '4000111122223333', 'イノウエ タクヤ', '0327', 0, NULL, NULL, NULL, NULL, NULL, 250000, 8000000, 5000000, 'クレジット'),
(6, '0000000000000000', NULL, NULL, 0, 'ゆうちょ銀行', '01010123456789', '京都支店', '401', 'ナカノ ミウ', 5000, 120000, 50000, '普通'),
(7, '4567890123456789', 'アオキ ソウタ', '1125', 0, NULL, NULL, NULL, NULL, NULL, 40000, 950000, 700000, 'クレジット'),
(8, '0000000000000000', NULL, NULL, 0, 'みずほ銀行', '5432109876543210', '横浜支店', '201', 'ホシノ ミツキ', 65000, 1800000, 1200000, '普通'),
(9, '5432109876543210', 'キムラ リサ', '0829', 0, NULL, NULL, NULL, NULL, NULL, 20000, 450000, 300000, 'クレジット'),
(10, '0000000000000000', NULL, NULL, 0, 'りそな銀行', '7654321098765432', '仙台支店', '301', 'スズキ ジュン', 150000, 4000000, 3500000, '当座'),
(11, '4321098765432109', 'カトウ サクラ', '0126', 0, NULL, NULL, NULL, NULL, NULL, 30000, 600000, 400000, 'クレジット'),
(12, '0000000000000000', NULL, NULL, 0, '地方銀行', '0001112223334445', '高松支店', '501', 'ワタナベ ダイチ', 25000, 700000, 500000, '普通'),
(13, '5213456789012345', 'タナカ アオイ', '1228', 0, NULL, NULL, NULL, NULL, NULL, 75000, 2000000, 1500000, 'クレジット'),
(14, '0000000000000000', NULL, NULL, 0, '新生銀行', '6789012345678901', '浦和支店', '601', 'モリタ リョウタ', 95000, 2500000, 2000000, '普通'),
(15, '4777666655554444', 'クドウ ナナミ', '0427', 0, NULL, NULL, NULL, NULL, NULL, 180000, 5500000, 4000000, 'クレジット'),
(16, '0000000000000000', NULL, NULL, 0, '信託銀行', '8765432109876543', '金沢支店', '701', 'アベ ケンジ', 35000, 850000, 600000, '当座'),
(17, '5555444433332222', 'シミズ マナ', '0729', 0, NULL, NULL, NULL, NULL, NULL, 15000, 300000, 100000, 'クレジット'),
(18, '0000000000000000', NULL, NULL, 0, '楽天銀行', '1111000099998888', '大阪支店', '801', 'エンドウ ハルト', 50000, 1100000, 900000, '普通'),
(19, '4222333344445555', 'フジタ リノ', '0925', 0, NULL, NULL, NULL, NULL, NULL, 60000, 1400000, 1000000, 'クレジット'),
(20, '0000000000000000', NULL, NULL, 0, '地方銀行', '9999888877776666', '岐阜支店', '901', 'マツイ ユウマ', 110000, 2900000, 2500000, '普通'),
(21, '5111222233334444', 'イシダ カナ', '1226', 0, NULL, NULL, NULL, NULL, NULL, 25000, 700000, 450000, 'クレジット'),
(22, '0000000000000000', NULL, NULL, 0, '静岡銀行', '7777666655554444', '静岡支店', '005', 'サカイ タクミ', 200000, 7500000, 6000000, '当座'),
(23, '4001001001001001', 'オオイシ モモカ', '0526', 0, NULL, NULL, NULL, NULL, NULL, 10000, 250000, 150000, 'クレジット'),
(24, '0000000000000000', NULL, NULL, 0, '関西みらい銀行', '5555444433332222', '神戸支店', '105', 'コウダ ハヤト', 70000, 1900000, 1500000, '普通'),
(25, '5000500050005000', 'ヨシダ アカネ', '0327', 0, NULL, NULL, NULL, NULL, NULL, 85000, 2100000, 1700000, 'クレジット'),
(26, '0000000000000000', NULL, NULL, 0, '三井住友信託銀行', '3333222211110000', '名古屋支店', '205', 'モリ シュン', 130000, 4200000, 3000000, '当座'),
(27, '4444555566667777', 'タナカ ユア', '0126', 0, NULL, NULL, NULL, NULL, NULL, 2000, 50000, 10000, 'クレジット'),
(28, '0000000000000000', NULL, NULL, 0, '西日本シティ銀行', '2222111100009999', '福岡支店', '305', 'イシイ カイト', 90000, 2400000, 2000000, '普通'),
(29, '5678901234567890', 'オオシマ ユウキ', '1125', 1, NULL, NULL, NULL, NULL, NULL, 40000, 980000, 750000, 'クレジット'),
(30, '0000000000000000', NULL, NULL, 0, '埼玉りそな銀行', '8888777766665555', '大宮支店', '405', 'ナカムラ リサ', 70000, 1600000, 1200000, '普通');

----------------------------------------------------------------------

--メンバーシップ情報テーブル
CREATE TABLE membership_tbl(
    user_id INT,
    join_date DATETIME,
    renewal_date DATETIME CURRENT_TIMESTAMP,
    payment_status CHAR(16),
    payment_method CHAR(8),
    bonus_id VARCHAR(255),
    creator_id INT,
    PRIMARY KEY(user_id,creator_id)
);


INSERT INTO membership_tbl (
    user_id, join_date, renewal_date, payment_status, payment_method, bonus_id, creator_id
) VALUES
(1, '2024-01-10 10:00:00', '2025-01-10 10:00:00', '成功', 'クレジット', 'BNS-GTR-TANA', 101),
(1, '2024-05-20 15:30:00', '2024-11-20 15:30:00', '成功', '口座振替', 'BNS-DGN-PRJ', 103),
(2, '2024-07-05 12:00:00', '2025-07-05 12:00:00', '成功', 'クレジット', 'BNS-WEB-GUIDE', 103),
(3, '2024-03-15 09:00:00', '2024-09-15 09:00:00', '失敗', 'クレジット', 'BNS-VDO-BASIC', 102),
(4, '2024-02-01 14:00:00', '2025-02-01 14:00:00', '成功', 'クレジット', 'BNS-TRV-NEWS', 104),
(5, '2024-09-01 18:00:00', '2025-10-01 18:00:00', '成功', '口座振替', 'BNS-ENG-ADV', 105),
(6, '2024-04-22 11:00:00', '2025-04-22 11:00:00', '成功', 'クレジット', 'BNS-WEB-BASIC', 103),
(7, '2024-10-10 09:30:00', '2025-10-10 09:30:00', '成功', '口座振替', 'BNS-VDO-ADV', 102),
(8, '2024-01-05 17:00:00', '2025-01-05 17:00:00', '成功', 'クレジット', 'BNS-COOK-RSP', 104),
(9, '2024-06-18 13:00:00', '2024-12-18 13:00:00', '成功', '口座振替', 'BNS-DGN-TIPS', 103),
(10, '2024-08-01 10:00:00', '2025-08-01 10:00:00', '成功', 'クレジット', 'BNS-MUS-MASTER', 101),
(11, '2024-03-01 08:00:00', '2025-03-01 08:00:00', '成功', '口座振替', 'BNS-TRV-BLOG', 104),
(12, '2024-07-25 19:00:00', '2025-07-25 19:00:00', '成功', 'クレジット', 'BNS-OUT-GEAR', 102),
(13, '2024-05-10 16:30:00', '2025-05-10 16:30:00', '成功', 'クレジット', 'BNS-ILL-SKETCH', 103),
(13, '2024-09-05 12:00:00', '2025-09-05 12:00:00', '成功', '口座振替', 'BNS-MINI-GUIDE', 105),
(14, '2024-01-20 13:00:00', '2025-01-20 13:00:00', '成功', 'クレジット', 'BNS-MKT-TREND', 104),
(15, '2024-06-05 10:00:00', '2024-12-05 10:00:00', '成功', '口座振替', 'BNS-MUS-BEAT', 101),
(16, '2024-08-10 14:00:00', '2024-11-10 14:00:00', '失敗', 'クレジット', 'BNS-BUS-DOC', 105),
(17, '2024-04-04 17:30:00', '2025-04-04 17:30:00', '成功', 'クレジット', 'BNS-FAS-LOOK', 104),
(18, '2024-02-15 11:00:00', '2025-02-15 11:00:00', '成功', '口座振替', 'BNS-ENG-TALK', 105),
(19, '2024-07-01 10:00:00', '2024-11-01 10:00:00', '成功', 'クレジット', 'BNS-FIT-PLAN', 102),
(20, '2024-05-01 15:00:00', '2025-05-01 15:00:00', '成功', '口座振替', 'BNS-COOK-JAP', 104),
(21, '2024-08-28 14:00:00', '2025-08-28 14:00:00', '成功', 'クレジット', 'BNS-NAT-TREK', 102),
(22, '2024-03-05 16:00:00', '2025-03-05 16:00:00', '成功', '口座振替', 'BNS-TECH-NEWS', 105),
(23, '2024-10-20 10:00:00', '2025-10-20 10:00:00', '成功', 'クレジット', 'BNS-KDR-LIST', 104),
(24, '2024-01-01 12:00:00', '2025-01-01 12:00:00', '成功', '口座振替', 'BNS-FREE-DESIGN', 103),
(24, '2024-09-10 11:00:00', '2024-11-10 11:00:00', '失敗', 'クレジット', 'BNS-VDO-CUT', 102),
(25, '2024-06-01 15:30:00', '2025-06-01 15:30:00', '成功', 'クレジット', 'BNS-COOK-TIPS', 104),
(26, '2024-03-10 09:00:00', '2025-03-10 09:00:00', '成功', '口座振替', 'BNS-AI-MODEL', 105),
(27, '2024-07-15 13:00:00', '2025-07-15 13:00:00', '成功', 'クレジット', 'BNS-MUS-CHORD', 101),
(28, '2024-04-10 10:00:00', '2025-04-10 10:00:00', '成功', '口座振替', 'BNS-PHO-EDIT', 102),
(29, '2024-02-20 14:00:00', '2025-02-20 14:00:00', '成功', 'クレジット', 'BNS-COM-REPORT', 105),
(30, '2024-05-15 11:00:00', '2025-05-15 11:00:00', '成功', '口座振替', 'BNS-DGN-COLOR', 103);



----------------------------------------------------------------------


--商品情報テーブル
CREATE TABLE product_tbl(
    id VARCHAR(255),
    favorites INT(32),
    product_view_flag TINYINT(1) DEFAULT 0,
    user_id	INT,	
    PRIMARY KEY(id)
);

INSERT INTO product_tbl (
    id, favorites, product_view_flag, user_id
) VALUES
('PRD-GTR-101', 52345, 1, 1),
('PRD-VDO-102', 12340, 1, 7),
('PRD-DGN-103', 9876, 1, 9),
('PRD-ENG-104', 350000, 1, 18),
('PRD-WEB-105', 1200, 0, 5),
('PRD-JAP-201', 5000, 1, 20),
('PRD-MKT-202', 25000, 1, 14),
('PRD-FIT-203', 150, 0, 19),
('PRD-AIT-204', 450000, 1, 26),
('PRD-MUS-205', 89000, 1, 10),
('PRD-PHO-301', 50, 0, 28),
('PRD-LIF-302', 22000, 1, 4),
('PRD-COD-303', 180000, 1, 22),
('PRD-ART-304', 300, 0, 13),
('PRD-HIS-305', 7500, 1, 6),
('PRD-FAS-401', 1000, 1, 17),
('PRD-YOG-402', 500, 0, 23),
('PRD-BUS-403', 95000, 1, 16),
('PRD-VOG-404', 32000, 1, 2),
('PRD-MED-405', 10, 0, 12),
('PRD-COOK-501', 75000, 1, 8),
('PRD-ILL-502', 150000, 1, 13),
('PRD-TRE-503', 40000, 1, 21),
('PRD-SKT-504', 800, 0, 27),
('PRD-WRI-505', 12000, 1, 11),
('PRD-FIL-601', 2000, 1, 7),
('PRD-CRM-602', 1500, 0, 29),
('PRD-DIY-603', 75000, 1, 25),
('PRD-GRW-604', 100000, 1, 5),
('PRD-VDO-605', 250, 0, 18);

----------------------------------------------------------------------


--出品情報テーブル
CREATE TABLE listing_tbl(
    product_id	VARCHAR(255),		
    product_name CHAR(32),	
    product_price INT(7),
    shipping_area VARCHAR(4),		
    product_category CHAR(16),		
    product_condition CHAR(8),		
    product_description	VARCHAR(255),		
    listing_status TINYINT(1) DEFAULT 1,						
    listing_date DATETIME DEFAULT CURRENT_TIMESTAMP,		
    sales_status CHAR,		
    update_date	DATETIME DEFAULT CURRENT_TIMESTAMP,		
    product_upload_user CHAR(64),
    PRIMARY KEY(product_id,product_upload_user)
);
-- 同じ言葉が入っている商品が５本ほしい






CREATE TABLE listing_images_tbl(
    image_id VARCHAR(255),
    product_id VARCHAR(255),
    image_path VARCHAR(255),
    is_thumbnail TINYINT(1) DEFAULT 0,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES listing_tbl(product_id)
);

--取引情報テーブル
CREATE TABLE market_order_tbl(
    id INT AUTO_INCREMENT,						
    purchaser_id INT,					
    seller_id INT,					
    transaction_status CHAR(8),						
    transaction_startdate DATETIME DEFAULT CURRENT_TIMESTAMP,				
    transaction_completeddate DATETIME DEFAULT CURRENT_TIMESTAMP,    					
    total_amount INT(7),
    sales_profit INT(7),						
    shipping_cost INT(4),				
    total_commission INT(4),					
    shipping_status CHAR(8),			
    shipping_method	CHAR(16),			
    buyer_evaluation INT(1),				
    seller_evaluation INT(1),
    PRIMARY KEY(id)			
);


--取引メッセージテーブル
CREATE TABLE order_message_tbl(
    id INT AUTO_INCREMENT,				
    order_message_date DATETIME DEFAULT CURRENT_TIMESTAMP,					
    order_message_user_id CHAR(64),			
    transaction_id INT,		
    order_message_text VARCHAR(128),
    PRIMARY KEY(id,order_message_user_id,transaction_id)		
);


--投稿フィードアップロードテーブル
CREATE TABLE post_tbl(
    id INT AUTO_INCREMENT,					
    user_id INT,				
    post_date DATETIME DEFAULT CURRENT_TIMESTAMP,			
    post_text VARCHAR(255),			
    post_media VARCHAR(255),		
    post_update_date DATETIME DEFAULT CURRENT_TIMESTAMP,				
    post_report_flag TINYINT(1) DEFAULT 0,				
    post_status	TINYINT(1) DEFAULT 1,
    PRIMARY KEY(id)			
);



--投稿フィードいいねテーブル
CREATE TABLE feed_like_tbl(
    id INT AUTO_INCREMENT,
    post_id INT,
    user_id INT,
    like_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id), 
    FOREIGN KEY (post_id) REFERENCES post_tbl(id)
);



--投稿フィードコメントテーブル
CREATE TABLE feed_comment_tbl(
    id INT AUTO_INCREMENT,					
    user_id	INT,					
    post_id	INT,			
    post_text VARCHAR(128),			
    comment_date DATETIME DEFAULT CURRENT_TIMESTAMP,					
    father_comment_id INT,
    PRIMARY KEY(id),
    FOREIGN KEY (post_id) REFERENCES post_tbl(id)				
);



--講義動画テーブル
CREATE TABLE video_tbl(
    id INT AUTO_INCREMENT,					
    video_title CHAR(32),						
    video_length INT(5),	
    video_uploader_id INT,					
    video_upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,				
    video_description_section VARCHAR(255),			
    video_public_status TINYINT(1),		
    video_category CHAR(16),						
    video_tag CHAR(16),	
    video_report_flag TINYINT(1) DEFAULT 0,						
    video_popularity_index FLOAT,			
    view_count INT(10),	
    like_count INT(10),				
    comment_count INT(10),					
    file_path VARCHAR(255),
    PRIMARY KEY(id, video_uploader_id)
);
-- 同じ言葉がタイトルに入っている動画が５本ほしい


--講義動画いいねテーブル
CREATE TABLE video_like_tbl(
    id INT AUTO_INCREMENT,			
    video_id INT,				
    video_uploader_id INT,					
    video_like_date DATETIME CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY (video_id) REFERENCES video_tbl(id)		 
);


--講義動画コメントテーブル
CREATE TABLE video_comment_tbl(
    comment_id INT AUTO_INCREMENT,				
    video_id INT,					
    commentor_id INT,					
    comment_date DATETIME DEFAULT CURRENT_TIMESTAMP,				
    comment_text VARCHAR(128),					
    parent_comment_id INT,
    PRIMARY KEY(comment_id),
    FOREIGN KEY (video_id) REFERENCES video_tbl(id)
);


--サポートテーブル
CREATE TABLE support_tbl(
    id INT AUTO_INCREMENT,	
    category CHAR(16),					
    content VARCHAR(255),			
    inquiry_user_id INT,				
    send_date DATETIME DEFAULT CURRENT_TIMESTAMP,				
    receiving_date DATETIME DEFAULT CURRENT_TIMESTAMP,						
    response_status CHAR(16),				
    response_date DATETIME DEFAULT CURRENT_TIMESTAMP,			
    attached_file VARCHAR(255),				
    response_content VARCHAR(255),
    PRIMARY KEY(id)				 
);


--審査テーブル
CREATE TABLE video_review_tbl(
    review_id INT AUTO_INCREMENT,				
    video_id INT,			
    reviewer_id	INT,					
    review_status CHAR(8),				
    review_result_comment VARCHAR(255),						
    reviewed_at	DATETIME DEFAULT CURRENT_TIMESTAMP,				
    created_at	DATETIME DEFAULT CURRENT_TIMESTAMP,			
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(review_id)
);
