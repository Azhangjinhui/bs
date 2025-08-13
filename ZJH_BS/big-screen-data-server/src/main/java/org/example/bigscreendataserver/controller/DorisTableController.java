package org.example.bigscreendataserver.controller;

import org.example.bigscreendataserver.service.DorisTableService;
import org.example.bigscreendataserver.util.CacheUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Doris碳排放数据接口控制器
 */
@RestController
@RequestMapping("/api/doris/carbon")
@CrossOrigin(origins = {"*"}) 
public class DorisTableController {
    
    private static final Logger logger = LoggerFactory.getLogger(DorisTableController.class);
    
    private final DorisTableService dorisTableService;
    private final CacheUtil cacheUtil;
    
    public DorisTableController(DorisTableService dorisTableService, CacheUtil cacheUtil) {
        this.dorisTableService = dorisTableService;
        this.cacheUtil = cacheUtil;
    }
    
    /**
     * 创建成功响应
     */
    private ResponseEntity<Map<String, Object>> createSuccessResponse(List<Map<String, Object>> data, String message) {
        Map<String, Object> response = new HashMap<>();
        response.put("code", 200);
        response.put("message", message);
        response.put("data", data);
        response.put("total", data != null ? data.size() : 0);
        return ResponseEntity.ok(response);
    }
    
    /**
     * 创建错误响应
     */
    private ResponseEntity<Map<String, Object>> createErrorResponse(Exception e, String operation) {
        logger.error("{}失败: {}", operation, e.getMessage(), e);
        Map<String, Object> errorResponse = new HashMap<>();
        errorResponse.put("code", 500);
        errorResponse.put("message", operation + "失败: " + e.getMessage());
        errorResponse.put("data", null);
        return ResponseEntity.status(500).body(errorResponse);
    }
    
    /**
     * 获取全球国家碳排放总量数据
     */
    @GetMapping("/dwd_all_country_Total_carbon_2024")
    public ResponseEntity<Map<String, Object>> getAllCountryTotalCarbonData() {
        try {
            logger.info("开始查询全球国家碳排放总量数据");
            List<Map<String, Object>> data = dorisTableService.getAllCountryTotalCarbonData();
            logger.info("查询全球国家碳排放总量数据成功，返回{}条记录", data.size());
            return createSuccessResponse(data, "查询成功");
        } catch (Exception e) {
            return createErrorResponse(e, "查询全球国家碳排放总量数据");
        }
    }
    
    /**
     * 获取中国碳排放行业数据
     */
    @GetMapping("/dwd_china_carbon_sector_2024")
    public ResponseEntity<Map<String, Object>> getChinaCarbonSectorData() {
        try {
            logger.info("开始查询中国碳排放行业数据");
            List<Map<String, Object>> data = dorisTableService.getChinaCarbonSectorData();
            logger.info("查询中国碳排放行业数据成功，返回{}条记录", data.size());
            return createSuccessResponse(data, "查询成功");
        } catch (Exception e) {
            return createErrorResponse(e, "查询中国碳排放行业数据");
        }
    }
    
    /**
     * 获取中国省份碳排放总量数据
     */
    @GetMapping("/dwd_china_provincial_total_carbon_2024")
    public ResponseEntity<Map<String, Object>> getChinaProvincialTotalCarbonData() {
        try {
            logger.info("开始查询中国省份碳排放总量数据");
            List<Map<String, Object>> data = dorisTableService.getChinaProvincialTotalCarbonData();
            logger.info("查询中国省份碳排放总量数据成功，返回{}条记录", data.size());
            return createSuccessResponse(data, "查询成功");
        } catch (Exception e) {
            return createErrorResponse(e, "查询中国省份碳排放总量数据");
        }
    }
    
    /**
     * 获取五国碳排放总量历史数据
     */
    @GetMapping("/dwd_five_country_Total_carbon_2019_2024")
    public ResponseEntity<Map<String, Object>> getFiveCountryTotalCarbonData() {
        try {
            logger.info("开始查询五国碳排放总量历史数据");
            List<Map<String, Object>> data = dorisTableService.getFiveCountryTotalCarbonData();
            logger.info("查询五国碳排放总量历史数据成功，返回{}条记录", data.size());
            return createSuccessResponse(data, "查询成功");
        } catch (Exception e) {
            return createErrorResponse(e, "查询五国碳排放总量历史数据");
        }
    }
    
    /**
     * 清除所有缓存
     */
    @DeleteMapping("/cache/clear")
    public ResponseEntity<Map<String, Object>> clearAllCache() {
        try {
            logger.info("开始清除所有碳排放缓存");
            cacheUtil.clearAllCarbonCache();
            logger.info("所有碳排放缓存清除成功");
            
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("message", "缓存清除成功");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return createErrorResponse(e, "清除缓存");
        }
    }
    
    /**
     * 清除指定缓存
     */
    @DeleteMapping("/cache/clear/{cacheName}")
    public ResponseEntity<Map<String, Object>> clearSpecificCache(@PathVariable String cacheName) {
        try {
            String fullCacheName = "carbon:" + cacheName;
            logger.info("开始清除缓存: {}", fullCacheName);
            cacheUtil.clearCache(fullCacheName);
            logger.info("缓存 {} 清除成功", fullCacheName);
            
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("message", "缓存 " + cacheName + " 清除成功");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return createErrorResponse(e, "清除缓存 " + cacheName);
        }
    }
}
