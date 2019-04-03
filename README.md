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

##### Pip
If `pip` don't install on you PC install by this instructions: 
* Windows:https://pip.pypa.io/en/stable/installing/
* Other OS: https://www.tecmint.com/install-pip-in-linux/

Install additional modules
```bash
$ pip install -r /path/to/project/folder/requirements.txt 
```

#### MySQL:

MySQL database schema creating script:

Database name can be any, but do not forget to specify this name in configurations.

```sql
CREATE DATABASE IF NOT EXISTS `OrdersHistory`

USE `OrdersHistory`;

DROP TABLE IF EXISTS `History`;

CREATE TABLE `History` (
  `pk_id` int NOT NULL AUTO_INCREMENT,
  `record_id` bigint NOT NULL,
  `direction` varchar(4) NOT NULL,
  `currency_pair` varchar(10) NOT NULL,
  `init_px` decimal(10,5) NOT NULL,
  `fill_px` decimal(10,5) NOT NULL,
  `init_vol` int NOT NULL,
  `fill_vol` int NOT NULL,
  `status` varchar(12) NOT NULL,
  `datetime` bigint NOT NULL,
  `tags` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `zone` varchar(5) NOT NULL,
  PRIMARY KEY (`pk_id`),
  UNIQUE KEY `id_UNIQUE` (`pk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5694 DEFAULT CHARSET=utf8;


```

#### RabbitMQ
Install RabbitMQ from https://www.rabbitmq.com/download.html

`Current 'Generator order history' has been writen with RMQ v3.7.13`

---
# Configurate 

Configurate generation settings before executing:

Required settings:

```
# Default settings
# Change parameters to your system confgurations
#

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

## Execution example
##### Starting history generation

