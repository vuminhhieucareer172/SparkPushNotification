package yourway.api.controller;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import models.JsonQuery;
import models.UserQuery;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import settings.Settings;
import utils.UtilKafka;

import javax.validation.Valid;
import java.lang.reflect.Type;
import java.util.*;

@CrossOrigin(maxAge = 3600)
@RestController
@RequestMapping(value = "/api/v1", produces = "application/json;charset=UTF-8")
public class QueryController {
    private final Gson gson = new Gson();

    private JsonQuery getLatestMessageQuery() {
        Properties propsConsumerQuery = UtilKafka.createConsumer("userQuery");
        ConsumerRecord<String, String> latestMessage = UtilKafka.getLatestMessage(propsConsumerQuery, Settings.TOPIC_USER_QUERY);
        System.out.println(latestMessage.value());
        Gson gson = new Gson();
        Type type = new TypeToken<JsonQuery>() {
        }.getType();
        return gson.fromJson(latestMessage.value(), type);
    }

    @GetMapping("/")
    public ResponseEntity<String> getDefault() {
        return new ResponseEntity<>("Hello from Yourway!", HttpStatus.OK);
    }

    @GetMapping("/query")
    public ResponseEntity<JsonQuery> getAllQuery() {
        JsonQuery allQuery = getLatestMessageQuery();
        return ResponseEntity.ok().body(allQuery);
    }

    @GetMapping("/query/{userId}")
    public ResponseEntity<HashMap<String, HashMap<String, Object>>> getQuery(@PathVariable(value = "userId") int userId) {
        JsonQuery allQuery = getLatestMessageQuery();
        System.out.println(allQuery);
        if (!allQuery.containsKey(String.valueOf(userId))) {
            HashMap<String, HashMap<String, Object>> result = new HashMap<>();
            return ResponseEntity.ok().body(result);
        }
        HashMap<String, HashMap<String, Object>> response = allQuery.get(String.valueOf(userId));
        return ResponseEntity.ok().body(response);
    }

    @PostMapping("/query")
    public ResponseEntity<Map<String, Object>> createUser(@Valid @RequestBody HashMap<String, Object> query) throws Exception {
        HashMap<String, HashMap<String, HashMap<String, Object>>> data = new HashMap<>();
        HashMap<String, HashMap<String, Object>> infoQuery = new HashMap<>();
        System.out.println(query);
        UserQuery userQuery = UserQuery.fromJson(query);
        infoQuery.put(String.valueOf(userQuery.getUserId()), userQuery.toJson());
        data.put(String.valueOf(userQuery.getUserId()), infoQuery);
        Properties properties = UtilKafka.createProducer("KafkaProducer");
        UtilKafka.sendMessageToKafka(properties, Settings.TOPIC_SET_USER_QUERY, String.valueOf(userQuery.getUserId()),
                gson.toJson(data));

        HashMap<String, Object> response = new HashMap<>();
        response.put("status", "ok");
        return ResponseEntity.ok().body(response);
    }

    @DeleteMapping("/query/{userId}/{queryId}")
    public Map<String, Boolean> deleteQuery(@PathVariable(value = "userId") int userId,
                                            @PathVariable(value = "queryId") String queryId) throws Exception {
        HashMap<String, HashMap<String, Object>> data = new HashMap<>();
        HashMap<String, Object> temp = new HashMap<>();
        UserQuery deleteQuery = new UserQuery(userId);
        temp.put(queryId, deleteQuery.toJson());
        data.put(String.valueOf(userId), temp);
        Properties properties = UtilKafka.createProducer("KafkaProducer");
        UtilKafka.sendMessageToKafka(properties, Settings.TOPIC_SET_USER_QUERY, String.valueOf(userId), gson.toJson(data));

        Map<String, Boolean> response = new HashMap<>();
        response.put("deleted", Boolean.TRUE);
        return response;
    }
}
