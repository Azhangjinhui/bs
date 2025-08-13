package org.example.bigscreendataserver.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

/**
 * 中国碳排放行业数据访问Mapper
 */
@Mapper
public interface ChinaCarbonSectorMapper {
    
    /**
     * 查询中国碳排放行业数据
     */
    @Select("SELECT * FROM dwd_china_carbon_sector_2024")
    List<Map<String, Object>> selectAll();
}