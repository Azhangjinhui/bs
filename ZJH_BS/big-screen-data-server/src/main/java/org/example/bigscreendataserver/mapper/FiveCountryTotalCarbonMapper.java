package org.example.bigscreendataserver.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

/**
 * 五国碳排放总量历史数据访问Mapper
 */
@Mapper
public interface FiveCountryTotalCarbonMapper {
    
    /**
     * 查询五国碳排放总量历史数据
     */
    @Select("SELECT * FROM dwd_five_country_Total_carbon_2019_2024")
    List<Map<String, Object>> selectAll();
}