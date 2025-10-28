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
birthday DATE NULL,
mail VARCHAR(32),
password CHAR(32),
introduction VARCHAR(100) NULL,
user_tags VARCHAR(48) NULL,
profile_icon VARCHAR(255),
report_flag INT(1),
PRIMARY KEY(id, user_name)
);



-- 測試資料：user_tbl
INSERT INTO user_tbl (
    user_name, first_name, last_name, first_name_katakana, last_name_katakana,
    tel_no, zip_code, prefecture, address1, address2, address3,
    birthday, mail, password, introduction, user_tags, profile_icon, report_flag
) VALUES
-- 1. 完整資料 - 男性 (標準)
('kazuya_tana', '和也', '田中', 'カズヤ', 'タナカ', '09012345678', '1000005', '東京都', '千代田区', '丸の内一丁目', '1-1', '1995-04-15', 'tanaka.k@example.com', 'a9979b9a65074e64f0b2af4c703cc4f2', '宜しくお願いします。ギターとプログラミングが好きです。', 'Guitar, Code', '/icons/tana_kazu.jpg', 0),

-- 2. 完整資料 - 女性 (標準)
('yui_sato', '結衣', '佐藤', 'ユイ', 'サトウ', '08098765432', '5300001', '大阪府', '大阪市北区', '梅田一丁目', '12-34', '1998-11-20', 'sato.yui@example.com', 'b4763e0018f6d2b4b7c61f8a84592a47', 'Webデザインを勉強中です。猫を飼っています。', 'Design, Cat', '/icons/sato_yui.jpg', 0),

-- 3. 完整資料 - 生日空值 (任選)
('h_yamada', '隼人', '山田', 'ハヤト', 'ヤマダ', '09055551111', '4600002', '愛知県', '名古屋市中区', '丸の内三丁目', NULL, NULL, 'h.yamada@example.com', 'c54094a11f211322237d6e60b134d19d', '動画編集に興味があります。', 'VideoEdit', '/icons/y_hayato.jpg', 0),

-- 4. 完整資料 - 報告標誌為 1
('emi_koike', '恵美', '小池', 'エミ', 'コイケ', '08033332222', '8120011', '福岡県', '福岡市博多区', '博多駅前二丁目', '5-5', '2000-07-01', 'e.koike@example.com', 'd0239b039648943809e3e7f9a89d1469', '英語の勉強と旅行が好きです。', 'Travel, English', '/icons/k_emi.jpg', 1),

-- 5. 完整資料 - 簡短自我介紹
('tk_inoue', '拓也', '井上', 'タクヤ', 'イノウエ', '09077778888', '1500001', '東京都', '渋谷区', '神宮前五丁目', '1-2-3', '1993-02-28', 't.inoue@example.com', 'e9f45d1797c23f1f3e792c3f19e48795', 'エンジニア。', 'Engineer', '/icons/i_taku.jpg', 0),

-- 6. 完整資料 - 標籤空值
('miu_nakano', '美羽', '中野', 'ミウ', 'ナカノ', '08011110000', '6008216', '京都府', '京都市下京区', '真宗本廟', NULL, '2001-05-10', 'm.nakano@example.com', 'f6d90708f5127e2a96996d9333c415e9', '着付けと歴史を学びたい。', NULL, '/icons/n_miu.jpg', 0),

-- 7. 完整資料 - 地址欄位 2/3 空值
('souta_aoki', '颯太', '青木', 'ソウタ', 'アオキ', '09022223333', '9000006', '沖縄県', '那覇市', NULL, NULL, '1997-09-03', 's.aoki@example.com', '0a4b3d7a9609a562d980a3a4014f5263', '動画編集の技術向上を目指す。', 'Video, Travel', '/icons/a_sota.jpg', 0),

-- 8. 完整資料 - 較長的用戶名
('m_hoshi_12345', '美月', '星野', 'ミツキ', 'ホシノ', '07066667777', '2200011', '神奈川県', '横浜市西区', '高島一丁目', '1-1-1', '1996-12-05', 'm.hoshino@example.com', '1b2a95c93a02c38d82136e0d9b400929', '料理と英語が好きです。', 'Cooking, English', '/icons/h_mizuki.jpg', 0),

-- 9. 完整資料 - 較新的生日
('risa_kimura', '莉彩', '木村', 'リサ', 'キムラ', '08088889999', '0600000', '北海道', '札幌市中央区', '北三条西', '1-2', '2004-01-25', 'r.kimura@example.com', '2c416c80526019623e595a6b0c679a92', '大学でデザインを専攻しています。', 'Design', '/icons/k_risa.jpg', 0),

