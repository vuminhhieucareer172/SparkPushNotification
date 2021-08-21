package yourway.api.controller;

import models.Job;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import settings.Settings;
import utils.UtilKafka;

import javax.validation.Valid;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

@RestController
@RequestMapping("/api/v1")
public class JobController {
    @PostMapping("/job")
    public Map<String, Object> createUser(@Valid @RequestBody Job job) throws Exception {
        HashMap<String, Object> response = new HashMap<>();
        response.put("status", "ok");
        Properties properties = UtilKafka.createProducer("KafkaProducer");
        UtilKafka.sendMessageToKafka(properties, Settings.TOPIC_JOB, String.valueOf(job.getId()), job.toMap().toString());
        return response;
    }
}
