package models;

import java.io.Serializable;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

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

    public void setId(int id) {
        this.id = id;
    }

    public String getCompanyAddress() {
        return company_address;
    }

    public void setCompanyAddress(String company_address) {
        this.company_address = company_address;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getSalary() {
        return salary;
    }

    public void setSalary(String salary) {
        this.salary = salary;
    }

    public String getYearExperiences() {
        return year_experiences;
    }

    public void setYearExperiences(String year_experiences) {
        this.year_experiences = year_experiences;
    }

    public String getEducationLevel() {
        return education_level;
    }

    public void setEducationLevel(String education_level) {
        this.education_level = education_level;
    }

    public String getJobAttribute() {
        return job_attribute;
    }

    public void setJobAttribute(String job_attribute) {
        this.job_attribute = job_attribute;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("id", id);
        map.put("company_address", company_address);
        map.put("age", age);
        map.put("salary", salary);
        map.put("year_experiences", year_experiences);
        map.put("education_level", education_level);
        map.put("job_attribute", job_attribute);
        return map;
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