-- 10. 完整資料 - 名字較短
('jun_suzuki', '潤', '鈴木', 'ジュン', 'スズキ', '09012121212', '9800811', '宮城県', '仙台市青葉区', '一番町三丁目', '10-2', '1990-10-10', 'j.suzuki@example.com', '3d56e9c916056345d8b85714f447f525', '音楽とプログラミング。', 'Music, Code', '/icons/s_jun.jpg', 0),

-- 11. 測試資料
('sakura_kato', 'さくら', '加藤', 'サクラ', 'カトウ', '07034567890', '7300011', '広島県', '広島市中区', '基町', '1-1', '1994-03-21', 's.kato@example.com', '4e16d443e06180633c6d7a5b3a86c6a6', '趣味は読書です。', 'Reading', '/icons/k_sakura.jpg', 0),

-- 12. 測試資料
('daichi_wata', '大地', '渡辺', 'ダイチ', 'ワタナベ', '08045678901', '7600023', '香川県', '高松市', '寿町二丁目', NULL, '1988-06-07', 'd.wata@example.com', '5f0e1f7a6279f38f7a637f5d933390c5', '釣りキャンプが好きです。', 'Fishing, Camp', '/icons/w_daichi.jpg', 0),

-- 13. 測試資料
('aoi_tanaka', '葵', '田中', 'アオイ', 'タナカ', '09056789012', '8600808', '熊本県', '熊本市中央区', '手取本町', '5-1', '2003-12-01', 'a.tanaka@example.com', '6a988d87a4128f73f27f54c37953b169', 'イラストレーター志望。', 'Illust', '/icons/t_aoi.jpg', 0),

-- 14. 測試資料
('ryota_morita', '亮太', '森田', 'リョウタ', 'モリタ', '07067890123', '3300072', '埼玉県', 'さいたま市浦和区', '木崎五丁目', '1-1', '1992-08-18', 'r.morita@example.com', '7b47b8e5c2d3a1f8e12d1b9d10e53a94', 'マーケティングを学びたい。', 'Marketing', '/icons/m_ryota.jpg', 0),

-- 15. 測試資料
('nanami_kudo', '七海', '工藤', 'ナナミ', 'クドウ', '08078901234', '9500911', '新潟県', '新潟市中央区', '礎町通一番町', '2222', '1999-04-04', 'n.kudo@example.com', '8c255c2f9d7f5703f8f2e71d37b83f0c', '音楽制作をしています。', 'Music', '/icons/k_nanami.jpg', 0),

-- 16. 測試資料
('kenji_abe', '健二', '阿部', 'ケンジ', 'アベ', '09089012345', '9200961', '石川県', '金沢市', '香林坊二丁目', NULL, '1985-10-29', 'k.abe@example.com', '9d571871f302a64c51f465a3d7008a1c', 'ビジネススキルを磨きたい。', 'Business', '/icons/a_kenji.jpg', 0),

-- 17. 測試資料
('mana_shimizu', '真菜', '清水', 'マナ', 'シミズ', '07090123456', '7900003', '愛媛県', '松山市', '三番町六丁目', '3-3-3', '2002-01-09', 'm.shimizu@example.com', 'a193b2a245d8b843103e33f67f2e18d3', 'コスメとファッションが好きです。', 'Fashion', '/icons/s_mana.jpg', 0),

-- 18. 測試資料 (報告標誌為 1)
('haruto_endo', '晴人', '遠藤', 'ハルト', 'エンドウ', '08012345000', '5500002', '大阪府', '大阪市西区', '江戸堀一丁目', NULL, '1991-05-23', 'h.endo@example.com', 'b2e04e13583c748c8b671a5c6d59580b', '英語の同時通訳スキルを練習中。', 'English, Report', '/icons/e_haruto.jpg', 1),

-- 19. 測試資料
('rino_fujita', '莉乃', '藤田', 'リノ', 'フジタ', '09023456000', '1350064', '東京都', '江東区', '青海二丁目', '10', '2000-08-07', 'r.fujita@example.com', 'c3f683e95079a4055273b4259b951e44', 'ダンスと筋トレ。', 'Dance, Gym', '/icons/f_rino.jpg', 0),

-- 20. 測試資料
('yuma_matsui', '悠馬', '松井', 'ユウマ', 'マツイ', '07034567000', '5008722', '岐阜県', '岐阜市', '加納桜道一丁目', '1', '1994-11-14', 'y.matsui@example.com', 'd4e21b06883d6a066c1f72a44d03e62f', '料理研究家を目指しています。', 'Cooking', '/icons/m_yuma.jpg', 0),

