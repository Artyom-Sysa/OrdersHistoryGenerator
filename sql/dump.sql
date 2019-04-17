CREATE DATABASE  IF NOT EXISTS `orders_history`;

USE `orders_history`;

DROP TABLE IF EXISTS `status`;

CREATE TABLE `status` (
  `status_id` int(11) NOT NULL AUTO_INCREMENT,
  `status_name` varchar(15) NOT NULL,
  PRIMARY KEY (`status_id`),
  UNIQUE KEY `status_name_UNIQUE` (`status_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

LOCK TABLES `status` WRITE;
INSERT INTO `status` VALUES (1,'New'),(2,'ToProvider'),(3,'Filled'),(4,'PartialFilled'),(5,'Rejected');
UNLOCK TABLES;


DROP TABLE IF EXISTS `direction`;

CREATE TABLE `direction` (
  `direction_id` int(11) NOT NULL AUTO_INCREMENT,
  `direction_name` varchar(10) NOT NULL,
  PRIMARY KEY (`direction_id`),
  UNIQUE KEY `direction_name_UNIQUE` (`direction_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

LOCK TABLES `direction` WRITE;
INSERT INTO `direction` VALUES (1,'Buy'),(2,'Sell');
UNLOCK TABLES;

DROP TABLE IF EXISTS `history`;

CREATE TABLE `history` (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) NOT NULL,
  `direction_id` int(11) NOT NULL,
  `currency_pair` varchar(10) NOT NULL,
  `init_px` decimal(10,5) NOT NULL,
  `fill_px` decimal(10,5) NOT NULL,
  `init_vol` decimal(20,8) NOT NULL,
  `fill_vol` decimal(20,8) NOT NULL,
  `status_id` int(11) NOT NULL,
  `datetime` bigint(20) NOT NULL,
  `tags` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`status_id`,`order_id`),
  UNIQUE KEY `id_UNIQUE` (`pk_id`),
  KEY `fk_status_idx` (`status_id`),
  KEY `fk_direction_idx` (`direction_id`),
  CONSTRAINT `fk_direction` FOREIGN KEY (`direction_id`) REFERENCES `direction` (`direction_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`status_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
