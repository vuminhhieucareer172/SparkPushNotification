package models;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.Serializable;
import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.SortedMap;
import java.util.TreeMap;

public class UserQuery implements Serializable {
    private int id;
    private String company_address;
    private Integer age;
    private String salary;
    private String year_experiences;
    private String education_level;
    private String job_attribute;

    public UserQuery() {
    }

    public UserQuery(int id, String company_address, Integer age, String salary, String year_experiences, String education_level, String job_attribute) {
        this.id = id;
        this.company_address = company_address;
        this.age = age;
        this.salary = salary;
        this.year_experiences = year_experiences;
        this.education_level = education_level;
        this.job_attribute = job_attribute;
    }

    public int getId() {
        return id;
    }

    public String getCompany_address() {
        return company_address;
    }

    public Integer getAge() {
        return age;
    }

    public String getSalary() {
        return salary;
    }

    public String getYear_experiences() {
        return year_experiences;
    }

    public String getEducation_level() {
        return education_level;
    }

    public String getJob_attribute() {
        return job_attribute;
    }

    public String toStringJson() {
        SortedMap<String, Object> map = new TreeMap<>();
        map.put("id", id);
        map.put("company_address", company_address);
        map.put("age", age);
        map.put("salary", salary);
        map.put("year_experiences", year_experiences);
        map.put("education_level", education_level);
        map.put("job_attribute", job_attribute);
        Gson gson = new Gson();
        Type gsonType = new TypeToken<HashMap<String, Object>>(){}.getType();
        return gson.toJson(map,gsonType);
    }

    @Override
    public String toString() {
        return "UserQuery{" +
                "id=" + id +
                ", company_address='" + company_address + '\'' +
                ", age=" + age +
                ", salary='" + salary + '\'' +
                ", year_experiences='" + year_experiences + '\'' +
                ", education_level='" + education_level + '\'' +
                ", job_attribute='" + job_attribute + '\'' +
                '}';
    }
}
