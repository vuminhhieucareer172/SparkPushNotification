package models;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.Serializable;
import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.List;
import java.util.SortedMap;
import java.util.TreeMap;

public class UserQuery implements Serializable {
    private int id;
    private String companyAddress;
    private String jobRole;
    private Integer age;
    private String salary;
    private Double yearExperiences;
    private String educationLevel;
    private String jobAttribute;
    private List<HashMap<String, String>> contact;

    public UserQuery() {
    }

    public UserQuery(int id, String companyAddress, String jobRole, Integer age, String salary, Double yearExperiences, String educationLevel, String jobAttribute, List<HashMap<String, String>> contact) {
        this.id = id;
        this.companyAddress = companyAddress;
        this.jobRole = jobRole;
        this.age = age;
        this.salary = salary;
        this.yearExperiences = yearExperiences;
        this.educationLevel = educationLevel;
        this.jobAttribute = jobAttribute;
        this.contact = contact;
    }

    public int getId() {
        return id;
    }

    public String getCompanyAddress() {
        return companyAddress;
    }

    public String getJobRole() {
        return jobRole;
    }

    public Integer getAge() {
        return age;
    }

    public String getSalary() {
        return salary;
    }

    public Double getYearExperiences() {
        return yearExperiences;
    }

    public String getEducationLevel() {
        return educationLevel;
    }

    public String getJobAttribute() {
        return jobAttribute;
    }

    public List<HashMap<String, String>> getContact() {
        return contact;
    }

    public String toStringJson() {
        SortedMap<String, Object> map = new TreeMap<>();
        map.put("id", id);
        map.put("companyAddress", companyAddress);
        map.put("jobRole", jobRole);
        map.put("age", age);
        map.put("salary", salary);
        map.put("yearExperiences", yearExperiences);
        map.put("educationLevel", educationLevel);
        map.put("jobAttribute", jobAttribute);
        map.put("contact", contact);
        Gson gson = new Gson();
        Type gsonType = new TypeToken<HashMap<String, Object>>() {
        }.getType();
        return gson.toJson(map, gsonType);
    }

    @Override
    public String toString() {
        return "UserQuery{" +
                "id=" + id +
                ", company_address='" + companyAddress + '\'' +
                ", job_role=" + jobRole +
                ", age=" + age +
                ", salary='" + salary + '\'' +
                ", year_experiences='" + yearExperiences + '\'' +
                ", education_level='" + educationLevel + '\'' +
                ", job_attribute='" + jobAttribute + '\'' +
                ", contact='" + contact + '\'' +
                '}';
    }
}
