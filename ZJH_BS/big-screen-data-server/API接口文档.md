# 大屏数据服务器 API 接口文档

## 基础信息

- **服务地址**: http://localhost:8080
- **接口前缀**: /api/doris/carbon

## 响应格式

```json
{
  "code": 200,
  "message": "查询成功",
  "data": [...],
  "total": 100
}
```

## 接口列表

### 1. 全球国家碳排放数据

**地址**: `GET /api/doris/carbon/dwd_all_country_Total_carbon_2024`

**响应示例**:

```json
{
    "total": 9,
    "code": 200,
    "data": [
        {
            "area": "意大利",
            "co2_mt": 285.352214,
            "year": 2024,
            "latitude": 41.90280000,
            "id": 2,
            "sector": "Total",
            "longitude": 12.49640000
        }
}
```

### 2. 中国行业碳排放数据

**地址**: `GET /api/doris/carbon/dwd_china_carbon_sector_2024`

**响应示例**:

```json
{
    "total": 36,
    "code": 200,
    "data": [
        {
            "area": "China",
            "co2_mt": 62.458511,
            "year": 2019,
            "id": 1,
            "sector": "国内航空"
        },
    
}
```

### 3. 中国省份碳排放数据

**地址**: `GET /api/doris/carbon/dwd_china_provincial_total_carbon_2024`

**响应示例**:

```json
{
    "total": 31,
    "code": 200,
    "data": [
        {
            "province": "安徽",
            "co2_mt": 417.851032,
            "year": 2024,
            "id": 1,
            "sector": "Total"
        },
}
```

### 4. 五国历史碳排放数据

**地址**: `GET /api/doris/carbon/dwd_five_country_Total_carbon_2019_2024`

**响应示例**:

```json
{
    "total": 36,
    "code": 200,
    "data": [
        {
            "area": "俄罗斯",
            "co2_mt": 1563.111161,
            "year": 2021,
            "id": 2,
            "sector": "Total"
        },
}
```

## 字段说明

- `id`: 主键
- `area`: 国家/地区
- `province`: 省份
- `co2_mt`: 碳排放量（百万吨）
- `sector`: 行业部门
- `year`: 年份
- `longitude`: 经度
- `latitude`: 纬度

# Redis缓存使用说明

## 概述

项目已集成Redis缓存，缓存时间为7天，提升查询性能。

## 环境要求

* Redis服务器：`118.145.198.148:6379`

## 缓存接口

以下接口已自动缓存30天：

1. 全球国家碳排放数据：`GET /api/doris/carbon/dwd_all_country_Total_carbon_2024`
2. 中国行业碳排放数据：`GET /api/doris/carbon/dwd_china_carbon_sector_2024`
3. 中国省份碳排放数据：`GET /api/doris/carbon/dwd_china_provincial_total_carbon_2024`
4. 五国历史碳排放数据：`GET /api/doris/carbon/dwd_five_country_Total_carbon_2019_2024`

## 缓存管理

### 检查Redis状态

```javascript
GET /api/cache/health
```

### 查看缓存信息

```javascript
GET /api/cache/stats
```

### 清除所有缓存

```javascript
DELETE /api/cache/clear/all
```

### 清除指定缓存

```javascript
DELETE /api/cache/clear/{cacheName}
```

可选值：`allCountry`、`chinaSector`、`chinaProvincial`、`fiveCountry`

## 使用示例

```javascript
fetch('http://localhost:8080/api/doris/carbon/dwd_all_country_Total_carbon_2024')
  .then(response => response.json())
  .then(data => console.log(data));
```
