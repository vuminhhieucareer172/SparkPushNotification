package com.yourway.alert.web.rest;

import com.google.gson.Gson;
import com.yourway.alert.domain.Query;
import com.yourway.alert.repository.QueryRepository;
import com.yourway.alert.streaming.settings.Settings;
import com.yourway.alert.utils.UtilKafka;
import com.yourway.alert.web.rest.errors.BadRequestAlertException;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.*;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;
import tech.jhipster.web.util.HeaderUtil;
import tech.jhipster.web.util.PaginationUtil;
import tech.jhipster.web.util.ResponseUtil;

/**
 * REST controller for managing {@link com.yourway.alert.domain.Query}.
 */
@RestController
@RequestMapping("/api")
@Transactional
public class QueryResource {

    private final Logger log = LoggerFactory.getLogger(QueryResource.class);

    private static final String ENTITY_NAME = "query";

    private final Gson gson;

    @Value("${jhipster.clientApp.name}")
    private String applicationName;

    private final QueryRepository queryRepository;

    public QueryResource(QueryRepository queryRepository) {
        this.queryRepository = queryRepository;
        this.gson = new Gson();
    }

    /**
     * {@code POST  /queries} : Create a new query.
     *
     * @param query the query to create.
     * @return the {@link ResponseEntity} with status {@code 201 (Created)} and with body the new query, or with status {@code 400 (Bad Request)} if the query has already an ID.
     * @throws URISyntaxException if the Location URI syntax is incorrect.
     */
    @PostMapping("/queries")
    public ResponseEntity<Query> createQuery(@Valid @RequestBody Query query) throws URISyntaxException {
        log.debug("REST request to save Query : {}", query);
        if (query.getId() != null) {
            throw new BadRequestAlertException("A new query cannot already have an ID", ENTITY_NAME, "idexists");
        }
        Query result = queryRepository.save(query);
        return ResponseEntity
            .created(new URI("/api/queries/" + result.getId()))
            .headers(HeaderUtil.createEntityCreationAlert(applicationName, false, ENTITY_NAME, result.getId().toString()))
            .body(result);
    }

    /**
     * {@code PUT  /queries/:id} : Updates an existing query.
     *
     * @param id    the id of the query to save.
     * @param query the query to update.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and with body the updated query,
     * or with status {@code 400 (Bad Request)} if the query is not valid,
     * or with status {@code 500 (Internal Server Error)} if the query couldn't be updated.
     * @throws URISyntaxException if the Location URI syntax is incorrect.
     */
    @PutMapping("/queries/{id}")
    public ResponseEntity<Query> updateQuery(@PathVariable(value = "id", required = false) final Long id, @Valid @RequestBody Query query)
        throws URISyntaxException {
        log.debug("REST request to update Query : {}, {}", id, query);
        if (query.getId() == null) {
            throw new BadRequestAlertException("Invalid id", ENTITY_NAME, "idnull");
        }
        if (!Objects.equals(id, query.getId())) {
            throw new BadRequestAlertException("Invalid ID", ENTITY_NAME, "idinvalid");
        }

        if (!queryRepository.existsById(id)) {
            throw new BadRequestAlertException("Entity not found", ENTITY_NAME, "idnotfound");
        }

        Query result = queryRepository.save(query);
        return ResponseEntity
            .ok()
            .headers(HeaderUtil.createEntityUpdateAlert(applicationName, false, ENTITY_NAME, query.getId().toString()))
            .body(result);
    }

