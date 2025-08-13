create table  china_provincial_carbon_2024(
                                              `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                              `province` varchar(50) NOT NULL  COMMENT '省名称',
                                              `co2_mt` decimal(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                              `sector` varchar(50) NOT NULL COMMENT '排放部门/行业',
                                              `year` year(4) NOT NULL COMMENT '年份',
                                              PRIMARY KEY (`id`),
                                              KEY `idx_sector` (`sector`) COMMENT '按部门查询优化'

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='中国各省市各行业排放数据2024';
-- 中国分行业碳排放数据表
CREATE TABLE china_carbon_2019_2024  (
                                         `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                         `area` varchar(50) NOT NULL DEFAULT 'China' COMMENT '地区名称',
                                         `co2_mt` decimal(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                         `sector` varchar(50) NOT NULL COMMENT '排放部门/行业',
                                         `year` year(4) NOT NULL COMMENT '年份',
                                         PRIMARY KEY (`id`),
                                         KEY `idx_year` (`year`) COMMENT '按年份查询优化'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='中国分行业碳排放数据(2019 - 2024)';

-- 美国分行业碳排放数据表
CREATE TABLE america_carbon_2019_2024  (
                                           `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                           `area` varchar(50) NOT NULL DEFAULT 'America' COMMENT '地区名称',
                                           `co2_mt` decimal(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                           `sector` varchar(50) NOT NULL COMMENT '排放部门/行业',
                                           `year` year(4) NOT NULL COMMENT '年份',
                                           PRIMARY KEY (`id`),
                                           KEY `idx_year` (`year`) COMMENT '按年份查询优化'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='美国分行业碳排放数据(2019 - 2024)';

-- 全球分行业碳排放数据表
CREATE TABLE world_carbon_2019_2024  (
                                         `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                         `area` varchar(50) NOT NULL DEFAULT 'World' COMMENT '地区名称',
                                         `co2_mt` decimal(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                         `sector` varchar(50) NOT NULL COMMENT '排放部门/行业',
                                         `year` year(4) NOT NULL COMMENT '年份',
                                         PRIMARY KEY (`id`),
                                         KEY `idx_year` (`year`) COMMENT '按年份查询优化'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='全球分行业碳排放数据(2019 - 2024)';

-- 英国分行业碳排放数据表
CREATE TABLE england_carbon_2019_2024  (
                                           `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                           `area` varchar(50) NOT NULL DEFAULT 'England' COMMENT '地区名称',
                                           `co2_mt` decimal(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                           `sector` varchar(50) NOT NULL COMMENT '排放部门/行业',
                                           `year` year(4) NOT NULL COMMENT '年份',
                                           PRIMARY KEY (`id`),
                                           KEY `idx_year` (`year`) COMMENT '按年份查询优化'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='英国分行业碳排放数据(2019 - 2024)';

-- 法国分行业碳排放数据表
CREATE TABLE france_carbon_2019_2024  (
                                          `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                          `area` varchar(50) NOT NULL DEFAULT 'France' COMMENT '地区名称',
                                          `co2_mt` decimal(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                          `sector` varchar(50) NOT NULL COMMENT '排放部门/行业',
                                          `year` year(4) NOT NULL COMMENT '年份',
                                          PRIMARY KEY (`id`),
                                          KEY `idx_year` (`year`) COMMENT '按年份查询优化'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='法国分行业碳排放数据(2019 - 2024)';

-- 德国分行业碳排放数据表
CREATE TABLE Germany_carbon_2019_2024  (
                                           `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                           `area` varchar(50) NOT NULL DEFAULT 'Germany' COMMENT '地区名称',
                                           `co2_mt` decimal(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                           `sector` varchar(50) NOT NULL COMMENT '排放部门/行业',
                                           `year` year(4) NOT NULL COMMENT '年份',
                                           PRIMARY KEY (`id`),
                                           KEY `idx_year` (`year`) COMMENT '按年份查询优化'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='德国分行业碳排放数据(2019 - 2024)';

-- 印度分行业碳排放数据表
CREATE TABLE india_carbon_2019_2024  (
                                         `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                         `area` varchar(50) NOT NULL DEFAULT 'India' COMMENT '地区名称',
                                         `co2_mt` decimal(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                         `sector` varchar(50) NOT NULL COMMENT '排放部门/行业',
                                         `year` year(4) NOT NULL COMMENT '年份',
                                         PRIMARY KEY (`id`),
                                         KEY `idx_year` (`year`) COMMENT '按年份查询优化'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='印度分行业碳排放数据(2019 - 2024)';

-- 意大利分行业碳排放数据表
CREATE TABLE italy_carbon_2019_2024  (
                                         `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                         `area` varchar(50) NOT NULL DEFAULT 'Italy' COMMENT '地区名称',
                                         `co2_mt` decimal(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                         `sector` varchar(50) NOT NULL COMMENT '排放部门/行业',
                                         `year` year(4) NOT NULL COMMENT '年份',
                                         PRIMARY KEY (`id`),
                                         KEY `idx_year` (`year`) COMMENT '按年份查询优化'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='意大利分行业碳排放数据(2019 - 2024)';

-- 日本分行业碳排放数据表
CREATE TABLE japan_carbon_2019_2024  (
                                         `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                         `area` varchar(50) NOT NULL DEFAULT 'Japan' COMMENT '地区名称',
                                         `co2_mt` decimal(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                         `sector` varchar(50) NOT NULL COMMENT '排放部门/行业',
                                         `year` year(4) NOT NULL COMMENT '年份',
                                         PRIMARY KEY (`id`),
                                         KEY `idx_year` (`year`) COMMENT '按年份查询优化'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='日本分行业碳排放数据(2019 - 2024)';

-- 俄罗斯分行业碳排放数据表
CREATE TABLE russia_carbon_2019_2024  (
                                          `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                          `area` varchar(50) NOT NULL DEFAULT 'Russia' COMMENT '地区名称',
                                          `co2_mt` decimal(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                          `sector` varchar(50) NOT NULL COMMENT '排放部门/行业',
                                          `year` year(4) NOT NULL COMMENT '年份',
                                          PRIMARY KEY (`id`),
                                          KEY `idx_year` (`year`) COMMENT '按年份查询优化'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='俄罗斯分行业碳排放数据(2019 - 2024)';








CREATE TABLE all_country_carbon_2019_2024 (
                                              `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
                                              `area` varchar(50) NOT NULL COMMENT '地区名称（如China、America、World等）',
                                              `co2_mt` decimal(15,6) NOT NULL COMMENT '二氧化碳排放量(百万吨)',
                                              `sector` varchar(50) NOT NULL COMMENT '排放部门/行业',
                                              `year` year(4) NOT NULL COMMENT '年份',
                                              PRIMARY KEY (`id`),
    -- 新增复合索引，优化多条件查询
                                              KEY `idx_area_year` (`area`, `year`) COMMENT '按地区+年份查询优化',
                                              KEY `idx_sector_year` (`sector`, `year`) COMMENT '按行业+年份查询优化'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='全球分国家/地区分行业碳排放数据(2019-2024)';


TRUNCATE TABLE all_country_carbon_2019_2024