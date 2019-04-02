CREATE SCHEMA `OrdersHistory` ;

CREATE TABLE `History` (
  `id` bigint(16) NOT NULL,
  `direction` varchar(4) NOT NULL,
  `currency_pair` varchar(10) NOT NULL,
  `init_px` decimal(10,5) NOT NULL,
  `fill_px` decimal(10,5) NOT NULL,
  `init_vol` decimal(10,5) NOT NULL,
  `fill_vol` decimal(10,5) NOT NULL,
  `status` varchar(45) NOT NULL,
  `datetime` bigint(16) NOT NULL,
  `tags` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
