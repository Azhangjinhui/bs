package org.example.bigscreendataserver;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


@SpringBootApplication
@MapperScan("org.example.bigscreendataserver.mapper")
public class BigScreenDataServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(BigScreenDataServerApplication.class, args);
    }
}