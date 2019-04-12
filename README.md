# Orders History Generator
Generator of orders history

Overview
--
Order format:
```
    ID - id of order
    Direction - order direction
    Currency pair name - name of currency pair
    InitPx - initial currency pair value
    FillPx - filled currency pair value
    InitVolume - initial volume
    InitVolume - filled volume
    Status - status of order
    StatusTimestamp - time of status changing in milliseconds
    Tags - order tags
    Desription - order descriptionn
```

All orders records divided distributed between 3 zones:
* `Red`: Order started in previous periods of trading and finish in current period
* `Green`: Order start and finish in same period 
* `Blue`: Order start in current period and finish in next periods

Trading execute on period `Friday-Tuesday except weekends`

## Pub / Sub
  
Generated orders history records publish to RabbitMQ to 3 queues (Red, Green and Blue).
This records consumed from RabbitMQ by subscriber in other thread and send it to MySQL database

## Install

```bash
$ git clone https://github.com/Artyom-Sysa/OrdersHistoryGenerator.git
```
#### Python:
Chech if `python` exists:
```bash
$ python --version
```
If it not exists install it. Download it from official site: https://www.python.org/.
Or update it if yours python version less than 3.7. 

#### Pip
If `pip` don't install on you PC install by this instructions: 
* Windows:https://pip.pypa.io/en/stable/installing/
* Other OS: https://www.tecmint.com/install-pip-in-linux/

Install additional modules
```bash
$ pip install -r ./requirements.txt 
```

#### RabbitMQ:
* donwload and install Erlang/OTP: https://www.erlang.org/downloads/
* download and install RabbitMQ: https://www.rabbitmq.com/download.html

`Current version of 'Generator order history' has been writen with RMQ v3.7.13, Erlang/OTP v21.3`

#### MySQL:

  * download and install MySQL server: https://dev.mysql.com/downloads/mysql/
  * create schema with next SQL-script:

```sql
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
  PRIMARY KEY (`pk_id`,`order_id`),
  UNIQUE KEY `id_UNIQUE` (`pk_id`),
  KEY `fk_status_idx` (`status_id`),
  KEY `fk_direction_idx` (`direction_id`),
  CONSTRAINT `fk_direction` FOREIGN KEY (`direction_id`) REFERENCES `direction` (`direction_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`status_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```

Database name can be any, but do not forget to specify this name in configurations.

---
# Configurate 

Configurate generation settings before executing:

Required settings:

```
# Default settings
# Change parameters to your system confgurations

[GENERAL]
orders_amount = 2000
orders_in_first_blue_zone = 3
red_zone_orders_percent = 15
green_zone_orders_percent = 60
blue_zone_orders_percent = 25
batch_size = 100
currency_deviation_percent = 5
order_history_write_file_path = .\Resources\Result.csv
currency_pairs_file_path = .\Resources\CurrencyPairs.txt
tags_file_path = .\Resources\Tags.txt
default_setting_file_path = .\Resources\settings.ini

[LOGGER]
logging_configurations_file_path = .\Resources\logging.conf

[MYSQL]
mysql_host = 127.0.0.1
mysql_port = 3306
mysql_user = root
mysql_password = 
mysql_db_name = OrdersHistory

[RABBITMQ]
rabbitmq_host = 127.0.0.1
rabbitmq_port = 5672
rabbitmq_virtual_host = /
rabbitmq_user = guest
rabbitmq_password = guest
rabbitmq_exchange_name = orders_records
rabbitmq_exchange_type = topic
rabbitmq_red_records_routing_key = r.order.red-zone.order-history-generator
rabbitmq_blue_records_routing_key = r.order.blue-zone.order-history-generator
rabbitmq_gree_records_routing_key = r.order.green-zone.order-history-generator

```

If you want you can change other parameters in your settins.ini file



## Run

```bash
$ python ./Launcher.py
```
You can call generating report during program execution by pressing `Enter` key

## Execution example
##### Starting history generation

