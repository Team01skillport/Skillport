-- ユーザー情報テーブル作成
CREATE TABLE user_tbl(
id INT(10),
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
    user_id INT(10),
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
    user_id INT(10),
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
    favorites CHAR(32),
    product_view_flag TINYINT(1),
    user_id	CHAR(10),	
    PRIMARY KEY(id)
);

--出品情報テーブル
CREATE TABLE listing_tbl(
    product_id	VARCHAR(64),
    product_image VARCHAR(128),		
    product_name VARCHAR(128),		
    product_price INT(7),
    shipping_area VARCHAR(4),		
    product_category CHAR(16),		
    product_condition CHAR(8),		
    product_description	VARCHAR(255),		
    listing_status TINYINT(1),						
    listing_date DATE,		
    sales_status CHAR(8),		
    update_date	DATETIME NULL,		
    product_upload_user	 CHAR(10),
    PRIMARY KEY(product_id,product_upload_user)
);

--取引情報テーブル
CREATE TABLE market_order_tbl(
    id CHAR(32),				
    purchaser_id CHAR(10),					
    seller_id CHAR(10),					
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

--取引メッセージテーブル
CREATE TABLE order_message_tbl(
    id INT(128),				
    order_message_date DATETIME					
    order_message_user_id INT(10),				
    transaction_id INT(32),		
    order_message_text VARCHAR(128),
    PRIMARY KEY(id,order_message_user_id,transaction_id)		
);

--投稿フィードアップロードテーブル
CREATE TABLE post_tbl
