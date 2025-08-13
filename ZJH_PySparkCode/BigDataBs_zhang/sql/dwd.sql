create database dwd_carbon



CREATE TABLE dwd_china_provincial_total_carbon_2024 (
                                                  `id` BIGINT  NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                                  `province` VARCHAR(50) NOT NULL COMMENT '省市名称',
                                                  `co2_mt` DECIMAL(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                                  `sector` VARCHAR(50) NOT NULL COMMENT '排放部门/行业',
                                                  `year` INT NOT NULL COMMENT '年份'
) ENGINE=OLAP
    DUPLICATE KEY(`id`)
COMMENT '中国各个省市总排放量2024'
DISTRIBUTED BY HASH(`id`) BUCKETS 2
PROPERTIES (
  "replication_num" = "1",
  "in_memory" = "false",
  "storage_format" = "V2"
);


CREATE TABLE dwd_china_carbon_sector_2024 (
                                                        `id` BIGINT  NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                                        `area` VARCHAR(50) NOT NULL COMMENT '中国',
                                                        `co2_mt` DECIMAL(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                                        `sector` VARCHAR(50) NOT NULL COMMENT '排放部门/行业',
                                                        `year` INT NOT NULL COMMENT '年份'
) ENGINE=OLAP
    DUPLICATE KEY(`id`)
COMMENT '中国各行业总排放量2019-2024'
DISTRIBUTED BY HASH(`id`) BUCKETS 2
PROPERTIES (
  "replication_num" = "1",
  "in_memory" = "false",
  "storage_format" = "V2"
);


CREATE TABLE dwd_all_country_Total_carbon_2024 (
                                              `id` BIGINT  NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                              `area` VARCHAR(50) NOT NULL COMMENT '国家',
                                              `co2_mt` DECIMAL(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                              `sector` VARCHAR(50) NOT NULL COMMENT '排放部门/行业',
                                              `year` INT NOT NULL COMMENT '年份',
                                              `longitude` DECIMAL(11, 8) NOT NULL COMMENT '经度（范围-180~180，保留8位小数）',
                                              `latitude` DECIMAL(10, 8) NOT NULL COMMENT '纬度（范围-90~90，保留8位小数）'

) ENGINE=OLAP
    DUPLICATE KEY(`id`)
COMMENT '全国总排放量2024'
DISTRIBUTED BY HASH(`id`) BUCKETS 2
PROPERTIES (
  "replication_num" = "1",
  "in_memory" = "false",
  "storage_format" = "V2"
);


CREATE TABLE dwd_five_country_Total_carbon_2019_2024 (
                                                   `id` BIGINT  NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                                   `area` VARCHAR(50) NOT NULL COMMENT '国家',
                                                   `co2_mt` DECIMAL(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                                   `sector` VARCHAR(50) NOT NULL COMMENT '排放部门/行业',
                                                   `year` INT NOT NULL COMMENT '年份'


) ENGINE=OLAP
    DUPLICATE KEY(`id`)
COMMENT '5国总排放量19-24'
DISTRIBUTED BY HASH(`id`) BUCKETS 2
PROPERTIES (
  "replication_num" = "1",
  "in_memory" = "false",
  "storage_format" = "V2"
);