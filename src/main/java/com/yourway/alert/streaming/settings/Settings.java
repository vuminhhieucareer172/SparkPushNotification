package com.yourway.alert.streaming.settings;

import java.util.*;

public class Settings {
    public static final String CHECKPOINT_PATH = "checkpoint";
    public static final String KAFKA_URI = "localhost:9092";
    public static final String TOPIC_JOB = "jobYourway";
    public static final String TOPIC_USER = "userId";
    public static final String GROUP_ID_USER = "userId";
    public static final String TOPIC_SET_USER_QUERY = "setUserQuery";
    public static final String TOPIC_USER_QUERY = "userQuery";

    public static final List<String> FIELD_JOB = Collections.unmodifiableList(Arrays.asList(
        "id",
        "application_deadline",
        "company_address",
        "company_name",
        "job_benefits",
        "job_descriptions",
        "job_formality",
        "job_other_info",
        "job_requirements",
        "job_trial_period",
        "salary",
        "skills",
        "title",
        "url",
        "ages",
        "education_level",
        "genders",
        "domains",
        "position",
        "job_attribute",
        "locations",
        "time",
        "year_experiences",
        "position_number"
    ));
    public static final List<String> FIELD_QUERY = Collections.unmodifiableList(Arrays.asList(
        "queryId",
        "userId",
        "name",
        "typeQuery",
        "companyAddress",
        "jobRole",
        "age",
        "salary",
        "yearExperiences",
        "educationLevel",
        "jobAttribute",
        "contact",
        "groupBy",
        "window"
    ));
    public static final Map<String, Integer> DICT_MIN_AGE;

    static {
        Map<String, Integer> aMap = new HashMap<>();
        aMap.put("Dưới 18", 0);
        aMap.put("18-30", 18);
        aMap.put("30-40", 30);
        aMap.put("40-50", 40);
        aMap.put("50-60", 50);
        aMap.put("Trên 60", 60);
        DICT_MIN_AGE = Collections.unmodifiableMap(aMap);
    }

    public static final Map<String, Integer> DICT_MAX_AGE;

    static {
        Map<String, Integer> aMap = new HashMap<>();
        aMap.put("Dưới 18", 18);
        aMap.put("18-30", 30);
        aMap.put("30-40", 40);
        aMap.put("40-50", 50);
        aMap.put("50-60", 60);
        aMap.put("Trên 60", 200);
        DICT_MAX_AGE = Collections.unmodifiableMap(aMap);
    }
}
