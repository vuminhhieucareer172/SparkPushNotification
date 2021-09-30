package com.yourway.alert.domain;

import com.google.gson.Gson;
import com.yourway.alert.domain.enumeration.EducationLevel;
import com.yourway.alert.domain.enumeration.TypeQuery;
import java.io.Serializable;
import java.time.Duration;
import java.util.HashMap;
import javax.persistence.*;
import javax.validation.constraints.*;

/**
 * A Query.
 */
@Entity
@Table(name = "query")
public class Query implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @NotNull
    @Column(name = "user_id", nullable = false)
    private Integer userId;

    @NotNull
    @Size(max = 50)
    @Column(name = "name", length = 50, nullable = false)
    private String name;

    @NotNull
    @Enumerated(EnumType.STRING)
    @Column(name = "type_query", nullable = false)
    private TypeQuery typeQuery;

    @Column(name = "company_address")
    private String companyAddress;

    @NotNull
    @Column(name = "job_role", nullable = false)
    private String jobRole;

    @NotNull
    @Min(value = 0)
    @Column(name = "age", nullable = false)
    private Integer age;

    @Min(value = 0L)
    @Column(name = "salary")
    private Long salary;

    @DecimalMin(value = "0.0")
    @Column(name = "year_experiences")
    private Float yearExperiences;

    @Enumerated(EnumType.STRING)
    @Column(name = "education_level")
    private EducationLevel educationLevel;

    @Column(name = "job_attribute")
    private String jobAttribute;

    @Lob
    @Column(name = "contact", nullable = false)
    private String contact;

    @Column(name = "group_by")
    private String groupBy;

    @Column(name = "slide_window")
    private Duration slideWindow;

    public Query() {

    }

    public Query(Integer userId,
                 String name,
                 String companyAddress,
                 String jobRole,
                 Integer age,
                 Long salary,
                 Float yearExperiences,
                 EducationLevel educationLevel,
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
        this.contact = contact;
    }

    // jhipster-needle-entity-add-field - JHipster will add fields here

    public Long getId() {
        return this.id;
    }

    public Query id(Long id) {
        this.setId(id);
        return this;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Integer getUserId() {
        return this.userId;
    }

    public Query userId(Integer userId) {
        this.setUserId(userId);
        return this;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public String getName() {
        return this.name;
    }

    public Query name(String name) {
        this.setName(name);
        return this;
    }

    public void setName(String name) {
        this.name = name;
    }

    public TypeQuery getTypeQuery() {
        return this.typeQuery;
    }

    public Query typeQuery(TypeQuery typeQuery) {
        this.setTypeQuery(typeQuery);
        return this;
    }

    public void setTypeQuery(TypeQuery typeQuery) {
        this.typeQuery = typeQuery;
    }

    public String getCompanyAddress() {
        return this.companyAddress;
    }

    public Query companyAddress(String companyAddress) {
        this.setCompanyAddress(companyAddress);
        return this;
    }

    public void setCompanyAddress(String companyAddress) {
        this.companyAddress = companyAddress;
    }

    public String getJobRole() {
        return this.jobRole;
    }

    public Query jobRole(String jobRole) {
        this.setJobRole(jobRole);
        return this;
    }

    public void setJobRole(String jobRole) {
        this.jobRole = jobRole;
    }

    public Integer getAge() {
        return this.age;
    }

    public Query age(Integer age) {
        this.setAge(age);
        return this;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Long getSalary() {
        return this.salary;
    }

    public Query salary(Long salary) {
        this.setSalary(salary);
        return this;
    }

    public void setSalary(Long salary) {
        this.salary = salary;
    }

    public Float getYearExperiences() {
        return this.yearExperiences;
    }

    public Query yearExperiences(Float yearExperiences) {
        this.setYearExperiences(yearExperiences);
        return this;
    }

    public void setYearExperiences(Float yearExperiences) {
        this.yearExperiences = yearExperiences;
    }

    public EducationLevel getEducationLevel() {
        return this.educationLevel;
    }

    public Query educationLevel(EducationLevel educationLevel) {
        this.setEducationLevel(educationLevel);
        return this;
    }

    public void setEducationLevel(EducationLevel educationLevel) {
        this.educationLevel = educationLevel;
    }

    public String getJobAttribute() {
        return this.jobAttribute;
    }

    public Query jobAttribute(String jobAttribute) {
        this.setJobAttribute(jobAttribute);
        return this;
    }

    public void setJobAttribute(String jobAttribute) {
        this.jobAttribute = jobAttribute;
    }

    public String getContact() {
        return this.contact;
    }

    public Query contact(String contact) {
        this.setContact(contact);
        return this;
    }

    public void setContact(String contact) {
        this.contact = contact;
    }

    public String getGroupBy() {
        return this.groupBy;
    }

    public Query groupBy(String groupBy) {
        this.setGroupBy(groupBy);
        return this;
    }

    public void setGroupBy(String groupBy) {
        this.groupBy = groupBy;
    }

    public Duration getSlideWindow() {
        return this.slideWindow;
    }

    public Query slideWindow(Duration slideWindow) {
        this.setSlideWindow(slideWindow);
        return this;
    }

    public void setSlideWindow(Duration slideWindow) {
        this.slideWindow = slideWindow;
    }

    // jhipster-needle-entity-add-getters-setters - JHipster will add getters and setters here

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (!(o instanceof Query)) {
            return false;
        }
        return id != null && id.equals(((Query) o).id);
    }

    @Override
    public int hashCode() {
        // see https://vladmihalcea.com/how-to-implement-equals-and-hashcode-using-the-jpa-entity-identifier/
        return getClass().hashCode();
    }

    public static Query fromJson(HashMap<String, Object> map) {
        assert map.containsKey("userId") && map.containsKey("jobRole");
        Gson gson = new Gson();
        return new Query((int) map.get("userId"),
            (String) map.get("name"),
            (String) map.get("companyAddress"),
            (String) map.get("jobRole"),
            (Integer) map.get("age"),
            (Long) map.get("salary"),
            Float.valueOf(map.get("yearExperiences").toString()),
            (EducationLevel) map.get("educationLevel"),
            (String) map.get("jobAttribute"),
            gson.toJson(map.get("contact")));
    }

    public HashMap<String, Object> toJson() {
        HashMap<String, Object> map = new HashMap<>();
        map.put("id", id);
        map.put("userId", userId);
        map.put("name", name);
        map.put("companyAddress", companyAddress);
        map.put("jobRole", jobRole);
        map.put("age", age);
        map.put("salary", salary);
        map.put("yearExperiences", yearExperiences);
        map.put("educationLevel", educationLevel);
        map.put("jobAttribute", jobAttribute);
        map.put("contact", contact);
        map.put("groupBy", groupBy);
        map.put("slideWindow", slideWindow);
        map.put("typeQuery", typeQuery);
        return map;
    }

    // prettier-ignore
    @Override
    public String toString() {
        return "Query{" +
            "id=" + getId() +
            ", userId=" + getUserId() +
            ", name='" + getName() + "'" +
            ", typeQuery='" + getTypeQuery() + "'" +
            ", companyAddress='" + getCompanyAddress() + "'" +
            ", jobRole='" + getJobRole() + "'" +
            ", age=" + getAge() +
            ", salary=" + getSalary() +
            ", yearExperiences=" + getYearExperiences() +
            ", educationLevel='" + getEducationLevel() + "'" +
            ", jobAttribute='" + getJobAttribute() + "'" +
            ", contact='" + getContact() + "'" +
            ", groupBy='" + getGroupBy() + "'" +
            ", slideWindow='" + getSlideWindow() + "'" +
            "}";
    }
}
