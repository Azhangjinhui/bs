package org.example.bigscreendataserver.controller;

import org.example.bigscreendataserver.util.CacheUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.TimeUnit;

/**
 * 缓存管理控制器
 */
@RestController
@RequestMapping("/api/cache")
@CrossOrigin(origins = "*")
public class CacheController {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Autowired
    private CacheUtil cacheUtil;

    /**
     * Redis健康检查
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> checkRedisHealth() {
        try {
            // 测试Redis连接
            String testKey = "health_check";
            String testValue = "ok";
            
            redisTemplate.opsForValue().set(testKey, testValue);
            String result = (String) redisTemplate.opsForValue().get(testKey);
            redisTemplate.delete(testKey);
            
            Map<String, Object> response = new HashMap<>();
            if (testValue.equals(result)) {
                response.put("code", 200);
                response.put("message", "Redis连接正常");
                response.put("status", "healthy");
            } else {
                response.put("code", 500);
                response.put("message", "Redis连接异常");
                response.put("status", "unhealthy");
            }
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 500);
            errorResponse.put("message", "Redis连接失败: " + e.getMessage());
            errorResponse.put("status", "error");
            return ResponseEntity.status(500).body(errorResponse);
        }
    }

    /**
     * 获取缓存统计信息
     */
    @GetMapping("/stats")
    public ResponseEntity<Map<String, Object>> getCacheStats() {
        try {
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("message", "缓存统计信息获取成功");
            
            Map<String, Object> stats = new HashMap<>();
            stats.put("redis_connected", true);
            
            // 获取所有缓存键
            Set<String> keys = redisTemplate.keys("carbon:*");
            stats.put("total_keys", keys != null ? keys.size() : 0);
            stats.put("cache_keys", keys);
            
            stats.put("cache_names", new String[]{
                "carbon:allCountry", 
                "carbon:chinaSector", 
                "carbon:chinaProvincial", 
                "carbon:fiveCountry"
            });
            response.put("data", stats);
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 500);
            errorResponse.put("message", "获取缓存统计信息失败: " + e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
    
    /**
     * 清除所有碳排放缓存
     */
    @DeleteMapping("/clear/all")
    public ResponseEntity<Map<String, Object>> clearAllCarbonCache() {
        try {
            cacheUtil.clearAllCarbonCache();
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("message", "所有碳排放缓存清除成功");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 500);
            errorResponse.put("message", "缓存清除失败: " + e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
    
    /**
     * 清除指定缓存
     */
    @DeleteMapping("/clear/{cacheName}")
    public ResponseEntity<Map<String, Object>> clearSpecificCache(@PathVariable String cacheName) {
        try {
            cacheUtil.clearCache("carbon:" + cacheName);
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("message", "缓存 " + cacheName + " 清除成功");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 500);
            errorResponse.put("message", "缓存清除失败: " + e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
    
    /**
     * 获取指定缓存的TTL（生存时间）
     */
    @GetMapping("/ttl/{key}")
    public ResponseEntity<Map<String, Object>> getCacheTTL(@PathVariable String key) {
        try {
            Long ttl = redisTemplate.getExpire(key, TimeUnit.SECONDS);
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("message", "TTL获取成功");
            
            Map<String, Object> data = new HashMap<>();
            data.put("key", key);
            data.put("ttl_seconds", ttl);
            data.put("ttl_minutes", ttl > 0 ? ttl / 60.0 : ttl);
            response.put("data", data);
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 500);
            errorResponse.put("message", "TTL获取失败: " + e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
    
    /**
     * 检查缓存键是否存在
     */
    @GetMapping("/exists/{key}")
    public ResponseEntity<Map<String, Object>> checkCacheExists(@PathVariable String key) {
        try {
            Boolean exists = redisTemplate.hasKey(key);
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("message", "缓存检查完成");
            
            Map<String, Object> data = new HashMap<>();
            data.put("key", key);
            data.put("exists", exists);
            response.put("data", data);
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("code", 500);
            errorResponse.put("message", "缓存检查失败: " + e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
}