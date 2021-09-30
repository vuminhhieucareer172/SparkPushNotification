package com.yourway.alert.web.rest;

import com.yourway.alert.domain.Job;
import com.yourway.alert.streaming.settings.Settings;
import com.yourway.alert.utils.UtilKafka;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

@CrossOrigin(maxAge = 3600)
@RestController
@RequestMapping("/api")
public class JobResource {
    @PostMapping("/job")
    public Map<String, Object> createUser(@Valid @RequestBody Job job) throws Exception {
        HashMap<String, Object> response = new HashMap<>();
        response.put("status", "ok");
        Properties properties = UtilKafka.createProducer("KafkaProducer");
        UtilKafka.sendMessageToKafka(properties, Settings.TOPIC_JOB, String.valueOf(job.getId()), job.toStringJson());
        return response;
    }
}
