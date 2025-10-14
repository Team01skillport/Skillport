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

--商品情報テーブル
CREATE TABLE product_tbl(
    id CHAR(32),
    favorites INT(32),
    product_view_flag TINYINT(1),
    user_id	INT (10),	
    PRIMARY KEY(id)
);

--出品情報テーブル
CREATE TABLE listing_tbl(
    product_id	CHAR(64),
    product_image CHAR(128),		
    product_name INT(128),		
    product_price INT(7),
    shipping_area VARCHAR(4),		
    product_category CHAR(16),		
    product_condition CHAR(8),		
    product_description	VARCHAR(128),		
    listing_status TINYINT(1),						
    listing_date DATE,		
    sales_status CHAR,		
    update_date	DATETIME,		
    product_upload_user	 INT(10),
    PRIMARY KEY(product_id,product_upload_user)
);

--取引情報テーブル
CREATE TABLE market_order_tbl(
    id						
    purchaser_id CHAR(32),					
    seller_id CHAR (10),					
    transaction_status CHAR(8),						
    transaction_startdate CHAR(8),				
    transaction_completeddate CHAR(8),    					
    total_amount INT(7),
    sales_profit INT(7),						
    shipping_cost INT(4),				
    total_commission INT(4),					
    shipping_status CHAR(8),			
    shipping_method	CHAR(16),			
    buyer_evaluation TINYINT(1),				
    seller_evaluation TINYINT(1),
    PRIMARY KEY(id)			
);

--取引メッセージテーブル
CREATE TABLE order_message_tbl(
    id CHAR(128),				
    order_message_date DATETIME					
    order_message_user_id INT(10),				
    transaction_id INT(32),		
    order_message_text VARCHAR(128),
    PRIMARY KEY(id,order_message_user_id,transaction_id)		
);

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