```bash
$ python ./Launcher.py

2019-04-03 15:55:13,079 - INFO - Program started
2019-04-03 15:55:13,080 - INFO - Launcher started
2019-04-03 15:55:13,081 - INFO - Started load configuration
2019-04-03 15:55:13,081 - INFO - Start execution loading configs function
2019-04-03 15:55:13,082 - INFO - Start execution reading config file by path .\Resources\settings.ini
2019-04-03 15:55:13,083 - INFO - Data from file .\Resources\settings.ini loaded to configparser
2019-04-03 15:55:13,084 - INFO - Start writing data to configuration object
2019-04-03 15:55:13,152 - INFO - Writing data to configuration object  successfully finished
2019-04-03 15:55:13,152 - INFO - Start execution function of configuration logger
2019-04-03 15:55:13,153 - INFO - Execution function of configuration logger finished
2019-04-03 15:55:13,153 - INFO - Loading configuration finished
2019-04-03 15:55:13,153 - INFO - [OrderHistoryMaker] Execute preparing to execution
2019-04-03 15:55:13,153 - INFO - [OrderHistoryMaker] Start loading currency pairs from file .\Resources\CurrencyPairs.txt
2019-04-03 15:55:13,154 - INFO - [OrderHistoryMaker] Loading currency pairs from file .\Resources\CurrencyPairs.txt finished
2019-04-03 15:55:13,155 - INFO - [OrderHistoryMaker] Start loading tags from file .\Resources\Tags.txt
2019-04-03 15:55:13,156 - INFO - [OrderHistoryMaker] Loading tags from file .\Resources\Tags.txt finished
2019-04-03 15:55:13,156 - INFO - [OrderHistoryMaker] Started calculating of orders volumes to period with zones percentes: red = 15, green =60, blue =25
2019-04-03 15:55:13,162 - INFO - [OrderHistoryMaker] Calculating of orders volumes to period with zones percentes finished
2019-04-03 15:55:13,163 - INFO - [OrderHistoryMaker] Starting calculating orders volumes for generating 2000 orders
2019-04-03 15:55:13,164 - INFO - [OrderHistoryMaker] Calculating orders volumes for each period finished
2019-04-03 15:55:13,164 - INFO - [OrderHistoryMaker] Starting calculating start date of first period for generation orders
2019-04-03 15:55:13,165 - INFO - [OrderHistoryMaker] Calculating start date of first period for generation orders finished. Start at 2019-01-18 00:00:00
2019-04-03 15:55:13,168 - INFO - [OrderHistoryMaker] Started registration linear congruential generators configs
2019-04-03 15:55:13,169 - INFO - [OrderHistoryMaker] Registration linear congruential generators configs finished
2019-04-03 15:55:13,169 - INFO - [OrderHistoryMaker] Execute preparing finished
2019-04-03 15:55:13,170 - INFO - [OrderHistoryMaker] Generating order history started
2019-04-03 15:55:13,170 - INFO - [OrderHistoryMaker] Started generation order history in green zone
2019-04-03 15:55:14,192 - INFO - [OrderHistoryMaker] Generation green zone orders history finished
2019-04-03 15:55:14,193 - INFO - [OrderHistoryMaker] Started generation order history in blue-red zone
2019-04-03 15:55:14,603 - INFO - [OrderHistoryMaker] Generation blue-red zone orders history finished
2019-04-03 15:55:14,604 - INFO - [OrderHistoryMaker] Generating order history finished
2019-04-03 15:55:14,604 - INFO - [OrderHistoryMaker] Start writing orders records history to file
2019-04-03 15:55:14,606 - INFO - [OrderHistoryMaker] Writing next list with records history to file started
2019-04-03 15:55:14,986 - INFO - [OrderHistoryMaker] Writing next list with records history to file started
2019-04-03 15:55:15,017 - INFO - [OrderHistoryMaker] Writing next list with records history to file started
2019-04-03 15:55:15,090 - INFO - [OrderHistoryMaker] Writing orders records history to file finished
2019-04-03 15:55:15,091 - INFO - [OrderHistoryMaker] Started reading records history from file
2019-04-03 15:55:15,134 - INFO - [OrderHistoryMaker] Reading records history from file finished
2019-04-03 15:55:15,135 - INFO - [OrderHistoryMaker] Sending records to RabbitMQ started
2019-04-03 15:55:15,476 - INFO - [OrderHistoryMaker] Sending next list with records to RabbitMQ
2019-04-03 15:55:15,813 - INFO - [OrderHistoryMaker] Sending next list with records to RabbitMQ
2019-04-03 15:55:16,820 - INFO - [OrderHistoryMaker] Sending next list with records to RabbitMQ
2019-04-03 15:55:20,727 - INFO - [OrderHistoryMaker] Sending records to RabbitMQ finished
2019-04-03 15:55:20,728 - INFO - [OrderHistoryMaker] Start sending records to MySQL
2019-04-03 15:55:20,917 - INFO - [OrderHistoryMaker] Sending next list wit records to MySQL
2019-04-03 15:55:21,152 - INFO - [OrderHistoryMaker] Sending next list wit records to MySQL
2019-04-03 15:55:21,536 - INFO - [OrderHistoryMaker] Sending next list wit records to MySQL
2019-04-03 15:55:23,303 - INFO - [OrderHistoryMaker] Sending records to MySQL finished
2019-04-03 15:55:23,304 - INFO - [ConsoleReporter] Start reporting

========== REPORT ==========
Order history generation
Max: 94.749 ms
Min: 65.82499999999999 ms
Avg: 71.41035000000002 ms
Tota: 1428.2070000000003 ms
---------------

Green records writing to file
Max: 37.873 ms
Min: 2.018 ms
Avg: 8.806697674418604 ms
Tota: 378.688 ms
---------------

Red records writing to file
Max: 7.003 ms
Min: 5.957 ms
Avg: 6.1824 ms
Tota: 30.912000000000003 ms
---------------

Blue records writing to file
Max: 7.978000000000001 ms
Min: 4.984 ms
Avg: 6.218 ms
Tota: 68.398 ms
---------------

Read and sort records by zones: 42.884 ms
---------------

Send RabbitMQ red zone records
Max: 85.77 ms
Min: 30.918999999999997 ms
Avg: 67.02079999999998 ms
Tota: 335.1039999999999 ms
---------------

Send RabbitMQ blue zone records
Max: 111.69999999999999 ms
Min: 37.898 ms
Avg: 91.48254545454544 ms
Tota: 1006.3079999999999 ms
---------------

Send RabbitMQ green zone records
Max: 149.601 ms
Min: 9.972999999999999 ms
Avg: 90.87327906976743 ms
Tota: 3907.551 ms
---------------

Send red zones records to MySql
Max: 80.232 ms
Min: 20.943 ms
Avg: 46.6438 ms
Tota: 233.219 ms
---------------

Send blue zones records to MySql
Max: 59.164 ms
Min: 14.958 ms
Avg: 34.75863636363636 ms
Tota: 382.345 ms
---------------

Send green zones records to MySql
Max: 455.16 ms
Min: 1.9949999999999999 ms
Avg: 41.07883720930232 ms
Tota: 1766.3899999999999 ms
---------------

========== REPORT END ==========
2019-04-03 15:55:23,337 - INFO - [ConsoleReporter] Reporting finished
2019-04-03 15:55:23,337 - INFO - [Launcher] Order history generation finished
2019-04-03 15:55:23,341 - INFO - [Launcher] Program finished
```

