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

2019-04-08 20:26:49,949 - INFO - Program started
2019-04-08 20:26:49,950 - INFO - Launcher started
2019-04-08 20:26:49,950 - INFO - Started load configuration
2019-04-08 20:26:49,950 - INFO - Start execution loading configs function
2019-04-08 20:26:49,950 - INFO - Start execution reading config file by path .\Resources\settings.ini
2019-04-08 20:26:49,950 - INFO - Data from file .\Resources\settings.ini loaded to configparser
2019-04-08 20:26:49,950 - INFO - Start writing data to configuration object
2019-04-08 20:26:49,960 - INFO - Writing data to configuration object  successfully finished
2019-04-08 20:26:49,960 - INFO - Start execution function of configuration logger
2019-04-08 20:26:49,960 - INFO - Execution function of configuration logger finished
2019-04-08 20:26:49,960 - INFO - Loading configuration finished
2019-04-08 20:26:49,961 - INFO - [OrderHistoryMaker] Execute preparing to execution
2019-04-08 20:26:49,961 - INFO - [OrderHistoryMaker] Start loading currency pairs from file .\Resources\CurrencyPairs.txt
2019-04-08 20:26:49,961 - INFO - [OrderHistoryMaker] Loading currency pairs from file .\Resources\CurrencyPairs.txt finished
2019-04-08 20:26:49,962 - INFO - [OrderHistoryMaker] Start loading tags from file .\Resources\Tags.txt
2019-04-08 20:26:49,962 - INFO - [OrderHistoryMaker] Loading tags from file .\Resources\Tags.txt finished
2019-04-08 20:26:49,962 - INFO - [OrderHistoryMaker] Started calculating of orders volumes to period with zones percentes: red = 15, green =60, blue =25
2019-04-08 20:26:49,965 - INFO - [OrderHistoryMaker] Calculating of orders volumes to period with zones percentes finished
2019-04-08 20:26:49,965 - INFO - [OrderHistoryMaker] Starting calculating orders volumes for generating 2000 orders
2019-04-08 20:26:49,966 - INFO - [OrderHistoryMaker] Calculating orders volumes for each period finished
2019-04-08 20:26:49,966 - INFO - [OrderHistoryMaker] Starting calculating start date of first period for generation orders
2019-04-08 20:26:49,966 - INFO - [OrderHistoryMaker] Calculating start date of first period for generation orders finished. Start at 2019-01-25 00:00:00
2019-04-08 20:26:49,969 - INFO - [OrderHistoryMaker] Started registration linear congruential generators configs 
2019-04-08 20:26:49,970 - INFO - [OrderHistoryMaker] Registration linear congruential generators configs finished
2019-04-08 20:26:50,188 - INFO - [OrderHistoryMaker] Execute preparing finished
2019-04-08 20:26:50,189 - INFO - [OrderHistoryMaker] Generating order history started
2019-04-08 20:26:50,189 - INFO - [RmqConsumer] Configuration consumer...
2019-04-08 20:26:50,189 - INFO - [OrderHistoryMaker] Started generation order history in green zone
2019-04-08 20:26:50,230 - INFO - [RmqConsumer] Consumer configurated
2019-04-08 20:26:50,231 - INFO - [RmqConsumer] Configuration database service...
2019-04-08 20:26:50,332 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:50,460 - INFO - [RmqConsumer] Database service configurated
2019-04-08 20:26:50,461 - INFO - [RmqConsumer] Start consuming
2019-04-08 20:26:50,591 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:50,591 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:50,693 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:50,694 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:50,718 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:50,809 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:50,810 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:50,951 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:50,951 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:51,067 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:51,068 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:51,157 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:51,179 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:51,180 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:51,303 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:51,303 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:51,398 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:51,399 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:51,530 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:51,606 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:51,607 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:51,783 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:51,784 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:51,920 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:51,921 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:51,934 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:52,056 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:52,057 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:52,248 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:52,249 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:52,342 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:52,355 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:52,355 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:52,499 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:52,500 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:52,624 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:52,624 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:52,691 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:52,789 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:52,789 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:52,909 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:52,910 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:53,028 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:53,029 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:53,103 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:53,153 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:53,154 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:53,262 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:53,262 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:53,377 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:53,377 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:53,476 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:53,584 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:53,585 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:53,740 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:53,740 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:53,829 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:53,932 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:53,933 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:54,081 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:54,082 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:54,221 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:54,221 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:54,230 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:54,379 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:54,379 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:54,491 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:54,492 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:54,609 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:54,609 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:54,618 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:54,733 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:54,734 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:54,874 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:54,874 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:54,989 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:54,989 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:55,017 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:55,143 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:55,143 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:55,283 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:55,406 - INFO - [OrderHistoryMaker] Generation green zone orders history finished
2019-04-08 20:26:55,406 - INFO - [OrderHistoryMaker] Started generation order history in blue-red zone
2019-04-08 20:26:55,473 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:55,618 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:55,618 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:55,762 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:55,763 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:55,908 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:55,909 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:55,917 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:56,017 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:56,018 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:56,107 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:56,108 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:56,199 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:56,200 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:56,286 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:56,287 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:56,378 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:56,379 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:56,471 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:56,471 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:56,559 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:56,560 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:56,586 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:56,648 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:56,648 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:56,762 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:56,762 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:56,856 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:56,856 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:56,957 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:56,958 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:57,049 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:57,049 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:57,135 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:57,136 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:57,189 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:57,222 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:57,222 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:57,342 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:57,343 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:57,438 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:57,439 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:57,547 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:57,616 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:57,616 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:57,734 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:57,734 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:57,829 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-08 20:26:57,933 - INFO - [RmqConsumer] Batch size data consumed
2019-04-08 20:26:57,934 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:58,032 - INFO - [OrderHistoryMaker] Generation blue-red zone orders history finished
2019-04-08 20:26:58,033 - INFO - [OrderHistoryMaker] Generating order history finished
2019-04-08 20:26:58,036 - INFO - [Launcher] Order history generation finished
2019-04-08 20:26:58,043 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-08 20:26:58,068 - INFO - [Utils] Getting statistic from db started
2019-04-08 20:26:58,104 - INFO - [Utils] Database service configurated
2019-04-08 20:26:58,104 - INFO - [Utils] Getting statistic from db finished

