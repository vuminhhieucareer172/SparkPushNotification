package yourway.api.controller;

import models.Job;
import org.springframework.web.bind.annotation.*;
import settings.Settings;
import utils.UtilKafka;

import javax.validation.Valid;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

@CrossOrigin(maxAge = 3600)
@RestController
@RequestMapping("/api/v1")
public class JobController {
    @PostMapping("/job")
    public Map<String, Object> createUser(@Valid @RequestBody Job job) throws Exception {
        HashMap<String, Object> response = new HashMap<>();
        response.put("status", "ok");
        Properties properties = UtilKafka.createProducer("KafkaProducer");
        UtilKafka.sendMessageToKafka(properties, Settings.TOPIC_JOB, String.valueOf(job.getId()), job.toStringJson());
        return response;
    }
}
