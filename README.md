# Orders History Generator
This application generates history of orders.

The history contains records about the status of each order. 

####Order format:
```
    ID - id of order
    Direction - order direction (can be either "Buy" or "Sell")
    Currency pair name - name of currency pair.
    InitPx - initial currency pair value (accepts a value with a deviation of +-5% (dy default settings) from the currency pair price)
    FillPx - filled currency pair value  (accepts values   with similar InitPx condition)
    InitVolume - initial volume 
    FillVolume - filled volume (may fully or partially correspond to the InitVolume value, also can be 0)
    Status - status of order (can be "New", "ToProvider", "Filled", "PartiallFilled", or "Rejected")
    StatusTimestamp - time of status changing in milliseconds
    Tags - order tags
    Desription - order descriptionn
```


All orders records divided distributed between 3 zones:
* `Red` - order started in previous periods of trading and finish in current period
* `Green` - order start and finish in same period 
* `Blue` - order start in current period and finish in next periods

Trading execute on period `Friday-Tuesday except weekends`

History is formed for several periods.


#### Pub / Sub
  
Generated orders history records publish to RabbitMQ to 3 queues (Red, Green and Blue).
This records consumed from RabbitMQ by subscriber in other thread and send it to MySQL database

## Install

```bash
$ git clone https://github.com/Artyom-Sysa/OrdersHistoryGenerator.git
```
## Before startup
For generation you must set configurations.
Configuration files must be in folder `Resources`

#### Currency pairs

Order generating uses list of currency pairs value.

You must fill this list in any file.
List must contains items in format `***/***;###`, where `***` - currency name, `###` - currency pair value in decimal format
All items with another format will be skip.



#### Tags

Order gsenerating uses list of tags.
You must fill this list in any file.
List item must be not empty line. All empty line will be skip. 

#### Logging

Default logging configuration exists in file `Resources/logging.conf`.
There you can set file and console logging levels.
If you delete this file it will be create in next application running with default settings


### Generation configurations

All files paths with settings must be write in file `Resources/setting.ini` in concrete fields
If this file removed - it will be created with default parameters

For configurate generation you can change all parameters. 
Basic parameters:
* `orders_amount` - total orders amount for generation
* `red_zone_orders_percent`, `green_zone_orders_percent`,  `blue_zone_orders_percent` - percentage of orders in each zone
* `batch_size` - size of data batch for sending to RabbitMQ and to MySQL
* `currency_deviation_percent` - deviation from currency pair values
* `currency_pairs_file_path`,`tags_file_path`, `logging_configurations_file_path` - paths to configuration files for generation and logging

Change default setting of RabbitMQ and MySQL settings to match your service configurations

