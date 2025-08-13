package org.example.bigscreendataserver.service;

import java.util.List;
import java.util.Map;

/**
 * Doris碳排放数据服务接口
 */
public interface DorisTableService {
    
    /**
     * 获取全球国家碳排放总量数据
     */
    List<Map<String, Object>> getAllCountryTotalCarbonData();
    
    /**
     * 获取中国碳排放行业数据
     */
    List<Map<String, Object>> getChinaCarbonSectorData();
    
    /**
     * 获取中国省份碳排放总量数据
     */
    List<Map<String, Object>> getChinaProvincialTotalCarbonData();
    
    /**
     * 获取五国碳排放总量历史数据
     */
    List<Map<String, Object>> getFiveCountryTotalCarbonData();
}