2019-04-08 20:26:58,104 - INFO - [ConsoleReporter] Start reporting

========== REPORT ==========
----- Generated orders -----
2000

----- Generated records -----
5693

----- Order history generation -----
Max: 227.39200000000002 ms
Min: 66.82100000000001 ms
Avg: 127.41045000000001 ms
Total: 2548.2090000000003 ms

----- Consumed messages -----
5693

----- Sending records batch to RabbitMQ -----
Max: 440.819 ms
Min: 118.682 ms
Avg: 264.09185 ms
Total: 5281.837 ms

----- Consuming data from RabbitMQ -----
Max: 186.504 ms
Min: 73.799 ms
Avg: 91.07735714285717 ms
Total: 5100.332000000001 ms

----- Send data to MySQL -----
Max: 353.056 ms
Min: 9.974 ms
Avg: 41.29417543859649 ms
Total: 2353.768 ms

----- Red zone avg order amount -----
29.2500

----- Green zone avg order amount -----
117.0000

----- Blue zone avg order amount -----
49.6667

----- Total orders in database -----
2000.0000

----- Total records in database -----
5693.0000

========== REPORT END ==========

2019-04-08 20:26:58,105 - INFO - [ConsoleReporter] Reporting finished

Press Enter to exit

2019-04-08 20:27:00,896 - INFO - [Launcher] Program finished
```


##### MySQL table content:

![](https://i.ibb.co/RhdDVx8/Screenshot-1.png)
