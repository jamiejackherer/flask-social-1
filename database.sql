-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: localhost    Database: social
-- ------------------------------------------------------
-- Server version	5.7.23-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('10866fe46656');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `followers`
--

DROP TABLE IF EXISTS `followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `followers` (
  `follower_id` int(11) DEFAULT NULL,
  `followed_id` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  KEY `followed_id` (`followed_id`),
  KEY `follower_id` (`follower_id`),
  CONSTRAINT `followers_ibfk_1` FOREIGN KEY (`followed_id`) REFERENCES `user` (`id`),
  CONSTRAINT `followers_ibfk_2` FOREIGN KEY (`follower_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `followers`
--

LOCK TABLES `followers` WRITE;
/*!40000 ALTER TABLE `followers` DISABLE KEYS */;
INSERT INTO `followers` VALUES (1,5,'2018-10-11 20:40:08'),(2,7,'2018-10-11 20:40:08'),(7,1,'2018-10-11 20:40:08'),(6,1,'2018-10-13 19:20:03'),(6,3,'2018-10-22 00:15:16'),(6,8,'2018-10-22 00:15:20'),(8,1,'2018-10-22 00:29:54'),(3,4,'2018-10-23 20:09:11'),(3,1,'2018-10-23 20:09:12'),(4,6,'2018-10-23 20:16:55');
/*!40000 ALTER TABLE `followers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `payload_json` text COLLATE utf8mb4_unicode_ci,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_notification_created` (`created`),
  CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
INSERT INTO `notification` VALUES (9,2,'{\"notifier_id\": 1, \"post_id\": 11, \"name\": \"post_like\"}','2018-10-15 01:56:53'),(10,2,'{\"notifier_id\": 1, \"comment_id\": 5, \"name\": \"comment\"}','2018-10-15 01:56:57'),(11,2,'{\"notifier_id\": 1, \"comment_id\": 5, \"name\": \"comment_like_post\", \"post_id\": 6}','2018-10-15 01:56:59'),(14,2,'{\"notifier_id\": 1, \"comment_id\": 6, \"name\": \"comment\", \"post_id\": 6}','2018-10-15 01:57:15'),(15,2,'{\"notifier_id\": 1, \"comment_id\": 6, \"name\": \"comment_like_post\", \"post_id\": 11}','2018-10-15 01:57:16'),(17,8,'{\"notifier_id\": 1, \"post_id\": 10, \"name\": \"post_like\"}','2018-10-15 01:57:32'),(18,2,'{\"notifier_id\": 1, \"post_id\": 6, \"name\": \"post_like\"}','2018-10-15 02:27:29'),(19,2,'{\"notifier_id\": 1, \"post_id\": 23, \"name\": \"post_like\"}','2018-10-15 02:27:32'),(27,4,'{\"notifier_id\": 1, \"comment_id\": 9, \"name\": \"comment\"}','2018-10-21 19:42:16'),(32,1,'{\"notifier_id\": 6, \"comment_id\": 11, \"name\": \"comment\", \"post_id\": 18}','2018-10-22 00:14:04'),(37,2,'{\"notifier_id\": 1, \"post_id\": 21, \"name\": \"post_like\"}','2018-10-22 07:04:48'),(43,1,'{\"notifier_id\": 3, \"post_id\": 27, \"name\": \"follow\"}','2018-10-23 20:09:12'),(44,3,'{\"post_id\": 27, \"notifier_id\": 6, \"name\": \"post_like\"}','2018-10-23 20:09:39'),(45,3,'{\"notifier_id\": 6, \"post_id\": 27, \"name\": \"comment\", \"comment_id\": 12}','2018-10-23 20:10:03'),(46,3,'{\"notifier_id\": 7, \"post_id\": 27, \"name\": \"post_like\", \"comment_id\": 12}','2018-10-23 20:10:18'),(47,3,'{\"post_id\": 27, \"notifier_id\": 7, \"name\": \"comment\", \"comment_id\": 13}','2018-10-23 20:10:32'),(48,6,'{\"post_id\": 27, \"notifier_id\": 7, \"name\": \"comment_like\", \"comment_id\": 12}','2018-10-23 20:10:36'),(49,3,'{\"post_id\": 27, \"notifier_id\": 7, \"name\": \"comment_like_post\", \"comment_id\": 12}','2018-10-23 20:10:36'),(50,7,'{\"notifier_id\": 3, \"post_id\": 27, \"name\": \"comment_like\", \"comment_id\": 13}','2018-10-23 20:11:12'),(51,6,'{\"notifier_id\": 3, \"post_id\": 27, \"name\": \"comment_like\", \"comment_id\": 12}','2018-10-23 20:11:14');
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `deleted` datetime DEFAULT NULL,
  `updated` datetime NOT NULL,
  `body` text COLLATE utf8mb4_unicode_ci,
  `author_id` int(11) DEFAULT NULL,
  `recipient_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `recipient_id` (`recipient_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`),
  CONSTRAINT `post_ibfk_2` FOREIGN KEY (`recipient_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (1,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','Hey Tammy, how\'s it going?',1,6),(2,0,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','Hey guys this is Daniel. You shouldn\'t see this post because it should be inactive.',1,1),(3,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','Hey guys, it\'s Jennifer. No one should see this, since I\'m a disabled user.',5,5),(4,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','Hey Daniel. You should\'t see this message on your wall, since I\'m a disabled user.',5,1),(5,0,'2018-10-15 00:45:03','2018-10-15 01:25:07','2018-10-15 01:25:07','Some other text.',1,1),(6,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','The D.L. Serventy Medal may be awarded annually by the Birdlife Australia for outstanding published work on birds in the Australasian region. It commemorates Dr Dominic Serventy (1904–1988) and was first awarded in 1991.[1] Source: Birdlife Australia Protogyrinus sculpturatus is a species of beetle in the family Gyrinidae, the only species in the genus Protogyrinus.',2,2),(7,0,'2018-10-11 20:40:00','2018-10-23 20:08:20','2018-10-23 20:08:20','Garner first worked for the Conservative Party as an organiser for the Young Conservatives in Yorkshire in 1948.[1] He revived the membership by organising fundraising weekends at Filey Holiday Camp.[1] By 1951, he became a Conservative Party agent in Halifax, West Yorkshire.',3,3),(8,0,'2018-10-11 20:40:00','2018-10-23 20:16:36','2018-10-23 20:16:36','In 1903 the building was purchased by Wijewardena\'s mother, Helena, who subsequently demolished the existing residence and rebuilt a new dwelling, Sri Ramya.[4] The new dwelling was designed by Herbert Henry Reid.[4] Wijewardena occupied the residence until her death in 1940. In May 1934, the Indian poet, Rabindranath Tagore and the Indian painter, Nandalal Bose, stayed at the house for a fortnight, when Tagore brought a troupe of Bengali dancers to Ceylon.',4,4),(9,0,'2018-10-15 01:59:22','2018-10-23 20:18:20','2018-10-23 20:18:20','What time is everyone going to the game tonight?',1,1),(10,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','In 1951 the building was purchased by the Government of the United States to serve as the chancery of its Embassy in Sri Lanka.[4] It functioned in that capacity until the United States Embassy moved to a new premises in 1984 and the building was transferred to USAid, for use as their offices.[5][6] Gamekeeper\'s thumb (also known as skier\'s thumb or UCL tear) is a type of injury to the ulnar collateral ligament (UCL) of the thumb.',8,8),(11,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','Traffic classification describes the methods of classifying traffic by observing features passively in the traffic, and in line to particular classification goals. There might be some that only have a vulgar classification goal. For example, whether it is bulk transfer, peer to peer file sharing or transaction-orientated.',2,2),(12,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','The basis of categorizing work is to classify the type of Internet traffic; this is done by putting common groups of applications into different categories, e.g., \"normal\" versus \"malicious\", or more complex definitions, e.g., the identification of specific applications or specific Transmission Control Protocol (TCP) implementations.',7,7),(13,0,'2018-10-11 20:40:00','2018-10-23 20:18:22','2018-10-23 20:18:22','The village itself is a designated conservation area, whilst the entire parish is located within the Dedham Vale Area of Outstanding Natural Beauty. It also contains Rowley Grove, a nature reserve classed as Ancient Woodland and a point to point racecourse which is home to the Waveney Harriers.',1,1),(14,0,'2018-10-11 20:40:00','2018-10-23 20:16:38','2018-10-23 20:16:38','Sir Anthony Stuart Garner (28 January 1927 – 22 March 2015) was a political organiser for the British Conservative Party. Anthony Garner was born on 28 February 1927 in Liverpool, England.[1][2] He was educated at Liverpool College.',4,4),(15,0,'2018-10-11 20:40:00','2018-10-23 20:16:41','2018-10-23 20:16:41','Symptoms of gamekeeper\'s thumb are instability of the MCP joint of the thumb, accompanied by pain and weakness of the pinch grasp. The severity of the symptoms are related to the extent of the initial tear of the UCL (in the case of Skier\'s thumb), or how long the injury has been allowed to progress (in the case of gamekeeper\'s thumb). Characteristic signs include pain, swelling, and ecchymosis around the thenar eminence, and especially over the MCP joint of the thumb.',4,4),(16,0,'2018-10-11 20:40:00','2018-10-23 20:13:38','2018-10-23 20:13:38','Some people argue that the new plan on Internet tax would prove disadvantageous to the country’s economic development, limit access to information and hinder the freedom of expression.[7] Approximately 36,000 people have signed up to take part in an event on Facebook to be held outside the Economy Ministry to protest against the possible tax.',6,6),(17,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','In October 2013, Swenson was cast as Inspector Javert in the 2014 Broadway revival of Les Misérables, which opened in March 2014 at New York\'s Imperial Theatre, where the musical had previously run for 13 years.[9] In 2018, Swenson played Satan in the New Group\'s off-Broadway production of \"Jerry Springer: The Opera.\" Swenson met his first wife Amy (née Westerby) while they were both in one of his grandmother\'s comedies, Hopsville Holiday.',8,8),(18,0,'2018-10-11 20:40:00','2018-10-21 23:52:17','2018-10-21 23:52:17','According to Yahoo News, economy minister Mihály Varga defended the move saying \"the tax was fair as it reflected a shift by consumers to the Internet away from phone lines\" and that \"150 forints on each transferred gigabyte of data – was needed to plug holes in the 2015 budget of one of the EU’s most indebted nations\".',1,1),(19,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','Hey Tammy! I just wanted to post on your wall. Curabitur eleifend himenaeos lorem ad lectus pulvinar cubilia tellus, erat ad tempus aenean urna nostra sapien mauris eleifen tempor convallis fames taciti nam lectus lacinia.',1,6),(20,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','Hey Jordan, how\'s it going? I just wanted to see how are? Nulla fringilla tempus ante litora sit diam et adipiscing ultricies eu, duis a nisi dictumst interdum mauris aliquam etiam senectus quis leo nam.',3,7),(21,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','Hey baby! How\'s it going? What are you going to do tonight? ',2,1),(22,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','Hey Sheree! I\'m doing well. I don\'t know what I\'m going to do yet. Let\'s definitely hang out though.',1,2),(23,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','A planned tax on Internet use in Hungary introduced a 150-forint (US$0.62, €0.47) tax per gigabyte of data traffic, in a move intended to reduce Internet traffic and also assist companies to offset corporate income tax against the new levy.[5] Hungary achieved 1.',2,2),(24,1,'2018-10-11 20:40:00',NULL,'2018-10-11 20:40:00','The Food Safety Act 1990[1][2] is an Act of the Parliament of the United Kingdom. It is the statutory obligation to treat food intended for human consumption in a controlled and managed way. The key requirements of the Act are that food must comply with food safety requirements, must be \"of the nature, substance and quality demanded\", and must be correctly described (labelled).',8,8),(25,0,'2018-10-11 20:40:00','2018-10-23 20:16:43','2018-10-23 20:16:43','The patient will often manifest a weakened ability to grasp objects or perform such tasks as tying shoes and tearing a piece of paper. Other complaints include intense pain experienced upon catching the thumb on an object, such as when reaching into a pants pocket. Gamekeeper\'s thumb and skier\'s thumb are two similar conditions, both of which involve insufficiency of the ulnar collateral ligament (UCL) of the thumb. The chief difference between these two conditions is that Skier\'s thumb is generally considered to be an acute condition acquired after a fall or similar abduction injury to the metacarpophalangeal (MCP) joint of the thumb, whereas gamekeeper\'s thumb typically refers to a chronic condition which has developed as a result of repeated episodes of lower-grade hyperabduction over a period of time.',4,4),(26,0,'2018-10-11 20:40:21','2018-10-11 21:24:56','2018-10-11 21:24:56','?',1,1),(27,1,'2018-10-23 20:08:56',NULL,'2018-10-23 20:08:56','Hey guys, does anyone know what time the game starts tonight? A bunch of friends and I are going down the street to watch the game, if anyone wants to join?',3,3),(28,1,'2018-10-23 20:15:28',NULL,'2018-10-23 20:15:28','Has anyone seen the movie \"It\"? That clown was sooooo creepy!',6,6),(29,1,'2018-10-23 20:18:59',NULL,'2018-10-23 20:18:59','wtf\r\n',6,6);
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_comment`
--

DROP TABLE IF EXISTS `post_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `deleted` datetime DEFAULT NULL,
  `updated` datetime NOT NULL,
  `body` text COLLATE utf8mb4_unicode_ci,
  `post_id` int(11) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `post_comment_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`),
  CONSTRAINT `post_comment_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_comment`
--

LOCK TABLES `post_comment` WRITE;
/*!40000 ALTER TABLE `post_comment` DISABLE KEYS */;
INSERT INTO `post_comment` VALUES (1,1,'2018-10-15 01:24:49',NULL,'2018-10-15 01:24:49','Testing',5,1),(2,0,'2018-10-15 01:25:24','2018-10-15 01:26:44','2018-10-15 01:26:44','Testing',6,1),(3,0,'2018-10-15 01:26:27','2018-10-15 01:26:41','2018-10-15 01:26:41','Testing',6,1),(4,0,'2018-10-15 01:26:32','2018-10-15 01:26:35','2018-10-15 01:26:35','Cheese',6,1),(5,1,'2018-10-15 01:56:57',NULL,'2018-10-15 01:56:57','Testing',6,1),(6,1,'2018-10-15 01:57:14',NULL,'2018-10-15 01:57:14','How\'s it going?',11,1),(7,1,'2018-10-15 01:57:38',NULL,'2018-10-15 01:57:38','Testing',9,1),(8,1,'2018-10-15 02:27:38',NULL,'2018-10-15 02:27:38','Testing',7,1),(9,1,'2018-10-21 19:42:16',NULL,'2018-10-21 19:42:16','Haha, that\'s funny, Susan!',14,1),(10,1,'2018-10-22 00:11:39',NULL,'2018-10-22 00:11:39','Good one Susan!',15,1),(11,1,'2018-10-22 00:14:03',NULL,'2018-10-22 00:14:03','I\'ll be there at 7.',9,6),(12,1,'2018-10-23 20:10:03',NULL,'2018-10-23 20:10:03','I\'m pretty sure it starts at 7. Where are you guys going to watch the game?',27,6),(13,1,'2018-10-23 20:10:32',NULL,'2018-10-23 20:10:32','I\'m down. Just let me know when and where.',27,7),(14,1,'2018-10-23 20:11:53',NULL,'2018-10-23 20:11:53','We\'re going to Rooster Joe\'s. It\'s on the corner of Dunlap and 64th.\r\n\r\nJordan, call me in a little bit.',27,3);
/*!40000 ALTER TABLE `post_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_comment_edit`
--

DROP TABLE IF EXISTS `post_comment_edit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post_comment_edit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` text COLLATE utf8mb4_unicode_ci,
  `user_id` int(11) DEFAULT NULL,
  `comment_id` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `comment_id` (`comment_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_comment_edit_ibfk_1` FOREIGN KEY (`comment_id`) REFERENCES `post_comment` (`id`),
  CONSTRAINT `post_comment_edit_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_comment_edit`
--

LOCK TABLES `post_comment_edit` WRITE;
/*!40000 ALTER TABLE `post_comment_edit` DISABLE KEYS */;
/*!40000 ALTER TABLE `post_comment_edit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_comment_like`
--

DROP TABLE IF EXISTS `post_comment_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post_comment_like` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `comment_id` int(11) DEFAULT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comment_id` (`comment_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_comment_like_ibfk_1` FOREIGN KEY (`comment_id`) REFERENCES `post_comment` (`id`),
  CONSTRAINT `post_comment_like_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_comment_like`
--

LOCK TABLES `post_comment_like` WRITE;
/*!40000 ALTER TABLE `post_comment_like` DISABLE KEYS */;
INSERT INTO `post_comment_like` VALUES (1,1,5,'2018-10-15 01:56:59'),(2,1,6,'2018-10-15 01:57:16'),(3,1,7,'2018-10-15 01:57:41'),(4,1,8,'2018-10-15 02:27:48'),(5,1,11,'2018-10-22 07:04:56'),(6,7,12,'2018-10-23 20:10:36'),(7,3,13,'2018-10-23 20:11:12'),(8,3,12,'2018-10-23 20:11:14');
/*!40000 ALTER TABLE `post_comment_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_edit`
--

DROP TABLE IF EXISTS `post_edit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post_edit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` text COLLATE utf8mb4_unicode_ci,
  `user_id` int(11) DEFAULT NULL,
  `post_id` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_edit_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`),
  CONSTRAINT `post_edit_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_edit`
--

LOCK TABLES `post_edit` WRITE;
/*!40000 ALTER TABLE `post_edit` DISABLE KEYS */;
INSERT INTO `post_edit` VALUES (1,'The American Center or the former United States Chancery are currently used as the offices of USAid in Colombo, Sri Lanka. The building is located on Galle Road, Colombo. The building was originally built by J. H. Meedeniya Adigar, which he named Rickman House. It was the home of D. R. Wijewardena (the founder of the Lake House newspaper group), who married Meedeniya\'s eldest daughter Alice.[1][2] The property is relatively unique as its land title, under the original old Dutch deed, extends down to the ocean, only one of a few such cases in Colombo.',1,5,'2018-10-11 20:40:00'),(2,'Swenson and actress Audra McDonald became engaged in January 2012[10] and were married on October 6, 2012. [11] In October 2016, McDonald and Swenson welcomed their first child, Sally. The Flaxbourne River is a river in the Marlborough region of New Zealand. It arises in the Inland Kaikoura Range and Halden Hills and flows east and then south-east into the South Pacific Ocean near Ward.',1,9,'2018-10-11 20:40:00'),(3,'Editing my post',1,9,'2018-10-15 01:59:22'),(4,'Editing my post.',1,9,'2018-10-21 19:41:22');
/*!40000 ALTER TABLE `post_edit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_like`
--

DROP TABLE IF EXISTS `post_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post_like` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `post_id` int(11) DEFAULT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_like_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`),
  CONSTRAINT `post_like_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_like`
--

LOCK TABLES `post_like` WRITE;
/*!40000 ALTER TABLE `post_like` DISABLE KEYS */;
INSERT INTO `post_like` VALUES (1,1,5,'2018-10-15 01:24:43'),(4,1,11,'2018-10-15 01:56:53'),(6,1,7,'2018-10-15 01:57:07'),(8,1,10,'2018-10-15 01:57:32'),(10,1,6,'2018-10-15 02:27:29'),(11,1,23,'2018-10-15 02:27:32'),(12,1,8,'2018-10-15 02:27:58'),(13,1,9,'2018-10-20 16:53:04'),(14,1,14,'2018-10-21 19:41:55'),(15,1,25,'2018-10-21 23:53:08'),(16,1,15,'2018-10-21 23:53:14'),(17,6,9,'2018-10-22 00:13:40'),(18,1,13,'2018-10-22 07:04:35'),(19,1,21,'2018-10-22 07:04:48'),(20,6,27,'2018-10-23 20:09:39'),(21,7,27,'2018-10-23 20:10:18');
/*!40000 ALTER TABLE `post_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `deleted` datetime DEFAULT NULL,
  `updated` datetime NOT NULL,
  `username` varchar(35) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(35) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(35) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bio` text COLLATE utf8mb4_unicode_ci,
  `last_seen` datetime DEFAULT NULL,
  `posts_per_page` int(11) NOT NULL,
  `location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `admin` tinyint(1) DEFAULT NULL,
  `notification_last_read_time` datetime DEFAULT NULL,
  `website_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `profile_photo` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,1,'2018-10-11 20:39:57',NULL,'2018-10-23 20:21:30','daniel','lindosemail@gmail.com','pbkdf2:sha256:50000$F57kqd9a$a0be01779c3489f5e7d367fb14d94d477cc34cffb3950b56e8ea9bbca3229255','Daniel','Lindegren','Day trader - Competitive shooter - Fitness enthusiast','2018-10-23 20:21:30',5,'Phoenix, Arizona',0,'2018-10-22 02:19:27','dlindegren.com','df90d116ddea086634669ba2a47d8165'),(2,1,'2018-10-11 20:39:57',NULL,'2018-10-22 02:21:27','sheree','sheree@testing.com','pbkdf2:sha256:50000$I0M2KdG7$7748324d93496ccaebfe7c6b94831be31ab3aea646d0a0075cc9c3d27a740a1c','Sheree','Score','','2018-10-22 02:21:27',10,'',0,NULL,'','2b039826ce0cebe9b055640baed6e742'),(3,1,'2018-10-11 20:39:57',NULL,'2018-10-23 20:13:09','mike','mike@testing.com','pbkdf2:sha256:50000$Icq13lIX$f4da0584ae6515528ec70f3ae12d9b772564ab58c2d7d0489f43b4e66169883f','Mike','Johnson','I like enjoy hiking and playing sports. I also like listening to good music!','2018-10-23 20:13:09',10,'Seattle, Washington',0,NULL,'','39551d653cf3d6a3aabb911dd51c366e'),(4,1,'2018-10-11 20:39:57',NULL,'2018-10-23 20:17:22','susan','susan@testing.com','pbkdf2:sha256:50000$zCpoWqSq$426b7b58b5ed693fdc4df62ce98a8686eb34ab4711d007ae6bf95f6c14354735','Susan','Roberts','','2018-10-23 20:17:22',10,'',0,NULL,'','ffb2bd8c8851672caa7958092073ab3c'),(5,0,'2018-10-11 20:39:57',NULL,'2018-10-22 02:27:17','jennifer','jennifer@testing.com','pbkdf2:sha256:50000$2CWDsNLr$e55696bd65a39c9d17e6484a624495cd7f5e769c36872207d5629cafb2272848','Jennifer','Michaels','','2018-10-22 02:27:17',10,'',0,NULL,'','830dcd16cbda93d5751ed82c7a6a69a7'),(6,1,'2018-10-11 20:39:57',NULL,'2018-10-23 20:18:59','tammy','tammy@testing.com','pbkdf2:sha256:50000$XgRckpIl$43474a92da0a3c18a0eaab0c3d633aeac54c1e6ea9ef68dea75f1d75c36803b1','Tammy','Fowler','Hey guys, my name is Tammy! I like long walks on the beach and listening to good music.','2018-10-23 20:18:59',10,'Phoenix, Arizona',0,'2018-10-23 20:13:48','tammyfowler.com','2f1267918d9d9f02b86fcdfe7d423ba0'),(7,1,'2018-10-11 20:39:57',NULL,'2018-10-23 20:10:36','jordan','jordan@testing.com','pbkdf2:sha256:50000$G8gYmTTp$49881a266c6a48fd062fe37a27fe2b84356f44aa5ce1d45f18cf297cdc77505e','Jordan','Smith','','2018-10-23 20:10:36',10,'',0,NULL,'','025ff6b744a61821ab88114af50fd4a2'),(8,1,'2018-10-11 20:39:57',NULL,'2018-10-22 02:22:46','sam','sam@testing.com','pbkdf2:sha256:50000$1ZitXMcD$de9c8053f3f7f8bded7436ed965a51d3545652eb18cc63d8d8d49391df437214','Sam','Jennings','','2018-10-22 02:22:46',10,'',0,NULL,'','01a325fb1745ec3c26025371eecfb59d');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-23 20:21:55
