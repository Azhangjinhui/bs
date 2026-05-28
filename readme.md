# 中国省级碳排放预测与可视化大屏系统

> 基于 MySQL → Canal → Kafka → Spark → Doris 实时数据管道的碳排放数据分析与预测系统

## 项目简介

本项目是一个端到端的大数据应用系统，围绕 **碳排放数据** 构建了完整的大数据处理链路。通过 **Canal** 实时捕获 **MySQL** 业务库的 binlog 增量数据，经由 **Kafka** 消息队列接入 **Spark Structured Streaming** 进行实时 ETL 处理，最终写入 **Apache Doris** 数据仓库，构建 ODS → DWD 分层数据模型。同时利用 **Spark MLlib 随机森林回归** 对历史数据进行时序特征工程和预测建模，完成 2025 年中国 31 个省份各行业碳排放的月度预测。

## 系统架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                        数据采集层                                    │
│                                                                     │
│   CSV 原始文件 ──→ PySpark 读取 ──→ 写入 Doris ODS 层               │
│   MySQL 业务库 ──→ Canal (binlog) ──→ Kafka ──→ Spark Streaming     │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────┐
│                        数据仓库层 (Apache Doris)                     │
│                                                                     │
│   ODS 层（原始数据层）                                               │
│   ├── ods_china_provincial_carbon_2019_2024   中国各省月度碳排放      │
│   ├── ods_china_provincial_carbon_2024        中国各省2024碳排放      │
│   └── ods_all_country_carbon_2019_2024        全球分国家碳排放        │
│                                                                     │
│   DWD 层（明细数据层）                                               │
│   ├── dwd_china_provincial_carbon_2019_2024   各省月度明细            │
│   ├── dwd_china_provincial_total_carbon_2024  各省年度汇总            │
│   ├── dwd_china_carbon_sector_2024            各行业排放明细          │
│   ├── dwd_all_country_Total_carbon_2024       全球国家排放汇总        │
│   ├── dwd_five_country_Total_carbon_2019_2024 五国排放对比            │
│   ├── dwd_pre_china_provincial_carbon_2025    2025年预测结果          │
│   └── dwd_china_provincial_carbon_2025_2026   2025-2026年预测结果     │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────┐
│                        计算引擎层                                    │
│                                                                     │
│   PySpark 批处理                                                     │
│   ├── ODS → DWD ETL 作业（数据清洗、字段标准化、中文映射）            │
│   ├── 时序特征工程（滞后特征、滚动均值、周期编码）                     │
│   └── Spark MLlib 随机森林回归预测                                    │
│                                                                     │
│   Spark Structured Streaming 流处理                                  │
│   ├── Kafka 用户行为事件流实时 ETL                                    │
│   └── Kafka Nginx 访问日志流实时解析                                  │
│                                                                     │
│   用户画像标签计算                                                    │
│   └── Spark + MySQL 标签规则 + Elasticsearch 标签存储                 │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────┐
│                        数据服务层                                    │
│                                                                     │
│   Spring Boot 3 后端 API                                             │
│   ├── MyBatis 查询 Doris 数据仓库                                    │
│   ├── Redis 缓存加速查询                                             │
│   └── 火山引擎豆包大模型 AI 对话                                      │
│                                                                     │
│   Vue 3 大屏可视化                                                   │
│   ├── ECharts 数据图表                                               │
│   ├── DataV 大屏组件                                                 │
│   └── Element Plus / Arco Design UI                                  │
└─────────────────────────────────────────────────────────────────────┘
```

## 技术栈

| 层级 | 技术组件 |
|------|---------|
| 数据采集 | MySQL、Canal、Kafka |
| 数据仓库 | Apache Doris（OLAP 引擎，支持 MySQL 协议） |
| 批处理引擎 | PySpark 3.4、Spark SQL |
| 流处理引擎 | Spark Structured Streaming |
| 机器学习 | Spark MLlib（随机森林回归、交叉验证） |
| 用户标签 | Elasticsearch |
| 后端服务 | Java 21、Spring Boot 3.5、MyBatis、Redis |
| AI 能力 | 火山引擎豆包大模型（doubao-seed-1.6） |
| 前端大屏 | Vue 3、ECharts 5、DataV、Element Plus、Pinia |
| 构建工具 | Maven（后端）、Vue CLI（前端） |

## 项目结构

```
张金晖_毕设代码/
├── ZJH_PySparkCode/                         # 大数据处理模块
│   └── BigDataBs_zhang/
│       ├── src/
│       │   ├── jobs/                        # PySpark ETL 作业
│       │   │   ├── ods_*.py                 # ODS 层数据导入作业
│       │   │   ├── dwd_*.py                 # DWD 层 ETL 转换作业
│       │   │   └── dwd_pre_china_provincial_carbon_2025.py  # 碳排放预测
│       │   └── demo.py                      # Spark 演示代码
│       ├── cn/
│       │   └── zhang/
│       │       ├── stream/                  # 流式处理模块
│       │       │   ├── base/StreamingBaseModel.py  # 流式基类
│       │       │   ├── UserEventModel.py    # 用户行为事件处理
│       │       │   ├── NginxAccessModel.py  # Nginx 日志解析
│       │       │   └── ...
│       │       └── tag/                     # 用户画像标签模块
│       │           ├── base/BaseModel.py    # 标签计算基类
│       │           ├── match/               # 标签匹配模型
│       │           └── statistics/          # 统计类标签
│       ├── data/                            # 原始数据（CSV）
│       │   ├── PySql/                       # 数据导入脚本
│       │   ├── 中国各省24年排放量/           # 省份碳排放 CSV
│       │   └── 各国19-24年排放量/            # 国家碳排放 CSV
│       ├── sql/                             # SQL 建表脚本
│       │   ├── ods.sql                      # ODS 层建表语句
│       │   ├── dwd.sql                      # DWD 层建表语句
│       │   └── mysql_ddl.sql                # MySQL 建表语句
│       └── requirements.txt                 # Python 依赖
│
└── ZJH_BS/                                  # 后端与前端模块
    ├── big-screen-data-server/              # Spring Boot 后端
    │   ├── src/main/java/.../
    │   │   ├── controller/                  # REST API 控制器
    │   │   ├── service/                     # 业务服务层
    │   │   ├── mapper/                      # MyBatis 数据访问层
    │   │   ├── config/                      # 配置（Redis、数据库）
    │   │   └── util/                        # 工具类
    │   └── pom.xml                          # Maven 依赖
    └── vue-big-screen-plugin-master/        # Vue 3 大屏前端
        ├── src/
        │   ├── views/                       # 页面组件
        │   ├── components/                  # 公共组件
        │   ├── api/                         # 接口请求
        │   ├── router/                      # 路由配置
        │   └── store/                       # Pinia 状态管理
        └── package.json                     # 前端依赖
