-- ユーザー情報テーブル作成
CREATE TABLE user_tbl(
id CHAR(10),
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
birthday DATE NULL,
mail VARCHAR(32),
password CHAR(32),
introduction VARCHAR(100) NULL,
report_flag INT(1),
PRIMARY KEY(id)
);


INSERT INTO user_tbl (
    id, user_name, first_name, last_name, 
    first_name_katakana, last_name_katakana, 
    tel_no, zip_code, prefecture, address1, address2, address3, 
    birthday, mail, password, introduction, report_flag
) VALUES
(1, 'tanaka01', '太郎', '田中', 'タロウ', 'タナカ',  8012345678, 5300001, '大阪府', '大阪市北区', '梅田', '1-2-3', '1980-05-12', 'tanaka@example.com', 'pass1234', '趣味は釣りです。', 0),
(2, 'suzuki02', '花子', '鈴木', 'ハナコ', 'スズキ',  9012345678, 1500001, '東京都', '渋谷区', '神宮前', '4-5-6', '1992-07-03', 'suzuki@example.com', 'flower22', '旅行が好きです。', 0),
(3, 'sato03', '健', '佐藤', 'ケン', 'サトウ',  7011112222, 9800011, '宮城県', '仙台市青葉区', '中央', '7-8-9', '1988-03-19', 'sato@example.com', 'kenpass', 'スポーツ観戦が趣味です。', 0),
(4, 'kobayashi04', '真由美', '小林', 'マユミ', 'コバヤシ',  6012223333, 4600008, '愛知県', '名古屋市中区', '栄', '2-3-4', '1995-09-25', 'kobayashi@example.com', 'mayu456', 'カフェ巡りが好きです。', 0),
(5, 'watanabe05', '翔太', '渡辺', 'ショウタ', 'ワタナベ',  5013334444, 8100001, '福岡県', '福岡市中央区', '天神', '5-6-7', '1990-12-11', 'watanabe@example.com', 'sho999', '映画を見るのが趣味です。', 0),
(6, 'yamamoto06', '絵里', '山本', 'エリ', 'ヤマモト',  4014445555, 6008001, '京都府', '京都市下京区', '四条通', '1-1-1', '1997-01-04', 'yamamoto@example.com', 'eri321', '音楽が大好きです。', 0),
(7, 'nakamura07', '健太', '中村', 'ケンタ', 'ナカムラ',  3015556666, 9800811, '宮城県', '仙台市青葉区', '一番町', '10-2-3', '1993-04-20', 'nakamura@example.com', 'kenta789', '料理が得意です。', 0),
(8, 'matsumoto08', '裕子', '松本', 'ユウコ', 'マツモト',  2016667777, 5500013, '大阪府', '大阪市西区', '新町', '2-4-5', '1985-11-09', 'matsumoto@example.com', 'yuko555', '読書が好きです。', 0),
(9, 'inoue09', '直樹', '井上', 'ナオキ', 'イノウエ',  1017778888, 9800021, '宮城県', '仙台市青葉区', '中央', '6-7-8', '1989-08-18', 'inoue@example.com', 'naoki12', 'ジョギングを毎朝しています。', 0),
(10, 'takahashi10', '美咲', '高橋', 'ミサキ', 'タカハシ',  9018889999, 1000001, '東京都', '千代田区', '千代田', '9-9-9', '1998-02-15', 'takahashi@example.com', 'misaki321', '猫が大好きです。', 0);


