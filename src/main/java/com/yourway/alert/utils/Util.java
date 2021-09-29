package com.yourway.alert.utils;

import com.yourway.alert.streaming.models.JsonQuery;
import com.yourway.alert.streaming.settings.Database;

import java.sql.*;
import java.util.HashMap;

public class Util {

    public static JsonQuery loadDataFromMySQL() {
        JsonQuery queries = new JsonQuery();

        try {
            Connection conn = DriverManager.getConnection(Database.DB_URL, Database.DB_USERNAME, Database.DB_PASSWORD);

            Statement stmt = conn.createStatement();
            String sql = "SELECT * FROM user_query";
            ResultSet rs = stmt.executeQuery(sql);
            while (rs.next()) {
                HashMap<String, Object> hashMap = new HashMap<>();
                hashMap.put("query_id", rs.getInt("query_id"));
                hashMap.put("user_id", rs.getInt("user_id"));
                hashMap.put("name", rs.getString("name"));
                hashMap.put("company_address", rs.getString("company_address"));
                hashMap.put("job_role", rs.getString("job_role"));
                hashMap.put("age", rs.getInt("age"));
                hashMap.put("salary", rs.getString("salary"));
                hashMap.put("year_experiences", rs.getFloat("year_experiences"));
                hashMap.put("education_level", rs.getString("education_level"));
                hashMap.put("job_attribute", rs.getString("job_attribute"));
                hashMap.put("is_delete", rs.getBoolean("is_delete"));
                hashMap.put("contact", rs.getString("contact"));

                HashMap<String, HashMap<String, Object>> hashMapHashMap = new HashMap<>();
                hashMapHashMap.put(String.valueOf(rs.getInt("query_id")), hashMap);

                queries.put(String.valueOf(rs.getInt("user_id")), hashMapHashMap);
            }
        } catch (SQLException e) {
            System.out.println(e.getMessage());
            e.printStackTrace();
        }
        return queries;
    }
}
