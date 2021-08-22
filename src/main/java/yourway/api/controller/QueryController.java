package yourway.api.controller;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import models.UserQuery;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import settings.Settings;
import utils.UtilKafka;

import javax.validation.Valid;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

@RestController
@RequestMapping("/api/v1")
public class QueryController {

    private ArrayList<UserQuery> getLatestMessageQuery() {
        Properties propsConsumerQuery = UtilKafka.createConsumer("userQuery");
        ConsumerRecord<String, String> latestMessage = UtilKafka.getLatestMessage(propsConsumerQuery, Settings.TOPIC_USER_QUERY);
        Gson gson = new Gson();
        Type type = new TypeToken<ArrayList<UserQuery>>() {
        }.getType();
        return gson.fromJson(latestMessage.value(), type);
    }

    @GetMapping("/")
    public ResponseEntity<Map<String, Object>> getDefault() {
        HashMap<String, Object> response = new HashMap<>();
        response.put("status", "ok");
        response.put("message", "Hello from Yourway!");
        return ResponseEntity.ok().body(response);
    }

    @GetMapping("/query")
    public ResponseEntity<ArrayList<UserQuery>> getAllQuery() {
        ArrayList<UserQuery> allQuery = getLatestMessageQuery();
        return ResponseEntity.ok().body(allQuery);
    }

    @GetMapping("/query/{queryId}")
    public ResponseEntity<UserQuery> getQuery(@PathVariable(value = "queryId") int queryId) {
        ArrayList<UserQuery> allQuery = getLatestMessageQuery();
        UserQuery response = null;
        for (UserQuery userQuery : allQuery)
            if (userQuery.getId() == queryId) {
                response = userQuery;
            }
        if (response != null) {
            return ResponseEntity.ok().body(response);
        }
        return ResponseEntity.ok().body(null);
    }

    @PostMapping("/query")
    public Map<String, Object> createUser(@Valid @RequestBody UserQuery query) throws Exception {
        HashMap<String, Object> response = new HashMap<>();
        response.put("status", "ok");
        Properties properties = UtilKafka.createProducer("KafkaProducer");
        UtilKafka.sendMessageToKafka(properties, Settings.TOPIC_SET_USER_QUERY, "setQuery", query.toStringJson());
        return response;
    }

    @DeleteMapping("/query/{queryId}")
    public Map<String, Boolean> deleteQuery(@PathVariable(value = "queryId") int queryId) throws Exception {
        Map<String, Boolean> response = new HashMap<>();
        response.put("deleted", Boolean.TRUE);
        Properties properties = UtilKafka.createProducer("KafkaProducer");
        UserQuery deleteQuery = new UserQuery(queryId, null, null, null, null, null, null);
        UtilKafka.sendMessageToKafka(properties, Settings.TOPIC_SET_USER_QUERY, "setQuery", deleteQuery.toStringJson());
        return response;
    }
}