-- 支払い情報テーブル作成
CREATE TABLE payment_tbl(
    user_id CHAR(10),
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

--メンバーシップ情報テーブル
CREATE TABLE membership_tbl(
    user_id CHAR(10),
    join_date DATE,
    renewal_date DATE,
    payment_status CHAR(16),
    payment_method CHAR(8),
    bonus_id CHAR(10),
    creator_id INT(10),
    PRIMARY KEY(user_id,creator_id)
);

INSERT INTO membership_tbl (
    user_id, join_date, renewal_date, payment_status, payment_method, bonus_id, creator_id
) VALUES
(1,  '2023-01-15', '2024-01-15', '有効',       'クレカ', 'B000000001', 101),
(2,  '2022-06-10', '2023-06-10', '期限切れ',   '銀行振込', 'B000000002', 102),
(3,  '2024-02-01', '2025-02-01', '有効',       'PayPay', 'B000000003', 103),
(4,  '2023-08-20', '2024-08-20', '停止中',     'クレカ', 'B000000004', 104),
(5,  '2023-03-05', '2024-03-05', '有効',       '銀行振込', 'B000000005', 105),
(6,  '2022-11-11', '2023-11-11', '期限切れ',   'コンビニ', 'B000000006', 106),
(7,  '2024-04-30', '2025-04-30', '有効',       'クレカ', 'B000000007', 107),
(8,  '2023-12-25', '2024-12-25', '有効',       'PayPay', 'B000000008', 108),
(9,  '2023-07-14', '2024-07-14', '停止中',     'クレカ', 'B000000009', 109),
(10, '2022-09-01', '2023-09-01', '期限切れ',   '銀行振込', 'B000000010', 110);


--商品情報テーブル
CREATE TABLE product_tbl(
    id CHAR(32),
    favorites INT(32),
    product_view_flag TINYINT(1),
    user_id	CHAR(10),	
    PRIMARY KEY(id)
);

INSERT INTO product_tbl (id, favorites, product_view_flag, user_id) VALUES
('prd0001', '125', 1, 'usr0001'),
('prd0002', '58',  1, 'usr0002'),
('prd0003', '342', 1, 'usr0003'),
('prd0004', '0',   0, 'usr0004'),
('prd0005', '76',  1, 'usr0005'),
('prd0006', '189', 1, 'usr0006'),
('prd0007', '250', 0, 'usr0007'),
('prd0008', '12',  1, 'usr0008'),
('prd0009', '480', 1, 'usr0009'),
('prd0010', '33',  0, 'usr0010');

--出品情報テーブル
CREATE TABLE listing_tbl(
    product_id	CHAR(64),
    product_image CHAR(128),		
    product_name INT(128),		
    product_price INT(7),
    shipping_area VARCHAR(4),		
    product_category CHAR(16),		
    product_condition CHAR(8),		
    product_description	VARCHAR(255),		
    listing_status TINYINT(1),						
    listing_date DATE,		
    sales_status CHAR,		
    update_date	DATETIME,		
    product_upload_user	 INT(10),
    PRIMARY KEY(product_id,product_upload_user)
);

INSERT INTO listing_tbl VALUES
(1001, 'image_1001.jpg',  'スニーカー',   8500,  '大阪', 'ファッション', '新品',   '人気ブランドのスニーカーです', 1, '2025-10-01', '販売中', '2025-10-01 12:30:00',  1),
(1002, 'image_1002.jpg',  'ノートパソコン', 78000, '東京', '家電',       '中古',   'バッテリー良好、傷少なめ',       1, '2025-09-28', '販売中', '2025-10-02 09:45:00',  2),
(1003, 'image_1003.jpg',  'ギター',       32000, '神奈川', '楽器',       '新品',   '初心者向けのアコースティックギター', 1, '2025-10-03', '販売中', '2025-10-03 15:10:00',  3),
(1004, 'image_1004.jpg',  'コート',       12000, '京都',   'ファッション', '中古',   '少し使用感あり、サイズL',       1, '2025-09-30', '販売中', '2025-10-04 08:20:00',  4),
(1005, 'image_1005.jpg',  'スマートフォン', 52000, '愛知', '家電',       '新品',   'SIMフリー未使用品',             1, '2025-10-05', '販売中', '2025-10-05 17:00:00',  5),
(1006, 'image_1006.jpg',  '腕時計',       25000, '大阪',   'アクセサリー', '中古',   '保証書付き、動作確認済み',       1, '2025-10-02', '販売中', '2025-10-06 11:45:00',  6),
(1007, 'image_1007.jpg',  'カメラ',       64000, '北海道', '家電',       '中古',   'レンズに小傷あり、動作良好',     1, '2025-09-27', '販売中', '2025-10-06 13:50:00',  7),
(1008, 'image_1008.jpg',  'ソファ',       18000, '兵庫',   '家具',       '中古',   '2人掛けソファ、少し使用感あり',   1, '2025-10-01', '販売中', '2025-10-07 14:00:00',  8),
(1009, 'image_1009.jpg',  'ヘッドフォン',   9800,  '千葉', '家電',       '新品',   'ワイヤレスBluetoothモデル',       1, '2025-10-04', '販売中', '2025-10-08 10:10:00',  9),
(1010, 'image_1010.jpg',  'バッグ',       13500, '福岡',   'ファッション', '新品',   'レザーバッグ・未使用',           1, '2025-10-06', '販売中', '2025-10-09 18:25:00', 10);


--取引情報テーブル
CREATE TABLE market_order_tbl(
    id						
    purchaser_id CHAR(32),					
    seller_id CHAR (10),					
    transaction_status CHAR(8),						
    transaction_startdate DATETIME,				
    transaction_completeddate DATETIME,    					
    total_amount INT(7),
    sales_profit INT(7),						
    shipping_cost INT(4),				
    total_commission INT(4),					
    shipping_status CHAR(8),			
    shipping_method	CHAR(16),			
    buyer_evaluation INT(5),				
    seller_evaluation INT(5),
    PRIMARY KEY(id)			
);


INSERT INTO market_order_tbl (
    purchaser_id, seller_id, transaction_status, transaction_startdate, transaction_completeddate,
    total_amount, sales_profit, shipping_cost, total_commission,
    shipping_status, shipping_method, buyer_evaluation, seller_evaluation
) VALUES
(1, 5, '完了', '2025-09-25', '2025-09-30', 8500, 7200, 500, 800, '発送済み', 'ヤマト運輸', 5, 5),
(2, 3, '完了', '2025-09-28', '2025-10-02', 32000, 28000, 700, 1300, '発送済み', 'ゆうパック', 4, 5),
(3, 7, '進行中', '2025-10-05', NULL, 18000, 15000, 600, 1200, '発送待ち', '佐川急便', NULL, NULL),
(4, 8, '完了', '2025-09-29', '2025-10-03', 52000, 48000, 800, 1200, '発送済み', 'ヤマト運輸', 5, 5),
(5, 2, 'キャンセル', '2025-10-01', '2025-10-01', 12000, 0, 0, 0, '未発送', 'なし', 1, 1),
(6, 9, '完了', '2025-09-30', '2025-10-04', 9800, 8700, 400, 700, '発送済み', 'ゆうメール', 4, 4),
(7, 4, '進行中', '2025-10-07', NULL, 25000, 22000, 600, 900, '発送待ち', '宅配便', NULL, NULL),
(8, 1, '完了', '2025-09-26', '2025-09-30', 13500, 12000, 500, 1000, '発送済み', '佐川急便', 5, 5),
(9, 10, '完了', '2025-09-27', '2025-09-29', 64000, 60000, 700, 1300, '発送済み', 'ヤマト運輸', 5, 5),
(10, 6, '進行中', '2025-10-06', NULL, 78000, 72000, 900, 1500, '発送準備', 'ゆうパック', NULL, NULL);


--取引メッセージテーブル
CREATE TABLE order_message_tbl(
    id CHAR(128),				
    order_message_date DATETIME					
    order_message_user_id INT(10),				
    transaction_id INT(32),		
    order_message_text VARCHAR(128),
    PRIMARY KEY(id,order_message_user_id,transaction_id)		
);

INSERT INTO order_message_tbl (
    order_message_date, order_message_user_id, transaction_id, order_message_text
) VALUES
('2025-09-25 10:15:00', 1, 1, '購入させていただきました、よろしくお願いします。'),
('2025-09-25 10:45:00', 5, 1, 'ご購入ありがとうございます、すぐに発送準備します。'),
('2025-09-28 09:20:00', 2, 2, '発送予定日はいつ頃になりますか？'),
('2025-09-28 12:00:00', 3, 2, '明日発送予定です、よろしくお願いします。'),
('2025-10-01 08:10:00', 3, 7, '支払いが完了しました。'),
('2025-10-01 09:00:00', 4, 7, '確認しました、発送準備中です。'),
('2025-10-02 19:40:00', 8, 8, '商品届きました、ありがとうございました！'),
('2025-10-02 20:10:00', 1, 8, '無事届いてよかったです、またよろしくお願いします。'),
('2025-10-06 15:25:00', 10, 10, '発送はいつ頃になりますか？'),
('2025-10-06 16:00:00', 6, 10, '本日中に発送いたします。');


--投稿フィードアップロードテーブル
CREATE TABLE post_tbl(
    id	CHAR(128),					
    user_id CHAR(128),				
    post_date DATETIME,			
    post_text VARCHAR(128),			
    post_media CHAR(128),		
    post_update_date DATETIME					
    post_report_flag TINYINT(1),				
    post_status	TINYINT(1),
    PRIMARY KEY(id)			
);

--投稿フィードいいねテーブル
CREATE TABLE feed_like_tbl(
    id INT(10),
    post_id INT (10),
    user_id INT (10),
    like_time DATE,
    PRIMARY KEY(id)
);

--投稿フィードコメントテーブル
CREATE TABLE feed_comment_tbl(
    id	CHAR(10),					
    user_id	CHAR(10),					
    post_id	CHAR(10),			
    post VARCHAR(128),			
    comment_date DATE,					
    father_comment_id INT(10),
    PRIMARY KEY(id)					
);

--講義動画テーブル
CREATE TABLE video_tbl(
    id CHAR(64),					
    video_title CHAR(32),						
    video_length INT(5),	
    video_uploader_id INT(10),					
    video_upload_date DATE,				
    video_description_section VARCHAR(256),			
    video_public_status TINYINT(1),		
    video_category CHAR(16),						
    video_tag CHAR(16)		
    video_report_flag TINYINT(1),						
    video_popularity_index FLOAT				
    view_count INT (),	
    like_count INT(),				
    comment_count INT(),					
    file_path VARCHAR(255),
    PRIMARY KEY(id,video_uploader_id)
);