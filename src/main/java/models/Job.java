package models;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.Serializable;
import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.Map;
import java.util.SortedMap;
import java.util.TreeMap;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.SortedMap;
import java.util.TreeMap;

public class Job {
    private int id;
    private String application_deadline;
    private String company_address;
    private String company_name;
    private String job_benefits;
    private String job_descriptions;
    private String job_formality;
    private String job_other_info;
    private String job_requirements;
    private String job_trial_period;
    private String salary;
    private String skills;
    private String title;
    private String url;
    private String ages;
    private String education_level;
    private String genders;
    private String domains;
    private String position;
    private String job_attribute;
    private String locations;
    private String time;
    private String year_experiences;
    private String position_number;

    public Job() {
    }

    public Job(int id, String application_deadline, String company_address, String company_name, String job_benefits, String job_descriptions, String job_formality, String job_other_info, String job_requirements, String job_trial_period, String salary, String skills, String title, String url, String ages, String education_level, String genders, String domains, String position, String job_attribute, String locations, String time, String year_experiences, String position_number) {
        this.id = id;
        this.application_deadline = application_deadline;
        this.company_address = company_address;
        this.company_name = company_name;
        this.job_benefits = job_benefits;
        this.job_descriptions = job_descriptions;
        this.job_formality = job_formality;
        this.job_other_info = job_other_info;
        this.job_requirements = job_requirements;
        this.job_trial_period = job_trial_period;
        this.salary = salary;
        this.skills = skills;
        this.title = title;
        this.url = url;
        this.ages = ages;
        this.education_level = education_level;
        this.genders = genders;
        this.domains = domains;
        this.position = position;
        this.job_attribute = job_attribute;
        this.locations = locations;
        this.time = time;
        this.year_experiences = year_experiences;
        this.position_number = position_number;
    }

    public int getId() {
        return id;
    }

    public String getApplication_deadline() {
        return application_deadline;
    }

    public String getCompany_address() {
        return company_address;
    }

    public String getCompany_name() {
        return company_name;
    }

    public String getJob_benefits() {
        return job_benefits;
    }

    public String getJob_descriptions() {
        return job_descriptions;
    }

    public String getJob_formality() {
        return job_formality;
    }

    public String getJob_other_info() {
        return job_other_info;
    }

    public String getJob_requirements() {
        return job_requirements;
    }

    public String getJob_trial_period() {
        return job_trial_period;
    }

    public String getSalary() {
        return salary;
    }

    public String getSkills() {
        return skills;
    }

    public String getTitle() {
        return title;
    }

    public String getUrl() {
        return url;
    }

    public String getAges() {
        return ages;
    }

    public String getEducation_level() {
        return education_level;
    }

    public String getGenders() {
        return genders;
    }

    public String getDomains() {
        return domains;
    }

    public String getPosition() {
        return position;
    }

    public String getJob_attribute() {
        return job_attribute;
    }

    public String getLocations() {
        return locations;
    }

    public String getTime() {
        return time;
    }

    public String getYear_experiences() {
        return year_experiences;
    }

    public String getPosition_number() {
        return position_number;
    }

    public String toStringJson() {
        SortedMap<String, Object> map = new TreeMap<>();
        map.put("id", id);
        map.put("application_deadline", application_deadline);
        map.put("company_address", company_address);
        map.put("company_name", company_name);
        map.put("job_benefits", job_benefits);
        map.put("job_descriptions", job_descriptions);
        map.put("job_formality", job_formality);
        map.put("job_other_info", job_other_info);
        map.put("job_requirements", job_requirements);
        map.put("job_trial_period", job_trial_period);
        map.put("salary", salary);
        map.put("skills", skills);
        map.put("title", title);
        map.put("url", url);
        map.put("ages", ages);
        map.put("education_level", education_level);
        map.put("genders", genders);
        map.put("domains", domains);
        map.put("position", position);
        map.put("job_attribute", job_attribute);
        map.put("locations", locations);
        map.put("time", time);
        map.put("year_experiences", year_experiences);
        map.put("position_number", position_number);
        Gson gson = new Gson();
        Type gsonType = new TypeToken<HashMap<String, Object>>(){}.getType();
        return gson.toJson(map,gsonType);
    }

    @Override
    public String toString() {
        return "Job{" +
                "id=" + id +
                ", application_deadline='" + application_deadline + '\'' +
                ", company_address='" + company_address + '\'' +
                ", company_name='" + company_name + '\'' +
                ", job_benefits='" + job_benefits + '\'' +
                ", job_descriptions='" + job_descriptions + '\'' +
                ", job_formality='" + job_formality + '\'' +
                ", job_other_info='" + job_other_info + '\'' +
                ", job_requirements='" + job_requirements + '\'' +
                ", job_trial_period='" + job_trial_period + '\'' +
                ", salary='" + salary + '\'' +
                ", skills='" + skills + '\'' +
                ", title='" + title + '\'' +
                ", url='" + url + '\'' +
                ", ages='" + ages + '\'' +
                ", education_level='" + education_level + '\'' +
                ", genders='" + genders + '\'' +
                ", domains='" + domains + '\'' +
                ", position='" + position + '\'' +
                ", job_attribute='" + job_attribute + '\'' +
                ", locations='" + locations + '\'' +
                ", time='" + time + '\'' +
                ", year_experiences='" + year_experiences + '\'' +
                ", position_number='" + position_number + '\'' +
                '}';
    }
}