```bash
$ python ./Launcher.py

2019-04-12 18:23:40,120 - INFO - Program started
2019-04-12 18:23:40,120 - INFO - Launcher started
2019-04-12 18:23:40,120 - INFO - Started load configuration
2019-04-12 18:23:40,120 - INFO - Start execution loading configs function
2019-04-12 18:23:40,121 - INFO - Start execution reading config file by path .\Resources\settings.ini
2019-04-12 18:23:40,121 - INFO - Data from file .\Resources\settings.ini loaded to configparser
2019-04-12 18:23:40,121 - INFO - Start writing data to configuration object
2019-04-12 18:23:40,129 - INFO - Writing data to configuration object  successfully finished
2019-04-12 18:23:40,129 - INFO - Start execution function of configuration logger
2019-04-12 18:23:40,129 - INFO - Execution function of configuration logger finished
2019-04-12 18:23:40,129 - INFO - Loading configuration finished
2019-04-12 18:23:40,130 - INFO - [OrderHistoryMaker] Execute preparing to execution
2019-04-12 18:23:40,130 - INFO - [OrderHistoryMaker] Start loading currency pairs from file .\Resources\CurrencyPairs.txt
2019-04-12 18:23:40,131 - INFO - [OrderHistoryMaker] Loading currency pairs from file .\Resources\CurrencyPairs.txt finished
2019-04-12 18:23:40,131 - INFO - [OrderHistoryMaker] Start loading tags from file .\Resources\Tags.txt
2019-04-12 18:23:40,132 - INFO - [OrderHistoryMaker] Loading tags from file .\Resources\Tags.txt finished
2019-04-12 18:23:40,132 - INFO - [OrderHistoryMaker] Started registration linear congruential generators configs 
2019-04-12 18:23:40,133 - INFO - [OrderHistoryMaker] Registration linear congruential generators configs finished
2019-04-12 18:23:40,133 - INFO - [OrderHistoryMaker] Started calculating of orders volumes to period with zones percentes: red = 15, green =60, blue =25
2019-04-12 18:23:40,133 - INFO - [OrderHistoryMaker] Starting calculating orders volumes for generating 2000 orders
2019-04-12 18:23:40,133 - INFO - [OrderHistoryMaker] Calculating orders volumes for each period finished
2019-04-12 18:23:40,133 - INFO - [OrderHistoryMaker] Starting calculating start date of first period for generation orders
2019-04-12 18:23:40,134 - INFO - [OrderHistoryMaker] Calculating start date of first period for generation orders finished. Start at 2018-12-07 00:00:00
2019-04-12 18:23:40,294 - INFO - [OrderHistoryMaker] Execute preparing finished
2019-04-12 18:23:40,294 - INFO - [OrderHistoryMaker] Generating order history started
2019-04-12 18:23:40,295 - INFO - [OrderHistoryMaker] Started generation order history in green zone
2019-04-12 18:23:40,295 - INFO - [RmqConsumer] Configuration consumer...
2019-04-12 18:23:40,332 - INFO - [RmqConsumer] Consumer configurated
2019-04-12 18:23:40,332 - INFO - [RmqConsumer] Configuration database service...
2019-04-12 18:23:40,374 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:40,547 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:40,650 - INFO - [RmqConsumer] Database service configurated
2019-04-12 18:23:40,650 - INFO - [RmqConsumer] Start consuming
2019-04-12 18:23:40,760 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:40,761 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:40,867 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:40,868 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:40,877 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:41,015 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:41,015 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:41,141 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:41,141 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:41,223 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:41,223 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:41,294 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:41,355 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:41,355 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:41,500 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:41,501 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:41,652 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:41,653 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:41,670 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:41,868 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:41,869 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:41,956 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:42,052 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:42,053 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:42,201 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:42,438 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:42,438 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:42,455 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:42,590 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:42,590 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:42,702 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:42,703 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:42,848 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:42,848 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:42,863 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:43,027 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:43,027 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:43,153 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:43,174 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:43,174 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:43,276 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:43,276 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:43,403 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:43,404 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:43,491 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:43,765 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:43,772 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:43,781 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:43,910 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:43,911 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:44,046 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:44,046 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:44,098 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:44,207 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:44,207 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:44,417 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:44,424 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:44,425 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:44,589 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:44,589 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:44,662 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:44,825 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:44,826 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:44,921 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:44,973 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:44,973 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:45,159 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:45,160 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:45,274 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:45,274 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:45,291 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:45,411 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:45,411 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:45,567 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:45,594 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:45,594 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:45,791 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:45,792 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:45,841 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:46,009 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:46,010 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:46,081 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-12 18:23:46,232 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:46,233 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:46,257 - INFO - [OrderHistoryMaker] Generating order history finished
2019-04-12 18:23:46,258 - INFO - [Launcher] Order history generation finished
2019-04-12 18:23:46,571 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:46,571 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:46,626 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:46,626 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:46,746 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:46,746 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:46,849 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:46,849 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:47,035 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:47,035 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:47,362 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:47,362 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:47,412 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:47,413 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:47,458 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:47,458 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:47,495 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:47,496 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:47,537 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:47,537 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:47,583 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:47,583 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:47,632 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:47,632 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:47,685 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:47,685 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:47,837 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:47,837 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:47,902 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:47,902 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:47,949 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:47,949 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:48,000 - INFO - [RmqConsumer] Batch size data consumed
2019-04-12 18:23:48,001 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-12 18:23:48,017 - INFO - [Utils] Getting statistic from db started
2019-04-12 18:23:51,074 - INFO - [Utils] Database service configurated
2019-04-12 18:23:51,074 - INFO - [Utils] Getting statistic from db finished

2019-04-12 18:23:51,074 - INFO - [ConsoleReporter] Start reporting

========== REPORT ==========
----- Generated orders -----
2000

----- Generated records -----
5000

----- Order history generation -----
Max: 166.555 ms
Min: 50.861999999999995 ms
Avg: 94.65139999999998 ms
Total: 1893.0279999999996 ms

----- Sending records batch to RabbitMQ -----
Max: 345.076 ms
Min: 113.697 ms
Avg: 203.20190000000002 ms
Total: 4064.0380000000005 ms

----- Consumed messages -----
5000

----- Consuming data from RabbitMQ -----
Max: 143.617 ms
Min: 26.927 ms
Avg: 80.46260000000001 ms
Total: 4023.1300000000006 ms

----- Send data to MySQL -----
Max: 288.883 ms
Min: 7.978000000000001 ms
Avg: 65.81522 ms
Total: 3290.761 ms

----- Red zone orders avg amount -----
16.6667

----- Green zone orders avg amount -----
66.6667

----- Blue zone orders avg amount -----
27.7778

----- Total orders in database -----
2000.0000

----- Total records in database -----
5000.0000

========== REPORT END ==========

2019-04-12 18:23:51,075 - INFO - [ConsoleReporter] Reporting finished

Press Enter to exit


2019-04-12 18:23:54,207 - INFO - [Launcher] Program finished
```


##### MySQL table content:

![](https://i.ibb.co/B6wc7Dk/Screenshot-3.png)
