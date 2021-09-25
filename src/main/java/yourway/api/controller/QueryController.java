package yourway.api.controller;

import com.google.gson.Gson;
import models.UserQuery;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import settings.Settings;
import utils.UtilKafka;
import yourway.api.repository.UserQueryRepository;

import javax.validation.Valid;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

@CrossOrigin(maxAge = 3600)
@RestController
@RequestMapping(value = "/api/v1", produces = "application/json;charset=UTF-8")
public class QueryController {
    private final Gson gson;
    private final UserQueryRepository userQueryRepository;

    public QueryController(UserQueryRepository userQueryRepository) {
        this.userQueryRepository = userQueryRepository;
        this.gson = new Gson();
    }

    @GetMapping("/")
    public ResponseEntity<String> getDefault() {
        return new ResponseEntity<>("Hello from Yourway!", HttpStatus.OK);
    }

    @GetMapping("/query")
    public Iterable<UserQuery> getAllQuery() {
        try {
            return userQueryRepository.findAll();
        } catch (java.lang.NullPointerException e) {
            return null;
        }
    }

    @GetMapping("/query/{userId}")
    public ResponseEntity<List<UserQuery>> getQuery(@PathVariable(value = "userId") Integer userId) {
        try {
            List<UserQuery> response = userQueryRepository.findAllByUserId(userId);
            return ResponseEntity.ok().body(response);
        } catch (java.lang.NullPointerException e) {
            return null;
        }
    }

    @PostMapping("/query")
    public ResponseEntity<Map<String, Object>> createUser(@Valid @RequestBody HashMap<String, Object> query) throws Exception {
        // process input
        HashMap<String, HashMap<String, HashMap<String, Object>>> data = new HashMap<>();
        HashMap<String, HashMap<String, Object>> infoQuery = new HashMap<>();
        UserQuery userQuery = UserQuery.fromJson(query);

        // save to database
        UserQuery newQuery = userQueryRepository.save(userQuery);

        // save to kafka
        infoQuery.put(String.valueOf(newQuery.getUserId()), newQuery.toJson());
        data.put(String.valueOf(newQuery.getUserId()), infoQuery);
        Properties properties = UtilKafka.createProducer("KafkaProducer");
        UtilKafka.sendMessageToKafka(properties, Settings.TOPIC_SET_USER_QUERY, String.valueOf(newQuery.getUserId()),
                gson.toJson(data));

        // return status
        HashMap<String, Object> response = new HashMap<>();
        response.put("status", "ok");
        return ResponseEntity.ok().body(response);
    }

    @DeleteMapping("/query/{userId}/{queryId}")
    public Map<String, Boolean> deleteQuery(@PathVariable(value = "userId") Integer userId,
                                            @PathVariable(value = "queryId") Integer queryId) throws Exception {
        // process input
        HashMap<Integer, HashMap<Integer, Object>> data = new HashMap<>();
        HashMap<Integer, Object> temp = new HashMap<>();
        UserQuery deleteQuery = userQueryRepository.findByQueryId(queryId);

        // send message delete to kafka
        temp.put(queryId, deleteQuery.toJson());
        data.put(userId, temp);
        Properties properties = UtilKafka.createProducer("KafkaProducer");
        UtilKafka.sendMessageToKafka(properties, Settings.TOPIC_SET_USER_QUERY, String.valueOf(userId), gson.toJson(data));

        // delete in database
        userQueryRepository.delete(deleteQuery);

        // return status
        Map<String, Boolean> response = new HashMap<>();
        response.put("deleted", Boolean.TRUE);
        return response;
    }
}