```

## 数据链路说明

### 1. 批处理链路（离线）

```
CSV 原始数据
    │
    ▼ PySpark 读取
ODS 层（原始数据落盘）
    │
    ▼ PySpark ETL 作业
    ├── 数据清洗（空值处理、类型转换）
    ├── 字段标准化（省份/行业中英文映射）
    └── 月度聚合
DWD 层（明细数据层）
    │
    ▼ Spark MLlib
    ├── 时序特征工程
    │   ├── lag_1 / lag_3 / lag_6（滞后特征）
    │   ├── roll_mean_3（滚动均值）
    │   └── month_sin / month_cos（月份周期编码）
    ├── 随机森林回归 + 3折交叉验证
    └── 2025年月度碳排放预测
预测结果 → DWD 预测表
```

### 2. 实时链路（流处理）

```
MySQL 业务库
    │
    ▼ Canal 监听 binlog
Kafka Topic
    │
    ▼ Spark Structured Streaming
    ├── JSON 解析与字段提取
    ├── IP 地址解析（百度开放 API）
    ├── User-Agent 解析
    └── 实时聚合计算
    │
    ▼ foreachBatch
MySQL / Doris（实时结果表）
```

### 3. 用户画像链路

```
MySQL 标签规则表（4级/5级标签）
    │
    ▼ Spark 读取标签规则
    ├── 解析 rule 字段 → 转换为查询条件
    ├── 从 Elasticsearch 查询业务数据
    ├── 5级标签与业务数据打标签
    ├── 读取 ES 历史标签
    └── 新旧标签合并
