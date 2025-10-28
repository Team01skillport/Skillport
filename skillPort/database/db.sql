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