-- 21. 測試資料
('kana_ishida', '加奈', '石田', 'カナ', 'イシダ', '08045678000', '3900811', '長野県', '松本市', '中央二丁目', NULL, '1987-03-03', 'k.ishida@example.com', 'e5a610f925b4c10041d8d21b0f199342', '自然の中での活動が好きです。', 'Nature', '/icons/i_kana.jpg', 0),

-- 22. 測試資料
('takumi_sakai', '匠', '酒井', 'タクミ', 'サカイ', '09056789000', '4200853', '静岡県', '静岡市葵区', '追手町', '2-1', '1995-07-27', 't.sakai@example.com', 'f6b283b7f1e7d0e417a86f1e8f237f37', '最新IT技術に詳しい。', 'IT, Tech', '/icons/s_takumi.jpg', 0),

-- 23. 測試資料
('momoka_oishi', '桃香', '大石', 'モモカ', 'オオイシ', '07067890000', '5140009', '三重県', '津市', '羽所町', '700', '2001-09-12', 'm.oishi@example.com', '07b8a7b3c2d6e3c544d99c7f56f1a9d1', '韓国ドラマにハマっています。', 'K-Drama', '/icons/o_momoka.jpg', 0),

-- 24. 測試資料
('hayato_koda', '勇人', '幸田', 'ハヤト', 'コウダ', '08078901000', '6500021', '兵庫県', '神戸市中央区', '三宮町二丁目', '11-1', '1993-01-01', 'h.koda@example.com', '18b335c0a37e9081a9f1b95f9c5208e4', 'フリーランスとして活動中。', 'Freelance', '/icons/k_hayato.jpg', 0),

-- 25. 測試資料
('akane_yoshida', '茜', '吉田', 'アカネ', 'ヨシダ', '09089012000', '2770852', '千葉県', '柏市', '旭町一丁目', '5-5', '1997-04-20', 'a.yoshida@example.com', '29c1e956b6858e727e02a939f8d93333', '料理のスキルを共有したい。', 'Cooking, Share', '/icons/y_akane.jpg', 0),

-- 26. 測試資料
('shun_mori', '俊', '森', 'シュン', 'モリ', '07090123000', '4506488', '愛知県', '名古屋市中村区', '名駅三丁目', '28-12', '1996-06-06', 's.mori@example.com', '3a7d20f1c902787c883a992e5e1824a7', 'AIの動向を追いかけています。', 'AI, Future', '/icons/m_shun.jpg', 0),

-- 27. 測試資料 (介紹和標籤皆空)
('yua_tanaka', '結愛', '田中', 'ユア', 'タナカ', '08012340001', '1008111', '東京都', '千代田区', '千代田一丁目', '1', '2005-02-14', 'y.tanaka2@example.com', '4b3d7a9609a562d980a3a4014f5263a2', NULL, NULL, '/icons/t_yua.jpg', 0),

-- 28. 測試資料
('kaito_ishii', '海斗', '石井', 'カイト', 'イシイ', '09023450001', '8100041', '福岡県', '福岡市中央区', '大名二丁目', '6-6', '1992-09-01', 'k.ishii@example.com', '5c416c80526019623e595a6b0c679a92', '写真撮影が趣味。', 'Photo', '/icons/i_kaito.jpg', 0),

-- 29. 測試資料
('yuki_oshima', '悠希', '大島', 'ユウキ', 'オオシマ', '07034560001', '2310023', '神奈川県', '横浜市中区', '山下町', '1', '1989-12-31', 'y.oshima@example.com', '6d56e9c916056345d8b85714f447f525', '地域活性化に貢献したい。', 'Community', '/icons/o_yuki.jpg', 0),

-- 30. 測試資料
('risa_nakamura', '莉沙', '中村', 'リサ', 'ナカムラ', '08045670001', '5406591', '大阪府', '大阪市中央区', '天満橋京町', '1-1', '1998-03-17', 'r.nakamura@example.com', '7e16d443e06180633c6d7a5b3a86c6a6', 'デザインの基礎知識を教えます。', 'Design, Tutor', '/icons/n_risa.jpg', 0);


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


--商品情報テーブル
CREATE TABLE product_tbl(
    id VARCHAR(255),
    favorites INT(32),
    product_view_flag TINYINT(1) DEFAULT 0,
    user_id	INT,	
    PRIMARY KEY(id)
);


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
