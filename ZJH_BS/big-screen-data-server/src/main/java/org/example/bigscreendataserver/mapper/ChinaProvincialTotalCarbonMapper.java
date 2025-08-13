package org.example.bigscreendataserver.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

/**
 * 中国省份碳排放总量数据访问Mapper
 */
@Mapper
public interface ChinaProvincialTotalCarbonMapper {
    
    /**
     * 查询中国省份碳排放总量数据
     */
    @Select("SELECT * FROM dwd_china_provincial_total_carbon_2024")
    List<Map<String, Object>> selectAll();
}