All additional generated parameters except id of order in the application are generated using the [Linear congruential method](https://en.wikipedia.org/wiki/Linear_congruential_generator).

You can change any generation parameters, but considering that the maximum generated value will not exceed the value of the "modulus" parameter

## Startup

Two startup options are supported: native and using docker

------

### Native:

You must install some software for run generator:

##### Python:

Python must be installed on your computer.

Chech if python exists:

```bash
$ python --version
```
Install it if it not exists. Download it from official site: https://www.python.org/.
Or update it if yours python version less than 3.7. 

##### Pip

If `pip` don't install on you PC install by this instructions: 
* Windows: https://pip.pypa.io/en/stable/installing/
* Linux: https://www.tecmint.com/install-pip-in-linux/
* Mac OS: https://wsvincent.com/install-python3-mac/

##### RabbitMQ:

* download and install Erlang/OTP: https://www.erlang.org/downloads/
* download and install RabbitMQ: https://www.rabbitmq.com/download.html


These links contain installation instructions.

`Current version of 'Generator order history' has been writen with RMQ v3.7.13, Erlang/OTP v21.3`

##### MySQL:

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
  PRIMARY KEY (`status_id`,`order_id`),
  UNIQUE KEY `id_UNIQUE` (`pk_id`),
  KEY `fk_status_idx` (`status_id`),
  KEY `fk_direction_idx` (`direction_id`),
  CONSTRAINT `fk_direction` FOREIGN KEY (`direction_id`) REFERENCES `direction` (`direction_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`status_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```

Database name can be any, but do not forget to specify this name in configurations

#### Requirements
    
You install additional modules by running next command from application folder  

```bash
$ pip install -r ./requirements.txt 
```

If you system can't find `pip` run next command

```bash
$ python -m pip install -r ./requirements.txt 
```

Also you can install next the modules separately:
* pika==1.0.1
* protobuf==3.7.1
* mysql-connector==2.2.9


##### Running

Running in native mode stars by command:
```bash
$ python ./Launcher.py
```
------
### Docker

Install Docker and Docker Compose if they are missing: https://docs.docker.com/install/

Run MySQL and RabbitMQ services:

```bash
$ docker-compose up
```
Build Docker image:

```bash
$ docker build -t history .
```

Run container:
```bash
$ docker run --network=ordershistorygenerator_default history
```

## Execution example

```bash
$ docker run --network=ordershistorygenerator_default history

2019-04-22 16:34:38,821 - INFO - Program started
2019-04-22 16:34:38,821 - INFO - Launcher started
2019-04-22 16:34:38,821 - INFO - Started load configuration
2019-04-22 16:34:38,821 - INFO - Start execution loading configs function
2019-04-22 16:34:38,822 - INFO - Start execution reading config file by path ./Resources/settings.ini
2019-04-22 16:34:38,822 - INFO - Data from file ./Resources/settings.ini loaded to configparser
2019-04-22 16:34:38,822 - INFO - Start writing data to configuration object
2019-04-22 16:34:38,829 - INFO - Writing data to configuration object  successfully finished
2019-04-22 16:34:38,829 - INFO - Start execution function of configuration logger
2019-04-22 16:34:38,829 - INFO - Execution function of configuration logger finished
2019-04-22 16:34:38,829 - INFO - Loading configuration finished
2019-04-22 16:34:38,829 - INFO - [OrderHistoryMaker] Execute preparing to execution
2019-04-22 16:34:38,830 - INFO - [OrderHistoryMaker] Start loading currency pairs from file ./Resources/CurrencyPairs.txt
2019-04-22 16:34:38,830 - INFO - [OrderHistoryMaker] Loading currency pairs from file ./Resources/CurrencyPairs.txt finished
2019-04-22 16:34:38,830 - INFO - [OrderHistoryMaker] Start loading tags from file ./Resources/Tags.txt
2019-04-22 16:34:38,831 - INFO - [OrderHistoryMaker] Loading tags from file ./Resources/Tags.txt finished
2019-04-22 16:34:38,831 - INFO - [OrderHistoryMaker] Started registration linear congruential generators configs 
2019-04-22 16:34:38,831 - INFO - [OrderHistoryMaker] Registration linear congruential generators configs finished
2019-04-22 16:34:38,831 - INFO - [OrderHistoryMaker] Started calculating of orders volumes to period with zones percentes: red = 15, green =60, blue =25
2019-04-22 16:34:38,831 - INFO - [OrderHistoryMaker] Starting calculating orders volumes for generating 2000 orders
2019-04-22 16:34:38,832 - INFO - [OrderHistoryMaker] Calculating orders volumes for each period finished
2019-04-22 16:34:38,832 - INFO - [OrderHistoryMaker] Starting calculating start date of first period for generation orders
2019-04-22 16:34:38,832 - INFO - [OrderHistoryMaker] Calculating start date of first period for generation orders finished. Start at 2018-12-14 00:00:00
2019-04-22 16:34:39,165 - INFO - [OrderHistoryMaker] Execute preparing finished
2019-04-22 16:34:39,166 - INFO - [OrderHistoryMaker] Generating order history started
2019-04-22 16:34:39,168 - INFO - [RmqConsumer] Configuration consumer...
2019-04-22 16:34:39,168 - INFO - [OrderHistoryMaker] Started generation order history in green zone
2019-04-22 16:34:39,223 - INFO - [RmqConsumer] Consumer configurated
2019-04-22 16:34:39,225 - INFO - [RmqConsumer] Configuration database service...
2019-04-22 16:34:39,284 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:39,413 - INFO - [RmqConsumer] Database service configurated
2019-04-22 16:34:39,413 - INFO - [RmqConsumer] Start consuming
2019-04-22 16:34:39,520 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:39,520 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:39,560 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:39,787 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:39,787 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:39,848 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:40,016 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:40,016 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:40,320 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:40,320 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:40,423 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:40,423 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:40,423 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:40,563 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:40,563 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:40,651 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:40,789 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:40,790 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:40,957 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:40,960 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:41,061 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:41,172 - INFO - [Launcher] Start reporting
Start getting reporting data at 2019-04-22 16:34:41.172344
2019-04-22 16:34:41,172 - INFO - [Utils] Getting statistic from db started
2019-04-22 16:34:41,208 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:41,365 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:41,365 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:41,569 - INFO - [Utils] Database service configurated
2019-04-22 16:34:41,570 - INFO - [Utils] Getting statistic from db finished

2019-04-22 16:34:41,574 - INFO - [ConsoleReporter] Start reporting

========== REPORT ==========
----- Generated orders -----
741

----- Generated records -----
1850

----- Order history generation -----
Max: 186.54000000000002 ms
Min: 44.339000000000006 ms
Avg: 117.08357142857143 ms
Total: 819.585 ms

----- Sending records batch to RabbitMQ -----
Max: 473.028 ms
Min: 101.22399999999999 ms
Avg: 204.51628571428571 ms
Total: 1431.614 ms

----- Consumed messages -----
972

----- Consuming data from RabbitMQ -----
Max: 168.969 ms
Min: 60.42 ms
Avg: 114.54288888888888 ms
Total: 1030.886 ms

----- Send data to MySQL -----
Max: 259.538 ms
Min: 41.383 ms
Avg: 109.07133333333334 ms
Total: 981.642 ms

----- Red zone orders avg amount -----
19.0000

----- Green zone orders avg amount -----
56.6667

----- Blue zone orders avg amount -----
17.0000

----- Total orders in database -----
278.0000

----- Total records in database -----
700.0000

========== REPORT END ==========

2019-04-22 16:34:41,576 - INFO - [ConsoleReporter] Reporting finished

Reporter finished data at 2019-04-22 16:34:41.578945
2019-04-22 16:34:41,578 - INFO - [Launcher] Reporting finished
2019-04-22 16:34:41,614 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:41,615 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:41,699 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:41,796 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:41,796 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:42,117 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:42,118 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:42,149 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:42,381 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:42,381 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:42,531 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:42,630 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:42,630 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:42,863 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:42,864 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:43,087 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:43,088 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:43,116 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:43,371 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:43,372 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:43,419 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:43,567 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:43,567 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:43,586 - INFO - [Launcher] Start reporting
Start getting reporting data at 2019-04-22 16:34:43.587408
2019-04-22 16:34:43,588 - INFO - [Utils] Getting statistic from db started
2019-04-22 16:34:43,778 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:43,779 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:43,894 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:44,186 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:44,188 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:44,303 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:44,400 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:44,401 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:44,546 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:44,547 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:44,577 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:44,857 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:44,859 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:44,930 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:45,207 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:45,207 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:45,388 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:45,389 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:45,418 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:45,669 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:45,832 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:46,213 - INFO - [Utils] Database service configurated
2019-04-22 16:34:46,215 - INFO - [Utils] Getting statistic from db finished

2019-04-22 16:34:46,219 - INFO - [ConsoleReporter] Start reporting

========== REPORT ==========
----- Generated orders -----
1983

----- Generated records -----
4956

----- Order history generation -----
Max: 276.738 ms
Min: 37.932 ms
Avg: 121.26831578947366 ms
Total: 2304.0979999999995 ms

----- Sending records batch to RabbitMQ -----
Max: 473.028 ms
Min: 101.22399999999999 ms
Avg: 239.6301578947369 ms
Total: 4552.973000000001 ms

----- Consumed messages -----
2538

----- Consuming data from RabbitMQ -----
Max: 177.99200000000002 ms
Min: 60.42 ms
Avg: 127.36339999999998 ms
Total: 3184.0849999999996 ms

----- Send data to MySQL -----
Max: 682.04 ms
Min: 41.383 ms
Avg: 137.31624 ms
Total: 3432.9059999999995 ms

----- Red zone orders avg amount -----
17.0000

----- Green zone orders avg amount -----
68.0000

----- Blue zone orders avg amount -----
28.3333

----- Total orders in database -----
680.0000

----- Total records in database -----
1700.0000

========== REPORT END ==========

2019-04-22 16:34:46,221 - INFO - [ConsoleReporter] Reporting finished

Reporter finished data at 2019-04-22 16:34:46.224583
2019-04-22 16:34:46,224 - INFO - [Launcher] Reporting finished
2019-04-22 16:34:46,305 - INFO - [OrderHistoryMaker] Sending ordres batch information to RabbitMQ
2019-04-22 16:34:46,320 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:46,320 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:46,556 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:46,556 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:46,651 - INFO - [OrderHistoryMaker] Generating order history finished
2019-04-22 16:34:46,658 - INFO - [Launcher] Order history generation finished
2019-04-22 16:34:46,699 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:46,699 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:46,895 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:46,895 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:47,026 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:47,026 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:47,169 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:47,170 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:47,378 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:47,378 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:47,515 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:47,515 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:47,665 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:47,665 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:47,791 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:47,792 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:47,944 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:47,944 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:48,021 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:48,022 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:48,179 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:48,179 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:48,227 - INFO - [Launcher] Start reporting
Start getting reporting data at 2019-04-22 16:34:48.228592
2019-04-22 16:34:48,228 - INFO - [Utils] Getting statistic from db started
2019-04-22 16:34:48,328 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:48,328 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:48,478 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:48,479 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:48,589 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:48,590 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:48,698 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:48,698 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:49,056 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:49,057 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:49,326 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:49,326 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:49,416 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:49,416 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:49,491 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:49,491 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:49,575 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:49,576 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:49,664 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:49,664 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:49,873 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:49,873 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:49,993 - INFO - [RmqConsumer] Batch size data consumed
2019-04-22 16:34:49,993 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:50,058 - INFO - [RmqConsumer] Sending readed batch records to MySQL
2019-04-22 16:34:52,646 - INFO - [Utils] Database service configurated
2019-04-22 16:34:52,647 - INFO - [Utils] Getting statistic from db finished

2019-04-22 16:34:52,647 - INFO - [ConsoleReporter] Start reporting

========== REPORT ==========
----- Generated orders -----
2000

----- Generated records -----
5000

----- Order history generation -----
Max: 276.738 ms
Min: 37.932 ms
Avg: 128.76385 ms
Total: 2575.2769999999996 ms

----- Sending records batch to RabbitMQ -----
Max: 473.028 ms
Min: 101.22399999999999 ms
Avg: 244.84605000000005 ms
Total: 4896.921000000001 ms

----- Consumed messages -----
5000

----- Consuming data from RabbitMQ -----
Max: 247.282 ms
Min: 35.568000000000005 ms
Avg: 112.33843999999999 ms
Total: 5616.922 ms

----- Send data to MySQL -----
Max: 682.04 ms
Min: 3.019 ms
Avg: 97.49150980392157 ms
Total: 4972.067 ms

----- Red zone orders avg amount -----
17.5714

----- Green zone orders avg amount -----
64.5714

----- Blue zone orders avg amount -----
26.8571

----- Total orders in database -----
1526.0000

----- Total records in database -----
3800.0000

========== REPORT END ==========

2019-04-22 16:34:52,647 - INFO - [ConsoleReporter] Reporting finished

Reporter finished data at 2019-04-22 16:34:52.647867
2019-04-22 16:34:52,647 - INFO - [Launcher] Reporting finished
2019-04-22 16:34:52,648 - INFO - [Launcher] Start reporting
Start getting reporting data at 2019-04-22 16:34:52.648113
2019-04-22 16:34:52,648 - INFO - [Utils] Getting statistic from db started
2019-04-22 16:34:55,477 - INFO - [Utils] Database service configurated
2019-04-22 16:34:55,477 - INFO - [Utils] Getting statistic from db finished

2019-04-22 16:34:55,477 - INFO - [ConsoleReporter] Start reporting

========== REPORT ==========
----- Generated orders -----
2000

----- Generated records -----
5000

----- Order history generation -----
Max: 276.738 ms
Min: 37.932 ms
Avg: 128.76385 ms
Total: 2575.2769999999996 ms

----- Sending records batch to RabbitMQ -----
Max: 473.028 ms
Min: 101.22399999999999 ms
Avg: 244.84605000000005 ms
Total: 4896.921000000001 ms

----- Consumed messages -----
5000

----- Consuming data from RabbitMQ -----
Max: 247.282 ms
Min: 35.568000000000005 ms
Avg: 112.33843999999999 ms
Total: 5616.922 ms

----- Send data to MySQL -----
Max: 682.04 ms
Min: 3.019 ms
Avg: 97.49150980392157 ms
Total: 4972.067 ms

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

2019-04-22 16:34:55,478 - INFO - [ConsoleReporter] Reporting finished

Reporter finished data at 2019-04-22 16:34:55.478318
2019-04-22 16:34:55,478 - INFO - [Launcher] Reporting finished
2019-04-22 16:34:55,478 - INFO - [Launcher] Program finished

```


##### MySQL table content:

![](https://i.ibb.co/B6wc7Dk/Screenshot-3.png)