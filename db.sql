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

--メンバーシップ情報
CREATE TABLE membership_tbl(
    user_id INT(10),
    join_date DATE(10),
    renewal_date DATE(8),
    payment_status CHAR(16),
    payment_method CHAR(8),
    bonus_id CHAR(10),
    creator_id INT(10),
    PRIMARY KEY(user_id,creator_id)
);






