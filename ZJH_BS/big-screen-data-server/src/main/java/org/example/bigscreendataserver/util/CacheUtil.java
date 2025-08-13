package org.example.bigscreendataserver.util;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cache.Cache;
import org.springframework.cache.CacheManager;
import org.springframework.stereotype.Component;

/**
 * 缓存工具类
 */
@Component
public class CacheUtil {
    
    private static final Logger logger = LoggerFactory.getLogger(CacheUtil.class);

    private final CacheManager cacheManager;
    
    public CacheUtil(CacheManager cacheManager) {
        this.cacheManager = cacheManager;
    }

    /**
     * 清除指定缓存
     * @param cacheName 缓存名称
     * @param key 缓存键
     */
    public void evictCache(String cacheName, String key) {
        logger.debug("尝试清除缓存: {}, key: {}", cacheName, key);
        Cache cache = cacheManager.getCache(cacheName);
        if (cache != null) {
            cache.evict(key);
            logger.debug("缓存键已清除: {}, key: {}", cacheName, key);
        } else {
            logger.warn("缓存不存在: {}", cacheName);
        }
    }

    /**
     * 清除指定缓存的所有数据
     * @param cacheName 缓存名称
     */
    public void clearCache(String cacheName) {
        logger.debug("尝试清除缓存: {}", cacheName);
        Cache cache = cacheManager.getCache(cacheName);
        if (cache != null) {
            cache.clear();
            logger.info("缓存已清除: {}", cacheName);
        } else {
            logger.warn("缓存不存在: {}", cacheName);
        }
    }

    /**
     * 清除所有碳排放相关缓存
     */
    public void clearAllCarbonCache() {
        logger.info("开始清除所有碳排放相关缓存");
        clearCache("carbon:allCountry");
        clearCache("carbon:chinaSector");
        clearCache("carbon:chinaProvincial");
        clearCache("carbon:fiveCountry");
        logger.info("所有碳排放相关缓存清除完成");
    }
}