##### Result file content:
```bash
27131965806,Buy,EUR/MKD,58.823287,2263,0,0,1548790081879,New,"Car, Bussiness, Trip","Order for: Car, Bussiness, Trip",Green
27131965806,Buy,EUR/MKD,58.823287,2263,0,0,1548794640939,ToProvider,"Car, Bussiness, Trip","Order for: Car, Bussiness, Trip",Green
27131965806,Buy,EUR/MKD,58.823287,2263,61.636094,2263,1548796920469,Filled,"Car, Bussiness, Trip","Order for: Car, Bussiness, Trip",Green
24517804434850,Buy,EUR/USD,1.180976958,896,0,0,1548776868368,New,"PS, Games","Order for: PS, Games",Green
24517804434850,Buy,EUR/USD,1.180976958,896,0,0,1548788034183,ToProvider,"PS, Games","Order for: PS, Games",Green
24517804434850,Buy,EUR/USD,1.180976958,896,1.154031074,896,1548789812128,Filled,"PS, Games","Order for: PS, Games",Green
38360167762086,Buy,USD/MKD,53.238288000000004,2733,0,0,1548748866038,New,"Bitcoin, Study, XBOX","Order for: Bitcoin, Study, XBOX",Green
38360167762086,Buy,USD/MKD,53.238288000000004,2733,0,0,1548752239809,ToProvider,"Bitcoin, Study, XBOX","Order for: Bitcoin, Study, XBOX",Green
38360167762086,Buy,USD/MKD,53.238288000000004,2733,0,0,1548755636781,Rejected,"Bitcoin, Study, XBOX","Order for: Bitcoin, Study, XBOX",Green
32667397771369,Buy,USD/UAH,28.3670937,2726,0,0,1548446479959,New,"Car, Phone","Order for: Car, Phone",Green

...

8106763523504,Buy,CHF/GIP,0.78212256,253,0,0,1548771166113,New,"Study, Music, XBOX","Order for: Study, Music, XBOX",Blue
8106763523504,Buy,CHF/GIP,0.78212256,253,0,0,1548785183056,ToProvider,"Study, Music, XBOX","Order for: Study, Music, XBOX",Blue
38883681097952,Buy,CHF/JPY,109.1501918,2006,0,0,1548781991020,New,"Car, Bussiness, Phone","Order for: Car, Bussiness, Phone",Blue
24158604709557,Buy,GBP/NZD,1.961713418,1523,0,0,1548781149015,New,"Bitbon, PC","Order for: Bitbon, PC",Blue
24158604709557,Buy,GBP/NZD,1.961713418,1523,0,0,1548790174507,ToProvider,"Bitbon, PC","Order for: Bitbon, PC",Blue
66755469279655,Sell,USD/CZK,22.4707903,36,0,0,1548763121468,New,"Bitcoin, Study, Music","Order for: Bitcoin, Study, Music",Blue
66755469279655,Sell,USD/CZK,22.4707903,36,0,0,1548785787957,ToProvider,"Bitcoin, Study, Music","Order for: Bitcoin, Study, Music",Blue
55576595143550,Sell,GBP/BYN,2.7182399999999998,1193,0,0,1548729331189,New,"Car, Bussiness, Trip","Order for: Car, Bussiness, Trip",Blue
55576595143550,Sell,GBP/BYN,2.7182399999999998,1193,0,0,1548793371667,ToProvider,"Car, Bussiness, Trip","Order for: Car, Bussiness, Trip",Blue
72240132256821,Sell,GBP/JPY,141.9851971,666,0,0,1548686891501,New,"PS, Games","Order for: PS, Games",Blue

```

##### MySQL table content:

![](https://i.ibb.co/Lr93XsN/Screenshot.png)