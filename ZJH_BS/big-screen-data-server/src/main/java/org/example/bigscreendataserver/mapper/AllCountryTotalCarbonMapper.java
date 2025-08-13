package org.example.bigscreendataserver.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

/**
 * 全球国家碳排放总量数据访问Mapper
 */
@Mapper
public interface AllCountryTotalCarbonMapper {
    
    /**
     * 查询全球国家碳排放总量数据
     */
    @Select("SELECT * FROM dwd_all_country_Total_carbon_2024")
    List<Map<String, Object>> selectAll();
}