用户标签 → Elasticsearch
```

## 数据仓库建表

ODS 层与 DWD 层建表语句分别位于：
- [ZJH_PySparkCode/BigDataBs_zhang/sql/ods.sql](ZJH_PySparkCode/BigDataBs_zhang/sql/ods.sql) — ODS 层建表
- [ZJH_PySparkCode/BigDataBs_zhang/sql/dwd.sql](ZJH_PySparkCode/BigDataBs_zhang/sql/dwd.sql) — DWD 层建表
- [ZJH_PySparkCode/BigDataBs_zhang/sql/mysql_ddl.sql](ZJH_PySparkCode/BigDataBs_zhang/sql/mysql_ddl.sql) — MySQL 业务库建表

### Doris 建表示例

```sql
-- DWD 层：中国各省份月度碳排放
CREATE TABLE dwd_china_provincial_carbon_2019_2024 (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `province` VARCHAR(50) NOT NULL COMMENT '省市名称',
    `co2_mt` DECIMAL(15,6) NOT NULL COMMENT 'CO2排放量(百万吨)',
    `sector` VARCHAR(50) NOT NULL COMMENT '排放部门/行业',
    `year` DATE NOT NULL COMMENT '月份'
) ENGINE=OLAP
DUPLICATE KEY(`id`)
DISTRIBUTED BY HASH(`id`) BUCKETS 2;
```

## 模型预测说明

### 算法选择

采用 **随机森林回归（RandomForestRegressor）**，适合处理具有时序特征的碳排放数据，对异常值和噪声有较好的鲁棒性。

### 特征工程

| 特征名称 | 说明 |
|---------|------|
| time_index | 相对时间索引（按月递增） |
| month_sin | 月份正弦编码（捕捉季节性） |
| month_cos | 月份余弦编码（捕捉季节性） |
| lag_1 | 前1个月排放量 |
| lag_3 | 前3个月排放量 |
| lag_6 | 前6个月排放量 |
| roll_mean_3 | 近3个月滚动平均排放量 |

### 超参数调优

```python
param_grid = ParamGridBuilder()
    .addGrid(rf.numTrees, [50, 100])
    .addGrid(rf.maxDepth, [5, 8])
    .addGrid(rf.minInstancesPerNode, [3, 5])
    .build()
```

通过 **3 折交叉验证（CrossValidator）** 在 8 种超参数组合中自动选择 RMSE 最优的模型。

### 预测范围

- **预测对象**：中国 31 个省级行政区 × 7 个行业
- **预测粒度**：月度
- **预测时间段**：2025 年 1-12 月

## 环境依赖

### Python 依赖

```
pyspark~=3.4.1
apache-flink~=2.0.0
requests~=2.32.2
numpy
```

安装依赖：

```bash
cd ZJH_PySparkCode/BigDataBs_zhang
pip install -r requirements.txt
```

### 基础环境

| 组件 | 版本要求 |
|------|---------|
| JDK | 1.8 |
| Apache Spark | 3.5+ |
| Apache Doris | 2.x+ |
| Kafka | 2.x+ |
| MySQL | 5.7+ |
| Redis | 6.x+ |
| Node.js | 16+（前端构建） |

### 环境变量配置

```bash
export JAVA_HOME=/usr/local/jdk1.8.0_281/
export SPARK_HOME=/usr/local/spark
```

## 运行方式

### 1. 数据仓库建表

```bash
# 在 Doris 中执行建表语句
mysql -h node01 -P 9030 -u root < ZJH_PySparkCode/BigDataBs_zhang/sql/ods.sql
mysql -h node01 -P 9030 -u root < ZJH_PySparkCode/BigDataBs_zhang/sql/dwd.sql
```

### 2. 执行 ODS 层数据导入

```bash
cd ZJH_PySparkCode/BigDataBs_zhang
spark-submit --master local[2] src/jobs/ods_china_provincial_carbon_2019_2024.py
spark-submit --master local[2] src/jobs/ods_all_country_carbon_2019-2024.py
```

### 3. 执行 DWD 层 ETL 作业

```bash
spark-submit --master local[2] src/jobs/dwd_china_provincial_carbon_2019_2024.py
spark-submit --master local[2] src/jobs/dwd_china_provincial_total_carbon_2024.py
spark-submit --master local[2] src/jobs/dwd_china_carbon_sector_2024.py
spark-submit --master local[2] src/jobs/dwd_all_country_Total_carbon_2024.py
spark-submit --master local[2] src/jobs/dwd_five_country_Total_carbon_2019_2024.py
```

### 4. 执行碳排放预测

```bash
spark-submit --master local[2] src/jobs/dwd_pre_china_provincial_carbon_2025.py
```

### 5. 启动后端服务

```bash
cd ZJH_BS/big-screen-data-server
mvn spring-boot:run
```

### 6. 启动前端大屏

```bash
cd ZJH_BS/vue-big-screen-plugin-master
npm install
npm run serve
```

## 数据来源

碳排放数据来源于全球碳排放追踪数据集，覆盖：
- **时间范围**：2019 年 1 月 - 2024 年 12 月（月度数据）
- **地理范围**：中国 31 个省级行政区
- **行业分类**：电力、工业、地面运输、居民消费、国内航空、国际航空、总排放
- **指标**：CO₂ 排放量（百万吨）
