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
    InitVolume - initial volume
    FillPx - filled currency pair value
    InitVolume - filled volume
    Status - status of order
    StatusTimestamp - time of status changing in milliseconds
    Tags - order tags
    Desription - order descriptionn
```

All orders records divided distributed between 3 zones:
* Red: Order started in previous periods of trading and finish in current period
* Green: Order start and finish in same period 
* Blue: Order start in current period and finish in next periods

Trading execute on period Friday-Tuesday except weekends




Install:

```bash
$ git clone https://github.com/Artyom-Sysa/OrdersHistoryGenerator.git
```

Chech if python exists:
```bash
$ python --version
```
If it not exists install it. Download it from official site: https://www.python.org/
Or update it if yours python version less than 3.7. 



Install additional modules
```bash
$ pip install -r /path/to/project/folder/requirements.txt 
```

Install RabbitMQ

Create MySQL database
```sql
CREATE DATABASE `OrdersHistory`;

USE `OrdersHistory`;

CREATE TABLE `History` (
  `id` bigint(16) NOT NULL,
  `direction` varchar(4) NOT NULL,
  `currency_pair` varchar(10) NOT NULL,
  `init_px` decimal(10,5) NOT NULL,
  `fill_px` decimal(10,5) NOT NULL,
  `init_vol` decimal(10,5) NOT NULL,
  `fill_vol` decimal(10,5) NOT NULL,
  `status` varchar(45) NOT NULL,
  `datetime` bigint NOT NULL,
  `tags` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

---
#Usage

Configurate generation settings before executing
:

Required settings:


```
// Change to your configurations

[GENERAL]
orders_amount = 2000
orders_in_first_blue_zone = 3
red_zone_orders_percent = 15
green_zone_orders_percent = 60
blue_zone_orders_percent = 25
batch_size = 100
currency_deviation_percent = 5
order_history_write_file_path = C:\Users\Artyom Sysa\Documents\OrdersHistoryGenerator\Resources\Result.csv
currency_pairs_file_path = C:\Users\Artyom Sysa\Documents\OrdersHistoryGenerator\Resources\CurrencyPairs.txt
tags_file_path = C:\Users\Artyom Sysa\Documents\OrdersHistoryGenerator\Resources\Tags.txt

[LOGGER]
logging_folder_path = C:\Users\Artyom Sysa\Documents\OrdersHistoryGenerator\Log
logger_format = %%(levelname)s	%%(asctime)s.%%(msecs)d   %%(name)s : %%(message)s
logger_date_format = %%d-%%m-%%Y %%H:%%M:%%S
logger_level = ERROR

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
rabbitmq_red_records_routing_key = r.order.red-zone.order-history-generator
rabbitmq_blue_records_routing_key = r.order.blue-zone.order-history-generator
rabbitmq_gree_records_routing_key = r.order.green-zone.order-history-generator

```

If you want you can change other parameters in your settins.ini file

## Starting history generation

```
$ python Launcher.py
```

---
## Execution example
```bash
$ python Launcher.py

Generating orders records history...
Writing records to file...
Reading records from file...
Sending records to RabbitMQ...
Sending records to MySQL...

========== REPORT ==========
Order history generation
Max: 32.942 ms
Min: 22.913 ms
Avg: 26.67985 ms
---------------

Green records writing to file
Max: 66.82000000000001 ms
Min: 3.9880000000000004 ms
Avg: 14.704860465116282 ms
---------------

Red records writing to file
Max: 5.986 ms
Min: 5.983 ms
Avg: 5.984 ms
---------------

Blue records writing to file
Max: 6.982 ms
Min: 5.982 ms
Avg: 6.074636363636364 ms
---------------

Read and sort records by zones: 35.902 ms
---------------

Send RabbitMQ red zone records
Max: 48.869 ms
Min: 17.953 ms
Avg: 35.5052 ms
---------------

Send RabbitMQ blue zone records
Max: 81.78 ms
Min: 29.919999999999998 ms
Avg: 68.81590909090909 ms
---------------

Send RabbitMQ green zone records
Max: 58.844 ms
Min: 6.983 ms
Avg: 51.69897674418605 ms
---------------

Send red zones records to MySql
Max: 103.722 ms
Min: 8.975999999999999 ms
Avg: 35.1062 ms
---------------

Send blue zones records to MySql
Max: 21.942 ms
Min: 10.971 ms
Avg: 19.402636363636365 ms
---------------

Send green zones records to MySql
Max: 108.646 ms
Min: 3.965 ms
Avg: 17.347767441860466 ms
---------------

========== REPORT END ==========
```

Result file content:
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

MySQL table content:

![](https://i.ibb.co/zGBDZd2/Screenshot-2.png)
