package org.example.bigscreendataserver.service.impl;

import org.example.bigscreendataserver.mapper.*;
import org.example.bigscreendataserver.service.DorisTableService;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

/**
 * Doris碳排放数据服务实现类
 */
@Service
public class DorisTableServiceImpl implements DorisTableService {
    
    private final AllCountryTotalCarbonMapper allCountryTotalCarbonMapper;
    private final ChinaCarbonSectorMapper chinaCarbonSectorMapper;
    private final ChinaProvincialTotalCarbonMapper chinaProvincialTotalCarbonMapper;
    private final FiveCountryTotalCarbonMapper fiveCountryTotalCarbonMapper;
    

    public DorisTableServiceImpl(AllCountryTotalCarbonMapper allCountryTotalCarbonMapper,
                                ChinaCarbonSectorMapper chinaCarbonSectorMapper,
                                ChinaProvincialTotalCarbonMapper chinaProvincialTotalCarbonMapper,
                                FiveCountryTotalCarbonMapper fiveCountryTotalCarbonMapper) {
        this.allCountryTotalCarbonMapper = allCountryTotalCarbonMapper;
        this.chinaCarbonSectorMapper = chinaCarbonSectorMapper;
        this.chinaProvincialTotalCarbonMapper = chinaProvincialTotalCarbonMapper;
        this.fiveCountryTotalCarbonMapper = fiveCountryTotalCarbonMapper;
    }
    
    @Override
    @Cacheable(value = "carbon:allCountry", key = "'all'")
    public List<Map<String, Object>> getAllCountryTotalCarbonData() {
        try {
            List<Map<String, Object>> result = allCountryTotalCarbonMapper.selectAll();
            return result;
        } catch (Exception e) {
            // 错误处理
            throw new RuntimeException("查询全球国家碳排放总量数据失败: " + e.getMessage());
        }
    }
    
    @Override
    @Cacheable(value = "carbon:chinaSector", key = "'all'")
    public List<Map<String, Object>> getChinaCarbonSectorData() {
        try {
            List<Map<String, Object>> result = chinaCarbonSectorMapper.selectAll();
            return result;
        } catch (Exception e) {
            // 错误处理
            throw new RuntimeException("查询中国碳排放行业数据失败: " + e.getMessage());
        }
    }
    
    @Override
    @Cacheable(value = "carbon:chinaProvincial", key = "'all'")
    public List<Map<String, Object>> getChinaProvincialTotalCarbonData() {
        try {
            List<Map<String, Object>> result = chinaProvincialTotalCarbonMapper.selectAll();
            return result;
        } catch (Exception e) {
            // 错误处理
            throw new RuntimeException("查询中国省份碳排放总量数据失败: " + e.getMessage());
        }
    }
    
    @Override
    @Cacheable(value = "carbon:fiveCountry", key = "'all'")
    public List<Map<String, Object>> getFiveCountryTotalCarbonData() {
        try {
            List<Map<String, Object>> result = fiveCountryTotalCarbonMapper.selectAll();
            return result;
        } catch (Exception e) {
            // 错误处理
            throw new RuntimeException("查询五国碳排放总量历史数据失败: " + e.getMessage());
        }
    }
}