package models;

import org.apache.spark.sql.sources.In;
import scala.Int;

import java.io.Serializable;
import java.util.HashMap;
import java.util.List;

public class UserQuery implements Serializable {
    private final int userId;
    private final String name;
    private final String companyAddress;
    private final String jobRole;
    private final Integer age;
    private final String salary;
    private final Double yearExperiences;
    private final String educationLevel;
    private final String jobAttribute;
    private final Boolean isDelete;
    private final List<HashMap<String, String>> contact;

    public UserQuery(int userId) {
        this.userId = userId;
        this.isDelete = Boolean.TRUE;
        this.name = null;
        this.companyAddress = null;
        this.jobRole = null;
        this.age = null;
        this.salary = null;
        this.yearExperiences = null;
        this.educationLevel = null;
        this.jobAttribute = null;
        this.contact = null;
    }

    public UserQuery(int userId,
                     String name,
                     String companyAddress,
                     String jobRole,
                     Integer age,
                     String salary,
                     Double yearExperiences,
                     String educationLevel,
                     String jobAttribute,
                     List<HashMap<String, String>> contact) {
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

    public int getUserId() {
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

    public List<HashMap<String, String>> getContact() {
        return contact;
    }

    public static UserQuery fromJson(HashMap<String, Object> map) {
        assert map.containsKey("userId") && map.containsKey("jobRole");
        return new UserQuery((int) map.get("userId"),
                (String) map.get("name"),
                (String) map.get("companyAddress"),
                (String) map.get("jobRole"),
                (Integer) map.get("age"),
                (String) map.get("salary"),
                Double.valueOf(map.get("yearExperiences").toString()),
                (String) map.get("educationLevel"),
                (String) map.get("jobAttribute"),
                (List<HashMap<String, String>>) map.get("contact"));
    }

    public HashMap<String, Object> toJson() {
        HashMap<String, Object> map = new HashMap<>();
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
                "userId=" + userId +
                ", name='" + name + '\'' +
                ", company_address='" + companyAddress + '\'' +
                ", job_role=" + jobRole +
                ", age=" + age +
                ", salary='" + salary + '\'' +
                ", year_experiences='" + yearExperiences + '\'' +
                ", education_level='" + educationLevel + '\'' +
                ", job_attribute='" + jobAttribute + '\'' +
                ", is_delete='" + isDelete + '\'' +
                ", contact='" + contact + '\'' +
                '}';
    }
}
