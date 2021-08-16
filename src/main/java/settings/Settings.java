package settings;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Settings {
    public static final String CHECKPOINT_PATH = "checkpoint";
    public static final String KAFKA_URI = "localhost:9092";
    public static final String TOPIC_JOB = "jobYourway";
    public static final String TOPIC_USER = "userId";
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
            "id",
            "company_address",
            "salary",
            "age",
            "education_level",
            "job_attribute",
            "year_experiences"
            ));
//    public static final Map<String, Integer> DICT_MIN_AGE =  {
//        "Dưới 18": 0,
//                "18-30": 18,
//                "30-40": 30,
//                "40-50": 40,
//                "50-60": 50,
//                "Trên 60": 60
//    };
//public static final Map<String, Integer> DICT_MAX_AGE = {
//        "Dưới 18": 18,
//                "18-30": 30,
//                "30-40": 40,
//                "40-50": 50,
//                "50-60": 60,
//                "Trên 60": 200
//    };
//    public static final String EXAMPLE_FILE_QUERY = "data/user_query.csv";
}
