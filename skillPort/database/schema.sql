-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: skillport_db
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `feed_comment_tbl`
--

DROP TABLE IF EXISTS `feed_comment_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feed_comment_tbl` (
  `id` varchar(255) NOT NULL,
  `user_id` char(10) DEFAULT NULL,
  `post_id` varchar(255) DEFAULT NULL,
  `comment_text` varchar(128) DEFAULT NULL,
  `comment_date` datetime DEFAULT NULL,
  `father_comment_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feed_comment_tbl`
--

LOCK TABLES `feed_comment_tbl` WRITE;
/*!40000 ALTER TABLE `feed_comment_tbl` DISABLE KEYS */;
INSERT INTO `feed_comment_tbl` VALUES ('cmt0001','usr0002','pst0001','素敵な投稿ですね！','2025-10-01 10:20:00',NULL),('cmt0002','usr0003','pst0001','写真が綺麗！','2025-10-01 10:25:00',NULL),('cmt0003','usr0005','pst0002','いい商品ですね！','2025-10-02 09:15:00',NULL),('cmt0004','usr0006','pst0002','購入を考えています！','2025-10-02 09:30:00','cmt0003'),('cmt0005','usr0007','pst0003','ギター欲しい！','2025-10-03 13:00:00',NULL),('cmt0006','usr0004','pst0004','イベント楽しそう！','2025-10-03 18:10:00',NULL),('cmt0007','usr0008','pst0004','写真ありがとうございます！','2025-10-03 18:25:00','cmt0006'),('cmt0008','usr0009','pst0006','おめでとうございます！','2025-10-05 15:35:00',NULL),('cmt0009','usr0010','pst0007','カメラの設定教えてください','2025-10-06 17:40:00',NULL),('cmt0010','usr0001','pst0007','了解です！後で教えますね','2025-10-06 17:50:00','cmt0009');
/*!40000 ALTER TABLE `feed_comment_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feed_like_tbl`
--

DROP TABLE IF EXISTS `feed_like_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feed_like_tbl` (
  `id` varchar(255) NOT NULL,
  `post_id` varchar(255) DEFAULT NULL,
  `user_id` int(10) DEFAULT NULL,
  `like_time` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feed_like_tbl`
--

LOCK TABLES `feed_like_tbl` WRITE;
/*!40000 ALTER TABLE `feed_like_tbl` DISABLE KEYS */;
INSERT INTO `feed_like_tbl` VALUES ('like0001','pst0001',0,'2025-10-01'),('like0002','pst0001',0,'2025-10-01'),('like0003','pst0002',0,'2025-10-02'),('like0004','pst0003',0,'2025-10-02'),('like0005','pst0004',0,'2025-10-03'),('like0006','pst0006',0,'2025-10-05'),('like0007','pst0007',0,'2025-10-06'),('like0008','pst0008',0,'2025-10-07'),('like0009','pst0009',0,'2025-10-08'),('like0010','pst0010',0,'2025-10-09');
/*!40000 ALTER TABLE `feed_like_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listing_tbl`
--

DROP TABLE IF EXISTS `listing_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `listing_tbl` (
  `product_id` varchar(64) NOT NULL,
  `product_image` varchar(128) DEFAULT NULL,
  `product_name` varchar(128) DEFAULT NULL,
  `product_price` int(7) DEFAULT NULL,
  `shipping_area` varchar(4) DEFAULT NULL,
  `product_category` char(16) DEFAULT NULL,
  `product_condition` char(8) DEFAULT NULL,
  `product_description` varchar(255) DEFAULT NULL,
  `listing_status` tinyint(1) DEFAULT NULL,
  `listing_date` date DEFAULT NULL,
  `sales_status` char(8) DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `product_upload_user` char(10) NOT NULL,
  PRIMARY KEY (`product_id`,`product_upload_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listing_tbl`
--

LOCK TABLES `listing_tbl` WRITE;
/*!40000 ALTER TABLE `listing_tbl` DISABLE KEYS */;
INSERT INTO `listing_tbl` VALUES ('1001','image_1001.jpg','スニーカー',8500,'大阪','ファッション','新品','人気ブランドのスニーカーです',1,'2025-10-01','販売中','2025-10-01 12:30:00','1'),('1002','image_1002.jpg','ノートパソコン',78000,'東京','家電','中古','バッテリー良好、傷少なめ',1,'2025-09-28','販売中','2025-10-02 09:45:00','2'),('1003','image_1003.jpg','ギター',32000,'神奈川','楽器','新品','初心者向けのアコースティックギター',1,'2025-10-03','販売中','2025-10-03 15:10:00','3'),('1004','image_1004.jpg','コート',12000,'京都','ファッション','中古','少し使用感あり、サイズL',1,'2025-09-30','販売中','2025-10-04 08:20:00','4'),('1005','image_1005.jpg','スマートフォン',52000,'愛知','家電','新品','SIMフリー未使用品',1,'2025-10-05','販売中','2025-10-05 17:00:00','5'),('1006','image_1006.jpg','腕時計',25000,'大阪','アクセサリー','中古','保証書付き、動作確認済み',1,'2025-10-02','販売中','2025-10-06 11:45:00','6'),('1007','image_1007.jpg','カメラ',64000,'北海道','家電','中古','レンズに小傷あり、動作良好',1,'2025-09-27','販売中','2025-10-06 13:50:00','7'),('1008','image_1008.jpg','ソファ',18000,'兵庫','家具','中古','2人掛けソファ、少し使用感あり',1,'2025-10-01','販売中','2025-10-07 14:00:00','8'),('1009','image_1009.jpg','ヘッドフォン',9800,'千葉','家電','新品','ワイヤレスBluetoothモデル',1,'2025-10-04','販売中','2025-10-08 10:10:00','9'),('1010','image_1010.jpg','バッグ',13500,'福岡','ファッション','新品','レザーバッグ・未使用',1,'2025-10-06','販売中','2025-10-09 18:25:00','10');
/*!40000 ALTER TABLE `listing_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `market_order_tbl`
--

DROP TABLE IF EXISTS `market_order_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `market_order_tbl` (
  `id` char(32) NOT NULL,
  `purchaser_id` char(10) DEFAULT NULL,
  `seller_id` char(10) DEFAULT NULL,
  `transaction_status` char(8) DEFAULT NULL,
  `transaction_startdate` datetime DEFAULT NULL,
  `transaction_completeddate` datetime DEFAULT NULL,
  `total_amount` int(7) DEFAULT NULL,
  `sales_profit` int(7) DEFAULT NULL,
  `shipping_cost` int(4) DEFAULT NULL,
  `total_commission` int(4) DEFAULT NULL,
  `shipping_status` char(8) DEFAULT NULL,
  `shipping_method` char(16) DEFAULT NULL,
  `buyer_evaluation` int(5) DEFAULT NULL,
  `seller_evaluation` int(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `market_order_tbl`
--

LOCK TABLES `market_order_tbl` WRITE;
/*!40000 ALTER TABLE `market_order_tbl` DISABLE KEYS */;
INSERT INTO `market_order_tbl` VALUES ('ord0001','usr0001','usr0005','完了','2025-09-25 10:00:00','2025-09-30 14:00:00',8500,7200,500,800,'発送済み','ヤマト運輸',5,5),('ord0002','usr0002','usr0003','完了','2025-09-28 09:30:00','2025-10-02 16:00:00',32000,28000,700,1300,'発送済み','ゆうパック',4,5),('ord0003','usr0003','usr0007','進行中','2025-10-05 13:15:00',NULL,18000,15000,600,1200,'発送待ち','佐川急便',NULL,NULL),('ord0004','usr0004','usr0008','完了','2025-09-29 11:00:00','2025-10-03 18:20:00',52000,48000,800,1200,'発送済み','ヤマト運輸',5,5),('ord0005','usr0005','usr0002','キャンセル','2025-10-01 08:45:00','2025-10-01 09:10:00',12000,0,0,0,'未発送','なし',1,1),('ord0006','usr0006','usr0009','完了','2025-09-30 12:40:00','2025-10-04 15:50:00',9800,8700,400,700,'発送済み','ゆうメール',4,4),('ord0007','usr0007','usr0004','進行中','2025-10-07 17:00:00',NULL,25000,22000,600,900,'発送待ち','宅配便',NULL,NULL),('ord0008','usr0008','usr0001','完了','2025-09-26 09:25:00','2025-09-30 11:45:00',13500,12000,500,1000,'発送済み','佐川急便',5,5),('ord0009','usr0009','usr0010','完了','2025-09-27 14:10:00','2025-09-29 19:30:00',64000,60000,700,1300,'発送済み','ヤマト運輸',5,5),('ord0010','usr0010','usr0006','進行中','2025-10-06 15:00:00',NULL,78000,72000,900,1500,'発送準備','ゆうパック',NULL,NULL);
/*!40000 ALTER TABLE `market_order_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `membership_tbl`
--

DROP TABLE IF EXISTS `membership_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `membership_tbl` (
  `user_id` int(10) NOT NULL,
  `join_date` date DEFAULT NULL,
  `renewal_date` date DEFAULT NULL,
  `payment_status` char(16) DEFAULT NULL,
  `payment_method` char(8) DEFAULT NULL,
  `bonus_id` char(10) DEFAULT NULL,
  `creator_id` int(10) NOT NULL,
  PRIMARY KEY (`user_id`,`creator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membership_tbl`
--

LOCK TABLES `membership_tbl` WRITE;
/*!40000 ALTER TABLE `membership_tbl` DISABLE KEYS */;
INSERT INTO `membership_tbl` VALUES (1,'2023-01-15','2024-01-15','有効','クレカ','B000000001',101),(2,'2022-06-10','2023-06-10','期限切れ','銀行振込','B000000002',102),(3,'2024-02-01','2025-02-01','有効','PayPay','B000000003',103),(4,'2023-08-20','2024-08-20','停止中','クレカ','B000000004',104),(5,'2023-03-05','2024-03-05','有効','銀行振込','B000000005',105),(6,'2022-11-11','2023-11-11','期限切れ','コンビニ','B000000006',106),(7,'2024-04-30','2025-04-30','有効','クレカ','B000000007',107),(8,'2023-12-25','2024-12-25','有効','PayPay','B000000008',108),(9,'2023-07-14','2024-07-14','停止中','クレカ','B000000009',109),(10,'2022-09-01','2023-09-01','期限切れ','銀行振込','B000000010',110);
/*!40000 ALTER TABLE `membership_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_message_tbl`
--

DROP TABLE IF EXISTS `order_message_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_message_tbl` (
  `id` char(128) NOT NULL,
  `order_message_date` datetime DEFAULT NULL,
  `order_message_user_id` char(10) NOT NULL,
  `transaction_id` char(32) NOT NULL,
  `order_message_text` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`,`order_message_user_id`,`transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_message_tbl`
--

LOCK TABLES `order_message_tbl` WRITE;
/*!40000 ALTER TABLE `order_message_tbl` DISABLE KEYS */;
INSERT INTO `order_message_tbl` VALUES ('','2025-09-25 10:15:00','1','1','購入させていただきました、よろしくお願いします。'),('','2025-10-02 20:10:00','1','8','無事届いてよかったです、またよろしくお願いします。'),('','2025-10-06 15:25:00','10','10','発送はいつ頃になりますか？'),('','2025-09-28 09:20:00','2','2','発送予定日はいつ頃になりますか？'),('','2025-09-28 12:00:00','3','2','明日発送予定です、よろしくお願いします。'),('','2025-10-01 08:10:00','3','7','支払いが完了しました。'),('','2025-10-01 09:00:00','4','7','確認しました、発送準備中です。'),('','2025-09-25 10:45:00','5','1','ご購入ありがとうございます、すぐに発送準備します。'),('','2025-10-06 16:00:00','6','10','本日中に発送いたします。'),('','2025-10-02 19:40:00','8','8','商品届きました、ありがとうございました！');
/*!40000 ALTER TABLE `order_message_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_tbl`
--

DROP TABLE IF EXISTS `payment_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_tbl` (
  `user_id` int(10) NOT NULL,
  `card_num` int(16) NOT NULL,
  `card_name` char(16) DEFAULT NULL,
  `card_expiration` char(4) DEFAULT NULL,
  `card_block` tinyint(1) DEFAULT NULL,
  `bank_name` varchar(30) DEFAULT NULL,
  `bank_account_num` char(16) DEFAULT NULL,
  `branch_name` char(7) DEFAULT NULL,
  `branch_num` char(3) DEFAULT NULL,
  `acc_holder_name` char(16) DEFAULT NULL,
  `monthly_sales` int(16) DEFAULT NULL,
  `total_sales` int(16) DEFAULT NULL,
  `withdrawal` int(16) DEFAULT NULL,
  `account_type` char(10) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`card_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_tbl`
--

LOCK TABLES `payment_tbl` WRITE;
/*!40000 ALTER TABLE `payment_tbl` DISABLE KEYS */;
INSERT INTO `payment_tbl` VALUES (1,2147483647,'VISA','2608',0,'Mitsui Bank','1234567890123456','Namba','001','YAMADA TARO',50000,120000,30000,'普通'),(2,2147483647,'MasterCard','2507',0,'Mizuho Bank','9876543210987654','Shibuya','002','SUZUKI ICHIRO',72000,150000,50000,'当座'),(3,2147483647,'JCB','2701',1,'SMBC','0000111122223333','Umeda','003','SATO HANAKO',0,30000,0,'普通'),(4,2147483647,'Discover','2412',0,'Rakuten Bank','4444333322221111','Nagoya','004','TANAKA KEN',20000,80000,10000,'普通'),(5,2147483647,'VISA','2610',0,'MUFG','3333222211110000','Kyoto','005','YOSHIDA EMI',35000,100000,25000,'当座'),(6,2147483647,'MasterCard','2803',0,'PayPay Bank','5555666677778888','Tennoji','006','KOBAYASHI TAKU',60000,90000,40000,'普通'),(7,2147483647,'JCB','2905',0,'Japan Post Bank','1212121212121212','Osaka','007','KIMURA RYO',10000,30000,5000,'普通'),(8,2147483647,'Discover','2512',1,'Sony Bank','9090909090909090','Fukuoka','008','MORI HARUKA',0,5000,0,'普通'),(9,2147483647,'VISA','2709',0,'Shinsei Bank','8080808080808080','Sapporo','009','MATSUMOTO KEI',45000,60000,30000,'当座'),(10,2147483647,'MasterCard','2605',0,'Aeon Bank','2020202020202020','Kobe','010','NAKAMURA YUI',55000,75000,40000,'普通');
/*!40000 ALTER TABLE `payment_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_tbl`
--

DROP TABLE IF EXISTS `post_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post_tbl` (
  `id` char(128) NOT NULL,
  `user_id` char(10) DEFAULT NULL,
  `post_date` datetime DEFAULT NULL,
  `post_text` varchar(128) DEFAULT NULL,
  `post_media` varchar(128) DEFAULT NULL,
  `post_update_date` datetime DEFAULT NULL,
  `post_report_flag` tinyint(1) DEFAULT NULL,
  `post_status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_tbl`
--

LOCK TABLES `post_tbl` WRITE;
/*!40000 ALTER TABLE `post_tbl` DISABLE KEYS */;
INSERT INTO `post_tbl` VALUES ('pst0001','usr0001','2025-10-01 10:00:00','初めての投稿です！','img_post1.jpg','2025-10-01 10:00:00',0,1),('pst0002','usr0002','2025-10-02 08:30:00','新しい商品を紹介します！','item_20251002.png','2025-10-02 08:31:00',0,1),('pst0003','usr0003','2025-10-02 20:45:00','ギターが届いた！','guitar_post3.jpg','2025-10-02 21:00:00',0,1),('pst0004','usr0004','2025-10-03 12:00:00','大阪のイベントに行きました〜','event_osaka4.jpg','2025-10-03 12:10:00',0,1),('pst0005','usr0005','2025-10-04 09:50:00','投稿が通報されました','none','2025-10-04 10:00:00',1,0),('pst0006','usr0006','2025-10-05 15:20:00','フォロワー100人ありがとう！','img_celebration6.jpg','2025-10-05 15:30:00',0,1),('pst0007','usr0007','2025-10-06 17:15:00','新しいカメラで撮影しました????','camera_test7.png','2025-10-06 17:20:00',0,1),('pst0008','usr0008','2025-10-07 11:25:00','今日のランチ????','ramen8.jpg','2025-10-07 11:30:00',0,1),('pst0009','usr0009','2025-10-08 20:10:00','不適切な内容を含む投稿','none','2025-10-08 20:20:00',1,0),('pst0010','usr0010','2025-10-09 13:45:00','友達と旅行行った！最高！','trip10.png','2025-10-09 14:00:00',0,1);
/*!40000 ALTER TABLE `post_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_tbl`
--

DROP TABLE IF EXISTS `product_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_tbl` (
  `id` char(32) NOT NULL,
  `favorites` char(32) DEFAULT NULL,
  `product_view_flag` tinyint(1) DEFAULT NULL,
  `user_id` char(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_tbl`
--

LOCK TABLES `product_tbl` WRITE;
/*!40000 ALTER TABLE `product_tbl` DISABLE KEYS */;
INSERT INTO `product_tbl` VALUES ('prd0001','125',1,'usr0001'),('prd0002','58',1,'usr0002'),('prd0003','342',1,'usr0003'),('prd0004','0',0,'usr0004'),('prd0005','76',1,'usr0005'),('prd0006','189',1,'usr0006'),('prd0007','250',0,'usr0007'),('prd0008','12',1,'usr0008'),('prd0009','480',1,'usr0009'),('prd0010','33',0,'usr0010');
/*!40000 ALTER TABLE `product_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `support_tbl`
--

DROP TABLE IF EXISTS `support_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `support_tbl` (
  `id` varchar(255) NOT NULL,
  `category` char(16) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `inquiry_user_id` char(10) DEFAULT NULL,
  `send_date` datetime DEFAULT NULL,
  `receiving_date` datetime DEFAULT NULL,
  `response_status` char(16) DEFAULT NULL,
  `response_date` datetime DEFAULT NULL,
  `attached_file` varchar(255) DEFAULT NULL,
  `response_content` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `support_tbl`
--

LOCK TABLES `support_tbl` WRITE;
/*!40000 ALTER TABLE `support_tbl` DISABLE KEYS */;
INSERT INTO `support_tbl` VALUES ('sup001','ログイン','パスワードを忘れてしまいました。','user001','2025-10-01 09:15:00','2025-10-01 09:16:00','対応済み','2025-10-01 10:00:00',NULL,'パスワード再設定のリンクを送信しました。'),('sup002','バグ報告','動画が再生途中で止まります。','user002','2025-10-01 12:30:00','2025-10-01 12:31:00','確認中',NULL,'error_log.txt',NULL),('sup003','アカウント','ユーザー名を変更したいです。','user003','2025-10-02 08:45:00','2025-10-02 08:46:00','対応済み','2025-10-02 09:20:00',NULL,'ユーザー名を更新しました。'),('sup004','その他','プレミアムプランの詳細を教えてください。','user004','2025-10-02 14:10:00','2025-10-02 14:12:00','対応済み','2025-10-02 14:45:00',NULL,'料金と機能の詳細をメールでご案内しました。'),('sup005','動画アップロード','アップロードが途中で失敗します。','user005','2025-10-03 11:20:00','2025-10-03 11:22:00','対応中',NULL,'upload_error.png',NULL),('sup006','コメント','コメントが投稿できません。','user006','2025-10-03 16:00:00','2025-10-03 16:01:00','対応済み','2025-10-03 17:00:00',NULL,'一時的な不具合を修正しました。'),('sup007','バグ報告','スマホでページが崩れています。','user007','2025-10-04 09:50:00','2025-10-04 09:52:00','確認中',NULL,'screenshot.jpg',NULL),('sup008','アカウント','退会方法を教えてください。','user002','2025-10-04 15:30:00','2025-10-04 15:32:00','対応済み','2025-10-04 16:00:00',NULL,'退会ページへのリンクをご案内しました。'),('sup009','動画再生','音声が出ません。','user003','2025-10-05 10:10:00','2025-10-05 10:12:00','対応中',NULL,NULL,NULL),('sup010','その他','機能の追加要望があります。','user001','2025-10-05 20:00:00','2025-10-05 20:01:00','未対応',NULL,NULL,NULL);
/*!40000 ALTER TABLE `support_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tbl`
--

DROP TABLE IF EXISTS `user_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_tbl` (
  `id` int(10) NOT NULL,
  `user_name` char(16) DEFAULT NULL,
  `first_name` char(8) DEFAULT NULL,
  `last_name` char(8) DEFAULT NULL,
  `first_name_katakana` char(8) DEFAULT NULL,
  `last_name_katakana` char(8) DEFAULT NULL,
  `tel_no` char(12) DEFAULT NULL,
  `zip_code` char(7) DEFAULT NULL,
  `prefecture` varchar(20) DEFAULT NULL,
  `address1` varchar(20) DEFAULT NULL,
  `address2` varchar(20) DEFAULT NULL,
  `address3` varchar(20) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `mail` varchar(32) DEFAULT NULL,
  `password` char(32) DEFAULT NULL,
  `introduction` varchar(100) DEFAULT NULL,
  `report_flag` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tbl`
--

LOCK TABLES `user_tbl` WRITE;
/*!40000 ALTER TABLE `user_tbl` DISABLE KEYS */;
INSERT INTO `user_tbl` VALUES (1,'tanaka01','太郎','田中','タロウ','タナカ','8012345678','5300001','大阪府','大阪市北区','梅田','1-2-3','1980-05-12','tanaka@example.com','pass1234','趣味は釣りです。',0),(2,'suzuki02','花子','鈴木','ハナコ','スズキ','9012345678','1500001','東京都','渋谷区','神宮前','4-5-6','1992-07-03','suzuki@example.com','flower22','旅行が好きです。',0),(3,'sato03','健','佐藤','ケン','サトウ','7011112222','9800011','宮城県','仙台市青葉区','中央','7-8-9','1988-03-19','sato@example.com','kenpass','スポーツ観戦が趣味です。',0),(4,'kobayashi04','真由美','小林','マユミ','コバヤシ','6012223333','4600008','愛知県','名古屋市中区','栄','2-3-4','1995-09-25','kobayashi@example.com','mayu456','カフェ巡りが好きです。',0),(5,'watanabe05','翔太','渡辺','ショウタ','ワタナベ','5013334444','8100001','福岡県','福岡市中央区','天神','5-6-7','1990-12-11','watanabe@example.com','sho999','映画を見るのが趣味です。',0),(6,'yamamoto06','絵里','山本','エリ','ヤマモト','4014445555','6008001','京都府','京都市下京区','四条通','1-1-1','1997-01-04','yamamoto@example.com','eri321','音楽が大好きです。',0),(7,'nakamura07','健太','中村','ケンタ','ナカムラ','3015556666','9800811','宮城県','仙台市青葉区','一番町','10-2-3','1993-04-20','nakamura@example.com','kenta789','料理が得意です。',0),(8,'matsumoto08','裕子','松本','ユウコ','マツモト','2016667777','5500013','大阪府','大阪市西区','新町','2-4-5','1985-11-09','matsumoto@example.com','yuko555','読書が好きです。',0),(9,'inoue09','直樹','井上','ナオキ','イノウエ','1017778888','9800021','宮城県','仙台市青葉区','中央','6-7-8','1989-08-18','inoue@example.com','naoki12','ジョギングを毎朝しています。',0),(10,'takahashi10','美咲','高橋','ミサキ','タカハシ','9018889999','1000001','東京都','千代田区','千代田','9-9-9','1998-02-15','takahashi@example.com','misaki321','猫が大好きです。',0);
/*!40000 ALTER TABLE `user_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_comment_tbl`
--

DROP TABLE IF EXISTS `video_comment_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_comment_tbl` (
  `comment_id` varchar(255) NOT NULL,
  `video_id` varchar(64) NOT NULL,
  `commentor_id` char(10) DEFAULT NULL,
  `comment_date` datetime DEFAULT NULL,
  `comment_text` varchar(64) DEFAULT NULL,
  `parent_comment_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`comment_id`,`video_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_comment_tbl`
--

LOCK TABLES `video_comment_tbl` WRITE;
/*!40000 ALTER TABLE `video_comment_tbl` DISABLE KEYS */;
INSERT INTO `video_comment_tbl` VALUES ('cmt001','vid001','user001','2025-10-01 12:00:00','最高の動画ですね！',NULL),('cmt002','vid001','user002','2025-10-01 12:05:30','編集がうまい！',NULL),('cmt003','vid001','user003','2025-10-01 12:10:15','同意です！','cmt002'),('cmt004','vid002','user004','2025-10-02 09:20:00','音質めっちゃ良い！',NULL),('cmt005','vid002','user005','2025-10-02 09:35:50','途中の展開好き',NULL),('cmt006','vid003','user006','2025-10-03 14:10:00','サムネに惹かれた笑',NULL),('cmt007','vid003','user007','2025-10-03 14:12:30','同じく！','cmt006'),('cmt008','vid004','user002','2025-10-04 11:00:00','投稿お疲れ様です！',NULL),('cmt009','vid004','user003','2025-10-04 11:03:15','もっと見たい！',NULL),('cmt010','vid005','user001','2025-10-05 16:45:00','また次も期待してます！',NULL);
/*!40000 ALTER TABLE `video_comment_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_like_tbl`
--

DROP TABLE IF EXISTS `video_like_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_like_tbl` (
  `id` varchar(255) NOT NULL,
  `video_id` varchar(255) NOT NULL,
  `video_uploader_id` char(10) DEFAULT NULL,
  `video_like_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`,`video_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_like_tbl`
--

LOCK TABLES `video_like_tbl` WRITE;
/*!40000 ALTER TABLE `video_like_tbl` DISABLE KEYS */;
INSERT INTO `video_like_tbl` VALUES ('user001','vid001','upl001','2025-10-01 12:34:56'),('user001','vid003','upl003','2025-10-02 11:10:45'),('user002','vid001','upl001','2025-10-01 12:35:12'),('user002','vid005','upl005','2025-10-05 18:55:33'),('user003','vid002','upl002','2025-10-02 09:22:18'),('user003','vid004','upl004','2025-10-05 17:40:10'),('user004','vid003','upl003','2025-10-02 10:45:00'),('user005','vid004','upl004','2025-10-03 14:25:30'),('user006','vid005','upl005','2025-10-03 16:50:00'),('user007','vid002','upl002','2025-10-04 08:15:20');
/*!40000 ALTER TABLE `video_like_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_review_tbl`
--

DROP TABLE IF EXISTS `video_review_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_review_tbl` (
  `review_id` varchar(255) NOT NULL,
  `video_id` varchar(255) DEFAULT NULL,
  `reviewer_id` char(16) DEFAULT NULL,
  `review_status` char(8) DEFAULT NULL,
  `review_result_comment` varchar(255) DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_review_tbl`
--

LOCK TABLES `video_review_tbl` WRITE;
/*!40000 ALTER TABLE `video_review_tbl` DISABLE KEYS */;
INSERT INTO `video_review_tbl` VALUES ('rev001','vid001','admin01','承認','問題なし。公開を許可しました。','2025-10-01 09:30:00','2025-10-01 09:00:00','2025-10-01 09:31:00'),('rev002','vid002','admin02','修正','タイトルに不適切な単語があります。','2025-10-01 10:45:00','2025-10-01 10:20:00','2025-10-01 10:46:00'),('rev003','vid003','admin01','承認','映像・音声ともに問題なし。','2025-10-02 08:10:00','2025-10-02 07:55:00','2025-10-02 08:11:00'),('rev004','vid004','admin03','拒否','著作権素材が使用されています。','2025-10-02 14:25:00','2025-10-02 14:00:00','2025-10-02 14:26:00'),('rev005','vid005','admin02','修正','音量バランスに問題あり。','2025-10-03 11:40:00','2025-10-03 11:15:00','2025-10-03 11:41:00'),('rev006','vid006','admin01','承認','適切な内容です。','2025-10-03 16:05:00','2025-10-03 15:45:00','2025-10-03 16:06:00'),('rev007','vid007','admin03','拒否','暴力的な描写が含まれています。','2025-10-04 09:20:00','2025-10-04 09:00:00','2025-10-04 09:21:00'),('rev008','vid008','admin02','承認','短くて見やすい動画でした。','2025-10-04 13:00:00','2025-10-04 12:40:00','2025-10-04 13:01:00'),('rev009','vid009','admin01','修正','説明文が不足しています。','2025-10-05 10:15:00','2025-10-05 09:55:00','2025-10-05 10:16:00'),('rev010','vid010','admin03','承認','内容・品質ともに良好。','2025-10-05 18:30:00','2025-10-05 18:10:00','2025-10-05 18:31:00');
/*!40000 ALTER TABLE `video_review_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_tbl`
--

DROP TABLE IF EXISTS `video_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_tbl` (
  `id` varchar(255) NOT NULL,
  `video_title` char(32) DEFAULT NULL,
  `video_length` int(5) DEFAULT NULL,
  `video_uploader_id` char(10) NOT NULL,
  `video_upload_date` datetime DEFAULT NULL,
  `video_description_section` varchar(255) DEFAULT NULL,
  `video_public_status` tinyint(1) DEFAULT NULL,
  `video_category` char(16) DEFAULT NULL,
  `video_tag` char(16) DEFAULT NULL,
  `video_report_flag` tinyint(1) DEFAULT NULL,
  `video_popularity_index` float DEFAULT NULL,
  `view_count` int(10) DEFAULT NULL,
  `like_count` int(10) DEFAULT NULL,
  `comment_count` int(10) DEFAULT NULL,
  `file_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`,`video_uploader_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_tbl`
--

LOCK TABLES `video_tbl` WRITE;
/*!40000 ALTER TABLE `video_tbl` DISABLE KEYS */;
INSERT INTO `video_tbl` VALUES ('vid0001','街ブラ日記',320,'usr0001','2025-09-25 10:00:00','大阪の街を散歩しながら紹介します。',1,'旅行','#大阪',0,7.8,2300,150,12,'/videos/vid0001.mp4'),('vid0002','ギター練習',420,'usr0002','2025-09-26 14:10:00','初心者向けギターコード練習講座',1,'音楽','#ギター',0,8.3,5400,380,45,'/videos/vid0002.mp4'),('vid0003','英語勉強法',600,'usr0003','2025-09-27 09:30:00','短期間で英語力を伸ばすコツを紹介',1,'教育','#英語',0,9,10200,890,65,'/videos/vid0003.mp4'),('vid0004','猫の一日',210,'usr0004','2025-09-28 17:50:00','うちの猫の可愛い日常です????',1,'ペット','#猫',0,6.2,1200,95,8,'/videos/vid0004.mp4'),('vid0005','料理チャレンジ',540,'usr0005','2025-09-29 19:00:00','初めてのパスタ作り挑戦！',1,'料理','#パスタ',0,7,3400,220,30,'/videos/vid0005.mp4'),('vid0006','メイク講座',480,'usr0006','2025-09-30 12:00:00','ナチュラルメイクのやり方を紹介',1,'美容','#メイク',0,8.1,7800,540,42,'/videos/vid0006.mp4'),('vid0007','筋トレ日記',360,'usr0007','2025-10-01 08:30:00','今日のワークアウトルーティン',1,'フィットネス','#筋トレ',0,9.3,15000,1200,110,'/videos/vid0007.mp4'),('vid0008','夜景撮影',260,'usr0008','2025-10-02 21:00:00','カメラ設定と撮影のコツを紹介',1,'カメラ','#夜景',0,8.5,6500,410,27,'/videos/vid0008.mp4'),('vid0009','日常Vlog',300,'usr0009','2025-10-03 10:40:00','朝のルーティンを紹介します',1,'ライフスタイル','#vlog',0,7.2,2100,170,15,'/videos/vid0009.mp4'),('vid0010','炎上事件',400,'usr0010','2025-10-04 13:15:00','内容が不適切と報告されました',0,'ニュース','#炎上',1,2.1,500,20,8,'/videos/vid0010.mp4');
/*!40000 ALTER TABLE `video_tbl` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-16 12:15:36
