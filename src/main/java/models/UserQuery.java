package models;

import com.google.gson.Gson;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import java.io.Serializable;
import java.util.HashMap;

@Entity
public class UserQuery implements Serializable {
    @Id
    @GeneratedValue(strategy= GenerationType.AUTO)
    private Integer queryId;
    private Integer userId;
    private String name;
    private String companyAddress;
    private String jobRole;
    private Integer age;
    private String salary;
    private Double yearExperiences;
    private String educationLevel;
    private String jobAttribute;
    private Boolean isDelete;
    private String contact;

    public UserQuery(Integer userId,
                     String name,
                     String companyAddress,
                     String jobRole,
                     Integer age,
                     String salary,
                     Double yearExperiences,
                     String educationLevel,
                     String jobAttribute,
                     String contact) {
        this.userId = userId;
        this.name = name;
        this.companyAddress = companyAddress;
        this.jobRole = jobRole;
        this.age = age;
        this.salary = salary;
        this.yearExperiences = yearExperiences;
        this.educationLevel = educationLevel;
        this.jobAttribute = jobAttribute;
        this.isDelete = Boolean.FALSE;
        this.contact = contact;
    }

    public UserQuery() {

    }

    public Integer getQueryId() {
        return queryId;
    }

    public Integer getUserId() {
        return userId;
    }

    public String getName() {
        return name;
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

    public String getContact() {
        return contact;
    }

    public static UserQuery fromJson(HashMap<String, Object> map) {
        assert map.containsKey("userId") && map.containsKey("jobRole");
        Gson gson = new Gson();
        return new UserQuery((int) map.get("userId"),
                (String) map.get("name"),
                (String) map.get("companyAddress"),
                (String) map.get("jobRole"),
                (Integer) map.get("age"),
                (String) map.get("salary"),
                Double.valueOf(map.get("yearExperiences").toString()),
                (String) map.get("educationLevel"),
                (String) map.get("jobAttribute"),
                gson.toJson(map.get("contact")));
    }

    public HashMap<String, Object> toJson() {
        HashMap<String, Object> map = new HashMap<>();
        map.put("queryId", queryId);
        map.put("userId", userId);
        map.put("name", name);
        map.put("companyAddress", companyAddress);
        map.put("jobRole", jobRole);
        map.put("age", age);
        map.put("salary", salary);
        map.put("yearExperiences", yearExperiences);
        map.put("educationLevel", educationLevel);
        map.put("jobAttribute", jobAttribute);
        map.put("isDelete", isDelete);
        map.put("contact", contact);
        return map;
    }

    @Override
    public String toString() {
        return "UserQuery{" +
                "queryId='" + queryId +
                ", userId=" + userId +
                ", name='" + name + '\'' +
                ", companyAddress='" + companyAddress + '\'' +
                ", jobRole=" + jobRole +
                ", age=" + age +
                ", salary='" + salary + '\'' +
                ", yearExperiences='" + yearExperiences + '\'' +
                ", educationLevel='" + educationLevel + '\'' +
                ", jobAttribute='" + jobAttribute + '\'' +
                ", isDelete='" + isDelete + '\'' +
                ", contact='" + contact + '\'' +
                '}';
    }
}