    /**
     * {@code PATCH  /queries/:id} : Partial updates given fields of an existing query, field will ignore if it is null
     *
     * @param id    the id of the query to save.
     * @param query the query to update.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and with body the updated query,
     * or with status {@code 400 (Bad Request)} if the query is not valid,
     * or with status {@code 404 (Not Found)} if the query is not found,
     * or with status {@code 500 (Internal Server Error)} if the query couldn't be updated.
     * @throws URISyntaxException if the Location URI syntax is incorrect.
     */
    @PatchMapping(value = "/queries/{id}", consumes = {"application/json", "application/merge-patch+json"})
    public ResponseEntity<Query> partialUpdateQuery(
        @PathVariable(value = "id", required = false) final Long id,
        @NotNull @RequestBody Query query
    ) throws URISyntaxException {
        log.debug("REST request to partial update Query partially : {}, {}", id, query);
        if (query.getId() == null) {
            throw new BadRequestAlertException("Invalid id", ENTITY_NAME, "idnull");
        }
        if (!Objects.equals(id, query.getId())) {
            throw new BadRequestAlertException("Invalid ID", ENTITY_NAME, "idinvalid");
        }

        if (!queryRepository.existsById(id)) {
            throw new BadRequestAlertException("Entity not found", ENTITY_NAME, "idnotfound");
        }

        Optional<Query> result = queryRepository
            .findById(query.getId())
            .map(existingQuery -> {
                if (query.getUserId() != null) {
                    existingQuery.setUserId(query.getUserId());
                }
                if (query.getName() != null) {
                    existingQuery.setName(query.getName());
                }
                if (query.getTypeQuery() != null) {
                    existingQuery.setTypeQuery(query.getTypeQuery());
                }
                if (query.getCompanyAddress() != null) {
                    existingQuery.setCompanyAddress(query.getCompanyAddress());
                }
                if (query.getJobRole() != null) {
                    existingQuery.setJobRole(query.getJobRole());
                }
                if (query.getAge() != null) {
                    existingQuery.setAge(query.getAge());
                }
                if (query.getSalary() != null) {
                    existingQuery.setSalary(query.getSalary());
                }
                if (query.getYearExperiences() != null) {
                    existingQuery.setYearExperiences(query.getYearExperiences());
                }
                if (query.getEducationLevel() != null) {
                    existingQuery.setEducationLevel(query.getEducationLevel());
                }
                if (query.getJobAttribute() != null) {
                    existingQuery.setJobAttribute(query.getJobAttribute());
                }
                if (query.getContact() != null) {
                    existingQuery.setContact(query.getContact());
                }
                if (query.getGroupBy() != null) {
                    existingQuery.setGroupBy(query.getGroupBy());
                }
                if (query.getSlideWindow() != null) {
                    existingQuery.setSlideWindow(query.getSlideWindow());
                }

                return existingQuery;
            })
            .map(queryRepository::save);

        return ResponseUtil.wrapOrNotFound(
            result,
            HeaderUtil.createEntityUpdateAlert(applicationName, false, ENTITY_NAME, query.getId().toString())
        );
    }

    /**
     * {@code GET  /queries} : get all the queries.
     *
     * @param pageable the pagination information.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and the list of queries in body.
     */
    @GetMapping("/queries")
    public ResponseEntity<List<Query>> getAllQueries(Pageable pageable) {
        log.debug("REST request to get a page of Queries");
        Page<Query> page = queryRepository.findAll(pageable);
        HttpHeaders headers = PaginationUtil.generatePaginationHttpHeaders(ServletUriComponentsBuilder.fromCurrentRequest(), page);
        return ResponseEntity.ok().headers(headers).body(page.getContent());
    }

    /**
     * {@code GET  /queries/:id} : get the "id" query.
     *
     * @param id the id of the query to retrieve.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and with body the query, or with status {@code 404 (Not Found)}.
     */
    @GetMapping("/queries/{id}")
    public ResponseEntity<Query> getQuery(@PathVariable Long id) {
        log.debug("REST request to get Query : {}", id);
        Optional<Query> query = queryRepository.findById(id);
        return ResponseUtil.wrapOrNotFound(query);
    }

    /**
     * {@code DELETE  /queries/:id} : delete the "id" query.
     *
     * @param id the id of the query to delete.
     * @return the {@link ResponseEntity} with status {@code 204 (NO_CONTENT)}.
     */
    @DeleteMapping("/queries/{id}")
    public ResponseEntity<Void> deleteQuery(@PathVariable Long id) {
        log.debug("REST request to delete Query : {}", id);
        queryRepository.deleteById(id);
        return ResponseEntity
            .noContent()
            .headers(HeaderUtil.createEntityDeletionAlert(applicationName, false, ENTITY_NAME, id.toString()))
            .build();
    }

    /**
     *
     */
    @GetMapping("/")
    public ResponseEntity<String> getDefault() {
        return new ResponseEntity<>("Hello from Yourway!", HttpStatus.OK);
    }

    @GetMapping("/query")
    public Iterable<Query> getAllQuery() {
        try {
            return queryRepository.findAll();
        } catch (java.lang.NullPointerException e) {
            return null;
        }
    }

    @GetMapping("/query/{userId}")
    public ResponseEntity<List<Query>> getQuery(@PathVariable(value = "userId") Integer userId) {
        try {
            List<Query> response = queryRepository.findAllByUserId(userId);
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
        Query mapQuery = Query.fromJson(query);

        // save to database
        Query newQuery = queryRepository.save(mapQuery);

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
        Query deleteQuery = queryRepository.findByQueryId(queryId);

        // send message delete to kafka
        temp.put(queryId, deleteQuery.toJson());
        data.put(userId, temp);
        Properties properties = UtilKafka.createProducer("KafkaProducer");
        UtilKafka.sendMessageToKafka(properties, Settings.TOPIC_SET_USER_QUERY, String.valueOf(userId), gson.toJson(data));

        // delete in database
        queryRepository.delete(deleteQuery);

        // return status
        Map<String, Boolean> response = new HashMap<>();
        response.put("deleted", Boolean.TRUE);
        return response;
    }
}
